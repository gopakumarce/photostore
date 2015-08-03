import sys
sys.path.insert(0, "../")

from collection import Collection
import collections
import time

class CollectionTest(object):
    def __init__(self):
        self.photostore_collection = Collection(True)
        self.photostore_collection.create()

    def test_collection(self):
        curtime = str(time.time())    
        self.photostore_collection.put('gopa', curtime,
                                   '[%s]: test put' % curtime)
        data = self.photostore_collection.get('gopa', curtime)
        for d in data:
            print 'GET: data cltnid %s, uid %s, description %s, date %s\n' % \
                (d['CollectionID'], d['g_uid'], \
                 d['collection_text'], d['CollectionDate'])
        data = self.photostore_collection.get('gopa', None)
        for d in data:
            print 'QUERY: data cltnid %s, uid %s, description %s, date %s\n' % \
                (d['CollectionID'], d['g_uid'], \
                 d['collection_text'], d['CollectionDate'])
    
def main():
    photostore_cltn_test = CollectionTest()
    photostore_cltn_test.test_collection()

if __name__=="__main__":
    main()
