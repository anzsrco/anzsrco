import csv
from rdflib import Graph, Literal
from anzsrc import (RFCD, SKOS, RDF, OWL, RDFS, ANZSRC, DC,
                    ontoannot, ontoversion, createNode)


def genrfcd():
    '''
    generate RFCD 2008 ontology for08.owl

    for:RFCD ... top level class         broad  narrow
    for:RFCD2 ... subclass of for:RFCD    -      RFCD4
    for:RFCD4 ... subclass of for:RFCD   RFCD2   RFCD6
    for:RFCD6 ... subclass of for:RFCD   RFCD4    -

    properties:
      rdfs:label ... name
      for:code   ... code (not used yet)
      skos:narrower ... narrower
      skos:broader  ... broader
    '''
    # generate class definitions
    g = Graph()
    g.add((RFCD, RDF.type, OWL.Ontology))
    g.add((RFCD, RDF.type, SKOS.ConceptScheme))
    g.add((RFCD, RDFS.label, Literal(u'RFCD 1998 Ontology')))
    g.add((RFCD, RDFS.comment, Literal(u'An ontology that provides classes '
                                      u'codes and hierarchical information '
                                      u'about RFCD 1998 codes.')))
    g.add((RFCD, DC.title, Literal(u"Australian Standard Research "
                                   u"Classification (ASRC): "
                                   u"Research Fields, Courses and Disciplines "
                                   u"Classification", lang=u"en")))
    g.add((RFCD, DC.description, Literal(u"This classification allows both R&D"
            u" activity and other activity within the higher education sector "
            u"to be categorised."
            u"\n"
            u"The categories in the classification include recognised academic"
            u" disciplines and related major sub-fields taught at universities"
            u" or tertiary institutions, major fields of research investigated"
            u" by national research institutions and organisations, and "
            u"emerging areas of study.", lang="en")))
    ontoannot(g, RFCD)
    ontoversion(g, RFCD)

    g.add((RFCD.RFCD, RDF.type, OWL.Class))
    g.add((RFCD.RFCD, RDFS.subClassOf, SKOS.Concept))
    g.add((RFCD.RFCD, RDFS.label, Literal(u'RFCD 1998 Code')))
    g.add((RFCD.RFCD, RDFS.comment, Literal(u'Superclass for RFCD 1998 '
                                            u'codes')))

    g.add((RFCD.RFCD2, RDF.type, OWL.Class))
    g.add((RFCD.RFCD2, RDFS.subClassOf, RFCD.RFCD))
    g.add((RFCD.RFCD2, RDFS.label, Literal(u'RFCD 1998 2 digit Code')))
    g.add((RFCD.RFCD2, RDFS.comment,
           Literal(u'Class for RFCD 1998 2 digit codes')))

    g.add((RFCD.RFCD4, RDF.type, OWL.Class))
    g.add((RFCD.RFCD4, RDFS.subClassOf, RFCD.RFCD))
    g.add((RFCD.RFCD4, RDFS.label, Literal(u'RFCD 1998 4 digit Code')))
    g.add((RFCD.RFCD4, RDFS.comment,
           Literal(u'Class for RFCD 1998 4 digit codes')))

    g.add((RFCD.RFCD6, RDF.type, OWL.Class))
    g.add((RFCD.RFCD6, RDFS.subClassOf, RFCD.RFCD))
    g.add((RFCD.RFCD6, RDFS.label, Literal(u'RFCD 1998 6 digit Code')))
    g.add((RFCD.RFCD6, RDFS.comment,
           Literal(u'Class for RFCD 1998 6 digit codes')))

    # read data from csv files
    rfcdcsv = csv.reader(open('anzsrc_data/rfcd.csv'))
    next(rfcdcsv)
    next(rfcdcsv)  # skip file header

    division = {}  # collect divisions here
    discipline = {}  # collect discplines here
    for code, title in rfcdcsv:
        if len(code) == 2:
            division[int(code)] = title
        elif len(code) == 4:
            discipline[int(code)] = title

    rfcdcsv = csv.reader(open('anzsrc_data/rfcd-for08.csv'))
    for i in range(0, 5):
        next(rfcdcsv)

    subject = {}  # collect RFCD-6 codes in here
    # check if all data exists and collect objective codes
    for f98, n98, f08, n08 in rfcdcsv:
        if not f98:
            continue
        divcode = int(f98[:2])
        if divcode not in division:
            print "WARNING division %d does net exist" % divcode

        disccode = int(f98[:4])
        if disccode not in discipline:
            print "WARNING discipline %d does not exist" % disccode

        subjcode = int(f98)
        if subjcode not in subject:
            subject[subjcode] = n98
        elif subject[subjcode] != n98:
            print "WARNING subject %d %s differs from %d %s" % (subjcode,
                                        subject[subjcode], subjcode, n98)

    # All data read, print out a summary and start creating instances
    print 'RFCD 98'
    # from 12970_98.pdf: 24 divisions, 139 disciplines, 898 subjects
    print 'Divisions (24):', len(division)
    print 'Disciplines (139):', len(discipline)
    print 'Subjects (898):', len(subject)

    def createDivision(code, name):
        rfcdcode = RFCD.term(code)
        g.add((rfcdcode, RDF.type, RFCD.RFCD2))
        g.add((rfcdcode, RDF.type, OWL.Thing))
        g.add((rfcdcode, RDFS.label, Literal(unicode(name))))
        g.add((rfcdcode, ANZSRC.code, Literal(code)))

    for div in division.items():
        createDivision(u'%02d' % div[0], div[1])

    for disc in discipline.items():
        createNode(g, RFCD, RFCD.RFCD4, u'%04d' % disc[0], disc[1],
                   (u'%04d' % disc[0])[:2])

    for subj in subject.items():
        createNode(g, RFCD, RFCD.RFCD6, u'%06d' % subj[0], subj[1],
                   (u'%06d' % subj[0])[:4])

    return g
