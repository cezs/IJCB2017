import os
import csv

use_resized_dataset = True
use_original_classes = False

if not use_resized_dataset:
    input_training_listing = '/media/win/_/IJCB2017/protocol/training_updated.csv'
    output_training_listing ='/media/win/_/IJCB2017/ijcb2017_training_updated.txt'
    training_images = '/media/win/_/IJCB2017/training'

    input_validation_listing = '/media/win/_/IJCB2017/protocol/validation.csv'
    output_validation_listing ='/media/win/_/IJCB2017/ijcb2017_validation.txt'
    validation_images = '/media/win/_/IJCB2017/validation'

    img_height = 5184.0
    img_width = 3456.0
else:
    input_training_listing = '/media/win/_/IJCB2017/protocol/training_resized.csv'
    output_training_listing ='/media/win/_/IJCB2017/ijcb2017_training_resized.txt'
    training_images = '/media/win/_/IJCB2017/training_resized'

    input_validation_listing = '/media/win/_/IJCB2017/protocol/validation.csv'
    output_validation_listing ='/media/win/_/IJCB2017/ijcb2017_validation.txt'
    validation_images = '/media/win/_/IJCB2017/validation'

    img_height = 576.0
    img_width = 384.0

#######################
# train files listing #
#######################

train_filenames = []
subject_id= []
x = []
y = []
width = []
height = []

# append each image filename for training to list 
with open(input_training_listing, 'rb') as in_train_listing:
    reader = csv.reader(in_train_listing)
    next(reader)
    for row in reader:
        train_filenames.append(row[1])
        if (use_original_classes):
            # use original class
            subject_id.append(row[2])
        else:
            # use binary classification
            if (row[2] >= 0):
                subject_id.append(1)
            else:
                subject_id.append(0)
        # recalculate starting position of bounding box to the center
        # of it instead of the supplied upper left corner and make
        # position as well as dimensions of this bounding box relative
        # to image dimensions
        x.append( (float(row[3]) + float(row[5]) / 2.0) / img_width)
        y.append( (float(row[4]) + float(row[6]) / 2.0) / img_height)
        width.append(float(row[5]) / img_width)
        height.append(float(row[6]) / img_height)


# print converted listing of images for training 
with open(output_training_listing, 'wb') as out_train_listing:
    for f in set(train_filenames):
        out_train_listing.write("{}/{}\n".format(training_images, f))

#############################
# individual training files #
#############################

# make list of filenames for files which are going to store individual
# id, x, y, width and height
individual_filenames = []

for f in train_filenames:
    individual_filenames.append(f.rsplit(".", 1)[0] + '.txt')
    
for i in range(len(x)):
    with open("{}/{}".format(training_images, individual_filenames[i]), 'w') as newfile:
        newfile.write("{} {} {} {} {}\n".format(subject_id[i], \
                                                x[i], \
                                                y[i], \
                                                width[i], \
                                                height[i]))

##########################
# all classes names file #
##########################

classes_file = '/media/win/_/IJCB2017/ijcb2017.names'

with open(classes_file, 'wb') as classes:
        if (use_original_classes):
            # use original classification
            for i in set(subject_id):
                classes.write("{}\n".format(i))
        else:
            # use binary classification
            classes.write("{}\n".format(0))
            classes.write("{}\n".format(1))

############################
# validation files listing #
############################

v_filenames = []
v_subject_id= []
v_x = []
v_y = []
v_width = []
v_height = []

# append each image filename for validation to list 
with open(input_validation_listing, 'rb') as in_validation_listing:
    reader = csv.reader(in_validation_listing)
    next(reader)
    for row in reader:
        v_filenames.append(row[1])
        if (use_original_classes):
            # use original class
            v_subject_id.append(row[2])
        else:
            # use binary classification
            if (row[2] >= 0):
                v_subject_id.append(1)
            else:
                v_subject_id.append(0)
        # recalculate starting position of bounding box to the center
        # of it instead of the supplied upper left corner and make
        # position as well as dimensions of this bounding box relative
        # to image dimensions
        v_x.append( (float(row[3]) + float(row[5]) / 2.0) / img_width)
        v_y.append( (float(row[4]) + float(row[6]) / 2.0) / img_height)
        v_width.append(float(row[5]) / img_width)
        v_height.append(float(row[6]) / img_height)


# print converted listing of images for training 
with open(output_validation_listing, 'wb') as out_validation_listing:
    for f in set(v_filenames):
        out_validation_listing.write("{}/{}\n".format(validation_images, f))

###############################
# individual validation files #
###############################

# make list of filenames for files which are going to store individual
# id, x, y, width and height
v_individual_filenames = []

for f in v_filenames:
    v_individual_filenames.append(f.rsplit(".", 1)[0] + '.txt')
    
for i in range(len(v_x)):
    with open("{}/{}".format(validation_images, v_individual_filenames[i]), 'w') as newfile:
        newfile.write("{} {} {} {} {}\n".format(v_subject_id[i], \
                                                v_x[i], \
                                                v_y[i], \
                                                v_width[i], \
                                                v_height[i]))

######################
# configuration file #
######################

config_file = '/media/win/_/IJCB2017/ijcb2017.data'

with open(config_file, 'wb') as cfg_file:
    if (use_original_classes):
        # use original classification
        cfg_file.write("{} = {}\n".format("classess",len(set(subject_id))))
    else:
        # use binary classification
        cfg_file.write("{} = {}\n".format("classess", 2))
    cfg_file.write("{} = {}\n".format("train", output_training_listing))
    cfg_file.write("{} = {}\n".format("valid", output_validation_listing))
    # cfg_file.write("{} = {}\n".format("valid", output_test_listing)) 
    cfg_file.write("{} = {}\n".format("names", classes_file))
    cfg_file.write("{} = {}\n".format("backup","backup"))


# NOTE: Test dataset has yet to be released on 04/17/2017

# input_test_listing = '/media/win/_/IJCB2017/protocol/test.csv'
# output_test_listing = '/media/win/_/IJCB2017/ijcb2017_test.txt'

# ######################
# # test files listing #
# ######################

# # store filenames of images for testing in list
# test_filenames = []

# # append each image filename for testing to list 
# with open(input_test_listing, 'rb') as in_test_listing:
#     reader = csv.reader(in_test_listing)
#     next(reader)
#     for row in reader:
#         test_filenames.append(row[0])

# # print converted listing of images for testing 
# with open(output_test_listing, 'wb') as out_test_listing:
#     for f in set(test_filenames):
#         out_test_listing.write("{}/{}\n".format(training_images, f))
