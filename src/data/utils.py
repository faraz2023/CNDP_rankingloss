import matplotlib.pyplot as plt
import networkx as nx
import collections
import numpy as np
import json
from scipy.stats import rankdata
from sklearn.preprocessing import OneHotEncoder
from scipy.linalg import expm
from src.data import config
from joblib import Parallel, delayed
import time, math
from tqdm import tqdm

##
class GenerateData():
    def __init__(self):
        print("Generation class is invoked")

        # self.maxdegree = 0.7 * self.size
        self.alba_m =3
        self.rgradius = 0.2 # threshold radius for connecting edges in RGN
        self.triprob = 0.5
        self.erprob = 0.2
        # self.maxdegree = 0.8*self.size
        self.maxbetweenness = 0.8*1.0

    def generate_degreedata(self,n, datadir,genflag=0,):
        if genflag ==1:
            inputtensor = []
            targetvec = []
            def get_sample():
                g = nx.generators.random_graphs.powerlaw_cluster_graph(self.size, 1, self.triprob)
                temp_input = nx.adj_matrix(g).toarray()

                temp_label = []
                for node,deg in nx.degree(g):
                    if deg <= (0.33*self.maxdegree):
                        temp_label.append(0)
                    elif (deg > (0.33*self.maxdegree)) and (deg <= 0.66*self.maxdegree):
                        temp_label.append(1)
                    elif deg > (0.66*self.maxdegree):
                        temp_label.append(2)

                return temp_input, temp_label

            for i in range(n):
                input, target = get_sample()
                inputtensor.append(input)
                targetvec.append(target)

            np.save(datadir+'\degree_adj.npy', inputtensor)
            np.save(datadir+'\degree_target.npy', targetvec)

        else:
            inputtensor = np.load(datadir + '\degree_adj.npy')
            targetvec = np.load(datadir + '\degree_target.npy')

        return np.array(inputtensor), np.array(targetvec)

    def generate_betdata_plmodel(self,n, V, datadir, predictor, genflag=0):
        if genflag ==1:
            inputtensor = []
            targetvec = []
            featurevec =[]
            def get_sample():
                g = nx.generators.random_graphs.powerlaw_cluster_graph(V, 1, self.triprob)
                temp_input = nx.adj_matrix(g).toarray()
                # temp_input = expm(temp_input)
                # temp_input = nx.laplacian_matrix(g).toarray()
                # temp_input = np.linalg.pinv(temp_input)
                # temp_input = nx.normalized_laplacian_matrix(g).toarray()

                temp_label = []
                for key, deg in nx.betweenness_centrality(g).items():
                    if deg <= (0.33*self.maxbetweenness):
                        temp_label.append(0)
                    elif (deg > (0.33*self.maxbetweenness)) and (deg <= 0.66*self.maxbetweenness):
                        temp_label.append(1)
                    elif deg > (0.66*self.maxbetweenness):
                        temp_label.append(2)

                # input node feature
                feat = np.ones(shape=(V, 1))
                feat[:, 0] = np.reshape(np.sum(nx.adj_matrix(g).todense(), axis=1), (V,))
                return temp_input, temp_label, feat

            for i in range(n):
                input, target, feat = get_sample()
                inputtensor.append(input)
                targetvec.append(target)
                featurevec.append(feat)


            np.save(datadir+'predictor.npy', inputtensor)
            np.save(datadir+'target.npy', targetvec)
            np.save(datadir+'feature.npy', featurevec)

        else:
            inputtensor = np.load(datadir + 'predictor.npy')
            targetvec = np.load(datadir + 'target.npy')
            featurevec = np.load(datadir + 'feature.npy')

        return np.array(inputtensor), np.array(targetvec), np.array(featurevec)

    def generate_betdata_ermodel(self,n, datadir, predictor, genflag=0):
        if genflag ==1:
            inputtensor = []
            targetvec = []
            def get_sample(predictor):
                g = nx.erdos_renyi_graph(self.size,self.erprob)
                if predictor == "adjacency":
                    temp_input = nx.adj_matrix(g).toarray()
                else:
                    temp_input = nx.laplacian_matrix(g).toarray()
                    temp_input = np.linalg.pinv(temp_input)

                temp_label = []
                for key, deg in nx.betweenness_centrality(g).items():
                    if deg <= 0.1:
                        temp_label.append(0)
                    elif (deg > 0.1) and (deg <= 0.2):
                        temp_label.append(1)
                    elif deg > 0.2:
                        temp_label.append(2)

                return temp_input, temp_label

            for i in range(n):
                input, target = get_sample(predictor)
                inputtensor.append(input)
                targetvec.append(target)

            np.save(datadir+'feature.npy', inputtensor)
            np.save(datadir+'target.npy', targetvec)

        else:
            inputtensor = np.load(datadir + 'feature.npy')
            targetvec = np.load(datadir + 'target.npy')

        return np.array(inputtensor), np.array(targetvec)

    def generate_betdata_albamodel(self,n, V, datadir, predictor, genflag=0):
        if genflag ==1:
            inputtensor = []
            targetvec = []
            def get_sample(predictor):
                g = nx.barabasi_albert_graph(V, self.alba_m)

                if predictor == "adjacency":
                    temp_input = nx.adj_matrix(g).toarray()
                else:
                    temp_input = nx.laplacian_matrix(g).toarray()
                    temp_input = np.linalg.pinv(temp_input)

                temp_label = []
                for key, deg in nx.betweenness_centrality(g).items():
                    if deg <= 0.05:
                        temp_label.append(0)
                    elif (deg > 0.05) and (deg <= 0.15):
                        temp_label.append(1)
                    elif deg > 0.15:
                        temp_label.append(2)

                return temp_input, temp_label

            for i in range(n):
                input, target = get_sample(predictor)
                inputtensor.append(input)
                targetvec.append(target)

            np.save(datadir+'feature.npy', inputtensor)
            np.save(datadir+'target.npy', targetvec)

        else:
            inputtensor = np.load(datadir + 'feature.npy')
            targetvec = np.load(datadir + 'target.npy')

        return np.array(inputtensor), np.array(targetvec)

    def generate_betdata_rgmodel(self,n, datadir, predictor, genflag=0):
        if genflag ==1:
            inputtensor = []
            targetvec = []
            def get_sample(predictor):
                g = nx.random_geometric_graph(self.size, self.rgradius)

                if predictor == "adjacency":
                    temp_input = nx.adj_matrix(g).toarray()
                else:
                    temp_input = nx.laplacian_matrix(g).toarray()
                    temp_input = np.linalg.pinv(temp_input)

                temp_label = []
                for key, deg in nx.betweenness_centrality(g).items():
                    if deg <= 0.05:
                        temp_label.append(0)
                    elif (deg > 0.05) and (deg <= 0.15):
                        temp_label.append(1)
                    elif deg > 0.15:
                        temp_label.append(2)

                return temp_input, temp_label

            for i in range(n):
                input, target = get_sample(predictor)
                inputtensor.append(input)
                targetvec.append(target)

            np.save(datadir+'feature.npy', inputtensor)
            np.save(datadir+'target.npy', targetvec)

        else:
            inputtensor = np.load(datadir + 'feature.npy')
            targetvec = np.load(datadir + 'target.npy')

        return np.array(inputtensor), np.array(targetvec)

    def splitthree_data(self, data, label, feature):
        trainingind = int(0.75*len(data))
        valind = int(0.85*len(data))

        xtrain = data[0:trainingind,:]
        ytrain = label[0:trainingind,:]
        ftrain = feature[0:trainingind,:]

        xval = data[trainingind:valind]
        yval = label[trainingind:valind,:]
        fval = feature[trainingind:valind,:]

        xtest = data[valind:len(data)]
        ytest = label[valind:len(data),:]
        ftest = feature[valind:len(data), :]

        return xtrain, ytrain, ftrain, xval, yval, fval, xtest, ytest, ftest

    def splittwo_data(self, data, label, feature):
        trainingind = int(0.90*len(data))

        xtrain = data[0:trainingind,:]
        ytrain = label[0:trainingind,:]
        ftrain = feature[0:trainingind,:]

        xtest = data[trainingind:len(data),:]
        ytest = label[trainingind:len(data),:]
        ftest = feature[trainingind:len(data), :]

        return xtrain, ytrain, ftrain, xtest, ytest, ftest

    def generate_betweenness_plmodel(self,n, V, datadir, predictor, genflag=0):
        if genflag ==1:
            inputtensor = []
            targetvec = []
            featurevec =[]
            def get_sample():
                g = nx.generators.random_graphs.powerlaw_cluster_graph(V, 1, self.triprob)
                temp_input = nx.adj_matrix(g).toarray()
                # temp_input = expm(temp_input)
                # temp_input = nx.laplacian_matrix(g).toarray()
                # temp_input = np.linalg.pinv(temp_input)
                # temp_input = nx.normalized_laplacian_matrix(g).toarray()

                temp_label = list(nx.betweenness_centrality(g).values())

                # input node feature
                feat = np.ones(shape=(V, 1))
                feat[:, 0] = np.reshape(np.sum(nx.adj_matrix(g).todense(), axis=1), (V,))
                return temp_input, np.array(temp_label), feat

            for i in range(n):
                input, target, feat = get_sample()
                inputtensor.append(input)
                targetvec.append(target)
                featurevec.append(feat)


            np.save(datadir+'predictor.npy', inputtensor)
            np.save(datadir+'target.npy', targetvec)
            np.save(datadir+'feature.npy', featurevec)

        else:
            inputtensor = np.load(datadir + 'predictor.npy')
            targetvec = np.load(datadir + 'target.npy')
            featurevec = np.load(datadir + 'feature.npy')

        return np.array(inputtensor), np.array(targetvec), np.array(featurevec)

