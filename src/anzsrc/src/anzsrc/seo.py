import csv
from rdflib import Graph, Literal
from anzsrc import (SEO, SEO98, SEO08, RDF, OWL, RDFS, VIVO, SKOS, ANZSRC,
                    ontoannot, add_matchingproperties)


def genseo():
    """
    generate base SEO ontology. seo.owl

    this ontology combines SEO08 and SEO98 and defines their relations

    TODO: add owl:versionInfo
    """
    g = Graph()
    g.add((SEO, RDF.type, OWL.Ontology))
    g.add((SEO, RDFS.label, Literal(u'SEO Ontology')))
    g.add((SEO, RDFS.comment, Literal(u'An ontology that provides some base '
                                     u'definitions for SEO 1998 and SEO 2008 '
                                     u'ontologies.')))
    ontoannot(g, SEO)

    g.add((SEO.SEO, RDF.type, OWL.Class))
    g.add((SEO.SEO, RDFS.label, Literal(u'SEO Code')))
    g.add((SEO.SEO, RDFS.comment,
           Literal(u'Superclass for SEO codes')))
    g.add((SEO.SEO, RDFS.subClassOf, SKOS.Concept))

    g.add((SEO98.SEO, RDFS.subClassOf, SEO.SEO))
    g.add((SEO08.SEO, RDFS.subClassOf, SEO.SEO))

    add_matchingproperties(g)

    genseomatches(g)
    return g


def genseomatches(g):
    """
    generate equivalency relations for SEO98 <-> SEO08.
    """
    seo98csv = csv.reader(open('anzsrc_data/seo98-seo08.csv'))
    for i in range(0, 5):
        seo98csv.next()

    for s98, n98, s08, n98 in seo98csv:
        if not s98 or not s08:
            continue
        seo98code = SEO98.term(s98)
        if s08.endswith('p'):
            # SEO98 is covered partially by SEO08
            seo08code = SEO08.term(s08[:-1])
            g.add((seo98code, ANZSRC.partialMatch, seo08code))
        else:
            # SEO98 is covered fully by SEO8
            seo08code = SEO08.term(s08)
            g.add((seo98code, ANZSRC.fullMatch, seo08code))

    seo08csv = csv.reader(open('anzsrc_data/seo08-seo98.csv'))
    for i in range(0, 5):
        seo08csv.next()

    for s08, n08, s98, n08 in seo08csv:
        if not s08 or not s98:
            continue
        seo08code = SEO08.term(s08)
        if s98.endswith('p'):
            # SEO08 is covered partially by SEO98
            seo98code = SEO98.term(s98[:-1])
            g.add((seo08code, ANZSRC.partialMatch, seo98code))
        else:
            # SEO08 is covered fully by SEO98
            seo98code = SEO98.term(s98)
            g.add((seo08code, ANZSRC.fullMatch, seo98code))

    return g
