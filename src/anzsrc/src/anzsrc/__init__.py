from datetime import date
from rdflib import Namespace, Literal, URIRef, Graph

ANZSRC = Namespace(u'http://purl.org/asc/1297.0/')
ANZSRCVIVO = Namespace("http://purl.org/asc/1297.0/vivo.rdf")

SEO = Namespace(u'http://purl.org/asc/1297.0/seo/')
SEO08 = Namespace(u'http://purl.org/asc/1297.0/2008/seo/')
SEO98 = Namespace(u'http://purl.org/asc/1297.0/1998/seo/')
FOR = Namespace(u'http://purl.org/asc/1297.0/for/')
FOR08 = Namespace(u'http://purl.org/asc/1297.0/2008/for/')
RFCD = Namespace(u'http://purl.org/asc/1297.0/1998/rfcd/')
TOA = Namespace(u'http://purl.org/asc/1297.0/1993/toa/')

OWL = Namespace(u'http://www.w3.org/2002/07/owl#')
RDF = Namespace(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
VIVO = Namespace(u'http://vivoweb.org/ontology/core#')
RDFS = Namespace(u'http://www.w3.org/2000/01/rdf-schema#')
SKOS = Namespace(u'http://www.w3.org/2004/02/skos/core#')
DC = Namespace(u'http://purl.org/dc/elements/1.1/')
CC = Namespace(u'http://creativecommons.org/ns#')
XSD = Namespace(u'http://www.w3.org/2001/XMLSchema#')

CC3AU = URIRef(u'http://creativecommons.org/licenses/by-nc/3.0/au/')
ABSANZSRC08 = URIRef(u"http://www.abs.gov.au/AUSSTATS/abs@.nsf/"
                     u"allprimarymainfeatures/"
                     u"5D99AEA1DD8AA8E0CA2574180005421C")
ABSANZSRC = URIRef(u'http://www.abs.gov.au/ausstats/abs@.nsf/mf/1297.0')


def ontoversion(g, ns):
    # dcterms:hasVersion ponits to another version of the same thing.
    # owl:versionInfo is an annotation property. (might be used to describe
    # changes)
    g.add((ns, OWL.versionInfo, ns.term(u'0.2')))
    g.add((ns, OWL.priorVersion, ns.term(u'0.1')))
    # g.add((ns, DCTERMS.hasVersion, ns + u'/0.2'))
    # duplicate the node ns with correct versioned URI
    for (s, p, o) in g.triples((ns, None, None)):
        g.add((ns.term(u'0.2'), p, o))


def ontoannot(g, ns):
    """
    add dc annotations to ontology.
    """
    g.add((ns, DC.creator, Literal(u'Griffith University')))
    g.add((ns, DC.creator, Literal(u'University of Southern Queensland')))
    g.add((ns, DC.date, Literal(date.today().isoformat())))
    g.add((ns, DC.source, ABSANZSRC08))
    g.add((ns, RDFS.seeAlso, ABSANZSRC))
    g.add((ns, DC.rights, Literal(u'The source data is published by the '
                                  u'Australian Bureau of Statistics, and '
                                  u'can be found at the following address: '
                                  u'http://www.abs.gov.au/ausstats/abs@.nsf/0/'
                                  u'4AE1B46AE2048A28CA25741800044242 . This '
                                  u'document is published under the Creative '
                                  u'Commons Attribution License 3.0 '
                                  u'Australia.')))
    g.add((ns, CC.license, CC3AU))
    g.add((ns, CC.morePermissions, ABSANZSRC))


def createNode(g, ns, class_, code, name, broader):
    codeuri = ns.term(code)
    g.add((codeuri, RDF.type, OWL.Thing))
    g.add((codeuri, RDF.type, class_))
    if broader is not None:
        g.add((codeuri, SKOS.broader, ns.term(broader)))
        g.add((ns.term(broader), SKOS.narrower, codeuri))
    else:
        g.add((ns, SKOS.hasTopConcept, codeuri))
    g.add((codeuri, RDFS.label, Literal(name.decode('utf-8'))))
    g.add((codeuri, ANZSRC.code, Literal(code)))
    g.add((codeuri, SKOS.inScheme, ns))
    g.add((codeuri, SKOS.prefLabel, Literal(name.decode('utf-8'), lang=u"en")))


def setnamespaceprefixes(g):
    g.namespace_manager.bind('seo', SEO)
    g.namespace_manager.bind('seo08', SEO08)
    g.namespace_manager.bind('seo98', SEO98)
    g.namespace_manager.bind('for', FOR)
    g.namespace_manager.bind('for08', FOR08)
    g.namespace_manager.bind('rfcd', RFCD)
    g.namespace_manager.bind('toa', TOA)
    g.namespace_manager.bind('owl', OWL)
    g.namespace_manager.bind('vivo', VIVO)
    g.namespace_manager.bind('skos', SKOS)
    g.namespace_manager.bind('dc', DC)
    g.namespace_manager.bind('cc', CC)
    g.namespace_manager.bind('xsd', XSD)
    g.namespace_manager.bind('anzsrc', ANZSRC)


def genanzsrc():
    g = Graph()

    g.add((ANZSRC, RDF.type, OWL.Ontology))
    g.add((ANZSRC, RDFS.label, Literal(u'ANZSRC Base Ontology')))
    g.add((ANZSRC, RDFS.comment,
           Literal(u'An ontology that provides some base definitions for '
                   u'commonly used by all FOR, RFCD, SEO, etc. '
                   u'ontologies.')))

    ontoannot(g, ANZSRC)
    ontoversion(g, ANZSRC)

    g.add((ANZSRC.ANZSRC, RDF.type, OWL.Class))
    g.add((ANZSRC.ANZSRC, RDFS.label, Literal(u'ANZSRC code')))
    g.add((ANZSRC.ANZSRC, RDFS.comment,
           Literal(u'Superclass for ANZSRC codes')))
    g.add((ANZSRC.ANZSRC, RDFS.subClassOf, SKOS.Concept))

    g.add((FOR.FOR, RDFS.subClassOf, ANZSRC.ANZSRC))
    g.add((SEO.SEO, RDFS.subClassOf, ANZSRC.ANZSRC))
    g.add((TOA.TOA, RDFS.subClassOf, ANZSRC.ANZSRC))

    add_matchingproperties(g)

    return g


def add_matchingproperties(g):
    # these properties don't describe any hierarchical or symmetric relation
    g.add((ANZSRC.partialMatch, RDF.type, OWL.ObjectProperty))
    g.add((ANZSRC.partialMatch, RDFS.subPropertyOf, SKOS.relatedMatch))
    g.add((ANZSRC.partialMatch, RDFS.comment,
           Literal(u'The subject concept is partially covered by the object.')))
    g.add((ANZSRC.fullMatch, RDF.type, OWL.ObjectProperty))
    g.add((ANZSRC.fullMatch, RDFS.subPropertyOf, SKOS.relatedMatch))
    g.add((ANZSRC.fullMatch, RDFS.comment,
           Literal(u'The subject concept is fully covered by the object.')))


def addvivo(g):
    """
    add vivo specific triples.
    """
    g.add((ANZSRC.ANZSRC, RDFS.subClassOf, VIVO.SubjectArea))

    return g
