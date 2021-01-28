#!/usr/bin/python
'''
    Envia comandos ao XBMC. 
'''
# sudo apt-get install python3-websockets
# sudo apt-get install python3-pip
# 

import threading
import subprocess
import socket
import sys
import os

import xbmc

def mPrint(msg):
    if xbmc:
        xbmc.log(msg, level=xbmc.LOGNOTICE)
    else:
        print >> sys.stderr, msg

def Notificar(msg):
    xbmc.executebuiltin("xbmc.Notification(Rasperry TV Alexa, %s)" % msg)

def instalar_programas():
    ret = subprocess.call('sudo apt-get install python3-pip python3-websockets && pip3 install sinricpro', shell=True)
    mPrint("ADDON> Pacotes r=%s" % str(ret))

def lancar_servico():
    instalar_programas()
    t1 = threading.Thread(
        target= lambda: subprocess.call('python3 servico.py %d' % os.getpid(), shell=True, cwd=os.path.dirname(os.path.abspath(__file__)))
    )
    t1.start()
    mPrint("ADDON> Servico lancado.")
    # os.system('python3 servico.py %d' % os.getpid())

if __name__ == '__main__':
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