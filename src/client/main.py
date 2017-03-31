import sys
import time
import requests
import uuid
import random

import alpha

class Slave(object):
    def __init__(self):
        self.node_id = str(uuid.uuid4())
        self.is_alpha = False
        self.running = True
        self.registered = True
        self.alpha_port

    def try_alpha(self):
        print "Trying to become alpha!"
        resp = requests.post('http://127.0.0.1:6543/alpha',
            json={'node_id': self.node_id}).json()

        if resp['is_alpha']:
            print "I am alpha!"
            self.is_alpha = True
            self.running = False
        else:
            print "I am a slave!"

        return resp

    def get_alpha(self):
        resp = requests.get('http://127.0.0.1:6543/alpha').json()
        return json['alpha']

    def register(self):
        print "I'm registering with the server."
        resp = requests.post('http://127.0.0.1:6543/register',
            json={'node_id':self.node_id}).json()

        if resp['registered'] == False:
            print "[ERROR] I'm not sure what happend, honestly."
            sys.exit(-1)
        else:
            return True

    def release_access(self):
        print "I'm releasing access and letting others do stuff"
        resp = requests.post('http://127.0.0.1:6544/release/doc_1')

    def make_edit(self):
        print "I'm taking my turn and making an edit."
        possible_edits = ["Edit", "Test", "Adding stuff", "Adding more stuff", "Blah",
            "Foo", "Bar", "Baz", "Bin", "Bake", "Fake", "Sake", "Jake", "Daisy", "Tumwater",
            "Snake", "Cake", "Rake", "Make", "Lake", "Break", "Long line of text"]

        resp = requests.post('http://127.0.0.1:6544/edit/doc_1',
            json={'node_id':self.node_id, 'edit': random.choice(possible_edits)})

    def request_access(self):
        print "I'm seeing if I can edit yet."
        resp = requests.post('http://127.0.0.1:6544/request/doc_1',
            json={'node_id':self.node_id}).json()
        return resp['can_edit']


def become_alpha(port):
    foo = alpha.Alpha(port)
    foo.begin_serving()


def become_slave(slave, alpha_port, port):
    print "My port is: " + str(port)
    print "Alpha's port is: " + str(alpha_port)
    slave.alpha_port = alpha_port

    while(slave.running):
        if slave.request_access():
            slave.make_edit()
            slave.release_access()
        else:
            pass
        print "I've done my thing, going to sleep for a second to simulate... I dunno... something?"
        time.sleep(5)

if __name__ == '__main__':
    slave = Slave()

    if slave.register():
        resp = slave.try_alpha()
        if slave.is_alpha:
            become_alpha(resp['port'])
        else:
            become_slave(slave, resp['alpha_port'], resp['port'])
