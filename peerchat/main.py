import sys
from peerbase import Node
import json
import time

try:
    cfg = sys.argv[1]
except IndexError:
    raise IndexError('Please include a path to a config file.')

with open(cfg, 'r') as f:
    conf = json.load(f)

chatnode = Node(
    conf['node_name'],
    conf['network'],
    conf['key'],
    ports=conf['ports'],
    servers=conf['remotes'],
    use_local=False
)

def recv_msg(node, args, kwargs):
    print(f'{kwargs["node_name"]} @ [{str(time.ctime())}] >>> {str(kwargs["message"])}')
    return {'result':'success'}

chatnode.register_command('recv',recv_msg)
chatnode.start_multithreaded()

while len(chatnode.peers.keys()) == 0 and len(chatnode.remote_peers.keys()) == 0:
    print('Waiting for peers.')
    time.sleep(2)

print('Ready to connect.')

while True:
    msg = input('')
    print(f'{chatnode.name} (self) @ [{str(time.ctime())}] >>> {msg}')
    res = chatnode.command(command_path='recv', kwargs={'node_name':chatnode.name, 'message':msg})
    while len(chatnode.peers.keys()) == 0 and len(chatnode.remote_peers.keys()) == 0:
        print('Waiting for peers.')
    time.sleep(2)