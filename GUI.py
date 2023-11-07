import tkinter
import tkinter.messagebox
import customtkinter
import cv2
import numpy as np
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
from PIL import ImageTk, Image
from zoming import CanvasImage
import pandas as pd
from tkinter import Menu,filedialog,filedialog,PhotoImage,ALL, EventType,Entry,Label,Button,StringVar,Tk,Frame,Checkbutton,IntVar,S,N,SE,NE,W,E,SW
import random
from InteriorOrientation import Interior_Orientation,Read_Camera
from StreoImage import StreoImages
from NCC_Matching import area_base_pixcel_matching,area_base_pixcel_matching_full_image,area_base_pixcel_matching_by_sererchAREA
from LSM_Matching import LSM_geo_radio,LSM_s_r,LSM_Full_Geometry
class App(customtkinter.CTk):
    
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def __init__(self):
        super().__init__()
        
        # configure window
        self.title("Digital Photogrammetry Work station.py")
        self.geometry(f"{1500}x{680}")
        
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Work station Features", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.InteriorOrientation,text='Interior Orientation')
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.ReletiveOrientation,text='Reletive Orientation')
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.VLL,text='VLL')
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, command=self.NCC,text='Correlation Matching')
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)
        self.sidebar_button_5 = customtkinter.CTkButton(self.sidebar_frame, command=self.LSM,text='Least Square Matching')
        self.sidebar_button_5.grid(row=5, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))
        
        self.sidebar_button_2.configure(state="disabled")
        self.sidebar_button_3.configure(state="disabled")
        self.sidebar_button_4.configure(state="disabled")
        self.sidebar_button_5.configure(state="disabled")
        self.appearance_mode_optionemenu.set("System")
        self.tagesL=[]
        self.tagesR=[]      
        self.Sensors_L=None
        self.Sensors_R=None
        # intoror 
        self.tabviewL = customtkinter.CTkTabview(self, width=100)
        self.tabviewR = customtkinter.CTkTabview(self, width=100)
        self.scrollable_frame0 = customtkinter.CTkTabview(self, width=100)
        self.checkbox_slider_frame = customtkinter.CTkTabview(self, width=100)
        ##
        self.frame_image_l=customtkinter.CTkFrame(self)
        self.frame_image_r=customtkinter.CTkFrame(self)
        
        self.frame_image_r.grid_columnconfigure(0, weight = 1, uniform=1)
        self.frame_image_r.grid_rowconfigure(0, weight = 1, uniform=1)
        self.frame_image_l.grid_columnconfigure(0, weight = 1, uniform=1)
        self.frame_image_l.grid_rowconfigure(0, weight = 1, uniform=1)
        # ReletiveOrientation frames:
        self.frame01 = customtkinter.CTkFrame(self)
        self.frame02 = customtkinter.CTkFrame(self)
        self.frame_streo = customtkinter.CTkFrame(self)
        
        self.frame_streo.grid_columnconfigure(0, weight = 1, uniform=1)
        self.frame_streo.grid_rowconfigure(0, weight = 1, uniform=1)
        self.ReletiveOrientation_stase=False
        # VLL 
        self.frame_vll_01 = customtkinter.CTkFrame(self)
        self.frame_vll_02 = customtkinter.CTkFrame(self)
        self.match_window_l=customtkinter.CTkFrame(self)
        self.match_window_r=customtkinter.CTkFrame(self)
        # NCC
        self.frame_NCC_01 = customtkinter.CTkFrame(self)
        self.frame_NCC_02 = customtkinter.CTkFrame(self)

        self.match_window_r.grid_columnconfigure(0, weight = 1, uniform=1)
        self.match_window_r.grid_rowconfigure(0, weight = 1, uniform=1)
        self.match_window_l.grid_columnconfigure(0, weight = 1, uniform=1)
        self.match_window_l.grid_rowconfigure(0, weight = 1, uniform=1)
        self.tagesNCC=[]
        # NCC
        self.frame_NCC_01 = customtkinter.CTkFrame(self)
        self.frame_NCC_02 = customtkinter.CTkFrame(self)
        ## lsm
        self.frame_LSM_01=customtkinter.CTkFrame(self)
        self.frame_LSM_02=customtkinter.CTkFrame(self)
        
        self.InteriorOrientation()
      #   self.ReletiveOrientation()
      # #  self.VLL()
       # self.NCC()
        #self.LSM()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
    def do_Interior_left(self):
          Method='Projetive'
          do=True
          Control__Point_list,Check__Point_list=[],[]
          X,Y,number=[],[],[]
          for i in range(8):
                if  self.scrollable_frame_switches_on[i].get()=='on':
                    number.append((i+1))
                    line=self.input_scrollable_frame_switches_for_left_point[i].get()
                    postion = line.find(',')
                    x=float(line[:postion-1])
                    y=float(line[postion+1:])
                    X.append(x)
                    Y.append(y)
                    if  self.scrollable_frame_switches[i].get() =='on':
                          Control__Point_list.append(str(i+1))
                    if  self.scrollable_frame_switches[i].get() =='off':
                          Check__Point_list.append(str(i+1))
          xy_obs_L=pd.DataFrame({'number':number,'point_x':X,'point_y':Y})            
          if self.checkbox_1.get()=='on':
                  Method='Comformal'
                  if len(Control__Point_list)<2:
                    self.VS0.set('you a least need 2 control points to do Comformal!!')
                    do=False
          elif self.checkbox_2.get()=='on':
                  Method='Afine'
                  if len(Control__Point_list)<3:
                    self.VS0.set('you a least need 3 control points to do Afine!!')
                    do=False
          elif self.checkbox_3.get()=='on':
                  Method='Projetive'
                  if len(Control__Point_list)<4:
                    self.VS0.set('you a least need 4 control points to do Projetive!!')
                    do=False
          else:  
              self.VS0.set('You most chose Method!!')
              do=False
              
          if do==True:
              print(xy_obs_L)
              print(Control__Point_list)
              print
              self.Sensors_L.organize_point(xy_obs_L,Control__Point_list,self.filename_cameraL)
              self.Sensors_L.Mapping_Method(Method)
              self.Sensors_L.Mapping_Method_to_picel()
              text="Method :"+Method+" rmse control points on left sensor= " + str(self.Sensors_L.Rmse_Control)+'\n'+"rmse check  points on left sensor= "+str(self.Sensors_L.Rmse_Check)
              self.Sensors_L_condision='Done'
              self.VS0.set(text)
    def do_Interior_right(self,):
          Method='Projetive'
          do=True
          Control__Point_list,Check__Point_list=[],[]
          X,Y,number=[],[],[]
          for i in range(8):
                
                if  self.Rscrollable_frame_switches_on[i].get()=='on':
                    number.append((i+1))
                    line=self.Rinput_scrollable_frame_switches_for_left_point[i].get()
                    postion = line.find(',')
                    x=float(line[:postion-1])
                    y=float(line[postion+1:])
                    X.append(x)
                    Y.append(y)
                    if  self.scrollable_frame_switches[i].get() =='on':
                          Control__Point_list.append(str(i+1))
                    if  self.scrollable_frame_switches[i].get() =='off':
                          Check__Point_list.append(str(i+1))
          xy_obs_R=pd.DataFrame({'number':number,'point_x':X,'point_y':Y})            
          if self.checkbox_1.get()=='on':
                  Method='Comformal'
                  if len(Control__Point_list)<2:
                    self.VS0.set('you a least need 2 control points to do Comformal!!')
                    do=False
          elif self.checkbox_2.get()=='on':
                  Method='Afine'
                  if len(Control__Point_list)<3:
                    self.VS0.set('you a least need 3 control points to do Afine!!')
                    do=False
          elif self.checkbox_3.get()=='on':
                  Method='Projetive'
                  if len(Control__Point_list)<4:
                    self.VS0.set('you a least need 4 control points to do Projetive!!')
                    do=False
          else:  
              self.VS0.set('You most chose Method!!')
              do=False
              
          if do==True:
              print(Check__Point_list)
              print(Control__Point_list)
              print
              self.Sensors_R.organize_point(xy_obs_R,Control__Point_list,self.filename_cameraR)
              self.Sensors_R.Mapping_Method(Method)
              self.Sensors_R.Mapping_Method_to_picel()
              text="Method :"+Method+" rmse control points on left sensor= " + str(self.Sensors_R.Rmse_Control)+'\n'+"rmse check  points on left sensor= "+str(self.Sensors_R.Rmse_Check)
              self.Sensors_R_condision='Done'
              self.VS0.set(text)
    def InteriorOrientation(self):
        # create main entry and button
            def open_new_leval_1():
                if self.Sensors_R_condision=='none':
                    self.VS0.set('You need to make sure Interior Orientation for right sensor has been done')
                if self.Sensors_L_condision=='none':
                    self.VS0.set('You need to make sure Interior Orientation for left sensor has been done')
                if self.Sensors_L_condision=='Done' and self.Sensors_R_condision=='Done':
                   self.sidebar_button_2.configure(state="normal")
                   self.VS0.set('Nice job')
                   
            self.remove_widgets_based_on_location()  
            self.frame_image_r.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
            self.frame_image_l.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
            
            self.canvasL = customtkinter.CTkCanvas(self.frame_image_l, width= 50, height= 500,background = '#06749b')
            self.canvasL.grid(row=0, column=0, padx=(10, 0), pady=(20, 0), sticky="nsew")


            self.canvasR = customtkinter.CTkCanvas(self.frame_image_r, width= 50, height= 500,background = '#06749b')
            self.canvasR.grid(row=0, column=0, padx=(10, 0), pady=(20, 0), sticky="nsew")
            
            self.Sensors_L_condision='none'
            self.Sensors_R_condision='none'
            self.VS0=StringVar()
            self.entry = customtkinter.CTkEntry(self, placeholder_text="Error Messages",textvariable=self.VS0)
            self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
            
            self.main_button_1 = customtkinter.CTkButton(master=self,text='Submit', fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),command=open_new_leval_1)
            self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

            # create tabview
            self.tabviewL = customtkinter.CTkTabview(self, width=100)
            self.tabviewL.grid(row=1, column=1, padx=(10, 0), pady=(10, 0), sticky="nsew")
            
            self.tabviewL.add("Image Left")
            self.tabviewL.add("Camra File")
            self.tabviewL.tab("Image Left").grid_columnconfigure(1, weight=1)# configure grid of individual tabs
            self.tabviewL.tab("Camra File").grid_columnconfigure(1, weight=1)

            self.input_button1 = customtkinter.CTkButton(self.tabviewL.tab("Image Left"), text="Open Image",
                                                                command=self.left_selection)

            self.input_button3 = customtkinter.CTkButton(self.tabviewL.tab("Camra File"), text="Open Camra File",
                                                                command=self.camera_selectionL)
            self.input_button1.grid(row=2, column=1, padx=20, pady=(5, 5))

            self.input_button3.grid(row=2, column=1, padx=20, pady=(10, 10))
            self.input_button1_1 = customtkinter.CTkButton(self.tabviewL.tab("Image Left"), text="Auto Fill",
                                                                command=self.auto_fill_left)
            self.input_button1_2 = customtkinter.CTkButton(self.tabviewL.tab("Image Left"), text="Interior Orientation",
                                                                command=self.do_Interior_left)
            self.input_button1_2.configure(state="disabled")
            self.tabviewR = customtkinter.CTkTabview(self, width=100)
            self.tabviewR.grid(row=1, column=2, padx=(10, 0), pady=(10, 0), sticky="nsew")
            self.tabviewR.add("Image Right")
            self.tabviewR.add("Camra File")
            self.tabviewR.tab("Image Right").grid_columnconfigure(1, weight=1)
            self.tabviewR.tab("Camra File").grid_columnconfigure(1, weight=1)
            self.input_button3_R = customtkinter.CTkButton(self.tabviewR.tab("Camra File"), text="Open Camra File",
                                                                command=self.camera_selectionR)
            self.input_button2 = customtkinter.CTkButton(self.tabviewR.tab("Image Right"), text="Open Image",
                                                                command=self.right_selection)
            self.input_button2_1 = customtkinter.CTkButton(self.tabviewR.tab("Image Right"), text="Auto Fill",
                                                                command=self.auto_fill_right)
            self.input_button2_2 = customtkinter.CTkButton(self.tabviewR.tab("Image Right"), text="Interior Orientation",
                                                                command=self.do_Interior_right)
            self.input_button2_2.configure(state="disabled")
            
            self.input_button3_R.grid(row=2, column=1, padx=20, pady=(10, 10))
            self.input_button2.grid(row=2, column=1, padx=20, pady=(10, 10))
            self.input_button1_1.grid(row=3, column=1, padx=20, pady=(5, 5))
            self.input_button1_2.grid(row=4, column=1, padx=20, pady=(5, 5))
            self.input_button2_1.grid(row=3, column=1, padx=20, pady=(5, 5))
            self.input_button2_2.grid(row=4, column=1, padx=20, pady=(5, 5))

            # create scrollable frame input
            self.input_scrollable_frame = customtkinter.CTkScrollableFrame(self.tabviewL.tab("Image Left"), label_text="Fiducial Marks Measure")
            self.input_scrollable_frame.grid(row=5, column=1, padx=(20, 0), pady=(10, 0), sticky="nsew")
            self.input_scrollable_frame.grid_columnconfigure(4, weight=3)
            self.input_scrollable_frame.grid_rowconfigure(8, weight=10)
            self.vs_1,self.vs_2,self.vs_3,self.vs_4,self.vs_5,self.vs_6,self.vs_7,self.vs_8= StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar()
            #############################################3
            #left image
            self.inputswitch_xy_1 = customtkinter.CTkEntry(master=self.input_scrollable_frame,textvariable=self.vs_1)
            self.inputswitch_xy_2 = customtkinter.CTkEntry(master=self.input_scrollable_frame,textvariable=self.vs_2)
            self.inputswitch_xy_3 = customtkinter.CTkEntry(master=self.input_scrollable_frame,textvariable=self.vs_3)
            self.inputswitch_xy_4 = customtkinter.CTkEntry(master=self.input_scrollable_frame,textvariable=self.vs_4)
            self.inputswitch_xy_5 = customtkinter.CTkEntry(master=self.input_scrollable_frame,textvariable=self.vs_5)
            self.inputswitch_xy_6 = customtkinter.CTkEntry(master=self.input_scrollable_frame,textvariable=self.vs_6)
            self.inputswitch_xy_7 = customtkinter.CTkEntry(master=self.input_scrollable_frame,textvariable=self.vs_7)
            self.inputswitch_xy_8 = customtkinter.CTkEntry(master=self.input_scrollable_frame,textvariable=self.vs_8)
            self.measure_xy_1 = customtkinter.CTkButton(master=self.input_scrollable_frame,text=f"measure Point {1}", command=self.measure1)
            self.measure_xy_2 = customtkinter.CTkButton(master=self.input_scrollable_frame,text=f"measure Point {2}", command=self.measure2)
            self.measure_xy_3 = customtkinter.CTkButton(master=self.input_scrollable_frame,text=f"measure Point {3}", command=self.measure3)
            self.measure_xy_4 = customtkinter.CTkButton(master=self.input_scrollable_frame,text=f"measure Point {4}", command=self.measure4)
            self.measure_xy_5 = customtkinter.CTkButton(master=self.input_scrollable_frame,text=f"measure Point {5}", command=self.measure5)
            self.measure_xy_6 = customtkinter.CTkButton(master=self.input_scrollable_frame,text=f"measure Point {6}", command=self.measure6)
            self.measure_xy_7 = customtkinter.CTkButton(master=self.input_scrollable_frame,text=f"measure Point {7}", command=self.measure7)
            self.measure_xy_8 = customtkinter.CTkButton(master=self.input_scrollable_frame,text=f"measure Point {8}", command=self.measure8)
            self.tempearaty   = customtkinter.CTkLabel(master=self.input_scrollable_frame,text="").grid(row=9, column=1, padx=10, pady=(10, 10))
            self.tempearaty   = customtkinter.CTkLabel(master=self.input_scrollable_frame,text="").grid(row=10, column=1, padx=10, pady=(10, 10))
            self.tempearaty   = customtkinter.CTkLabel(master=self.input_scrollable_frame,text="").grid(row=11, column=1, padx=10, pady=(10, 10))
            self.inputswitch_xy_1.configure(state="disabled")
            self.input_scrollable_frame_switches_for_left_point=[self.inputswitch_xy_1,self.inputswitch_xy_2,self.inputswitch_xy_3,self.inputswitch_xy_4,self.inputswitch_xy_5,self.inputswitch_xy_6,self.inputswitch_xy_7,self.inputswitch_xy_8]
            self.measure_scrollable_frame_switches_for_left_point=[self.measure_xy_1,self.measure_xy_2,self.measure_xy_3,self.measure_xy_4,self.measure_xy_5,self.measure_xy_6,self.measure_xy_7,self.measure_xy_8]

            self.scrollable_frame_switches_on = []
            for i,(E,M) in enumerate(zip(self.input_scrollable_frame_switches_for_left_point,self.measure_scrollable_frame_switches_for_left_point)):
                E.grid(row=i, column=2, padx=10, pady=(10, 10))
                E.configure(state="disabled")
                M.grid(row=i, column=1, padx=10, pady=(10, 10))
                M.configure(state="disabled")
                
                switch = customtkinter.CTkSwitch(master=self.input_scrollable_frame, text=f"Point {i+1}", onvalue="on", offvalue="off")
                switch.grid(row=i, column=3, padx=10, pady=(10,10))
                self.scrollable_frame_switches_on.append(switch)
                self.scrollable_frame_switches_on[i].configure(state="disabled")
            #############################################3
            #right image
            # create scrollable frame input
            self.Rinput_scrollable_frame = customtkinter.CTkScrollableFrame(self.tabviewR.tab("Image Right"), label_text="Fiducial Marks Measure")
            self.Rinput_scrollable_frame.grid(row=5, column=1, padx=(20, 0), pady=(10, 0), sticky="nsew")
            self.Rinput_scrollable_frame.grid_columnconfigure(4, weight=3)
            self.Rinput_scrollable_frame.grid_rowconfigure(8, weight=10)
            self.Rvs_1,self.Rvs_2,self.Rvs_3,self.Rvs_4,self.Rvs_5,self.Rvs_6,self.Rvs_7,self.Rvs_8= StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar()
            self.Rinputswitch_xy_1 = customtkinter.CTkEntry(master=self.Rinput_scrollable_frame,textvariable=self.Rvs_1)
            self.Rinputswitch_xy_2 = customtkinter.CTkEntry(master=self.Rinput_scrollable_frame,textvariable=self.Rvs_2)
            self.Rinputswitch_xy_3 = customtkinter.CTkEntry(master=self.Rinput_scrollable_frame,textvariable=self.Rvs_3)
            self.Rinputswitch_xy_4 = customtkinter.CTkEntry(master=self.Rinput_scrollable_frame,textvariable=self.Rvs_4)
            self.Rinputswitch_xy_5 = customtkinter.CTkEntry(master=self.Rinput_scrollable_frame,textvariable=self.Rvs_5)
            self.Rinputswitch_xy_6 = customtkinter.CTkEntry(master=self.Rinput_scrollable_frame,textvariable=self.Rvs_6)
            self.Rinputswitch_xy_7 = customtkinter.CTkEntry(master=self.Rinput_scrollable_frame,textvariable=self.Rvs_7)
            self.Rinputswitch_xy_8 = customtkinter.CTkEntry(master=self.Rinput_scrollable_frame,textvariable=self.Rvs_8)
            self.Rmeasure_xy_1 = customtkinter.CTkButton(master=self.Rinput_scrollable_frame,text=f"measure Point {1}", command=self.Rmeasure1)
            self.Rmeasure_xy_2 = customtkinter.CTkButton(master=self.Rinput_scrollable_frame,text=f"measure Point {2}", command=self.Rmeasure2)
            self.Rmeasure_xy_3 = customtkinter.CTkButton(master=self.Rinput_scrollable_frame,text=f"measure Point {3}", command=self.Rmeasure3)
            self.Rmeasure_xy_4 = customtkinter.CTkButton(master=self.Rinput_scrollable_frame,text=f"measure Point {4}", command=self.Rmeasure4)
            self.Rmeasure_xy_5 = customtkinter.CTkButton(master=self.Rinput_scrollable_frame,text=f"measure Point {5}", command=self.Rmeasure5)
            self.Rmeasure_xy_6 = customtkinter.CTkButton(master=self.Rinput_scrollable_frame,text=f"measure Point {6}", command=self.Rmeasure6)
            self.Rmeasure_xy_7 = customtkinter.CTkButton(master=self.Rinput_scrollable_frame,text=f"measure Point {7}", command=self.Rmeasure7)
            self.Rmeasure_xy_8 = customtkinter.CTkButton(master=self.Rinput_scrollable_frame,text=f"measure Point {8}", command=self.Rmeasure8)
            self.Rtempearaty   = customtkinter.CTkLabel(master=self.Rinput_scrollable_frame,text="").grid(row=9, column=1, padx=10, pady=(10, 10))
            self.Rtempearaty   = customtkinter.CTkLabel(master=self.Rinput_scrollable_frame,text="").grid(row=10, column=1, padx=10, pady=(10, 10))
            self.Rtempearaty   = customtkinter.CTkLabel(master=self.Rinput_scrollable_frame,text="").grid(row=11, column=1, padx=10, pady=(10, 10))
            self.inputswitch_xy_1.configure(state="disabled")
            self.Rinput_scrollable_frame_switches_for_left_point=[self.Rinputswitch_xy_1,self.Rinputswitch_xy_2,self.Rinputswitch_xy_3,self.Rinputswitch_xy_4,self.Rinputswitch_xy_5,self.Rinputswitch_xy_6,self.Rinputswitch_xy_7,self.Rinputswitch_xy_8]
            self.Rmeasure_scrollable_frame_switches_for_left_point=[self.Rmeasure_xy_1,self.Rmeasure_xy_2,self.Rmeasure_xy_3,self.Rmeasure_xy_4,self.Rmeasure_xy_5,self.Rmeasure_xy_6,self.Rmeasure_xy_7,self.Rmeasure_xy_8]

            self.Rscrollable_frame_switches_on = []
            for i,(E,M) in enumerate(zip(self.Rinput_scrollable_frame_switches_for_left_point,self.Rmeasure_scrollable_frame_switches_for_left_point)):
                E.grid(row=i, column=2, padx=10, pady=(10, 10))
                E.configure(state="disabled")
                M.grid(row=i, column=1, padx=10, pady=(10, 10))
                M.configure(state="disabled")
                
                switch = customtkinter.CTkSwitch(master=self.Rinput_scrollable_frame, text=f"Point {i+1}", onvalue="on", offvalue="off")
                switch.grid(row=i, column=3, padx=10, pady=(10,10))
                self.Rscrollable_frame_switches_on.append(switch)
                self.Rscrollable_frame_switches_on[i].configure(state="disabled")
                              
             #  
            #    b.configure(state="normal")

            # create scrollable frame
            self.scrollable_frame0 = customtkinter.CTkFrame(self)
            self.scrollable_frame0.grid_columnconfigure(1, weight=0)

            self.scrollable_frame0.grid_rowconfigure(1, weight=0)
            self.scrollable_frame0.grid(row=0, column=3, padx=(0, 0), pady=(0, 0), sticky="nsew")
            self.scrollable_frame = customtkinter.CTkScrollableFrame(master=self.scrollable_frame0, label_text="Fiducial Marks")
            self.scrollable_frame.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
       #     self.tempearaty   = customtkinter.CTkLabel(master=self.input_scrollable_frame,text=""Fiducial Marks"").grid(row=11, column=1, padx=10, pady=(10, 10))
            self.scrollable_frame.grid_columnconfigure(1, weight=0)
            self.scrollable_frame_switches = []
            for i in range(8):
                switch_control = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"Control: {i+1}", onvalue="on", offvalue="off")
                switch_control.grid(row=i, column=1, padx=10, pady=(0, 10))
                self.scrollable_frame_switches.append(switch_control)
                self.scrollable_frame_switches[i].configure(state="disabled")
            # create checkbox and switch frame
            self.checkbox_slider_frame = customtkinter.CTkFrame(self)
            self.checkbox_slider_frame.grid_columnconfigure(0, weight=0)
            self.checkbox_slider_frame.grid_rowconfigure(1, weight=0)
            self.checkbox_slider_frame.grid(row=1, column=3, padx=(10, 10), pady=(20, 0), sticky="nsew")
            self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text="Comformal",command=self.method_C1,onvalue="on", offvalue="off")
            self.checkbox_1.grid(row=1, column=0, pady=(15, 0), padx=5, sticky="n")
            self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text="Afine",command=self.method_C2,onvalue="on", offvalue="off")
            self.checkbox_2.grid(row=2, column=0, pady=(15, 0), padx=5, sticky="n")
            self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,text="Projetive",command=self.method_C3,onvalue="on", offvalue="off")
            self.checkbox_3.grid(row=3, column=0, pady=15, padx=5, sticky="n")

            # set default values
        #    self.sidebar_button_3.configure(state="disabled")
            self.checkbox_1.configure(state="disabled")
            self.checkbox_2.configure(state="disabled")
            self.checkbox_3.configure(state="disabled")
           # self.checkbox_1.select()
 
            
            # load image
           # self.tabview = customtkinter.CTkTabview(self, width=250)


         #   self.canvas.bind('<B1-Motion>',     self.__move_to)  # move canvas to the new position

            # self.canvasR = customtkinter.CTkCanvas(self, width= 500, height= 500,background = '#06749b')
            # self.canvasR.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
            def get_mouse_posn(event):
                    global topx, topy
                    topx, topy = int(self.canvas.canvasx(event.x)), int(self.canvas.canvasy(event.y))
    def method_C1(self):
        print('2')
        if self.checkbox_1.get()=='on':
                self.checkbox_2.configure(state="disabled")
                self.checkbox_3.configure(state="disabled")
        else :
                self.checkbox_2.configure(state="normal")
                self.checkbox_3.configure(state="normal")
    def method_C2(self):
        if self.checkbox_2.get()=='on':
                self.checkbox_1.configure(state="disabled")
                self.checkbox_3.configure(state="disabled")
        else :
                self.checkbox_1.configure(state="normal")
                self.checkbox_3.configure(state="normal")
    def method_C3(self):
        if self.checkbox_3.get()=='on':
                self.checkbox_1.configure(state="disabled")
                self.checkbox_2.configure(state="disabled")
        else :
                self.checkbox_1.configure(state="normal")
                self.checkbox_2.configure(state="normal")
    def measure1(self,):
        self.vs_1.set('{} , {}'.format(round(self.point_x_L,3),round(self.point_y_L,3)))
        self.scrollable_frame_switches_on[0].configure(state="normal")
        self.scrollable_frame_switches[0].configure(state="normal")
        self.scrollable_frame_switches_on[0].select()
        self.scrollable_frame_switches[0].select()
    def measure2(self,):
        self.vs_2.set('{} , {}'.format(round(self.point_x_L,3),round(self.point_y_L,3)))
        self.scrollable_frame_switches_on[1].configure(state="normal")
        self.scrollable_frame_switches[1].configure(state="normal")
        self.scrollable_frame_switches_on[1].select()
        self.scrollable_frame_switches[1].select()
    def measure3(self,):
        self.vs_3.set('{} , {}'.format(round(self.point_x_L,3),round(self.point_y_L,3)))
        self.scrollable_frame_switches_on[2].configure(state="normal")
        self.scrollable_frame_switches[2].configure(state="normal")
        self.scrollable_frame_switches_on[2].select()
        self.scrollable_frame_switches[2].select()
    def measure4(self,):
        self.vs_4.set('{} , {}'.format(round(self.point_x_L,3),round(self.point_y_L,3)))
        self.scrollable_frame_switches_on[3].configure(state="normal")
        self.scrollable_frame_switches[3].configure(state="normal")
        self.scrollable_frame_switches_on[3].select()
        self.scrollable_frame_switches[3].select()
    def measure5(self,):
        self.vs_5.set('{} , {}'.format(round(self.point_x_L,3),round(self.point_y_L,3)))
        self.scrollable_frame_switches_on[4].configure(state="normal")
        self.scrollable_frame_switches[4].configure(state="normal")
        self.scrollable_frame_switches_on[4].select()
        self.scrollable_frame_switches[4].select()
    def measure6(self,):
        self.vs_6.set('{} , {}'.format(round(self.point_x_L,3),round(self.point_y_L,3)))
        self.scrollable_frame_switches_on[5].configure(state="normal")
        self.scrollable_frame_switches[5].configure(state="normal")
        self.scrollable_frame_switches_on[5].select()
        self.scrollable_frame_switches[5].select()
    def measure7(self,):
        self.vs_7.set('{} , {}'.format(round(self.point_x_L,3),round(self.point_y_L,3)))
        self.scrollable_frame_switches_on[6].configure(state="normal")
        self.scrollable_frame_switches[6].configure(state="normal")
        self.scrollable_frame_switches_on[6].select()
        self.scrollable_frame_switches[6].select()
    def measure8(self,):
        self.vs_8.set('{} , {}'.format(round(self.point_x_L,3),round(self.point_y_L,3)))
        self.scrollable_frame_switches_on[7].configure(state="normal")
        self.scrollable_frame_switches[7].configure(state="normal")
        self.scrollable_frame_switches_on[7].select()
        self.scrollable_frame_switches[7].select()
    def auto_fill_left(self):
        self.vs_1.set('{} , {}'.format(989.858 , 498.907))
        self.vs_2.set('{} , {}'.format(9.179 , 499.346))
        self.vs_3.set('{} , {}'.format(499.616 , 9.073))
        self.vs_4.set('{} , {}'.format(499.64 , 989.876))
        self.vs_5.set('{} , {}'.format(989.852 , 9.497))
        self.vs_6.set('{} , {}'.format(9.34 , 989.39))
        self.vs_7.set('{} , {}'.format(9.243 , 9.031))
        self.vs_8.set('{} , {}'.format(989.593 , 989.408))
        for i in range(8):
            self.scrollable_frame_switches_on[i].configure(state="normal")
            self.scrollable_frame_switches[i].configure(state="normal")
            self.scrollable_frame_switches_on[i].select()
            self.scrollable_frame_switches[i].select()
