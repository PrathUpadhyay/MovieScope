import glob
import os
import pandas as pd
import cv2
from sys import argv
import numpy as np
import scenedetect
genre=["horror","romance"]

def draw_flow(img, flow, step=16):
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1).astype(int)
    fx, fy = flow[y,x].T
    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.polylines(vis, lines, 0, (0, 255, 0))
    for (x1, y1), (x2, y2) in lines:
        cv2.circle(vis, (x1, y1), 1, (0, 255, 0), -1)
    return vis


def draw_hsv(flow):
    h, w = flow.shape[:2]
    fx, fy = flow[:,:,0], flow[:,:,1]
    ang = np.arctan2(fy, fx) + np.pi
    v = np.sqrt(fx*fx+fy*fy)
    hsv = np.zeros((h, w, 3), np.uint8)
    hsv[...,0] = ang*(180/np.pi/2)
    hsv[...,1] = 255
    hsv[...,2] = np.minimum(v*4, 255)
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return bgr


def warp_flow(img, flow):
    h, w = flow.shape[:2]
    flow = -flow
    flow[:,:,0] += np.arange(w)
    flow[:,:,1] += np.arange(h)[:,np.newaxis]
    res = cv2.remap(img, flow, None, cv2.INTER_LINEAR)
    return res


def optical_flow(video):
    cap = cv2.VideoCapture(video)
    print video
    ret, prev = cap.read()
    prev = cv2.resize(prev, (224,224)) 
    prevgray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
    show_hsv = False
    show_glitch = False
    cur_glitch = prev.copy()

    while(True):
        ret,img = cap.read()
        img = cv2.resize(img, (224, 224))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
        flow = cv2.calcOpticalFlowFarneback(prevgray, gray, 0.5, 3, 15, 3, 5, 1.2, 0)
        prevgray = gray
        print
        print
        cv2.imshow('flow', draw_flow(gray, flow))
        if show_hsv:
            cv2.imshow('flow HSV', draw_hsv(flow))
        if show_glitch:
            cur_glitch = warp_flow(cur_glitch, flow)
            cv2.imshow('glitch', cur_glitch)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        ch = 0xFF & cv2.waitKey(5)
        if ch == 27:
            break
        if ch == ord('1'):
            show_hsv = not show_hsv
            print('HSV flow visualization is', ['off', 'on'][show_hsv])
        if ch == ord('2'):
            show_glitch = not show_glitch
            if show_glitch:
                cur_glitch = img.copy()
            print('glitch is', ['off', 'on'][show_glitch])
    cv2.destroyAllWindows()

def main():
    
    prevdir = os.getcwd()
    for g in genre[:1]:
        os.chdir('./genres/'+g)
        for file_format in ["*.mp4"]:#, "*.webm"):
            title=glob.glob(file_format)
            for video in title[:1]:
                optical_flow(video)  


if __name__ == '__main__':
    optical_flow(argv[1])
   #main()
    
