import numpy as np
import cv2
from os import listdir

class Video():

    def __init__(self):
        pass

    def save_frames(self):
        cap = cv2.VideoCapture("data/Vídeos/potholessnow.mp4")
        i=0
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret==True:
                if(i>630):
                    cap.release()
                    break
                name = "00000000"+str(i)+".jpg"
                name = name[len(name)-10:len(name)]
                cv2.imwrite('data/frames2/'+name,frame)
                i+=1
        cap.release()
    
    def make_video(self,video_index,fps,size,path_frames):
        video_name = "000000000"+str(video_index)
        video_name = video_name[len(video_name)-8:len(video_name)]
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter("data/results/"+video_name+'.avi',fourcc, fps, size)

        files = list(listdir(path_frames))

        for x in files:
            frame = cv2.imread(path_frames+x)
            out.write(frame)

        out.release()
        return video_name+'.avi'