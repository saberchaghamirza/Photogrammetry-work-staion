# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 02:06:26 2023

@author: Saber
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# #-------------------------------------------------------------------------------------------
import cv2
from numpy.linalg import inv
from skimage.feature import graycomatrix, graycoprops

from ReletiveOrientation import Collinearity_Equation
def List_Squre(A,L):
    A=np.array(A)
    L=np.array(L)
    AT=A.transpose()
    x=(inv(AT.dot(A)).dot(AT)).dot(L)
    v=A.dot(x)-L
   #  RMSE (Root mean square error) and SD (Standard deviation) have similar formula s in this case.
    rmse=np.sqrt((v.transpose().dot(v))/len(v))
    return x,rmse

class StreoImages:
    
    def __init__(self,Sensors_L,Sensors_R):
         self.Sensors_L=Sensors_L
         self.Sensors_R=Sensors_R
         self.ptsLeft =[]
         self.ptsRight=[]
         self.Relative_orientation=Collinearity_Equation(Sensors_L,Sensors_R)
         
    def ExtractMatchedPoints(self,RatioTest):
        # sift
        sift=cv2.SIFT_create() 
        # extract keyPoints and descriptors
        keyPointsLeft , descriptorsLeft  = sift.detectAndCompute(self.Sensors_L.Gry,None)
        keyPointsRight, descriptorsRight = sift.detectAndCompute(self.Sensors_R.Gry, None)
        # FLANN parameters
        FLANN_INDEX_KDTREE = 2
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks=50)   # or pass empty dictionary
        flann = cv2.FlannBasedMatcher(index_params,search_params)
        # feature matching
        matches = flann.knnMatch(descriptorsLeft,descriptorsRight,k=2)  

        self.ptsLeft,self.ptsRight=[],[]
        for m,n in matches:
            # Apply ratio test
         if m.distance < RatioTest * n.distance:
             # Featured matched keypoints from images 1 and 2
            self.ptsLeft .append(keyPointsLeft [(m.queryIdx)].pt)
            self.ptsRight.append(keyPointsRight[(m.trainIdx)].pt)
        self.ptsLeft_pixcel=pd.DataFrame({'x':np.array(self.ptsLeft)[:,0],'y':np.array(self.ptsLeft)[:,1]})
        self.ptsRight_pixcel=pd.DataFrame({'x':np.array(self.ptsLeft)[:,0],'y':np.array(self.ptsLeft)[:,1]})
        
    def InitializeProjective(self):    #2d DLT
        L,A=[],[]
        for coordsLeft,coordsRight in zip(self.ptsLeft,self.ptsRight): 
            xL,yL=coordsLeft
            xR,yR=coordsRight
            L.append(xR)
            L.append(yR)        
            A.append([xL,yL,1,0,0,0,-xL*xR, -yL*xR])
            A.append([0,0,0,xL,yL,1,-xL*yR, -yL*yR])
            
        self.X,self.Std_Projective=List_Squre(A,L)


    def Initialize_Relative_orientation_in_pp(self,focal_length,tershold):
        ''' lines - corresponding epilines '''
        ptsL = np.int32(self.ptsLeft)
        ptsR = np.int32(self.ptsRight)

        self.FundamentalMat, mask = cv2.findFundamentalMat(ptsR,ptsL,cv2.FM_RANSAC,ransacReprojThreshold=1.0, confidence=0.99)
        # We select only inlier points
        ptsL = ptsL[mask.ravel()==1]
        ptsR = ptsR[mask.ravel()==1]
        self.ptsLeft_mm=self.Sensors_L.Mapping_to_point(np.array(ptsL)[:,0],np.array(ptsL)[:,1])
        self.ptsRight_mm=self.Sensors_R.Mapping_to_point(np.array(ptsR)[:,0],np.array(ptsR)[:,1])
       
        omega,phi,kappa,bx,by,bz,R=self.Relative_orientation.collinearity_equation_for_Relative_orientation(self.ptsLeft_mm,self.ptsRight_mm,focal_length,tershold)
        projective_matrix_R=self.Relative_orientation.projective_matrix_to_image_SP_pixel()
        self.inverse_projective_matrix_R=self.Relative_orientation.Inverse_projective_matrix_to_image_SP_pixel()
        rows, cols =self.Sensors_R.img.shape[:2]
        self.Sensors_R_New= cv2.warpPerspective(self.Sensors_R.img,projective_matrix_R, (cols,rows),flags=cv2.INTER_CUBIC)
        return projective_matrix_R
    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    
    def Initialize_VLL(self,X,Y,step,shift=25):
        #------------------------------------
        def serch_obj_and_image(X,Y,Z):
            correlation=[]
            for index in range(len(Z)):
                 Geo={'X':[X],'Y':[Y],'Z':[Z[index]]}
                 cor,window_L,window_R,xy_pixcel_L,xy_pixcel_R=self.Relative_orientation.Object_SP_to_image_SP_pixel(Geo,shift,self.Sensors_L.Gry,self.Sensors_R.Gry)
                 correlation.append(cor)
            result=pd.DataFrame({'correlation':correlation,'Z':Z})
            maxSerch=result[result['correlation'] == max(correlation)].reset_index()
            return maxSerch,xy_pixcel_L,xy_pixcel_R
        #---------------------------------------
        Z_start=self.Relative_orientation.Z_Avrage
       # print(Z_start)
        MaxCorrelation,matchig_pixcel_L,matchig_pixcel_R=serch_obj_and_image(X,Y,[Z_start])
        MaxCorrelation=MaxCorrelation['correlation'][0]
      #  print(MaxCorrelation)
        while step>10**-3:
          #  Z= [(lambda x: Z_start+x*serech_t+-serech_t*serech_t/2)(x) for x in range(20)] 
            Z= [Z_start-step, Z_start+step]
            maxSerch,xy_pixcel_L,xy_pixcel_R=serch_obj_and_image(X,Y,Z)
            if maxSerch['correlation'][0]>MaxCorrelation:
                MaxCorrelation=maxSerch['correlation'][0]
                Z_start       =maxSerch['Z'][0]
                matchig_pixcel_L=xy_pixcel_L
                matchig_pixcel_R=xy_pixcel_R
                #print(MaxCorrelation)
            step=step/2
        


        return matchig_pixcel_L,matchig_pixcel_R,Z_start
    
    def ploting(self,step,plot_step,shift):
        s=plot_step
        Model_X_range=min(self.Relative_orientation.Geo.X)+s,max(self.Relative_orientation.Geo.X)-s
        Model_Y_range=min(self.Relative_orientation.Geo.Y)+s,max(self.Relative_orientation.Geo.Y)-s
        
        X = np.arange(int(Model_X_range[0]), int(Model_X_range[1]), plot_step)
        Y = np.arange(int(Model_Y_range[0]), int(Model_Y_range[1]), plot_step)
        X_len=X.shape[0]
        Y_len=Y.shape[0]
        X, Y = np.meshgrid(X, Y)
        Z=np.zeros_like(X)
        PL=[]
        PR=[]
        print(X.shape)
        for j in range(X_len):
           for i in range(Y_len):

             matchig_pixcel_L,matchig_pixcel_R,z=self.Initialize_VLL(X[i,j],Y[i,j],step,shift)
             Z[i,j]=z
             PL.append([matchig_pixcel_L.x[0],matchig_pixcel_L.y[0]])
             PR.append([matchig_pixcel_R.x[0],matchig_pixcel_R.y[0]])

        self.VLL_matchig_pixcel_L=pd.DataFrame({'x':np.array(PL)[:,0],'y':np.array(PL)[:,1]})
        self.VLL_matchig_pixcel_R=pd.DataFrame({'x':np.array(PR)[:,0],'y':np.array(PR)[:,1]})
        # Plotting the Animation
        fig = plt.figure(figsize=(15, 7))
        ax1 = fig.add_subplot(121, projection='3d')
        mycmap = plt.get_cmap('gist_earth') 
        surf=ax1.plot_surface(X, Y, Z, cmap=mycmap,linewidth=0.01) 
       
        plt.colorbar(surf, shrink=0.5, aspect=5,ax=ax1)
        plt.show()
        
     
        
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# area base matching
    def Mapping_to_point_from_rotated_to_real(self,xp,yp):
        x_o=(self.inverse_projective_matrix_R[0]*xp+self.inverse_projective_matrix_R[1]*yp+self.inverse_projective_matrix_R[2])/(self.inverse_projective_matrix_R[6]*xp+self.inverse_projective_matrix_R[7]*yp +1)
        y_o=(self.inverse_projective_matrix_R[3]*xp+self.inverse_projective_matrix_R[4]*yp+self.inverse_projective_matrix_R[5])/(self.inverse_projective_matrix_R[6]*xp+self.inverse_projective_matrix_R[7]*yp +1)
        xy={'x':x_o,"y":y_o}
        try:xy=pd.DataFrame(xy)       
        except:xy=xy
        return xy
    
    def area_base_pixcel_matching(self,matchig_pixcel_L,Shift,serech_domain_y,serech_domain_x):
        serech_domain_y= np.arange(-serech_domain_y, serech_domain_y, 1, dtype=int)
        serech_domain_x= np.arange(-serech_domain_x, serech_domain_x, 1, dtype=int)
        window_L=self.Sensors_L.img[int(matchig_pixcel_L['y']-Shift-1):int(matchig_pixcel_L['y']+Shift),int(matchig_pixcel_L['x']-Shift-1):int(matchig_pixcel_L['x']+Shift)]
        matchig_pixcel_R=self.Mapping_to_point_from_rotated_to_real(matchig_pixcel_L['x'].copy(),matchig_pixcel_L['y'].copy())
        MaxCorrelation=0
        for i in serech_domain_y:
            for j in serech_domain_x:
                window_R=self.Sensors_R.img[int(matchig_pixcel_R['y']-Shift-1+i):int(matchig_pixcel_R['y']+Shift+i),int(matchig_pixcel_R['x']-Shift-1+j):int(matchig_pixcel_R['x']+Shift+j)]   
                Correlation = cv2.matchTemplate(window_L, window_R, cv2.TM_CCORR_NORMED)[0][0]
                if MaxCorrelation<Correlation:
                    MaxCorrelation=Correlation
                    ii,jj=i,j
        matchig_pixcel_R['x']=matchig_pixcel_R['x']+jj
        matchig_pixcel_R['y']=matchig_pixcel_R['y']+ii
        window_R=self.Sensors_R.img[int(matchig_pixcel_R['y']-Shift-1):int(matchig_pixcel_R['y']+Shift),int(matchig_pixcel_R['x']-Shift-1):int(matchig_pixcel_R['x']+Shift)] 
        return matchig_pixcel_R ,window_L,window_R
    
    
    
    def Find_MatchCase(self): 
         def click_event(event, x, y, flags, params):
             if event == cv2.EVENT_LBUTTONDOWN: # checking  left mouse clicks
                 global point            
                 point=[x,y]
                 # displaying the point on the image window
                 cv2.circle(img, (x,y), 1, (0,0,255), -1)
                 cv2.imshow(window_title, img)
                 matchCase.append(point)
                 
         matchCase=[]
         for img,window_title in zip([self.imgLeft,self.imgRight],['imgLeft','imgRight']) :
             # displaying the image
             cv2.imshow(window_title, img)
             cv2.setMouseCallback(window_title, click_event)
             cv2.waitKey(0)
             # close the window
             cv2.destroyAllWindows()
             
         return matchCase

