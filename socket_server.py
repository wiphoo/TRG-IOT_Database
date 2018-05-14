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

import socketserver

#######################################################################################
#
#	LOCAL IMPORTS
#


#######################################################################################
#
#	PROGRAM DEFENITIONS
#

#	version of this program
Version = '0.1'

#	program usage, it is a string of an example for how to use this program with arugments
ArgsUsage = ''

#	number of required arugments
NumRequiredArgs = 0

#######################################################################################
#
#	GLOBAL VARIABLES
#

#	define default server host name and port
DefaultServerHostName = 'localhost'
DefaultServerPort = 12345

#######################################################################################
#
#	HELPER FUNCTIONS
#


#######################################################################################
#
#	CLASS DEFINITIONS
#

class RequestHandler( socketserver.BaseRequestHandler ):
	''' This class is designed for handle the request from client for our server
	
		The request handler class must define a new handle() method, 
			and can override any of the following methods. 
			A new instance is created for each request.
			
			
		This class works similar to the TCP handler class, except that
		    self.request consists of a pair of data and client socket, and since
		    there is no connection the client address must be given explicitly
		    when sending data back via sendto().
	'''

	def handle( self ):
		''' override handle function from base class.
			This function must do all the work required to service a request,
				for datagram services, self.request is a pair of string and socket.
		'''
		
		print( 'self.request = {}'.format( self.request ) )
		print( 'self.client_address = {}'.format( self.client_address ) )
		
		#	extract data string and socket from the self.request
		( data, socket ) = self.request
		
		
#warning for testing only
		data = self.request[0].strip()
		socket = self.request[1]
		socket.sendto( data.upper(), self.client_address )


#######################################################################################
#
#	MAIN
#


def main():
	''' main function of this program '''
	
	###################################################################################
	#	options parsing

	usage = 'usage: %prog [options]'
	parser = OptionParser( usage=usage, version=Version )
	parser.add_option( '-v', '--verbose',
							action='store_true', dest='verbose', default=True )
	parser.add_option( '--serverHostName', 
							dest='serverHostName',
							default=DefaultServerHostName,
							help='a host name to serve this socket server [default: %default]' )
	parser.add_option( '--serverPort',
							dest='serverPort',
							default=DefaultServerPort,
							help='a port to serve this socket server [default: %default]' )	
	( options, args ) = parser.parse_args()
	
	#	check the required arguments
	if len( args ) != NumRequiredArgs:
	#	the given arguments is not equals the required arguments,
	#		so print the error meessage and exit
		parser.error( 'incorrect number of arguments.\n {!r}'.format( usage ) )
		sys.exit( -1 )
	
	###################################################################################
	#	parse arguments / options
	
	#	server host name and port
	serverHostName = options.serverHostName
	serverPort = options.serverPort
	
	print( 'serverHostName = {}'.format( serverHostName ) )
	print( 'serverPort = {}'.format( serverPort ) )
		
	###################################################################################
	#	program start here
	
	#	create the UDP socket server with given hostname and port
	#		bind then request handler to RequestHandler class
	server = socketserver.UDPServer( ( serverHostName, serverPort ), RequestHandler )
	
	#	run server forever
	server.serve_forever()

if __name__ == "__main__":
	#	call main function
	main()
