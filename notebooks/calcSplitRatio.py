## Written by Katherine S. Geist, PhD
## Merrimack College, Massachusetts
## Please do not distribute without attribution
## https://github.com/ksgeist

import sys

## Check if packages are loaded; if not, import them
if 'numpy' not in sys.modules:
    import numpy as np
if 'pandas' not in sys.modules:
    import pandas as pd


def calcSplitRatio(df, p=None):
    """
    Calculate the ideal split ratio for training and testing sets.
    
    Parameters:
    p (int): The number of parameters (optional). If not provided, defaults to 
    the number of columns minus 1 (assuming the last column is the target).
    
    df (DataFrame): The DataFrame that will be used for analysis.
    
    Returns:
    float: The training set proportion.
    """
    ## Set p to the number of predictors if not provided
    if p is None:
        p = df.shape[1] - 1  ## The number of features (predictors), 
                             ## assuming last column is target
    
    ## Calculate ideal number for testing set
    test_N = (1 / np.sqrt(p)) * len(df)
    
    ## Calculate testing proportion
    test_prop = round(test_N / len(df), 2)
    
    ## Calculate training proportion
    train_prop = 1 - test_prop
    
    ## Print the results
    print(f"The ideal split ratio is {train_prop}:{test_prop} training:testing")
    
    ## Return the size of the training set proportion
    return train_prop
