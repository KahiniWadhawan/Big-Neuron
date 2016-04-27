#------------------------------------------------------------------------
#Author: Kahini Wadhawan
#------------------------------------------------------------------------

# NetworkX code for reading in edgelist, calculations on networks,
# adding attributes to nodes, reducing network size in principled way
# saving to json (and reading in json if you want to add to your json graph)

import networkx as nx    # using 1.6, from http://networkx.lanl.gov/
from networkx.readwrite import json_graph
from operator import itemgetter
import json
import community   # lib from http://perso.crans.org/aynaud/communities/
import matplotlib.pyplot as plt  #-- only needed for a single graph below in draw_partition
from matplotlib.backends.backend_pdf import PdfPages
import os

# Global vars
configs = json.loads(open('user_info.json','r').read())
path = 'temp/'
inputjsonfile = 'new_json.json'
smalloutputjsonfile = 'small_graph.json'
bigoutputjsonfile = 'big_graph.json'
edgesfile = 'data.edgelist'
node_id = str(configs['user_id'])
small_graph_size = configs['size']

pg = PdfPages('temp/partition.pdf')

def read_in_edges(filename, info=True):
    # a directed graph by default.  Change this if you want undirected.
    # Edgelist looks like:
    # node1 node2
    # node3 node1
    # node1 node3
    # ...
    g_orig = nx.read_edgelist(filename, create_using=nx.DiGraph())
    if info:
        print "Read in edgelist file ", filename
        print nx.info(g_orig)
    return g_orig

def save_to_jsonfile(filename, graph):
    g = graph
    g_json = json_graph.node_link_data(g) # node-link format to serialize
    json.dump(g_json, open(filename,'w'))

def read_json_file(filename, info=True):
    graph = json_graph.load(open(filename))
    if info:
        print "Read in file ", filename
        print nx.info(graph)
    return graph

def report_node_data(graph, node=""):
    g = graph
    if len(node) == 0:
        print "Found these sample attributes on the nodes:"
        print g.nodes(data=True)[0]
    else:
        print "Values for node " + node
        print [d for n,d in g.nodes_iter(data=True) if n==node]

def calculate_degree(graph):
    print "Calculating degree..."
    g = graph
    deg = nx.degree(g)
    nx.set_node_attributes(g,'degree',deg)
    return g, deg

def calculate_indegree(graph):
    # will only work on DiGraph (directed graph)
    print "Calculating indegree..."
    g = graph
    indeg = g.in_degree()
    nx.set_node_attributes(g, 'indegree', indeg)
    return g, indeg

def calculate_outdegree(graph):
    # will only work on DiGraph (directed graph)
    print "Calculating outdegree..."
    g = graph
    outdeg = g.out_degree()
    nx.set_node_attributes(g, 'outdegree', outdeg)
    return g, outdeg

def calculate_betweenness(graph):
    print "Calculating betweenness..."
    g = graph
    bc=nx.betweenness_centrality(g)
    nx.set_node_attributes(g,'betweenness',bc)
    return g, bc

def calculate_eigenvector_centrality(graph):
    print "Calculating Eigenvector Centrality..."
    g = graph
    ec = nx.eigenvector_centrality(g)
    nx.set_node_attributes(g,'eigen_cent',ec)
    #ec_sorted = sorted(ec.items(), key=itemgetter(1), reverse=True)
    # color=nx.get_node_attributes(G,'betweenness')  (returns a dict keyed by node ids)
    return g, ec

def calculate_degree_centrality(graph):
    print "Calculating Degree Centrality..."
    g = graph
    dc = nx.degree_centrality(g)
    nx.set_node_attributes(g,'degree_cent',dc)
    degcent_sorted = sorted(dc.items(), key=itemgetter(1), reverse=True)
    for key,value in degcent_sorted[0:10]:
        print "Highest degree Centrality:", key, value

    return graph, dc

def find_cliques(graph):
    # returns cliques as sorted list
    g = graph
    cl = nx.find_cliques(g)
    cl = sorted(list( cl ), key=len, reverse=True)
    print "Number of cliques:", len(cl)
    cl_sizes = [len(c) for c in cl]
    print "Size of cliques:", cl_sizes
    return cl

def find_partition(graph):
    # code and lib from http://perso.crans.org/aynaud/communities/
    # must be an undirected graph
    # returns partition which is dict
    g = graph
    partition = community.best_partition( g )
    print "Partitions found values: ", len(partition.values())
    print "Partitions found: ", len(set(partition.values()))
    # to show members of each partition:
    #for i in set(partition.values()):
        #members = [nodes for nodes in partition.keys() if partition[nodes] == i]
        #for member in members:
            #print member, i
    #print "Partition for centre node user input in: ", partition[node_id]
    nx.set_node_attributes(g,'partition',partition)
    return g, partition

def draw_partition(graph, partition):
    # requires matplotlib.pyplot, uncomment above
    # uses community code and sample from http://perso.crans.org/aynaud/communities/ to draw matplotlib graph in shades of gray
    g = graph
    count = 0
    size = float(len(set(partition.values())))
    pos = nx.spring_layout(g)
    for com in set(partition.values()):
        count = count + 1
        list_nodes = [nodes for nodes in partition.keys()
                                    if partition[nodes] == com]
        nx.draw_networkx_nodes(g, pos, list_nodes, node_size = 20,
                                    node_color = str(count / size))
    nx.draw_networkx_edges(g,pos, alpha=0.5)
    #plt.show()
    plt.savefig(pg, format='pdf')
    pg.close()


