import random
from flask import Flask, request, jsonify

app = Flask(__name__)

class Node(object):
    def __init__(self, node_id, is_alpha):
        self.node_id = node_id
        self.is_alpha = is_alpha

class GL(object):
    def __init__(self):
        self.nodes = []
        self.alpha = None

    def register_node(self, node):
        self.nodes.append(node)
        return node

    def pick_alpha(self, node):
        self.alpha = random.choice(self.nodes)
        return self.alpha

    def alpha_picked(self):
        return self.alpha is not None

    def get_node(self, node_id):
        for node in self.nodes:
            if node.node_id == node_id:
                return node

    def make_alpha(self, node):
        self.alpha = node
        node.is_alpha = True

gl = GL()

@app.route('/alpha', methods=['POST', 'GET'])
def alpha():
    if request.method == 'POST':
        content = request.json
        resp = {"is_alpha": False}
        node = gl.get_node(content['node_id'])

        if gl.alpha_picked():
            print "Got a request to make node alpha, but we already have a alpha."
            return jsonify(resp)
        else:
            print "No alpha picked, making alpha node with ID: " + str(node.node_id)
            gl.make_alpha(node)
            resp['is_alpha'] = True
            return jsonify(resp)
    else:
        resp = {'alpha': gl.alpha}
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
