rm /home/cs/_/IJCB2017/ijcb2017*
rm /home/cs/_/IJCB2017/training/*.txt
rm /home/cs/_/IJCB2017/training_resized/*.txt
rm /home/cs/_/IJCB2017/training_resized/*.txt
python /home/cs/_/IJCB2017/scripts/cs_resize.py
python /home/cs/_/IJCB2017/scripts/cs_convert_to_darknet.py
