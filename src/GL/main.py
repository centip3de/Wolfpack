import random
import sys
import time
import requests
from requests.exceptions import ConnectionError, Timeout
from flask import Flask, request, jsonify

app = Flask(__name__)

class Node(object):
    def __init__(self, node_id, is_alpha):
        self.node_id = node_id
        self.is_alpha = is_alpha
        self.port = 0

class GL(object):
    def __init__(self):
        self.nodes = []
        self.alpha = None
        self.port = 6543
        self.alpha_port = 0

    def register_node(self, node):
        self.nodes.append(node)
        return node

    def pick_alpha(self):
        self.nodes.remove(self.alpha)

        self.alpha = random.choice(self.nodes)
        self.alpha_port = self.alpha.port
        self.alpha.is_alpha = True
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
        self.alpha_port = node.port

gl = GL()

@app.route('/new_alpha', methods=["POST"])
def new_alpha():
    print "Just heard we couldn't contact alpha. Pinging."
    words = ["Duck", "Luck", "Shuck", "Truck"]
    random_word = random.choice(words)
    try:
        url = "http://127.0.0.1:" + str(gl.alpha_port) + "/ping"
        resp = requests.post(url, timeout=10, json={'word':random_word}).json()
        print "Sent: " + random_word + " Received: " + resp['word']
        if resp['word'] == random_word:
            print "I could connect to alpha. Ignoring new alpha request."
            return jsonify(
                    {
                        'alpha':gl.alpha_port,
                        'alpha_id':gl.alpha.node_id
                    })
        else:
            print "Weird shit's happening. Quitting."
            sys.exit(-1)

    except (Timeout, ConnectionError):
        print "I couldn't contact alpha either. Choosing new alpha."
        new_alpha = gl.pick_alpha()
        print "New alpha port: " + str(new_alpha.port)
        return jsonify({
            'alpha':new_alpha.port,
            'alpha_id':new_alpha.node_id
            })

@app.route('/alpha', methods=['POST', 'GET'])
def alpha():
    if request.method == 'POST':
        content = request.json
        resp = {"is_alpha": False}
        node = gl.get_node(content['node_id'])
        gl.port += 1
        node.port = gl.port

        if gl.alpha_picked():
            print "Got a request to make node alpha, but we already have a alpha."
            resp['port'] =  node.port
            resp['alpha_port'] = gl.alpha_port
            return jsonify(resp)
        else:
            print "No alpha picked, making alpha node with ID: " + str(node.node_id)
            gl.make_alpha(node)
            resp['is_alpha'] = True
            resp['port'] = node.port
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
