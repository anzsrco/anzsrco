# cd /Users/gerhard/Documents/Projects/Uni/workspace_eif/Kepler-Vitro/test
# ../../ANDS-Vitro-SVN-root/ontology/trunk/bin/xslt rifcs2rdf.xslt testdata.xml  | xml fo

import sys
from lxml import etree
from datetime import datetime, tzinfo, timedelta
from time import strptime
try:
    from hashlib import md5
except ImportError:
    from md5 import md5

ZERO = timedelta(0)


# A UTC class.

class UTC(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "Z"

    def dst(self, dt):
        return ZERO

utc = UTC()

# A class capturing the platform's idea of local time.

import time as _time

STDOFFSET = timedelta(seconds=-_time.timezone)
if _time.daylight:
    DSTOFFSET = timedelta(seconds=-_time.altzone)
else:
    DSTOFFSET = STDOFFSET

DSTDIFF = DSTOFFSET - STDOFFSET


class LocalTimezone(tzinfo):

    def utcoffset(self, dt):
        if self._isdst(dt):
            return DSTOFFSET
        else:
            return STDOFFSET

    def dst(self, dt):
        if self._isdst(dt):
            return DSTDIFF
        else:
            return ZERO

    def tzname(self, dt):
        return _time.tzname[self._isdst(dt)]

    def _isdst(self, dt):
        tt = (dt.year, dt.month, dt.day,
              dt.hour, dt.minute, dt.second,
              dt.weekday(), 0, -1)
        stamp = _time.mktime(tt)
        tt = _time.localtime(stamp)
        return tt.tm_isdst > 0

Local = LocalTimezone()


def md5Hex(context, input_):
    # print context, input_
    # print dir(input_)
    if isinstance(input_, basestring):
        text = input_
    else:
        text = input_[0].text
    return md5(text).hexdigest()

funcns = etree.FunctionNamespace('org.apache.commons.codec.digest.DigestUtils')
funcns['md5Hex'] = md5Hex


def formatUTCDate(context, input_):
    '''
    parse iso full datetime if necessary and output it
    corrected to Z time zone.
    '''
    if isinstance(input_, basestring):
        text = input_
    else:
        text = input_[0].text
    if text is not None and text.endswith('Z'):
        return text
    if text is None:
        dt = datetime.now()
    else:
        dt = datetime(*(strptime(text, '%Y-%m-%dT%H:%M:%S')[0:6]))
    dt = dt.replace(tzinfo=LocalTimezone()).astimezone(UTC())
    return dt.strftime('%Y-%m-%dT%H:%M:%S%Z')


def formatPhone(context, input_):
    if isinstance(input_, basestring):
        text = input_
    else:
        text = input_[0].text
    if text.startswith(u'3735'):
        text = u'+61 7 %s' % text
    elif text.startswith(u'373 5'):
        text = u'+61 7 3735 %s' % text[5:]
    elif text.startswith(u'373'):
        text = u'+61 7 %s' % text
    elif text.startswith(u'3382'):
        text = u'+61 7 %s' % text
    elif text.startswith(u'338'):
        text = u'+61 7 %s' % text
    elif text.startswith(u'5552'):
        text = u'+61 7 %s' % text
    elif text.startswith(u'555'):
        text = u'+61 7 %s' % text
    elif text.startswith(u'07'):
        text = u'+61 7 %s' % text[2:]
    elif text.startswith(u'3875'):
        text = u'+61 7 3735' % text[4:]
    elif text.startswith(u'07 3875'):
        text = u'+61 7 3735 %s' % text[7:]
    trans = {ord(u'/'): None,
             ord(u'+'): None,
             ord(u' '): u'-'}
    return u'tel:%s' % text.replace(u'  ', u' ').translate(trans)


def formatEmail(context, input_):
    if isinstance(input_, basestring):
        text = input_
    else:
        text = input_[0].text
    return u'email:%s' % text


def escapeURI(context, input_):
    # maybe should check all of these characters.
    # they are additional reserved
    # characters in the update URI - RFC. (the older one used to defin
    # xsd:anyURI is superseded by this one).
    # '#', '!', "'", "(", ")", "*",
    if isinstance(input_, basestring):
        text = input_
    else:
        text = input_[0].text
    return text.replace(u"'", u'%27')

xextns = etree.FunctionNamespace('au.edu.guqut.XSLTExtensions')
xextns['formatPhone'] = formatPhone
xextns['formatEmail'] = formatEmail
xextns['formatUTCDate'] = formatUTCDate
xextns['escapeURI'] = escapeURI


def main():
    xslfn = sys.argv[1]
    xmlfn = sys.argv[2]
    if xmlfn == '-':
        xmlfn = sys.stdin
    xslt_doc = etree.parse(xslfn)
    xslt = etree.XSLT(xslt_doc)
    doc = etree.parse(xmlfn)
    try:
        result = xslt(doc)
        print str(result)
    except etree.XSLTError, ex:
        print "XSLT Error:"
        print ex.error_log
        raise ex

if __name__ == "__main__":
    main()
