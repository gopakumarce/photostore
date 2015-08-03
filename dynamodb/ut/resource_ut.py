import sys
sys.path.insert(0, "../")

from resource import Resource
import collections
import time
class ResourceTest(object):
    def __init__(self):
        self.photostore_resource = Resource(True)
        self.photostore_resource.create()

    def test_resource(self):
        curtime = str(time.time())    
        self.photostore_resource.put('gopa', 1, '[%s]: test put' % curtime,
                                 curtime)
        data = self.photostore_resource.get('gopa', 1, curtime)
        for d in data:
            print 'GET: data cltnid %s, uid %s, description %s\n' % \
                (d['g_rsrc_collectionid'], d['g_uid'], \
                 d['description'])
        data = self.photostore_resource.get('gopa', 1, None)
        for d in data:
            print 'QUERY: data cltnid %s, uid %s, description %s\n' % \
                (d['g_rsrc_collectionid'], d['g_uid'], d['description'])
    
def main():
    photostore_rsrc_test = ResourceTest()
    photostore_rsrc_test.test_resource()

if __name__=="__main__":
    main()
