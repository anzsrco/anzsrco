import sys
from rdflib import Graph, Namespace, BNode, URIRef

OWL = Namespace('http://www.w3.org/2002/07/owl#')
RDF = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
ANDS = Namespace('http://www.ands.org.au/ontologies/ns/0.1/VITRO-ANDS.owl')
VIVO = Namespace('http://vivoweb.org/ontology/core')
BIBO = Namespace('http://purl.org/ontology/bibo/')
DC = Namespace('http://purl.org/dc/elements/1.1/')
DCT = Namespace('http://purl.org/dc/terms/')
DCAM = Namespace('http://purl.org/dc/dcam/')
DCTYPES = Namespace('http://purl.org/dc/dcmitype/')
EVENT = Namespace('http://purl.org/NET/c4dm/event.owl')
GEOPOL = Namespace('http://aims.fao.org/aos/geopolitical.owl')
SKOS = Namespace('http://www.w3.org/2004/02/skos/core')
FOAF = Namespace('http://xmlns.com/foaf/0.1/')
VITRO = Namespace('http://vitro.mannlib.cornell.edu/ns/vitro/0.7')

skos = './ontologies/skos.rdf'
geopol = './ontologies/geopolitical.owl'
bibio = './ontologies/bibo.owl'
foaf = './ontologies/foaf.rdf'
dc = './ontologies/dcelements.rdf'
dct = './ontologies/dcterms.rdf'
event = './ontologies/event.n3'
vitro = './ontologies/vitro.owl'
vivo = './orig-ontologies/vivo-core-1.0d.owl'
ands = './orig-ontologies/ANDS-VITRO.owl'


def loadOntology(name):
    g = Graph()
    if name.endswith('n3'):
        g.load(name, format='n3')
    else:
        g.load(name)
    return g


def splitgraph(g1, g2):
    '''
    g1 has triples which are in g2, we want to get rid of them.

    returns:
        a graph with all the removed triples.
    '''
    gr = Graph()
    for t in g1:
        # iterate over all triples.
        if t in g2:
            gr.add(t)
    return gr


def removeBNodeObjects(g1, obj, ns):
    '''
    recursively remove anonymous nodes.
    but keep BNodes which do use ns as subject or predicate
    '''
    r = []
    toremove = [obj]
    for t in g1.triples((obj, None, None)):
        if ns in t[1] or ns in t[2]:
            toremove = []
            break
        # not sure here, but recursion should currently not be in use.
        if isinstance(t[2], BNode):
            r.extend(removeBNodeObjects(g1, t[2]))
    r.extend(toremove)
    return r


def removeForeignObjects(g1, ns):
    '''
    remove triples about resources in foreign namespace....
    returns:
        all removed triples, which might go into separate xml file.
    '''
    gr = Graph()
    for t in g1:
        if hasattr(t[0], 'defrag'):
            if ns != t[0].defrag():
                # remov bnodes if not referenced by ns
                if isinstance(t[2], BNode):
                    for bn in removeBNodeObjects(g1, t[2], ns):
                        for bt in g1.triples((bn, None, None)):
                            g1.remove(bt)
                            gr.add(bt)
                # remove only if there is no ref to ns
                elif ns in t[1] or ns in t[2]:
                    continue
                # remove....
                gr.add(t)
                g1.remove(t)

        # else:
        #     print t
    return gr


def removePropertiesFromNS(g1, ns):
    '''
    filter out properties from specific ns
    (used to extract vitro specific configuration statements)
    returns:
        all triples with properties from ns
    '''
    gr = Graph()
    for t in g1:
        if ns == t[1].defrag():
            gr.add(t)
            g1.remove(t)
    return gr


def vivosep():
    g1 = Graph()
    g2 = Graph()
    # g1.parse would be an alternative (new way to do it)
    g1.load(vivo)  # load vivo
    g2.load(foaf)  # load foaf
    g2.load(skos)  # load skos
    g2.load(geopol)
    g2.load(bibio)
    g2.load(dc)
    g2.load(dct)
    g2.load(vitro)
    g2.load(event, format='n3')
    splitgraph(g1, g2)  # filter out duplicates
    foreign = removeForeignObjects(g1, VIVO)
    vitroconfig = removePropertiesFromNS(g1, VITRO)
    # clean up remainder

    # remove statements which type dcelements and dcterms as ontology
    # TODO: maybe this goes into extensions?
    g1.remove((DC, RDF.type, OWL.Ontology))
    g1.remove((DCT, RDF.type, OWL.Ontology))

    # add import statements to g1
    g1.add((VIVO, OWL.imports, BIBO))
    g1.add((VIVO, OWL.imports, EVENT))
    g1.add((VIVO, OWL.imports, DC))
    g1.add((VIVO, OWL.imports, DCT))
    g1.add((VIVO, OWL.imports, DCAM))
    g1.add((VIVO, OWL.imports, DCTYPES))
    g1.add((VIVO, OWL.imports, FOAF))
    g1.add((VIVO, OWL.imports, GEOPOL))
    g1.add((VIVO, OWL.imports, SKOS))

    #write to file
    f = open('vivo.owl', 'w')
    g1.serialize(f)
    f.close()
    f = open('vivo-extensions.rdf', 'w')
    foreign.serialize(f)
    f.close()
    f = open('vivo-vitro.rdf', 'w')
    vitroconfig.serialize(f)
    f.close()


def andssep():
    g1 = Graph()
    g2 = Graph()
    # g1.parse would be an alternative (new way to do it)
    g1.load(ands)
    g2.load(vivo)  # load vivo
    g2.load(foaf)  # load foaf
    g2.load(skos)  # load skos
    g2.load(geopol)
    g2.load(bibio)
    g2.load(dc)
    g2.load(dct)
    g2.load(vitro)
    g2.load(event, format='n3')
    splitgraph(g1, g2)  # filter out duplicates
    foreign = removeForeignObjects(g1, ANDS)
    vitroconfig = removePropertiesFromNS(g1, VITRO)
    # clean up remainder

    # remove statements which type dcelements and dcterms as ontology
    # TODO: maybe this goes into extensions?
    g1.remove((DC, RDF.type, OWL.Ontology))
    g1.remove((DCT, RDF.type, OWL.Ontology))

    # add import statements to g1
    g1.add((VIVO, OWL.imports, VIVO))

    #write to file
    f = open('ands.owl', 'w')
    g1.serialize(f)
    f.close()
    f = open('ands-extensions.rdf', 'w')
    foreign.serialize(f)
    f.close()
    f = open('ands-vitro.rdf', 'w')
    vitroconfig.serialize(f)
    f.close()


def removeBNodes(g):
    for s, p, o in g:
        if BNode in (type(s), type(o)):
            g.remove((s, p, o))
    return g


def main():
    if sys.argv[1] == 'vivo':
        vivosep()
    elif sys.argv[1] == 'ands':
        andssep()
    else:
        g1 = loadOntology(sys.argv[1])
        g2 = loadOntology(sys.argv[2])
        g1 -= g2
        #removeBNodes(g1)
        f = open('rest.n3', 'w')
        g1.serialize(f, format='n3')
        f.close()


if __name__ == "__main__":
    main()
