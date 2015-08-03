import time
from db import Database

class Resource(Database):
    def __init__(self, ut=False):
        super(Resource, self).__init__(ut)
        if ut:
            self.__name = 'resource_ut'
        else:
            self.__name = 'resource'
        self.__index1 = 'rsrcwclnt'
        self.__index2 = 'rsrcwuser'
        self.__keys = [
                          {'hash': 'g_uid'}, {'range': 'cid+rid'},
                          {'hash': 'g_uid', 'local': self.__index1,
                           'range': 'g_rsrc_collectionid'},
                          {'hash': 'g_uid', 'local': self.__index2,
                           'range': 'g_rsrc_dummy'}
                         ]

    def create(self):
        self.__table = self.create_table(self.__name, self.__keys)

    def delete(self):
        self.delete_table(self.__name)

    def put(self, user, collectionid, description, rsrc_id, hires_url, lowres_url, 
            thumb_url, rsrc_type='image', tags=None):
        rangekey   = str(collectionid) + ":" + rsrc_id
        data = {
                'g_rsrc_collectionid' : str(collectionid),
                'g_rsrc_id': rsrc_id,
                'cid+rid' : rangekey,
                'g_uid' : user,
                'rsrc_type' : rsrc_type,
                'description' : description,
                'hires_url'  : hires_url,
                'lowres_url' : lowres_url,
                'thumb_url' : thumb_url,
                'g_rsrc_dummy': 'dummy'
               }
        if tags:
            data['tagged'] = '1'
            data['tags'] = tags
        else:
            data['tagged'] = '0'
        keys = { 'g_uid' : user, 'cid+rid' : rangekey} 
        self.put_data(self.__name, data, keys)

    def boto2json(self, boto):
        ret = {
                'g_rsrc_collectionid': boto['g_rsrc_collectionid'],
                'ResourceId' : boto['g_rsrc_id'],
                'g_uid' : boto['g_uid'],
                'TypeDescription' : boto['rsrc_type'],
                'description' : boto['description'],
                'hires_url' : boto['hires_url'],
                'lowres_url' : boto['lowres_url'],
                'ThumbURL' : boto['thumb_url'],
                'CreationDate' : time.strftime("%c")
               } 
        if 'tags' in boto:
	    ret.update({'tags' : boto['tags']})
	else:        
	    ret.update({'tags' : 'No tags'})
     
        return ret
           
    def get(self, user, collectionid, rsrcid):
        '''
        If rsrcid and collectionid are provided, we can do an exact lookup,
        otherwise if collectionid and user are provided, we can do a query
        lookup of all the resources matching that key
        '''
        if collectionid and rsrcid:
            # lookup on primary keys
            keys = {
                    'g_uid' : user,
                    'cid+rid': str(collectionid)+":"+str(rsrcid)
                   }
            data = self.get_data(self.__name, keys)
            if data:
                return [self.boto2json(data)]
            else:
                return []
        else:
            if collectionid:
                keys = {
                        'g_uid__eq': user,
                        'g_rsrc_collectionid__eq' : str(collectionid)
                    }
                retdata = self.query_data(self.__name, keys, self.__index1)
            else:
                keys = {
                        'g_uid__eq': user,
                        'g_rsrc_dummy__eq' : 'dummy'
                       }
                retdata = self.query_data(self.__name, keys, self.__index2)
            data = []
            if retdata:
                for r in retdata:
                    data.append(self.boto2json(r))
            return data                
