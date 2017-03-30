# remove generated files
rm /home/cs/_/IJCB2017/ijcb2017*
rm /home/cs/_/IJCB2017/training/*.txt
rm /home/cs/_/IJCB2017/training_resized/*.txt
rm /home/cs/_/IJCB2017/validation/*.txt

# update csv file
python /home/cs/_/IJCB2017/scripts/cs_resize.py

# generate files for multi-class classifications
python /home/cs/_/IJCB2017/scripts/cs_convert_ijcb2017_to_darknet.py -abcdefgij

# # generate files for binary classification
# python /home/cs/_/IJCB2017/scripts/cs_convert_ijcb2017_to_darknet.py -acdefgij