class GenEgrData():

    def __init__(self):
        print("Generation of EGR class is invoked")

    def get_egr(self, graph):
        eig = nx.linalg.spectrum.laplacian_spectrum(graph)
        try:
            eigtemp1 = [1/num for num in eig if num > 5e-10]
            # eig = [1 / num for num in eig[1:] if num != 0]
            eigtemp2 = sum(np.abs(eigtemp1))
        except:
            print("zero encountered in Laplacian eigen values")

        Rg = (2 / (len(graph.nodes()) - 1))*(eigtemp2)
        return np.round(Rg, 3)

    def get_flowrobustness(self,graph):
        n= len(graph.nodes)
        ci = [len(c) for c in sorted(nx.connected_components(graph), key=len, reverse=True)]
        tempfr = sum([count*(count-1) for count in ci])
        result  = tempfr/(n*(n-1))

        return result

    def get_weightedspectrum(self, graph):

        lambdas = nx.linalg.spectrum.normalized_laplacian_spectrum(graph)
        wghtspm = sum([(1 - eigs)**3 for eigs in lambdas])

        return round(wghtspm,3)

    def get_criticality(self, g):
        L = nx.laplacian_matrix(g).toarray()
        Linv = np.linalg.pinv(L)
        TraceLinv = np.trace(Linv)
        ncr = (2/(len(g.nodes)-1))*TraceLinv

        return np.round(ncr,3)

    ### get rank of edges from eigen values of laplacian method- exact method

    def get_egrlinkrank(self, g):

        egr_new = np.zeros(len(g.edges))
        for countedge, (v1, v2) in enumerate(g.edges()):
            g[v1][v2]['edgepos'] = countedge
            gcopy = g.copy()
            gcopy.remove_edge(v1, v2)
            egr_new[countedge] = self.get_egr(gcopy)

        # egr_diff = egr_new - egr_old
        ### rank of the egr_new
        order = egr_new.argsort()
        ranks = order.argsort() + 1  # getting ranks from 1 and high rank denotes high importance score

        #### normalize to 0 to 1 range
        # ranks = (ranks - min(ranks)) / (max(ranks) - min(ranks))

        return ranks

    def get_egrnoderank(self, g):

        egr_new = np.zeros(len(g.nodes))
        for countnode, node in enumerate(g.nodes()):
            # g[v1][v2]['edgepos'] = countedge
            gcopy = g.copy()
            ## node removal at secondary
            # noderemoval=[node]
            # for neighbor in g.neighbors(node):
            #     if g.degree(neighbor) == 1:
            #         noderemoval.append(neighbor)

            gcopy.remove_node(node)
            egr_new[countnode] = self.get_egr(gcopy)
            # print(countnode)

        # lower egr corresponds to low robustness/connectivity
        ranks = rankdata(egr_new, method='dense')

        return ranks

    def get_wghtspectnoderank(self,g):

        ws_new = np.zeros(len(g.nodes))

        for countnode, node in enumerate(g.nodes()):
            gcopy = g.copy()
            gcopy.remove_node(node)
            ws_new[countnode] = self.get_weightedspectrum(gcopy)

        # higher ws corresponds to lower robustness/connectivity
        ranks = rankdata([-1 * i for i in ws_new], method='dense')

        return ranks
    # generate power law cluster graphs (scale free + small world)

    def gen_plclustermodel(self, n, V, metrictype, genflag=0):
        if genflag ==1:
            targetvec = []
            featurevec = []
            graphvec = []

            enc = OneHotEncoder(handle_unknown='ignore')

            def get_sample(metrictype):
                g = nx.generators.random_graphs.powerlaw_cluster_graph(V, 1, 0.1)

                ## node rank on the basis of egr/weighted spectrum
                if metrictype == 'egr':
                    ranks = self.get_egrnoderank(g)
                elif metrictype == 'weightedspectrum':
                    ranks = self.get_wghtspectnoderank(g)

                # ranks = np.array([2 if ind >= int(0.75*V) else 1 if (ind > int(0.25*V)) and (ind < int(0.75*V)) else 0 for ind in temp_ranks])
                ranks = (ranks - min(ranks)) / (max(ranks) - min(ranks))

                # ranks = np.array([1/(1+np.exp(-1*ind)) for ind in temp_ranks])

                # input node feature with degree

                degfeat = (np.sum(nx.adj_matrix(g).todense(), axis=1))

                x = np.reshape(np.arange(V), (V, 1))
                Idenfeat = enc.fit_transform(x).toarray()

                feat = np.concatenate((Idenfeat, degfeat), axis=1)

                # return temp_input, ranks, feat, g
                return ranks, feat, g

            for i in range(n):
                target, feature,g = get_sample(metrictype)
                # inputtensor.append(input)
                targetvec.append(target)
                featurevec.append(feature)
                graphvec.append(g)

        else:
            print("invalid arguement")
            # inputtensor = np.load(datadir + 'predictor.npy')
            # targetvec = np.load(datadir + 'target.npy')
            # featurevec = np.load(datadir + 'feature.npy')
            # graphvec = np.load(datadir + 'graphvec.npy')

        return np.array(targetvec), np.array(featurevec), graphvec

    # generate scale-free model (power law degre dist.)
    def gen_plmodel(self, n, V, metrictype, genflag=0):
        if genflag ==1:
            targetvec = []
            featurevec = []
            graphvec = []

            enc = OneHotEncoder(handle_unknown='ignore')

            def get_sample(metrictype):

                g = nx.scale_free_graph(V).to_undirected()

                ## node rank on the basis of egr/weighted spectrum
                if metrictype == 'egr':
                    ranks = self.get_egrnoderank(g)
                elif metrictype == 'weightedspectrum':
                    ranks = self.get_wghtspectnoderank(g)

                # ranks = np.array([2 if ind >= int(0.75*V) else 1 if (ind > int(0.25*V)) and (ind < int(0.75*V)) else 0 for ind in temp_ranks])
                ranks = (ranks - min(ranks)) / (max(ranks) - min(ranks))

                # ranks = np.array([1/(1+np.exp(-1*ind)) for ind in temp_ranks])

                # input node feature with degree

                degfeat = (np.sum(nx.adj_matrix(g).todense(), axis=1))

                x = np.reshape(np.arange(V), (V, 1))
                Idenfeat = enc.fit_transform(x).toarray()

                feat = np.concatenate((Idenfeat, degfeat), axis=1)

                # return temp_input, ranks, feat, g
                return ranks, feat, g

            for i in range(n):
                target, feature,g = get_sample(metrictype)
                # inputtensor.append(input)
                targetvec.append(target)
                featurevec.append(feature)
                graphvec.append(g)

        else:
            print("invalid arg")
            # inputtensor = np.load(datadir + 'predictor.npy')
            # targetvec = np.load(datadir + 'target.npy')
            # featurevec = np.load(datadir + 'feature.npy')
            # graphvec = np.load(datadir + 'graphvec.npy')

        return np.array(targetvec), np.array(featurevec), graphvec

    # generate erdos-renyi- model (preferrential arttachment)
    def gen_ermodel(self, n, V, datadir, metrictype, genflag=0):
        if genflag ==1:
            targetvec = []
            featurevec = []
            graphvec = []

            enc = OneHotEncoder(handle_unknown='ignore')

            def get_sample(metrictype):

                g = nx.erdos_renyi_graph(V,0.2)

                ## node rank on the basis of egr/weighted spectrum
                if metrictype == 'egr':
                    ranks = self.get_egrnoderank(g)
                elif metrictype == 'weightedspectrum':
                    ranks = self.get_wghtspectnoderank(g)

                # ranks = np.array([2 if ind >= int(0.75*V) else 1 if (ind > int(0.25*V)) and (ind < int(0.75*V)) else 0 for ind in temp_ranks])
                ranks = (ranks - min(ranks)) / (max(ranks) - min(ranks))

                # ranks = np.array([1/(1+np.exp(-1*ind)) for ind in temp_ranks])

                # input node feature with degree

                degfeat = (np.sum(nx.adj_matrix(g).todense(), axis=1))

                x = np.reshape(np.arange(V), (V, 1))
                Idenfeat = enc.fit_transform(x).toarray()

                feat = np.concatenate((Idenfeat, degfeat), axis=1)

                # return temp_input, ranks, feat, g
                return ranks, feat, g

            for i in range(n):
                target, feature,g = get_sample(metrictype)
                # inputtensor.append(input)
                targetvec.append(target)
                featurevec.append(feature)
                graphvec.append(g)

        else:
            # inputtensor = np.load(datadir + 'predictor.npy')
            targetvec = np.load(datadir + 'target.npy')
            featurevec = np.load(datadir + 'feature.npy')
            graphvec = np.load(datadir + 'graphvec.npy')

        return np.array(targetvec), np.array(featurevec), graphvec

    def gen_abmodel(self, n, V, datadir, predictor, genflag=0):
        if genflag ==1:
            inputtensor = []
            targetvec = []
            featurevec = []
            enc = OneHotEncoder(handle_unknown='ignore')
            def get_sample(predictor):
                g = nx.barabasi_albert_graph(V, 3)

                temp_input = nx.adj_matrix(g).todense()

                # link rank on basis of egr
                # ranks = self.get_egrlinkrank(g)
                ## node rank on the basis of egr
                ranks = self.get_egrnoderank(g)

                # ranks = np.array([2 if ind >= int(0.75*V) else 1 if (ind > int(0.25*V)) and (ind < int(0.75*V)) else 0 for ind in temp_ranks])
                ranks = (ranks - min(ranks)) / (max(ranks) - min(ranks))

                # ranks = np.array([1/(1+np.exp(-1*ind)) for ind in temp_ranks])

                # input node feature with degree

                degfeat = (np.sum(nx.adj_matrix(g).todense(), axis=1))

                x = np.reshape(np.arange(V), (V, 1))
                Idenfeat = enc.fit_transform(x).toarray()

                feat = np.concatenate((Idenfeat, degfeat), axis=1)
                return temp_input, ranks, feat

            for i in range(n):
                input, target, feature = get_sample(predictor)
                inputtensor.append(input)
                targetvec.append(target)
                featurevec.append(feature)

            np.save(datadir+'predictor.npy', inputtensor)
            np.save(datadir+'target.npy', targetvec)
            np.save(datadir+'feature.npy', featurevec)

        else:
            inputtensor = np.load(datadir + 'predictor.npy')
            targetvec = np.load(datadir + 'target.npy')
            featurevec = np.load(datadir + 'feature.npy')

        return np.array(inputtensor), np.array(targetvec), np.array(featurevec)

    def gen_graphegr_plmodel(self, n, V, datadir, predictor, genflag=0):
        if genflag ==1:
            targetvec = []
            # featurevec = []
            graphvec = []

            enc = OneHotEncoder(handle_unknown='ignore')
            def get_sample(predictor):

                g = nx.generators.random_graphs.powerlaw_cluster_graph(V, 1, 0.1)

                ranks = self.get_egrnoderank(g)

                ranks = (ranks - min(ranks)) / (max(ranks) - min(ranks))

                return ranks, g

            for i in range(n):
                target, g = get_sample(predictor)

                targetvec.append(target)

                graphvec.append(g)

            np.save(datadir+'target.npy', targetvec)

        else:

            targetvec = np.load(datadir + 'target.npy')


        return np.array(targetvec), graphvec

    def split_data(self, data, label, feature):
        trainingind = int(0.90*len(data))

        xtrain = data[0:trainingind,:]
        ytrain = label[0:trainingind,:]
        ftrain = feature[0:trainingind,:]

        xtest = data[trainingind:len(data),:]
        ytest = label[trainingind:len(data),:]
        ftest = feature[trainingind:len(data), :]

        return xtrain, ytrain, ftrain, xtest, ytest, ftest

