from flask import Flask
from flask import jsonify
from flask import request
from flask import make_response
from flask import Response
from resource import Resource
from collection import Collection
from sources import Sources
from targets import Targets
import time
import json
    
app = Flask(__name__)
app.config['DEBUG'] = True

def put_collection(data):
    cltn = Collection(True)
    if 'collectionid' in data:
        collectionid = data['collectionid']
    else:
        collectionid = str(time.time())
    cltn.put(data['user'], collectionid, data['description'])
    return collectionid

def get_collection(data):
    if not data:
        return {'NOTFOUND'}
    cltn = Collection(True)
    if 'collectionid' in data:
        collectionid = data['collectionid']
    else:
        collectionid = None
    return cltn.get(data['user'], collectionid)

def get_resource(data):
    if not data:
        return {'NOTFOUND'}
    rsrc = Resource(True)
    if 'collectionid' in data:
        collectionid = data['collectionid']
    else:
        collectionid = None
    if 'resourceid' in data:
        resourceid = data['resourceid']
    else:
        resourceid = None
    return rsrc.get(data['user'], collectionid, resourceid)

def put_resource(data):
    rsrc = Resource(True)
    if 'resourceid' in data:
        rsrcid = data['resourceid']
    else:
        rsrcid = str(time.time())
    # the last param None is the photo data which we will fill in later
    rsrc.put(data['user'], data['collectionid'], data['description'], rsrcid, None)
    return rsrcid

def post_handler(data):
    if data['type'] == 'collection':
        objid = put_collection(data)
        return jsonify({'status': 'OK', 'method': 'POST', 'collectionid': objid})
    if data['type'] == 'resource':
        objid = put_resource(data)
        return jsonify({'status': 'OK', 'method': 'POST', 'resourceid': objid})

    return jsonify({'status': 'UNKNOWN-TYPE', 'method': 'POST'})

def get_handler(data):
    if data['type'] == 'collection':
        results = get_collection(data)
        return jsonify({'status': 'OK', 'method': 'GET', 'results': results})
    if data['type'] == 'resource':
        results = get_resource(data)
        return jsonify({'status': 'OK', 'method': 'GET', 'results': results})

    return jsonify({'status': 'UNKNOWN-TYPE', 'method': 'GET'})

def get_user_info(username):
    return None
   
def get_user_sources(username):
    src = Sources()
    src.create()
    return src.get(username)      

def get_user_targets(username):
    tgt = Targets()
    tgt.create()
    return tgt.get(username, None)      

def get_user_resources(username, collectionid, resourceid):
    rsrc = Resource()
    rsrc.create()
    return rsrc.get(username, collectionid, resourceid)

def get_user_resource_details(username, collectionid, resourceid):
    rsrc = Resource()
    rsrc.create()
    result = rsrc.get(username, collectionid, resourceid)
    if not result:
        return {'Not found'}
    else:
        return {
                'FileSource': result[0]['hires_url'],
                'Description' : 'Powered by PhotoStore Technology',
                'Location': 'Palo Alto'
               }
          

def get_user_resource_comments(username, collectionid, resourceid):
    rsrc = Resource()
    rsrc.create()
    result = rsrc.get(username, collectionid, resourceid)
    return [{'CommentText': 'Nice pic!!'}]

def get_user_resource_tags(username, collectionid, resourceid):
    rsrc = Resource()
    rsrc.create()
    result = rsrc.get(username, collectionid, resourceid)
    if not result:
        return [{'No tags'}]
    else:
        return [{'TagText': result[0]['tags']}]

def get_user_collections(username):
    cltn = Collection()
    cltn.create()
    return cltn.get(username, None)

