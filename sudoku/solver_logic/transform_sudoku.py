import numpy as np
import cv2
import math  
from . import digit_recognizer as dr

def preProcess(cell):
    rowTop=-1
    rowBottom=-1
    colLeft=-1
    colRight=-1
    thresholdBottom = 1
    thresholdTop = 1
    thresholdLeft = 1
    thresholdRight = 1
    center = int(cell.shape[0]/2)

    #print(cell.shape)
    for i in range(center):
        if(rowTop==-1):
            temp = cell[i,0:]
            if(cv2.sumElems(temp)[0] > thresholdTop or i==cell.shape[0]-1):
               rowTop = i
               #print('top',i)

        if(rowBottom==-1):
            temp = cell[cell.shape[0]-i-1,0:]
            if(cv2.sumElems(temp)[0] > thresholdBottom or i==cell.shape[0]-1):
               rowBottom = cell.shape[0]-i
               #print('bottom',cell.shape[0]-i)

        if(colLeft==-1):
            temp = cell[0:,i]
            if(cv2.sumElems(temp)[0] > thresholdLeft or i==cell.shape[1]-1):
               colLeft = i
               #print('left',i)

        if(colRight==-1):
            temp = cell[0:,cell.shape[1]-i-1]
            if(cv2.sumElems(temp)[0] > thresholdRight or i==cell.shape[1]-1):
               colRight = cell.shape[1]-i
               #print('right',cell.shape[1]-i)
               
    if(rowTop==-1):
        rowTop=int(cell.shape[0]/2)
    if(rowBottom==-1):
        rowBottom=int(cell.shape[0]/2)
    if(colLeft==-1):
        colLeft=int(cell.shape[0]/2)
    if(colRight==-1):
        colRight=int(cell.shape[0]/2)


    new_cell = np.zeros(shape=cell.shape, dtype=np.uint8)
    startAtX = int((new_cell.shape[1]/2)-(colRight-colLeft)/2)
    endAtX = int((new_cell.shape[1]/2)+(colRight-colLeft)/2)
    startAtY = int((new_cell.shape[0]/2)-(rowBottom-rowTop)/2)
    endAtY = int((new_cell.shape[0]/2)+(rowBottom-rowTop)/2)

    empty = 255*np.ones(shape=cell.shape, dtype=np.uint8)

    for y in range(startAtY,endAtY):
        for x in range(startAtX,endAtX):
            new_cell[y,x]=cell[rowTop+(y-startAtY),colLeft+(x-startAtX)]

    for i in range(new_cell.shape[0]):
        cv2.floodFill(new_cell,None, (0,i), 0)
        cv2.floodFill(new_cell,None, (new_cell.shape[1]-1,i), 0)
        cv2.floodFill(new_cell,None, (i,0), 0)
        cv2.floodFill(new_cell,None, (i,new_cell.shape[1]-1), 0)

    
    #img_concate_Hori=np.concatenate((new_cell,empty,cell),axis=1)
    #cv2.imshow('concatenated_Hori',img_concate_Hori)
    #cv2.waitKey(0)
    return new_cell



