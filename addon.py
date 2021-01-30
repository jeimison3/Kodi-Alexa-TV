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
xbmc_path = util.find_spec("kodi_six")
if xbmc_path:
    from kodi_six import xbmc, xbmcaddon, xbmcplugin, xbmcgui


def mPrint(msg):
    if xbmc_path:
        xbmc.log(msg, level=xbmc.LOGINFO)
    else:
        print(msg)

def Notificar(msg):
    if xbmc_path:
        xbmc.executebuiltin("Notification(Kodi Alexa TV, %s)" % msg)


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
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
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
            data = connection.recv(1024)
            if not data:
                mPrint("ADDON> ERR")
            else:
                receive = data.decode("utf-8")
                mPrint("ADDON> RECV: %s" % receive)
                # https://codedocs.xyz/AlwinEsch/kodi/class_x_b_m_c_addon_1_1xbmc_1_1_player.html
                if receive == "Play":
                    if xbmc.Player().isPlaying():
                        xbmc.Player().pause()
                    else:
                        xbmc.Player().play()
                elif receive == "Pause":
                    xbmc.Player().pause()
                elif receive == "Stop":
                    xbmc.Player().stop()
                else:
                    xbmc.executebuiltin(receive)
        finally:
            connection.close()