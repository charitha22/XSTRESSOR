import sys
from z3 import *
from utils import *
from model import *
from expr_writer import *
# from cfg_emulator import *
import time


class predicateModel:
    def __init__(self, predicate, seq_data, scale_data):

        printDbgMsg(
            "building a predicate model for predicate " +
            str(predicate))
        printDbgMsg("shape of seq_data : " + str(dim_of_list(seq_data)))
        printDbgMsg("shape of scale_data : " + str(dim_of_list(scale_data)))
        self.predicate = predicate
        self.seq_data = seq_data
        self.scale_data = scale_data
        self.seq_models = []
        self.scale_model = None

        self.hasScale = False
        self.non_scale_models = []

        if(self.seq_data is not None and self.scale_data is not None):
            self.hasScale = True
            self.buildSeqModels()
            self.buildScaleModel()

    def buildScaleModel(self):

        self.scale_model = fitLowestRankPolyModel(
            self.scale_data[0], self.scale_data[1])

    def buildSeqModels(self):

        for i in range(0, len(self.seq_data)):
            seq = self.seq_data[i]
            seq_model = sequenceModel(seq, None)
            self.seq_models.append(seq_model)

    def buildNonScaledModel(self, scale_to_cond_map):
        scales = sorted(scale_to_cond_map.keys())

        for i in range(0, len(scale_to_cond_map[scales[0]][0])):
            seq = []
            for j in range(0, len(scales)):
                seq.append(scale_to_cond_map[scales[j]][0][i])

            model = fitLowestRankPolyModel(list(scales), seq)

            self.non_scale_models.append(model)


class PredicateMap:
    def __init__(self):
        # this is map of maps
        # preidicate -> (scale -> value_vecs) type
        self.pred_to_scale_to_cond_map = {}
        self.predicates = []
        self.max_scale = 0
        self.min_scale = 0

    def addPredicate(self, predicate):

        if(str(predicate) not in self.pred_to_scale_to_cond_map.keys()):
            self.predicates.append(predicate)
            self.pred_to_scale_to_cond_map[str(predicate)] = {}

    def findUniquePredicates(self, longest_path, scale_longest_path):

        for item in longest_path:

            if(isinstance(item, str)):
                continue

            else:
                # TODO : value_vec is not used here! combine addPathCond with
                # this
                [predicate, value_vec] = getPredStrucAndValueVec(item)

                self.addPredicate(predicate)

                # update scale map
                for i in range(0, scale_longest_path):
                    self.pred_to_scale_to_cond_map[str(predicate)][i + 1] = []

    # for every predicate we need to update

    def updateTrace(self, loop_tag, scale):

        # for all predicates
        for predicate in self.pred_to_scale_to_cond_map.keys():

            scale_map = self.pred_to_scale_to_cond_map[predicate]

            scale_map[scale].append(loop_tag)

    def addPathCond(self, expr_array, scale):

        for expr in expr_array:
            # get the strcuture
            if(isinstance(expr, str)):
                self.updateTrace(expr, scale)

            else:
                [predicate_struct, value_vecs] = getPredStrucAndValueVec(expr)
                self.updateMap(predicate_struct, scale, value_vecs)

        # update max scale and min scale
        scales = sorted(
            self.pred_to_scale_to_cond_map[str(self.predicates[0])].keys())

        self.max_scale = scales[-1]
        self.min_scale = scales[0]

    def updateMap(self, predicate, scale, feature_vec):

        self.pred_to_scale_to_cond_map[str(
            predicate)][scale].append(feature_vec)

    def buildPredicateModel(self, predicate):
        scale_to_cond_map = self.pred_to_scale_to_cond_map[str(predicate)]
        printDbgMsg("max scale = " + str(self.max_scale))

        # train the sequence generators at different scales.
        # This is important because some of the generators are dependant on scale
        # i.e. their leaf polynomials changes with scale
        predicate_models = []
        for t in range(0, 5):
            longest_path = scale_to_cond_map[self.max_scale - t]
            # how many independant induction vars?
            num_seqs = len(removeTags(longest_path)[0])
            seqs = [[] for i in range(0, num_seqs)]

            # split longest path into ind variable sequences
            for item in longest_path:
                if(isinstance(item, str)):
                    for j in range(0, len(seqs)):
                        seqs[j].append(item)
                else:
                    for j in range(0, len(seqs)):
                        seqs[j].append(item[j])

            # get scale data
            scale_values = []
            predicate_hits = []

            for i in range(1, self.max_scale + 1):
                scale_values.append(i)
                predicate_hits.append(len(removeTags(scale_to_cond_map[i])))

            # TODO : ugly hack to handle complicated initial conditions of sequences
            # seqs = self.handleInitialConditions(seqs)

            predicate_model = None
            if(self.hasScaleProperties(predicate_hits)):
                scale_data = [scale_values, predicate_hits]
                predicate_model = predicateModel(predicate, seqs, scale_data)

            else:
                predicate_model = predicateModel(predicate, None, None)
                predicate_model.buildNonScaledModel(scale_to_cond_map)

            predicate_models.append(predicate_model)

            # if this predicate is a one time thing then no need to
            # train acorss scales
            if(not self.hasScaleProperties(predicate_hits)):
                break

        # final model need to be scale-independant
        final_pred_model = None
        if(len(predicate_models) > 1):
            train_scales = self.getTrainScales()
            self.makePredicateScaleIndependant(predicate_models, train_scales)

        # we apply the correction to only the predicate trained
        # using maximum scale
        final_pred_model = predicate_models[0]

        return final_pred_model

    # TODO : if we train on different scales this function
    # needs to be changed
    def getTrainScales(self):
        train_scales = [self.max_scale - i for i in range(0, 5)]
        return train_scales

    def makePredicateScaleIndependant(self, models, train_scales):
        printDbgMsg("No of predicate models = " + str(len(models)))
        no_of_models = len(models)
        no_of_seq_models = len((models[0].seq_models))

        for i in range(0, no_of_seq_models):
            max_scale_leaf_models = []

            for j in range(0, no_of_models):
                leaf_models = []
                models[j].seq_models[i].getLeafModels(leaf_models)

                if(j == 0):
                    max_scale_leaf_models = leaf_models

                for k in range(0, len(leaf_models)):
                    max_scale_leaf_models[k].leaf_correction_data.append(
                        int(round(leaf_models[k].models.c[-1])))

            # print(dim_of_list(model_list))
            for k in range(0, len(max_scale_leaf_models)):
                max_scale_leaf_models[k].leaf_correction_train_scales = train_scales
                max_scale_leaf_models[k].updateCorrectionModel()

    # if predicate hits is 1 across all scales we decide this predicate
    # doesn't scale

    def hasScaleProperties(self, pred_hits):

        for i in range(0, len(pred_hits)):
            if(pred_hits[i] != 1):
                return True

        return False


