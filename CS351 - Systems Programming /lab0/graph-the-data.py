#!/usr/bin/env python3
from matplotlib import pyplot as plt

x_coordinates = [1000, 100000, 10000000]
gy_coordinates = [0.015, 0.296, 30.379]
sy_coordinates = [0.005, 0.240, 29.282]

#make a graph for generate-dataset.sh
plt.plot(x_coordinates, gy_coordinates, Label="generate-dataset.sh")

#make a graph for sort-data.sh
plt.plot(x_coordinates, sy_coordinates, Label="sort-data.sh")

plt.xlabel("Record Number (Line Number)")
plt.ylabel("Time Taken to Execute (s)")
plt.legend()
plt.title("Record Number vs Time Taken (S)")
plt.savefig("recnum-vs-time-graph.png")
plt.close()
