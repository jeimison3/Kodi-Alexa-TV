#!/usr/bin/python3
'''
    Recebe comandos da Alexa.
    Repassa ao servidor do Addon.
'''

import socket
import sys
import os

os.chdir( os.path.join(os.path.dirname(os.path.abspath(__file__))) )
sys.path.append( os.path.join("lib", "websockets-8.1", "src") ) # https://pypi.org/project/websockets/#files
sys.path.append( os.path.join("lib", "loguru") )
sys.path.append( os.path.join("lib", "sinricprosdk") )

from localclientwrapper import ClientWrapper
from lib import TV
# from config.credentials import appKey,secretKey
# from config.credentials import myTv



def check_alive():
    try:
        os.kill(int(sys.argv[1]), 0)
    except OSError:
        print("pid is unassigned")
        exit(1)

def printLog(msg):
    print(msg)
    envia_msg('LOG: %s' % msg)
'''
Funcoes para envio dos comandos para o Addon
'''

def envia_msg(msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 10001)
    sock.connect(server_address)
    try:
        # print('SERVICE> Enviando: "%s"' % msg)
        sock.send(msg.encode())

    finally:
        pass
        # print('SERVICE> Fechando socket.')
        # sock.close()

'''
Implemented functions for TV
'''

tvMuted = False

def tv_powerState(arg):
    check_alive()
    if arg[0] == "Off":
        envia_msg('Shutdown')
    printLog("SERVICE> tv_powerState= %s" % str(arg))
    return True,arg[0]

def tv_setVolume(arg):
    check_alive()
    envia_msg('SetVolume(%d, true)' % arg[0])
    # xbmc.executebuiltin()
    printLog("SERVICE> tv_[set/adjust]Volume=%s" % str(arg))
    return True, arg[0]
    
def tv_setMute(arg):
    check_alive()
    global tvMuted
    if tvMuted != arg[0]:
        envia_msg('Mute')
        # xbmc.executebuiltin('xbmc.Mute')
        tvMuted = arg[0]
    printLog("SERVICE> tv_setMute=%s" % str(arg))
    return True, arg[0]

def tv_mediaControl(arg):
    check_alive()
    # https://kodi.wiki/view/List_of_built-in_functions#Player_built-in.27s
    if str(arg[0]).lower() == "play":
        envia_msg('Play')
    elif str(arg[0]).lower() == "pause":
        envia_msg('Pause')
    elif str(arg[0]).lower() == "stop":
        envia_msg('Stop')

    elif str(arg[0]).lower() == "next":
        envia_msg('PlayerControl(Next)')
        # xbmc.executebuiltin('xbmc.PlayerControl(Next)')
    elif str(arg[0]).lower() == "previous":
        envia_msg('PlayerControl(Previous)')
        # xbmc.executebuiltin('xbmc.PlayerControl(Previous)')

    elif str(arg[0]).lower() == "forward":
        envia_msg('PlayerControl(Forward)')
        # xbmc.executebuiltin('xbmc.PlayerControl(Forward)')
    elif str(arg[0]).lower() == "rewind":
        envia_msg('PlayerControl(Rewind)')
        # xbmc.executebuiltin('xbmc.PlayerControl(Rewind)')
    # else:
        # envia_msg('ALEXA: Recebido: %s' % str(arg[0]))
    printLog("SERVICE> tv_mediaControl=%s" % str(arg))
    return True, arg[0]

def tv_selectInput(arg):
    check_alive()
    printLog("SERVICE> tv_selectInput=%s" % str(arg))
    return True, arg[0]

def tv_changeChannel(arg):
    check_alive()
    # envia_msg('ALEXA: Recebido: %s' % str(arg[0]))
    printLog("SERVICE> tv_changeChannel=%s" % str(arg))
    return True, arg[0]

def tv_skipChannels(arg):
    check_alive()
    printLog("SERVICE> tv_skipChannels=%s" % str(arg))
    return True, arg[0]


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("SERVICE> Inicializacao invalida!")
        exit(1)
    print("SERVICE> PID %s" % sys.argv[1])
    check_alive()


    tv = TV(sys.argv[4])
    tv.powerState(tv_powerState)
    tv.setVolume(tv_setVolume)
    tv.adjustVolume(tv_setVolume)
    tv.setMute(tv_setMute)
    tv.mediaControl(tv_mediaControl)
    tv.selectInput(tv_selectInput)
    tv.changeChannel(tv_changeChannel)
    tv.skipChannels(tv_skipChannels)


    devices = [tv]

    wrap = ClientWrapper(devices, sys.argv[2], sys.argv[3])
    wrap.start()