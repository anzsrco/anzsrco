from rdflib import Graph, URIRef
from anzsrc import seo, seo1998, seo2008, for_, rfcd, for2008, toa, ontoannot
from anzsrc import setnamespaceprefixes, addvivo, genanzsrc, ANZSRCVIVO
from anzsrc import SEO, SEO08, SEO98, FOR, FOR08, RFCD, TOA, ANZSRC
import os

OUTPUT_DIR = "anzsrc_output"


def genoutput(gengraph, fname, base):
    g = gengraph()
    setnamespaceprefixes(g)
    f = open(OUTPUT_DIR + "/" + fname + '.rdf', 'w')
    g.serialize(f, format='xml')
    f.close()
    f = open(OUTPUT_DIR + "/" + fname + '.n3', 'w')
    g.serialize(f, format='n3')
    f.close()


def main():
    # check if output dir exists
    d = os.path.abspath(OUTPUT_DIR)
    if not os.path.exists(d):
        os.makedirs(OUTPUT_DIR)

    genoutput(seo.genseo, 'seo', SEO)

    genoutput(seo1998.genseo98, 'seo98', SEO98)

    genoutput(seo2008.genseo08, 'seo08', SEO08)

    genoutput(for_.genfor, 'for', FOR)

    genoutput(rfcd.genrfcd, 'rfcd', RFCD)

    genoutput(for2008.genfor08, 'for08', FOR08)

    genoutput(toa.gentoa, 'toa', TOA)

    genoutput(genanzsrc, 'anzsrc', ANZSRC)

    g = Graph()
    setnamespaceprefixes(g)
    fref = URIRef(ANZSRCVIVO)
    ontoannot(g, fref)
    addvivo(g)
    f = open(OUTPUT_DIR + '/anzsrc_vivo.rdf', 'w')
    g.serialize(f)
    f.close()
