import socket


class ipHelper:

    def getLocalIP(self):
        myname = socket.getfqdn(socket.gethostname())
        myaddr = socket.gethostname(myname)
        return myaddr