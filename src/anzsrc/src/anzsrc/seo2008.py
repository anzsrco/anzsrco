import csv
from rdflib import Graph, Literal
from anzsrc import (SEO08, SKOS, RDF, OWL, RDFS,
                    ontoannot, createNode, add_anzsrc_code_prop)

######################################################
# Static data not reflected in csv files
######################################################
sector = {u'A': u'Defence',
          u'B': u'Economic Development',
          u'C': u'Society',
          u'D': u'Environment',
          u'E': u'Expanding knowledge'}
code2sector = {81: u'A',
               82: u'B', 83: u'B', 84: u'B', 85: u'B', 86: u'B', 87: u'B',
               88: u'B', 89: u'B', 90: u'B', 91: u'B',
               92: u'C', 93: u'C', 94: u'C', 95: u'C',
               96: u'D',
               97: u'E'}


def genseo08():
    """
    generate SEO 2008 ontology. seo08.owl
    """
    g = Graph()
    g.add((SEO08, RDF.type, OWL.Ontology))
    g.add((SEO08, RDFS.label, Literal(u'SEO 2008 Ontology')))
    g.add((SEO08, RDFS.comment, Literal(u'An ontology that provides classes '
                                        u'codes and hierarchical information '
                                        u'about SEO 2008 codes.')))
    g.add((SEO08, DC.title, Literal(u"Australian and New Zealand Standard "
                                    u"Research Classification (ANZSRC): "
                                    u"Socio-Economic Objective.", lang=u"en")))
    g.add((SEO08, DC.description, Literal(u"The ANZSRC SEO classification "
            u"allows R&D activity in Australia and New Zealand to be "
            u"categorised according to the intended purpose or outcome of the "
            u"research, rather than the processes or techniques used in order "
            u"to achieve this objective."
            u"\n"
            u"The purpose categories include processes, products, health, "
            u"education and other social and environmental aspects in "
            u"Australia and New Zealand that R&D activity aims to improve.",
                                          lang=u"en")))
    ontoannot(g, SEO08)

    g.add((SEO08.SEO, RDF.type, OWL.Class))
    g.add((SEO08.SEO, RDFS.subClassOf, SKOS.Concept))
    g.add((SEO08.SEO, RDFS.label, Literal(u'SEO 2008 Code')))
    g.add((SEO08.SEO, RDFS.comment, Literal(u'Superclass for SEO 2008 codes')))

    g.add((SEO08.SEOSection, RDF.type, OWL.Class))
    g.add((SEO08.SEOSection, RDFS.subClassOf, SEO08.SEO))
    g.add((SEO08.SEOSection, RDFS.label, Literal(u'SEO 2008 Section Code')))
    g.add((SEO08.SEOSection, RDFS.comment,
           Literal(u'Class for SEO 2008 Section codes')))

    g.add((SEO08.SEO2, RDF.type, OWL.Class))
    g.add((SEO08.SEO2, RDFS.subClassOf, SEO08.SEO))
    g.add((SEO08.SEO2, RDFS.label, Literal(u'SEO 2008 2 digit Code')))
    g.add((SEO08.SEO2, RDFS.comment,
           Literal(u'Class for SEO 2008 2 digit codes')))

    g.add((SEO08.SEO4, RDF.type, OWL.Class))
    g.add((SEO08.SEO4, RDFS.subClassOf, SEO08.SEO))
    g.add((SEO08.SEO4, RDFS.label, Literal(u'SEO 2008 4 digit Code')))
    g.add((SEO08.SEO4, RDFS.comment,
           Literal(u'Class for SEO 2008 4 digit codes')))

    g.add((SEO08.SEO6, RDF.type, OWL.Class))
    g.add((SEO08.SEO6, RDFS.subClassOf, SEO08.SEO))
    g.add((SEO08.SEO6, RDFS.label, Literal(u'SEO 2008 6 digit Code')))
    g.add((SEO08.SEO6, RDFS.comment,
           Literal(u'Class for SEO 2008 6 digit codes')))

    add_anzsrc_code_prop(g)

    seo98csv = csv.reader(open('anzsrc_data/seo08.csv'))
    seo98csv.next()

    division = {}
    group = {}
    objective = {}

    for sec, div, gr, obj, code in seo98csv:
        divcode = int(code[:2])
        if divcode not in division:
            division[divcode] = div
        elif division[divcode] != div:
            print "WARNING division %d does not exist" % divcode

        grcode = int(code[:4])
        if grcode not in group:
            group[grcode] = gr
        elif group[grcode] != gr:
            print "WARNING group %d does not exist" % grcode

        obcode = int(code)
        if obcode not in objective:
            objective[obcode] = obj
        elif objective[obcode] != obj:
            print "WARNING objective %d %s differs from %d %s" % (obcode,
                                            objective[obcode], obcode, obj)

    print 'SEO 08'
    print 'Sectors (5):', len(sector)
    print 'Divisions (17):', len(division)
    print 'Groups (119):', len(group)
    print 'Objective (847):', len(objective)

    # checkagainst mapping:
    seo98csv = csv.reader(open('anzsrc_data/seo08-seo98.csv'))
    for i in range(0, 5):
        seo98csv.next()
    for row in seo98csv:
        try:
            if int(row[0]) not in objective:
                print 'WARNING: missing code ', row
        except ValueError:
            continue

    for sec in sector.items():
        createNode(g, SEO08, SEO08.SEOSection, sec[0], sec[1], None)

    for div in division.items():
        createNode(g, SEO08, SEO08.SEO2, u'%02d' % div[0], div[1],
                   code2sector[div[0]])

    for gr in group.items():
        createNode(g, SEO08, SEO08.SEO4, u'%04d' % gr[0], gr[1],
                   (u'%04d' % gr[0])[:2])

    for obj in objective.items():
        createNode(g, SEO08, SEO08.SEO6, u'%06d' % obj[0], obj[1],
                   (u'%06d' % obj[0])[:4])

    return g
