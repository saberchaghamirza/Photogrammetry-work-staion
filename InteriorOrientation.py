# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 23:40:48 2023

@author: Saber
"""

import pandas as pd



def Read_Camera(filename):
    i = 1
    fiducial_coordinates = pd.DataFrame(data=[])
    distortions_df = pd.DataFrame(data=[])
    with open(filename, 'r') as f:
        file = f.readlines()

    for line in file:
        if i==1:
         camera_name=line
        elif i == 4:
            postion = line.find(':')
            focal_length = float(line[postion +1:-5])
        elif i < 10:
            o=0
            # do none
        elif i < 18:

            point_name = int(line[ 25:27])
            point_x = float(line[ 28:37])
            point_y = float(line[ 43:52])
            temp_df = pd.DataFrame(data=[{"number": point_name,"point_x": point_x,"point_y": point_y}])
            fiducial_coordinates = pd.concat([fiducial_coordinates, temp_df], axis=0)
        i = i + 1
    distortion_spacing=file[39]   
    distortions=file[40]
    i=26
    for ii in range(15):

      if ii<10 :
       ds=int(distortion_spacing[i:i+3])
       d=int((distortions[i:i+3]))
       temp_df = pd.DataFrame(data=[{"distortion_spacing": ds,"distortions": d}])
       distortions_df = pd.concat([distortions_df, temp_df], axis=0)
       i=i+3
      else :
          ds=int(distortion_spacing[i+1:i+4])
          d=int(distortions[i+2:i+4])
          i=i+4
          temp_df = pd.DataFrame(data=[{"distortion_spacing": ds,"distortions": d}])
          distortions_df = pd.concat([distortions_df, temp_df], axis=0)     
          
    return camera_name,focal_length,fiducial_coordinates,distortions_df

import numpy as np
from numpy.linalg import inv
import math as m 

def List_Squre(A,L,A_Check,L_Check):
    A=np.array(A)
    L=np.array(L)
    AT=A.transpose()
    X=(inv(AT.dot(A)).dot(AT)).dot(L)
    V_Control=A.dot(X)-L
    Rmse_Control=m.sqrt((V_Control.transpose().dot(V_Control))/len(V_Control))
    try:
        V_Check=np.array(A_Check).dot(X)-L_Check  
        Rmse_Check=m.sqrt((V_Check.transpose().dot(V_Check))/len(V_Check))
    except:
        V_Check=''
        Rmse_Check=''
    return X,V_Control,Rmse_Control,V_Check,Rmse_Check


#---------------------------------------------------------------------------------------------------------

from pandasql import sqldf
mysql = lambda q: sqldf(q, globals()) 

import cv2



class Interior_Orientation:
    
    def __init__(self,ImagePath):
          self.img = cv2.imread(ImagePath)
          self.Gry =(cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY))
          self.Laplacian  = cv2.Laplacian(self.Gry ,cv2.CV_64F)
          self.ptsLeft =[]
          self.ptsRight=[]
         
#------------------------------------------------------------------------------------------------------------------        
    def organize_point(self ,xy_ob_input,control_list,Camera_Path,investiy=False):
        self.camera_name,self.focal_length,self.fiducial_coordinates,self.Camera_distortions=Read_Camera(Camera_Path)

        global xy_obs 
        global xy_true 
        global Control_list 
        global Check_list 
        global AllPoint 
        xy_obs,xy_true=xy_ob_input,self.fiducial_coordinates
        Control_list=pd.DataFrame(control_list,columns=['Chose_number'])
        Check_list=pd.DataFrame(control_list,columns=['Chose_number'])

        query='''
            SELECT xy_obs.number number,  xy_obs.point_x x_obs,  xy_obs.point_y  y_obs, xy_true.point_x  x_true, xy_true.point_y  y_true
            from  xy_obs , xy_true 
            where xy_true.number=xy_obs.number;
        '''
        AllPoint=mysql(query)
        query='''
        SELECT *
        from  AllPoint
        where AllPoint.number IN (select * from Control_list);
        '''
        self.Control_Points=mysql(query)
        query='''
        SELECT *
        from  AllPoint 
        where AllPoint.number NOT IN (select * from Control_list);
        '''
        self.Check_Points=mysql(query)

# ------------------------------------------------------------------------------------------------------------------------
    def Mapping_Method(self,Method):
        L,A,L_Check,A_Check=[],[],[],[]
        self.Method=Method
        R=0
        for xp,yp,XC,YC in zip(self.Control_Points.x_obs,self.Control_Points.y_obs,self.Control_Points.x_true,self.Control_Points.y_true):            
            L.append(XC)
            L.append(YC) 
            
            if Method=='Comformal':
                A.append([xp, yp,1,0])
                A.append([yp,-xp,0,1])
                
            if Method=='Afine':
                A.append([xp,yp,1,0,0,0])
                A.append([0,0,0,xp,yp,1])
                
            if Method=='Projetive':
                A.append([xp,yp,1,0,0,0,-xp*XC,-yp*XC])
                A.append([0,0,0,xp,yp,1,-xp*YC,-yp*YC])
                
        for xp,yp,XC,YC in zip(self.Check_Points.x_obs,self.Check_Points.y_obs,self.Check_Points.x_true,self.Check_Points.y_true): 
            L_Check.append(XC)
            L_Check.append(YC)   
            
            if Method=='Comformal':
                A_Check.append([xp,yp,1,0])
                A_Check.append([yp,-xp,0,1])
                
            if Method=='Afine':                
                A_Check.append([xp,yp,1,0,0,0])
                A_Check.append([0,0,0,xp,yp,1])
                
            if Method=='Projetive':  
                A_Check.append([xp,yp,1,0,0,0,-xp*XC,-yp*XC])
                A_Check.append([0,0,0,xp,yp,1,-xp*YC,-yp*YC])   

        self.X,self.V_Control,self.Rmse_Control,self.V_check,self.Rmse_Check=List_Squre(A,L,A_Check,L_Check)

        
    def Mapping_Method_to_picel(self):
       L,A,L_Check,A_Check=[],[],[],[]
       Method=self.Method
       R=0
       for xp,yp,XC,YC in zip(self.Control_Points.x_true,self.Control_Points.y_true,self.Control_Points.x_obs,self.Control_Points.y_obs):            
           L.append(XC)
           L.append(YC) 
           
           if Method=='Comformal':
               A.append([xp, yp,1,0])
               A.append([yp,-xp,0,1])
               
           if Method=='Afine':
               A.append([xp,yp,1,0,0,0])
               A.append([0,0,0,xp,yp,1])
               
           if Method=='Projetive':
               A.append([xp,yp,1,0,0,0  ,-xp*XC,-yp*XC])
               A.append([0,0,0  ,xp,yp,1,-xp*YC,-yp*YC])
               
       for xp,yp,XC,YC in zip(self.Check_Points.x_true,self.Check_Points.y_true,self.Check_Points.x_obs,self.Check_Points.y_obs): 
           L_Check.append(XC)
           L_Check.append(YC)   
           
           if Method=='Comformal':
               A_Check.append([xp,yp,1,0])
               A_Check.append([yp,-xp,0,1])
               
           if Method=='Afine':                
               A_Check.append([xp,yp,1,0,0,0])
               A_Check.append([0,0,0,xp,yp,1])
               
           if Method=='Projetive':  
               A_Check.append([xp,yp,1,0,0,0,-xp*XC,-yp*XC])
               A_Check.append([0,0,0,xp,yp,1,-xp*YC,-yp*YC])     
       self.X_to_pixcel,self.V_Control_to_pixcel,self.Rmse_Control_to_pixcel,self.V_check_to_pixcel,self.Rmse_Check_to_pixcel=List_Squre(A,L,A_Check,L_Check)
#-------------------------------------------------------------------------------------------------------------------------        
    def Mapping_to_point(self,xp,yp):
        Method=self.Method
        x_o,y_o=0,0
        if Method=='Comformal':
            x_o=(self.X[0]*xp +self.X[1]*yp +self.X[2])
            y_o=(-self.X[1]*xp+self.X[0]*yp+self.X[3])
        if Method=='Afine':                
            x_o=(self.X[0]*xp+self.X[1]*yp+self.X[2])
            y_o=(self.X[3]*xp+self.X[4]*yp+self.X[5])
        if Method=='Projetive':  
            x_o=(self.X[0]*xp+self.X[1]*yp+self.X[2])/(self.X[6]*xp+self.X[7]*yp +1)
            y_o=(self.X[3]*xp+self.X[4]*yp+self.X[5])/(self.X[6]*xp+self.X[7]*yp +1)
        xy={'x':x_o,"y":y_o}
        try:xy=pd.DataFrame(xy)       
        except:xy=xy
        return xy
    
    def Mapping_to_Pixcel(self,xp ,yp):
       # xp: np.array or number  
       # yp: np.array or number
        Method=self.Method
        x_o,y_o=0,0
        if Method=='Comformal':
            x_o=(self.X_to_pixcel[0]*xp-self.X_to_pixcel[1]*yp +self.X_to_pixcel[2])
            y_o=(self.X_to_pixcel[1]*xp+self.X_to_pixcel[0]*yp+self.X_to_pixcel[3])
        if Method=='Afine':                
            x_o=(self.X_to_pixcel[0]*xp+self.X_to_pixcel[1]*yp+self.X_to_pixcel[2])
            y_o=(self.X_to_pixcel[3]*xp+self.X_to_pixcel[4]*yp+self.X_to_pixcel[5])
        if Method=='Projetive':  
            x_o=(self.X_to_pixcel[0]*xp+self.X_to_pixcel[1]*yp+self.X_to_pixcel[2])/(self.X_to_pixcel[6]*xp+self.X_to_pixcel[7]*yp+1)
            y_o=(self.X_to_pixcel[3]*xp+self.X_to_pixcel[4]*yp+self.X_to_pixcel[5])/(self.X_to_pixcel[6]*xp+self.X_to_pixcel[7]*yp+1)
        xy={'x':x_o,"y":y_o}
        try:xy=pd.DataFrame(xy)       
        except:xy=xy
        return xy
    
    

#-----------------------------------------------------------------------------------------------------------------------------------------
    def Fiducial_Mark(self):
        matchCase=[]
        def click_event(event, x, y, flags, params):
             if event == cv2.EVENT_LBUTTONDOWN: # checking  left mouse clicks
                 global point
                 point=[x,y]
                 matchCase.append(point)
                 # displaying the point on the image window
                 cv2.circle(self.img, (x,y), 1, (0,0,255), -1)
                 cv2.imshow(win_name,self.img)
             if event == cv2.EVENT_RBUTTONDOWN: # checking  left mouse clicks

               #  matchCase.remove(0)
                 # displaying the point on the image window
                 cv2.circle(self.img, (x,y), 1, (0,0,255), -1)
                # cv2.imshow(win_name,self.img)
                 cv2.destroyAllWindows()
                                 
        def show():
            
        
            cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
            
            # Move it to (X,Y)
            cv2.moveWindow(win_name, 0, 0)
                
            # Show the Image in the Window
            cv2.imshow(win_name, self.img)
                
            # Resize the Window
            cv2.resizeWindow(win_name, 400, 300)
            
        #    cv2.imshow(window_title, self.img)
            
            cv2.setMouseCallback(win_name, click_event)
            
            cv2.waitKey(0)
            # close the window
            cv2.destroyAllWindows()
        win_name='chose 8 maker'
        show()
        return matchCase
       
   
 
        #self.img_rotated = cv2.warpAffine(self.Gry, R, (cols,rows))

Image_Path = {'left':r'D:\Projects\2.Term2\Digital_Photogrammetry\project1\main\data\21_60_.png',
              'right':r'D:\Projects\2.Term2\Digital_Photogrammetry\project1\main\data\22_60_.png'}
Fiducial_Mark_Path = {'left':r'D:\Projects\2.Term2\Digital_Photogrammetry\project1\main\data\Fiducial_Mark_On_Left_Image_readed.txt',
                      'right':r'D:\Projects\2.Term2\Digital_Photogrammetry\project1\main\data\Fiducial_Mark_On_Right_Image_readed.txt'}

Camera_Path=r"D:\Projects\2.Term2\Digital_Photogrammetry\project1\main\data\CAMERA.txt"

# Sensors_R=Interior_Orientation(Image_Path['right'],Camera_Path)

# cc=Sensors_R.Fiducial_Mark()