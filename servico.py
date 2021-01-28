#!/usr/bin/python3
'''
    Recebe comandos da Alexa.
    Repassa ao servidor do Addon.
'''
# sudo apt-get install python3-websockets
# sudo apt-get install python3-pip
#

import socket
import sys
import os

from localclientwrapper import ClientWrapper
from lib import TV
from config.credentials import appKey,secretKey
from config.credentials import myTv



def check_alive():
    try:
        os.kill(int(sys.argv[1]), 0)
    except OSError:
        print("pid is unassigned")
        exit(1)


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
    print("SERVICE> tv_powerState=",arg)
    return True,arg[0]

def tv_setVolume(arg):
    check_alive()
    envia_msg('xbmc.SetVolume(%d, true)' % arg[0])
    # xbmc.executebuiltin()
    print("SERVICE> tv_setVolume=",arg)
    return True, arg[0]
    
def tv_adjustVolume(arg):
    check_alive()
    envia_msg('ALEXA: Recebido (VOL): %s' % str(arg[0]))
    print("SERVICE> tv_adjustVolume=",arg)
    return True, arg[0]

def tv_setMute(arg):
    check_alive()
    global tvMuted
    if tvMuted != arg[0]:
        envia_msg('xbmc.Mute')
        # xbmc.executebuiltin('xbmc.Mute')
        tvMuted = arg[0]

    print("SERVICE> tv_setMute=",arg)
    return True, arg[0]

def tv_mediaControl(arg):
    check_alive()
    # https://kodi.wiki/view/List_of_built-in_functions#Player_built-in.27s
    if str(arg[0]).lower() == "play":
        envia_msg('xbmc.PlayerControl(Play)')
    elif str(arg[0]).lower() == "pause":
        envia_msg('xbmc.PlayerControl(Play)')
    elif str(arg[0]).lower() == "stop":
        envia_msg('xbmc.PlayerControl(Stop)')

    elif str(arg[0]).lower() == "next":
        envia_msg('xbmc.PlayerControl(Next)')
        # xbmc.executebuiltin('xbmc.PlayerControl(Next)')
    elif str(arg[0]).lower() == "previous":
        envia_msg('xbmc.PlayerControl(Previous)')
        # xbmc.executebuiltin('xbmc.PlayerControl(Previous)')

    elif str(arg[0]).lower() == "forward":
        envia_msg('xbmc.PlayerControl(Forward)')
        # xbmc.executebuiltin('xbmc.PlayerControl(Forward)')
    elif str(arg[0]).lower() == "rewind":
        envia_msg('xbmc.PlayerControl(Rewind)')
        # xbmc.executebuiltin('xbmc.PlayerControl(Rewind)')
    else:
        envia_msg('ALEXA: Recebido: %s' % str(arg[0]))
    print("SERVICE> tv_mediaControl=",arg)
    return True, arg[0]

def tv_selectInput(arg):
    check_alive()
    print("SERVICE> tv_selectInput=",arg)
    return True, arg[0]

def tv_changeChannel(arg):
    check_alive()
    envia_msg('ALEXA: Recebido: %s' % str(arg[0]))
    print("SERVICE> tv_changeChannel=",arg)
    return True, arg[0]

def tv_skipChannels(arg):
    check_alive()
    print("SERVICE> tv_skipChannels=",arg)
    return True, arg[0]


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("SERVICE> Inicializacao invalida!")
        exit(1)
    print("SERVICE> PID %s" % sys.argv[1])
    check_alive()


    tv = TV(myTv)
    tv.powerState(tv_powerState)
    tv.setVolume(tv_setVolume)
    tv.adjustVolume(tv_adjustVolume)
    tv.setMute(tv_setMute)
    tv.mediaControl(tv_mediaControl)
    tv.selectInput(tv_selectInput)
    tv.changeChannel(tv_changeChannel)
    tv.skipChannels(tv_skipChannels)


    devices = [tv]

    wrap = ClientWrapper(devices, appKey, secretKey)
    wrap.start()