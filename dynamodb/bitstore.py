#!/usr/bin/env python
 
import os
import uuid
import boto
from boto.s3.connection import S3Connection 
from boto.s3.key import Key

class BitStore(object):
    def __init__(self,ut=False):
        if ut:
            self.__name = 'photostore-bucket-test'
        else:
            self.__name = 'photostore-bucket'
        self.__conn = S3Connection('YOUR_ACCOUNT',
                                   'YOUR_KEY')

    def create(self):
        try:
            self.__bucket = self.__conn.get_bucket(self.__name)
            self.__bucket.set_acl('public-read')
            print self.__conn, self.__bucket
        except Exception as e:
            print 'Bucket create exception %s\n' % e
            pass

    def delete(self):
        try:
            bucket = self.__conn.get_bucket(self.__name)
            for key in bucket.list():
                key.delete()
            self.__conn.delete_bucket(self.__name)
        except Exception as e:
            print 'Bucket delete exception %s\n' % e
            pass

    def put(self, filename, fileuid):
        k = Key(self.__bucket)
        k.key = str(fileuid)
        k.set_contents_from_filename(filename)
        url = k.generate_url(expires_in=0, query_auth=False)
        k.make_public()
        return (fileuid, url)

    def get(self, key, filename):
        k = self.__bucket.get_key(key)
        if not key:
            return 0
        k.get_contents_to_filename(filename)
        return 1
        
