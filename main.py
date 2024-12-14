import random
import numpy as np
import pandas as pd # draw arrow
import networkx as nx
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import  ImageTk,Image

class Node:
    def __init__(self, value, color): #constructor
        self.__value = value #parametre
        self.__color = color

    def get_value(self):
        return self.__value #value

    def get_color(self):
        return self.__color # değerleri tutuyo

    def set_color(self, color):
        self.__color = color


class Graph:
    def __init__(self, available_colors=None):
        self.__nodemap = {} #dictionary
        self.__graph = {} #depolamak için

        if available_colors is None:
            r = Tk() # renk seçtirme ekranı
            self.__available_colors = [] #list

            check_var = [] #list

            checkVar1 = IntVar() #verileri depoladık
            checkVar2 = IntVar()
            checkVar3 = IntVar()
            checkVar4 = IntVar()
            checkVar5 = IntVar()
            checkVar6 = IntVar()
            checkVar7 = IntVar()
            checkVar8 = IntVar()

            def done():
                label = Label(r, text="first things first (Believer Lyrics)").pack()

            C1 = Checkbutton(r, text="red", variable=checkVar1, onvalue=1, offvalue=0, height=5, width=20).pack()
            C2 = Checkbutton(r, text="blue", variable=checkVar2, onvalue=1, offvalue=0, height=5, width=20).pack()
            C3 = Checkbutton(r, text="gray", variable=checkVar3, onvalue=1, offvalue=0, height=5, width=20).pack()
            C4 = Checkbutton(r, text="pink", variable=checkVar4, onvalue=1, offvalue=0, height=5, width=20).pack()
            C5 = Checkbutton(r, text="orange", variable=checkVar5, onvalue=1, offvalue=0, height=5, width=20).pack()
            C6 = Checkbutton(r, text="yellow", variable=checkVar6, onvalue=1, offvalue=0, height=5, width=20).pack()
            C7 = Checkbutton(r, text="cyan", variable=checkVar7, onvalue=1, offvalue=0, height=5, width=20).pack()
            C8 = Checkbutton(r, text="purple", variable=checkVar8, onvalue=1, offvalue=0, height=5, width=20).pack()

            btn = Button(r, text='submit', command=lambda:[done(), r.destroy()]).pack()

            r.mainloop()
            check_var.append(checkVar1.get()) #verileri ekledik
            check_var.append(checkVar2.get())
            check_var.append(checkVar3.get())
            check_var.append(checkVar4.get())
            check_var.append(checkVar5.get())
            check_var.append(checkVar6.get())
            check_var.append(checkVar7.get())
            check_var.append(checkVar8.get())

            if check_var[0]: #indeksinden check ettik
                self.__available_colors.append('red')
            if check_var[1]:
                self.__available_colors.append('blue')
            if check_var[2]:
                self.__available_colors.append('gray')
            if check_var[3]:
                self.__available_colors.append('pink')
            if check_var[4]:
                self.__available_colors.append('orange')
            if check_var[5]:
                self.__available_colors.append('yellow')
            if check_var[6]:
                self.__available_colors.append('cyan')
            if check_var[7]:
                self.__available_colors.append('purple')

        else:
            self.__available_colors = available_colors

        self.__selected_colors = []

    def add_undirected_edge(self, u, v): #bi node dan bi noda gitme yolu
        if u not in self.__nodemap:
            u_node = Node(u, None)
            self.__nodemap[u] = u_node

        if v not in self.__nodemap:
            v_node = Node(v, None)
            self.__nodemap[v] = v_node

        if len(self.__graph.keys()) == 0:
            start_node_color = random.choice(list(self.__available_colors)) #random bir şekilde available colors listten appendliyoruz
            self.__selected_colors.append(start_node_color)
            self.__nodemap[u].set_color(start_node_color)

        if u in self.__graph:
            self.__graph[u].append(v)
        else:
            self.__graph[u] = [v]

        if v in self.__graph:
            self.__graph[v].append(u)
        else:
            self.__graph[v] = [u]

    def __get_adjacent_vertices(self, node):
        return self.__graph[node]

    def color(self):
        for parent_node in list(self.__graph.keys()):
            parent_color = self.__nodemap[parent_node].get_color()

            neighbour_colors = []
            for neighbour_node in self.__get_adjacent_vertices(parent_node):
                neighbour_colors.append(self.__nodemap[neighbour_node].get_color())

            if parent_color is None:
                unique_neighbour_colors = [x for x in neighbour_colors if x is not None]
                non_chosen_colors = set(self.__selected_colors) - set(unique_neighbour_colors)

                if len(non_chosen_colors) == 0:
                    non_selected_new_color = random.choice(list(set(self.__available_colors) - set(neighbour_colors)))
                    self.__nodemap[parent_node].set_color(non_selected_new_color)
                    self.__selected_colors.append(non_selected_new_color)
                else:
                    self.__nodemap[parent_node].set_color(random.choice(list(non_chosen_colors)))

            print(self.__nodemap[parent_node].get_value(), self.__nodemap[parent_node].get_color(), "->",
                  neighbour_colors)

        for node in self.__nodemap:
            print(self.__nodemap[node].get_value(), self.__nodemap[node].get_color())

    def visualize_w_color(self):
        self.color()

        ordered_nodes = list(self.__nodemap.keys())
        n_node = len(ordered_nodes)
        adj_matrix = np.zeros((n_node, n_node))
        for node in self.__graph:
            for neighbour in self.__graph[node]:
                adj_matrix[ordered_nodes.index(node), ordered_nodes.index(neighbour)] = 1

        adj_df = pd.DataFrame(adj_matrix, index=ordered_nodes, columns=ordered_nodes)

        G = nx.from_pandas_adjacency(adj_df)
        node_colormap = []
        for node in G:
            node_colormap.append(self.__nodemap[node].get_color())
        nx.draw(G, node_color=node_colormap, with_labels=True)
        plt.show()  #draw the graph


