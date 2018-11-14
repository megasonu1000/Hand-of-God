###############################################################################
#     Project C (Hand of God) Dated July 3rd 2018 Tuesday 1654 Hours          #
#     Developer- Kuldeep Paul                                                 #
#     Developed for Quinch Systems Pvt. Ltd.                                  #
#     Copyright 2018                                                          #
###############################################################################

# OpenCV Python program to detect palm in video frame
# import libraries of python OpenCV
import datetime
import imutils
import time
import cv2
from Position import position
# capture frames from camera
cap = cv2.VideoCapture(0)
firstFrame = None

# Trained XML classifiers describes some features of some object we want to detect
palm_cascade = cv2.CascadeClassifier('open_palm.xml')
palm_no=0
# loop runs if capturing has been initialized.
while True:
    palm_no=0
    # reads frames from a video
    ret, frame = cap.read()
    frames = cv2.flip(frame, +1)
    # convert to gray scale of each frames and blur it
    frames = imutils.resize(frames, width=456, height=256)
    gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if firstFrame is None:
        firstFrame = gray
        cv2.imshow('first frame', gray)
        prev_frame = firstFrame
        continue

    cv2.imshow('previous frame', gray)
    frameDelta = cv2.absdiff(prev_frame, gray)
    cv2.imshow('delta', frameDelta)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    prev_frame = gray
    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    cv2.imshow('threshold', thresh)
    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < 700:
            continue

        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frames, (x, y), (x + w, y + h), (0, 255, 0), 1)
        roi_x = x
        roi_y = y
        roi_w = w
        roi_h = h
        roi = frames[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]
        # Detects palms of different sizes in the input image
        palms = palm_cascade.detectMultiScale(roi, 1.1, 1)
        # To draw a circle in each palm
        for (x,y,w,h) in palms:
            #filter smaller palm_cascade
            if (w+h)/2 >50 :
                px = x+w/2
                py = y+h/2
                cv2.circle(frames, (roi_x+px, roi_y+py), (w+h)/2, (0,0,255), 2)
                cv2.circle(frames, (roi_x+px, roi_y+py), (w+h)/2+10, (0,255,255), 2)
                cv2.circle(frames, (roi_x+px, roi_y+py), (w+h)/2+30, (255,0,255), 2)
                cv2.circle(frames, (roi_x+px, roi_y+py), (w+h)/2+70, (255,255,0), 2)
                cv2.circle(frames, (roi_x+px, roi_y+py), (w+h)/2+90, (0,255,0), 2)
                palm_no += 1
                position(roi_x+px, roi_y+py)  # positions the cursor to a definite location
                print str(palm_no) + ":" + str(px) + "," + str(py) + "   " + str((w+h)/2)
                cv2.putText(frames, "Palm" + str(palm_no), (roi_x, roi_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 2,0), 4)
        # Display frames in a window
        cv2.imshow('feed', frames)

    # Wait for Esc key to stop
    if cv2.waitKey(33)==27:
        break

# De-allocate any associated memory usage
cv2.destroyAllWindows()