def get_graphfromdf(edgelist, source, target):
    g = nx.from_pandas_edgelist(edgelist, source, target)
    return g

def get_graphtxt(path):
    g = nx.read_edgelist(path, create_using=nx.DiGraph(), nodetype=int)
    return g

def get_graphfeaturelabel_syn(graphtype, metrictype, graphsizelist):
    listgraph=[]
    listlabel=[]
    md = GenEgrData()

    if graphtype == 'pl':

        for graphsize in graphsizelist:
            label, feature, graphlist = md.gen_plmodel(1, graphsize, metrictype, genflag=1)
            listgraph.append(graphlist[0])
            listlabel.append(label[0, :])
            print("current loop element", graphsize)

    elif graphtype == 'plc':
        for graphsize in graphsizelist:
            label, feature, graphlist = md.gen_plclustermodel(1, graphsize, metrictype, genflag=1)
            listgraph.append(graphlist[0])
            listlabel.append(label[0, :])
            print("current loop element", graphsize)

    return listgraph, listlabel

def get_egrbatch(countnode):

    gcopy = g.copy()
    gcopy.remove_node(countnode)
    eig = nx.linalg.spectrum.laplacian_spectrum(gcopy)

    eigtemp1 = eig[eig > 5e-10]

    return np.sum(np.reciprocal(eigtemp1))

