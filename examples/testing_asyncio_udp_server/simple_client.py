#!/usr/bin/env python3
import asyncio

hostName = 'localhost'
port = 12345

class WIotDatabaseClientProtocol:
	def __init__( self, message, loop ):
		self.message = message
		self.loop = loop
		self.transport = None

	def connection_made( self, transport ):
		self.transport = transport
		print( 'Send:', self.message )
		self.transport.sendto( self.message.encode() )
		
loop = asyncio.get_event_loop()
message = "Hello World!"
connect = loop.create_datagram_endpoint( lambda : WIotDatabaseClientProtocol( message, loop ), 
											remote_addr=( hostName, port ) )
transport, protocol = loop.run_until_complete( connect )
loop.run_forever()
transport.close()
loop.close()
