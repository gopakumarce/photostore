import sys
sys.path.insert(0, "../")

from targets import Targets
import time

class TargetsTest(object):
    def __init__(self):
        self.photostore_targets = Targets(True)
        self.photostore_targets(create)

    def test_targets(self):
        curtime = str(time.time())    
        self.photostore_targets.put('1', 'foo', 'Foo', 'fa-user')
        self.photostore_targets.put('1', 'bar', 'Bar', 'fa-user')
        self.photostore_targets.put('1', 'goo', 'goo', 'fa-user')
        self.photostore_targets.put('1', 'gopa', 'Gopa Kumar', 'fa-user')
        self.photostore_targets.put('1', 'blar', 'Blar', 'fa-user')
        data = self.photostore_targets.get('1')
        for d in data:
            print 'GET: data target %s, description %s, icon %s, act %s\n' % \
                (d['g_uid'], 
                 d['TargetDescription'], 
                 d['TargetIcon'], d['TargetAccount'])
        data = self.photostore_targets.get('1', 'foo')
        for d in data:
            print 'QUERY: data target %s, description %s, icon %s, act %s\n' % \
                (d['g_uid'], 
                 d['TargetDescription'], 
                 d['TargetIcon'], d['TargetAccount'])
    
def main():
    photostore_targets_test = TargetsTest()
    photostore_targets_test.test_targets()

if __name__=="__main__":
    main()
