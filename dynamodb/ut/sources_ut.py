import sys
sys.path.insert(0, "../")

from sources import Sources
import time

class SourcesTest(object):
    def __init__(self):
        self.photostore_sources = Sources(True)
        self.photostore_sources.create()

    def test_sources(self):
        curtime = str(time.time())    
        self.photostore_sources.put('1', 'foo', 'Foo', 'fa-user')
        self.photostore_sources.put('1', 'bar', 'Bar', 'fa-user')
        self.photostore_sources.put('1', 'goo', 'Goo', 'fa-user')
        self.photostore_sources.put('1', 'gopa', 'Gopa Kumar', 'fa-user')
        self.photostore_sources.put('1', 'blar', 'Blar', 'fa-user')
        data = self.photostore_sources.get('1')
        for d in data:
            print 'GET: data source %s, description %s, icon, %s act %s\n' % \
                (d['g_uid'], 
                 d['SourceDescription'], 
                 d['SourceIcon'], d['SourceAccount'])
        data = self.photostore_sources.get('1', 'foo')
        for d in data:
            print 'QUERY: data source %s, description %s, icon %s, act %s\n' % \
                (d['g_uid'], 
                 d['SourceDescription'], 
                 d['SourceIcon'], d['SourceAccount'])
    
def main():
    photostore_sources_test = SourcesTest()
    photostore_sources_test.test_sources()

if __name__=="__main__":
    main()
