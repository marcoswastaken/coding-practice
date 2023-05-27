#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 25 18:42:13 2023

Disclaimer:
I am not claiming any credit for the work below.
This is just practice code thrown together as I learn, mostly from provided course notes or labs with minor modifications.
See the README for links to the associated courses and other info.

"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import copy
import math

# Import data to dataframe
housing_data = pd.read_csv('boston.csv', header=0)

# Set features aside from targets
X_train = housing_data[['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE',
                        'DIS', 'RAD', 'TAX', 'PTRATIO', 'B',
                        'LSTAT']].to_numpy()

# Set aside targets
y_train = housing_data['MEDV'].to_numpy()

# Set aside feature names
feature_names = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS',
                 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT']

# Plot the features vs. the target
fig,ax=plt.subplots(1, 13, figsize=(12, 3), sharey=True)
for i in range(len(ax)):
    ax[i].scatter(X_train[:,i],y_train)
    ax[i].set_xlabel(feature_names[i])
ax[0].set_ylabel("Price (1000's)")
plt.show()


# fig,ax=plt.subplots(3, 4, figsize=(12, 12), sharey=True)
# for i in range(len(ax)):
#     ax[i//3][i%4].scatter(X_train[:,i],y_train)
#     ax[i//3][i%4].set_xlabel(feature_names[i])
# ax[1][0].set_ylabel("Price (1000's)")
# plt.show()



# Define the cost function
def compute_cost(X, y, w, b):
    '''

    Parameters
    ----------
    X : (npumpy.ndarray, (m,n))
        An array containing the training data: m rows with n features
    y : (npumpy.ndarray, (m,1))
        An array containing the target values: m rows
    w : (npumpy.ndarray, (n,1))
        A model paremeter
        An array containing the weights for each feature
    b : (scalar)
        A model parameter
        The bias for the model
    Returns
    -------
    (scalar)
    The squared error cost of the given parameters, scaled by 1/2m

    '''

    m = X.shape[0]
    cost = 0.0

    for i in range(m):
        model_i = np.dot(w,X[i])+b   # output projected by model
        error_i = model_i - y[i]        # diff. between projection and target
        cost += error_i**2              # update cost by square of error

    return cost/(2*m)

# Define the gradient of the cost function
def compute_gradient(X, y, w, b):
    '''

    Parameters
    ----------
    X : (npumpy.ndarray, (m,n))
        An array containing the training data: m rows with n features
    y : (npumpy.ndarray, (m,))
        An array containing the target values: m rows
    w : (npumpy.ndarray, (n,))
        A model paremeter
        An array containing the weights for each feature
    b : (scalar)
        A model parameter
        The bias for the model
    Returns
    -------
    dj_dw : (numpy.ndarray, (n,))
        The derivative of the cost function with respect to w
    dj_db : (scalar)
        The derivative of the cost function with respect to b

    '''

    m, n = X.shape
    dj_dw = np.zeros((n,))
    dj_db = 0.0

    for i in range(m):
        model_i = np.dot(w,X[i])+b   # output projected by model
        error_i = model_i - y[i]        # diff. between projection and target

        for j in range(n):
            dj_dw[j] +=  error_i * X[i, j]

        dj_db += error_i

    return dj_dw/m , dj_db/m

# Perform a gradient descent algorithm
def gradient_descent(X, y, w_in, b_in, cost_function, gradient_function,
                     alpha, num_iters):
    '''

    Learn w and b parameteres using batch gradient descent

    Parameters
    ----------
    X : (npumpy.ndarray, (m,n))
        An array containing the training data: m rows with n features
    y : (npumpy.ndarray, (m,))
        An array containing the target values: m rows
    w_in : (npumpy.ndarray, (n,))
        An initial guess at the model paremeter w
        The weights for each feature
    b_in : (scalar)
        an initial guess for the model parameter b
        The bias for the model
    cost_function : (function)
        A cost function.
    gradient_function : (function)
        The gradient of the cost function.
    alpha : (float)
        The learning rate (step size).
    num_iters : (int)
        The number of itterations of the gradient descent algorithm
        to perform before returning the updated values for w and b.

    Returns
    -------
    w : (numpy.ndarray, (n,))
        The updated guess for w
    b : (scalar)
        The updated guess for b
    J_hist : (list)
        The history of cost at each itteration
    '''

    J_hist = [] # A place to keep track of the cost at each step
    w = copy.deepcopy(w_in) # Avoid modifying a global w within function
    b = b_in
    for i in range(num_iters):
        # Step 1: compute the gradient at the current w, b
        dj_dw, dj_db = gradient_function(X, y, w, b)

        # Step 2: Update the parameters in the direction of the gradient
        w -= alpha * dj_dw
        b -= alpha * dj_db

        # Step 3 (optional): Keep track of the cost at this itteration
        if i < 100000:
            J_hist.append(cost_function(X, y, w, b))

        # Step 4 (optional): Print the cost at intervals
        if i % math.ceil(num_iters / 10) == 0:
            print(f"Iteration {i:4d}: Cost {J_hist[-1]:8.4f}   ")

    return w, b, J_hist #return final w,b and J history for graphing

##
##  Testing the algorithm
##

# Normalize the feature values
mu     = np.mean(X_train,axis=0)
sigma  = np.std(X_train,axis=0)
X_mean = (X_train - mu)
X_norm = (X_train - mu)/sigma


m, n = X_train.shape

# Initialize the starting parameters
w_init = np.zeros(n)
b_init = 0


# Some gradient descent settings
iterations = 5000
alpha = 1.0e-2
# run gradient descent
w_final, b_final, J_hist = gradient_descent(X_norm, y_train, w_init,
                                            b_init, compute_cost,
                                            compute_gradient,
                                            alpha, iterations)
print(f"b,w found by gradient descent: {b_final:0.2f},{w_final} ")