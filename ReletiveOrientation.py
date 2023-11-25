# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 11:19:00 2023

@author: Saber


"""
import numpy as np
from numpy.linalg import inv
import math as m 
from scipy import signal
import cv2
def List_Squre(A,L):
    
    A=np.array(A)
    L=np.array(L)
    AT=A.transpose()
    X=(inv(AT.dot(A)).dot(AT)).dot(L)
    V=A.dot(X)-L
    Rmse_Control=m.sqrt((V.transpose().dot(V))/len(V))
    return X,V,Rmse_Control

import numpy as np
import pandas as pd
from math import cos,sin,pi
#left photo coordinates[mm]
def rotation_by_angels(omega,phi,kappa):
           R = np.zeros([3,3]);
           R[0,0] =  cos(phi)*cos(kappa);
           R[0,1] =  sin(omega)*sin(phi)*cos(kappa)+cos(omega)*sin(kappa);
           R[0,2] = -cos(omega)*sin(phi)*cos(kappa)+sin(omega)*sin(kappa);
           R[1,0] = -cos(phi)*sin(kappa);
           R[1,1] = -sin(omega)*sin(phi)*sin(kappa)+cos(omega)*cos(kappa);
           R[1,2] = cos(omega)*sin(phi)*sin(kappa)+sin(omega)*cos(kappa);
           R[2,0] = sin(phi);
           R[2,1] = -sin(omega)*cos(phi);
           R[2,2] = cos(omega)*cos(phi);
           return R

#focal length
def XYZ_To_xy(M,R,Geo,L_Center,R_Center,c):
    Fx_L,Fy_L,Fx_R,Fy_R=[],[],[],[]
    for i in range(len(Geo['X'])):
        # numerator for x in the collinearity equation for every ground control point (left image)
        rL= M[0,0]*(Geo['X'][i]-L_Center['x'])+M[0,1]*(Geo['Y'][i]-L_Center['y'])+M[0,2]*(Geo['Z'][i]-L_Center['z']) 
        sL= M[1,0]*(Geo['X'][i]-L_Center['x'])+M[1,1]*(Geo['Y'][i]-L_Center['y'])+M[1,2]*(Geo['Z'][i]-L_Center['z']) 
        qL= M[2,0]*(Geo['X'][i]-L_Center['x'])+M[2,1]*(Geo['Y'][i]-L_Center['y'])+M[2,2]*(Geo['Z'][i]-L_Center['z']) 
        # numerator for x in the collinearity equation for every ground control point (RIHGT image)
        rR= R[0,0]*(Geo['X'][i]-R_Center['x'])+R[0,1]*(Geo['Y'][i]-R_Center['y'])+R[0,2]*(Geo['Z'][i]-R_Center['z'])  
        sR= R[1,0]*(Geo['X'][i]-R_Center['x'])+R[1,1]*(Geo['Y'][i]-R_Center['y'])+R[1,2]*(Geo['Z'][i]-R_Center['z'])  
        qR= R[2,0]*(Geo['X'][i]-R_Center['x'])+R[2,1]*(Geo['Y'][i]-R_Center['y'])+R[2,2]*(Geo['Z'][i]-R_Center['z'])  
        # from collinearity equation for the left image
        Fx_L.append( -c*(rL/qL))
        Fy_L.append( -c*(sL/qL))
        # from collinearity equation for the right image
        Fx_R.append( -c*(rR/qR))
        Fy_R.append( -c*(sR/qR))
    return Fx_L,Fy_L,Fx_R,Fy_R
    
class Collinearity_Equation:
    
    def __init__(self,Sensors_L,Sensors_R):
         self.Sensors_R=Sensors_R
         self.Sensors_L=Sensors_L
         self.ptsLeft =[]
         self.ptsRight=[]
         
         
    def collinearity_equation_for_Relative_orientation(self,left,right,c,tershold):
        #the approximate exterior orientation parameters of the left image
        X0l = 0;
        Y0l = 0;
        Z0l = 0;
        #the approximate exterior orientation parameters of the right image
        bx = c;
        by = 0;
        bz = 0;
        omega = 0;
        phi = 0;
        kappa = 0;
        #approximate reference point coordinates
        X,Y,H,Z = [],[],[],[]
        x_left,y_left,x_right,y_right=[],[],[],[]
        for i  in range(len(left.x)) :
            #parallax
            px = left.x[i] - right.x[i];
            if px>5 and px<200:
                X.append( left.x[i]*(bx/px));
                Y.append( left.y[i]*(bx/px));
                H.append( (c*bx)/px);
                Z.append( Z0l - H[-1]);
                x_left.append(left.x[i])
                y_left.append(left.y[i])
                x_right.append(right.x[i])
                y_right.append(right.y[i])  
                self.ptsLeft.append([left.x[i],left.y[i]])
                self.ptsRight.append([right.x[i],right.y[i]])
        #-----------------------------------------------------

        M=rotation_by_angels(omega,phi,kappa)
        t=10
        while t>tershold:
    #for i in range(10):
    #if __name__=='__main__':
        
       #ñ^cc
        
           # Rùöê
           R=rotation_by_angels(omega,phi,kappa)
           # ñ^cc
        
           
           rL,sL,qL,rR,sR,qR=[],[],[],[],[],[]
           Fx_L,Fy_L,Fx_R,Fy_R=[],[],[],[]
           dL,A=[],[]
           count=1
           for x,y,z,Lx,Ly,Rx,Ry in zip(X,Y,Z,x_left,y_left,x_right,y_right):
       
                # numerator for x in the collinearity equation for every ground control point (left image)
                rL= M[0,0]*(x-X0l)+M[0,1]*(y-Y0l)+M[0,2]*(z-Z0l) 
                sL= M[1,0]*(x-X0l)+M[1,1]*(y-Y0l)+M[1,2]*(z-Z0l) 
                qL= M[2,0]*(x-X0l)+M[2,1]*(y-Y0l)+M[2,2]*(z-Z0l) 
                # numerator for x in the collinearity equation for every ground control point (RIHGT image)
                rR= R[0,0]*(x-bx)+R[0,1]*(y-by)+R[0,2]*(z-bz)  
                sR= R[1,0]*(x-bx)+R[1,1]*(y-by)+R[1,2]*(z-bz)  
                qR= R[2,0]*(x-bx)+R[2,1]*(y-by)+R[2,2]*(z-bz)  
               #--------------------------------------------------------------------------------------------------------------
               #1
               # LEFT
                zerolist_start=[ 0 for i in range ((count-1)*3)]
                zerolist_end  =[ 0 for i in range ((len(X)-count)*3)]
                zerolist_Kwnone  =[ 0 for i in range (5)]
                # x Equation on left for XYZ
                B_dX_Lx  = c*(M[2,0]*rL-M[0,0]*qL)/(qL)**2;
                B_dY_Lx =  c*(M[2,1]*rL-M[0,1]*qL)/(qL)**2;
                B_dZ_Lx =  c*(M[2,2]*rL-M[0,2]*qL)/(qL)**2;
                # y Equation on left for XYZ
                B_dX_Ly  = c*(M[2,0]*sL-M[1,0]*qL)/(qL)**2;
                B_dY_Ly =  c*(M[2,1]*sL-M[1,1]*qL)/(qL)**2;
                B_dZ_Ly =  c*(M[2,2]*sL-M[1,2]*qL)/(qL)**2;
                
                
                A1= zerolist_Kwnone+zerolist_start+[B_dX_Lx,B_dY_Lx,B_dZ_Lx]+zerolist_end 
                A2= zerolist_Kwnone+zerolist_start+[B_dX_Ly,B_dY_Ly,B_dZ_Ly]+zerolist_end
              
                # RIGHT
                dx=x-bx
                dy=y-by
                dz=z-bz
                
                B_11  =   (c/qR**2)*(rR*(-R[2,2]*dy+R[2,1]*dz)-qR*(-R[0,2]*dy+R[0,1]*dz));
                B_12  =   (c/qR**2)*((rR*(cos(phi)*dx + sin(omega)*sin(phi)*dy-cos(omega)*sin(phi)*dz)) -
                                      qR*(-sin(phi)*cos(kappa)*dx + sin(omega)*cos(phi)*cos(kappa)*dy - cos(omega)*cos(phi)*cos(kappa)*dz  ));
                B_13  =   -(c/qR)*(R[1,0]*dx+R[1,1]*dy+R[1,2]*dz);
                
                B_14  =   -c*(R[2,1]*rR-R[0,1]*qR)/(qR)**2;   
                B_15  =   -c*(R[2,2]*rR-R[0,2]*qR)/(qR)**2; 
                
                B_dX_Rx =  c*(R[2,0]*rR-R[0,0]*qR)/(qR)**2;
                B_dY_Rx =  c*(R[2,1]*rR-R[0,1]*qR)/(qR)**2;
                B_dZ_Rx =  c*(R[2,2]*rR-R[0,2]*qR)/(qR)**2;
                
                A3=[B_11]+[B_12]+[B_13]+[B_14]+[B_15]+zerolist_start+[B_dX_Rx,B_dY_Rx,B_dZ_Rx]+zerolist_end
                
               # test_list3 = test_list3 + test_list4
               
                B_21  =   (c/qR**2)*(sR*(-R[2,2]*dy+R[2,1]*dz)-qR*(-R[1,2]*dy+R[1,1]*dz));
                B_22  =   (c/qR**2)*(sR*(cos(phi)*dx+sin(omega)*sin(phi)*dy-cos(omega)*sin(phi)*dz) -
                                     qR*(sin(phi)*sin(kappa)*dx - sin(omega)*cos(phi)*sin(kappa)*dy + cos(omega)*cos(phi)*sin(kappa)*dz  ));
                B_23  =   (c/qR)   *(R[0,0]*dx+R[0,1]*dy+R[0,2]*dz);
                
                B_24   =  -c*(R[2,1]*sR-R[1,1]*qR)/(qR)**2; 
                B_25   =  -c*(R[2,2]*sR-R[1,2]*qR)/(qR)**2;
                # y Equation on left for XYZ
                B_dx_Ry =  c*(R[2,0]*sR-R[1,0]*qR)/(qR)**2;
                B_dY_Ry =  c*(R[2,1]*sR-R[1,1]*qR)/(qR)**2;
                B_dZ_Ry =  c*(R[2,2]*sR-R[1,2]*qR)/(qR)**2;
               
                A4=[B_21]+[B_22]+[B_23]+[B_24]+[B_25]+zerolist_start+[B_dx_Ry,B_dY_Ry,B_dZ_Ry]+zerolist_end
                
                A.append(A1)
                A.append(A2)
                A.append(A3)
                A.append(A4)
               #--------------------------------------------------------------------------------------------------------------------
               # from collinearity equation for the left image
                Fx_L= -c*(rL/qL)
                Fy_L= -c*(sL/qL)
               # from collinearity equation for the right image
                Fx_R= -c*(rR/qR)
                Fy_R= -c*(sR/qR)
                
                
                dL.append( Lx-Fx_L);
                dL.append( Ly-Fy_L);
                dL.append( Rx-Fx_R);
                dL.append( Ry-Fy_R);
                count=count+1
           dX,V,Rmse= List_Squre(A,dL)
           omega = omega+(dX[0]);
           phi = phi+(dX[1]);
           kappa = kappa+(dX[2]);
           by = dX[3]+by;
           bz = dX[4]+bz;
           for i in range(len(X)):
               X[i]=dX[3*i+5]+X[i]
               Y[i]=dX[3*i+6]+Y[i]
               Z[i]=dX[3*i+7]+Z[i]
           
           t=max(abs(dX[5:]))
           print(t)
        self.Rmse=Rmse
        self.Geo=pd.DataFrame({'X':X,'Y':Y,'Z':Z})
        self.omega=omega
        self.phi=phi
        self.kappa=kappa
        self.L_Center={'x':0 ,'y':0 ,'z':0}
        self.R_Center={'x':bx,'y':by,'z':bz}
        self.By=by
        self.Bz=bz  
        self.x_L=Fx_L
        self.y_L=Fy_L
        self.x_R=Fx_R
        self.y_R=Fy_R
        self.c=c
        self.Z_Avrage=sum(Z)/len(Z)
        self.A=A
        return omega,phi,kappa,bx,by,bz,R
    
    
    def projective_matrix_to_image_SP_pixel(self):
        M=rotation_by_angels(0,0,0)
        R=rotation_by_angels(self.omega,self.phi,self.kappa)
        Fx_L,Fy_L,Fx_R,Fy_R=XYZ_To_xy(M,R,self.Geo,self.L_Center,self.R_Center,self.c)
        self.xy_pixcel_L=self.Sensors_L.Mapping_to_Pixcel(np.array(Fx_L),np.array(Fy_L))
        self.xy_pixcel_R=self.Sensors_R.Mapping_to_Pixcel(np.array(Fx_R),np.array(Fy_R))
        L,A=[],[]
        for xp,yp,XC,YC in zip(self.xy_pixcel_R.x,self.xy_pixcel_R.y,self.xy_pixcel_L.x,self.xy_pixcel_L.y):            
                L.append(XC)
                L.append(YC) 
                A.append([xp,yp,1,0,0,0,-xp*XC,-yp*XC])
                A.append([0,0,0,xp,yp,1,-xp*YC,-yp*YC])
        X,V,Rmse_Control =List_Squre(A,L)  
        projective_matrix_R=np.array([  [X[0],X[1],X[2]],
                                        [X[3],X[4],X[5]],
                                        [X[6],X[7],1  ]]) 
        self.projective_matrix_R=X
        return projective_matrix_R
    def Inverse_projective_matrix_to_image_SP_pixel(self):

        L,A=[],[]
        for xp,yp,XC,YC in zip(self.xy_pixcel_L.x,self.xy_pixcel_L.y,self.xy_pixcel_R.x,self.xy_pixcel_R.y):            
                L.append(XC)
                L.append(YC) 
                A.append([xp,yp,1,0,0,0,-xp*XC,-yp*XC])
                A.append([0,0,0,xp,yp,1,-xp*YC,-yp*YC])
        X,V,Rmse_Control =List_Squre(A,L)  
        inverse_projective_matrix_R=np.array([  [X[0],X[1],X[2]],
                                        [X[3],X[4],X[5]],
                                        [X[6],X[7],1  ]]) 
        self.inverse_projective_matrix_R=X
        return X   
    
    def Object_SP_to_image_SP_pixel(self,Geo,shift,img_L,img_R):
       
        M=rotation_by_angels(0,0,0)
        R=rotation_by_angels(self.omega,self.phi,self.kappa)
        Fx_L,Fy_L,Fx_R,Fy_R=XYZ_To_xy(M,R,Geo,self.L_Center,self.R_Center,self.c)
        xy_pixcel_R={'x':0,'y':0}       

        xy_pixcel_L=self.Sensors_L.Mapping_to_Pixcel(np.array(Fx_L),np.array(Fy_L))
        xy_pixcel_R=self.Sensors_L.Mapping_to_Pixcel(np.array(Fx_R),np.array(Fy_R))

        methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR','cv2.TM_CCORR_NORMED',     'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
       # try:
        if True:
            # window_L=self.Sensors_L.img[int(xy_pixcel_L['x']-shift):int(xy_pixcel_L['x']+shift),int(xy_pixcel_L['y']-shift):int(xy_pixcel_L['y']+shift)]
            # window_R=self.Sensors_R.img[int(xy_pixcel_R['x']-shift):int(xy_pixcel_R['x']+shift),int(xy_pixcel_R['y']-shift):int(xy_pixcel_R['y']+shift)]          
   #         try:
                window_L=self.Sensors_L.img[int(xy_pixcel_L['y']-shift-1):int(xy_pixcel_L['y']+shift),int(xy_pixcel_L['x']-shift-1):int(xy_pixcel_L['x']+shift)]
                window_R=self.Sensors_R.img[int(xy_pixcel_R['y']-shift-1):int(xy_pixcel_R['y']+shift),int(xy_pixcel_R['x']-shift-1):int(xy_pixcel_R['x']+shift)]     
                result = cv2.matchTemplate(window_L, window_R, cv2.TM_CCOEFF_NORMED)[0][0]
            # except:
            #       result=0
            #       window_L=0
            #       window_R=0

        #except: result=0
        return result,window_L,window_R,xy_pixcel_L,xy_pixcel_R
 # test
#--------------------------------------------------
 #partial derivatives with respect to x1 (left image)
if __name__=="__main__":

    left =np.array([[9.44,33.25],
           [23.85,32.21],
           [36.46,33.20],
           [12.66,-24.04],
           [20.70,-7.58],
           [43.99,-23.80],])
    #right photo coordinates[mm]
    right =np.array([[-29.40,31.44],
            [-15.24,30.34],
            [-2.64,31.32],
            [-32.93,-26.05],
            [-22.38,-9.54],
            [-1.82,-25.84]])
    left=(pd.DataFrame(data=left,columns=['x','y']))
    right=(pd.DataFrame(data=right,columns=['x','y']))
    #focal length
    c = 80;
    tershold=0.000001
    RELTIVE=Collinearity_Equation()
  #  omega,phi,kappa,bx,by,bz,,R=RELTIVE.collinearity_equation_for_Relative_orientation(left,right,c,tershold)
    
