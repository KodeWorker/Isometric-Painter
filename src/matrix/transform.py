import numpy as np

def PerspectiveProjection(r_gamma, r_beta, r_alpha):
    gamma, beta, alpha = -r_gamma*np.pi/180, -r_beta*np.pi/180, -r_alpha*np.pi/180

    R = np.array([[np.cos(beta)*np.cos(gamma), np.cos(beta)*np.sin(gamma), -np.sin(beta)],
                  [np.sin(alpha)*np.sin(beta)*np.cos(gamma)-np.cos(alpha)*np.sin(gamma), np.sin(alpha)*np.sin(beta)*np.sin(gamma)+np.cos(alpha)*np.cos(gamma), np.sin(alpha)*np.cos(beta)],
                  [np.cos(alpha)*np.sin(beta)*np.cos(gamma)+np.sin(alpha)*np.sin(gamma), np.cos(alpha)*np.sin(beta)*np.sin(gamma)-np.sin(alpha)*np.cos(gamma), np.cos(alpha)*np.cos(beta)]])
    return R
