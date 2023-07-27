import cv2 # for image processing
import numpy as np #mathematical library for image handling

cap = cv2.VideoCapture(0)
background = cv2.imread('./image.jpg')

while cap.isOpened():
    #caturing the live frame
    ret, current_frame = cap.read()
    if ret:
        #converting from rgb to hsv color space
        hsv_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2HSV)

        #range for lower red USING COLOR BLUE
        l_red = np.array([90,103,20])
        u_red = np.array([119,255,255])
        mask1 = cv2.inRange(hsv_frame, l_red, u_red)

        #range for lower red USING COLOR BLUE
        l_red2 = np.array([180,98,20])
        u_red2 = np.array([170,255,255])
        mask2 = cv2.inRange(hsv_frame, l_red2, u_red2)

        #generating the final red mask
        red_mask = mask1 + mask2

        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, np.ones((3,3), np.uint8), iterations = 10) 
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_DILATE, np.ones((3,3), np.uint8), iterations = 1)  

        #subsituting the red portion with backgrpound image
        part1 = cv2.bitwise_and(background, background, mask= red_mask)
        
        # detecting things which are not red
        red_free = cv2.bitwise_not(red_mask)

        # if cloak is not present show the current image
        part2 = cv2.bitwise_and(current_frame, current_frame, mask= red_free)


        #final output
        cv2.imshow("cloak", part1 + part2)
        if cv2.waitKey(5) == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()