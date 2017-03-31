import sys
import time
import requests
import uuid
import random
from requests.exceptions import ConnectionError, Timeout

import alpha

class Slave(object):
    def __init__(self):
        self.node_id = str(uuid.uuid4())
        self.is_alpha = False
        self.running = True
        self.registered = True
        self.alpha_port = 0
        self.gl_port = 6543
        self.base_url = "http://127.0.0.1"

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
        url = self.base_url + ":" + str(self.alpha_port) + "/release/doc_1"
        resp = requests.post(url)

    def new_alpha(self):
        print "Trying to tell GL that we need a new alpha."
        try:
            url = self.base_url + ":" + str(self.gl_port) + "/new_alpha"
            resp = requests.post(url, timeout=15).json()
            if resp['alpha'] != self.alpha_port:
                print "New alpha has been chosen."
                alpha_port = resp['alpha']
                alpha_id = resp['alpha_id']

                if alpha_id == self.node_id:
                    print "I've been promoted to alpha!"
                    self.running = False
                    become_alpha(alpha_port)
                else:
                    print "I am not the new alpha... and that's fine. :("
                    self.alpha_port = alpha_port
            else:
                print "Weird shit is going on"
                print "I think alpha's port is: " + str(self.alpha_port)

        except (Timeout, ConnectionError):
            print "Couldn't connect to the GL either. There's a problem with me. Shutting down."
            sys.exit(-1)

    def make_edit(self):
        print "I'm taking my turn and making an edit."
        possible_edits = ["Edit", "Test", "Adding stuff", "Adding more stuff", "Blah",
            "Foo", "Bar", "Baz", "Bin", "Bake", "Fake", "Sake", "Jake", "Daisy", "Tumwater",
            "Snake", "Cake", "Rake", "Make", "Lake", "Break", "Long line of text"]

        url = self.base_url + ":" + str(self.alpha_port) + "/edit/doc_1"
        try:
            resp = requests.post(url,
                json={
                    'node_id':self.node_id,
                    'edit': random.choice(possible_edits)
                }, timeout=5).json()
        except (Timeout, ConnectionError):
            print "Couldn't connect to master! Telling GL."
            self.new_alpha()

    def request_access(self):
        print "I'm seeing if I can edit yet."
        try:
            url = self.base_url + ":" + str(self.alpha_port) + "/request/doc_1"
            resp = requests.post(url,
                json={'node_id':self.node_id}, timeout=5).json()
            return resp['can_edit']
        except (Timeout, ConnectionError):
            print "Couldn't connect to master! Telling GL."
            self.new_alpha()


def become_alpha(port):
    foo = alpha.Alpha(port)
    shutdown = foo.begin_serving()
    if shutdown:
        print "Becoming slave."
        main()


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
        time.sleep(2)

def main():
    slave = Slave()

    if slave.register():
        resp = slave.try_alpha()
        if slave.is_alpha:
            become_alpha(resp['port'])
        else:
            become_slave(slave, resp['alpha_port'], resp['port'])

if __name__ == "__main__":
    main()