def get_graphfeaturelabel_real(filepath, metrictype):

    filepath = config.datapath + 'raw'+ fileext

    g = get_graphtxt(filepath)

    g = g.to_undirected()

    Listnodes = tqdm(list(g.nodes()))

    if metrictype == 'egr':
        metricraw = Parallel(n_jobs=4, prefer="threads")(delayed(get_egrbatch)(node) for node in Listnodes)
    elif metrictype == 'weightedspectrum':
        metricraw = Parallel(n_jobs=4, prefer="threads")(delayed(get_egrbatch)(node) for node in Listnodes)

    metricraw = metricraw * (2/(len(g.nodes)-1))

    metricraw = np.round(metricraw, 3)

    ranks = rankdata(metricraw, method='dense')

    ranks = (ranks - min(ranks)) / (max(ranks) - min(ranks))

    return g, ranks

## paralllelization for loop
#
# num = 10
#
# g = nx.scale_free_graph(1000).to_undirected()
# templist = list(g.nodes())
# Listnodes = tqdm(templist)
#
#
# ##
# temp=[]
# start = time.time()
# for i in Listnodes:
#     temp.append(get_egrbatch(i))
# end = time.time()
#
# print('{:.4f} s'.format(end-start))

##
#
# temppl =[]
# start = time.time()
# # n_jobs is the number of parallel jobs
# temppl= Parallel(n_jobs=4, prefer="threads")(delayed(get_egrbatch)(node) for node in Listnodes )
# end = time.time()
# print('{:.4f} s'.format(end-start))




##