# this class is responsible for extracting the
# features from  the set of conditions in a path
# condition for all scales

class PathAnalyzer:

    def __init__(self, path_conditions):
        self.paths = path_conditions
        self.program = PredicateMap()
        self.predicate_models = []
        self.symbolic_store = {}

        self.updatePredicates()

    def updatePredicates(self):

        # find different predcates in the path condition
        longest_path = self.paths[-1]
        scale_longest_path = len(self.paths)
        self.program.findUniquePredicates(longest_path, scale_longest_path)
        # assume the scale starts at 1
        scale = 1

        for path in self.paths:

            self.program.addPathCond(path, scale)
            scale += 1

        # print(self.program.pred_to_scale_to_cond_map)

    # this function builds a model for each of the predicate
    # to predict how the induction variables change in large scale
    def buildModel(self):

        printInfoMsg("This program has " +
                     str(len(self.program.predicates)) +
                     " symbolic predicates")

        for predicate in self.program.predicates:

            predicate_model = self.program.buildPredicateModel(predicate)

            self.predicate_models.append(predicate_model)

    # we need model the assignmensts first
    def rearrangePredicates(self):

        assignments = []
        normal_predicates = []

        for pmodel in self.predicate_models:
            if("assign" in str(pmodel.predicate)):
                assignments.append(pmodel)
            else:
                normal_predicates.append(pmodel)

        self.predicate_models = assignments + normal_predicates

    def genScaleTest(self, scale):

        printInfoMsg("Generating a test case for scale " + str(scale))

        path_condition = []
        symbolic_store_state = {}
        array_funcs = []

        # self.rearrangePredicates()

        for pmodel in self.predicate_models:
            # generate induction variable sequences
            ind_var_seqs = []

            # add array funcs : give that to user to add initial constraints
            self.updateArrayFuncs(pmodel.predicate, array_funcs)

            # hack to handle non scaling predicates
            if(not pmodel.hasScale):
                seq = []
                for m in pmodel.non_scale_models:
                    ind_var_seqs.append([int(round(m(scale)))])

            else:
                # how many predcate hits
                phits = int(round(pmodel.scale_model(scale)))

                for seq_model in pmodel.seq_models:

                    ind_var_seqs.append(seq_model.predictSeq(phits, scale))

            # add symbolic varibles need for prediction
            self.updateSymbolicStore(pmodel.predicate, ind_var_seqs)

            for i in range(0, len(ind_var_seqs[0])):

                expr_val_vec = []

                for j in range(0, len(ind_var_seqs)):
                    expr_val_vec.append(ind_var_seqs[j][i])

                cond_writer = ExprWriter(
                    pmodel.predicate, expr_val_vec, self.symbolic_store)
                path_condition.append(cond_writer.condition)

        return [path_condition, self.symbolic_store, array_funcs]

    def solve(self, conditions):

        s = Solver()

        for c in conditions:

            s.add(c)

        printInfoMsg("Satisfiability : " + str(s.check()))
        solution = []

        if(str(s.check()) == "sat"):

            m = s.model()

            for item in m:
                s = str(item) + " = " + str(m[item])
                # print(s)
                solution.append(s)

        # return solution
        ret = None

        if(len(solution) > 0):
            ret = solution

        return ret

    def updateArrayFuncs(self, predicate, arrays):
        for struct in predicate:
            if(is_array(struct) and struct not in arrays):
                arrays.append(struct)

    def updateSymbolicStore(self, structure, value_seq):

        # vriable j points to current reading location of the value_seq
        j = 0

        for i in range(0, len(structure)):

            if("var" in str(structure[i])):

                # multi dimensional case
                if("mda" in str(structure[i])):
                    # get the dimension of array variable, say d.
                    # then get d no of elements from the value_seq and
                    # create a new symbolic variable

                    dim = int(str(structure[i]).split("mda")[1].split("_")[0])

                    for k in range(0, len(value_seq[j])):

                        dim_values = ""

                        for d in range(0, dim):
                            dim_values += "_" + str(value_seq[j + d][k])

                        var_name = str(structure[i]) + dim_values

                        if(var_name not in self.symbolic_store.keys()):

                            # hack to support bools
                            if("bool" in var_name):
                                self.symbolic_store[var_name] = Bool(var_name)
                            else:
                                self.symbolic_store[var_name] = Int(var_name)

                    j += dim

                # one deimensional case
                else:

                    for item in value_seq[j]:

                        var_name = str(structure[i]) + str(item)
                        if(var_name not in self.symbolic_store.keys()):

                            self.symbolic_store[var_name] = Int(var_name)

                    j += 1

            elif("const" in str(structure[i])):
                j += 1
