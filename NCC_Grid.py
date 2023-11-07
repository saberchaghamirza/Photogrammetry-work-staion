# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 07:07:04 2023

@author: Saber
"""

import cv2
import numpy as np
import pandas  as pd 
def area_base_pixcel_matching_full_image(Sensors_L,Sensors_R,matchig_pixcel_L,Shift,method):
   
    Sensors_R = Sensors_R.img.copy()
    window_L=Sensors_L.img[int(matchig_pixcel_L['y']-Shift-1):int(matchig_pixcel_L['y']+Shift),int(matchig_pixcel_L['x']-Shift-1):int(matchig_pixcel_L['x']+Shift)]
    matchig_pixcel_R=matchig_pixcel_L.copy()
    
    res = cv2.matchTemplate(Sensors_R,window_L,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
     top_left = min_loc
    else:
     top_left = max_loc
    matchig_pixcel_R = {'x':top_left[0] + Shift+1,'y': top_left[1] + Shift+1}
    window_R=Sensors_R[int(matchig_pixcel_R['y']-Shift-1):int(matchig_pixcel_R['y']+Shift),int(matchig_pixcel_R['x']-Shift-1):int(matchig_pixcel_R['x']+Shift)] 
    return matchig_pixcel_R,window_R



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
     method= cv2.TM_CCOEFF_NORMED
     Window_Size=10
     
     x=100
     step=20
     rows, cols =Sensors_L.Gry.shape
     if rows>x:
         X = np.arange(x    ,cols , step)
         Y = np.arange(2*Window_Size ,rows , step)
         Pt_L=[]
         Pt_R=[]
         for i in X:
             for j in Y:
                 matchig_pixcel_L={'x': i, 'y': j}
                 matchig_pixcel_R,window_R=area_base_pixcel_matching_full_image(Sensors_L,Sensors_R,matchig_pixcel_L,Window_Size,method)
                 Pt_L.append([matchig_pixcel_L['x'],matchig_pixcel_L['y']])
                 Pt_R.append([matchig_pixcel_R['x'],matchig_pixcel_R['y']])
         NCC_matchig_pixcel_L=pd.DataFrame({'x':np.array(Pt_L)[:,0],'y':np.array(Pt_L)[:,1]})
         NCC_matchig_pixcel_R=pd.DataFrame({'x':np.array(Pt_R)[:,0],'y':np.array(Pt_R)[:,1]})
