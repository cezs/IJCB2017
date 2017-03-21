#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import csv
import argparse

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def script_info(msg):
    print bcolors.HEADER + "[INFO] " + str(msg) + bcolors.ENDC

def lib_info(msg):
    print bcolors.OKBLUE + "[INFO] " + str(msg) + bcolors.ENDC

def ijcb2017_to_darknet(ijcb2017_annotations, use_original_classes):
    """
    covert to darknet format and store in python lists.
    returns bboxes with classes and corresponding images filenames.
    """
    filenames = []
    subject_id= []
    x = []
    y = []
    width = []
    height = []

    # append each image filename for training to list 
    with open(ijcb2017_annotations, 'r') as img_sid_bbox_list:
        reader = csv.reader(img_sid_bbox_list)
        next(reader)
        for row in reader:
            filenames.append(row[1])
            if (use_original_classes):
                # use original class
                # TODO: map original subject_id to label
                # instead of using int() + 1 hack
                subject_id.append(int(row[2]) + 1)
            else:
                # just detect
                subject_id.append(1)
            # recalculate starting position of bounding box to the center
            # of it instead of the supplied upper left corner and make
            # position as well as dimensions of this bounding box relative
            # to image dimensions
            x.append((float(row[3]) + float(row[5]) / 2.0) / img_width)
            y.append((float(row[4]) + float(row[6]) / 2.0) / img_height)
            width.append(float(row[5]) / img_width)
            height.append(float(row[6]) / img_height)
    return filenames, subject_id, x, y, width, height


def create_darknet_list(output_training_listing, training_images, train_filenames):
    """training list"""
    # print converted listing of images for training 
    with open(output_training_listing, 'wb') as out_train_listing:
        # note the use of set to from list from only unique filenames
        for f in set(train_filenames):
            out_train_listing.write("{}/{}\n".format(training_images, f))

def create_darknet_annotations(train_filenames, training_images, subject_id, x, y, width, height):
    """create individual training annotations"""
    # make list of filenames for files which are going to store individual
    # id, x, y, width and height
    individual_filenames = []

    for f in train_filenames:
        individual_filenames.append(f.rsplit(".", 1)[0] + '.txt')

    for i in range(len(x)):
        with open("{}/{}".format(training_images, individual_filenames[i]), 'a') as newfile:
            newfile.write("{} {} {} {} {}\n".format(subject_id[i], \
                                                    x[i], \
                                                    y[i], \
                                                    width[i], \
                                                    height[i]))

def create_labels_file(labels_file, use_original_classes, subject_id):
    """labels file"""
    with open(labels_file, 'wb') as labels:
        if (use_original_classes):
            # use original classification
            for i in range(len(set(subject_id))):
                labels.write("{}\n".format(i))
        else:
            # use binary classification
            labels.write("{}\n".format(0))
            labels.write("{}\n".format(1))

def create_names_file(names_file, use_original_classes, subject_id):
    """names file"""
    with open(names_file, 'wb') as names:
            if (use_original_classes):
                # use original classification
                for i in set(subject_id):
                    names.write("{}\n".format(i))
            else:
                # use binary classification
                names.write("{}\n".format("nothing"))
                names.write("{}\n".format("face"))

def create_darknet_data_configuration_file(config_file_path):
    """configuration file"""
    config_file = config_file_path

    with open(config_file, 'wb') as cfg_file:
        if (use_original_classes):
            # use original classification
            cfg_file.write("{} = {}\n".format("classess",len(set(subject_id))))
        else:
            # use binary classification
            cfg_file.write("{} = {}\n".format("classess", 2))
        cfg_file.write("{} = {}\n".format("train", output_training_listing))
        cfg_file.write("{} = {}\n".format("valid", output_training_listing))
        cfg_file.write("{} = {}\n".format("labels", labels_file))
        cfg_file.write("{} = {}\n".format("names", names_file))
        cfg_file.write("{} = {}\n".format("backup","backup"))

