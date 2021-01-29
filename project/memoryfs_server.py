# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 15:09:35 2020

@author: Jonathan
"""

# Block size (in Bytes)
import hashlib
from sys import argv
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from memoryfs_client import BLOCK_SIZE,TOTAL_NUM_BLOCKS

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


def main(argv):
  if len(argv)!=2 and len(argv)!=3:
      print ('server need one argument for port or two arguments for port and corrupt block')
      return
#  data=0
  
  block = []
  checksum=[]
  for i in range (0, TOTAL_NUM_BLOCKS):
      putdata = bytearray(BLOCK_SIZE)
      block.insert(i,putdata)
      checksum.insert(i,hashlib.md5(bytes(str(putdata),'utf-8')).digest())

  # Create server
  print ('running on port ',int(argv[1]))
  server = SimpleXMLRPCServer(('127.0.0.1', int(argv[1])),
                        requestHandler=RequestHandler) 

  ifCorrupt=False
  if len(argv)==3:
      ifCorrupt=True
      corruptBlock=int(argv[2])

  def Put(block_number, block_data):
    block[block_number] = block_data
    checksum[block_number] = hashlib.md5(block_data.data).digest()
    #print (checksum)
    return 0

  server.register_function(Put, 'Put')

  def Get(block_number):
    Flag=False if hashlib.md5(bytes(str(block[block_number]),'utf-8'))!=checksum[block_number] else True
    if ifCorrupt and block_number==corruptBlock:
        return bytearray(BLOCK_SIZE),True
    return block[block_number],Flag


  server.register_function(Get, 'Get')

  # Run the server's main loop
  server.serve_forever()

if __name__ == "__main__":
  main(argv)
