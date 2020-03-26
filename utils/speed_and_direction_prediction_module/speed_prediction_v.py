#!/usr/bin/python
# -*- coding: utf-8 -*-

from utils.image_utils import image_saver

is_vehicle_detected = [0]
current_frame_number_list = [0]
bottom_position_of_detected_vehicle = [0]


def predict_speed(
    top,
    bottom,
    right,
    left,
    current_frame_number,
    crop_img,
    roi_position,
    ):
    speed = 'n.a.'  # means not available, it is just initialization
    direction = 'n.a.'  # means not available, it is just initialization
    scale_constant = 1  # manual scaling because we did not performed camera calibration
    isInROI = True  # is the object that is inside Region Of Interest
    update_csv = False

    if bottom < 250:
        scale_constant = 1  # scale_constant is used for manual scaling because we did not performed camera calibration
    elif bottom > 250 and bottom < 320:
        scale_constant = 2  # scale_constant is used for manual scaling because we did not performed camera calibration
    else:
        isInROI = False
    roi_position = 400
    print("ROI IS in function: ",roi_position)
    
    print(len(bottom_position_of_detected_vehicle), " != 0 and ",  (roi_position-50), " < ", right, " and ", right, " < ", (roi_position+50))
    if len(bottom_position_of_detected_vehicle) != 0 and (roi_position-50) < right and right < (roi_position+50):
        print("Vehicle Detected at: ",bottom,bottom_position_of_detected_vehicle[0])
        is_vehicle_detected.insert(0, 1)
        update_csv = True
        image_saver.save_image(crop_img)  # save detected vehicle image

    # for debugging
    print("Top [0]: " + str(bottom_position_of_detected_vehicle[0]))
    print("Top: " + str(right))
    # if bottom > bottom_position_of_detected_vehicle[0]:
    #     direction = 'down'
    # else:
    #     direction = 'up'

    # if isInROI:
    #     pixel_length = bottom - bottom_position_of_detected_vehicle[0]
    #     scale_real_length = pixel_length * 44  # multiplied by 44 to convert pixel length to real length in meters (chenge 44 to get length in meters for your case)
    #     total_time_passed = current_frame_number - current_frame_number_list[0]
    #     scale_real_time_passed = total_time_passed * 24  # get the elapsed total time for a vehicle to pass through ROI area (24 = fps)
    #     if scale_real_time_passed != 0:
    #         speed = scale_real_length / scale_real_time_passed / scale_constant  # performing manual scaling because we have not performed camera calibration
    #         speed = speed / 6 * 40  # use reference constant to get vehicle speed prediction in kilometer unit
    #         current_frame_number_list.insert(0, current_frame_number)
    #         bottom_position_of_detected_vehicle.insert(0, right)

    return ("down", "speed", is_vehicle_detected, update_csv)
