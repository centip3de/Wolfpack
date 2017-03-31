import sys
import time
import requests
import uuid

class Master(object):
    def __init__(self):
        self.ip_address = None
        self.running = True

    def register(self):
        pass

class Slave(object):
    def __init__(self):
        self.node_id = str(uuid.uuid4())
        self.is_master = False
        self.running = True
        self.registered = True

    def try_master(self):
        print "Trying to become master!"
        resp = requests.post('http://127.0.0.1:6543/master',
            json={'node_id': self.node_id}).json()

        if resp['is_master']:
            print "I am master!"
            self.is_master = True
            self.running = False
        else:
            print "I am a slave!"

    def get_master(self):
        resp = requests.get('http://127.0.0.1:6543/master').json()
        return json['master']

    def register(self):
        print "I'm registering with the server."
        resp = requests.post('http://127.0.0.1:6543/register',
            json={'node_id':self.node_id}).json()

        if resp['registered'] == False:
            print "[ERROR] I'm not sure what happend, honestly."
            sys.exit(-1)
        else:
            return True

    def make_edit(self):
        print "I'm taking my turn and making an edit."

    def request_access(self):
        print "I'm seeing if I can edit yet."
        return False

def become_master():
    master = Master()
    master.register()


def become_slave(slave):
    while(slave.running):
        if slave.request_access():
            make_edit()
        else:
            pass
        print "I've done my thing, going to sleep for a second to simulate... I dunno... something?"
        time.sleep(1)

if __name__ == '__main__':
    slave = Slave()

    if slave.register():
        slave.try_master()
        if slave.is_master:
            become_master()

        else:
            become_slave(slave)