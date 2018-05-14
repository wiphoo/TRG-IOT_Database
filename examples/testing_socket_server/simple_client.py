#!/usr/bin/env python3

import sys
import socket

#	server host name and port
ServerHostName = 'localhost'
ServerPort = 12345

data = " ".join( sys.argv[1:] )

# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto().
sock.sendto( bytes( data + '\n', 'utf-8' ), ( ServerHostName, ServerPort ) )
received = str( sock.recv( 1024 ), 'utf-8' )

print( 'Sent:     {}'.format( data ) )
print( 'Received: {}'.format( received ) )
