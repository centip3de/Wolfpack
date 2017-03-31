import random
from flask import Flask, request, jsonify

app = Flask(__name__)

class Node(object):
    def __init__(self, node_id, is_master):
        self.node_id = node_id
        self.is_master = is_master

class GL(object):
    def __init__(self):
        self.nodes = []
        self.master = None

    def register_node(self, node):
        self.nodes.append(node)
        return node

    def pick_master(self, node):
        self.master = random.choice(self.nodes)
        return self.master

    def master_picked(self):
        return self.master is not None

    def get_node(self, node_id):
        for node in self.nodes:
            if node.node_id == node_id:
                return node

    def make_master(self, node):
        self.master = node
        node.is_master = True

gl = GL()

@app.route('/master', methods=['POST', 'GET'])
def master():
    if request.method == 'POST':
        content = request.json
        resp = {"is_master": False}
        node = gl.get_node(content['node_id'])

        print gl.master_picked()
        print gl.master

        if gl.master_picked():
            print "Got a request to make node master, but we already have a master."
            return jsonify(resp)
        else:
            print "No master picked, making master node with ID: " + str(node.node_id)
            gl.make_master(node)
            resp['is_master'] = True
            return jsonify(resp)
    else:
        resp = {'master': gl.master}
        return jsonify(resp)


@app.route('/register', methods=['POST'])
def register():
    content = request.json
    print content
    node = gl.register_node(Node(content['node_id'], False))
    print "Registering new node with ID: " + str(node.node_id)
    return jsonify({'registered': node in gl.nodes})

@app.route('/')
def main():
    return "Yo"
