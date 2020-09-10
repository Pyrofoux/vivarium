import numpy as np
import matplotlib.pyplot as plt

class Logger():

    data = {}

    def add(value, label = "logs"):

        if not label in Logger.data:
            Logger.data[label] = []

        Logger.data[label].append(value)

        #WARNING : you need to call Logger.show() after all plots
        #To show multiple figures at once !
    def plot(char = '.', labels = False, type = 'plot'):

        plt.figure()
        if not labels:
            labels = dict.keys(Logger.data)

        for label in labels:

            if type == 'polar':
                plt.polar(Logger.data[label], np.arange(0,len(Logger.data[label]),1), char)

            elif type== 'plot':
                plt.plot(Logger.data[label], char)

            elif type =='scatter':
                print( Logger.data[label])
                x = [x for (x,y) in Logger.data[label]]
                y = [y for (x,y) in Logger.data[label]]
                plt.scatter(x,y)

        plt.legend(labels)

        #Need to manually call plt.show() after all plots!
        #plt.show()

    def show():
        plt.show()
