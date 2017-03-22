current_dir=$(pwd)

darknet="/home/cs/Documents/packages/darknet_fork"
data_cfg="/media/win/_/IJCB2017/cfg/ijcb2017-yolo9000-uno.data"
network_cfg="/media/win/_/IJCB2017/cfg/ijcb2017-yolo9000-uno.cfg"
weights="/media/win/_/IJCB2017/weights/ijcb2017-yolo9000-uno_3000.weights"
images="/media/win/_/IJCB2017/training_resized"
bboxes="/media/win/_/IJCB2017/bboxes"

thresh=0.001

cd $darknet

mkdir $bboxes

for filename in $images/*.jpg; do
    $darknet/darknet detector test $data_cfg $network_cfg $weights $filename -thresh $thresh;
    image_with_detections=$(echo $(basename "$filename" ".jpg")_detections.png
    mv "predictions.png" $bboxes/$image_with_detections)
    echo "[  OK  ] Created $filename";
done

cd $curent_dir

