from collections import Counter

import networkx as nx

from database.DAO import DAO

class Model:
    def __init__(self):
        self._brands = []
        self._years = []
        self._nodes = []
        self._edges = []
        self._graph = nx.Graph()
        self._idMap = {}


    def getBrands(self):
        self._brands = DAO.getBrands()
        return self._brands

    def getYears(self):
        self._years = DAO.getYears()
        return self._years

    def getNodes(self, brand):
        self._nodes = DAO.getNodes(brand)
        return self._nodes

    def getEdges(self, brand, year):
        self._edges = DAO.getEdges(brand, year)
        return self._edges

    def addAllEdges(self, brand, year):
        self.getEdges(brand, year)
        for e in self._edges:
            if e.prod1 in self._idMap and e.prod2 in self._idMap:
                u = self._idMap[e.prod1]
                v = self._idMap[e.prod2]
                self._graph.add_edge(u, v, weight=e.peso)

    def buildGraph(self, year, brand):
        self._nodes = []
        self._edges = []
        self._idMap = {}
        self._graph.clear()
        self._nodes = DAO.getNodes(brand)
        for node in self._nodes:
            self._idMap[node.Product_number] = node
        self._graph.add_nodes_from(self._nodes)
        self.addAllEdges(brand, year)
        return self._graph

    def getGraphDetails(self):
        nNodes = self._graph.number_of_nodes()
        nEdges = self._graph.number_of_edges()
        return nNodes, nEdges

    def bestNodes(self):
        edges_list = list(self._graph.edges(data=True))
        top3 = edges_list[:3]
        return top3

    def getRipetuti(self):
        top3 = self.bestNodes()
        nodi = []
        ripetuti = []
        for e in top3:
            nodi.append(e[0])
            nodi.append(e[1])

        count = Counter(nodi)
        for node, count in count.items():
            if count > 1:
                ripetuti.append(node)
        return ripetuti