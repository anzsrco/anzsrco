import sys
from rdflib import Graph


def loadOntology(name):
    g = Graph()
    if name.endswith('n3'):
        g.load(name, format='n3')
    else:
        g.load(name)
    return g


def rdfppmain():
    g = loadOntology(sys.argv[1])
    g.serialize(sys.stdout, encoding='UTF-8')
