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
import subprocess

def add_resource(user, collection, picfile, picuid, tags):
    global cltns
    global rsrcs

    thumbuid  = picuid + "_thumb";   
    thumbfile = "/tmp/" + picuid + "_thumb.gif" 
    thumbcmd = "convert " +  picfile + " -auto-orient -thumbnail 310x165 -unsharp 0x.5 " +  thumbfile
    p = subprocess.Popen(thumbcmd, shell=True, stderr=subprocess.PIPE)
    while True:
        out = p.stderr.read(1)
        if out == '' and p.poll() != None:
            break
        if out != '':
            sys.stdout.write(out)
            sys.stdout.flush()

    (uuid, url)       = bits.put(picfile, picuid)
    (uuid, thumb_url) = bits.put(thumbfile, thumbuid)

    description = "%s's collection %s" % (user['uid'], collection)
    cltns.put(user['uid'], collection, description)
    description = "image %s" % picfile
    rsrcs.put(user['uid'], collection, description, picuid ,url, url, thumb_url, 'image', tags)

word_file = "/usr/share/dict/words"
WORDS = open(word_file).read().splitlines()

userpics = '/home/ubuntu/photostore/pics/'
picsbase = '/home/ubuntu/pics/'
users = [
          {'uid': 'foo', 'name' : 'Foo', 'type': 'fa-user'},
          {'uid': 'bar', 'name' : 'Bar', 'type': 'fa-user'},
          {'uid': 'goo', 'name' : 'Goo', 'type': 'fa-user'},
          {'uid': 'gopa', 'name' : 'Gopa Kumar', 'type': 'fa-user'},
        ]
alldirs = []

if len(sys.argv) >= 2:
    delete = int(sys.argv[1])
else:
    delete = 0

# First delete existing tables, then create new
bits = BitStore()
if delete:
    bits.delete()
bits.create()

cltns = Collection()
if delete:
    cltns.delete()
cltns.create()

rsrcs = Resource()
if delete:
    rsrcs.delete()
rsrcs.create()

srcs = Sources()
if delete:
    srcs.delete()
srcs.create()

tgts = Targets()
if delete:
    tgts.delete()
tgts.create()

srctgt = CollectionSrcTgt()
if delete:
    srctgt.delete()
srctgt.create()

time.sleep(30)

usertuples=itertools.combinations(users, 2)           
for ua, ub in usertuples:
    srcs.put(ua['uid'], ub['uid'], ub['name'], ub['type'])
    tgts.put(ua['uid'], ub['uid'], ub['name'], ub['type'])
    srcs.put(ub['uid'], ua['uid'], ua['name'], ua['type'])
    tgts.put(ub['uid'], ua['uid'], ua['name'], ua['type'])

for user in users:
    os.system('mkdir %s' % userpics+user['uid'])
    numcltn = random.randint(1, 10)
    for i in range(1,numcltn):
        os.system('mkdir %s' % userpics+user['uid']+"/"+str(i))

for user in users:
    uid = user['uid']
    userpic = userpics + uid
    usercltn = os.listdir(userpic)
    for c in usercltn:
        alldirs.append(userpics+user['uid']+"/"+c)

allpics = os.listdir(picsbase)
for a in allpics:
    d = random.choice(alldirs)
    os.system('cp %s %s' % (picsbase+a, d))

for user in users:
    uid = user['uid']
    cdir = userpics + uid + "/"
    cltndirs = os.listdir(cdir)
    for c in cltndirs:
        picdir = cdir + c + "/"
        pics = os.listdir(picdir)
        for p in pics:
            picfile = picdir + p
            picuid = os.path.splitext(p)[0]
            word1 = random.choice(WORDS)
            word2 = random.choice(WORDS)
            word3 = random.choice(WORDS)
            word4 = random.choice(WORDS)
            tags = word1 + " " + word2 + " " + word3 + " " + word4
            add_resource(user, c, picfile, picuid, tags) 
 
