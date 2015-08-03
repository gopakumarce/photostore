#!/usr/bin/env python

import sys
import unirest
import json
import time

def camfind_request(url):
    # These code snippets use an open-source library. http://unirest.io/python
    headers={
        "X-Mashape-Key": "INSERT_YOUR_KEY",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    params={
        "focus[x]": "480",
        "focus[y]": "640",
        "image_request[altitude]": "27.912109375",
        "image_request[language]": "en",
        "image_request[latitude]": "35.8714220766008",
        "image_request[locale]": "en_US",
        "image_request[longitude]": "14.3583203002251",
        "image_request[remote_image_url]": "%s" % url
    }
    response = unirest.post("https://camfind.p.mashape.com/image_requests",
                            headers=headers, params=params)
    return response

def camfind_response(token):
    # These code snippets use an open-source library. http://unirest.io/python
    response = unirest.get("https://camfind.p.mashape.com/image_responses/{0}".format(token),
        headers={
            "X-Mashape-Key": "INSERT_YOUR_KEY",
            "Accept": "application/json"
        }
    )
    return response

def response_status(response):
    try:
        response_json = json.loads(response.raw_body)
    except:
        return 'dontwait'
    status_key = unicode('status')
    if status_key in response_json:
        status = response_json[status_key]
        if status == 'not completed':
            return 'wait'
    else:
        return 'dontwait'

def get_image_tag(url):

    # First get post the image and get the token for results
    result = camfind_request(url)
    if not result:
        return None
    else:
        print "%s %s %s %s\n" % (result.code, result.headers, result.body,
                                 result.raw_body)
    try:
        result_json = json.loads(result.raw_body)
    except:
        return None

    token_key = unicode('token')
    if token_key in result_json:
        token = result_json[token_key]
    else:
        return None

    # Given the token find more details
    response = camfind_response(token)
    if not response:
        return None
    else:
        print "%s %s %s %s\n" % (response.code, response.headers,
                                 response.body, response.raw_body)

    while response_status(response) == 'wait':
        print 'waiting :-w...' 
        time.sleep(10)   
        response = camfind_response(token)
        if not response:
            return None
        else:
            print "%s %s %s %s\n" % (response.code, response.headers,
                                     response.body, response.raw_body)

    response_json = json.loads(response.raw_body)
    # Check what the name tags say
    name_key = unicode('name')
    if name_key in response_json:
        return response_json[name_key]
    else:
        return None

if __name__=="__main__":
    if len(sys.argv) <= 1:
        url = 'http://upload.wikimedia.org/wikipedia/en/2/2d/Mashape_logo.png'
    else:
        url = sys.argv[1];
    tags = get_image_tag(url)
    if tags:
        print 'Tags: %s\n' % tags
    else:
        print 'No tags found\n'
