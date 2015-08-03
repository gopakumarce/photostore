import time
from db import Database

class Collection(Database):
    def __init__(self, ut=False):
        super(Collection, self).__init__(ut)
        if ut:
            self.__name = 'collection_ut'
        else:
            self.__name = 'collection'
        self.__index = 'cltnlocal'
        self.__keys = [
                          {'hash': 'g_uid'}, {'range': 'g_rsrc_collectionid'},
                          {'hash': 'g_uid', 'local': self.__index,
                           'range': 'g_rsrc_collectionid'}
                         ]

    def create(self):
        self.__table = self.create_table(self.__name, self.__keys)
    
    def delete(self):
        self.delete_table(self.__name)

    def put(self, user, collectionid, description):
        data = {
                'g_rsrc_collectionid' : collectionid,
                'g_uid' : user,
                'collection_text' : description
               }
        keys = { 'g_uid' : user, 'g_rsrc_collectionid' : collectionid} 
        self.put_data(self.__name, data, keys)

    def boto2json(self, boto):
        # The date is bogus, need to fix that 
        return {
                'g_uid': boto['g_uid'], 
                'CollectionID': boto['g_rsrc_collectionid'],
                'collection_text': boto['collection_text'],
                'CollectionDate': time.strftime("%c")
               }        

    def get(self, user, collectionid):
        if collectionid:
            # lookup on primary keys
            keys = {
                    'g_uid' : user,
                    'g_rsrc_collectionid': collectionid
                   }
            data = self.get_data(self.__name, keys)
            if data:
                return [self.boto2json(data)]
            else:
                return []
        else:
            keys = {
                    'g_uid__eq': user
                   }
            data = []
            retdata = self.query_data(self.__name, keys, self.__index)
            for r in retdata:
                data.append(self.boto2json(r))
            return data
        
