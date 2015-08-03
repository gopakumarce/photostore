from boto.dynamodb2.layer1 import DynamoDBConnection
from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.fields import RangeKey
from boto.dynamodb2.fields import KeysOnlyIndex
from boto.dynamodb2.fields import GlobalAllIndex
from boto.dynamodb2.fields import AllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2 import connect_to_region

class Database(object):
    def __init__(self, ut=False, read_tput=None, write_tput=None):
        self.conn = None
        self.tables = {}
        self.keys = {}
        if read_tput:
            self.throughput_read = read_tput
        else:
            self.throughput_read = 10
        if write_tput:
            self.throughput_write = write_tput
        else:
            self.throughput_write = 10

        # override this for testing with dynamodb local
        local = False

        if local:        
            self.conn = DynamoDBConnection(
                            aws_access_key_id='photostore',
                            aws_secret_access_key='local',
                            host='localhost',
                            port=8000,
                            is_secure=False)
        else:
            self.conn = connect_to_region(
                            'us-west-2',
                            aws_access_key_id='YOUR_ACCOUNT',
                            aws_secret_access_key='YOUR_KEY'
                        )

    def create_table(self, name, keys):
        schema = []
        local = []
        for k in keys:
            if 'local' in k:
                if 'range' in k:
                    local.append(AllIndex(k['local'], parts=[
                                    HashKey(k['hash']),
                                    RangeKey(k['range'])
                                    ]))
                else:
                    local.append(AllIndex(k['local'], parts=[
                                    HashKey(k['hash']),
                                    RangeKey(k['range'])
                                    ],
                                    throughput={
                                        'read': self.throughput_read,
                                        'write': self.throughput_write
                                    }))
            elif 'hash' in k:
                schema.append(HashKey(k['hash']))
            elif 'range' in k:
                schema.append(RangeKey(k['range']))
        try:
            table = Table.create(name, schema=schema, indexes=local,
                                    throughput={
                                        'read': self.throughput_read,
                                        'write': self.throughput_write
                                    }, connection=self.conn)
        except Exception as e:
            print 'Create table exception [%s]: adding in-mem table\n' % e
            table = Table(name, connection=self.conn)
            pass
        self.keys[name] = keys
        self.tables[name] = table

    def delete_table(self, name):
        try:
            table = Table(name, connection=self.conn)
            table.delete()
        except Exception as e:
            print 'Exception deleting table %s [%s]\n' % (name, e)

    def put_data(self, name, item_data, keys=None):
        if keys:
            itemget = self.get_data(name, keys)
        else:
            itemget = None
        if itemget:
            for k in item_data:
                itemget[k] = item_data[k]
            itemget.save()
        else:
            try:
                self.tables[name].put_item(data=item_data)
            except Exception as e:
                print 'Exception[%s]: Unable to store [%s]: %s\n' % (e, name, item_data)

    def get_data(self, name, keys): 
        try:
            item = self.tables[name].get_item(**keys)
        except:
            return None
        return item

    def query_data(self, name, keys, index): 
        try:
            item = self.tables[name].query_2(index=index, **keys)
        except:
            return None
        return item

    def scan_data(self, name, keys):
        try:
            item = self.tables[name].scan(**keys)
        except:
            return None
        return item

