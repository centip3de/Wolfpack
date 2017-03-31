from flask import Flask, jsonify, request

app = Flask(__name__)

class Alpha(object):
    docs = {}
    doc_contents = {}
    shutdown = False

    def __init__(self, port):
        self.ip_address = None
        self.port = port

    def begin_serving(self):
        app.run(host="0.0.0.0", port=self.port)
        return Alpha.shutdown

    def shutdown_server():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

@app.route('/ping', methods=["POST"])
def handle_ping():
    print "I'm being pinged by GL."
    content = request.json
    return jsonify({'word':content['word']})


@app.route('/demote', methods=["POST"])
def handle_demotion():
    print "I'm being demoted. :( Killing my server."
    Alpha.shutdown = True
    Alpha.shutdown_server()

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