def trim_nodes_by_attribute_for_remaining_number(graph, attributelist, count):
    # e.g., remove first 1000 from 1644 nodes by low eigenvector_centrality -- assumes it's sorted in reverse order!
    g = graph
    to_remove = len(graph.nodes()) - count - 1
    g.remove_nodes_from([x[0] for x in attributelist[0:to_remove]])
    print "Now graph has node count: ", len(g.nodes())
    return g

def trim_nodes_by_attribute_value(graph, attributedict, threshold):
    g = graph
    g.remove_nodes_from([k for k,v in attributedict.iteritems() if v <= threshold])
    return g

def write_node_attributes(graph, attributes):
    # utility function to let you print the node + various attributes in a csv format
    if type(attributes) is not list:
        attributes = [attributes]
    for node in graph.nodes():
        vals = [str(dict[node]) for dict in [nx.get_node_attributes(graph,x) for x in attributes]]
        print node, ",", ",".join(vals)

def write_forcedirected_d3_json(graph,partition):
    # function to write json for force directed graph d3 visualization
    json_dict = {'nodes':[],'links':[]}
    array_pos = {}
    g_nodes = graph.nodes()
    #print('size nodes & parition :: ',graph.number_of_nodes(),len(partition))

    #inserting nodes into json
    for i in range(len(g_nodes)):
        node_temp_dict = {}
        nodeid = g_nodes[i]
        node_temp_dict['name'] = nodeid
        #print('node temp dict :: ',node_temp_dict,partition.values()[i])
        node_temp_dict['group'] = partition.values()[i]
        node_temp_dict['id'] = nodeid
        #append node temp dict to nodes list
        json_dict['nodes'].append(node_temp_dict)
        array_pos[nodeid] = i

    #inserting links into json
    g_edges = graph.edges()
    for edge_tup in g_edges:
        link_temp_dict = {}
        link_temp_dict['source'] = array_pos[edge_tup[0]]
        link_temp_dict['target'] = array_pos[edge_tup[1]]
        link_temp_dict['value']  = 1
        #print('links data :: ', array_pos[edge_tup[0]],array_pos[edge_tup[1]])
        #append link temp dict to links list
        json_dict['links'].append(link_temp_dict)


    network_json=json.dumps(json_dict)
    #print network_json
    #write json to file
    file_path = os.path.join('temp/network.json')  #revisit - to put politician name
    write_tofile(file_path,network_json)

def write_tofile(file_path,text):
    fp = open(file_path,'wb')
    fp.write(text)
    fp.close()



def run_analysis():
    g = read_in_edges(path+edgesfile) # my func will create a Digraph from node pairs.
    #g = read_json_file(path + inputjsonfile)

    g, deg = calculate_degree(g)
    g, indeg = calculate_indegree(g)
    g, outdeg = calculate_outdegree(g)
    # Taking forever, need to investigate
    # g, bet = calculate_betweenness(g)
    g, eigen = calculate_eigenvector_centrality(g)
    g, degcent = calculate_degree_centrality(g)

    print('no. of nodes & edges in g:: ',g.number_of_nodes(),g.number_of_edges())
    #print('edges :: ',g.edges())
    #print('nodes ::', g.nodes())

    # verify that the graph's nodes are carrying the attributes:
    #report_node_data(g, node=node_id)

    # to print out values for a scatterplot, for example:
    #write_node_attributes(g, "betweenness", "eigen_cent")

    # to do community partitions, must have undirected graph.
    undir_g = g.to_undirected()
    # Examine partitioning algo and potentially tweak.
    undir_g, part = find_partition(undir_g)  # uses the community lib included about, linked from NetworkX site
    #draw_partition(undir_g, part)   # draws a matplotlib graph in grays

    #mine
    write_forcedirected_d3_json(g,part)
    # show that the partition info is added to the nodes:
    #report_node_data(undir_g, node=node_id)

    # reduce what you send to Javascript --
    # trim what's saved to js file by taking only N nodes, with top values of a certain attribute...
    eigen_sorted = sorted(eigen.items(), key=itemgetter(1), reverse=True)
    for key, val in eigen_sorted[0:5]:
        print "highest eigenvector centrality nodes:", key, val
    # for trimming, you want it reverse sorted, with low values on top.
    eigen_sorted = sorted(eigen.items(), key=itemgetter(1), reverse=False)

    small_graph = trim_nodes_by_attribute_for_remaining_number(undir_g, eigen_sorted, small_graph_size)

    # print nx.info(small_graph)

    # # to do community partitions, must have undirected graph.
    # undir_small_g = small_graph.to_undirected()
    # # Examine partitioning algo and potentially tweak.
    # undir_small_g, part1 = find_partition(undir_small_g)  # uses the community lib included about, linked from NetworkX site
    # #draw_partition(undir_g, part1)   # draws a matplotlib graph in grays
    #
    # #mine
    # write_forcedirected_d3_json(small_graph,part)

    #save as json for use in javascript - small graph, and full graph if you want
    save_to_jsonfile(path+smalloutputjsonfile, small_graph)
    print "Saved small graph to new file: ", path+smalloutputjsonfile
    save_to_jsonfile(path+bigoutputjsonfile, undir_g)
    print "Saved big graph to new file: ", path+bigoutputjsonfile

if __name__ == '__main__':
    run_analysis()
