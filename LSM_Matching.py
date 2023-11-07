# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 01:15:36 2023

@author: Saber
"""
import matplotlib.pyplot as plt
import math
from StreoImage import  List_Squre
import numpy as np
import cv2

def LSM_geo_radio(Window_Size,Max_iteration,Sensors_L,Sensors_R,matchig_pixcel_L,matchig_pixcel_R,plot_interval,K):
      
    L_img=Sensors_L.Gry
    R_img0=Sensors_R.Gry
    
    window_L=L_img[int(matchig_pixcel_L['y']-1-Window_Size):int(matchig_pixcel_L['y']+Window_Size),int(matchig_pixcel_L['x']-1-Window_Size):int(matchig_pixcel_L['x']+Window_Size)]
    window_R0=R_img0[int(matchig_pixcel_R['y']-1-Window_Size):int(matchig_pixcel_R['y']+Window_Size),int(matchig_pixcel_R['x']-1-Window_Size):int(matchig_pixcel_R['x']+Window_Size)]
    rows1, cols1 =R_img0.shape[:2]
    a1,a2,a3=1,0,0
    b1,b2,b3=0,1,0
    r0,r1=0,1
    affine_matrix=np.array([[a1,a2,a3],
                           [b1,b2,b3]], dtype='f')


    print('*********************************************************')
    print('least Squre Matching:')
    window_list=[]
    i=1
    R_img=R_img0
    #while dx>10**-4:
    for counter in range(Max_iteration):
        affine_matrix=np.array([[a1,a2,a3],[b1,b2,b3]], dtype='f')
        # Apply shift and scale to the gray values
        shifted_scaled_image = (R_img0.astype(np.float32) + r0) * r1
        
        # Clip the values to ensure they stay within the valid range
        shifted_scaled_image = np.clip(shifted_scaled_image, 0, 255).astype(np.uint8)

        R_img=cv2.warpAffine(shifted_scaled_image,affine_matrix, (rows1,cols1),flags=cv2.INTER_NEAREST  )#flags=cv2.INTER_CUBIC
        window_R=R_img[int(matchig_pixcel_R['y']-K-Window_Size-1):int(matchig_pixcel_R['y']+Window_Size+K),int(matchig_pixcel_R['x']-K-Window_Size-1):int(matchig_pixcel_R['x']+Window_Size+K)] 
        sobelx = cv2.Sobel(window_R,cv2.CV_64F,1,0,ksize=K)  # x ,
        sobely = cv2.Sobel(window_R,cv2.CV_64F,0,1,ksize=K)  # y
        # resize the widow after sobel 
        sobelx=sobelx[K:-K,K:-K]
        sobely=sobely[K:-K,K:-K]
        window_R=window_R[K:-K,K:-K]

        rows, cols=window_L.shape
      #  f_s=np.average(window_L)
      #  g_s=np.average(window_R)
        L,A=[],[]
        for y in range(rows):
           for x in range(cols):
                gx=float(sobelx[y,x])
                gy=float(sobely[y,x])
                g0=float(window_R[y,x])
                f=float(window_L[y,x])
                A.append([gx*x,gx*y,gx,gy*x,gy*y,gy,-1,g0])
                L.append(-f+g0)
                
        X,v=List_Squre(A,L)  
        a1=a1+X[0]
        a2=a2+X[1]
        a3=a3+X[2]
        b1=b1+X[3]
        b2=b2+X[4]
        b3=b3+X[5]
        r0=X[6]
      #  r1=X[7]
        if counter % plot_interval == 0:
            window_list.append(window_R)
#############################################################################
 # Plot
    print()
    print(window_L.shape)
    print(window_R.shape)
    n=(int(math.sqrt(Max_iteration/plot_interval)+1))
    plt.figure(figsize=(10,10)) # specifying the overall grid size
    plt.subplot(n,n,1)
    plt.imshow(window_L,'gray')
    plt.title(str('window_L'))
    plt.subplot(n,n,2)
    plt.imshow(window_R0,'gray')
    plt.title(str('window_R'))
    
    for i in range(len(window_list)):
        plt.subplot(n,n,i+3)    # the number of images in the grid is 5*5 (25)
        plt.imshow(window_list[i],'gray')
        plt.title(str((i+1)*plot_interval))
        plt.xticks([])
        plt.yticks([])

    plt.show()
    point_matrix=np.array([[matchig_pixcel_R['x']],[matchig_pixcel_R['y']],[-1]], dtype='f')
    new_point=affine_matrix.dot(point_matrix)
    matchig_pixcel_new={'x':new_point[0],'y':new_point[1]}
    return matchig_pixcel_new,affine_matrix




class ImageMatching:
    
    def __init__(self,ImagePath):
          self.img = cv2.imread(ImagePath)
          self.Gry =(cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY))

if __name__=='__main__':

     
     Image_Path = {'left':r'D:\Projects\2.Term2\Digital_Photogrammetry\project3\ted_L.png',
                   'right':r'D:\Projects\2.Term2\Digital_Photogrammetry\project3\ted_R.png'}
     matchig_pixcel_L={'x': 210, 'y': 211}
     matchig_pixcel_R={'x': 195, 'y': 211}
     
     Sensors_L=ImageMatching(Image_Path['left'])
     Sensors_R=ImageMatching(Image_Path['right'])
     Max_iteration=500
     Window_Size=20
     plot_interval=20
     K=7
     matchig_pixcel_new,affine_matrix=LSM_geo_radio(Window_Size,Max_iteration,Sensors_L,Sensors_R,matchig_pixcel_L,matchig_pixcel_R,plot_interval,K)
     print(matchig_pixcel_new)







    
def LSM_Full_Geometry(Window_Size,Max_iteration,Sensors_L,Sensors_R,matchig_pixcel_L,matchig_pixcel_R,plot_interval,K):
      
    L_img=Sensors_L.Gry
    R_img0=Sensors_R.Gry
    
    window_L=L_img[int(matchig_pixcel_L['y']-1-Window_Size):int(matchig_pixcel_L['y']+Window_Size),int(matchig_pixcel_L['x']-1-Window_Size):int(matchig_pixcel_L['x']+Window_Size)]
    window_R0=R_img0[int(matchig_pixcel_R['y']-1-Window_Size):int(matchig_pixcel_R['y']+Window_Size),int(matchig_pixcel_R['x']-1-Window_Size):int(matchig_pixcel_R['x']+Window_Size)]
    rows1, cols1 =R_img0.shape[:2]
    a1,a2,a3=1,0,0
    b1,b2,b3=0,1,0
    r0,r1=0,1
    affine_matrix=np.array([[a1,a2,a3],
                           [b1,b2,b3]], dtype='f')


    print('*********************************************************')
    print('least Squre Matching:')
    window_list=[]
    dx=1
    i=1
    R_img=R_img0
    #while dx>10**-4:
    for counter in range(Max_iteration):
        affine_matrix=np.array([[a1,a2,a3],[b1,b2,b3]], dtype='f')
        R_img=cv2.warpAffine(R_img0,affine_matrix, (rows1,cols1),flags=cv2.INTER_NEAREST  )#flags=cv2.INTER_CUBIC
        window_R=R_img[int(matchig_pixcel_R['y']-K-Window_Size-1):int(matchig_pixcel_R['y']+Window_Size+K),int(matchig_pixcel_R['x']-K-Window_Size-1):int(matchig_pixcel_R['x']+Window_Size+K)] 
        sobelx = cv2.Sobel(window_R,cv2.CV_64F,1,0,ksize=K)  # x ,
        sobely = cv2.Sobel(window_R,cv2.CV_64F,0,1,ksize=K)  # y
        # resize the widow after sobel 
        sobelx=sobelx[K:-K,K:-K]
        sobely=sobely[K:-K,K:-K]
        window_R=window_R[K:-K,K:-K]

        rows, cols=window_L.shape
        f_s=np.average(window_L)
        g_s=np.average(window_R)
        L,A=[],[]
        for y in range(rows):
           for x in range(cols):
                gx=float(sobelx[y,x])
                gy=float(sobely[y,x])
                g0=float(window_R[y,x])
                f=float(window_L[y,x])
                A.append([gx*x,gx*y,gx,gy*x,gy*y,gy])
                L.append(-f+g0)
                
        X,v=List_Squre(A,L)  
        a1=a1+X[0]
        a2=a2+X[1]
        a3=a3+X[2]
        b1=b1+X[3]
        b2=b2+X[4]
        b3=b3+X[5]
        if counter % plot_interval == 0:
            window_list.append(window_R)
#############################################################################
 # Plot
    print()
    print(window_L.shape)
    print(window_R.shape)
    n=(int(math.sqrt(Max_iteration/plot_interval)+1))
    plt.figure(figsize=(10,10)) # specifying the overall grid size
    plt.subplot(n,n,1)
    plt.imshow(window_L,'gray')
    plt.title(str('window_L'))
    plt.subplot(n,n,2)
    plt.imshow(window_R0,'gray')
    plt.title(str('window_R'))
    
    for i in range(len(window_list)):
        plt.subplot(n,n,i+3)    # the number of images in the grid is 5*5 (25)
        plt.imshow(window_list[i],'gray')
        plt.title(str((i+1)*plot_interval))
        plt.xticks([])
        plt.yticks([])

    plt.show()
    point_matrix=np.array([[matchig_pixcel_R['x']],[matchig_pixcel_R['y']],[-1]], dtype='f')
    new_point=affine_matrix.dot(point_matrix)
    matchig_pixcel_new={'x':new_point[0],'y':new_point[1]}
    return matchig_pixcel_new,affine_matrix
    
def LSM_s_r(Window_Size,Max_iteration,Sensors_L,Sensors_R,matchig_pixcel_L,matchig_pixcel_R,plot_interval,K):
    
    L_img=Sensors_L.Gry
    R_img0=Sensors_R.Gry
    
    window_L=L_img[int(matchig_pixcel_L['y']-1-Window_Size):int(matchig_pixcel_L['y']+Window_Size),int(matchig_pixcel_L['x']-1-Window_Size):int(matchig_pixcel_L['x']+Window_Size)]
    window_R0=R_img0[int(matchig_pixcel_R['y']-1-Window_Size):int(matchig_pixcel_R['y']+Window_Size),int(matchig_pixcel_R['x']-1-Window_Size):int(matchig_pixcel_R['x']+Window_Size)]
    rows1, cols1 =R_img0.shape[:2]
    a1,a2,a3=1,0,0
    b1,b2,b3=0,1,0
    r0,r1=0,1
    affine_matrix=np.array([[a1,a2,a3],
                           [b1,b2,b3]], dtype='f')


    print('*********************************************************')
    print('least Squre Matching:')
    window_list=[]
    dx=1
    i=1
    R_img=R_img0
    #while dx>10**-4:
    for counter in range(Max_iteration):
        affine_matrix=np.array([[a1,a2,a3],[b1,b2,b3]], dtype='f')
        R_img=cv2.warpAffine(R_img0,affine_matrix, (rows1,cols1),flags=cv2.INTER_NEAREST  )#flags=cv2.INTER_CUBIC
        window_R=R_img[int(matchig_pixcel_R['y']-K-Window_Size-1):int(matchig_pixcel_R['y']+Window_Size+K),int(matchig_pixcel_R['x']-K-Window_Size-1):int(matchig_pixcel_R['x']+Window_Size+K)] 
        sobelx = cv2.Sobel(window_R,cv2.CV_64F,1,0,ksize=K)  # x ,
        sobely = cv2.Sobel(window_R,cv2.CV_64F,0,1,ksize=K)  # y
        # resize the widow after sobel 
        sobelx=sobelx[K:-K,K:-K]
        sobely=sobely[K:-K,K:-K]
        window_R=window_R[K:-K,K:-K]

        rows, cols=window_L.shape
        f_s=np.average(window_L)
        g_s=np.average(window_R)
        L,A=[],[]
        for y in range(rows):
           for x in range(cols):
                gx=float(sobelx[y,x])
                gy=float(sobely[y,x])
                g0=float(window_R[y,x])
                f=float(window_L[y,x])
                A.append([-gx,-gy])
                L.append(f-g0)
                
        X,v=List_Squre(A,L)     
        a3=a3+X[0]
        b3=b3+X[1]
        if counter % plot_interval == 0:
            window_list.append(window_R)
#############################################################################
 # Plot
    print(window_L.shape)
    print(window_R.shape)
    n=(int(math.sqrt(Max_iteration/plot_interval)+1))
    plt.figure(figsize=(10,10)) # specifying the overall grid size
    plt.subplot(n,n,1)
    plt.imshow(window_L,'gray')
    plt.title(str('window_L'))
    plt.subplot(n,n,2)
    plt.imshow(window_R0,'gray')
    plt.title(str('window_R'))
    
    for i in range(len(window_list)):
        plt.subplot(n,n,i+3)    # the number of images in the grid is 5*5 (25)
        plt.imshow(window_list[i],'gray')
        plt.title(str((i+1)*plot_interval))
        plt.xticks([])
        plt.yticks([])

    plt.show()
    point_matrix=np.array([[matchig_pixcel_R['x']],[matchig_pixcel_R['y']],[-1]], dtype='f')
    new_point=affine_matrix.dot(point_matrix)
    matchig_pixcel_new={'x':new_point[0],'y':new_point[1]}
    return matchig_pixcel_new,affine_matrix 
    
    
    
  