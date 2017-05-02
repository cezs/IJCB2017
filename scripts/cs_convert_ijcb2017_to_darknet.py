#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import csv

class colours:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WARNING = '\033[93m'

def script_info(msg):
    print(colours.BOLD + "[INFO] " + str(msg) + colours.ENDC)

def script_check(msg):
    print colours.PURPLE + "[CHECK] " + str(msg) + colours.ENDC

def script_pass(msg):
    print colours.GREEN + "[PASS] " + str(msg) + colours.ENDC

def script_fail(msg):
    print colours.RED + "[FAIL] " + str(msg) + colours.ENDC

def ijcb2017_to_darknet(ijcb2017_annotations, use_original_classes, img_width, img_height):
    """
    Covert to darknet format and store in python lists.
    Returns bboxes with classes and corresponding images filenames.
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
            if (use_original_classes):
                # use original class
                # TODO: map original subject_id to label
                # Do not include unknown identities
                # if int(row[2]) != -1:
                #     subject_id.append(int(row[2]))
                # else:
                #     continue
                # Including unknown identities
                subject_id.append(int(row[2]))
            else:
                # just detect
                subject_id.append(1)
            filenames.append(row[1])
            # recalculate starting position of bounding box to the center
            # of it instead of the supplied upper left corner and make
            # position as well as dimensions of this bounding box relative
            # to image dimensions
            x.append((float(row[3]) + float(row[5]) / 2.0) / img_width)
            y.append((float(row[4]) + float(row[6]) / 2.0) / img_height)
            width.append(float(row[5]) / img_width)
            height.append(float(row[6]) / img_height)
    return filenames, subject_id, x, y, width, height


def create_darknet_list(output_list, prepended_directory, input_list):
    """Create list of paths to images"""
    # print converted listing of images
    with open(output_list, 'wb') as out_list:
        # note the use of set to from list from only unique filenames
        for f in set(input_list):
            out_list.write("{}/{}\n".format(prepended_directory, f))

def create_darknet_annotations(output_directory, input_list,\
                               subject_id, x, y, width, height):
    """
    Create individual annotations. Store each individual bbox's id, 
    x, y, width and height in file with name corresponding to 
    the image's name.
    """
    individual_filenames = []

    for f in input_list:
        # take image's file name and change extension to .txt
        individual_filenames.append(f.rsplit(".", 1)[0] + '.txt')

    for i in range(len(subject_id)):
        # generate annotation
        # note: each annotation might be opened and written to, 
        # more than once, thus we set it to appending mode.
        with open("{}/{}".format(output_directory,\
                                 individual_filenames[i]), 'a') as newfile:
            newfile.write("{} {} {} {} {}\n".format(subject_id[i],\
                                                    x[i],\
                                                    y[i],\
                                                    width[i],\
                                                    height[i]))

def create_labels_file(labels_file, use_original_classes, subject_id):
    """Create labels file."""
    with open(labels_file, 'wb') as labels:
        if (use_original_classes):
            # use original classification
            for i in range(len(sorted(set(subject_id)))):
                labels.write("{}\n".format(i))
        else:
            # use binary classification
            labels.write("{}\n".format(0))
            labels.write("{}\n".format(1))

def create_names_file(names_file, use_original_classes, subject_id):
    """Create names file."""
    with open(names_file, 'wb') as names:
            if (use_original_classes):
                # use original classification
                for i in sorted(set(subject_id)):
                    names.write("{}\n".format(i))
            else:
                # use binary classification
                names.write("{}\n".format("nothing"))
                names.write("{}\n".format("identity"))

def create_darknet_data_configuration_file(data_config_file,\
                                           use_original_classes,\
                                           subject_id,\
                                           output_training_listing,\
                                           output_validation_listing,\
                                           labels_file,\
                                           names_file,\
                                           backup_dir,
                                           valid_dir):
    """Create configuration file."""
    with open(data_config_file, 'wb') as cfg_file:
        if (use_original_classes):
            # use original classification
            cfg_file.write("{} = {}\n".format("classess", len(set(subject_id))))
        else:
            # use binary classification
            cfg_file.write("{} = {}\n".format("classess", 2))
            # # use unary classification
            # cfg_file.write("{} = {}\n".format("classess", 1))
        cfg_file.write("{} = {}\n".format("train", output_training_listing))
        cfg_file.write("{} = {}\n".format("valid", output_validation_listing))
        cfg_file.write("{} = {}\n".format("labels", labels_file))
        cfg_file.write("{} = {}\n".format("names", names_file))
        cfg_file.write("{} = {}\n".format("backup", backup_dir))
        cfg_file.write("{} = {}\n".format("results", valid_dir))
        
def create_darknet_data_configuration_file_short(cfg, paths, subject_id):
    return create_darknet_data_configuration_file(paths.data_config_file,\
                                                  cfg.use_original_classes,\
                                                  subject_id,\
                                                  paths.output_training_listing,\
                                                  paths.output_validation_listing,\
                                                  paths.labels_file,\
                                                  paths.names_file,\
                                                  paths.backup_dir,\
                                                  paths.valid_dir)

class Paths(dict):
    """Store paths."""
    def __init__(self, **kwargs):
        super(Paths, self).__init__(**kwargs)
        self.__dict__ = self

class Config(dict):
    """Store boolean values"""
    def __init__(self, **kwargs):
        super(Config, self).__init__(**kwargs)
        self.__dict__ = self

def run(cfg, paths):
    "Run program"
    if cfg.use_resized_dataset:
        script_check("Using resized dataset")
    else:
        script_check("Using original dataset")

    if cfg.use_original_classes:
        script_check("Using original classification")
    else:
        script_check("Using detection / unary classification")

    train_filenames, subject_id, x, y, width, height = \
        ijcb2017_to_darknet(paths.input_training_listing,\
                            cfg.use_original_classes,\
                            paths.img_width,\
                            paths.img_height)
        
    if cfg.do_create_darknet_list_for_training:
        create_darknet_list(paths.output_training_listing,\
                            paths.training_images,\
                            train_filenames)
        script_pass("Created darknet list for training")

    if cfg.do_create_darknet_annotations_for_training:
        create_darknet_annotations(paths.training_images,\
                                   train_filenames,\
                                   subject_id,\
                                   x, y, width, height)
        script_pass("Created darknet annotations for training")

    v_filenames, v_subject_id, v_x, v_y, v_width, v_height = \
        ijcb2017_to_darknet(paths.input_validation_listing,\
                            cfg.use_original_classes,\
                            paths.img_width, paths.img_height)

    if cfg.do_create_darknet_list_for_validation:
        create_darknet_list(paths.output_validation_listing,\
                             paths.validation_images,\
                             v_filenames)
        script_pass("Created darknet list for validation")

    if cfg.do_create_darknet_annotations_for_validation:
        create_darknet_annotations(paths.validation_images,\
                                   v_filenames,\
                                   v_subject_id,\
                                   v_x, v_y, v_width, v_height)
        script_pass("Created darknet annotations for validation")

    if cfg.do_create_labels_file:
        create_labels_file(paths.labels_file,\
                           cfg.use_original_classes,\
                           subject_id)
        script_pass("Created labels file")

    if cfg.do_create_names_file:
        create_names_file(paths.names_file,\
                          cfg.use_original_classes,\
                          subject_id)
        script_pass("Created names file")

    if cfg.do_create_configuration_file:
        create_darknet_data_configuration_file(paths.data_config_file,\
                                               cfg.use_original_classes,\
                                               subject_id,\
                                               paths.output_training_listing,\
                                               paths.output_validation_listing,\
                                               paths.labels_file,\
                                               paths.names_file,\
                                               paths.backup_dir,
                                               paths.valid_dir)
        script_pass("Created configuration file")


def getArgs():
    parser = argparse.ArgumentParser(
        description="Unconstrained Face Detection and Open Set Recognition" \
        "Challenge in Darknet")
    parser.add_argument('-a', '--resized_dataset', dest='a', action='store_true',
                        help='Use resized dataset')
    parser.add_argument('-b', '--original_classes', dest='b', action='store_true',
                        help='Use original classes')
    parser.add_argument('-c', '--training_list', dest='c', action='store_true',
                        help='Create Darknet list for training')
    parser.add_argument('-d', '--training_annotations', dest='d', action='store_true',
                        help='Create Darknet annotations for training')
    parser.add_argument('-e', '--validation_list', dest='e', action='store_true',
                        help='Create Darknet list for validation')
    parser.add_argument('-f', '--validation_annotations', dest='f', action='store_true',
                        help='Create Darknet annotations for validation')
    parser.add_argument('-g', '--labels_file', dest='g', action='store_true',
                        help='Create labels file')
    parser.add_argument('-i', '--names_file', dest='i', action='store_true',
                        help='Create names file')
    parser.add_argument('-j', '--data_cfg_file', dest='j', action='store_true',
                        help='Create data configuration file')
    args = parser.parse_args()

    script_info("Entered main function")

    # if args empty
    if not len(sys.argv) > 1:
        # cfg = Config(True, False, True, True, True, True, True, True, True)
        cfg = Config(use_resized_dataset = True,\
                     use_original_classes = False,\
                     do_create_darknet_list_for_training = True,\
                     do_create_darknet_annotations_for_training = True,\
                     do_create_darknet_list_for_validation = True,\
                     do_create_darknet_annotations_for_validation = True,\
                     do_create_labels_file = True,\
                     do_create_names_file = True,\
                     do_create_configuration_file = True)
    else:
        cfg = Config(use_resized_dataset = args.a,\
                     use_original_classes = args.b,\
                     do_create_darknet_list_for_training = args.c,\
                     do_create_darknet_annotations_for_training = args.d,\
                     do_create_darknet_list_for_validation = args.e,\
                     do_create_darknet_annotations_for_validation = args.f,\
                     do_create_labels_file = args.g,\
                     do_create_names_file = args.i,\
                     do_create_configuration_file = args.j)
    
    paths = Paths(data_config_file = '/media/win/_/IJCB2017/cfg/ijcb2017.data',\
                  labels_file = '/media/win/_/IJCB2017/data/ijcb2017.labels',\
                  names_file = '/media/win/_/IJCB2017/data/ijcb2017.names',\
                  backup_dir =  '/media/win/_/IJCB2017/weights',\
                  valid_dir = '/media/win/_/IJCB2017/valid',\
                  # map = ...
                  # eval = ...
                  # top= ...

                  input_training_listing = '/media/win/_/IJCB2017/protocol/training_modified.csv',\
                  output_training_listing ='/media/win/_/IJCB2017/protocol/ijcb2017.train.list',\
                  training_images = '/media/win/_/IJCB2017/training',\

                  input_validation_listing = '/media/win/_/IJCB2017/protocol/validation.csv',\
                  output_validation_listing ='/media/win/_/IJCB2017/protocol/ijcb2017.valid.list',\
                  validation_images = '/media/win/_/IJCB2017/validation',\

                  # TODO: Use library to get dimensions and remove from here
                  img_height = 3456.0,\
                  img_width = 5184.0)

    # Overwrite `paths` upon receiving particular option
    if cfg.use_resized_dataset:
        paths.input_training_listing = '/media/win/_/IJCB2017/protocol/training_resized.csv'
        paths.training_images = '/media/win/_/IJCB2017/training_resized'
        # TODO: Use library to get dimensions and remove from here
        paths.img_height = 384.0
        paths.img_width = 576.0

    return cfg, paths

class Infodata:
    def __init__(self, paths, cfg):
        # self.filename, self.subject_id, self.x, self.y, self.width, self.height = \
        #     ijcb2017_to_darknet(paths.input_validation_listing,\
        #                         cfg.use_original_classes,\
        #                         paths.img_width, paths.img_height)
        filename, subject_id, x, y, width, height = \
            ijcb2017_to_darknet(paths.input_validation_listing,\
                                cfg.use_original_classes,\
                                paths.img_width, paths.img_height)
        self.filename = filename
        self.subject_id = subject_id
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def printer(self):
        print '{}\n{}\n{}\n{}\n{}\n{}'.format(self.filename, self.subject_id,\
                                         self.x, self.y, self.width, self.height)

def short_create_darknet_list_for_training(paths, infodata):
    return create_darknet_list(paths.output_training_listing,\
                         paths.training_images,\
                         infodata.filename)

def short_create_darknet_annotations_for_training(paths, infodata):
    return create_darknet_annotations(paths.training_images,\
                                      infodata.filename,\
                                      infodata.subject_id,\
                                      infodata.x, infodata.y,\
                                      infodata.width, infodata.height)

def short_create_darknet_list_for_validation(paths, infodata):
    return create_darknet_list(paths.output_validation_listing,\
                         paths.validation_images,\
                         infodata.filename)

def short_create_darknet_annotations_for_validation(paths, infodata):
    return create_darknet_annotations(paths.validation_images,\
                                      infodata.filename,\
                                      infodata.subject_id,\
                                      infodata.x, infodata.y, infodata.width, infodata.height)

def short_create_labels_file(paths, cfg, infodata):
    return create_labels_file(paths.labels_file,\
                       cfg.use_original_classes,\
                       infodata.subject_id)

def short_create_names_file(paths, cfg, infodata):
    return create_names_file(paths.names_file,\
                      cfg.use_original_classes,\
                      infodata.subject_id)

def short_create_configuration_file(paths, cfg, infodata):
    return create_darknet_data_configuration_file(paths.data_config_file,\
                                                  cfg.use_original_classes,\
                                                  infodata.subject_id,\
                                                  paths.output_training_listing,\
                                                  paths.output_validation_listing,\
                                                  paths.labels_file,\
                                                  paths.names_file,\
                                                  paths.backup_dir,\
                                                  paths.valid_dir)

if __name__ == "__main__":
    
    cfg, paths = getArgs()

    run(cfg, paths)

# if __name__ == "__main__":
    
#     cfg, paths = getArgs()

#     infodata = Infodata(paths, cfg)
#     infodata.printer()