#### RIGHT
    def Rmeasure1(self,):
        self.Rvs_1.set('{} , {}'.format(round(self.point_x_R,3),round(self.point_y_R,3)))
        self.Rscrollable_frame_switches_on[0].configure(state="normal")
        self.scrollable_frame_switches[0].configure(state="normal")
        self.Rscrollable_frame_switches_on[0].select()
        self.scrollable_frame_switches[0].select()
    def Rmeasure2(self,):
        self.Rvs_2.set('{} , {}'.format(round(self.point_x_R,3),round(self.point_y_R,3)))
        self.Rscrollable_frame_switches_on[1].configure(state="normal")
        self.scrollable_frame_switches[1].configure(state="normal")
        self.Rscrollable_frame_switches_on[1].select()
        self.scrollable_frame_switches[1].select()
    def Rmeasure3(self,):
        self.Rvs_3.set('{} , {}'.format(round(self.point_x_R,3),round(self.point_y_R,3)))
        self.Rscrollable_frame_switches_on[2].configure(state="normal")
        self.scrollable_frame_switches[2].configure(state="normal")
        self.Rscrollable_frame_switches_on[2].select()
        self.scrollable_frame_switches[2].select()
    def Rmeasure4(self,):
        self.Rvs_4.set('{} , {}'.format(round(self.point_x_R,3),round(self.point_y_R,3)))
        self.Rscrollable_frame_switches_on[3].configure(state="normal")
        self.scrollable_frame_switches[3].configure(state="normal")
        self.Rscrollable_frame_switches_on[3].select()
        self.scrollable_frame_switches[3].select()
    def Rmeasure5(self,):
        self.Rvs_5.set('{} , {}'.format(round(self.point_x_R,3),round(self.point_y_R,3)))
        self.Rscrollable_frame_switches_on[4].configure(state="normal")
        self.scrollable_frame_switches[4].configure(state="normal")
        self.Rscrollable_frame_switches_on[4].select()
        self.scrollable_frame_switches[4].select()
    def Rmeasure6(self,):
        self.Rvs_6.set('{} , {}'.format(round(self.point_x_R,3),round(self.point_y_R,3)))
        self.Rscrollable_frame_switches_on[5].configure(state="normal")
        self.scrollable_frame_switches[5].configure(state="normal")
        self.Rscrollable_frame_switches_on[5].select()
        self.scrollable_frame_switches[5].select()
    def Rmeasure7(self,):
        self.Rvs_7.set('{} , {}'.format(round(self.point_x_R,3),round(self.point_y_R,3)))
        self.Rscrollable_frame_switches_on[6].configure(state="normal")
        self.scrollable_frame_switches[6].configure(state="normal")
        self.Rscrollable_frame_switches_on[6].select()
        self.scrollable_frame_switches[6].select()
    def Rmeasure8(self,):
        self.Rvs_8.set('{} , {}'.format(round(self.point_x_R,3),round(self.point_y_R,3)))
        self.Rscrollable_frame_switches_on[7].configure(state="normal")
        self.scrollable_frame_switches[7].configure(state="normal")
        self.Rscrollable_frame_switches_on[7].select()
        self.scrollable_frame_switches[7].select()
    def auto_fill_right(self):
        self.Rvs_1.set('{} , {}'.format(989.835 , 499.719))
        self.Rvs_2.set('{} , {}'.format(9.325 , 499.228))
        self.Rvs_3.set('{} , {}'.format(499.729 , 9.492))
        self.Rvs_4.set('{} , {}'.format(499.697 , 989.093))
        self.Rvs_5.set('{} , {}'.format(989.589 , 9.628))
        self.Rvs_6.set('{} , {}'.format(9.177 , 988.911))
        self.Rvs_7.set('{} , {}'.format(9.328 , 9.087))
        self.Rvs_8.set('{} , {}'.format(989.318 , 989.429))
        for i in range(8):
            self.Rscrollable_frame_switches_on[i].configure(state="normal")
            self.scrollable_frame_switches[i].configure(state="normal")
            self.Rscrollable_frame_switches_on[i].select()
            self.scrollable_frame_switches[i].select()
    # #move
    def motion_L(self,event):
        box_image = self.canvasL.canvas.coords(self.canvasL.container) 
        # Get scroll region box
        box_canvas = (self.canvasL.canvas.canvasx(0),  # get visible area of the canvas
                      self.canvasL.canvas.canvasy(0),
                      self.canvasL.canvas.canvasx(self.canvasL.canvas.winfo_width()),
                      self.canvasL.canvas.canvasy(self.canvasL.canvas.winfo_height()))
        x1 = max(box_canvas[0] - box_image[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
        y1 = max(box_canvas[1] - box_image[1], 0)
        self.x0_L=(event.x+x1)/self.canvasL.scaleE
        self.y0_L=(event.y+y1)/self.canvasL.scaleE
        self.x0_for_drow=self.canvasL.canvas.canvasx(event.x)
        self.y0_for_drow=self.canvasL.canvas.canvasx(event.y)
        self.textL='({}, {})'.format(round(self.x0_L,3),round(self.y0_L,3))
        tag='lll'
        self.canvasL.canvas.delete(tag)
        self.canvasL.canvas.create_text(-40+self.x0_for_drow,+40+self.y0_for_drow,fill="red",font="Times 8 italic bold",text=self.textL,tags=tag)
  #     self.canvasL.canvas.update
    def motion_R(self,event):
        box_image = self.canvasR.canvas.coords(self.canvasR.container) 
        # Get scroll region box
        box_canvas = (self.canvasR.canvas.canvasx(0),  # get visible area of the canvas
                      self.canvasR.canvas.canvasy(0),
                      self.canvasR.canvas.canvasx(self.canvasR.canvas.winfo_width()),
                      self.canvasR.canvas.canvasy(self.canvasR.canvas.winfo_height()))
        x1 = max(box_canvas[0] - box_image[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
        y1 = max(box_canvas[1] - box_image[1], 0)
        self.x0_R=(event.x+x1)/self.canvasR.scaleE
        self.y0_R=(event.y+y1)/self.canvasR.scaleE
        
        self.textR='({}, {})'.format(round(self.x0_R,3),round(self.y0_R,3))
        tag='RRR'
        self.canvasR.canvas.delete(tag)
        self.canvasR.canvas.create_text(-40+self.canvasR.canvas.canvasx(event.x),+40+self.canvasR.canvas.canvasy(event.y),fill="darkblue",font="Times 8 italic bold",text=self.textR,tags=tag)
    def point_select_LEFT(self,event):
        self.point_x_L = self.x0_L
        self.point_y_L = self.y0_L
        self.point_x_L_for_drow=self.x0_for_drow
        self.point_y_L_for_drow=self.y0_for_drow
        # x=event.x
        # y=event.y
        x = self.canvasL.canvas.canvasx(event.x)  # get coordinates of the event on the canvas
        y = self.canvasL.canvas.canvasy(event.y)
        myrtag='L({},{})'.format(round(self.point_x_L,2) ,round(self.point_y_L,2) )
        self.tagesL.append(myrtag)
        r=5
        color = ('red', 'orange', 'yellow', 'green', 'blue')[0]
     #   self.canvas.canvas.create_circle(x1, y1, 50, fill="blue", outline="#DDD", width=4)
        self.canvasL.canvas.create_oval(x-r, y-r, x+r, y+r,fill=color,tags=myrtag)
    def point_select_RIGHT(self,event):
      self.point_x_R = self.x0_R
      self.point_y_R = self.y0_R
      
      # x=event.x
      # y=event.y
      x = self.canvasR.canvas.canvasx(event.x)  # get coordinates of the event on the canvas
      y = self.canvasR.canvas.canvasy(event.y)
      myrtag='R({},{})'.format(round(self.point_x_R,3) ,round(self.point_y_R,3) )
      self.tagesR.append(myrtag)
      r=5
      color = ('red', 'orange', 'yellow', 'green', 'blue')[4]
   #   self.canvas.canvas.create_circle(x1, y1, 50, fill="blue", outline="#DDD", width=4)
      self.canvasR.canvas.create_oval(x-r, y-r, x+r, y+r,fill=color,tags=self.tagesR[-1])

    def point_select_deleteL(self,event):
          self.canvasL.canvas.delete(self.tagesL[-1])
          self.tagesL=self.tagesL[:-1]
    def point_select_deleteR(self,event):
          self.canvasR.canvas.delete(self.tagesR[-1])
          self.tagesR=self.tagesR[:-1]

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())
    def left_selection(self):
                self.input_button1.configure(text="Loading...")
                self.filename_left=  filedialog.askopenfilename(initialdir = "/",title = "Select Left Image",filetypes = (("png","*.png"),("jpeg","*.jpeg"),("all files","*.*")))
                self.input_button1.configure(text="Left image selected")
                
                self.canvasL = CanvasImage(self.frame_image_l, self.filename_left)  # create widget
                self.canvasL.canvas.destroy()
                self.canvasL = CanvasImage(self.frame_image_l, self.filename_left)  # create widget
                self.canvasL.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")
                self.canvasL.canvas.bind('<Motion>', self.motion_L)
                self.canvasL.canvas.bind('<ButtonPress-3>', self.point_select_LEFT)
                self.canvasL.canvas.bind('<ButtonPress-2>', self.point_select_deleteL)
                self.text_text = self.canvasL.canvas.create_text(0, 0, anchor='nw', text=self.canvasL.text)
                for E,M in zip(self.input_scrollable_frame_switches_for_left_point,self.measure_scrollable_frame_switches_for_left_point):
                    E.configure(state="normal")
                    M.configure(state="normal")
              # ADD IMAGE LEFT
                self.Sensors_L=Interior_Orientation(self.filename_left)
    def right_selection(self):
                self.input_button2.configure(text="Loading...")
                self.filename_right=  filedialog.askopenfilename(initialdir = "/",title = "Select Right Image",filetypes = (("png","*.png"),("jpeg","*.jpeg"),("all files","*.*")))
                
                self.input_button2.configure(text="Right image selected")
                self.canvasR = CanvasImage(self.frame_image_r, self.filename_right)  # create widget
                self.canvasR.canvas.destroy()
                self.canvasR = CanvasImage(self.frame_image_r, self.filename_right)  # create widget
                self.canvasR.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")
                self.canvasR.canvas.bind('<Motion>', self.motion_R)
                self.canvasR.canvas.bind('<ButtonPress-3>', self.point_select_RIGHT)
                self.canvasR.canvas.bind('<ButtonPress-2>', self.point_select_deleteR)
                self.text_text = self.canvasR.canvas.create_text(0, 0, anchor='nw', text=self.canvasR.text)
                for E,M in zip(self.Rinput_scrollable_frame_switches_for_left_point,self.Rmeasure_scrollable_frame_switches_for_left_point):
                    E.configure(state="normal")
                    M.configure(state="normal")
             # ADD IMAGE  RIGHT
                self.Sensors_R=Interior_Orientation(self.filename_right)
                self.sidebar_button_4.configure(state="normal")
                self.sidebar_button_5.configure(state="normal")
    def camera_selectionL(self):
                self.input_button3.configure(text="Loading...")
                self.filename_cameraL=  filedialog.askopenfilename(initialdir = "/",title = "Camera Calibration File",filetypes = (("txt","*.txt"),("all files","*.*")))
                self.input_button3.configure(text="Camera Calibration selected")
                self.input_button1_2.configure(state="normal")
                self.checkbox_1.configure(state="normal")
                self.checkbox_2.configure(state="normal")
                self.checkbox_3.configure(state="normal")
    def camera_selectionR(self):
                self.input_button3_R.configure(text="Loading...")
                self.filename_cameraR=  filedialog.askopenfilename(initialdir = "/",title = "Camera Calibration File",filetypes = (("txt","*.txt"),("all files","*.*")))
                self.input_button3_R.configure(text="Camera Calibration selected")
                self.input_button2_2.configure(state="normal")
                self.checkbox_1.configure(state="normal")
                self.checkbox_2.configure(state="normal")
                self.checkbox_3.configure(state="normal")
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")
   
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------



    def ReletiveOrientation(self):
           self.remove_widgets_based_on_location()
          # self.makait_work()
           camera_name,self.focal_length,fiducial_coordinates,Camera_distortions=Read_Camera(self.filename_cameraL)
           self.frame_image_l.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
           self.frame_image_r.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        # do -----------------------------------
           # create KONWONS frame
           self.RO_1,self.RO_2,self.RO_3,self.RO_4,self.RO_5,self.RO_6,self.RO_7,self.RO_8,self.RO_9,self.RO_10,self.RO_11,self.RO_12= StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar()
           self.RO=[self.RO_1,self.RO_2,self.RO_3,self.RO_4,self.RO_5,self.RO_6,self.RO_7,self.RO_8,self.RO_9,self.RO_10,self.RO_11,self.RO_12]
### result printing
           self.frame01 = customtkinter.CTkFrame(self)
           self.frame01.grid_columnconfigure(1, weight=0)
           self.frame01.grid_rowconfigure(5, weight=0)
           self.frame01.grid(row=0, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
           for i in range(6):
             self.labale_ro = customtkinter.CTkLabel(master=self.frame01,textvariable=self.RO[i]).grid(row=i, column=0, padx=10, pady=(10, 10))
             self.labale_ro_input = customtkinter.CTkLabel(master=self.frame01,textvariable=self.RO[i+6]).grid(row=i, column=1, padx=10, pady=(10, 10))
           self.RO_1.set('Omega :')
           self.RO_2.set('Phi   :'),
           self.RO_3.set('Kappa :'),
           self.RO_4.set('By    :')
           self.RO_5.set('Bz    :')   
           self.RO_6.set('Bx    :')
           self.RO_12.set(str(self.focal_length))
           self.rato=StringVar()
           
 # oprations          
           self.frame02 = customtkinter.CTkFrame(self)
           self.frame02.grid_columnconfigure(1, weight=0)
           self.frame02.grid_rowconfigure(5, weight=0)
           self.frame02.grid(row=1, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
           self.ro_get_match   = customtkinter.CTkButton(master=self.frame01,text=f"Extract Matched Points", command=self.ExtractMatchedPoints)
           self.rato_box   = customtkinter.CTkEntry(master=self.frame01,textvariable=self.rato)
           self.ro_start   = customtkinter.CTkButton(master=self.frame02,text=f"Reletive Orientation", command=self.Initialize_ReletiveOrientation)
           self.re_see     = customtkinter.CTkButton(master=self.frame02,text=f"streo view", command=self.see_streo)
     #      self.Rmeasure_xy_8 = customtkinter.CTkButton(master=self.Rinput_scrollable_frame,text=f"measure Point {8}", command=self.Rmeasure8)
           self.ro_start.grid(row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
           self.re_see.grid(row=2, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
           self.ro_get_match.grid(row=8, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
           self.rato_box.grid(row=8, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
           self.re_see.configure(state="disabled")
           self.ro_start.configure(state="disabled")
           self.rato.set('0.35')
    def ExtractMatchedPoints(self):
        
        # PART 2 
        RatioTest=float(self.rato.get())
        self.Streo=StreoImages(self.Sensors_L,self.Sensors_R)
        self.Streo.ExtractMatchedPoints(RatioTest=0.35)        
        self.point_driwnig(self.Streo.ptsLeft_pixcel,self.Streo.ptsRight_pixcel)
        self.ro_start.configure(state="normal")
        
    def Initialize_ReletiveOrientation(self):
        
        # PART 2 
        self.projective_matrix=self.Streo.Initialize_Relative_orientation_in_pp(self.focal_length,0.000001)
        self.RO_7.set(str(self.Streo.Relative_orientation.omega))
        self.RO_8.set(str(self.Streo.Relative_orientation.phi)),
        self.RO_9.set(str(self.Streo.Relative_orientation.kappa)),
        self.RO_10.set(str(self.Streo.Relative_orientation.By))
        self.RO_11.set(str(self.Streo.Relative_orientation.Bz)) 
        self.re_see.configure(state="normal")
        self.sidebar_button_3.configure(state="normal")
        self.ReletiveOrientation_stase=True
        
        self.point_driwnig(self.Streo.Relative_orientation.xy_pixcel_L,self.Streo.Relative_orientation.xy_pixcel_R)
        self.VS0.set('Reletive Orientation Rmse :' +str(self.Streo.Relative_orientation.Rmse))
    def see_streo(self):
        self.frame_image_l.grid_forget()
        self.frame_image_r.grid_forget()
        img = self.Streo.Sensors_R_New.copy()
        img_L = self.Sensors_L.img.copy()
        img_L[:,:,0]=img[:,:,1]
        self.frame_streo = customtkinter.CTkFrame(self)
        self.frame_streo.grid(row=0, column=1,rowspan=1,columnspan=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        cv2.imwrite('streo.png',img_L)
      #  self.frame_streo.grid_columnconfigure(1, weight = 2, uniform=1) 
    #    self.canvas_streo = CanvasImage(self.frame_streo, self.filename_left)  # create widget
        self.canvas_streo = CanvasImage(self.frame_streo, 'streo.png')  # create widget
        self.canvas_streo.grid(row=0, column=0, padx=(10, 0), pady=(20, 0), sticky="news")

    def point_driwnig(self,matchig_pixcel_L,matchig_pixcel_R):

     # CREATE A rectangle

     img=self.Sensors_R.img.copy()
     for x,y in zip(matchig_pixcel_R.x,matchig_pixcel_R.y):
        img = cv2.circle(img, (int(x),int(y)), 2, (255, 0, 0), 2)
     cv2.imwrite(r"cash\new_R.png",img)
     self.canvasR.canvas.destroy()
     self.canvasR = CanvasImage(self.frame_image_r, r'cash\new_R.png') 
     self.canvasR.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")
     self.canvasR.canvas.bind('<Motion>', self.motion_R)
     self.canvasR.canvas.bind('<ButtonPress-3>', self.point_select_RIGHT)
     self.canvasR.canvas.bind('<ButtonPress-2>', self.point_select_deleteR)
     # Point
     img1=self.Sensors_L.img.copy()
     for x,y in zip(matchig_pixcel_L.x,matchig_pixcel_L.y):
         
        img1 = cv2.circle(img1, (int(x),int(y)), 2, (0, 0, 255), 2)
     cv2.imwrite(r"cash\new_L.png",img1)
     self.canvasL.canvas.destroy()
     self.canvasL = CanvasImage(self.frame_image_l, r'cash\new_L.png') 
     self.canvasL.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")
     self.canvasL.canvas.bind('<Motion>', self.motion_L)
     self.canvasL.canvas.bind('<ButtonPress-3>', self.point_select_LEFT)
     self.canvasL.canvas.bind('<ButtonPress-2>', self.point_select_deleteL)
        
        
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
    def VLL(self):
      self.remove_widgets_based_on_location()
     # self.makait_work()
      self.frame_image_l.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
      self.frame_image_r.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
      self.match_window_l.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
      self.match_window_r.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
      self.frame_vll_01 = customtkinter.CTkFrame(self)
      self.frame_vll_01.grid(row=0, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
      self.frame_vll_02 = customtkinter.CTkFrame(self)
      self.frame_vll_02.grid(row=1, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
     
     
      self.canvasL_W=customtkinter.CTkCanvas(master=self.match_window_l, width= 50, height= 50,background = '#06748b')
      self.canvasL_W.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")
      self.canvasR_W=customtkinter.CTkCanvas(master=self.match_window_r, width= 50, height= 50,background = '#06748b')
      self.canvasR_W.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")
 

     
   #   self.vll_labale1   = customtkinter.CTkLabel(master=self.frame_vll_01,text="Inputs :").grid(row=0, column=0, padx=10, pady=(10, 10))
      self.vll_labale2   = customtkinter.CTkLabel(master=self.frame_vll_01,text="Window Size :").grid(row=1, column=0, padx=10, pady=(5, 5))
      self.vll_labale3   = customtkinter.CTkLabel(master=self.frame_vll_01,text="Start Step  :").grid(row=2, column=0, padx=10, pady=(5, 5))
      self.vll_labale4   = customtkinter.CTkLabel(master=self.frame_vll_01,text="Model X :").grid(row=4, column=0, padx=10, pady=(5, 5))
      self.vll_labale5   = customtkinter.CTkLabel(master=self.frame_vll_01,text="Model Y :").grid(row=6, column=0, padx=10, pady=(5, 5))
      
      self.vll_xp_l=StringVar()
      self.vll_yp_l=StringVar()
      self.vll_xp_r=StringVar()
      self.vll_yp_r=StringVar()
      self.vll_labale11   = customtkinter.CTkLabel(master=self.frame_vll_02,textvariable=self.vll_xp_l).grid(row=0, column=1, padx=10, pady=(5, 5))
      self.vll_labale21   = customtkinter.CTkLabel(master=self.frame_vll_02,textvariable=self.vll_yp_l).grid(row=1, column=1, padx=10, pady=(5, 5))
      self.vll_labale31   = customtkinter.CTkLabel(master=self.frame_vll_02,textvariable=self.vll_xp_r).grid(row=2, column=1, padx=10, pady=(5, 5))
      self.vll_labale41   = customtkinter.CTkLabel(master=self.frame_vll_02,textvariable=self.vll_yp_r).grid(row=3, column=1, padx=10, pady=(5, 5))
      self.vll_labale11   = customtkinter.CTkLabel(master=self.frame_vll_02,text="left  image xp :").grid(row=0, column=0, padx=10, pady=(5, 5))
      self.vll_labale22   = customtkinter.CTkLabel(master=self.frame_vll_02,text="left  image yp :").grid(row=1, column=0, padx=10, pady=(5, 5))
      self.vll_labale33   = customtkinter.CTkLabel(master=self.frame_vll_02,text="right image xp :").grid(row=2, column=0, padx=10, pady=(5, 5))
      self.vll_labale44   = customtkinter.CTkLabel(master=self.frame_vll_02,text="right image yp :").grid(row=3, column=0, padx=10, pady=(5, 5))
      self.vll_xp_l.set('')
      self.vll_yp_l.set('')
      self.vll_xp_r.set('')
      self.vll_yp_r.set('')
   #   frame_NCC_01
      self.vll_window=StringVar()
      self.vll_step=StringVar()
      self.X_VLL=StringVar()
      self.Y_VLL=StringVar()
      self.vll_grid_step=StringVar()
      self.vll_windos_input = customtkinter.CTkEntry(master=self.frame_vll_01,textvariable=self.vll_window)
      self.vll_windos_input .grid(row=1, column=1, padx=10, pady=(5, 5))
      self.vll_setep_input_x= customtkinter.CTkEntry(master=self.frame_vll_01,textvariable=self.vll_step)
      self.vll_setep_input_x .grid(row=2, column=1, padx=10, pady=(5, 5)) 
      self.vll_model_x= customtkinter.CTkEntry(master=self.frame_vll_01,textvariable=self.X_VLL)
      self.vll_model_x .grid(row=4, column=1, padx=10, pady=(5, 5)) 
      self.vll_model_y= customtkinter.CTkEntry(master=self.frame_vll_01,textvariable=self.Y_VLL)
      self.vll_model_y .grid(row=6, column=1, padx=10, pady=(5, 5)) 
      self.vll_setep= customtkinter.CTkEntry(master=self.frame_vll_01,textvariable=self.vll_grid_step)
      self.vll_setep .grid(row=8, column=1, padx=10, pady=(5, 5)) 
            
      self.find_LSM_match = customtkinter.CTkButton(master=self.frame_vll_01,text=f"Show the matchs", command=self.vll_matching)
      self.find_LSM_match .grid(row=7, column=1, padx=10, pady=(5, 5))
      self.VLL_GRID = customtkinter.CTkButton(master=self.frame_vll_01,text=f"Build a Grid", command=self.vllg_rid)
      self.VLL_GRID .grid(row=9, column=1, padx=10, pady=(5, 5))
     # self.find_LSM_match = customtkinter.CTkButton(master=self.frame_vll_01,text=f"Affine geometry", command=self.Find_in_full_image)
     # self.find_LSM_match .grid(row=5, column=1, padx=10, pady=(5, 5))
     # self.find_LSM_match = customtkinter.CTkButton(master=self.frame_vll_01,text=f"Geometry and radiometric", command=self.Find_by_guideness)
     # self.find_LSM_match .grid(row=6, column=1, padx=10, pady=(5, 5))
      self.Model_X_range=round(min(self.Streo.Relative_orientation.Geo.X),2),round(max(self.Streo.Relative_orientation.Geo.X),2)
      self.Model_Y_range=round(min(self.Streo.Relative_orientation.Geo.Y),2),round(max(self.Streo.Relative_orientation.Geo.Y),2)
      text_x=str(self.Model_X_range[0]) +' , '+str(self.Model_X_range[1])
      text_y=str(self.Model_Y_range[0]) +' , '+str(self.Model_Y_range[1])
      self.vll_labale4   = customtkinter.CTkLabel(master=self.frame_vll_01,text='Model X Range : ').grid(row=3, column=0, padx=10, pady=(5, 5))
      self.vll_labale5   = customtkinter.CTkLabel(master=self.frame_vll_01,text='Model Y Range : ').grid(row=5, column=0, padx=10, pady=(5, 5))
      self.vll_labale5   = customtkinter.CTkLabel(master=self.frame_vll_01,text='Model Step    : ').grid(row=8, column=0, padx=10, pady=(5, 5))
      self.vll_labale4   = customtkinter.CTkLabel(master=self.frame_vll_01,text=text_x).grid(row=3, column=1, padx=10, pady=(5, 5))
      self.vll_labale5   = customtkinter.CTkLabel(master=self.frame_vll_01,text=text_y).grid(row=5, column=1, padx=10, pady=(5, 5))
                  
      self.vll_window.set('55')
      self.vll_step.set('10')
      self.vll_grid_step.set('20')
    def vllg_rid(self): 
        size   =int(self.vll_window.get())
        step   =float(self.vll_step.get())
        gerid_step=float(self.vll_step.get())
        if 25<size :
         # matching 
           try:
             self.Streo.ploting(step,gerid_step,size)
             self.point_driwnig(self.Streo.VLL_matchig_pixcel_L,self.Streo.VLL_matchig_pixcel_R)
             self.VS0.set('')
           except:
             self.VS0.set('sorry somting went wrong look back to your inputs')

        else:
            self.VS0.set('Serech area most be biger than 25 pixcel')      
    def vll_matching(self): 
       size   =int(self.vll_window.get())
       step   =float(self.vll_step.get())
       Model_X=float((self.X_VLL.get()))
       Model_Y=float((self.Y_VLL.get()))
       if 3<size :
        if Model_X>self.Model_X_range[0] and Model_X<self.Model_X_range[1]:
         if Model_Y>self.Model_Y_range[0] and Model_Y<self.Model_Y_range[1]:
        # matching 
          try:

            matchig_pixcel_L,matchig_pixcel_R,Z=self.Streo.Initialize_VLL(Model_X,Model_Y,step,shift=size)
            self.left_changes(size,matchig_pixcel_L)
            self.right_changes(size,matchig_pixcel_R)
            self.VS0.set('')
          except:
            self.VS0.set('sorry somting went wrong')
          else:
                self.VS0.set('Model Y in not in the Range')
        else:
                    self.VS0.set('Model Y in not in the Range')
       else:
           self.VS0.set('Serech area most be biger')
      
          
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
    def method_ncc1(self):
        for i in  range(6):
          if self.ncc_checkbox[i].get()=='off':
           for ii in range(i):
                 self.ncc_checkbox[ii].configure(state="normal")
           for jj in range(6-i-1):
            self.ncc_checkbox[jj+i+1].configure(state="normal")
            self.find_ncc_match1.configure(state='disabled')
            self.find_ncc_match2.configure(state='disabled')
            self.find_ncc_match3.configure(state='disabled') 
            self.grid_ncc_.configure(state='disabled')
        for i in  range(6):
          if self.ncc_checkbox[i].get()=='on':
            self.method_ncc=self.ncc_methods_i[i]
            for ii in range(i):
                 self.ncc_checkbox[ii].configure(state="disabled")
            for jj in range(6-i-1):
                  self.ncc_checkbox[jj+i+1].configure(state="disabled")
            self.find_ncc_match1.configure(state='normal')
            self.find_ncc_match2.configure(state='normal')
            self.find_ncc_match3.configure(state='normal')  
            self.grid_ncc_.configure(state='normal')
      


#---------------------------------------------------------------------------------------------------------------------------------------------------------------
    def NCC(self):
      self.remove_widgets_based_on_location()
      self.frame_NCC_01 = customtkinter.CTkFrame(self)
      self.frame_NCC_02 = customtkinter.CTkFrame(self)
      #self.makait_work()
      self.frame_image_l.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
      self.frame_image_r.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
      self.match_window_l.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
      self.match_window_r.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
      self.frame_NCC_01.grid(row=0, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
      self.frame_NCC_02.grid(row=1, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")  
      
      
      self.canvasL_W=customtkinter.CTkCanvas(master=self.match_window_l, width= 50, height= 50,background = '#06748b')
      self.canvasL_W.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")
      self.canvasR_W=customtkinter.CTkCanvas(master=self.match_window_r, width= 50, height= 50,background = '#06748b')
      self.canvasR_W.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")
   #   self.frame_NCC_02.grid(row=1, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew") 

      
    #  self.ncc_labale1   = customtkinter.CTkLabel(master=self.frame_NCC_01,text="Inputs :").grid(row=0, column=0, padx=10, pady=(10, 10))
      self.ncc_labale2   = customtkinter.CTkLabel(master=self.frame_NCC_01,text="Window size     :").grid(row=0, column=0, padx=10, pady=(0, 5))
      self.ncc_labale3   = customtkinter.CTkLabel(master=self.frame_NCC_01,text="Serech Area size x:").grid(row=1, column=0, padx=10, pady=(5, 5))
      self.ncc_labale4   = customtkinter.CTkLabel(master=self.frame_NCC_01,text="Serech Area size y:").grid(row=2, column=0, padx=10, pady=(5, 10))
      
      self.ncc_xp_l=StringVar()
      self.ncc_yp_l=StringVar()
      self.ncc_xp_r=StringVar()
      self.ncc_yp_r=StringVar()
      self.ncc_labale11   = customtkinter.CTkLabel(master=self.frame_NCC_02,textvariable=self.ncc_xp_l).grid(row=0, column=1, padx=10, pady=(7, 7))
      self.ncc_labale21   = customtkinter.CTkLabel(master=self.frame_NCC_02,textvariable=self.ncc_yp_l).grid(row=1, column=1, padx=10, pady=(7, 7))
      self.ncc_labale31   = customtkinter.CTkLabel(master=self.frame_NCC_02,textvariable=self.ncc_xp_r).grid(row=2, column=1, padx=10, pady=(7, 7))
      self.ncc_labale41   = customtkinter.CTkLabel(master=self.frame_NCC_02,textvariable=self.ncc_yp_r).grid(row=3, column=1, padx=10, pady=(7, 7))
      self.ncc_labale11   = customtkinter.CTkLabel(master=self.frame_NCC_02,text="left  image xp :").grid(row=0, column=0, padx=10, pady=(7, 7))
      self.ncc_labale22   = customtkinter.CTkLabel(master=self.frame_NCC_02,text="left  image yp :").grid(row=1, column=0, padx=10, pady=(7, 7))
      self.ncc_labale33   = customtkinter.CTkLabel(master=self.frame_NCC_02,text="right image xp :").grid(row=2, column=0, padx=10, pady=(7, 7))
      self.ncc_labale44   = customtkinter.CTkLabel(master=self.frame_NCC_02,text="right image yp :").grid(row=3, column=0, padx=10, pady=(7, 7))
      
      self.checkbox_slider_ncc = customtkinter.CTkFrame(self.frame_NCC_01)
      self.checkbox_slider_ncc.grid_columnconfigure(0, weight=0)
      self.checkbox_slider_ncc.grid_rowconfigure(1, weight=0)
      self.checkbox_slider_ncc.grid(row=8, column=1, padx=(7, 10), pady=(10, 0), sticky="nsew")
      self.ncc_checkbox=[]
      methods =[ 'TM_CCORR_NORMED', 'TM_CCOEFF_NORMED','TM_SQDIFF_NORMED' ,
                 'TM_CCORR       ', 'TM_CCOEFF       ','TM_SQDIFF       ' ]

      self.ncc_methods_i = [cv2.TM_CCORR_NORMED, cv2.TM_CCOEFF_NORMED,cv2.TM_SQDIFF_NORMED,
                             cv2.TM_CCORR ,cv2.TM_CCOEFF,cv2.TM_SQDIFF]
      for i in range(6):
          ncc_checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_ncc,text=methods[i],command=self.method_ncc1,onvalue="on", offvalue="off")
          ncc_checkbox_1.grid(row=i, column=0, pady=(0, 5), padx=5, sticky="n")
          self.ncc_checkbox.append(ncc_checkbox_1)
      
    # set default values
#    self.sidebar_button_3.configure(state="disabled")
      # self.ncc_checkbox_1.configure(state="disabled")
      # self.ncc_checkbox_1.configure(state="disabled")
      # self.ncc_checkbox_1.configure(state="disabled")
      self.ncc_xp_l.set('')
      self.ncc_yp_l.set('')
      self.ncc_xp_r.set('')
      self.ncc_yp_r.set('')
      
    #   frame_NCC_01
      self.ncc_px_step=StringVar()
      self.ncc_serech_step=StringVar()
      self.ncc_px_input = customtkinter.CTkEntry(master=self.frame_NCC_02,textvariable=self.ncc_px_step)
      self.ncc_px_input .grid(row=0, column=4, padx=10, pady=(5, 5))
      self.ncc_step_input= customtkinter.CTkEntry(master=self.frame_NCC_02,textvariable=self.ncc_serech_step)
      self.ncc_step_input .grid(row=1, column=4, padx=10, pady=(5, 5))
      self.grid_ncc_ = customtkinter.CTkButton(master=self.frame_NCC_02,text=f"Grid Matching", command=self.drow_ncc_grid)
      self.grid_ncc_ .grid(row=2, column=4, padx=10, pady=(5, 5))      
      self.ncc_labale222   = customtkinter.CTkLabel(master=self.frame_NCC_02,text="xp :").grid(row=0, column=3, padx=10, pady=(7, 7))
      self.ncc_labale333   = customtkinter.CTkLabel(master=self.frame_NCC_02,text="Step :").grid(row=1, column=3, padx=10, pady=(7, 7))

    #   frame_NCC_01
      self.ncc_window=StringVar()
      self.ncc_serech_area_x=StringVar()
      self.ncc_serech_area_y=StringVar()
      self.ncc_windos_input = customtkinter.CTkEntry(master=self.frame_NCC_01,textvariable=self.ncc_window)
      self.ncc_windos_input .grid(row=0, column=1, padx=10, pady=(5, 5))
      self.ncc_serech_input_x= customtkinter.CTkEntry(master=self.frame_NCC_01,textvariable=self.ncc_serech_area_x)
      self.ncc_serech_input_y= customtkinter.CTkEntry(master=self.frame_NCC_01,textvariable=self.ncc_serech_area_y)
      self.ncc_serech_input_x .grid(row=1, column=1, padx=10, pady=(5, 5))
      self.ncc_serech_input_y .grid(row=2, column=1, padx=10, pady=(5, 5))    
      self.find_ncc_match1 = customtkinter.CTkButton(master=self.frame_NCC_01,text=f"Find in Area", command=self.get_match_parts)
      self.find_ncc_match1 .grid(row=4, column=1, padx=10, pady=(5, 5))
      self.find_ncc_match2 = customtkinter.CTkButton(master=self.frame_NCC_01,text=f"Find in full image", command=self.Find_in_full_image)
      self.find_ncc_match2 .grid(row=5, column=1, padx=10, pady=(5, 5))
      self.find_ncc_match3 = customtkinter.CTkButton(master=self.frame_NCC_01,text=f"Find in full image", command=self.Find_in_full_image)
     # self.find_ncc_match3 .grid(row=5, column=1, padx=10, pady=(5, 5))
      
      self.find_ncc_match1.configure(state='disabled')
      self.find_ncc_match2.configure(state='disabled')
      self.grid_ncc_.configure(state='disabled')
      self.ncc_window.set('25')
      self.ncc_serech_area_x.set('500')
      self.ncc_serech_area_y.set('150')
      self.ncc_px_step.set('100')
      self.ncc_serech_step.set('50')

    def left_changes(self,size,matchig_pixcel_L):

         # CREATE A rectangle

         x1=int(matchig_pixcel_L['x']-(size-1)/2-1)
         x2=int(matchig_pixcel_L['x']+(size-1)/2-1)
         y1=int(matchig_pixcel_L['y']-(size-1)/2-1)
         y2=int(matchig_pixcel_L['y']+(size-1)/2+1)
         img=self.Sensors_L.img.copy()
         cv2.rectangle(img, (x1, y1), (x2, y2), (0,0,255),  2)
         cv2.imwrite(r"cash\new_L.png",img)
         self.canvasL.canvas.destroy()
         self.canvasL = CanvasImage(self.frame_image_l, r'cash\new_L.png') 
         self.canvasL.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")
         self.canvasL.canvas.bind('<Motion>', self.motion_L)
         self.canvasL.canvas.bind('<ButtonPress-3>', self.point_select_LEFT)
         self.canvasL.canvas.bind('<ButtonPress-2>', self.point_select_deleteL)
         # CREATE A WINDOW 
         img=self.Sensors_L.img.copy()
         img_WL=img[y1:y2,x1:x2]
         cv2.imwrite(r"cash\window_L.png",img_WL)
       #  self.canvasL_W.canvas.destroy()
         self.canvasL_W = CanvasImage(self.match_window_l, r'cash\window_L.png') 
         self.canvasL_W.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")
         try:
            self.vll_xp_l.set(str(int(matchig_pixcel_L['x'])))
            self.vll_yp_l.set(str(int(matchig_pixcel_L['y'])))  
         except:
                print('soryy') 
         try:
                 self.ncc_xp_l.set(str(int(matchig_pixcel_L['x'])))
                 self.ncc_yp_l.set(str(int(matchig_pixcel_L['y'])))
         except:
                 print('soryy')
 
         try:
             self.lsm_xp_l.set(str(int(matchig_pixcel_L['x'])))
             self.lsm_yp_l.set(str(int(matchig_pixcel_L['y'])))
         except:
                   print('soryy')                             
    def right_changes(self,size,matchig_pixcel_R):

         # CREATE A rectangle

         x1=int(matchig_pixcel_R['x']-(size-1)/2-1)
         x2=int(matchig_pixcel_R['x']+(size-1)/2+1)
         y1=int(matchig_pixcel_R['y']-(size-1)/2-1)
         y2=int(matchig_pixcel_R['y']+(size-1)/2+1)
         img=self.Sensors_R.img.copy()
         img_WR=img[y1:y2,x1:x2]
         cv2.imwrite(r"cash\window_R.png",img_WR)
         
         cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,0),  2)
         cv2.imwrite(r"cash\new_R.png",img)
         self.canvasR.canvas.destroy()
         self.canvasR = CanvasImage(self.frame_image_r, r'cash\new_R.png') 
         self.canvasR.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")
         self.canvasR.canvas.bind('<Motion>', self.motion_R)
         self.canvasR.canvas.bind('<ButtonPress-3>', self.point_select_RIGHT)
         self.canvasR.canvas.bind('<ButtonPress-2>', self.point_select_deleteR)
         # Point
         self.canvasR_W = CanvasImage(self.match_window_r, r'cash\window_R.png') 
         self.canvasR_W.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew") 
         try:
                 self.ncc_xp_r.set(str(int(matchig_pixcel_R['x'])))
                 self.ncc_yp_r.set(str(int(matchig_pixcel_R['y'])))
         except:
                     print('sorry')
         try:
                 self.vll_xp_r.set(str(int(matchig_pixcel_R['x'])))
                 self.vll_yp_r.set(str(int(matchig_pixcel_R['y'])))  
         except:
                     print('sorry')
         try:
             self.lsm_xp_r.set(str(int(matchig_pixcel_R['x'])))
             self.lsm_yp_r.set(str(int(matchig_pixcel_R['y'])))
         except:
               print('sorry')
    def get_match_parts(self):
        size  =int(self.ncc_windos_input.get())
        serech_domain_x=int(self.ncc_serech_input_x.get())
        serech_domain_y=int(self.ncc_serech_input_y.get())
        if serech_domain_y>size and serech_domain_x>size:
         

         # matching 
         try:
             matchig_pixcel_L={'x':self.point_x_L,'y':self.point_y_L}
             matchig_pixcel_R,window_R=area_base_pixcel_matching_by_sererchAREA(self.Sensors_L,self.Sensors_R,matchig_pixcel_L,size,serech_domain_y,serech_domain_x,self.method_ncc)
             self.left_changes(size,matchig_pixcel_L)
             self.right_changes(size,matchig_pixcel_R)
             self.VS0.set('')
         except:
             self.VS0.set('Serech area is biger than image, or make sure you have choosed a point')
        else:
            self.VS0.set('Serech area most be biger than window size')
    def Find_in_full_image(self):
        size  =int(self.ncc_windos_input.get())
        matchig_pixcel_L={'x':self.point_x_L,'y':self.point_y_L}
        
        matchig_pixcel_R,window_R=area_base_pixcel_matching_full_image(self.Sensors_L,self.Sensors_R,matchig_pixcel_L,size,self.method_ncc)
        self.left_changes(size,matchig_pixcel_L)
        self.right_changes(size,matchig_pixcel_R)
        self.VS0.set('')
  
    def drow_ncc_grid(self):
        Window_Size=int(self.ncc_windos_input.get())
        
        x=int(self.ncc_px_step.get())
        step=int(self.ncc_serech_step.get())
        rows, cols =self.Sensors_L.Gry.shape
        if rows>x:
         X = np.arange(x    ,cols , step)
         Y = np.arange(2*Window_Size ,rows , step)
         Pt_L=[]
         Pt_R=[]
         for i in X:
            for j in Y:
                matchig_pixcel_L={'x': i, 'y': j}
                matchig_pixcel_R,window_R=area_base_pixcel_matching_full_image(self.Sensors_L,self.Sensors_R,matchig_pixcel_L,Window_Size,self.method_ncc)
                Pt_L.append([matchig_pixcel_L['x'],matchig_pixcel_L['y']])
                Pt_R.append([matchig_pixcel_R['x'],matchig_pixcel_R['y']])
         NCC_matchig_pixcel_L=pd.DataFrame({'x':np.array(Pt_L)[:,0],'y':np.array(Pt_L)[:,1]})
         NCC_matchig_pixcel_R=pd.DataFrame({'x':np.array(Pt_R)[:,0],'y':np.array(Pt_R)[:,1]})

         self.point_driwnig(NCC_matchig_pixcel_L,NCC_matchig_pixcel_R)
         self.VS0.set('')                     
        else :
            self.VS0.set('xp must be smaller than image rows')        
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
    def LSM(self):
     self.remove_widgets_based_on_location()
     self.remove_widgets_based_on_location()
    # self.makait_work()
     self.frame_image_l.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
     self.frame_image_r.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
     self.match_window_l.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
     self.match_window_r.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
     
     self.frame_LSM_01 = customtkinter.CTkFrame(self)
     self.frame_LSM_02 = customtkinter.CTkFrame(self)
      
     self.frame_LSM_01.grid(row=0, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
     self.frame_LSM_02.grid(row=1, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")  
     
     
     self.canvasL_W=customtkinter.CTkCanvas(master=self.match_window_l, width= 50, height= 50,background = '#06748b')
     self.canvasL_W.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")
     self.canvasR_W=customtkinter.CTkCanvas(master=self.match_window_r, width= 50, height= 50,background = '#06748b')
     self.canvasR_W.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")
 
     self.match_windos_l=customtkinter.CTkFrame(self)
     self.match_windos_r=customtkinter.CTkFrame(self)
     
     self.lsm_labale1   = customtkinter.CTkLabel(master=self.frame_LSM_01,text="Inputs :").grid(row=0, column=0, padx=10, pady=(5, 5))
     self.lsm_labale2   = customtkinter.CTkLabel(master=self.frame_LSM_01,text="Window size   :").grid(row=1, column=0, padx=10, pady=(5, 5))
     self.lsm_labale3   = customtkinter.CTkLabel(master=self.frame_LSM_01,text="Max iteration :").grid(row=2, column=0, padx=10, pady=(5, 5))
     self.lsm_labale4   = customtkinter.CTkLabel(master=self.frame_LSM_01,text="Plot interval :").grid(row=3, column=0, padx=10, pady=(5, 5))
     self.lsm_labale5   = customtkinter.CTkLabel(master=self.frame_LSM_01,text="gradians size :").grid(row=4, column=0, padx=10, pady=(5, 10))
       
     self.lsm_xp_l=StringVar()
     self.lsm_yp_l=StringVar()
     self.lsm_xp_r=StringVar()
     self.lsm_yp_r=StringVar()
     self.lsm_labale11   = customtkinter.CTkLabel(master=self.frame_LSM_02,textvariable=self.lsm_xp_l).grid(row=0, column=1, padx=10, pady=(7, 7))
     self.lsm_labale21   = customtkinter.CTkLabel(master=self.frame_LSM_02,textvariable=self.lsm_yp_l).grid(row=1, column=1, padx=10, pady=(7, 7))
     self.lsm_labale31   = customtkinter.CTkLabel(master=self.frame_LSM_02,textvariable=self.lsm_xp_r).grid(row=2, column=1, padx=10, pady=(7, 7))
     self.lsm_labale41   = customtkinter.CTkLabel(master=self.frame_LSM_02,textvariable=self.lsm_yp_r).grid(row=3, column=1, padx=10, pady=(7, 7))
     self.lsm_labale11   = customtkinter.CTkLabel(master=self.frame_LSM_02,text="left  image xp :").grid(row=0, column=0, padx=10, pady=(7, 7))
     self.lsm_labale22   = customtkinter.CTkLabel(master=self.frame_LSM_02,text="left  image yp :").grid(row=1, column=0, padx=10, pady=(7, 7))
     self.lsm_labale33   = customtkinter.CTkLabel(master=self.frame_LSM_02,text="right image xp :").grid(row=2, column=0, padx=10, pady=(7, 7))
     self.lsm_labale44   = customtkinter.CTkLabel(master=self.frame_LSM_02,text="right image yp :").grid(row=3, column=0, padx=10, pady=(7, 7))
     self.lsm_xp_l.set('')
     self.lsm_yp_l.set('')
     self.lsm_xp_r.set('')
     self.lsm_yp_r.set('')
   #   frame_NCC_01
     self.lsm_window=StringVar()
     self.Max_iteration=StringVar()
     self.lsm_plot=StringVar()
     self.lsm_gradinan=StringVar()

     self.lsm_windos_input = customtkinter.CTkEntry(master=self.frame_LSM_01,textvariable=self.lsm_window)
     self.lsm_windos_input .grid(row=1, column=1, padx=10, pady=(5, 5))
     self.lsm_serech_input_x= customtkinter.CTkEntry(master=self.frame_LSM_01,textvariable=self.Max_iteration)
     self.lsm_serech_input_x .grid(row=2, column=1, padx=10, pady=(5, 5)) 
     self.lsm_windos_input = customtkinter.CTkEntry(master=self.frame_LSM_01,textvariable=self.lsm_plot)
     self.lsm_windos_input .grid(row=3, column=1, padx=10, pady=(5, 5))
     self.lsm_serech_input_x= customtkinter.CTkEntry(master=self.frame_LSM_01,textvariable=self.lsm_gradinan)
     self.lsm_serech_input_x .grid(row=4, column=1, padx=10, pady=(5, 10)) 
         
     self.find_LSM_match = customtkinter.CTkButton(master=self.frame_LSM_01,text=f"Shift and scale", command=self.LSM_Shift_Scale)
     self.find_LSM_match .grid(row=5, column=1, padx=10, pady=(5, 5))
     self.find_LSM_match = customtkinter.CTkButton(master=self.frame_LSM_01,text=f"Affine geometry", command=self.LSM_Geometry)
     self.find_LSM_match .grid(row=6, column=1, padx=10, pady=(5, 5))
     self.find_LSM_match = customtkinter.CTkButton(master=self.frame_LSM_01,text=f"Geometry and radiometric", command=self.LSM_geo_radio)
     self.find_LSM_match .grid(row=7, column=1, padx=10, pady=(5, 5))

           
     self.lsm_window.set('20')
     self.Max_iteration.set('1000')
     self.lsm_plot.set('50')
     self.lsm_gradinan.set('1')

      
    def LSM_Shift_Scale(self): 
       size  =int(self.lsm_window.get())
       Max_iteration=int(self.Max_iteration.get())
       Plot_interval=int(self.lsm_plot.get())
       gradians_size=int(self.lsm_gradinan.get())
       if 3<size and Max_iteration>1:
        if gradians_size % 2 ==0:
            self.VS0.set('gradians size most be Odd number')
        else:
            
        # matching 
         try:
            matchig_pixcel_L={'x':self.point_x_L,'y':self.point_y_L}
            matchig_pixcel_R={'x':self.point_x_R,'y':self.point_y_R}
            
            matchig_pixcel_R,affine_matrix=LSM_s_r(size,Max_iteration,self.Sensors_L,self.Sensors_R,matchig_pixcel_L,matchig_pixcel_R,Plot_interval,gradians_size)
            self.left_changes(size,matchig_pixcel_L)
            self.right_changes(size,matchig_pixcel_R)
            self.VS0.set('')
         except:
                self.VS0.set('make sure you have choosed a point')
        #except:
        #    self.VS0.set('sorry somting went wrong')
       else:
           self.VS0.set('Serech area most be biger or you need more iteration than 0')
    def LSM_Geometry(self): 
       size  =int(self.lsm_window.get())
       Max_iteration=int(self.Max_iteration.get())
       Plot_interval=int(self.lsm_plot.get())
       gradians_size=int(self.lsm_gradinan.get())
       if 3<size and Max_iteration>1:
        if gradians_size % 2 ==0:
            self.VS0.set('gradians size most be Odd number')
        else:

        # matching 
         try:
            matchig_pixcel_L={'x':self.point_x_L,'y':self.point_y_L}
            matchig_pixcel_R={'x':self.point_x_R,'y':self.point_y_R}
            
            matchig_pixcel_R,affine_matrix=LSM_Full_Geometry(size,Max_iteration,self.Sensors_L,self.Sensors_R,matchig_pixcel_L,matchig_pixcel_R,Plot_interval,gradians_size)
            self.left_changes(size,matchig_pixcel_L)
            self.right_changes(size,matchig_pixcel_R)
            self.VS0.set('')
         except:
                self.VS0.set(' make sure you have choosed a point')
       else:
           self.VS0.set('Serech area most be biger or you need more iteration than 0')
    def LSM_geo_radio(self): 
        size  =int(self.lsm_window.get())
        Max_iteration=int(self.Max_iteration.get())
        Plot_interval=int(self.lsm_plot.get())
        gradians_size=int(self.lsm_gradinan.get())
        if 3<size and Max_iteration>1:
         if gradians_size % 2 ==0:
             self.VS0.set('gradians size most be Odd number')
         else:

         # matching 
          try:
             matchig_pixcel_L={'x':self.point_x_L,'y':self.point_y_L}
             matchig_pixcel_R={'x':self.point_x_R,'y':self.point_y_R}
             
             matchig_pixcel_R,affine_matrix=LSM_geo_radio(size,Max_iteration,self.Sensors_L,self.Sensors_R,matchig_pixcel_L,matchig_pixcel_R,Plot_interval,gradians_size)
             self.left_changes(size,matchig_pixcel_L)
             self.right_changes(size,matchig_pixcel_R)
             self.VS0.set('')
          except:
                self.VS0.set(' make sure you have choosed a point')
        else:
            self.VS0.set('Serech area most be biger or you need more iteration than 0')
                  
      
    def remove_widgets_based_on_location(self,):

     self.tabviewL.destroy()
     self.tabviewR.destroy()

     self.scrollable_frame0.destroy()
     self.checkbox_slider_frame.destroy()
     for i in range(len(self.tagesL)):
         self.canvasL.canvas.delete(self.tagesL[i])
     for i in range(len(self.tagesR)):
        self.canvasR.canvas.delete(self.tagesR[i])
     self.tagesL=[]
     self.tagesR=[]
     self.frame_streo.destroy()
     self.frame01.destroy()
     self.frame02.destroy()
     self.frame_vll_01.destroy()
     self.frame_vll_02.destroy()
     self.frame_NCC_01.destroy()
     self.frame_NCC_02.destroy()
     self.frame_LSM_01.destroy()
     self.frame_LSM_02.destroy()
     self.frame_image_l.grid_forget()
     self.frame_image_r.grid_forget()
     self.match_window_l.grid_forget()
     self.match_window_r.grid_forget()
    def makait_work(self):
                self.filename_left=r'D:\Projects\2.Term2\Digital_Photogrammetry\project1\main\data\21_60_.png'
                self.filename_cameraL=r"D:\Projects\2.Term2\Digital_Photogrammetry\project1\main\data\CAMERA.txt"
                self.filename_right=r'D:\Projects\2.Term2\Digital_Photogrammetry\project1\main\data\22_60_.png'
                self.canvasL = CanvasImage(self.frame_image_l, self.filename_left)  # create widget
                self.canvasL.canvas.destroy()
                self.canvasL = CanvasImage(self.frame_image_l, self.filename_left)  # create widget            
                self.canvasL.grid(row=0, column=0, padx=(10, 0), pady=(20, 0), sticky="nsew")
            
                self.canvasL.canvas.bind('<Motion>', self.motion_L)
                self.canvasL.canvas.bind('<ButtonPress-3>', self.point_select_LEFT)
                self.canvasL.canvas.bind('<ButtonPress-2>', self.point_select_deleteL)
                self.text_text = self.canvasL.canvas.create_text(0, 0, anchor='nw', text=self.canvasL.text)
                self.Sensors_L=Interior_Orientation(self.filename_left)
                
                self.canvasR = CanvasImage(self.frame_image_r, self.filename_right)  # create widget
                self.canvasR.canvas.destroy()
                self.canvasR = CanvasImage(self.frame_image_r, self.filename_right)  # create widget
                self.canvasR.grid(row=0, column=0, padx=(10, 0), pady=(20, 0), sticky="nsew")
                self.canvasR.canvas.bind('<Motion>', self.motion_R)
                self.canvasR.canvas.bind('<ButtonPress-3>', self.point_select_RIGHT)
                self.canvasR.canvas.bind('<ButtonPress-2>', self.point_select_deleteR)
                self.Sensors_R=Interior_Orientation(self.filename_right)
             # ADD IMAGE  RIGHT
    def makait_work2(self):
                 self.filename_left=r'D:\Projects\2.Term2\Digital_Photogrammetry\project3\ted_L.png'
                 self.filename_right=r'D:\Projects\2.Term2\Digital_Photogrammetry\project3\ted_L.png'
                 self.canvasL = CanvasImage(self.frame_image_l, self.filename_left)  # create widget
                 self.canvasL.canvas.destroy()
                 self.canvasL = CanvasImage(self.frame_image_l, self.filename_left)  # create widget            
                 self.canvasL.grid(row=0, column=0, padx=(10, 0), pady=(20, 0), sticky="nsew")
             
                 self.canvasL.canvas.bind('<Motion>', self.motion_L)
                 self.canvasL.canvas.bind('<ButtonPress-3>', self.point_select_LEFT)
                 self.canvasL.canvas.bind('<ButtonPress-2>', self.point_select_deleteL)
                 self.text_text = self.canvasL.canvas.create_text(0, 0, anchor='nw', text=self.canvasL.text)
                 self.Sensors_L=Interior_Orientation(self.filename_left)
                 
                 self.canvasR = CanvasImage(self.frame_image_r, self.filename_right)  # create widget
                 self.canvasR.canvas.destroy()
                 self.canvasR = CanvasImage(self.frame_image_r, self.filename_right)  # create widget
                 self.canvasR.grid(row=0, column=0, padx=(10, 0), pady=(20, 0), sticky="nsew")
                 self.canvasR.canvas.bind('<Motion>', self.motion_R)
                 self.canvasR.canvas.bind('<ButtonPress-3>', self.point_select_RIGHT)
                 self.canvasR.canvas.bind('<ButtonPress-2>', self.point_select_deleteR)
                 self.Sensors_R=Interior_Orientation(self.filename_right)
             
                # relettive 
                # camera_name,focal_length,fiducial_coordinates,Camera_distortions=Read_Camera(self.filename_cameraL)
                # self.Streo=StreoImages(self.Sensors_L,self.Sensors_R)
                # self.Streo.ExtractMatchedPoints(RatioTest=0.35)
                # self.projective_matrix=self.Streo.Initialize_Relative_orientation_in_pp(focal_length,0.0001)
                # self.ReletiveOrientation_stase=True   
      
      


if __name__ == "__main__":
    app = App()
    app.canvas=None
    app.mainloop()