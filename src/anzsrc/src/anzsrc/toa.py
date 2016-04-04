from rdflib import Graph, Literal, URIRef
from anzsrc import (TOA, RDF, OWL, RDFS, SKOS, VIVO, DC,
                    ontoannot, ontoversion)


def gentoa():
    g = Graph()

    # statements about the ontology itself
    g.add((URIRef(TOA), RDF.type, OWL.Ontology))
    g.add((URIRef(TOA), RDF.type, SKOS.ConceptScheme))
    g.add((URIRef(TOA), RDFS.label, Literal(u'TOA 1993 Ontology')))
    g.add((URIRef(TOA), RDFS.comment, Literal(u'An ontology that provides classes '
                u'codes and hierarchical information about ASRC/ANZSRC '
                u'Type of Activity definitions.')))
    g.add((URIRef(TOA), DC.title, Literal(u"Australian and New Zealand Standard "
                                    u"Research Classification (ANZSRC): "
                                    u"Type of Activity.", lang=u"en")))
    ontoannot(g, TOA)
    ontoversion(g, TOA)

    # a class for TOA
    g.add((TOA.TOA, RDF.type, OWL.Class))
    g.add((TOA.TOA, RDFS.subClassOf, SKOS.Concept))
    g.add((TOA.TOA, RDFS.label, Literal(u'TOA 1993 Definition')))
    g.add((TOA.TOA, RDFS.comment, Literal(u'Instances of this class describe '
                                          u'TOA definitions')))

    # Pure basic research
    toa = TOA.term(u'PureBasicResearch')
    g.add((toa, RDF.type, TOA.TOA))
    g.add((toa, RDF.type, OWL.Thing))
    g.add((toa, RDFS.label, Literal(u'Pure basic research')))
    g.add((toa, RDFS.comment, Literal(u'Pure basic research is experimental '
                u'and theoretical work undertaken to acquire new knowledge '
                u'without looking for long term benefits other than the '
                u'advancement of knowledge.')))
    g.add((toa, SKOS.prefLabel, Literal(u'Pure basic research', lang=u"en")))
    g.add((URIRef(TOA), SKOS.hasTopConcept, toa))
    g.add((toa, SKOS.inScheme, URIRef(TOA)))
    # Strategic basic research
    toa = TOA.term(u'StrategicBasicResearch')
    g.add((toa, RDF.type, TOA.TOA))
    g.add((toa, RDF.type, OWL.Thing))
    g.add((toa, RDFS.label, Literal(u'Strategic basic research')))
    g.add((toa, RDFS.comment, Literal(u'Strategic basic research is '
                u'experimental and theoretical work undertaken to acquire new '
                u'knowledge directed into specified broad areas in the '
                u'expectation of useful discoveries. It provides the broad '
                u'base of knowledge necessary for the solution of recognised '
                u'practical problems.')))
    g.add((toa, SKOS.prefLabel, Literal(u'Strategic basic research', lang=u"en")))
    g.add((URIRef(TOA), SKOS.hasTopConcept, toa))
    g.add((toa, SKOS.inScheme, URIRef(TOA)))
    # Applied research
    toa = TOA.term(u'AppliedResearch')
    g.add((toa, RDF.type, TOA.TOA))
    g.add((toa, RDF.type, OWL.Thing))
    g.add((toa, RDFS.label, Literal(u'Applied research')))
    g.add((toa, RDFS.comment, Literal(u'Applied research is original work '
                u'undertaken primarily to acquire new knowledge with a '
                u'specific application in view. It is undertaken either to '
                u'determine possible uses for the findings of basic research '
                u'or to determine new ways of achieving some specific and '
                u'predetermined objectives.')))
    g.add((toa, SKOS.prefLabel, Literal(u'Applied research', lang=u"en")))
    g.add((URIRef(TOA), SKOS.hasTopConcept, toa))
    g.add((toa, SKOS.inScheme, URIRef(TOA)))
    # Experimental development
    toa = TOA.term(u'ExperimentalDevelopment')
    g.add((toa, RDF.type, TOA.TOA))
    g.add((toa, RDF.type, OWL.Thing))
    g.add((toa, RDFS.label, Literal(u'Experimental development')))
    g.add((toa, RDFS.comment, Literal(u'Experimental development is systematic'
                u' work, using existing knowledge gained from research or '
                u'practical experience, that is directed to producing new '
                u'materials, products or devices, to installing new processes,'
                u' systems and services, or to improving substantially those '
                u'already produced or installed.')))
    g.add((toa, SKOS.prefLabel, Literal(u'Experimental development', lang=u"en")))
    g.add((URIRef(TOA), SKOS.hasTopConcept, toa))
    g.add((toa, SKOS.inScheme, URIRef(TOA)))
    return g
