import matplotlib.pyplot as plt
plt.style.use('ggplot')

# 22
filepath='/home/cs/remote/titanx/media/win/_/IJCB2017/recall/ijcb2017-yolo-voc.recall'[0:]

ijcb2017 = []
ijcb2017_rp_per_img = []
offset = 36

with open(filepath, 'rb') as recall:
    for i in range(offset):
        recall.next()
    for line in recall:
        fields = line.strip().split()
        rank = float(fields[0])
        correct = float(fields[1])
        total = float(fields[2])
        rp_per_image = float(fields[4])
        iou = float(fields[6].replace("%",""))
        recall = float(fields[7].replace("%","").replace("Recall:",""))
        ijcb2017.append([rank, correct, total, rp_per_image, iou, recall])
        # print '{} {} {} {} {} {}'.format(fields[0],\
        #                   fields[1],\
        #                   fields[2],\
        #                   fields[4],\
        #                   fields[6].replace("%",""),\
        #                   fields[7].replace("%","").replace("Recall:",""))

# results = len(ijcb2017)
fig, ax = plt.subplots(3,2)
for i in range(3):
    for j in range(2):
        ax[i, j].plot([row[j*3+i] for row in ijcb2017])
        ax[i, j].grid()
plt.show()

