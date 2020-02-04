#classes and subclasses to import
import cv2
import numpy as np

####################################################################################################
# SOME GLOBAL VARIABLES 

# define range of blue color in HSV
LOWER_BLUE = np.array([120,0,0])
UPPER_BLUE = np.array([255,0,0])

# define range of green color in HSV
LOWER_GREEN = np.array([0,0,0])
UPPER_GREEN = np.array([0,255,0])

# define range of red color in HSV
LOWER_RED = np.array([0,0,0])
UPPER_RED = np.array([0,0,255])

color = {0 : 'Blue', 1 : 'Green', 2 : 'Red'}

#####################################################################################################


def detect(img):
#####################################################################################################
    #Write your code here!!!
#####################################################################################################

    hsv = cv2.bilateralFilter(img,9,75,75)
    #hsv  = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    cv2.imshow("HSV", hsv)

    F = hsv.copy()
    F[:,:,0] = 0
    F[:,:,2] = 0
    
    cv2.imshow("F",F)
    #Mask and Threshold the BGR image to get only primary colors
    mask_blue   = cv2.inRange(hsv.copy(), LOWER_BLUE, UPPER_BLUE)
    mask_green  = cv2.inRange(hsv.copy(), LOWER_GREEN, UPPER_GREEN)
    mask_red    = cv2.inRange(hsv.copy(), LOWER_RED, UPPER_RED)

    cv2.imshow("BLUE",mask_blue)
    cv2.imshow("GREEN", mask_green)
    cv2.imshow("RED",  mask_red)

    ret1, thresh1 = cv2.threshold(mask_blue,120,255,0)
    ret2, thresh2 = cv2.threshold(mask_green,120,255,0)
    ret3, thresh3 = cv2.threshold(mask_red,120,255,0)

    contours = [[],[],[]]
      
    im, contours[0], hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    im, contours[1], hierarchy = cv2.findContours(thresh2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    im, contours[2], hierarchy = cv2.findContours(thresh3,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    #print("Blue Len : " , len(contours[0]))
    #print("Green Len : ", len(contours[1]))
    #print("Red Len : ", len(contours[2])) 
    cv2.waitKey(0)

    blue_len   = len(contours[0])
    green_len  = len(contours[1])
    red_len    = len(contours[2])

    print(blue_len, green_len, red_len)
    if (blue_len > red_len and blue_len > green_len):
	i = 0
    elif (red_len > blue_len and red_len > green_len):
        i = 2
    elif (green_len > red_len and green_len > blue_len):
	i = 1
    else:
	pass

    count = {'Triangle' : 0, 'Square' : 0, 'Circle' : 0}
	    	
    for j in contours[i]:
        M = cv2.moments(j)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        approx = cv2.approxPolyDP(j,0.01*cv2.arcLength(j,True),True)
        vertices = len(approx)
       
        
        if vertices == 3:
            shape = "Triangle"
        elif vertices == 4:
            shape = "Square"   
        else :
            shape = "Circle"
        
	count[shape] += 1

    # cv2.destroyAllWindows()
    print(count, color[i])

img = cv2.imread('image.png')
detect(img)        

