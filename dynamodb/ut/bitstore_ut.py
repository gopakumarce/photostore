import sys
sys.path.insert(0, "../")

from bitstore import BitStore

class BitStoreTest(object):
    def __init__(self):
        self.photostore = BitStore(True)
        self.photostore.create()

    def test_bits(self, srcfile, dstfile):
        (key, url) = self.photostore.put(srcfile)
        print 'File stored, key is %s, url %s\n' % (key, url)
        if key:
            self.photostore.get(key, dstfile)
        
def main(srcfile, dstfile):
    photostore_test = BitStoreTest()
    photostore_test.test_bits(srcfile, dstfile)

if __name__=="__main__":
    main(sys.argv[1], sys.argv[2])
