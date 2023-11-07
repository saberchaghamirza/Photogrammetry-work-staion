# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 22:45:48 2023

@author: Saber
"""

import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
#from Function import collinearity_equation_for_Relative_orientation
import pandas as pd
from pandasql import sqldf
mysql = lambda q: sqldf(q, globals()) 

import cv2
    

    
Image_Path = {'left':r'D:\Projects\2.Term2\Digital_Photogrammetry\project1\main\data\21_60_.png',
              'right':r'D:\Projects\2.Term2\Digital_Photogrammetry\project1\main\data\22_60_.png'}
Fiducial_Mark_Path = {'left':r'D:\Projects\2.Term2\Digital_Photogrammetry\project1\main\data\Fiducial_Mark_On_Left_Image_readed.txt',
                      'right':r'D:\Projects\2.Term2\Digital_Photogrammetry\project1\main\data\Fiducial_Mark_On_Right_Image_readed.txt'}

Camera_Path=r"D:\Projects\2.Term2\Digital_Photogrammetry\project1\main\data\CAMERA.txt"


from InteriorOrientation import Interior_Orientation,Read_Camera
camera_name,focal_length,fiducial_coordinates,Camera_distortions=Read_Camera(Camera_Path)


ALL_Method=['Comformal','Afine','Projetive']
Method=ALL_Method[1]
Control__Point_list=[1,2,7,6,3,4,5,8]
Check__Point_list=[]
xy_obs_L = pd.read_csv(Fiducial_Mark_Path['left'],sep=" ",names=['number','point_x','point_y'])
xy_obs_R = pd.read_csv(Fiducial_Mark_Path['right'],sep=" ",names=['number','point_x','point_y'])

# Interior Orientation for left img:
Sensors_L=Interior_Orientation(Image_Path['left'])
Sensors_L.organize_point(xy_obs_L,Control__Point_list,Camera_Path)
Sensors_L.Mapping_Method(Method)
Sensors_L.Mapping_Method_to_picel()
pp_L=Sensors_L.Mapping_to_Pixcel(0,0)
xo=Sensors_L.Mapping_to_Pixcel(fiducial_coordinates.point_x,fiducial_coordinates.point_y)
xo=Sensors_L.Mapping_to_point(xy_obs_L.point_x,xy_obs_L.point_y)
print("rmse control points  on left sensor= " + str(Sensors_L.Rmse_Control)+'\n'+"rmse check  points on left sensor= "+str(Sensors_L.Rmse_Check))

# Interior Orientation for right img:
Sensors_R=Interior_Orientation(Image_Path['right'])
Sensors_R.organize_point(xy_obs_R,Control__Point_list,Camera_Path)
Sensors_R.Mapping_Method(Method)
Sensors_R.Mapping_Method_to_picel()
pp_R=Sensors_R.Mapping_to_Pixcel(0,0)

print("rmse control points  on right sensor= " + str(Sensors_R.Rmse_Control)+'\n'+"rmse check  points on right sensor= "+str(Sensors_R.Rmse_Check))

    
from plot_functions import ploting
#---------------------------------------------
# PART2 : RELTIVE ORINATION
from StreoImage import StreoImages
# PART 2 
Streo=StreoImages(Sensors_L,Sensors_R)
Streo.ExtractMatchedPoints(RatioTest=0.35)  
projective_matrix=Streo.Initialize_Relative_orientation_in_pp(focal_length,0.000001)
############ STREO
img = Streo.Sensors_R_New.copy()
img_L = Sensors_L.img
img_L[:,:,0]=img[:,:,1]
cv2.imshow('left',img_L)
#------------------------
# PART 5 VLL
Model_X_range=min(Streo.Relative_orientation.Geo.X),max(Streo.Relative_orientation.Geo.X)
Model_Y_range=min(Streo.Relative_orientation.Geo.Y),max(Streo.Relative_orientation.Geo.Y)
Model_Z_range=min(Streo.Relative_orientation.Geo.Z),max(Streo.Relative_orientation.Geo.Z)
step=int(Model_Z_range[1]-Model_Z_range[0])
matchig_pixcel_L,matchig_pixcel_L,Z=Streo.Initialize_VLL(Model_X_range[0]+50,Model_Y_range[0],step,)

plot_step=20

#Streo.ploting(3,plot_step,50)
# PART 3 TMPLATE MATCH for points in left findeing in right
#-----------------------------------------------------------------------------------------------------------


# All the 6 methods for comparison in a list
x,y=800.8,500.98
matchig_pixcel_L={'x':x,'y':y}
Shift=11
serech_domain_y= 10
serech_domain_x= 20
matchig_pixcel_R ,window_L,window_R=Streo.area_base_pixcel_matching(matchig_pixcel_L,Shift,serech_domain_y,serech_domain_x)
# # --------- showing:
# cv2.circle(window_R,(int(Shift),(int(Shift))), 1, (0,0,255), -1)
# cv2.imshow('match_R',window_R)
# cv2.circle(window_L, (int(Shift),int(Shift)), 1, (0,0,255), -1)
# cv2.imshow('match_L',window_L)

###------------------------------------------------------------------------------------------

# Window_Size=20
# L_img=Sensors_L.Gry
# R_img0=Sensors_R.Gry
# from StreoImage import  List_Squre
# window_L=L_img[int(matchig_pixcel_L['y']-1-Window_Size):int(matchig_pixcel_L['y']+Window_Size),int(matchig_pixcel_L['x']-1-Window_Size):int(matchig_pixcel_L['x']+Window_Size)]
# rows1, cols1 =R_img0.shape[:2]
# a1,a2,a3=1,0,0
# b1,b2,b3=0,1,0
# r0,r1=0,1
# affine_matrix=np.array([[a1,a2,a3],
#                        [b1,b2,b3]], dtype='f')
# window_R=R_img0[int(matchig_pixcel_R['y']-1-Window_Size-1):int(matchig_pixcel_R['y']+Window_Size+1),int(matchig_pixcel_R['x']-1-Window_Size-1):int(matchig_pixcel_R['x']+Window_Size+1)] 
# #R_img= cv2.warpAffine(R_img,affine_matrix, (cols1,rows1) ,flags=cv2.INTER_CUBIC) 
# cv2.imshow('INPUT_R',window_R)
# cv2.imshow('INPUT_L',window_L)
# print('*********************************************************')
# print('least Squre Matching:')

# dx=1
# i=1
# #while dx>10**-4:
# for iiiii in range(200):
#     projective_matrix_R=np.array([[a1,a2,a3],[b1,b2,b3],[0,0,1]], dtype='f')
#     shifted_image = R_img0.astype(np.int16) 
#     R_img0 = np.clip(shifted_image, 0, 255).astype(np.uint8)
#     R_img=cv2.warpPerspective(R_img0,projective_matrix_R, (cols1,rows1),flags=cv2.INTER_NEAREST )
#     window_R=R_img[int(matchig_pixcel_R['y']-1-Window_Size-1):int(matchig_pixcel_R['y']+Window_Size+1),int(matchig_pixcel_R['x']-1-Window_Size-1):int(matchig_pixcel_R['x']+Window_Size+1)] 
#     sobelx = cv2.Sobel(window_R,cv2.CV_64F,1,0,ksize=7)  # x ,
#     sobely = cv2.Sobel(window_R,cv2.CV_64F,0,1,ksize=7)  # y
#     sobelx=sobelx[1:-1,1:-1]
#     sobely=sobely[1:-1,1:-1]
#     window_R=window_R[1:-1,1:-1]
#     # ksize

#    # Using cv2.blur() method 

#     rows, cols=window_L.shape
#     f_s=np.average(window_L)
#     g_s=np.average(window_R)
#     L,A=[],[]
#     for y in range(rows):
#        for x in range(cols):
#             gx=float(sobelx[y,x])
#             gy=float(sobely[y,x])
#             g0=float(window_R[y,x])
#             f=float(window_L[y,x])
#             #g0=float(window_R_b[y,x])
#             #f= float(window_L_b[y,x])
#             A.append([gx*x,gx*y,gx,gy*x,gy*y,gy])
#             L.append(-f+g0)
            
#     X,v=List_Squre(A,L)     
#     a1=a1+X[0]
#     a2=a2+X[1]
#     a3=a3+X[2]
#     b1=b1+X[3]
#     b2=b2+X[4]
#     b3=b3+X[5]
#  #   r0=X[6]
#   #  r1=X[7]
    
#     #affine_matrix=np.array([[a1,a2,a3],[b1,b2,b3]], dtype='f')
#     #R_img=cv2.warpAffine(R_img,affine_matrix, (rows1,cols1),flags=cv2.INTER_NEAREST  )#flags=cv2.INTER_CUBIC
  

#     dx=max(X[:6])
#     print(str(dx))
    
#     i=i+1
# cv2.imshow(str(i),window_R) 
# cv2.imshow('r',R_img)  