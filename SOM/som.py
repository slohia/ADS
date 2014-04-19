from __future__ import division
from random import *
from math import *
import sys
import scipy
from scipy.spatial.distance import cityblock

class SOM:

    def __init__(self, max_train_values, name="som", height=10, width=10, fv_size=10, learning_rate=0.005, seed=255):
        self.name = name
        self.height = height
        self.width = width
        self.fv_size = fv_size
        self.radius = (height + width)*2
        self.learning_rate = learning_rate
        self.max_train_values = max_train_values
        self.threshold = 0
        self.nodes = scipy.array([[[random()*seed for i in range(fv_size)] for x in range(width)] for y in range(height)])

    # train_vector: [ fv0, fv1, fv2, ...] -> [ [...], [...], [...], ...]
    # train vector may be a list, will be converted to a list of scipy arrays
    def train(self, train_vector, iterations=1000):
        self.save_image(0)
        for t in range(len(train_vector)):
            train_vector[t] = scipy.array(train_vector[t])
        time_constant = iterations/log(self.radius)
        delta_nodes = scipy.array([[[0 for i in range(self.fv_size)] for x in range(self.width)] for y in range(self.height)])

        for i in range(1, iterations+1):
            delta_nodes.fill(0)
            radius_decaying = self.radius * exp(-1.0 * i / time_constant)
            rad_div_val = 2 * radius_decaying * i
            learning_rate_decaying = self.learning_rate * exp(-1.0 * i / time_constant)
            sys.stdout.write("\rTraining Iteration: " + str(i) + "/" + str(iterations))

            for j in range(len(train_vector)):
                best = self.best_match(train_vector[j])
                if i == iterations:
                    min_y = max(int(best[0] - 1), 0)
                    max_y = min(int(best[0] + 1), self.height - 1)
                    min_x = max(int(best[1] - 1), 0)
                    max_x = min(int(best[1] + 1), self.width - 1)

                    distance = cityblock(self.nodes[best[0], best[1]], self.nodes[max_y, best[1]])
                    distance += cityblock(self.nodes[best[0], best[1]], self.nodes[min_y, best[1]])
                    distance += cityblock(self.nodes[best[0], best[1]], self.nodes[best[0], min_x])
                    distance += cityblock(self.nodes[best[0], best[1]], self.nodes[best[0], max_x])
                    if self.threshold < distance:
                        self.threshold = distance

                #self.save_predict_image(best, i, j)
                for loc in self.find_neighborhood(best, radius_decaying):
                    influence = exp((-1.0 * (loc[2]**2)) / rad_div_val)
                    inf_lrd = influence*learning_rate_decaying

                    delta_nodes[loc[0], loc[1]] += inf_lrd*(train_vector[j] - self.nodes[loc[0], loc[1]])
            self.nodes += delta_nodes
            self.save_image(i)
        #self.threshold /= len(train_vector)
        sys.stdout.write("\n")

    def predict(self, feature_vector):
        data_point = feature_vector[:]
        for i in range(self.fv_size):
            data_point[i] = int(data_point[i] * 100.0 / self.max_train_values[i])

        best = self.best_match(data_point)
        min_y = max(int(best[0] - 1), 0)
        max_y = min(int(best[0] + 1), self.height - 1)
        min_x = max(int(best[1] - 1), 0)
        max_x = min(int(best[1] + 1), self.width - 1)

        distance = cityblock(self.nodes[best[0], best[1]], self.nodes[max_y, best[1]])
        distance += cityblock(self.nodes[best[0], best[1]], self.nodes[min_y, best[1]])
        distance += cityblock(self.nodes[best[0], best[1]], self.nodes[best[0], min_x])
        distance += cityblock(self.nodes[best[0], best[1]], self.nodes[best[0], max_x])
        if distance > self.threshold + 0.1:
            self.save_predict_image(best, "predict", "anomaly")
            print self.threshold, distance, best, "Anomaly"
        else:
            self.save_predict_image(best, "predict", "normal")
            print self.threshold, distance, best, "Normal"

    # Returns a list of points which live within 'dist' of 'pt'
    # Uses the Chessboard distance
    # pt is (row, column)
    def find_neighborhood(self, pt, dist):
        min_y = max(int(pt[0] - dist), 0)
        max_y = min(int(pt[0] + dist), self.height)
        min_x = max(int(pt[1] - dist), 0)
        max_x = min(int(pt[1] + dist), self.width)
        neighbors = []
        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                dist = abs(y - pt[0]) + abs(x - pt[1])
                neighbors.append((y, x, dist))
        return neighbors

    # Returns location of best match, uses Euclidean distance
    # target_fv is a scipy array
    def best_match(self, target_fv):
        loc = scipy.argmin((((self.nodes - target_fv)**2).sum(axis=2))**0.5)
        r = 0
        while loc >= self.width:
            loc -= self.width
            r += 1
        c = loc
        return (r, c)

    # returns the Euclidean distance between two Feature Vectors
    # FV_1, FV_2 are scipy arrays
    def fv_distance(self, fv_1, fv_2):
        return (sum((fv_1 - fv_2)**2))**0.5

    def save_image(self, image_number):
        try:
            from PIL import Image
            print " Saving Image: " + self.name + "_" + str(image_number) + ".png..."
            img = Image.new("RGB", (width, height))
            for r in range(height):
                for c in range(width):
                    if self.fv_size != 3:
                        sum = 0
                        for i in range(self.fv_size):
                            sum += self.nodes[r, c, i]
                            #print sum
                        val = int(sum/self.fv_size)
                        img.putpixel((r, c), (val, val, val))
                    else:
                        img.putpixel((r, c), (int(self.nodes[r, c, 0]), int(self.nodes[r, c, 1]), int(self.nodes[r, c, 2])))
            img = img.resize((width*10, height*10), Image.NEAREST)
            img.save(self.name + "_" + str(image_number) + ".png")
        except Exception, e:
            print str(e)

    def save_predict_image(self, best, iteration, image_number):
        try:
            from PIL import Image
            #print " Saving Image: " + self.name + "_predict_" + str(iteration) + "_" + str(image_number) + ".png..."
            img = Image.new("RGB", (width, height))
            for r in range(height):
                for c in range(width):
                    if (c, r) == best:
                        img.putpixel(best, (0, 255, 0))
                    elif self.fv_size != 3:
                        sum = 0
                        for i in range(self.fv_size):
                            sum += self.nodes[r, c, i]
                            #print sum
                        val = int(sum/self.fv_size)
                        img.putpixel((c, r), (val, val, val))
                    else:
                        img.putpixel((c, r), (int(self.nodes[r, c, 0]), int(self.nodes[r, c, 1]), int(self.nodes[r, c, 2])))
            img = img.resize((width*10, height*10), Image.NEAREST)
            img.save("CPU/" + self.name + "_predict_" + str(iteration) + "_" + str(image_number) + ".png")
        except Exception, e:
            print str(e)


