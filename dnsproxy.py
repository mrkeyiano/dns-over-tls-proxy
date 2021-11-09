#!/usr/bin/python3

import socket, threading, socketserver
from dnslib import *
import ssl, struct, sys, certifi

DNS_PORT=9999
DNS_HOST="0.0.0.0"

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):

    # override socketserver.UDPServer

    #Bonus point
    #Allow multiple incoming requests at the same time
    def __init__(self, server_address, RequestHandlerClass):

        socketserver.UDPServer.__init__(self,server_address,RequestHandlerClass)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):

        #override socketserver.TCPServer

        #Bonus point
        #Allow multiple incoming requests at the same time
		daemon_threads = True
		allow_reuse_address = True

		def __init__(self, server_address, RequestHandlerClass):
			socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)




class UDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        (req_data,req_socket) = self.request
        try:
            # parse DNS request using dnslib
            d = DNSRecord.parse(req_data)

        except Exception:
            print("%s: ERROR: Invalid DNS request" % self.client_address[0])
        else:
            #connect to cloudflare DoT on port 853
            upstream_response = dns_over_tls_query(req_data)
            req_socket.sendto(upstream_response, self.client_address)


class TCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)

        # Remove the addition "length" parameter used in the
        # TCP DNS protocol
        req_data = data[2:]


        try:
            # parse DNS request using dnslib
            d = DNSRecord.parse(req_data)
 
        except Exception:
            print("%s: ERROR: Invalid DNS request" % self.client_address[0])
        else:

            #connect to cloudflare DoT on port 853
            response = dns_over_tls_query(req_data)

            #return response to client
            length = binascii.unhexlify("%04x" % len(response))
            self.request.sendall(length+response)

def dns_over_tls_query(request):

    host="1.0.0.1"
    port=853
    hostname="cloudflare-dns.com"

    # prepend 2-byte length
    request = struct.pack("!H", len(request)) + request

    #initate socket obJect
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    response = ""

    #wrap socket in ssl for TLS connection

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.load_verify_locations(cafile=certifi.where())
    conn = ssl_context.wrap_socket(s, server_hostname=hostname)

    try:
        #connect to cloudflare DoT
        conn.connect((host, port))
    except socket.error as e:
        print("socket error: %s" % e)
    except ssl.SSLError as e:
        print("TLS error: %s" % e)
    else:
        #connection successful, forward client request to cloudflare
        conn.sendall(request)

        lbytes = recvSocket(conn, 2)

        if (len(lbytes) != 2):
            raise ErrorMessage("recv() on socket failed.")
        # unpack from the buffer
        resp_len, = struct.unpack('!H', lbytes)
        response = recvSocket(conn, resp_len)

    finally:
        #always close connection
        conn.close()

    return response


def recvSocket(s, numOctets):
    """Read and return numOctets of data from a connected socket"""
    response = b""
    octetsRead = 0
    while (octetsRead < numOctets):
        chunk = s.recv(numOctets-octetsRead)
        chunklen = len(chunk)
        if chunklen == 0:
            return b""
        octetsRead += chunklen
        response += chunk
    return response





if __name__ == "__main__":

    args=sys.argv
    protocol=""


    if len(args)>1:
        protocol=args[1]


    HOST, PORT = DNS_HOST, DNS_PORT

    #Bonus points
    #Add support for udp & tcp connections

    if protocol == "udp":
        print("[*] DNSProxy is running in UDP mode")
        server = ThreadedUDPServer((HOST, PORT), UDPHandler)

    else:
        print("[*] DNSProxy is running in TCP mode")
        server = ThreadedTCPServer((HOST, PORT), TCPHandler)


    print("[*] DNSProxy started on "+HOST+":"+str(PORT))
    server.serve_forever()

