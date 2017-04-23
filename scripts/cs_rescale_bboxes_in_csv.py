import os
import csv

factor = 1.0/9.0

face_id = []
filename = []
subject_id= []
x = []
y = []
width = []
height = []

first_row = []

training_input_file = '/media/win/_/IJCB2017/protocol/training_updated.csv'
training_output_file = '/media/win/_/IJCB2017/protocol/training_resized.csv'

with open(training_input_file, 'rb') as in_file:
    reader = csv.reader(in_file)
    first_row = next(reader)
    for row in reader:
        face_id.append(row[0])
        filename.append(row[1])
        subject_id.append(row[2])
        x.append(float(row[3]) * factor)
        y.append(float(row[4]) * factor)
        width.append(float(row[5]) * factor)
        height.append(float(row[6]) * factor)

with open(training_output_file, 'wb') as out_file:
    writer = csv.writer(out_file, delimiter=',')
    writer.writerow(first_row)
    for i in range(len(face_id)):
        writer.writerow([face_id[i],    \
                         filename[i],   \
                         subject_id[i], \
                         x[i],          \
                         y[i],          \
                         width[i],      \
                         height[i]])
