# -*- coding: utf-8 -*-
# Imports
import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import cv2
import numpy as np
import csv
import time
import datetime
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
from utils import label_map_util
from utils import visualization_utils as vis_util

#Specifies ROI Position 
ROI_POSITION = 400
# initialize .csv
with open('traffic_measurement_custom.csv', 'w') as f:
    writer = csv.writer(f)
    csv_line = 'Vehicle Type/Size, Vehicle Color, Vehicle Movement Direction, Vehicle Speed (km/h)'
    writer.writerows([csv_line.split(',')])

# if tf.__version__ < '1.4.0':
#    raise ImportError('Please upgrade your tensorflow installation to v1.4.* or later!')
# input video
cap = cv2.VideoCapture("../anpr/192.168.1.66_ch1_20000102_044633.dav")
# cap = cv2.VideoCapture("../anpr/192.168.1.66_ch1_20000102_052311.dav")
# Variables
total_passed_vehicle = 0  # using it to count vehicles
# By default I use an "SSD with Mobilenet" model here. See the detection model zoo (https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md) for a list of other models that can be run out-of-the-box with varying speeds and accuracies.
# What model to download.
MODEL_NAME = 'output_inference_graph_licensePlate_ocr'
MODEL_FILE = MODEL_NAME + '.tar'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'
# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = 'frozen_inference_graph.pb'
# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = 'label_map.pbtxt'

NUM_CLASSES = 2

# Download Model
# uncomment if you have not download the model yet
# Load a (frozen) Tensorflow model into memory.

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

# Loading label map
# Label maps map indices to category names, so that when our convolution network predicts 5, we know that this corresponds to airplane. Here I use internal utility functions, but anything that returns a dictionary mapping integers to appropriate string labels would be fine
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# Helper code
def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape((im_height, im_width,3)).astype(np.uint8)


# Detection
def object_detection_function():

    total_passed_vehicle = 0
    speed = 'waiting...'
    direction = 'waiting...'
    size = 'waiting...'
    color = 'waiting...'
    drop_frame = 0
    deviation = 3 # the constant that represents the object counting area
    roi_Lane1 = 0
    roi_Lane2 = 590
    _width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    _height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(_width, " ==== ", _height)
    # fps = 15
    # now = datetime.datetime.now()
    # formatDate = now.strftime("%d:%m:%Y %H:%M:%S")
    # fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    # output_movie = cv2.VideoWriter()
    # success = output_movie.open('Recorded_videos/output_'+str(formatDate) + '.mp4',fourcc,fps,(640, 480),True)
    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            # Definite input and output Tensors for detection_graph
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            # Each box represents a part of the image where a particular object was detected.
            detection_boxes = detection_graph.get_tensor_by_name(
                'detection_boxes:0')
            # Each score represent how level of confidence for each of the objects.
            # Score is shown on the result image, together with the class label.
            detection_scores = detection_graph.get_tensor_by_name(
                'detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name(
                'detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name(
                'num_detections:0')
            # for all the frames that are extracted from input video
            while cap.isOpened():
                # (ret, frame) = cap.read()
                # frame = cv2.flip(frame, -1)
                drop_frame += 3
                ret = cap.grab()  #grab frame but don't process it 
                if drop_frame % 2 == 0: #check if not dropping frame
                    ret, frame = cap.retrieve() #process frame
                    if not ret:
                        print ('end of the video file...')
                        break

                    input_frame = frame
                    input_frame = cv2.resize(input_frame, (1400, 760))
                    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                    image_np_expanded = np.expand_dims(input_frame, axis=0)
                    # Actual detection.
                    (boxes, scores, classes, num) = sess.run([detection_boxes, detection_scores,
                                                              detection_classes, num_detections],
                                                             feed_dict={image_tensor: image_np_expanded})
                    # Visualization of the results of a detection.
                    (counter, csv_line) = vis_util.visualize_boxes_and_labels_on_image_array(
                        cap.get(1),
                        input_frame,
                        np.squeeze(boxes),
                        np.squeeze(classes).astype(np.int32),
                        np.squeeze(scores),
                        category_index,
                        roi_Lane2,
                        y_reference = roi_Lane1,
                        deviation = deviation,
                        use_normalized_coordinates=True,
                        line_thickness=4
                    )
                    # input_frame,
                    #  2,
                    #  is_color_recognition_enabled,
                    #  np.squeeze(boxes),
                    #  np.squeeze(classes).astype(np.int32),
                    #  np.squeeze(scores),
                    #  category_index,
                    #  roi_Lane2,
                    #  y_reference = roi_Lane1,
                    #  deviation = deviation,
                    #  use_normalized_coordinates=True,
                    #  line_thickness=4
                    cv2.line(input_frame, (152, roi_Lane2), (_width, roi_Lane2), (0, 0, 0xFF), 5)
                    if counter == 1:                            
                        cv2.line(input_frame, (152, roi_Lane2), (_width, roi_Lane2), (0, 0xFF, 0), 5)
                    else:
                        cv2.line(input_frame, (152, roi_Lane2), (_width, roi_Lane2), (0, 0, 0xFF), 5)
                        # print("Current Counter ", counter)

                    # total_passed_vehicle = total_passed_vehicle + counter
                    # insert information text to video frame
                    # font = cv2.FONT_HERSHEY_SIMPLEX
                    # cv2.putText(
                    #     input_frame,
                    #     'Detected Vehicles: ' + str(total_passed_vehicle),
                    #     (10, 35),
                    #     font,
                    #     0.8,
                    #     (0, 0xFF, 0xFF),
                    #     2,
                    #     cv2.FONT_HERSHEY_SIMPLEX,
                    # )

                    # print("shape of image: ",input_frame.shape)
                    # height_img,width_img,_=input_frame.shape
                    # when the vehicle passed over line and counted, make the color of ROI line green
                    # print("ROI is : ",ROI_POSITION)
                    # if counter == 1:
                    #     # cv2.line(input_frame, (0, ROI_POSITION),
                    #     #          (width_img, ROI_POSITION), (0, 0xFF, 0), 5)
                    #     #total_passed_vehicle = total_passed_vehicle + counter
                    # else:
                        # cv2.line(input_frame, (0, ROI_POSITION),
                        #          (width_img, ROI_POSITION), (0, 0, 0xFF), 5)

                    cv2.imshow('vehicle detection', input_frame)
                    # output_movie.write(input_frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

            cap.release()
            cv2.destroyAllWindows()


object_detection_function()