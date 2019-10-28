#!/usr/bin/python2.7

import ari
import logging
import json

logging.basicConfig(level=logging.ERROR)

client = ari.connect('http://localhost:8088/', 'mell', '123456')

def on_dtmf(channel, event):
    digit = event['digit']
    if digit == '#':
        channel.play(media='sound:goodbye')
        channel.continueInDialplan()
    elif digit == '*':
        channel.play(media='sound:asterisk-friend')
    else:
        channel.play(media='sound:digits/%s' % digit)


def on_start(channel, event):
	channel = channel.get('channel')
	print(channel)
	#print channel.get('id')
	#print(event)
	channel.play(media='sound:hello-world')
	channel.on_event('ChannelDtmfReceived', on_dtmf)
	channel.answer()


client.on_channel_event('StasisStart', on_start)
client.run(apps="hello")
