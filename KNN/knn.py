from os.path import exists
import math
from collections import Counter
from os.path import abspath, join, dirname

MAIN_PATH = dirname(__file__)

test_element = [91.1,6.9,2.0,66.1,26.0,7.9]
test_element_2 = [10.0,20.0,70.0,10.0,10.0,80.0]
test_element_3 = [20.0,50.0,30.0,30.0,50.0,20.0]

class KnnClassifier(object):
    def __init__(self, attr_qtt, class_qtt, db_size, file_name, trainning_perc=100):
        self.attr_qtt = attr_qtt
        self.class_qtt = class_qtt
        self.db_size = db_size
        self.file_name = file_name
        self.trainning_size = int(self.db_size*(trainning_perc))

        #Get a list of all instances in the file.
        self.elements = self.GetElementsFromFile(file_name, self.attr_qtt)
        
        #Find the range in every attribute.
        self.ranges = self.SetAttrRange()

        #Set the trainning set.
        self.trainning_set = self.elements[0:self.trainning_size]

    #Reads the file and returns a list of elements with respective attributes.
    def GetElementsFromFile(self, file_name, qt_attr):

        file_path = join(MAIN_PATH, file_name)

        #Opening and Opening the file
        source_file = open(file_path, "r")

        #Reading the Lines
        lines = source_file.readlines()

        #Building the list of list.
        element_set = []
        for line in lines:
            new_line = line.strip('\n')     #Removing '\n'.
            new_element = map(float,new_line.rsplit(',',qt_attr))       #Separating the Attributes and Setting them as float.
            element_set.append(new_element)

        return element_set

        from_file = "breast_cancer_db_shuffled.txt"

    #Returns a list of ranges for each of the attributes.
    def SetAttrRange(self):
    
        ranges = []
    
        #For every attribute.
        for x in range (0, self.attr_qtt):
            min = self.elements[0][x]
            max = self.elements[0][x]
    
            for element in self.elements:
                if (element[x] < min ):     #Update min.
                    min = element[x]
    
                if (element[x] > max):     #Update max.
                    max = element[x]
    
            ranges.append(round(max - min,2))
    
        return ranges

    def classify_element(self, test_element, k=3):
        #Get the k-closest neighbors of test_element.
        k_closest_neighboors = self.KNN(k, test_element, self.trainning_set, self.attr_qtt , self.ranges)

        #Get the frequency of every close neighbor.
        most_common = self.GetMostCommonPattern(k_closest_neighboors, self.class_qtt, self.attr_qtt)

        #Gets the decision if the system hit or missed the pattern and append to a list.
        return most_common[0][0]

    #Returns a dict with the frequency of each class among the closest neighbors.
    def GetMostCommonPattern(self, neighbor_list, qt_of_classes, qt_of_attr):

        neighbors = []
        for element in neighbor_list:
            neighbors.append(element[0][qt_of_attr])

        return Counter(neighbors).most_common(1)

    #Returns the K-Closest Neighbors
    def KNN(self, k, xq, elements, Attr_Qtt, ranges):

        def NormalizedEuclidian(xq, element, qt_attr, ranges):

            #XQ = [x0,x1,...,xn]
            #element = [e0,e0,...,en]
            #range = [r0,r1,...,rn]

            sum = 0.0
            for x in range (0, qt_attr):
                sum = sum + math.pow(((xq[x]-element[x])/ranges[x]),2)

            return round(math.sqrt(sum),6)

        closest_set = []

        #Fill closest_set with the k first elements and their respective distance from the query pattern.
        #closest_set = [[element,dist],...,[element,dist]]
        for x in range(0,k):
            dist = NormalizedEuclidian(xq, elements[x], Attr_Qtt, ranges)
            new_element = []
            new_element.append(elements[x])
            new_element.append(dist)
            closest_set.append(new_element)

        #Sort the closest_set
        closest_set.sort(key = lambda tup: tup[1])

        #Find the k-closest Neighbors
        for element in elements[k:]:
            dist = NormalizedEuclidian(xq, element, Attr_Qtt, ranges)

            if( dist < closest_set[k -1][1]):   #Change the last element and reorder the list.
                new_element = []
                new_element.append(element)
                new_element.append(dist)
                closest_set[k -1] = new_element
                closest_set.sort(key = lambda tup: tup[1])

        return closest_set
