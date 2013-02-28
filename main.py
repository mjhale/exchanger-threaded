#! /usr/bin/python

# Author: Michael Hale
# Date: February 27, 2013
# Homework 3
# CSCI 331 Spring 2013
# Reference: http://www.cs.unca.edu/brock/classes/Spring2013/csci331/notes/networkingserver.html

import re
import socket
import thread

def handleConnection(strm, addr, lock):
    pattern = re.compile('^SWAP\s(\S+)\sUSING\s(\S+)\n$')
    instrm = strm.makefile('r')
    outstrm = strm.makefile('w')
    line = instrm.readline()

    while line:
        lock.acquire()
        print addr, ":", line
        match = pattern.match(line)
        if (match == None):
            repl = 'Bad Syntax'
        else:
            repl = ' '.join(['RETURN', match.group(1), 'USING', match.group(2)])
        outstrm.write(repl+'\n\r')
        outstrm.flush()
        line = instrm.readline()
        lock.release()
    instrm.close()
    outstrm.close()
    strm.close()
    print "Connection closed at", addr

def serverCAS():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
        sock.bind(('', 33101))
        sock.listen(1)

        while True:
            strm, addr = sock.accept()
            try:
                lock = thread.allocate_lock()
                thread.start_new_thread(handleConnection, (strm, addr, lock))
            except:
                print "Unable to start thread", addr
                strm.close()
    except KeyboardInterrupt: 
        print 'Exit'
        sock.close()

if __name__ == "__main__":
    serverCAS()
