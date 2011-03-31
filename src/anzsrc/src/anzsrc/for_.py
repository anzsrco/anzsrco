import csv
from rdflib import Graph, Literal
from anzsrc import (FOR, RFCD, FOR08, VIVO, RDF, OWL, RDFS, SKOS, ANZSRC,
                    ontoannot, add_matchingproperties)


def genfor():
    """
    generate base FOR ontology. for.owl

    This ontology combines RFCD and FOR and defines their relations
    """
    g = Graph()
    g.add((FOR, RDF.type, OWL.Ontology))
    g.add((FOR, RDFS.label, Literal(u'FOR Ontology')))
    g.add((FOR, RDFS.comment, Literal(u'An ontology that provides some base '
                                      u'definitions for RFCD 1998 and '
                                      u'FOR 2008 ontologies.')))
    ontoannot(g, FOR)

    g.add((FOR.FOR, RDF.type, OWL.Class))
    g.add((FOR.FOR, RDFS.label, Literal(u'FOR code')))
    g.add((FOR.FOR, RDFS.comment, Literal(u'Superclass for FOR codes')))
    g.add((FOR.FOR, RDFS.subClassOf, SKOS.Concept))

    g.add((FOR08.FOR, RDFS.subClassOf, FOR.FOR))
    g.add((RFCD.RFCD, RDFS.subClassOf, FOR.FOR))

    add_matchingproperties(g)

    genformatches(g)

    return g


def genformatches(g):
    """
    generate equivalency relations for RFCD <-> FOR.
    """
    forcsv = csv.reader(open('anzsrc_data/rfcd-for08.csv'))
    for i in range(0, 5):
        forcsv.next()

    for f98, n98, f08, n08 in forcsv:
        if not f98 or not f08:
            continue
        for98code = RFCD.term(f98)
        if f08.endswith('p'):
            # rfcd code is covered partially by for
            for08code = FOR08.term(f08[:-1])
            g.add((for98code, ANZSRC.partialMatch, for08code))
        else:
            # rfcd code is covered fully by for
            for08code = FOR08.term(f08)
            g.add((for98code, ANZSRC.fullMatch, for08code))

    forcsv = csv.reader(open('anzsrc_data/for08-rfcd.csv'))
    for i in range(0, 5):
        forcsv.next()

    # narrow match is being used as partial match.
    # TODO: consider defining a partial match property
    for f08, n08, f98, n98 in forcsv:
        if not f98 or not f08:
            continue
        for08code = FOR08.term(f08)
        if f98.endswith('p'):
            # for code is covered partially by rfcd
            for98code = RFCD.term(f98[:-1])
            g.add((for08code, ANZSRC.partialMatch, for98code))
        else:
            # for code is covered fully by rfcd
            for98code = RFCD.term(f98)
            g.add((for08code, ANZSRC.fullMatch, for98code))

    return g
