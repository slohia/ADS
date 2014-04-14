from __future__ import division
from random import *
from math import *
import sys
import scipy

class SOM:

    def __init__(self, name="som", height=10, width=10, FV_size=10, learning_rate=0.005, seed=255):
        self.name = name
        self.height = height
        self.width = width
        self.FV_size = FV_size
        self.radius = (height+width)/3
        self.learning_rate = learning_rate
        self.nodes = scipy.array([[[random()*seed for i in range(FV_size)] for x in range(width)] for y in range(height)])

    # train_vector: [ FV0, FV1, FV2, ...] -> [ [...], [...], [...], ...]
    # train vector may be a list, will be converted to a list of scipy arrays
    def train(self, train_vector=[[]], iterations=1000):
        self.save_image(0)
        for t in range(len(train_vector)):
            train_vector[t] = scipy.array(train_vector[t])
        time_constant = iterations/log(self.radius)
        delta_nodes = scipy.array([[[0 for i in range(self.FV_size)] for x in range(self.width)] for y in range(self.height)])

        for i in range(1, iterations+1):
            delta_nodes.fill(0)
            radius_decaying = self.radius*exp(-1.0*i/time_constant)
            rad_div_val = 2 * radius_decaying * i
            learning_rate_decaying = self.learning_rate * exp(-1.0 * i / time_constant)
            sys.stdout.write("\rTraining Iteration: " + str(i) + "/" + str(iterations))

            for j in range(len(train_vector)):
                best = self.best_match(train_vector[j])
                #self.save_predict_image(best, j)
                for loc in self.find_neighborhood(best, radius_decaying):
                    influence = exp((-1.0 * (loc[2]**2)) / rad_div_val)
                    inf_lrd = influence*learning_rate_decaying

                    delta_nodes[loc[0], loc[1]] += inf_lrd*(train_vector[j] - self.nodes[loc[0],loc[1]])
            self.nodes += delta_nodes
            self.save_image(i)
        sys.stdout.write("\n")

    def predict(self, feature_vector):
        best = self.best_match(feature_vector)
        return best

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
                dist = abs(y-pt[0]) + abs(x-pt[1])
                neighbors.append((y,x,dist))
        return neighbors

    # Returns location of best match, uses Euclidean distance
    # target_FV is a scipy array
    def best_match(self, target_FV):
        loc = scipy.argmin((((self.nodes - target_FV)**2).sum(axis=2))**0.5)
        r = 0
        while loc > self.width:
            loc -= self.width
            r += 1
        c = loc
        return (r, c)

    # returns the Euclidean distance between two Feature Vectors
    # FV_1, FV_2 are scipy arrays
    def FV_distance(self, FV_1, FV_2):
        return (sum((FV_1 - FV_2)**2))**0.5

    def save_image(self, image_number):
        try:
            from PIL import Image
            print " Saving Image: " + self.name + "_" + str(image_number) + ".png..."
            img = Image.new("RGB", (width, height))
            for r in range(height):
                for c in range(width):
                    if self.FV_size != 3:
                        sum = 0
                        for i in range(self.FV_size):
                            sum += self.nodes[r, c, i]
                            #print sum
                        val = int(sum/self.FV_size)
                        img.putpixel((c, r), (val, val, val))
                    else:
                        img.putpixel((c, r), (int(self.nodes[r, c, 0]), int(self.nodes[r, c, 1]), int(self.nodes[r, c, 2])))
            img = img.resize((width*10, height*10), Image.NEAREST)
            img.save(self.name + "_" + str(image_number) + ".png")
        except Exception, e:
            print str(e)

    def save_predict_image(self, best, image_number):
        try:
            from PIL import Image
            print " Saving Image: " + self.name + "_predict_" + str(image_number) + ".png..."
            img = Image.new("RGB", (width, height))
            for r in range(height):
                for c in range(width):
                    if (c, r) == best:
                        img.putpixel(best, (255, 0, 0))
                    elif self.FV_size != 3:
                        sum = 0
                        for i in range(self.FV_size):
                            sum += self.nodes[r, c, i]
                            #print sum
                        val = int(sum/self.FV_size)
                        img.putpixel((c, r), (val, val, val))
                    else:
                        img.putpixel((c, r), (int(self.nodes[r, c, 0]), int(self.nodes[r, c, 1]), int(self.nodes[r, c, 1])))
            img = img.resize((width*10, height*10), Image.NEAREST)
            img.save(self.name + "_predict_" + str(image_number) + ".png")
        except Exception, e:
            print str(e)


if __name__ == "__main__":
    print "Initialization..."
    print "Demo 1:"
    colors = [ [0, 0, 0], [0, 0, 255], [0, 255, 0], [0, 255, 255], [255, 0, 0], [255, 0, 255], [255, 255, 0], [255, 255, 255]]
    width = 32
    height = 32
    color_som = SOM("colors", width, height, 3, 0.05)
    print "Training colors..."
    color_som.train(colors, 100)
    color_som.save_image(101)

    print "Demo 2:"
    train_file = 'train.txt'
    train_data = []
    with open(train_file,'r') as train:
        for line in train:
            sample = line.rstrip().split(',')
            train_data.append(sample)
    train_data = [map(int, x) for x in train_data]

    max_train_values = [0] * len(train_data[0])
    for i in range(len(train_data)):
        for j in range(len(train_data[i])):
                if train_data[i][j] > max_train_values[j]:
                    max_train_values[j] = train_data[i][j]

    # data whitening
    for i in range(len(train_data)):
        for j in range(len(train_data[i])):
            train_data[i][j] = int(train_data[i][j] / max_train_values[j])

    width = 32
    height = 32
    obs_som = SOM("cpu_som", width, height, 4, 0.03, 100)
    print "Training on observed data"
    obs_som.train(train_data, 100)
    obs_som.save_image(101);

    # for i in range(len(train_data)):
    #     best = obs_som.predict(train_data[i])
    #     obs_som.save_predict_image(best, i)