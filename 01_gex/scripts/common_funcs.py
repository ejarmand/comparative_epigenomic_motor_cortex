# commonly used functions 

import numpy as np
import pandas as pd
def save_list(outfile, listlike):
    '''
    writes a file as a newline seperated list, useful for gsea, or storing information in general
    
    args:
        outfile : a file path to write a list of genes
        listline : an interatable object like a python list, or a numpy array
    
    '''
    return open(outfile, 'w').write(''.join([i + '\n' for i in listlike]))

def read_list(listfile):
    '''
    reads a newline separated list like created by save_list
    args:
        listfile: path to a textfile containing a newline separated list
    returns:
        a list of strings saved in the list file
    '''
    return open(listfile, 'r').read().strip('\n').split('\n')

def list_intersection(to_intersect):
    '''
    get elements in the intersection of a group of lists/arrays
    
    args:
        to_intersect : a list of lists or other listlike objects
    returns:
        common : a numpy array of all elements common in all lists
    
    '''
    common = to_intersect[0]
    for item in to_intersect[1:]:
        common = np.intersect1d(common, item)
    return common

def common_index(a, b):
    '''
    finds the common indicies between two pandas dataframes
    
    args:
        a: a pandas dataframe  with some indecies in common w/ b
        b: a pandas dataframe with some indecies in common w/ a
    returns:
        a_prime : the dataframe a indexed by common elements with a
        b_prime : the dataframe b indexed by common elements with b
    '''
    a_prime = a.loc[a.index.isin(b.index)]
    b_prime = b.loc[a_prime.index]
    return a_prime, b_prime

def my_element_entropy(x):
    '''
    gets the entropy associated with a single probability
    
    args:
        x: a probability value ranging from 0 to 1
    '''
    if x==0 or x == np.NAN:
        return x
    return x*np.log2(x)
    

def my_gene_entropy(df, norm=False):
    '''
    Adatapted from BioQC entropy specificity, 
    
    @references   Martinez and Reyes-Valdes (2008) Defining diversity, 
    specialization, and gene specificity in transcriptomes through information 
    theory. PNAS 105(28):9709--9714
    
    args:
        df: a pandas dataframe with genes/genomic features as rows and 
        celltypes/conditions/tissues as columns
        norm: wether to normalize the output to be from 0 to 1. If false
            output will range from 0 to log2(the number of input columns)
    returns:
        specificity : a pandas series where each index is a genomic feature
        and the value found at that index represents the specificity
        of that genes activity across rows.
        
        
    '''
    df = df.div(df.sum(axis=0))
    df = df.div(df.mean(axis=1), axis=0)
    # get entropy
    df = df.applymap(my_element_entropy)
    specificity = df.mean(axis=1)
    if norm:
        return specificity/np.log2(df.shape[1])
    return specificity
    
def my_tissue_entropy(df):
    '''
    Adapted from  
    @references   Martinez and Reyes-Valdes (2008) Defining diversity, 
    specialization, and gene specificity in transcriptomes through information 
    theory. PNAS 105(28):9709--9714
    (I read the paper to make sure that I didn't copy an incorrect implementation
    from bioqc, it turns out the rest of the paper represents a relevant way
    to identify the conservation of tissue/cell type level programs across 
    species)
    
    Gets the entropy per gene per tissue among the matrix. 
    
    
    
    '''
    return
        
def my_tissued_divergence(df):
    '''
    Adapted from  
    @references   Martinez and Reyes-Valdes (2008) Defining diversity, 
    specialization, and gene specificity in transcriptomes through information 
    theory. PNAS 105(28):9709--9714
     
    Gets the KL divergence between tissues/conditions. 
    
    
    
    
    
    '''    
        
    return