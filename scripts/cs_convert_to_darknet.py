import os
import csv

use_resized_dataset = True
use_original_classes = False

if not use_resized_dataset:
    input_training_listing = '/media/win/_/IJCB2017/protocol/training_updated.csv'
    output_training_listing ='/media/win/_/IJCB2017/ijcb2017_updated.list'
    training_images = '/media/win/_/IJCB2017/training'

    input_validation_listing = '/media/win/_/IJCB2017/protocol/validation.csv'
    output_validation_listing ='/media/win/_/IJCB2017/ijcb2017.valid'
    validation_images = '/media/win/_/IJCB2017/validation'

    img_height = 3456.0
    img_width = 5184.0
else:
    input_training_listing = '/media/win/_/IJCB2017/protocol/training_resized.csv'
    output_training_listing ='/media/win/_/IJCB2017/ijcb2017_resized.list'
    training_images = '/media/win/_/IJCB2017/training_resized'

    input_validation_listing = '/media/win/_/IJCB2017/protocol/validation.csv'
    output_validation_listing ='/media/win/_/IJCB2017/ijcb2017.valid'
    validation_images = '/media/win/_/IJCB2017/validation'

    img_height = 384.0
    img_width = 576.0

######################################################
# covert to darknet format and store in python lists #
######################################################

train_filenames = []
subject_id= []
x = []
y = []
width = []
height = []

# append each image filename for training to list 
with open(input_training_listing, 'r') as in_train_listing:
    reader = csv.reader(in_train_listing)
    next(reader)
    for row in reader:
        train_filenames.append(row[1])
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


classes = []
labels = range(len(classes))
# append each image filename for training to list 
with open(input_training_listing, 'r') as in_train_listing:
    reader = csv.reader(in_train_listing)
    next(reader)
    for row in reader:
        classes.append(int(row[2]) + 1)
print(len(set(classes)))

#################
# training list #
#################

# print converted listing of images for training 
with open(output_training_listing, 'w') as out_train_listing:
    # note the use of set to from list from only unique filenames
    for f in set(train_filenames):
        out_train_listing.write("{}/{}\n".format(training_images, f))

###################################
# individual training annotations #
###################################

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

###############
# labels file #
###############

labels_file = '/media/win/_/IJCB2017/ijcb2017.labels'

with open(labels_file, 'wb') as labels:
        if (use_original_classes):
            # use original classification
            for i in range(len(set(subject_id))):
                labels.write("{}\n".format(i))
        else:
            # use binary classification
            labels.write("{}\n".format(0))
            labels.write("{}\n".format(1))

##############
# names file #
##############

names_file = '/media/win/_/IJCB2017/ijcb2017.names'

with open(names_file, 'wb') as names:
        if (use_original_classes):
            # use original classification
            for i in set(subject_id):
                names.write("{}\n".format(i))
        else:
            # use binary classification
            names.write("{}\n".format("nothing"))
            names.write("{}\n".format("face"))

##########################
# validation images list #
##########################

v_filenames = []
v_subject_id= []
v_x = []
v_y = []
v_width = []
v_height = []

# append each image filename for validation to list 
with open(input_validation_listing, 'r') as in_validation_listing:
    reader = csv.reader(in_validation_listing)
    next(reader)
    for row in reader:
        v_filenames.append(row[1])
        if (use_original_classes):
            # use original class
            v_subject_id.append(row[2])
        else:
            # just detect
            v_subject_id.append(1)
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

#####################################
# individual validation annotations #
#####################################

# make list of filenames for files which are going to store individual
# id, x, y, width and height
v_individual_filenames = []

for f in v_filenames:
    v_individual_filenames.append(f.rsplit(".", 1)[0] + '.txt')
    
for i in range(len(v_x)):
    with open("{}/{}".format(validation_images, v_individual_filenames[i]), 'a') as newfile:
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
    cfg_file.write("{} = {}\n".format("valid", output_training_listing))
    cfg_file.write("{} = {}\n".format("labels", labels_file))
    cfg_file.write("{} = {}\n".format("names", names_file))
    cfg_file.write("{} = {}\n".format("backup","backup"))

# ######################
# # test files listing #
# ######################

# NOTE: Test dataset has yet to be released on 04/17/2017

# input_test_listing = '/media/win/_/IJCB2017/protocol/test.csv'
# output_test_listing = '/media/win/_/IJCB2017/ijcb2017_test.txt'

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
