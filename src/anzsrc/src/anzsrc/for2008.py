import csv
from rdflib import Graph, Literal
from anzsrc import (FOR08, SKOS, RDF, OWL, RDFS, XSD, ANZSRC, DC,
                    ontoannot, createNode, ontoversion)


def genfor08():
    '''
    generate FOR 2008 ontology for08.owl

    for:FOR ... top level class       broad narrow
    for:FOR2 ... subclass of for:FOR   -      FOR4
    for:FOR4 ... subclass of for:FOR   FOR2   FOR6
    for:FOR6 ... subclass of for:FOR   FOR4    -

    properties:
      rdfs:label ... name
      for:code   ... code (not used yet)
      skos:narrower ... narrower
      skos:broader  ... broader
    '''
    g = Graph()
    g.add((FOR08, RDF.type, OWL.Ontology))
    g.add((FOR08, RDF.type, SKOS.ConceptScheme))
    g.add((FOR08, RDFS.label, Literal(u'FOR 2008 Ontology')))
    g.add((FOR08, RDFS.comment, Literal(u'An ontology that provides classes '
                                      u'codes and hierarchical information '
                                      u'about FOR 2008 codes.')))
    g.add((FOR08, DC.title, Literal(u"Australian and New Zealand Standard "
                                    u"Research Classification (ANZSRC): "
                                    u"Fields of Research.", lang=u"en")))
    g.add((FOR08, DC.description, Literal(u"The ANZSRC FOR allows R&D activity"
            u" to be categorised according to the methodology used in the R&D,"
            u" rather than the activity of the unit performing the R&D or the "
            u"purpose of the R&D."
            u"\n"
            u"The categories in the classification include major fields and "
            u"related sub-fields of research and emerging areas of study "
            u"investigated by businesses, universities, tertiary institutions,"
            u" national research institutions and other organisations."
            u"\n"
            u"This classification allows the categorisation of fields of "
            u"research activity within Australia and New Zealand.",
                                          lang=u"en")))
    ontoannot(g, FOR08)
    ontoversion(g, FOR08)

    g.add((FOR08.FOR, RDF.type, OWL.Class))
    g.add((FOR08.FOR, RDFS.subClassOf, SKOS.Concept))
    g.add((FOR08.FOR, RDFS.label, Literal(u'FOR 2008 Code')))
    g.add((FOR08.FOR, RDFS.comment,
           Literal(u'Superclass for FOR 2008 codes')))

    g.add((FOR08.FOR2, RDF.type, OWL.Class))

    g.add((FOR08.FOR2, RDFS.subClassOf, FOR08.FOR))
    g.add((FOR08.FOR2, RDFS.label, Literal(u'FOR 2008 2 digit Code')))
    g.add((FOR08.FOR2, RDFS.comment,
           Literal(u'Class for FOR 2008 2 digit codes')))

    g.add((FOR08.FOR4, RDF.type, OWL.Class))
    g.add((FOR08.FOR4, RDFS.subClassOf, FOR08.FOR))
    g.add((FOR08.FOR4, RDFS.label, Literal(u'FOR 2008 4 digit Code')))
    g.add((FOR08.FOR4, RDFS.comment,
           Literal(u'Class for FOR 2008 4 digit codes')))

    g.add((FOR08.FOR6, RDF.type, OWL.Class))
    g.add((FOR08.FOR6, RDFS.subClassOf, FOR08.FOR))
    g.add((FOR08.FOR6, RDFS.label, Literal(u'FOR 2008 6 digit Code')))
    g.add((FOR08.FOR6, RDFS.comment,
           Literal(u'Class for FOR 2008 6 digit codes')))

    # create property definition to hold code
    g.add((FOR08.code, RDF.type, OWL.DatatypeProperty))
    g.add((FOR08.code, RDFS.domain, FOR08.FOR))
    g.add((FOR08.code, RDFS.range, XSD.string))

    for98csv = csv.reader(open('anzsrc_data/for08.csv'))
    for98csv.next()

    division = {}
    group = {}
    field = {}

    for div, gr, fi, code in for98csv:
        divcode = int(code[:2])
        if divcode not in division:
            division[divcode] = div
        elif division[divcode] != div:
            print "WARNING division"

        grcode = int(code[:4])
        if grcode not in group:
            group[grcode] = gr
        elif group[grcode] != gr:
            print "WARNING group"

        ficode = int(code)
        if ficode not in field:
            field[ficode] = fi
        elif field[ficode] != fi:
            print "WARNING objective"

    # checkagainst mapping:
    for98csv = csv.reader(open('anzsrc_data/for08-rfcd.csv'))
    for98csv.next()
    for98csv.next()
    for98csv.next()
    for98csv.next()
    for98csv.next()
    for row in for98csv:
        try:
            if int(row[0]) not in field:
                print 'WARNING: missing code ', row
        except ValueError:
            continue

    print 'FOR'
    print 'Divisions (22):', len(division)
    print 'Groups (157):', len(group)
    print 'Field (1238):', len(field)

    for div in division.items():
        createNode(g, FOR08, FOR08.FOR2, '%02d' % div[0], div[1], None)

    for gr in group.items():
        createNode(g, FOR08, FOR08.FOR4, '%04d' % gr[0], gr[1],
                   ('%04d' % gr[0])[:2])

    for fi in field.items():
        createNode(g, FOR08, FOR08.FOR6, '%06d' % fi[0], fi[1],
                   ('%06d' % fi[0])[:4])

    return g
