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
import requests
import regex
from bs4 import BeautifulSoup as soup
from math import log

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
  nx_graph = Network(height="1000px", width = "100%", notebook = True, heading='PURR Tag Network') #array of three particles made, index starts at 0
  st.markdown("<h1 style = 'font-size: 50px;'> </h1>", unsafe_allow_html= True)
  
  
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
  for initial in range(0, 200):
          
     tag = sorted_nodes[initial][0]
     node_size = 3 * log(sorted_nodes[initial][2])
     # nx_graph.add_node(tag, tag, title = tag, size = node_size)
     
     #for each of the top 200 nodes, add search term
     
     #replace snake case with +
     tag_plus = regex.sub("_", "+", tag)
     tag_show = regex.sub("_", "_", tag)
     
     #HTML parse, get search results
     #site_raw = requests.get("https://purr.lib.purdue.edu/registry?q=" + tag_plus, verify = False)
     #site_soup = soup(site_raw.text, 'html.parser')
     #site_info = site_soup.find("p", {"class": "ml-2 mt-3"})
     #results = regex.compile("(<p class=\"ml-2 mt-3\">)\s*((Results[\s\w-]+)|(No record found\s+))(<\/p>)") #regex that finds count of results
     link = "https://purr.lib.purdue.edu/registry?q=" + tag_plus
     hyperlink = "<a href="+link+">View PURR data in :  '" + tag_show + "'""</a>"
     
     nx_graph.add_node(tag, tag, font_size= 300, title = hyperlink, size = node_size)
  
  #get information for nodes, including source and source location
  #normally 499
  for initial in range(0, 199):
    tag_init = sorted_nodes[initial][0]
    col_init = sorted_nodes[initial][1]
    
    #get destination and destination location, along with weight of edge
    #normally 500
    for start in range(initial + 1, 200):
        tag_value = sorted_nodes[start][0]
        col_value = sorted_nodes[start][1]
        node_weight = int(tags_df.iloc[col_init][col_value + 1])
        if node_weight != 0:
          nx_graph.add_edge(tag_init, tag_value, weight = 1)#node_weight)



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
  #turn off the physics option
  nx_graph.barnes_hut(gravity = -36000, central_gravity = 0, spring_length = 200, spring_strength = 0.04)
  nx_graph.show('BoW.html')
  