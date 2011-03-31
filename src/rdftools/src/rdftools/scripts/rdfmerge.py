import sys
from rdflib import Graph
from rdflib.graph import ReadOnlyGraphAggregate


def loadOntology(name):
    g = Graph()
    if name.endswith('n3'):
        g.load(name, format='n3')
    else:
        g.load(name)
    return g


def main():
    grlist = []
    for fn in sys.argv[1:]:
        grlist.append(loadOntology(fn))
    gc = ReadOnlyGraphAggregate(grlist)

    gc.serialize(sys.stdout, encoding='UTF-8')
