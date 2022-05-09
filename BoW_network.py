"""
Written by Collin Hoffman

4/7/2022 as part of Dr. Gang Shao's research.

BoW_network.py
"""

import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import pandas as pd
import streamlit as st
from operator import itemgetter

#read in data
tags_df = pd.read_csv('bag_of_words(1).csv')

node_info =[]
sub_list = []
#normally to tags_df.shape[0]


#USED TO TEST CODE SEGMENTS
for i in range(0, tags_df.shape[0]):
    sub_list = []
    
    #tag name
    sub_list.append(tags_df.iloc[i, 0])
    
    #column number
    sub_list.append(int(i))
    
    #node size
    sub_list.append(int(tags_df.iloc[i, i + 1]))
    node_info.append(sub_list)



sorted_nodes = sorted(node_info, key = itemgetter(2), reverse = True)


def simple_func(): 
  #create graph as an instance of a Pyvis network
  nx_graph = Network('500px', '500px', notebook = True, heading='') #array of three particles made, index starts at 0
  st.markdown("<h1 style = 'font-size: 100px;'> </h1>")
  
  
  #create empty master and sub list
  node_info =[]
  sub_list = []
  

  #for each row, reset sub_list to empty
  for i in range(0, tags_df.shape[0]):
    sub_list = []
    
    #append characteristics such as tag name, column number, and node size to sublist
    #tag name
    sub_list.append(tags_df.iloc[i, 0])
    
    #column number
    sub_list.append(int(i))
    
    #node size
    sub_list.append(int(tags_df.iloc[i, i + 1]))
    
    #add sublist to master list, repeat for another node
    node_info.append(sub_list)
  
  #sort the node information by node size, descending
  sorted_nodes = sorted(node_info, key = itemgetter(2), reverse = True)
  
  #This works for sure
  #normally 500
  for initial in range(0, 300):
     tag = sorted_nodes[initial][0]
     node_size = sorted_nodes[initial][2]
     nx_graph.add_node(tag, tag, title = tag, size = node_size)
  
  
  #get information for nodes, including source and source location
  #normally 499
  for initial in range(0, 299):
    tag_init = sorted_nodes[initial][0]
    col_init = sorted_nodes[initial][1]
    
    #get destination and destination location, along with weight of edge
    #normally 500
    for start in range(initial + 1, 300):
        tag_value = sorted_nodes[start][0]
        col_value = sorted_nodes[start][1]
        node_weight = int(tags_df.iloc[col_init][col_value + 1])
        if node_weight != 0:
          nx_graph.add_edge(tag_init, tag_value, weight = node_weight)



  '''
  
  ####PRE-EXISTING CODE####
  
  
  
  #create nodes of size based on diagonal, with title of tag
  #normally to tags_df.shape[0]
  for i in range(0, 500):
    sizes = int(tags_df.iloc[i, i + 1])
    nx_graph.add_node(tags_df.iloc[i, 0], tags_df.iloc[i, 0], title = tags_df.iloc[i, 0], size = sizes)
    
  #get a list of the columns (tags)
  columns = tags_df.columns.values.tolist()
  
  for rows in range(0, 500):
      
    for cols in range(rows + 2, 501):
        
      #get weights from matrix location
      weights = int(tags_df.iloc[rows, cols])
      
           
      #determine tag title as destination 
      column = columns[cols]
      
      #add edge
      if weights != 0:
          nx_graph.add_edge(tags_df.iloc[rows, 0], column, weight = weights)
  
    '''
  #show the graph at the end
  nx_graph.show_buttons(filter_=["physics"])
  nx_graph.show('BoW.html')
  