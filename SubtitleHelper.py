# -*- coding: utf-8 -*- 

import urllib
import unicodedata

def log(module, msg):
    print (u"### [%s] - %s" % (module, msg,)).encode('utf-8')
    
    
def normalizeString(str):
    return unicodedata.normalize(
        'NFKD', unicode(unicode(str, 'utf-8'))
    ).encode('ascii', 'ignore')
