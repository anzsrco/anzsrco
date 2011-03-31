import csv
from rdflib import Graph, Literal
from anzsrc import (SEO98, SKOS, RDF, OWL, RDFS, ANZSRC,
                    ontoannot, createNode, add_anzsrc_code_prop)

######################################################
# Static data not reflected in csv files
######################################################

# top level division codes
division = {u'1': u'Defence',
            u'2': u'Economic Development',
            u'3': u'Society',
            u'4': u'Environment',
            u'5': u'Non-Oriented Research'}

# map subdivision to divisions
code2division = {61: u'1',
                 62: u'2', 63: u'2', 64: u'2', 65: u'2', 66: u'2', 67: u'2',
                 68: u'2', 69: u'2', 70: u'2', 71: u'2', 72: u'2',
                 73: u'3', 74: u'3', 75: u'3',
                 76: u'4', 77: u'4',
                 78: u'5'}


def genseo98():
    """
    generate SEO 1998 ontology. seo98.owl
    """
    g = Graph()
    g.add((SEO98, RDF.type, OWL.Ontology))
    g.add((SEO98, RDFS.label, Literal(u'SEO 1998 Ontology')))
    g.add((SEO98, RDFS.comment, Literal(u'An ontology that provides classes '
                                        u'codes and hierarchical information '
                                        u'about SEO 1998 codes.')))
    ontoannot(g, SEO98)

    g.add((SEO98.SEO, RDF.type, OWL.Class))
    g.add((SEO98.SEO, RDFS.subClassOf, SKOS.Concept))
    g.add((SEO98.SEO, RDFS.label, Literal(u'SEO 1998 Code')))
    g.add((SEO98.SEO, RDFS.comment,
           Literal(u'Superclass for SEO 1998 codes')))

    g.add((SEO98.SEODivision, RDF.type, OWL.Class))
    g.add((SEO98.SEODivision, RDFS.subClassOf, SEO98.SEO))
    g.add((SEO98.SEODivision, RDFS.label, Literal(u'SEO 1998 Division Code')))
    g.add((SEO98.SEODivision, RDFS.comment,
           Literal(u'Class for SEO 1998 Division codes')))

    g.add((SEO98.SEO2, RDF.type, OWL.Class))
    g.add((SEO98.SEO2, RDFS.subClassOf, SEO98.SEO))
    g.add((SEO98.SEO2, RDFS.label, Literal(u'SEO 1998 2 digit Code')))
    g.add((SEO98.SEO2, RDFS.comment,
           Literal(u'Class for SEO 1998 2 digit codes')))

    g.add((SEO98.SEO4, RDF.type, OWL.Class))
    g.add((SEO98.SEO4, RDFS.subClassOf, SEO98.SEO))
    g.add((SEO98.SEO4, RDFS.label, Literal(u'SEO 1998 4 digit Code')))
    g.add((SEO98.SEO4, RDFS.comment,
           Literal(u'Class for SEO 1998 4 digit codes')))

    g.add((SEO98.SEO6, RDF.type, OWL.Class))
    g.add((SEO98.SEO6, RDFS.subClassOf, SEO98.SEO))
    g.add((SEO98.SEO6, RDFS.label, Literal(u'SEO 1998 6 digit Code')))
    g.add((SEO98.SEO6, RDFS.comment,
           Literal(u'Class for SEO 1998 6 digit codes')))

    add_anzsrc_code_prop(g)

    # read data from csv files
    seo98csv = csv.reader(open('anzsrc_data/seo98.csv'))
    seo98csv.next()
    seo98csv.next()

    subdivision = {}  # collect subdivision codes
    group = {}  # collect group codes

    for code, title in seo98csv:
        if len(code) == 2:
            subdivision[int(code)] = title
        if len(code) == 4:
            group[int(code)] = title

    seo98csv = csv.reader(open('anzsrc_data/seo98-seo08.csv'))
    for i in range(0, 5):
        seo98csv.next()

    objective = {}  # collect SEO-6 codes in here

    # check if all data exists and collect objective codes
    for s98, n98, s08, n08 in seo98csv:
        if not s98:
            continue
        subdivcode = int(s98[:2])
        if subdivcode not in subdivision:
            print "WARNING division %d does net exist" % subdivcode

        grcode = int(s98[:4])
        if grcode not in group:
            print "WARNING group %d does not exist" % grcode

        obcode = int(s98)
        if obcode not in objective:
            objective[obcode] = n98
        elif objective[obcode] != n98:
            print "WARNING objective %d %s differs from %d %s" % (obcode,
                                            objective[obcode], obcode, n98)

    # print summary and build instances
    print 'SEO 98'
    # from seo98.pdf: 5 divisions, 18 subdivisions, 107 groups and 594 classes
    print 'Divisions (5):', len(division)
    print 'Subdivisions (18): ', len(subdivision)
    print 'Groups (107):', len(group)
    print 'Objective (594):', len(objective)

    for div in division.items():
        createNode(g, SEO98, SEO98.SEODivision, div[0], div[1], None)

    for div in subdivision.items():
        createNode(g, SEO98, SEO98.SEO2, u'%02d' % div[0], div[1],
                   code2division[div[0]])

    for gr in group.items():
        createNode(g, SEO98, SEO98.SEO4, u'%04d' % gr[0], gr[1],
                   (u'%04d' % gr[0])[:2])

    for obj in objective.items():
        createNode(g, SEO98, SEO98.SEO6, u'%06d' % obj[0], obj[1],
                   (u'%06d' % obj[0])[:4])

    return g
