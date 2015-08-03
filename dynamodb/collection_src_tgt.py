import time
from db import Database

class CollectionSrcTgt(Database):
    def __init__(self, ut=False):
        super(CollectionSrcTgt, self).__init__(ut)
        if ut:
            self.__name = 'collection_src_tgt_ut'
        else:
            self.__name = 'collection_src_tgt'
        self.__index = 'cltn_src_tgt_local'
        self.__keys = [
                          {'hash': 'g_uid_combined'},
                          {'range': 'g_rsrc_collectionid'},
                          {'hash': 'g_uid_combined', 'local': self.__index,
                           'range': 'g_rsrc_collectionid'}
                         ]

    def create(self):
        self.__table = self.create_table(self.__name, self.__keys)

    def delete(self):
        self.delete_table(self.__name)

    def put(self, source, target, collectionid):
        # collectionid belongs to the source
        uid_combined = source+':'+target
        data = {
                'g_uid_src' : source,
                'g_uid_tgt' : target,
                'g_uid_combined' : uid_combined,
                'g_rsrc_collectionid' : collectionid
               }
        keys = {
                'g_uid_combined' : uid_combined,
                'g_rsrc_collectionid' : collectionid
               } 
        self.put_data(self.__name, data, keys)

    def boto2json(self, boto):
        return {
                'g_uid_src': boto['g_uid_src'], 
                'g_uid_tgt': boto['g_uid_tgt'], 
                'g_rsrc_collectionid': boto['g_rsrc_collectionid']
               }        

    def get(self, source, target, collectionid=None):
        uid_combined = source+':'+target
        if collectionid:
            # lookup on primary keys
            keys = {
                    'g_uid_combined' : uid_combined,
                    'g_rsrc_collectionid': collectionid
                   }
            data = self.get_data(self.__name, keys)
            if data:
                return [self.boto2json(data)]
            else:
                return []
        else:
            keys = {
                    'g_uid_combined__eq': uid_combined
                   }
            data = []
            retdata = self.query_data(self.__name, keys, self.__index)
            for r in retdata:
                data.append(self.boto2json(r))
            return data
        