def transformImage(base,filename,filetype,size):
    openfile=base+"/"+filename+"-cropped."+filetype
    # Load an color image in grayscale
    cropped_image = cv2.imread(openfile,0)
    #cv2.imshow('Cropped sudoku',cropped_image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    undistortedThreshed = cv2.adaptiveThreshold(cropped_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 101, 1)
    #cv2.imshow('Cropped sudoku',undistortedThreshed)
    #cv2.waitKey(0)
    dist = math.ceil(cropped_image.shape[0]/size)

    blank_cell = np.zeros(shape=(dist,dist), dtype=np.uint8)

    blank_arr=[[0 for i in range(size)] for j in range(size)]
    for i in range(size):
        for j in range(size):
            x=0
            while(x<dist and i*dist+x<undistortedThreshed.shape[0]):
                y=0
                while(y<dist and j*dist+y<undistortedThreshed.shape[1]):
                    blank_cell[x,y]=undistortedThreshed[i*dist+x, j*dist+y]
                    y=y+1
                x=x+1
            
            #cv2.imshow('Before',blank_cell)
            #cv2.waitKey(0)
            for y in range(blank_cell.shape[0]):
                for x in range(blank_cell.shape[1]):
                    if(blank_cell[y,x]>=128):
                        tempx = blank_cell[0:,x]
                        tempy = blank_cell[y,0:]
                        n_white_pix_x = np.sum(tempx == 255)
                        n_white_pix_y = np.sum(tempy == 255)
                        if(n_white_pix_x==len(tempx) or n_white_pix_y==len(tempy)):
                            cv2.floodFill(blank_cell,None, (x,y), 0)

            for y in range(blank_cell.shape[0]):
                for x in range(blank_cell.shape[1]):
                    if(blank_cell[y,x]!=255):
                        cv2.floodFill(blank_cell,None, (x,y), 0)
            #cv2.imshow('Between',blank_cell)
            #cv2.waitKey(0)
            maxarea=-1
            maxPt=(0,0)
            for y in range(blank_cell.shape[0]):
                for x in range(blank_cell.shape[1]):
                    if(blank_cell[y,x]>=128):
                        area = cv2.floodFill(blank_cell,None, (x,y), 64)
                        if(area[0]>maxarea):
                            maxPt = (x,y)
                            maxarea = area[0]
            for y in range(int(1*blank_cell.shape[0]/3),int(2*blank_cell.shape[0]/3)):
                for x in range(int(1*blank_cell.shape[1]/3),int(2*blank_cell.shape[1]/3)):
                    if(blank_cell[y,x]==64):
                        area = cv2.floodFill(blank_cell,None, (x,y), 32)
                        if(area[0]>=maxarea):
                            maxPt = (x,y)
                            maxarea = area[0]
            if(maxPt[1]>=int(1*blank_cell.shape[0]/3) and maxPt[1]<=int(2*blank_cell.shape[0]/3) and maxPt[0]>=int(1*blank_cell.shape[1]/3) and maxPt[0]<=int(2*blank_cell.shape[1]/3) and blank_cell[maxPt[1],maxPt[0]]>0):
                cv2.floodFill(blank_cell,None, maxPt, 255)
                for y in range(blank_cell.shape[0]):
                    for x in range(blank_cell.shape[1]):
                        if((blank_cell[y,x]==64 or blank_cell[y,x]==32) and x!=maxPt[0] and y!=maxPt[1]):
                            area = cv2.floodFill(blank_cell, None,(x,y), 0)
            else:
                for y in range(blank_cell.shape[0]):
                    for x in range(blank_cell.shape[1]):
                        if(blank_cell[y,x]==64 or blank_cell[y,x]==32):
                            area = cv2.floodFill(blank_cell, None,(x,y), 0)
            n_white_pix = np.sum(blank_cell == 255)
            #print(n_white_pix,undistortedThreshed.shape[0]*undistortedThreshed.shape[1])
            #cv2.imshow('After',blank_cell)
            #cv2.waitKey(0)
            if(n_white_pix>blank_cell.shape[0]*blank_cell.shape[1]*0.01):
                #cv2.imshow('Cropped sudoku',blank_cell)
                #cv2.waitKey(0)
                blank_cell_pp=preProcess(blank_cell)
                closefile=base+"/crops/"+filename+"-"+str(i)+str(j)+"."+filetype
                cv2.imwrite(closefile,blank_cell_pp)
                blank_arr[i][j]=dr.predictDigit(closefile)[0]
                #print(blank_arr[i][j])
    return(blank_arr)
    """
    for i in range(9):
        for j in range(9):
            print(blank_arr[i][j],end="\t")
            if((j+1)%3==0):
                print(end="\t")
        print(end="\n")
        if((i+1)%3==0):
            print(end="\n")
    """


#transformImage("sudoku1","jpg")