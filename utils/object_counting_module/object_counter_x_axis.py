from utils.image_utils import image_saver
from datetime import datetime 
import time

is_vehicle_detected = [0]
bottom_position_of_detected_vehicle = [0]

store_oldTime_Lane1 = []
store_oldTime_Lane2 = []

def count_objects_x_axis(top, bottom, right, left, temp, start_time, current_frame_number, crop_img, roi_position, roi_position1, y_min, y_max, deviation):   
        direction = "n.a." # means not available, it is just initialization
        isInROI = False # is the object that is inside Region Of Interest
        update_csv = False
        Lane = ""
        if (abs(((right+left)/2)-roi_position) < 40):
          # print("right: ", right, " left:  ", left, "centroid " ,abs(((right+left)/2)) ," roi_position: ", roi_position, "difference " ,(abs(((right+left)/2)-roi_position)), " deviation: ", deviation)
          if(abs(((bottom+top)/2))>0 and abs(((bottom+top)/2))<260):
            
            newTime = int(time.time()*1000.0)
            # for first entry
            if(len(store_oldTime_Lane1) == 0):
              is_vehicle_detected.insert(0,1)
              Lane = "Lane_1"
              store_oldTime_Lane1.append(start_time)
            else:  
              # print(newTime)
              # print(store_oldTime_Lane1[-1])
              timeDiff = newTime - store_oldTime_Lane1[-1]
              # print("timeDiff : ",timeDiff)
              convertSeconds = timeDiff/1000
              print("Difference in Seconds: ",convertSeconds)
              if(convertSeconds < 0.5):
                is_vehicle_detected.insert(0,None)
                Lane = "None"
                # del store_oldTime_Lane1[0] 
              else:
                is_vehicle_detected.insert(0,1)
                Lane = "Lane_1"
                store_oldTime_Lane1.append(start_time)
            

        elif(abs(((right+left)/2)-roi_position1) < 40):

          if(abs(((bottom+top)/2))>261 and abs(((bottom+top)/2))<720):
           
            newTime = int(time.time()*1000.0)
            # for first entry
            if(len(store_oldTime_Lane2) == 0):
              is_vehicle_detected.insert(0,1)
              Lane = "Lane_2"
              store_oldTime_Lane2.append(start_time)
            else:  
              # print(newTime)
              # print(store_oldTime_Lane2[-1])
              timeDiff = newTime - store_oldTime_Lane2[-1]
              # print("timeDiff : ",timeDiff)
              convertSeconds = timeDiff/1000
              print("Difference in Seconds: ",convertSeconds)
              if(convertSeconds < 0.5):
                is_vehicle_detected.insert(0,None)
                Lane = "None"
                # del store_oldTime_Lane2[0] 
              else:
                is_vehicle_detected.insert(0,1)
                Lane = "Lane_2"
                store_oldTime_Lane2.append(start_time)
        
          # image_saver.save_image(crop_img) # save detected object image
        # else:
          # print("right: ", right, " left:  ", left, "centroid " ,abs(((right+left)/2)) ," roi_position: ", roi_position, "difference " ,(abs(((right+left)/2)-roi_position)), " deviation: ", deviation)

        if(bottom > bottom_position_of_detected_vehicle[0]):
                direction = "down"
        else:
                direction = "up"

        bottom_position_of_detected_vehicle.insert(0,(bottom))

        return direction, Lane, is_vehicle_detected, update_csv

