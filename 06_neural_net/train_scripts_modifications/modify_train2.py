 # add N species trainability
    
    
def fit2(self, seqnn_model):
        
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

    ################################################################
    # prep

    # metrics
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

    if self.strategy is None:
      # generate decorated train steps
      @tf.function
      def train_step0(x, y):
        with tf.GradientTape() as tape:
          pred = seqnn_model.models[0](x, training=True)
          loss = self.loss_fn(y, pred) + sum(seqnn_model.models[0].losses)
        train_loss[0](loss)
        train_r[0](y, pred)
        train_r2[0](y, pred)
        gradients = tape.gradient(loss, seqnn_model.models[0].trainable_variables)
        self.optimizer.apply_gradients(zip(gradients, seqnn_model.models[0].trainable_variables))

      @tf.function
      def eval_step0(x, y):
        pred = seqnn_model.models[0](x, training=False)
        loss = self.loss_fn(y, pred) + sum(seqnn_model.models[0].losses)
        valid_loss[0](loss)
        valid_r[0](y, pred)
        valid_r2[0](y, pred)

      if self.num_datasets > 1:
        @tf.function
        def train_step1(x, y):
          with tf.GradientTape() as tape:
            pred = seqnn_model.models[1](x, training=True)
            loss = self.loss_fn(y, pred) + sum(seqnn_model.models[1].losses)
          train_loss[1](loss)
          train_r[1](y, pred)
          train_r2[1](y, pred)
          gradients = tape.gradient(loss, seqnn_model.models[1].trainable_variables)
          self.optimizer.apply_gradients(zip(gradients, seqnn_model.models[1].trainable_variables))

        @tf.function
        def eval_step1(x, y):
          pred = seqnn_model.models[1](x, training=False)
          loss = self.loss_fn(y, pred) + sum(seqnn_model.models[1].losses)
          valid_loss[1](loss)
          valid_r[1](y, pred)
          valid_r2[1](y, pred)
    else:
      def train_step0(x, y):
        with tf.GradientTape() as tape:
          pred = seqnn_model.models[0](x, training=True)
          loss_batch_len = self.loss_fn(y, pred)
          loss_batch = tf.reduce_mean(loss_batch_len, axis=-1)
          loss = tf.reduce_sum(loss_batch) / self.batch_size
          loss += sum(seqnn_model.models[0].losses) / self.num_gpu
        train_r[0](y, pred)
        train_r2[0](y, pred)
        gradients = tape.gradient(loss, seqnn_model.models[0].trainable_variables)
        self.optimizer.apply_gradients(zip(gradients, seqnn_model.models[0].trainable_variables))
        return loss

      @tf.function
      def train_step0_distr(xd, yd):
        replica_losses = self.strategy.run(train_step0, args=(xd, yd))
        loss = self.strategy.reduce(tf.distribute.ReduceOp.SUM,
                                    replica_losses, axis=None)
        train_loss[0](loss)

      def eval_step0(x, y):
        pred = seqnn_model.models[0](x, training=False)
        loss = self.loss_fn(y, pred) + sum(seqnn_model.models[0].losses)
        valid_loss[0](loss)
        valid_r[0](y, pred)
        valid_r2[0](y, pred)

      @tf.function
      def eval_step0_distr(xd, yd):
        return self.strategy.run(eval_step0, args=(xd, yd))

      if self.num_datasets > 1:
        def train_step1(x, y):
          with tf.GradientTape() as tape:
            pred = seqnn_model.models[1](x, training=True)
            loss_batch_len = self.loss_fn(y, pred)
            loss_batch = tf.reduce_mean(loss_batch_len, axis=-1)
            loss = tf.reduce_sum(loss_batch) / self.batch_size
            loss += sum(seqnn_model.models[1].losses) / self.num_gpu
          train_loss[1](loss)
          train_r[1](y, pred)
          train_r2[1](y, pred)
          gradients = tape.gradient(loss, seqnn_model.models[1].trainable_variables)
          self.optimizer.apply_gradients(zip(gradients, seqnn_model.models[1].trainable_variables))
          return loss

        @tf.function
        def train_step1_distr(xd, yd):
          replica_losses = self.strategy.run(train_step1, args=(xd, yd))
          loss = self.strategy.reduce(tf.distribute.ReduceOp.SUM,
                                      replica_losses, axis=None)
          train_loss[1](loss)

        def eval_step1(x, y):
          pred = seqnn_model.models[1](x, training=False)
          loss = self.loss_fn(y, pred) + sum(seqnn_model.models[1].losses)
          valid_loss[1](loss)
          valid_r[1](y, pred)
          valid_r2[1](y, pred)

        @tf.function
        def eval_step1_distr(xd, yd):
          return self.strategy.run(eval_step1, args=(xd, yd))

    # checkpoint manager
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

    ################################################################
    # training loop

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
          if self.strategy is None:
            if di == 0:
              train_step0(x, y)
            else:
              train_step1(x, y)
          else:
            if di == 0:
              train_step0_distr(x, y)
            else:
              train_step1_distr(x, y)
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
            if self.strategy is None:
              if di == 0:
                eval_step0(x, y)
              else:
                eval_step1(x, y)
            else:
              if di == 0:
                eval_step0_distr(x, y)
              else:
                eval_step1_distr(x, y)

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