#!/usr/bin/env python
import sys
import argparse
from RCubic.RCubicServer import RCubicServer
from RCubic.BotClient import BotClient

# Command line arguments
parser = argparse.ArgumentParser(description='Ask bot to query users and block until timeout or until all replies recieved')
parser.add_argument('--lport', dest='lport', default=8002, help='listen port for callback', type=int)
parser.add_argument('--lrange', dest='lrange', default=None, metavar='P', help='listen port range for callback', type=int, nargs=2)
parser.add_argument('--laddr', dest='laddr', default='0.0.0.0', help='listen address', type=str)
parser.add_argument('--lkey', dest='lkey',default=None, help='listen private key', type=str)
parser.add_argument('--lcert', dest='lcert', default=None, help='listen certificate', type=str)
parser.add_argument('--baddr', dest='baddr', default='127.0.0.1', help='bot address', type=str)
parser.add_argument('--blport', dest='blport', default='8001', help='bot listen port', type=int)
parser.add_argument('--cacert', dest='cacert', default=None, help='CACert to auth server', type=str)
parser.add_argument('--token', dest='token', default='', help='used to auth with bot server', type=str)
parser.add_argument('--name', dest='name', required=True, help='unique checkInName for callbacks', type=str)
parser.add_argument('--message', '-m', dest='message', default=None, help='message to send to the users', type=str)
parser.add_argument('--timeout', '-t', dest='timeout', default=3600, help='timeout for checkin in seconds', type=int)
parser.add_argument('--room', '-r', dest='room', default=None, help='ask for all users in room to checkin', type=str)
parser.add_argument('--anyuser', dest='anyuser', action='store_true', help='any user can send back confirmation')
parser.add_argument('--server', '-s', dest='server', required=True, default='localhost', help='xmpp server domain', type=str)
parser.add_argument('--users', '-u', dest='users', required=False, metavar='U', type=str, nargs='+', help='users to contact')
args = parser.parse_args()

# Start server and bot client
server = RCubicServer(bind=args.laddr, port=args.lport, portRange=args.lrange, SSLKey=args.lkey, SSLCert=args.lcert, token=args.token)
client = BotClient(server=args.baddr, port=args.blport, CACert=args.cacert, token=args.token)
client.registerRESTServer(server)
# Don't block so that we can execute check in
server.start(block=False)
# Block until users respond to check in
checks = client.requestUserCheckIn(args.users, args.name, args.message, args.server, args.lport, room=args.room, anyuser=args.anyuser, timeout=args.timeout)
server.stop()
if checks:
    sys.exit(0)
else:
    sys.exit(1)
