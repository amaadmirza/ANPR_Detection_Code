from utils.image_utils import image_saver
from datetime import datetime 
import time

is_vehicle_detected = [0]
bottom_position_of_detected_vehicle = [0]
global countFlag1
countFlag1 = "True"

def count_objects(top, bottom, right, left, start_time, current_frame_number, crop_img, roi_position, roi_position1, y_min, y_max, deviation):   
        direction = "n.a." # means not available, it is just initialization
        isInROI = False # is the object that is inside Region Of Interest
        update_csv = False
        Lane = ""
        # global countFlag
        global countFlag1
        
        if countFlag1=="True":
            if(abs(((right+left)/2))>152 and abs(((right+left)/2))<1400): 
                
                if bottom >= roi_position1 and bottom < roi_position1+30:
                        # global countFlag1
                        print(bottom)
                        print(roi_position1)
                        countFlag1 = "False"
                        print ("IF COUNTING OBJECT ENABLED LANE 2")
        print((bottom+top)/2)
        if(abs(((bottom+top)/2)-roi_position1) < 10): #centroid point difference slot
            if(abs(((right+left)/2))>152 and abs(((right+left)/2))<1400):
                if countFlag1 == "False":
                    print ("ELSE COUNTING OBJECT DISABLED LANE 2")
                    is_vehicle_detected.insert(0,1)
                    Lane = "Lane_2"
                    # global countFlag1
                    countFlag1 = "True"
                    image_saver.save_image(crop_img) # save detected object image
          # image_saver.save_image(crop_img) # save detected object image
        else:
            Lane="none"

        if(bottom > bottom_position_of_detected_vehicle[0]):
                direction = "down"
        else:
                direction = "up"

        return "down", Lane, is_vehicle_detected, update_csv, "a"

