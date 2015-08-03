import sys
sys.path.insert(0, "../")

from collection_src_tgt import CollectionSrcTgt
import collections
import time

class CollectionSrcTgtTest(object):
    def __init__(self):
        self.photostore_collection = CollectionSrcTgt(True)
        self.photostore_collection.create()

    def test_collection(self):
        curtime = str(time.time())    
        self.photostore_collection.put('gopa', 'foo', curtime)
        data = self.photostore_collection.get('gopa', 'foo', curtime)
        for d in data:
            print 'GET: data cltnid %s, src %s, tgt %s\n' % \
                (d['g_rsrc_collectionid'], d['g_uid_src'],  d['g_uid_tgt'])
        data = self.photostore_collection.get('gopa', 'foo', None)
        for d in data:
            print 'QUERY: data cltnid %s, src %s, tgt %s\n' % \
                (d['g_rsrc_collectionid'], d['g_uid_src'], d['g_uid_tgt'])
    
def main():
    photostore_cltn_test = CollectionSrcTgtTest()
    photostore_cltn_test.test_collection()

if __name__=="__main__":
    main()
