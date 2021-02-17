import os
import sys
from utils import *
import numpy as np

# merging a range sequence


def mergeRangeSeq(left_seq, right_seq, L):

    result = []

    for i in range(0, len(right_seq)):

        for j in range(0, abs(right_seq[i]-left_seq[i])+1):
            if(left_seq[i] <= right_seq[i]):
                result.append(left_seq[i]+j)
            else:
                result.append(left_seq[i]-j)

            if(len(result) == L):
                return result

    return result

# merging a step sequence


def mergeStepSeq(left_seq, right_seq, L):

    result = []

    for i in range(0, len(right_seq)):

        for j in range(0, right_seq[i]):
            result.append(left_seq[i])

            if(len(result) == L):
                return result
    return result


def fitLowestRankPolyModel(x_data, y_data):
    err = 1e-20
    model = None

    for r in range(1, 10):
        coeffs = np.polyfit(x_data, y_data, r, full=True)

        if(coeffs[1]):
            residual = float(coeffs[1][0])
        else:  # hack
            residual = 0.0
        if(residual < err):
            model = np.poly1d(coeffs[0])
            break

    return model


# check 2 tags are of the form l_tag_s , l_tag_e
def sameLoopTag(tag1, tag2):
    lnum1 = int(tag1.split("_")[0][1:])
    lnum2 = int(tag2.split("_")[0][1:])

    return (lnum2 == lnum1 and ("s" in tag1) and ("e" in tag2))


# removing the string tags used for loop boundries
def removeTags(data):
    result = []

    for i in range(0, len(data)):
        if("l" not in str(data[i])):
            result.append(data[i])
    return result


# classification routine : range vs step
def classify(data):

    data_wo_tags = removeTags(data)
    # type 1 : can fit a poly model
    strictly_incresing = True
    strictly_decreasing = True
    all_same = True

    step_type_count = 0
    range_type_count = 0

    for i in range(0, len(data_wo_tags)-1):
        if(data_wo_tags[i] >= data_wo_tags[i+1]):
            strictly_incresing = False
        if(data_wo_tags[i] <= data_wo_tags[i+1]):
            strictly_decreasing = False
        if(data_wo_tags[i] != data_wo_tags[i+1]):
            all_same = False

        # for deciding range vs step
        if(data_wo_tags[i] == data_wo_tags[i+1]):
            step_type_count += 1
        elif((data_wo_tags[i] < data_wo_tags[i+1]) or (data_wo_tags[i] > data_wo_tags[i+1])):
            range_type_count += 1

    if(strictly_decreasing or strictly_incresing or all_same):
        return 1

    # type 2 : range sequence
    if(step_type_count < range_type_count):
        return 2

    # type 3 : step sequnce
    elif(step_type_count > range_type_count):
        return 3

    # unknown sequence
    return 0

# summerization  routine


def summerizeSeq(data, type):

    child_1 = []
    child_2 = []

    loop_seq = []
    loop_stack = Stack()
    for i in range(0, len(data)):

        if("l" in str(data[i])):
            if(len(loop_seq) > 0):
                loop_stack.pop()
                if(type == 2):
                    loop_stack.push([loop_seq[0], loop_seq[-1]])
                elif(type == 3):
                    # check for merge possibilies
                    if((loop_stack.top() != None) and (loop_stack.top()[0] == loop_seq[0])):
                        top_element = loop_stack.top()
                        loop_stack.pop()
                        loop_stack.push(
                            [loop_seq[0], len(loop_seq)+top_element[1]])
                    else:
                        loop_stack.push([loop_seq[0], len(loop_seq)])
                loop_seq = []
            else:
                if("l" in str(loop_stack.top()) and sameLoopTag(loop_stack.top(), data[i])):
                    loop_stack.pop()
                else:
                    loop_stack.push(data[i])
        else:
            loop_seq.append(data[i])

    stack_seq = loop_stack.stack

    for i in range(0, len(stack_seq)):
        if("l" in str(stack_seq[i])):
            child_1.append(stack_seq[i])
            child_2.append(stack_seq[i])
        else:
            child_1.append(stack_seq[i][0])
            child_2.append(stack_seq[i][1])

    return [child_1, child_2]


