
# Importing Packages
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import cm


def ploting(fx,bounds,step,plot_step):


    
    X = np.arange(bounds[0][0], bounds[0][1], plot_step)
    Y = np.arange(bounds[1][0], bounds[1][1], plot_step)
    X, Y = np.meshgrid(X, Y)
    Z=np.zeros_like(X)
    
    for i in range(len(X)):
       for j in range(len(Y)):
         matchig_pixcel_L,matchig_pixcel_L,z=fx([X[i,j],Y[i,j]],step)
         Z[i,j]=z
   
        
    # Plotting the Animation
    fig = plt.figure(figsize=(15, 7))
    ax1 = fig.add_subplot(121, projection='3d')
    mycmap = plt.get_cmap('gist_earth') 
    surf=ax1.plot_surface(X, Y, Z, cmap=mycmap,linewidth=0.01) 
   
    plt.colorbar(surf, shrink=0.5, aspect=5,ax=ax1)
    plt.show()
    
 