def calculate_classes(input_training_listing, ):
    classes = []
    # append each image filename for training to list 
    with open(input_training_listing, 'r') as in_train_listing:
        reader = csv.reader(in_train_listing)
        next(reader)
        for row in reader:
            classes.append(row[2])
    print(len(set(classes)))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Unconstrained Face Detection and Open Set Recognition Challenge in Darknet")
    parser.add_argument('-a', '--resized_dataset', dest='a', action='store_true', help='Use resized dataset')
    parser.add_argument('-b', '--original_classes', dest='b', action='store_true', help='Use original classes')
    parser.add_argument('-c', '--training_list', dest='c', action='store_true', help='Create Darknet list for training')
    parser.add_argument('-d', '--training_annotations', dest='d', action='store_true', help='Create Darknet annotations for training')
    parser.add_argument('-e', '--validation_list', dest='e', action='store_true', help='Create Darknet list for validation')
    parser.add_argument('-f', '--validation_annotations', dest='f', action='store_true', help='Create Darknet annotations for validation')
    parser.add_argument('-g', '--labels_file', dest='g', action='store_true', help='Create labels file')
    parser.add_argument('-i', '--names_file', dest='i', action='store_true', help='Create names file')
    parser.add_argument('-j', '--data_cfg_file', dest='j', action='store_true', help='Create data configuration file')
    args = parser.parse_args()

    print(bcolors.BOLD + "Entered main function" + bcolors.ENDC)

    use_resized_dataset = args.a
    use_original_classes = args.b
    do_create_darknet_list_for_training = args.c
    do_create_darknet_annotations_for_training = args.d
    do_create_darknet_list_for_validation = args.e
    do_create_darknet_annotations_for_validation = args.f
    do_create_labels_file = args.g
    do_create_names_file = args.i
    do_create_configuration_file = args.j
    
    config_file = '/media/win/_/IJCB2017/cfg/ijcb2017.data'
    labels_file = '/media/win/_/IJCB2017/data/ijcb2017.labels'
    names_file = '/media/win/_/IJCB2017/data/ijcb2017.names'

    if not use_resized_dataset:
        input_training_listing = '/media/win/_/IJCB2017/protocol/training_updated.csv'
        output_training_listing ='/media/win/_/IJCB2017/ijcb2017_updated.train.list'
        training_images = '/media/win/_/IJCB2017/training'

        input_validation_listing = '/media/win/_/IJCB2017/protocol/validation.csv'
        output_validation_listing ='/media/win/_/IJCB2017/ijcb2017.valid.list'
        validation_images = '/media/win/_/IJCB2017/validation'

        img_height = 3456.0
        img_width = 5184.0
    else:
        input_training_listing = '/media/win/_/IJCB2017/protocol/training_resized.csv'
        output_training_listing ='/media/win/_/IJCB2017/ijcb2017_resized.train.list'
        training_images = '/media/win/_/IJCB2017/training_resized'

        input_validation_listing = '/media/win/_/IJCB2017/protocol/validation.csv'
        output_validation_listing ='/media/win/_/IJCB2017/ijcb2017.valid.list'
        validation_images = '/media/win/_/IJCB2017/validation'

        img_height = 384.0
        img_width = 576.0

    if use_resized_dataset:
        script_info("Using resized dataset")
    else:
        script_info("Using original dataset")

    if use_original_classes:
        script_info("Using original classification")
    else:
        script_info("Using binary classification")

    train_filenames, subject_id, x, y, width, height = \
        ijcb2017_to_darknet(input_training_listing, use_original_classes)
        
    if do_create_darknet_list_for_training:
        create_darknet_list(output_training_listing, \
                             training_images, \
                             train_filenames)
        script_info("Created darknet list for training")

    if do_create_darknet_annotations_for_training:
        create_darknet_annotations(train_filenames, training_images, subject_id, \
                                   x, y, width, height)
        script_info("Created darknet annotations for training")

    v_filenames, v_subject_id, v_x, v_y, v_width, v_height = \
        ijcb2017_to_darknet(input_validation_listing, use_original_classes)

    if do_create_darknet_list_for_validation:
        create_darknet_list(output_validation_listing, \
                             validation_images, \
                             v_filenames)
        script_info("Created darknet list for validation")

    if do_create_darknet_annotations_for_validation:
        create_darknet_annotations(v_filenames, validation_images, v_subject_id, \
                                   v_x, v_y, v_width, v_height)
        script_info("Created darknet annotations for validation")

    if do_create_labels_file:
        create_labels_file(labels_file, use_original_classes, subject_id)
        script_info("Created labels file")

    if do_create_names_file:
        create_names_file(names_file, use_original_classes, subject_id)
        script_info("Created names file")

    if do_create_configuration_file:
        create_darknet_data_configuration_file(config_file)
        script_info("Created configuration file")
