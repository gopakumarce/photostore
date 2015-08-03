import time
from db import Database

class Sources(Database):
    def __init__(self, ut=False):
        super(Sources, self).__init__(ut)
        if ut:
            self.__name = 'sources_ut'
        else:
            self.__name = 'sources'
        self.__index = 'srclocal'
        self.__keys = [
                          {'hash': 'g_uid'}, {'range': 'g_uid_src'},
                          {'hash': 'g_uid', 'local': self.__index,
                           'range': 'g_uid_src'}
                      ]

    def create(self):
        self.__table = self.create_table(self.__name, self.__keys)

    def delete(self):
        self.delete_table(self.__name)

    def put(self, user, source, description, icon):
        data = {
                'g_uid' : user,
                'g_uid_src' : source,
                'SourceName': description,
                'SourceDescription': description,
                'SourceIcon': icon,
                'SourceAccount': source
               }
        keys = { 'g_uid' : user, 'g_uid_src' : source} 
        self.put_data(self.__name, data, keys)

    def boto2json(self, boto):
        return {
                'g_uid': boto['g_uid_src'],
                'SourceDescription': boto['SourceDescription'], 
                'SourceIcon' : boto['SourceIcon'],
                'SourceAccount' : boto['SourceAccount'],
                'SourceName' : boto['SourceName']
               }        

    def get(self, user, source=None):
        if source:
            # lookup on primary keys
            keys = {
                    'g_uid' : user,
                    'g_uid_src': source
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
            if not retdata:
                return None
            for r in retdata:
                data.append(self.boto2json(r))
            return data
        
