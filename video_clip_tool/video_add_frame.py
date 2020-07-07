"""
video_clip 视频截取工具


"""

# -*- coding: utf-8-*-
import sys
import glob
from sys import version_info

if version_info.major == 3:
    from tkinter import *
    import tkinter.messagebox
    import tkinter.filedialog
else:
    from Tkinter import *
    import tkFileDialog
    import tkMessageBox
import os
import random
import numpy as np
# import xlrd
# import xlwt
import cv2
import time
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from PIL import ImageTk, Image
opencv_version = int(cv2.__version__.split(".")[0])
class show:

    cnt_color = 0
    image_w = 1300
    image_h = 700
    window_width = image_w
    window_height = 880

    video_name = ""
    video_lists = []
    video_folder = ""
    idx_video = 0
    idx_frame = 0
    start_frames = []
    end_frames = []
    clip_labels = []
    list_names_show_clip = []
    playend_frame = 0

    key_frame_ids = []
    list_names_show_keyframe = []

    flag_img_update = False
    scrollbar_max_length = 100.0
    scrollbar_resolution = 1
    flag_start_show = False
    flag_play = False
    flag_backward = False
    frame_step_base = 0
    frame_step_current = frame_step_base
    frame_step_speed = frame_step_base

    id_play = 0
    flag_clipstartbutton = False
    flag_clipendbutton = False
    fontsize = 15


    def __init__(self):
        # print len(self.binary_labels.keys())
        self.root = Tk()
        self.root.title('videol_clip')
        # You can set the geometry attribute to change the root windows size
        self.root.geometry(
            "%dx%d" % (self.window_width, self.window_height))  # You want the size of the app to be 500x500
        self.root.resizable(0, 0)  # Don't allow resizing in the x or y direction
        self.root.bind("<Key>", self.keyboard_callback)
        ########
        self.image_show = Frame(self.root, width=self.image_w, height=self.image_h, bg='black')
        self.image_show.grid(row=0,column=0,sticky=W)
        self.image_show.config()
        self.Canva = Canvas(self.image_show, bg="blue", height=self.image_h, width=self.image_w)
        ############
        # self.scrollbar = Scale(self.root, label="拉动", from_=0, to=12, orient=HORIZONTAL, length=500, showvalue=1, tickinterval=3,
        #            resolution=0.01, command=select)
        self.scrollbar = Scale(self.root, from_=0, to=self.scrollbar_max_length, orient=HORIZONTAL, length=self.image_w, showvalue=1,
                               tickinterval=3,resolution=self.scrollbar_resolution)
        self.scrollbar.grid(row=1, column=0,sticky=W)
        self.scrollbar.bind('<Button-1>', self.action)

        #########
        self.frame_play_button = Frame(self.root)
        self.frame_play_button.grid(row=2, column=0, sticky=W)
        self.frame_play_button.config()
        ###########
        # self.button_openvideo = Button(self.frame_play_button, text="打开", fg="green", font=("", 16),
        #                                command=self.openvideo)
        # self.button_openvideo.grid(row=0, column=0, sticky=N)
        ##############
        self.button_openvideofolder = Button(self.frame_play_button, text="打开文件夹", fg="green", font=("", self.fontsize),
                                             command=self.openvideofolder)
        self.button_openvideofolder.grid(row=0, column=1, sticky=N)
        ############
        # self.text_general_info = Label(self.frame_play_button,bg="white",fg="red",font=("", 12),height=2,text="这里显示一些提示信息",width=30,relief=RAISED)
        # self.text_general_info.grid(row=0, column=3, sticky=N)
        #####
        self.button_clipstart = Button(self.frame_play_button, text="开始", fg="blue", font=("", self.fontsize),command=self.clipstart)
        self.button_clipstart.grid(row=0, column=2, sticky=N)
        #######
        self.text_clipstart = Label(self.frame_play_button, bg="white", fg="red", font=("", 12), height=2, width=10, relief=RAISED,text="-1")
        self.text_clipstart.grid(row=0, column=3, sticky=N)
        #####
        self.button_clipend = Button(self.frame_play_button, text="结束", fg="blue", font=("", self.fontsize),command=self.clipend)
        self.button_clipend.grid(row=0, column=4, sticky=N)
        #######
        self.text_clipend = Label(self.frame_play_button, bg="white", fg="red", font=("", 12), height=2, width=10,
                                    relief=RAISED,text="-1")
        self.text_clipend.grid(row=0, column=5, sticky=N)
        #######
        self.text_label = Label(self.frame_play_button, text="标签", fg="blue", font=("", self.fontsize))
        self.text_label.grid(row=0, column=6, sticky=N)
        #######
        self.label_var = IntVar()
        self.entry_label = Entry(self.frame_play_button, textvariable=self.label_var, width=5,font=("", self.fontsize))
        self.entry_label.grid(row=0, column=7, sticky=N)
        self.entry_label.delete(0, END)
        self.entry_label.insert(0, "-1")
        #######
        self.button_addclip = Button(self.frame_play_button, text="添加 片 段", fg="blue", font=("", self.fontsize), command=self.addclip)
        self.button_addclip.grid(row=0, column=8, sticky=N)
        ###########
        self.list_clip = Listbox(self.frame_play_button,height=2,width=18,font=("", 12))
        self.list_clip.grid(row=0, column=9, sticky=N)
        #######
        self.text_cliptotal = Label(self.frame_play_button, bg="white", fg="red", font=("", 12), height=2, width=10,
                                  relief=RAISED, text="（共0个）")
        self.text_cliptotal.grid(row=0, column=10, sticky=N)
        #######
        self.button_deleteclip = Button(self.frame_play_button, text="删除", fg="blue", font=("", self.fontsize), command=self.deleteclip)
        self.button_deleteclip.grid(row=0, column=11, sticky=N)
        #######
        self.button_checkclip = Button(self.frame_play_button, text="查看", fg="blue", font=("", self.fontsize),
                                        command=self.checkclip)
        self.button_checkclip.grid(row=0, column=12, sticky=N)
        #######
        self.button_writecurrentvideo = Button(self.frame_play_button, text="保存", fg="blue", font=("", self.fontsize),
                                       command=self.write_to_disk)
        self.button_writecurrentvideo.grid(row=0, column=13, sticky=N)
        ###########
        self.button_nextvideo = Button(self.frame_play_button, text="下个视频", fg="green", font=("", self.fontsize),command=self.next_video)
        self.button_nextvideo.grid(row=0, column=14, sticky=N)
        ########
        self.button_prevvideo = Button(self.frame_play_button, text="上个视频", fg="green", font=("", self.fontsize),
                                       command=self.prev_video)
        self.button_prevvideo.grid(row=0, column=15, sticky=N)
        ########
        self.button_correctlabel= Button(self.frame_play_button, text="修改标签", fg="green", font=("", self.fontsize),
                                       command=self.correctlabel)
        self.button_correctlabel.grid(row=0, column=16, sticky=N)
        #########
        self.frame_play_speed = Frame(self.root)
        self.frame_play_speed.grid(row=3, column=0, sticky=W)
        self.frame_play_speed.config()

        #####
        l = Label(self.frame_play_speed, text="正常(左箭头)速度：", fg="red", font=("", 16))
        l.grid(row=0, column=0, sticky=N)
        self.frame_step_base_var = IntVar()
        self.entry_frame_step_base = Entry(self.frame_play_speed, textvariable=self.frame_step_base_var,width=5,font=("", self.fontsize))
        self.entry_frame_step_base.grid(row=0, column=1, sticky=W)
        self.entry_frame_step_base.delete(0, END)
        self.entry_frame_step_base.insert(0,"5")
        ########
        l = Label(self.frame_play_speed, text="快进(右箭头)速度：", fg="red", font=("", 16))
        l.grid(row=0, column=2, sticky=N)
        self.frame_step_speed_var = IntVar()
        self.entry_frame_step_speed = Entry(self.frame_play_speed, textvariable=self.frame_step_speed_var, width=5,font=("", self.fontsize))
        self.entry_frame_step_speed.grid(row=0, column=3, sticky=W)
        self.entry_frame_step_speed.delete(0, END)
        self.entry_frame_step_speed.insert(0, "20")
        #####
        #####
        self.button_keyframe = Button(self.frame_play_speed, text="添加关键帧", fg="blue", font=("", self.fontsize),
                                     command=self.addkeyframe)
        self.button_keyframe.grid(row=0, column=4, sticky=W)
        ####
        self.list_keyframe = Listbox(self.frame_play_speed, height=2, width=18, font=("", 12))
        self.list_keyframe.grid(row=0, column=5, sticky=W)
        ###
        self.text_keyframetotal = Label(self.frame_play_speed, bg="white", fg="red", font=("", 12), height=2, width=10,
                                    relief=RAISED, text="（共0个）")
        self.text_keyframetotal.grid(row=0, column=6, sticky=N)
        ######
        self.button_deletekeyframe = Button(self.frame_play_speed, text="删除", fg="blue", font=("", self.fontsize),
                                        command=self.deletekeyframe)
        self.button_deletekeyframe.grid(row=0, column=7, sticky=N)
        #######
        self.button_checkkeyframe = Button(self.frame_play_speed, text="查看", fg="blue", font=("", self.fontsize),
                                       command=self.checkkeyframe)
        self.button_checkkeyframe.grid(row=0, column=12, sticky=N)
        ##################
        # self.text_general_info = Label(self.frame_play_speed, bg="white", fg="red", font=("", 12), height=1, width=50,
        #                             relief=RAISED, text="..............................")
        # self.text_general_info.grid(row=1, column=4, sticky=N)
        #########
        self.frame_generalinfo = Frame(self.root)
        self.frame_generalinfo.grid(row=4, column=0, sticky=W)
        self.frame_generalinfo.config()
        self.text_general_info = Text(self.frame_generalinfo, bg="white", fg="blue", font=("", 12),width=self.image_w,height=1.5)
        self.text_general_info.insert(1.0, "............................................................................")
        self.text_general_info.grid(row=0, column=0, sticky=W)
        # self.label_general_info.place(height=h_button, width=self.window_width, x=0, y=self.window_height - h_button)
        # self.label_general_info.config(state="disabled")





    def openvideo(self):
        self.frame_step_base = self.frame_step_base_var.get()
        self.frame_step_speed = self.frame_step_speed_var.get()
        if version_info.major == 3:
            self.video_name = tkinter.filedialog.askopenfilename()
        else:
            self.video_name = tkFileDialog.askopenfilename()
        if len(self.video_name)>0:
            self.video_lists = []
            self.video_lists.append(self.video_name )
            self.cap = cv2.VideoCapture(self.video_lists[0])
            if opencv_version==2:
                self.num_frames_current = self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
            else:
                self.num_frames_current = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
            self.flag_start_show = True
            self.idx_frame = 0
            ret, frame = self.cap.read()
            frame = self.resize_img(frame)

            self.putimgoncanva(frame)
            self.scrollbar_max_length = self.num_frames_current
            self.scrollbar.config(to=self.num_frames_current,tickinterval=self.scrollbar_max_length/20)
            self.text_general_info.delete(1.0,END)
            self.text_general_info.insert(1.0, "正在处理：%s" % str(self.video_lists[0]))
            self.check_annotated()
            self.get_play_speed_step()
            self.frame_step_current = self.frame_step_base
            self.frame_step_speed = self.frame_step_base

    def openvideofolder(self):
        self.frame_step_base = self.frame_step_base_var.get()
        self.frame_step_speed = self.frame_step_speed_var.get()
        if version_info.major == 3:
            self.video_folder = tkinter.filedialog.askdirectory()
        else:
            self.video_folder = tkFileDialog.askdirectory()
        if len(self.video_folder)>0:
            v_lists = os.listdir(self.video_folder)
            self.video_lists = []
            for v_l in v_lists:
                if ".txt" not in v_l:
                    if "Thumbs.db" not in v_l:
                        self.video_lists.append(os.path.join(self.video_folder,v_l))
            self.cap = cv2.VideoCapture(self.video_lists[self.idx_video])
            if opencv_version==2:
                self.num_frames_current = self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
            else:
                self.num_frames_current = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
            self.flag_start_show = True
            self.idx_frame = 0
            ret, frame = self.cap.read()
            frame = self.resize_img(frame)
            self.putimgoncanva(frame)
            self.scrollbar_max_length = self.num_frames_current
            self.scrollbar.config(to=self.num_frames_current, tickinterval=self.scrollbar_max_length / 20)
            self.text_general_info.delete(1.0, END)
            self.text_general_info.insert(1.0, "正在处理：%s（%d/%d）" % (str(self.video_lists[self.idx_video]),self.idx_video+1,len(self.video_lists)))
            self.check_annotated()
            self.get_play_speed_step()
            self.frame_step_current = self.frame_step_base
            self.frame_step_speed = self.frame_step_base
    def putimgoncanva(self,cv_img):
        if self.flag_start_show:
            if cv_img is not None:
                cv_img = cv_img[:, :, (2, 1, 0)]
                if not self.flag_img_update:
                   self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv_img))
                   self.image_on_canvas = self.Canva.create_image(0, 0, image=self.photo,anchor=NW)
                   self.Canva.pack()
                   self.flag_img_update = True
                else:
                   self.photo.paste(Image.fromarray(cv_img),(0,0,self.image_w,self.image_h))
                   self.Canva.itemconfig(self.image_on_canvas, image=self.photo)
    def resize_img(self,img):
        img_h,img_w,_ = img.shape
        scale_h = float(self.image_h)/float(img_h)
        scale_w = float(self.image_w)/float(img_w)
        scale = min(scale_h,scale_w)
        img_resize = cv2.resize(img,dsize=None,fx=scale,fy=scale)
        return img_resize
    def next_video(self):
        if self.flag_start_show:
            self.photo.paste(Image.fromarray(np.zeros((self.image_h,self.image_w,3)).astype(np.uint8)), (0, 0, self.image_w, self.image_h))
            self.Canva.itemconfig(self.image_on_canvas, image=self.photo)
            self.idx_video += 1
            if self.idx_video > len(self.video_lists)-1:
                self.idx_video = len(self.video_lists)-1
            self.cap = cv2.VideoCapture(self.video_lists[self.idx_video])
            if opencv_version == 2:
                self.num_frames_current = self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
            else:
                self.num_frames_current = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)

            self.flag_start_show = True
            ret, frame = self.cap.read()
            frame = self.resize_img(frame)
            self.putimgoncanva(frame)
            self.idx_frame = 0
            self.scrollbar_max_length = self.num_frames_current
            self.scrollbar.config(to=self.num_frames_current, tickinterval=self.scrollbar_max_length / 20)
            self.text_general_info.delete(1.0, END)
            self.text_general_info.insert(1.0, "正在处理：%s（%d/%d）" % (str(self.video_lists[self.idx_video]), self.idx_video + 1, len(self.video_lists)))

            self.start_frames = []
            self.end_frames = []
            self.list_names_show_clip = []
            self.clip_labels = []
            list_names = StringVar(value=())
            self.list_clip.config(listvariable=list_names)
            str_show = "共%d个" % (len(self.start_frames))
            self.text_cliptotal.config(text=str_show)
            self.key_frame_ids = []
            self.list_names_show_keyframe = []
            list_names = StringVar(value=())
            self.list_keyframe.config(listvariable=list_names)
            str_show = "共%d个" % (len(self.key_frame_ids))
            self.text_keyframetotal.config(text=str_show)
            self.flag_img_update = False
            self.check_annotated()
    def prev_video(self):
        if self.flag_start_show:
            self.photo.paste(Image.fromarray(np.zeros((self.image_h,self.image_w,3)).astype(np.uint8)), (0, 0, self.image_w, self.image_h))
            self.Canva.itemconfig(self.image_on_canvas, image=self.photo)
            self.idx_video -= 1
            if self.idx_video < 0:
                self.idx_video = 0
            self.cap = cv2.VideoCapture(self.video_lists[self.idx_video])
            if opencv_version == 2:
                self.num_frames_current = self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
            else:
                self.num_frames_current = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)

            self.flag_start_show = True
            ret, frame = self.cap.read()
            frame = self.resize_img(frame)
            self.putimgoncanva(frame)
            self.idx_frame = 0
            self.scrollbar_max_length = self.num_frames_current
            self.scrollbar.config(to=self.num_frames_current, tickinterval=self.scrollbar_max_length / 20)
            self.text_general_info.delete(1.0, END)
            self.text_general_info.insert(1.0, "正在处理：%s（%d/%d）" % (str(self.video_lists[self.idx_video]), self.idx_video + 1, len(self.video_lists)))

            self.start_frames = []
            self.end_frames = []
            self.list_names_show_clip = []
            self.clip_labels = []
            list_names = StringVar(value=tuple(self.list_names_show_clip))
            self.list_clip.config(listvariable=list_names)
            str_show = "共%d个" % (len(self.start_frames))
            self.text_cliptotal.config(text=str_show)
            self.key_frame_ids = []
            self.list_names_show_keyframe = []
            list_names = StringVar(value=())
            self.list_keyframe.config(listvariable=list_names)
            str_show = "共%d个" % (len(self.key_frame_ids))
            self.text_keyframetotal.config(text=str_show)
            self.flag_img_update = False
            self.check_annotated()

    def play(self):
        if self.flag_start_show:

            if self.idx_frame>self.num_frames_current-1:
                self.idx_frame = self.num_frames_current-1
            if opencv_version == 2:
                self.cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, self.idx_frame)
            else:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.idx_frame)

            ret, frame = self.cap.read()
            frame = self.resize_img(frame)

            if ret:
                self.putimgoncanva(frame)
                if opencv_version == 2:
                    n_frame_current = self.cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)-1
                else:
                    n_frame_current = self.cap.get(cv2.CAP_PROP_POS_FRAMES) - 1
                self.scrollbar.set(n_frame_current)
            self.id_play = self.image_show.after(1,self.play)
            if not self.flag_backward:
                self.idx_frame += self.frame_step_current
            if self.flag_backward:
                self.flag_backward = False
            if self.frame_step_current>self.frame_step_base:
                self.frame_step_current = self.frame_step_base
    def play_static(self):
        if self.flag_start_show:
            if self.idx_frame > self.num_frames_current - 1:
                self.idx_frame = self.num_frames_current - 1
            if self.idx_frame < 0:
                self.idx_frame = 0
            if opencv_version == 2:
                self.cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, self.idx_frame)
            else:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.idx_frame)

            ret, frame = self.cap.read()
            frame = self.resize_img(frame)

            if ret:
                self.putimgoncanva(frame)
                if opencv_version == 2:
                    n_frame_current = self.cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)-1
                else:
                    n_frame_current = self.cap.get(cv2.CAP_PROP_POS_FRAMES)-1

                self.scrollbar.set(n_frame_current)
    def play_toend(self):
        if self.flag_start_show:
            self.get_play_speed_step()
            self.frame_step_current = self.frame_step_base
            if opencv_version == 2:
                self.cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, self.idx_frame)
            else:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.idx_frame)

            ret, frame = self.cap.read()
            frame = self.resize_img(frame)

            if ret:
                self.putimgoncanva(frame)
                if opencv_version == 2:
                    n_frame_current = self.cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)-1
                else:
                    n_frame_current = self.cap.get(cv2.CAP_PROP_POS_FRAMES)-1

                self.scrollbar.set(n_frame_current)
            self.id_play = self.image_show.after(1,self.play_toend)
            self.idx_frame += self.frame_step_current
            if self.idx_frame>self.playend_frame:
                self.image_show.after_cancel(self.id_play)

    def pause(self):
        self.image_show.after_cancel(self.id_play)
    def action(self, event):
        if self.flag_start_show:
            self.idx_frame = (float(event.x)/float(self.image_w)*self.num_frames_current)
            self.play_static()
    def keep_entry(self):
        try:
            label = self.label_var.get()
        except:
            label = -1
        self.entry_label.delete(0,END)
        self.entry_label.insert(0,label)
        try:
            step_base = self.frame_step_base_var.get()
        except:
            step_base = 5
        self.entry_frame_step_base.delete(0,END)
        self.entry_frame_step_base.insert(0, step_base)
        try:
            step_speed = self.frame_step_speed_var.get()
        except:
            step_speed = 20
        self.entry_frame_step_speed.delete(0, END)
        self.entry_frame_step_speed.insert(0, step_speed)
    def get_play_speed_step(self):
        try:
            self.frame_step_speed = self.frame_step_speed_var.get()
        except:
            self.frame_step_speed = 20
            self.entry_frame_step_speed.delete(0,END)
            self.entry_frame_step_speed.insert(0,self.frame_step_speed)

        try:
            self.frame_step_base = self.frame_step_base_var.get()
        except:
            self.frame_step_base = 5
            self.entry_frame_step_base.delete(0,END)
            self.entry_frame_step_base.insert(0,self.frame_step_base)

    def keyboard_callback(self, event):

        keycode = event.keycode
        if keycode == 32:#space
            self.keep_entry()
            self.get_play_speed_step()
            self.frame_step_current = self.frame_step_base
            self.flag_play = not self.flag_play
            if self.flag_play:
                self.play()
            else:
                self.pause()
        elif keycode == 39:#right arrow
            self.get_play_speed_step()
            self.frame_step_current = self.frame_step_speed
            if not self.flag_play:
                self.idx_frame += self.frame_step_current
                self.play_static()
            self.keep_entry()
        elif keycode == 37:#left arrow
            self.flag_backward = True
            self.get_play_speed_step()
            self.idx_frame -= self.frame_step_base
            if not self.flag_play:
                self.play_static()
            self.keep_entry()
        char = event.char
        if char == "s":
            self.keep_entry()
            self.write_to_disk()
        if char == "z":
            self.keep_entry()
            self.clipstart()
        if char == "c":
            self.keep_entry()
            self.clipend()

    def clipstart(self):
        if self.flag_start_show:
            if opencv_version == 2:
                n_frame_current = self.cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)-1
            else:
                n_frame_current = self.cap.get(cv2.CAP_PROP_POS_FRAMES)-1
            str="%d"%n_frame_current
            self.text_clipstart.config(text=str)
    def clipend(self):
        if self.flag_start_show:
            if opencv_version == 2:
                n_frame_current = self.cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)-1
            else:
                n_frame_current = self.cap.get(cv2.CAP_PROP_POS_FRAMES)-1
            str = "%d" % n_frame_current
            self.text_clipend.config(text=str)
    def addclip(self):
        if self.flag_start_show:
            start_f = int(self.text_clipstart.cget("text"))
            end_f = int(self.text_clipend.cget("text"))
            try:
                l = int(self.label_var.get())
            except:
                l = -1
            # if l == -1:
            #     if version_info.major == 3:
            #         tkinter.messagebox.showerror("错误","请输入片段标签")
            #     else:
            #         tkMessageBox.showerror("错误","请输入片段标签")
            #     return
            self.start_frames.append(start_f)
            self.end_frames.append(end_f)
            self.list_names_show_clip.append("片段:%d-%d(%d)"%(start_f,end_f,l))
            self.clip_labels.append(l)
            list_names = StringVar(value=tuple(self.list_names_show_clip))
            self.list_clip.config(listvariable=list_names)
            str="共%d个"%(len(self.start_frames))
            self.text_cliptotal.config(text=str)
            str = "-1"
            self.text_clipstart.config(text=str)
            self.text_clipend.config(text=str)
            self.entry_label.delete(0, END)
            self.entry_label.insert(0, "-1")
    def checkclip(self):
        if self.flag_start_show:
            cursel = self.list_clip.curselection()
            idx_check = cursel[0]
            start_frame = self.start_frames[idx_check]
            end_frame = self.end_frames[idx_check]
            self.idx_frame = start_frame
            self.playend_frame = end_frame
            self.play_toend()
    def deleteclip(self):
        if self.flag_start_show:
            cursel = self.list_clip.curselection()
            idx_del = cursel[0]
            self.start_frames.pop(idx_del)
            self.end_frames.pop(idx_del)
            self.list_names_show_clip.pop(idx_del)
            self.clip_labels.pop(idx_del)
            list_names = StringVar(value=tuple(self.list_names_show_clip))
            self.list_clip.config(listvariable=list_names)
            str = "共%d个" % (len(self.start_frames))
            self.text_cliptotal.config(text=str)
    def check_annotated(self):
        (filepath, tempfilename) = os.path.split(self.video_lists[self.idx_video])
        (filename, extension) = os.path.splitext(tempfilename)
        filepath_write = os.path.join(filepath, filename + ".txt")
        if os.path.exists(filepath_write):
            fh_lines = open(filepath_write).readlines()
            self.start_frames = []
            self.end_frames = []
            self.clip_labels = []
            self.list_names_show_clip = []
            for line in fh_lines:
                start_f,end_f,l = line.strip().split()
                start_f = int(start_f)
                end_f = int(end_f)
                l = int(l)
                self.start_frames.append(start_f)
                self.end_frames.append(end_f)
                self.clip_labels.append(l)
                self.list_names_show_clip.append("片段:%d-%d(%d)" % (start_f, end_f, l))
            list_names = StringVar(value=tuple(self.list_names_show_clip))
            self.list_clip.config(listvariable=list_names)
            str = "共%d个" % (len(self.start_frames))
            self.text_cliptotal.config(text=str)

            (filepath, tempfilename) = os.path.split(self.video_lists[self.idx_video])
            (filename, extension) = os.path.splitext(tempfilename)
            filepath_write = os.path.join(filepath, filename + "_keyframe.txt")
            if os.path.exists(filepath_write):
                fh_lines = open(filepath_write).readlines()
                self.key_frame_ids = []
                self.list_names_show_keyframe = []
                for line in fh_lines:
                    idx = int(line.strip())
                    self.key_frame_ids.append(idx)
                    self.list_names_show_keyframe.append("关键帧:%d" % idx)
                list_names = StringVar(value=tuple(self.list_names_show_keyframe))
                self.list_keyframe.config(listvariable=list_names)
                str = "共%d个" % (len(self.key_frame_ids))
                self.text_keyframetotal.config(text=str)

    def write_to_disk(self):
        if self.flag_start_show:
            #write clips
            (filepath, tempfilename) = os.path.split(self.video_lists[self.idx_video])
            (filename, extension) = os.path.splitext(tempfilename)
            filepath_write_clip = os.path.join(filepath,filename + ".txt")
            fh = open(filepath_write_clip,"w")
            size = self.list_clip.size()
            clip_strings = self.list_clip.get(0, size)
            for s in clip_strings:
                seg = s.split(":")[1]
                start_f = int(seg.split("-")[0])
                end_f = int(seg.split("-")[1].split("(")[0])
                l = int(seg.split("(")[1].split(")")[0])
                fh.writelines("%d %d %d\n" % (start_f, end_f, l))
            fh.close()
            # self.text_general_info.delete(1.0, END)
            # self.text_general_info.insert(1.0, "写入文件：%s" % str(filepath_write))

            #write keyframes
            (filepath, tempfilename) = os.path.split(self.video_lists[self.idx_video])
            (filename, extension) = os.path.splitext(tempfilename)
            filepath_write_keyframe = os.path.join(filepath, filename + "_keyframe.txt")
            fh = open(filepath_write_keyframe, "w")
            size = self.list_keyframe.size()
            clip_strings = self.list_keyframe.get(0, size)
            for s in clip_strings:
                idx = int(s.strip().split(":")[1])
                fh.writelines("%d\n" % idx)
            fh.close()
            str_show = "%s(%s)"%(filepath_write_clip,filepath_write_keyframe.split("\\")[-1])
            self.text_general_info.delete(1.0, END)
            self.text_general_info.insert(1.0, "写入文件：%s" % str(str_show))
    def correctlabel(self):
        if self.flag_start_show:
            cursel = self.list_clip.curselection()
            idx_del = cursel[0]
            try:
                l = int(self.label_var.get())
            except:
                l = -1
            if l == -1:
                if version_info.major == 3:
                    tkinter.messagebox.showerror("错误","请输入片段标签")
                else:
                    tkMessageBox.showerror("错误","请输入片段标签")
                return
            self.clip_labels[idx_del] = l
            # self.list_names_show_clip.pop(idx_del)
            start_f = self.start_frames[idx_del]
            end_f  = self.end_frames[idx_del]
            l = self.clip_labels[idx_del]
            self.list_names_show_clip[idx_del] = "片段:%d-%d(%d)" % (start_f, end_f, l)
            list_names = StringVar(value=tuple(self.list_names_show_clip))
            self.list_clip.config(listvariable=list_names)
            str = "共%d个" % (len(self.start_frames))
            self.text_cliptotal.config(text=str)

    def addkeyframe(self):
        # print "aaaa"
        if self.flag_start_show:
            if opencv_version == 2:
                n_frame_current = self.cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES) - 1
            else:
                n_frame_current = self.cap.get(cv2.CAP_PROP_POS_FRAMES) - 1
            self.key_frame_ids.append(n_frame_current)
            self.list_names_show_keyframe.append("关键帧:%d" % (n_frame_current))
            list_names = StringVar(value=tuple(self.list_names_show_keyframe))
            self.list_keyframe.config(listvariable=list_names)
            str = "共%d个" % (len(self.key_frame_ids))
            self.text_keyframetotal.config(text=str)
            str = "-1"
    def deletekeyframe(self):
        if self.flag_start_show:
            cursel = self.list_keyframe.curselection()
            idx_del = cursel[0]
            self.key_frame_ids.pop(idx_del)
            self.list_names_show_keyframe.pop(idx_del)
            list_names = StringVar(value=tuple(self.list_names_show_keyframe))
            self.list_keyframe.config(listvariable=list_names)
            str = "共%d个" % (len(self.key_frame_ids))
            self.text_keyframetotal.config(text=str)
    def checkkeyframe(self):
        if self.flag_start_show:
            cursel = self.list_keyframe.curselection()
            idx_check = cursel[0]
            n_frame_current = self.key_frame_ids[idx_check]
            self.idx_frame = n_frame_current
            self.play_static()


def main():
    d = show()
    mainloop()


if __name__ == "__main__":
    main()