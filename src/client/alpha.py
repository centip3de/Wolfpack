from flask import Flask, jsonify, request

app = Flask(__name__)

class Alpha(object):
    docs = {}
    doc_contents = {}

    def __init__(self):
        self.ip_address = None

    def begin_serving(self):
        app.run(host="0.0.0.0", port=6544)

    def shutdown_server(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

@app.route('/edit/<doc_id>', methods=["POST"])
def handle_edit(doc_id):
    content = request.json
    if doc_id in Alpha.docs:
        if Alpha.docs[doc_id] == content['node_id']:
            if doc_id in Alpha.doc_contents:
                Alpha.doc_contents[doc_id].append(content['edit'])
            else:
                Alpha.doc_contents[doc_id] = [content['edit']]

            print "Making an edit to doc " + str(doc_id) + ". Content is now:\n " + "\n".join(Alpha.doc_contents[doc_id])
            return jsonify({'result': Alpha.doc_contents[doc_id]})

    return jsonif({'result': 'Error'})

@app.route('/request/<doc_id>', methods=["POST"])
def handle_request(doc_id):
    content = request.json
    if doc_id in Alpha.docs:
        if Alpha.docs[doc_id] is not None:
            return jsonify({'can_edit':False})
        else:
            Alpha.docs[doc_id] = content['node_id']
            return jsonify({'can_edit':True})
    else:
        Alpha.docs[doc_id] = content['node_id']
        return jsonify({'can_edit':True})

@app.route('/release/<doc_id>', methods=["POST"])
def handle_release(doc_id):
    content = request.json
    if doc_id in Alpha.docs:
        Alpha.docs[doc_id] = None

    return jsonify({})
