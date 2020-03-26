from utils.image_utils import image_saver
from datetime import datetime 
import time

is_vehicle_detected = [0]
bottom_position_of_detected_vehicle = [0]
store_oldTime_Lane1 = []
store_oldTime_Lane2 = []
global countFlag
countFlag = "True"
global countFlag1
countFlag1 = "True"

def count_objects(top, bottom, right, left, temp, start_time, current_frame_number, crop_img, roi_position, roi_position1, y_min, y_max, deviation):   
        direction = "n.a." # means not available, it is just initialization
        isInROI = False # is the object that is inside Region Of Interest
        update_csv = False
        Lane = ""
        global countFlag
        global countFlag1

        if countFlag=="False":
            if(abs(((right+left)/2))>0 and abs(((right+left)/2))<500):  
                if top >= roi_position and  top < 395:
                    global countFlag
                    countFlag = "True"
                    print "ELSE COUNTING OBJECT DISABLED LANE 1"
        
        # if countFlag1=="False":
        #     if(abs(((right+left)/2))>502 and abs(((right+left)/2))<1024): 
        #         if top >= roi_position1:
        #             global countFlag1
        #             countFlag1 = "True"
        #             print "ELSE COUNTING OBJECT DISABLED LANE 2"

        if (abs(((bottom+top)/2)-roi_position) < 20):
          # print("right: ", right, " left:  ", left, "centroid " ,abs(((right+left)/2)) ," roi_position: ", roi_position, "difference " ,(abs(((right+left)/2)-roi_position)), " deviation: ", deviation)
            if(abs(((right+left)/2))>0 and abs(((right+left)/2))<500):
            
                if countFlag == "True":
                    print "IF COUNTING OBJECT ENABLED"
                    is_vehicle_detected.insert(0,1)
                    Lane = "Lane_1"
                    temp = temp
                    global countFlag
                    countFlag = "False"
            

        # elif(abs(((bottom+top)/2)-roi_position1) < 20):

        #     if(abs(((right+left)/2))>502 and abs(((right+left)/2))<1024):
        #         if countFlag1 == "True":
        #             print "IF COUNTING OBJECT ENABLED LANE 2"
        #             is_vehicle_detected.insert(0,1)
        #             Lane = "Lane_2"
        #             global countFlag1
        #             countFlag1 = "False"
           
        
          # image_saver.save_image(crop_img) # save detected object image
        # else:
          # print("right: ", right, " left:  ", left, "centroid " ,abs(((right+left)/2)) ," roi_position: ", roi_position, "difference " ,(abs(((right+left)/2)-roi_position)), " deviation: ", deviation)
        else:
            Lane="none"

        if(bottom > bottom_position_of_detected_vehicle[0]):
                direction = "down"
        else:
                direction = "up"

        return direction, Lane, is_vehicle_detected, update_csv, temp