@app.route('/json/', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def handle_json():

    try:
        data = request.get_json(force=True)
    except:
        data = None

    if request.method == 'GET':
        return get_handler(data)
    elif request.method == 'POST':
        return post_handler(data)
    else:
        return jsonify({'status': 'OK', 'method': 'UNKNOWN'})
        

@app.route('/api/PhotoStoreUser/<username>', methods=['GET'])
def handle_user(username):

    app.logger.error('USER: %s\n' % username)
    if username == '1':
        username = 'foo'

    if request.method == 'GET':
        userinfo = get_user_info(username)
        return jsonify({'status': 'OK', 'method': '<%s>NOT-IMPLEMENTED' % username}), 500
    else:
        return jsonify({'status': 'OK', 'method': 'UNKNOWN'}), 500

@app.route('/api/PhotoStoreUser/<username>/sources', methods=['GET'])
def handle_sources(username):
    
    app.logger.error('SOURCES: %s\n' % username)
    if username == '1':
        username = 'foo'

    if request.method == 'GET':
        sources = get_user_sources(username)
        app.logger.error('SOURCES: %s: %s\n' % (username, sources))
        return Response(json.dumps(sources), mimetype='application/json')
    else:
        return jsonify({'status': 'OK', 'method': 'UNKNOWN'}), 500

@app.route('/api/PhotoStoreUser/<username>/targets', methods=['GET'])
def handle_targets(username):
    
    app.logger.error('TARGETS: %s\n' % username)
    if username == '1':
        username = 'foo'

    if request.method == 'GET':
        targets = get_user_targets(username)
        app.logger.error('TARGETS: %s: %s\n' % (username, targets))
        return Response(json.dumps(targets), mimetype='application/json')
    else:
        return jsonify({'status': 'OK', 'method': 'UNKNOWN'}), 500


@app.route('/api/PhotoStoreUser/<username>/resources', methods=['GET'])
def handle_resources(username):

    app.logger.error('RESOURCES: %s\n' % username)
    if username == '1':
        username = 'foo'

    if request.method == 'GET':
        # This gets the "default" collections
        resources = get_user_resources(username, '0', None)
        app.logger.error('RESOURCES: %s: %s\n' % (username, resources))
        return Response(json.dumps(resources), mimetype='application/json')
    else:
        return jsonify({'status': 'OK', 'method': 'UNKNOWN'}), 500

@app.route('/api/PhotoStoreUser/<username>/collections', methods=['GET'])
def handle_collections(username):

    app.logger.error('COLLECTIONS: %s\n' % username)
    if username == '1':
        username = 'foo'

    if request.method == 'GET':
        collections = get_user_collections(username)
        app.logger.error('COLLECTIONS: %s: %s\n' % (username, collections))
        return Response(json.dumps(collections), mimetype='application/json')
    else:
        return jsonify({'status': 'OK', 'method': 'UNKNOWN'}), 500

@app.route('/api/PhotoStoreCollection/<username>/<collectionid>/resources', methods=['GET'])
def handle_one_collection(username, collectionid):

    app.logger.error('ONE_COLLECTION: %s\n' % collectionid)

    if username == '1':
        username = 'foo'

    if request.method == 'GET':
        resources = get_user_resources(username, collectionid, None)
        app.logger.error('ONE_COLLECTION: (%s, %s)\n' % (collectionid, resources))
        return Response(json.dumps(resources), mimetype='application/json')
    else:
        return jsonify({'status': 'OK', 'method': 'UNKNOWN'}), 500

@app.route('/api/PhotoStoreResource/<username>/<collectionid>/<resourceid>/details', methods=['GET'])
def handle_one_resource_detail(username, collectionid, resourceid):

    app.logger.error('RESOURCE_DETAIL: %s, %s\n' % (resourceid, collectionid))

    if username == '1':
        username = 'foo'

    if request.method == 'GET':
        resources = get_user_resource_details(username, collectionid, resourceid)
        app.logger.error('RESOURCE_DETAIL: (%s, %s)\n' % (collectionid, resources))
        return Response(json.dumps(resources), mimetype='application/json')
    else:
        return jsonify({'status': 'OK', 'method': 'UNKNOWN'}), 500

@app.route('/api/PhotoStoreTag/<username>/<collectionid>/<resourceid>/tags', methods=['GET'])
def handle_one_resource_tags(username, collectionid, resourceid):

    app.logger.error('RESOURCE_TAGS: %s, %s\n' % (resourceid, collectionid))

    if username == '1':
        username = 'foo'

    if request.method == 'GET':
        tags = get_user_resource_tags(username, collectionid, resourceid)
        app.logger.error('RESOURCE_TAGS: (%s, %s)\n' % (collectionid, tags))
        return Response(json.dumps(tags), mimetype='application/json')
    else:
        return jsonify({'status': 'OK', 'method': 'UNKNOWN'}), 500

@app.route('/api/PhotoStoreResource/<username>/<collectionid>/<resourceid>/comments', methods=['GET'])
def handle_one_resource_comments(username, collectionid, resourceid):

    app.logger.error('RESOURCE_COMMENTS: %s, %s\n' % (resourceid, collectionid))

    if username == '1':
        username = 'foo'

    if request.method == 'GET':
        comments = get_user_resource_comments(username, collectionid, resourceid)
        app.logger.error('RESOURCE_COMMENTS: (%s, %s)\n' % (collectionid, comments))
        return Response(json.dumps(comments), mimetype='application/json')
    else:
        return jsonify({'status': 'OK', 'method': 'UNKNOWN'}), 500



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

