import matplotlib.pyplot as plt
import random


def draw_rect(vehicle):
  colors = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple']
  fig = plt.figure()
  ax = fig.add_subplot(111)
  bin_list = vehicle.bin_list
  for bin in bin_list:
    point_list= bin.pointList
    start1=point_list[0].x
    end1=point_list[0].y
    width=point_list[1].x - point_list[0].x
    height=point_list[2].y - point_list[1].y
    color_index=random.randint(1,100)
    plt.gca().add_patch(plt.Rectangle((start1, end1), width, height,facecolor=colors[color_index%7]))
  plt.show()

colors = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple']
fig = plt.figure()
ax = fig.add_subplot(111)
plt.xlim(0, 4)
plt.ylim(0, 5)
color_index=random.randint(1,100)
plt.gca().add_patch(plt.Rectangle((0.1, 0.1), 1,2,facecolor=colors[color_index%7]))
plt.show()


