# remove generated files
rm ${HOME}/IJCB2017/protocol/ijcb2017*
rm ${HOME}/IJCB2017/training/*.txt
rm ${HOME}/IJCB2017/training_resized/*.txt
rm ${HOME}/IJCB2017/validation/*.txt

# update csv file
python ${HOME}/IJCB2017/scripts/cs_rescale_bboxes_in_csv.py

echo "Choose 1) for binary classifications/detection or 2) for multi-class classifications."
read num

case $num in
    # generate files for binary classifications / detection
    1) python ${HOME}/IJCB2017/scripts/cs_convert_ijcb2017_to_darknet.py -acdefgij ;;
    # generate files for multi-class classifications
    2) python ${HOME}/IJCB2017/scripts/cs_convert_ijcb2017_to_darknet.py -abcdefgij ;;
    *) echo "INVALID CHOICE!" ;;
esac
