 # add N species trainability
    
def fit3(self, seqnn_model):
    if not self.compiled:
      self.compile(seqnn_model)

    assert(len(seqnn_model.models) >= self.num_datasets)

    # inform optimizer about all trainable variables (v2.11-)
    vars_set = set()
    trainable_vars = []
    for di in range(self.num_datasets):
      for v in seqnn_model.models[di].trainable_variables:
        if v.name not in vars_set:
          vars_set.add(v.name)
          trainable_vars.append(v)
    try:
      self.optimizer.build(trainable_vars)
    except AttributeError:
      pass

#############################################################################
# set up metrics
#############################################################################
    train_loss, train_r, train_r2 = [], [], []
    valid_loss, valid_r, valid_r2 = [], [], []
    for di in range(self.num_datasets):
      num_targets = seqnn_model.models[di].output_shape[-1]
      train_loss.append(tf.keras.metrics.Mean(name='train%d_loss'%di))
      train_r.append(metrics.PearsonR(num_targets, name='train%d_r'%di))
      train_r2.append(metrics.R2(num_targets, name='train%d_r2'%di))
      valid_loss.append(tf.keras.metrics.Mean(name='valid%d_loss'%di))
      valid_r.append(metrics.PearsonR(num_targets, name='valid%d_r'%di))
      valid_r2.append(metrics.R2(num_targets, name='valid%d_r2'%di))    

#############################################################################
# set up single GPU training
#############################################################################
    
    if self.strategy is None:
        # training functions for no strategy
        def generate_training_function(idx=idx):
            @tf.function
            def train_step(x, y):
                with tf.GradientTape() as tape:
                    pred = seqnn_model.models[idx](x, training=True)
                    loss = self.loss_fn(y,pred) + sum(seqnn_model.models[idx].losses)
                train_loss[idx](loss)
                train_r[idx](y, pred)
                train_r2[idx](y, pred)

                gradients = tape.gradient(loss, seqnn_model.models[idx].trainable_variables)
                self.optimizer.apply_gradients(zip(gradients, seqnn_model.models[idx].trainable_variables))

            return train_step
        def generate_eval_step(idx=idx):
            @tf.function
            def eval_step(x, y):
                pred = seqnn_models.models[idx](x, training=False)
                loss = self.loss_fn(y, pred) + sum(seqnn_model.models[idx].losses)
                valid_loss[idx](loss)
                valid_r[idx](y, pred)
                valid_r2[idx](y, pred)

            return eval_step
        train_steps = []
        eval_steps = []
        for i in range(self.num_datsets):
            train_steps.append(generate_training_function(idx=i))
            eval_steps.append(generate_eval_function(idx=i))
        
        
#############################################################################
# set up distributed training
#############################################################################


    else:

    def generate_distruted_training_function(idx=idx):
        @tf.function
        def distr_train_step(xd, yd):
            def train_step(x, y):
                with tf.GradientTape() as tape:
                    pred = seqnn_model.models[idx](x, training=True)
                    loss_batch_len = self.loss_fn(y, pred)
                    loss_batch = tf.reduce_mean(loss_batch_len, axis=-1)
                    loss = tf.reduce_sum(loss_batch) / self.batch_size
                    loss += sum(seqnn_model.models[idx].losses) / self.num_gpu
                train_r[idx](y, pred)
                train_r2[idx](y, pred)

                gradients = tape.gradient(loss, seqnn_model.models[idx].trainable_variables)
                self.optimizer.apply_gradients(zip(gradients, seqnn_model.models[idx].trainable_variables))
                return loss

            # define replication

            replica_losses = self.strategy.run(train_step1, args=(xd, yd))
            loss = self.strategy.reduce(tf.distribute.ReduceOp.SUM,
                                  replica_losses, axis=None)
            train_loss[idx](loss)
        return distr_train_step
        
    def generate_distruted_eval_function(idx):
        @tf.function
        def eval_step_distr(xd, yd):
            def eval_step(x, y):
                pred = seqnn_model.models[idx](x, training=False)
                loss = self.loss_fn(y, pred) + sum(seqnn_model.models[idx].losses)
                valid_loss[idx](loss)
                valid_r[idx](y, pred)
                valid_r2[idx](y, pred)
        
            return self.strategy.run(eval_step, args=(xd, yd))
        return eval_step_distr
    
    train_steps = []
    eval_steps = []
    for i in range(self.num_datsets):
        train_steps.append(generate_distruted_training_function(idx=i))
        eval_steps.append(generate_distruted_eval_function(idx=i))

