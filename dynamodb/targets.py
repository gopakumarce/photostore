import time
from db import Database

class Targets(Database):
    def __init__(self, ut=False):
        super(Targets, self).__init__(ut)
        if ut:
            self.__name = 'targets_ut'
        else:
            self.__name = 'targets'
        self.__index = 'tgtlocal'
        self.__keys = [
                          {'hash': 'g_uid'}, {'range': 'g_uid_tgt'},
                          {'hash': 'g_uid', 'local': self.__index,
                           'range': 'g_uid_tgt'}
                      ]

    def create(self):
        self.__table = self.create_table(self.__name, self.__keys)

    def delete(self):
        self.delete_table(self.__name)

    def put(self, user, target, description, icon):
        data = {
                'g_uid' : user,
                'g_uid_tgt' : target,
                'TargetName': description,
                'TargetDescription': description,
                'TargetIcon': icon,
                'TargetAccount': target
               }
        keys = { 'g_uid' : user, 'g_uid_tgt' : target} 
        self.put_data(self.__name, data, keys)

    def boto2json(self, boto):
        return {
                'g_uid': boto['g_uid_tgt'],
                'TargetDescription': boto['TargetDescription'], 
                'TargetIcon' : boto['TargetIcon'],
                'TargetAccount' : boto['TargetAccount'],
                'TargetName' : boto['TargetName']
               }        

    def get(self, user, target=None):
        if target:
            # lookup on primary keys
            keys = {
                    'g_uid' : user,
                    'g_uid_tgt': target
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
        
