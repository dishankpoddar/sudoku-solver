import numpy as np
import cv2
import math  


def cropImage(filename,filetype):
    openfile=filename+"."+filetype
    # Load an color image in grayscale
    og_image = cv2.imread(openfile,0)
    #cv2.imshow('Original sudoku',og_image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    blank_image = np.zeros(shape=og_image.shape, dtype=np.uint8)
    #cv2.imshow('Blank Image',blank_image)
    #cv2.waitKey(0)

    blank_image = cv2.GaussianBlur(og_image, (11,11), 0 )
    #cv2.imshow('Gaussian Blur',og_image)
    #cv2.waitKey(0)

    blank_image = cv2.adaptiveThreshold(blank_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 2)
    #cv2.imshow('Adaptive Threshold',blank_image)
    #cv2.waitKey(0)

    blank_image = cv2.bitwise_not(blank_image)
    #cv2.imshow('Inverted Image',blank_image)
    #cv2.waitKey(0)

    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    blank_image = cv2.dilate(blank_image, kernel,iterations=1)
    #cv2.imshow('Dilated Image',blank_image)
    #cv2.waitKey(0)

    count=0
    maxarea=-1
    for y in range(blank_image.shape[0]):
        for x in range(blank_image.shape[1]):
            if(blank_image[y,x]>=128):
                 area = cv2.floodFill(blank_image,None, (x,y), 64)
                 if(area[0]>maxarea):
                     maxPt = (x,y)
                     maxarea = area[0]
    cv2.floodFill(blank_image,None, maxPt, 255)
    for y in range(blank_image.shape[0]):
        for x in range(blank_image.shape[1]):
            if(blank_image[y,x]==64 and x!=maxPt[0] and y!=maxPt[1]):
            	area = cv2.floodFill(blank_image, None,(x,y), 0)
    blank_image = cv2.erode(blank_image, kernel,iterations=1)
    #cv2.imshow('Lines',blank_image)
    #cv2.waitKey(0)


    edges = cv2.Canny(blank_image,50,150,apertureSize = 3)
    lines = cv2.HoughLines(blank_image,1,np.pi/180,150)
    for current in lines:
        for rho,theta in current:
            if(rho==0 and theta==-100):
                continue
            a = np.cos(theta)
            b = np.sin(theta)
            if(theta>np.pi*45/180 and theta<np.pi*135/180):
                x1=0
                y1=rho/b
                x2=blank_image.shape[1]
                y2=-x2*(a/b)+rho/b
            else:
                y1=0
                x1=rho/a
                y2=blank_image.shape[0]
                x2=-y2*(b/a)+rho/a
        for pos in lines:
            if((current==pos).all()):
                continue
            for rho1,theta1 in pos:
                if(rho1==0 and theta1==-100):
                    continue
                if(abs(rho-rho1)<20 and abs(theta-theta1)<np.pi*10/180):
                    a1 = np.cos(theta1)
                    b1 = np.sin(theta1)
                    if(theta1>np.pi*45/180 and theta1<np.pi*135/180):
                        x11=0
                        y11=rho1/b1
                        x21=blank_image.shape[1]
                        y21=-x21*(a1/b1)+rho1/b1
                    else:
                        y11=0
                        x11=rho1/a1
                        y21=blank_image.shape[0]
                        x21=-y21*(b1/a1)+rho1/a1
                    if(((x11-x1)*(x11-x1)+(y11-y1)*(y11-y1))<64*64 and ((x21-x2)*(x21-x2)+(y21-y2)*(y21-y2))<64*64):
                        current[0][0] = (current[0][0]+pos[0][0])/2
                        current[0][1] = (current[0][1]+pos[0][1])/2
                        pos[0][0]=0
                        pos[0][1]=-100
    for someline in lines:
        for rho,theta in someline:
            a = np.cos(theta)
            b = np.sin(theta)
            if(theta!=0):
                m = -1*(a/b)
                c = rho/b
                blank_image=cv2.line(blank_image,(0,int(c)),(blank_image.shape[1],int(m*blank_image.shape[1]+c)),255,1)
            else:
                blank_image=cv2.line(blank_image,(rho,0),(rho,blank_image.shape[0]),255,1)
    #cv2.imshow('Hough Lines',blank_image)
    #cv2.waitKey(0)



    topEdge = (1000,1000)    
    topYIntercept=100000
    topXIntercept=0

    bottomEdge = (-1000,-1000)        
    bottomYIntercept=0
    bottomXIntercept=0

    leftEdge = (1000,1000)    
    leftXIntercept=100000
    leftYIntercept=0

    rightEdge = (-1000,-1000)        
    rightXIntercept=0
    rightYIntercept=0

    for current in lines:
        for rho,theta in current:
            if(rho==0 and theta==-100):
                continue
            a = np.cos(theta)
            b = np.sin(theta)
            xIntercept = rho/a
            yIntercept = rho/(a*b)
            if(theta>np.pi*80/180 and theta<np.pi*100/180):
                if(rho<topEdge[0]):
                    topEdge=(rho,theta)
                if(rho>bottomEdge[0]):
                    bottomEdge=(rho,theta)
            elif(theta<np.pi*10/180 or theta>np.pi*170/180):
                if(xIntercept>rightXIntercept):
                    rightEdge=(rho,theta)
                    rightXIntercept=xIntercept
                if(xIntercept<=leftXIntercept):
                    leftEdge=(rho,theta)
                    leftXIntercept=xIntercept
    flines=[topEdge,bottomEdge,rightEdge,leftEdge]
    for someline in flines:
        rho=someline[0]
        theta=someline[1]
        a = np.cos(theta)
        b = np.sin(theta)
        if(theta!=0):
            m = -1*(a/b)
            c = rho/b
            og_image=cv2.line(og_image,(0,int(c)),(blank_image.shape[1],int(m*blank_image.shape[1]+c)),0,1)
        else:
            og_image=cv2.line(og_image,(rho,0),(rho,blank_image.shape[0]),0,1)
    #cv2.imshow('Final Lines',og_image)
    #cv2.waitKey(0)




    left1, left2, right1, right2, bottom1, bottom2, top1, top2=[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]

    height=og_image.shape[0]
    width=og_image.shape[1]

    leftcos=np.cos(leftEdge[1])
    leftsin=np.sin(leftEdge[1])
    lefttan=(leftsin/leftcos)

    rightcos=np.cos(rightEdge[1])
    rightsin=np.sin(rightEdge[1])
    righttan=(rightsin/rightcos)

    if(leftEdge[1]!=0):
        left1[0]=0
        left1[1]=leftEdge[0]/leftsin
        left2[0]=width
        left2[1]=-left2[0]/lefttan + left1[1]
    else:
        left1[1]=0
        left1[0]=leftEdge[0]/leftcos
        left2[1]=height
        left2[0]=left1[0] - height*lefttan

    if(rightEdge[1]!=0):
        right1[0]=0
        right1[1]=rightEdge[0]/rightsin
        right2[0]=width
        right2[1]=-right2[0]/righttan + right1[1]
    else:
        right1[1]=0
        right1[0]=rightEdge[0]/rightcos
        right2[1]=height
        right2[0]=right1[0] - height*righttan


    bottomcos=np.cos(bottomEdge[1])
    bottomsin=np.sin(bottomEdge[1])
    bottomtan=(bottomsin/bottomcos)

    topcos=np.cos(topEdge[1])
    topsin=np.sin(topEdge[1])
    toptan=(topsin/topcos)

    bottom1[0]=0
    bottom1[1]=bottomEdge[0]/bottomsin
    bottom2[0]=width
    bottom2[1]=-bottom2[0]/bottomtan + bottom1[1]

    top1[0]=0
    top1[1]=topEdge[0]/topsin
    top2[0]=width
    top2[1]=-top2[0]/toptan + top1[1]





    #Next, we find the intersection of  these four lines
    leftA = left2[1]-left1[1]
    leftB = left1[0]-left2[0]
    leftC = leftA*left1[0] + leftB*left1[1]

    rightA = right2[1]-right1[1]
    rightB = right1[0]-right2[0]
    rightC = rightA*right1[0] + rightB*right1[1]

    topA = top2[1]-top1[1]
    topB = top1[0]-top2[0]
    topC = topA*top1[0] + topB*top1[1]

    bottomA = bottom2[1]-bottom1[1]
    bottomB = bottom1[0]-bottom2[0]
    bottomC = bottomA*bottom1[0] + bottomB*bottom1[1]

    #Intersection of left and top
    detTopLeft = leftA*topB - leftB*topA
    ptTopLeft = ((topB*leftC - leftB*topC)/detTopLeft, (leftA*topC - topA*leftC)/detTopLeft)

    #Intersection of top and right
    detTopRight = rightA*topB - rightB*topA
    ptTopRight = ((topB*rightC-rightB*topC)/detTopRight, (rightA*topC-topA*rightC)/detTopRight)

    #Intersection of right and bottom
    detBottomRight = rightA*bottomB - rightB*bottomA
    ptBottomRight = ((bottomB*rightC-rightB*bottomC)/detBottomRight, (rightA*bottomC-bottomA*rightC)/detBottomRight)

    #Intersection of bottom and left
    detBottomLeft = leftA*bottomB-leftB*bottomA
    ptBottomLeft = ((bottomB*leftC-leftB*bottomC)/detBottomLeft, (leftA*bottomC-bottomA*leftC)/detBottomLeft)




    maxLength = (ptBottomLeft[0]-ptBottomRight[0]) * (ptBottomLeft[0]-ptBottomRight[0]) + (ptBottomLeft[1]-ptBottomRight[1]) * (ptBottomLeft[1]-ptBottomRight[1])
    temp = (ptTopRight[0]-ptBottomRight[0])*(ptTopRight[0]-ptBottomRight[0]) + (ptTopRight[1]-ptBottomRight[1])*(ptTopRight[1]-ptBottomRight[1])

    if(temp>maxLength):
        maxLength = temp
    temp = (ptTopRight[0]-ptTopLeft[0])*(ptTopRight[0]-ptTopLeft[0]) + (ptTopRight[1]-ptTopLeft[1])*(ptTopRight[1]-ptTopLeft[1])

    if(temp>maxLength):
        maxLength = temp
    temp = (ptBottomLeft[0]-ptTopLeft[0])*(ptBottomLeft[0]-ptTopLeft[0]) + (ptBottomLeft[1]-ptTopLeft[1])*(ptBottomLeft[1]-ptTopLeft[1])

    if(temp>maxLength):
        maxLength = temp

    maxLength = int(math.sqrt(maxLength))



    src=(ptTopLeft,ptTopRight,ptBottomRight,ptBottomLeft)
    src=np.array(src,np.float32)
    dst=((0,0),(maxLength-1,0),(maxLength-1,maxLength-1),(0,maxLength-1))
    dst=np.array(dst,np.float32)
    #print(src,dst)
    undistort = np.zeros(shape=(maxLength,maxLength), dtype=np.uint8)
    undistort=cv2.warpPerspective(og_image, cv2.getPerspectiveTransform(src, dst), dsize=(maxLength,maxLength))
    #cv2.imshow('Final Image',undistort)
    #cv2.waitKey(0)

    closefile=filename+"-cropped."+filetype
    cv2.imwrite(closefile,undistort)





#cropImage("sudoku-original","jpg")