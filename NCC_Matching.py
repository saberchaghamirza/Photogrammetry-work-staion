# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 18:21:40 2023

@author: Saber
"""
import cv2
import numpy as np
def area_base_pixcel_matching(Sensors_L,Sensors_R,matchig_pixcel_L,Shift,serech_domain_y,serech_domain_x):
    Sensors_R = Sensors_R.img.copy()
    window_L=Sensors_L.Gry[int(matchig_pixcel_L['y']-Shift-1):int(matchig_pixcel_L['y']+Shift),int(matchig_pixcel_L['x']-Shift-1):int(matchig_pixcel_L['x']+Shift)]
    matchig_pixcel_R=matchig_pixcel_L.copy()
    MaxCorrelation=0
    serech_domain_y= np.arange(-serech_domain_y, serech_domain_y, 1, dtype=int)
    serech_domain_x= np.arange(-serech_domain_x, serech_domain_x, 1, dtype=int)
    for i in serech_domain_y:
        for j in serech_domain_x:
            window_R=Sensors_R.Gry[int(matchig_pixcel_R['y']-Shift-1+i):int(matchig_pixcel_R['y']+Shift+i),int(matchig_pixcel_R['x']-Shift-1+j):int(matchig_pixcel_R['x']+Shift+j)]   
            Correlation = cv2.matchTemplate(window_L, window_R, cv2.TM_CCORR_NORMED)[0][0]
            if MaxCorrelation<Correlation:
                MaxCorrelation=Correlation
                ii,jj=i,j
    matchig_pixcel_R['x']=matchig_pixcel_R['x']+jj
    matchig_pixcel_R['y']=matchig_pixcel_R['y']+ii
    window_R=Sensors_R.img[int(matchig_pixcel_R['y']-Shift-1):int(matchig_pixcel_R['y']+Shift),int(matchig_pixcel_R['x']-Shift-1):int(matchig_pixcel_R['x']+Shift)] 
    return matchig_pixcel_R,window_R



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



def area_base_pixcel_matching_by_sererchAREA(Sensors_L,Sensors_R0,matchig_pixcel_L,Shift,serech_domain_y,serech_domain_x,method):
    
   
    Sensors_R = Sensors_R0.img.copy()
    rows, cols=Sensors_R0.Gry.shape
    dy2=min(serech_domain_y,rows)
    dx2=min(serech_domain_x,cols)
    Sensors_R = Sensors_R[int(matchig_pixcel_L['y']-serech_domain_y):int(matchig_pixcel_L['y']+dy2),int(matchig_pixcel_L['x']-serech_domain_x):int(matchig_pixcel_L['x']+dx2)] 
    window_L=Sensors_L.img[int(matchig_pixcel_L['y']-Shift-1):int(matchig_pixcel_L['y']+Shift),int(matchig_pixcel_L['x']-Shift-1):int(matchig_pixcel_L['x']+Shift)]

    
    res = cv2.matchTemplate(Sensors_R,window_L,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
     top_left = min_loc
    else:
     top_left = max_loc
    

    matchig_pixcel_R = {'x':(matchig_pixcel_L['x']-serech_domain_x+(top_left[0] +Shift+1)),'y': matchig_pixcel_L['y']-serech_domain_y+(top_left[1] + Shift+1)}
    window_R=Sensors_R[int(matchig_pixcel_R['y']-Shift-1):int(matchig_pixcel_R['y']+Shift),int(matchig_pixcel_R['x']-Shift-1):int(matchig_pixcel_R['x']+Shift)] 

    return matchig_pixcel_R,window_R
    



class ImageMatching:
    
    def __init__(self,ImagePath):
          self.img = cv2.imread(ImagePath)
          self.Gry =(cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY))


#if __name__=='__main__':
 #    print('hi')
 #    Image_Path = {'left':r'D:\Projects\2.Term2\Digital_Photogrammetry\project3\ted_L.png',
 #                  'right':r'D:\Projects\2.Term2\Digital_Photogrammetry\project3\ted_R.png'}
 #    Sensors_L=ImageMatching(Image_Path['left'])
 #    Sensors_R=ImageMatching(Image_Path['right'])
 #    Shift=5
 #    shiftL,shiftR=25,25
 #    matchig_pixcel_L={'x': 380.8, 'y': 190.98}
 #    matchig_pixcel_R=matchig_pixcel_L.copy()
 # #   matchig_pixcel_R,window_R=area_base_pixcel_matching_full_image(Sensors_L,Sensors_R,matchig_pixcel_L,Shift)
 #    #cv2.imshow('ii',window_R)
 #    #cv2.imshow('iiii')
 #    window_L=Sensors_L.img[int(matchig_pixcel_L['y']-Shift-1):int(matchig_pixcel_L['y']+Shift),int(matchig_pixcel_L['x']-Shift-1):int(matchig_pixcel_L['x']+Shift)]
 #    matchig_pixcel_R=matchig_pixcel_L
 #    MaxCorrelation=0
 #    rows, cols =Sensors_R.img.shape[:2]
 #    serech_domain_y= rows
 #    serech_domain_x= cols
 #    for i in range(serech_domain_y):
 #        for j in range(serech_domain_x):
 #            window_R=Sensors_R.img[int(i):int(2*Shift+1+i),int(j):int(2*Shift+1+j)]   
 #            Correlation = cv2.matchTemplate(window_L, window_R, cv2.TM_CCORR_NORMED)[0][0]
 #            if MaxCorrelation<Correlation:
 #                MaxCorrelation=Correlation
 #                ii,jj=i,j
 #    matchig_pixcel_R['x']=jj+Shift+1
 #    matchig_pixcel_R['y']=ii+Shift+1
 #    window_R=Sensors_R.img[int(matchig_pixcel_R['y']-Shift-1):int(matchig_pixcel_R['y']+Shift),int(matchig_pixcel_R['x']-Shift-1):int(matchig_pixcel_R['x']+Shift)] 
 #    cv2.imshow('ii',window_R)
 #    cv2.imshow('iiii',window_L)