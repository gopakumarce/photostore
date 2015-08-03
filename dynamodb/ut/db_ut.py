import sys
sys.path.insert(0, "../")

from db import Database

class DbTest(object):
    def __init__(self):
        self.photostore = Database(True)

    def test_tables(self):
        # No local index, only hash and range indices
        keys = [{'hash': 'hashkey'}, {'range': 'rangekey'}]
        self.photostore.create_table('photostore', keys)
        data = {
                 'hashkey' : 'gopa',
                 'rangekey' : 'sanjose',
                 'comments' : 'testing again...!' 
               }
        datakeys = {'hashkey' : 'gopa', 'rangekey' : 'sanjose'}
        # Store the data
        self.photostore.put_data('photostore', data, datakeys)
        # Retrieve it
        item = self.photostore.get_data('photostore', datakeys)
        if item:
            print 'GET: photo %s, tag %s, comments %s\n' % \
                  (item['hashkey'], item['rangekey'], item['comments'])
        else:
            print 'Item not found\n'

    def test_tables_localindex(self):
        # Only hash index and one local range index. Local hash has to be the
        # same as the hash index because thats how local indices work
        keys = [{'hash': 'hashkey'}, {'range': 'rangekey'},
                {'hash': 'hashkey', 'local': 'mylocal', 'range': 'rangekey_1'}]
        self.photostore.create_table('photostore-local', keys)
        # data set 1
        data = {
                 'hashkey' : 'gopa-local',
                 'rangekey' : 'sanjose-ca-95134',
                 'rangekey_1' : 'test1',
                 'comments' : 'testing local this time' 
               }
        datakeys = {'hashkey' : 'gopa-local', 'rangekey' : 'sanjose-ca-95134'}
        # store data set 1
        self.photostore.put_data('photostore-local', data, datakeys)
        # data set 2 .. note that the rangekey_1 which is the local index, is
        # the same as in data set 1 .. So when we query with the local index
        # (secondary index) we should get both the results
        data = {
                 'hashkey' : 'gopa-local',
                 'rangekey' : 'sanjose-ca-95134-1',
                 'rangekey_1' : 'test1',
                 'comments' : 'testing local this time, duplicate !!' 
               }
        datakeys = {'hashkey' : 'gopa-local',
                    'rangekey' : 'sanjose-ca-95134-1'}
        # store data set 2
        self.photostore.put_data('photostore-local', data, datakeys)
        # query with the local secondary index
        datakeys_query = {'hashkey__eq' : 'gopa-local', 
                          'rangekey_1__eq' : 'test1'}
        # we expect to see two entries
        item = self.photostore.query_data('photostore-local',
                                      datakeys_query, 'mylocal')
        for i in item:
            print 'QUERY: [%s, %s, %s, %s]\n' %  \
                  (i['hashkey'], i['rangekey'], i['rangekey_1'],
                   i['comments'])

        # now get item again with the primary hash/range keys
        datakeys = {'hashkey' : 'gopa-local', 'rangekey' : 'sanjose-ca-95134'}
        item = self.photostore.get_data('photostore-local', datakeys)
        if item:
            print 'GET: [%s, %s, %s, %s]\n' % \
                  (item['hashkey'], item['rangekey'], item['rangekey_1'],
                   item['comments'])

        # now get the second with the primary hash/range keys
        datakeys = {'hashkey' : 'gopa-local', 'rangekey' : 'sanjose-ca-95134-1'}
        item = self.photostore.get_data('photostore-local', datakeys)
        if item:
            print 'GET: [%s, %s, %s, %s]\n' % \
                  (item['hashkey'], item['rangekey'], item['rangekey_1'],
                   item['comments'])
def main():
    photostore_test = DbTest()
    photostore_test.test_tables()
    photostore_test.test_tables_localindex()

if __name__=="__main__":
    main()