# this class is used for modeling the variation of a gievn loop
# induction variable. For now only polynomial models are assumed
# order : nested level of the loop. order=1 means outer most loop

class sequenceModel:

    def __init__(self, data, parent):
        self.data = data

        # summmerization information
        self.isRange = False
        self.isStep = False
        self.isPoly = False
        self.leftModel = None
        self.rightModel = None
        self.model = None
        self.parent = parent

        # correction models make the sequence models independant of the scale by
        # traing it accross scales
        self.leaf_correction_data = []
        self.leaf_correction_model = None
        self.leaf_correction_train_scales = []

        pattern_type = classify(data)

        if(pattern_type == 1):
            self.isPoly = True
            self.buildPolyModel()
        elif(pattern_type == 2):
            self.isRange = True
            summerized = summerizeSeq(data, 2)

            self.leftModel = sequenceModel(summerized[0], self)
            self.rightModel = sequenceModel(summerized[1], self)

        elif(pattern_type == 3):
            self.isStep = True
            summerized = summerizeSeq(data, 3)

            self.leftModel = sequenceModel(summerized[0], self)
            self.rightModel = sequenceModel(summerized[1], self)
        else:
            printErrMsg("Can not fit model. Unknown sequence")
            sys.exit(-1)

    # if this model is a leaf model the constant coefficient of the
    # poly model needs to be trained across scale
    def updateCorrectionModel(self):

        if(not allSame(self.leaf_correction_data)):
            Y_data = self.leaf_correction_data
            X_data = self.leaf_correction_train_scales
            self.leaf_correction_model = fitLowestRankPolyModel(X_data, Y_data)

    def printModel(self):
        if(self.isPoly):
            print("poly")
            print(str(self.models))
        elif(self.isRange):
            print("range")
            self.leftModel. printModel()
            self.rightModel.printModel()
        elif(self.isStep):
            print("step")
            self.leftModel. printModel()
            self.rightModel.printModel()

    # This function appends only the leaf models
    # to the list
    def getLeafModels(self, leaf_models):
        if(self.isPoly):
            leaf_models.append(self)
        elif(self.isRange or self.isStep):
            self.leftModel.getLeafModels(leaf_models)
            self.rightModel.getLeafModels(leaf_models)

    def buildPolyModel(self):

        Y_data = removeTags(self.data)
        X_data = [i+1 for i in range(0, len(Y_data))]

        self.models = fitLowestRankPolyModel(X_data, Y_data)

    # predict the sequence for count number of elements

    def predictSeq(self, count, scale):

        result = []

        if(self.isPoly):
    
            const_coeff = int(round(self.models.c[-1]))

            correction = 0
            if(str(self.leaf_correction_model) != "None"):
                correction = -const_coeff+self.leaf_correction_model(scale)

            for i in range(0, count):
                float_val = self.models(i+1)

                # first remove the constant coefficient from the value
                # and then add back the correct value
                float_val = float_val+correction

                result.append(int(round(float_val)))

        elif(self.isRange or self.isStep):

            # TODO : we are being over predicting here
            leftSeq = self.leftModel.predictSeq(count, scale)
            rightSeq = self.rightModel.predictSeq(count, scale)

            # strip additional elements
            min_len = min(len(leftSeq), len(rightSeq))

            leftSeq = leftSeq[0:min_len]
            rightSeq = rightSeq[0:min_len]

            if(self.isRange):
                result = mergeRangeSeq(leftSeq, rightSeq, count)
            elif(self.isStep):
                result = mergeStepSeq(leftSeq, rightSeq, count)

        return result[0:count]


if __name__ == "__main__":
    main()