if __name__ == "__main__":
    graph = Graph()
    r = Tk() #realiton input ekranı
    amount = IntVar()
    a = 0
    def function():
        global a #fonksiyonun içinde sabit kalmalı
        z = amount.get()
        a=z
        lb1 = Label(r, text="The amount is " + str(z), font=('calibre', 10, 'normal'))
        lb1.pack()

    amount_label = Label(r, text="Enter the wished amount of relations: ", font=('calibre', 10, 'bold'))
    amount_label.pack()
    amount_entry = Entry(r, textvariable=amount, font=('calibre', 10, 'normal'))
    amount_entry.pack()
    sub_btn = Button(r, text='submit', command=lambda:[function(), r.destroy()])
    sub_btn.pack()

    r.mainloop()
    """i = 0
    while (i < a):
        x = input("Enter the first city")
        y = input("Enter the second city")
        graph.add_undirected_edge(x, y)
        i = i + 1
    graph.visualize_w_color()"""
    r = Tk()
    cities1_entries = []
    cities2_entries = []
    def citiesPrint():
        i = 0
        while(i<a):
            x = cities1_entries[i].get()
            y = cities2_entries[i].get()
            graph.add_undirected_edge(x, y)
            i = i + 1
        j = 0
        relation_list = ''
        while(j<a):
            relation_list = relation_list + cities1_entries[j].get() + " -> " + cities2_entries[j].get() + '\n' #döngüyle kullanıcıdan şehirleri aldık
            relation_label.config(text=relation_list)
            j = j + 1

    for x in range(a):
        cities1_entry = Entry(r)
        cities1_entry.grid(row=0, column=x,pady=20, padx=5)
        cities1_entries.append(cities1_entry)

        cities2_entry = Entry(r)
        cities2_entry.grid(row=1, column=x, pady=20, padx=5)
        cities2_entries.append(cities2_entry)

    my_button = Button(r, text="Enter", command=citiesPrint)
    my_button.grid(row=2, column=0, pady=20)

    relation_label = Label(r, text='')
    relation_label.grid(row=3, column=0, pady=20)

    r.mainloop()
    graph.visualize_w_color()

