#!/usr/bin/env python

import os
import sys
import random
import time
sys.path.insert(0, "../dynamodb/")
from bitstore import *
from collection import *
from resource import *
from sources import *
from targets import *
from collection_src_tgt import *
import itertools

users = [
          {'uid': 'foo', 'name' : 'Foo', 'type': 'fa-user'},
          {'uid': 'bar', 'name' : 'Bar', 'type': 'fa-user'},
          {'uid': 'goo', 'name' : 'Goo', 'type': 'fa-user'},
          {'uid': 'gopa', 'name' : 'Gopa Kumar', 'type': 'fa-user'},
        ]

rsrcs = Resource()
rsrcs.create()

srcs = Sources()
srcs.create()

tgts = Targets()
tgts.create()

for user in users:
    print 'USER SOURCES: %s----------------------------\n' % user['uid']
    data = srcs.get(user['uid'])
    for d in data:
        print 'QUERY: data source %s, description %s, icon %s, act %s\n' % \
              (d['g_uid'], 
               d['SourceDescription'], 
               d['SourceIcon'], d['SourceAccount'])

    print 'USER TARGETS: %s----------------------------\n' % user['uid']
    data = tgts.get(user['uid'])
    for d in data:
        for d in data:
            print 'QUERY: data target %s, description %s, icon %s, act %s\n' % \
                  (d['g_uid'], 
                   d['TargetDescription'], 
                   d['TargetIcon'], d['TargetAccount'])   
   
    print 'USER RESOURCES: %s----------------------------\n' % user['uid']
    rsrc = rsrcs.get(user['uid'], None, None)
    for r in rsrc:
        print 'cltnid %s, uid %s, description %s, rsrcid %s\n' % \
              (r['g_rsrc_collectionid'], r['g_uid'], r['description'],
               r['ResourceId'])
    print '\n\n'

