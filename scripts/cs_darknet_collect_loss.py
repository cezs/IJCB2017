from matplotlib import pyplot
import re

avg_loss = []

with open('nohup.out') as log:
    for line in log:
        if "avg" in line:
            fields = line.strip().split()
            matched = re.search(r'\d+\.\d+(?= avg)', line)
            if matched:
                avg_loss.append(float(matched.group(0)))
            # avg_loss.append(fields[2])
            # print fields

# print '{}\n'.format(avg_loss[0])
    
pyplot.plot(avg_loss)
pyplot.show()
