current_dir=$(pwd)

darknet="/home/cs/Documents/packages/darknet_fork"
configuration="/media/win/_/IJCB2017/cfg/my-yolo-voc-2-416.cfg"
weights="/home/cs/Documents/packages/darknet_fork/backup/my-yolo-voc-2-416_11000.weights"
images="/media/win/_/IJCB2017/training_resized"

cd $darknet

for filename in $images/*.jpg; do
	$darknet/darknet detect $configuration $weights $filename -thresh 0.01
done

cd $curent_dir

