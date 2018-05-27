#!/usr/bin/env python3
#######################################################################################
#
#	Copyright (c) 2018, Wiphoo (Terng) Methachawalit, All rights reserved.
#
#######################################################################################


#######################################################################################
#
#	STANDARD IMPORTS
#

import sys

from optparse import OptionParser

import asyncio

#######################################################################################
#
#	LOCAL IMPORTS
#


#######################################################################################
#
#	PROGRAM DEFENITIONS
#

#	version of this program
Version = '0.1b'

#	program usage, it is a string of an example for how to use this program with arugments
ArgsUsage = '<HOSTNAME> <PORT>'

#	number of required arugments
NumRequiredArgs = 2

#######################################################################################
#
#	GLOBAL VARIABLES
#


#######################################################################################
#
#	HELPER FUNCTIONS
#


#######################################################################################
#
#	CLASS DEFINITIONS
#

class WIotDatabaseServerProtocol( asyncio.DatagramProtocol ):
	''' Subclass from asyncio to implement our own UDP protocol
			The base class for implementing datagram protocols
		(for use with e.g. UDP transports). 
	'''
	
	def connection_made( self, transport ):
		''' Called when a connection is made.

			The transport argument is the transport representing the connection. 
				You are responsible for storing it somewhere (e.g. as an attribute) if you need to.
		'''
		print( 'WIotDatabaseServerProtocol.connection_made( transport = {} )'.format( transport ) )
		
		#	call base class
		asyncio.DatagramProtocol.connection_made( self, transport )
		
	def connection_lost( self, exc ):
		''' Called when the connection is lost or closed.

			The argument is either an exception object or None. The latter means a regular EOF is received, 
				or the connection was aborted or closed by this side of the connection.
		'''
		
		print( 'WIotDatabaseServerProtocol.connection_lost( exc = {} )'.format( exc ) )
		
		#	call base class
		asyncio.DatagramProtocol.connection_lost( self, transport )
	
	def datagram_received( self, data, addr ):
		''' Called when a datagram is received. 
				data is a bytes object containing the incoming data. 
				addr is the address of the peer sending the data; 
				the exact format depends on the transport.
		'''
		print( 'WIotDatabaseServerProtocol.datagram_received( data = {}, addr = {} )'.format( data, addr ) )
		
	def error_received( self, exc ):
		''' Called when a previous send or receive operation raises an OSError. 
				exc is the OSError instance.

			This method is called in rare conditions, 
				when the transport (e.g. UDP) detects that a datagram couldn't be delivered to its recipient. 
				In many conditions though, undeliverable datagrams will be silently dropped.
		'''
		
		print( 'WIotDatabaseServerProtocol.error_received( exc = {} )'.format( exc ) )
		


#######################################################################################
#
#	MAIN
#


def main():
	''' main function of this program '''
	
	###################################################################################
	#	options parsing

	usage = 'usage: %prog [options] {!r}'.format( ArgsUsage )
	parser = OptionParser( usage=usage, version=Version )
	parser.add_option( '-v', '--verbose',
							action='store_true', dest='verbose', default=True )
	( options, args ) = parser.parse_args()
	
	#	check the required arguments
	if len( args ) != NumRequiredArgs:
	#	the given arguments is not equals the required arguments,
	#		so print the error meessage and exit
		parser.error( 'incorrect number of arguments.' )
		sys.exit( -1 )
	
	###################################################################################
	#	parse arguments / options
	
	hostName = args[0]
	port = args[1]
	
	###################################################################################
	#	main
	
	print( '   host name = {}, port = {}'.format( hostName, port ) )
	
	#	construct the main asyncio event loop
	loop = asyncio.get_event_loop()
	print( 'Starting UDP server........' )
	
	#	One protocol instance will be created to serve all client requests
	listen = loop.create_datagram_endpoint( WIotDatabaseServerProtocol, 
											local_addr=( hostName, port ) )
	transport, protocol = loop.run_until_complete( listen )

	try:
		loop.run_forever()
	except KeyboardInterrupt:
		pass
	
	#	close
	transport.close()
	loop.close()

if __name__ == "__main__":
	#	call main function
	main()