#############################################################################
# set up checkpoint managers
#############################################################################

    managers = []
    for di in range(self.num_datasets):
      ckpt = tf.train.Checkpoint(model=seqnn_model.models[di], optimizer=self.optimizer)
      ckpt_dir = '%s/model%d' % (self.out_dir, di)
      manager = tf.train.CheckpointManager(ckpt, ckpt_dir, max_to_keep=1)
      if manager.latest_checkpoint:
        ckpt.restore(manager.latest_checkpoint)
        ckpt_end = 5+manager.latest_checkpoint.find('ckpt-')
        epoch_start = int(manager.latest_checkpoint[ckpt_end:])
        if self.strategy is None:
          opt_iters = self.optimizer.iterations
        else:
          opt_iters = self.optimizer.iterations.values[0]
        print('Checkpoint restored at epoch %d, optimizer iteration %d.' % \
            (epoch_start, opt_iters))
      else:
        print('No checkpoints found.')
        epoch_start = 0
      managers.append(manager)

    # improvement variables
    valid_best = [-np.inf]*self.num_datasets
    unimproved = [0]*self.num_datasets

#############################################################################
# train
#############################################################################

    first_step = True
    for ei in range(epoch_start, self.train_epochs_max):
      if ei >= self.train_epochs_min and np.min(unimproved) > self.patience:
        break
      else:
        # shuffle datasets
        np.random.shuffle(self.dataset_indexes)

        # get iterators
        train_data_iters = [iter(td.dataset) for td in self.train_data]

        # train
        t0 = time.time()
        for di in self.dataset_indexes:
          x, y = safe_next(train_data_iters[di])
          train_steps[di](x, y)
            
          if first_step:
            print('Successful first step!', flush=True)
            first_step = False
            
        print('Epoch %d - %ds' % (ei, (time.time()-t0)))
        for di in range(self.num_datasets):
          print('  Data %d' % di, end='')
          model = seqnn_model.models[di]          

          # print training accuracy
          print(' - train_loss: %.4f' % train_loss[di].result().numpy(), end='')
          print(' - train_r: %.4f' %  train_r[di].result().numpy(), end='')
          print(' - train_r: %.4f' %  train_r2[di].result().numpy(), end='')

          # evaluate
          for x, y in self.eval_data[di].dataset:
            eval_steps[di](x, y)

          # print validation accuracy
          print(' - valid_loss: %.4f' % valid_loss[di].result().numpy(), end='')
          print(' - valid_r: %.4f' % valid_r[di].result().numpy(), end='')
          print(' - valid_r2: %.4f' % valid_r2[di].result().numpy(), end='')
          early_stop_stat = valid_r[di].result().numpy()

          # checkpoint
          managers[di].save()
          model.save('%s/model%d_check.h5' % (self.out_dir, di),
                     include_optimizer=False)

          # check best
          if early_stop_stat > valid_best[di]:
            print(' - best!', end='')
            unimproved[di] = 0
            valid_best[di] = early_stop_stat
            model.save('%s/model%d_best.h5' % (self.out_dir, di),
                       include_optimizer=False)
          else:
            unimproved[di] += 1
          print('', flush=True)

          # reset metrics
          train_loss[di].reset_states()
          train_r[di].reset_states()
          train_r2[di].reset_states()
          valid_loss[di].reset_states()
          valid_r[di].reset_states()
          valid_r2[di].reset_states()