if __name__ == "__main__":
    # print "Demo 1:"
    # colors = [ [0, 0, 0], [0, 0, 255], [0, 255, 0], [0, 255, 255], [255, 0, 0], [255, 0, 255], [255, 255, 0], [255, 255, 255]]
    # width = 32
    # height = 32
    # color_som = SOM("colors", width, height, 3, 0.5)
    # print "Training colors..."
    # color_som.train(colors, 100)
    # color_som.save_image(101)
    train_file = 'train.txt'
    train_data = []
    with open(train_file, 'r') as train:
        for line in train:
            sample = line.rstrip().split(',')
            train_data.append(sample)
    train_data = [map(int, x) for x in train_data]

    test_data = []
    for i in range(len(train_data)):
        test_data.append(train_data[i][:])

    max_train_values = [0] * len(train_data[0])
    for i in range(len(train_data)):
        for j in range(len(train_data[i])):
                if train_data[i][j] > max_train_values[j]:
                    max_train_values[j] = train_data[i][j]
    print max_train_values

    # data whitening
    for i in range(len(train_data)):
        for j in range(len(train_data[i])):
            train_data[i][j] = int(train_data[i][j] * 100.0 / max_train_values[j])


    width = 32
    height = 32
    obs_som = SOM(max_train_values, "cpu_som", width, height, 4, 0.05, 100)
    print "Training on observed data"
    obs_som.train(train_data, 50)

    for i in range(len(test_data)):
        obs_som.predict(test_data[i])

    obs_som.predict([29522, 86902, 4302, 226230])
    obs_som.predict([29582, 86902, 4302, 226230])
    obs_som.predict([29522, 86982, 4302, 226230])
    obs_som.predict([29522, 86902, 4382, 226230])
    obs_som.predict([29522, 86902, 4302, 226830])
    obs_som.predict([29522, 86902, 4302, 26830])
    obs_som.predict([59522, 106902, 8302, 226830])
    obs_som.predict([29522, 86902, 4302, 326230])
    obs_som.predict([29522, 86902, 6302, 226230])
    obs_som.predict([2, 6902, 2, 6830])
    #obs_som.save_image(21)
