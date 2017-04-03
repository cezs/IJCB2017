#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv

prediction_list_path='/home/cs/remote/titanx/media/win/_/IJCB2017/valid/ijcb2017-yolo-voc/comp4_det_test_2.txt'[0:]
new_prediction_list_path='/home/cs/remote/titanx/media/win/_/IJCB2017/ijcb2017-yolo-voc-scores.csv'[0:]

def read_predictions_file(list_path):
    predictions_list = []
    with open(list_path, 'rb') as predictions:
        for line in predictions:
            fields = line.strip().split()
            image_filename = str(fields[0])
            class_probability = float(fields[1])
            bbox_x1 = float(fields[2])
            bbox_y1 = float(fields[3])
            bbox_x2 = float(fields[4])
            bbox_y2 = float(fields[5])
            predictions_list.append([image_filename, bbox_x1, bbox_y1, bbox_x2 - bbox_x1, bbox_y2 - bbox_y1, class_probability])
    return predictions_list

def write_predictions_file(predictions_list, list_path):
    with open(list_path, 'wb') as out_file:
        writer = csv.writer(out_file, delimiter=',')
        for entry in predictions_list:
            writer.writerow(entry)

predictions_list = read_predictions_file(prediction_list_path)
write_predictions_file(predictions_list, new_prediction_list_path)
