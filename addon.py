#!/usr/bin/python3
'''
    Envia comandos ao XBMC. 
'''

from importlib import util
import threading
import subprocess
import socket
import sys
import os

os.chdir( os.path.join(os.path.dirname(os.path.abspath(__file__))) )
xbmc_path = util.find_spec("xbmc")
if xbmc_path:
    import xbmc


def mPrint(msg):
    if xbmc_path:
        xbmc.log(msg, level=xbmc.LOGINFO)
    else:
        print(msg)#, io sys.stderr)

def Notificar(msg):
    if xbmc_path:
        xbmc.executebuiltin("xbmc.Notification(Rasperry TV Alexa, %s)" % msg)


def lancar_servico():
    t1 = threading.Thread(
        target= lambda: subprocess.call('python3 servico.py %d' % os.getpid(), shell=True, cwd=os.path.dirname(os.path.abspath(__file__)))
    )
    t1.start()

if __name__ == '__main__':
    if xbmc_path:
        mPrint("XBMC= %s" % str(xbmc_path))
        
    Notificar("Iniciando servico.")

    mPrint("Script atual: %s | CWD= %s\n" % (os.path.abspath(__file__), os.path.abspath(os.getcwd())))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_address = ('localhost', 10001)
    mPrint('ADDON> Iniciando em %s:%s' % server_address)
    sock.bind(server_address)

    lancar_servico()
    Notificar("Iniciado.")
    mPrint("ADDON> Servico pronto.")

    sock.listen(1) 
    while True:
        connection, client_address = sock.accept()
        try:
            # mPrint('ADDON> Conexao: %s' % str(client_address))
            data = connection.recv(1024)
            if not data:
                mPrint("ADDON> ERR")
            else:
                mPrint("ADDON> RECV: %s" % str(data))
                if "xbmc." in str(data):
                    xbmc.executebuiltin(data)
        finally:
            # mPrint("ADDON> FINAL")
            # Clean up the connection
            connection.close()