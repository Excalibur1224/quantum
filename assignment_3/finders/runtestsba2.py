# some imports 
import numpy as np 
import networkx as nx
import copy 
from itertools import product
from collections import Counter
import matplotlib.pyplot as plt
import random
#D-Wave Ocean SDK related
import dimod 
from dwave.system import DWaveSampler
from dwave.samplers import SimulatedAnnealingSampler
# from dwave.cloud import Client
# client = Client.from_config()
from dwave.embedding import embed_ising, unembed_sampleset
from minorminer import find_embedding


seed = 1224
random.seed(seed)

def assignWeights(graph):
    assigned_graph = {e:int(np.random.choice([-1,+1])) for e in graph.edges}
    return assigned_graph

def create_regular(n):
    return nx.random_regular_graph(d=3, n=n, seed=seed)
def create_square(n):
    return nx.grid_2d_graph(n=n, m=n)
def create_er(n):
    return nx.erdos_renyi_graph(n=n, p=0.5, seed=seed)
def create_full(n):
    return nx.complete_graph(n=n)
def create_ba1(n):
    return nx.barabasi_albert_graph(n=n, m=1, seed=seed)
def create_ba2(n):
    return nx.barabasi_albert_graph(n=n, m=2, seed=seed)

qpu_sampler = DWaveSampler(solver="Advantage_system4")

def assign_embed(graph, solver):
    embedding = find_embedding(list(graph.keys()), solver.edgelist, random_seed=seed)
    return embedding

def find_max_size(last_jump, failed_embed, create_graph):

    for i in range((failed_embed-last_jump)+100, failed_embed, 100):
        print("currently on: ",i)
        temp_graph = create_graph(i)
        weighted = assignWeights(temp_graph)
        embed = assign_embed(weighted, qpu_sampler)
        if not embed:
            print("embed fails at ",i)
            last_jump = 100
            failed_embed = i
            break;

    for i in range((failed_embed-last_jump)+10, failed_embed, 10):
        print("currently on: ",i)
        temp_graph = create_graph(i)
        weighted = assignWeights(temp_graph)
        embed = assign_embed(weighted, qpu_sampler)
        if not embed:
            print("embed fails at ",i)
            last_jump = 10
            failed_embed = i
            break;

    for i in range((failed_embed-last_jump)+1, failed_embed, 1):
        print("currently on: ",i)
        temp_graph = create_graph(i)
        weighted = assignWeights(temp_graph)
        embed = assign_embed(weighted, qpu_sampler)
        if not embed:
            print("embed fails at ",i)
            failed_embed = i
            break;

    for i in range(0, 6):
        print("currently on: ",i)
        temp_graph = create_graph(failed_embed)
        weighted = assignWeights(temp_graph)
        embed = assign_embed(weighted, qpu_sampler)
        if not embed:
            print("embed fails at ",i)
        else:
            print('embed succeeded')

find_max_size(500, 1100, create_ba2)
