#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#Принимаем звонок, играем гудки 8 секунд, пототм делаем hangup
#
import ari
import logging
import threading
import uuid

logging.basicConfig(level=logging.ERROR)

client = ari.connect('http://10.248.52.139:8088', 'mell', '123456')

channel_timers = {}


def stasis_end_cb(channel, ev):
    """Handler for StasisEnd event"""

    print "Channel %s just left our application" % channel.json.get('name')
    timer = channel_timers.get(channel.id)
    if timer:
        timer.cancel()
        del channel_timers[channel.id]


def stasis_start_cb(channel_obj, ev):
    """Handler for StasisStart event"""

    def answer_channel(channel, playback):
        """Callback that will actually answer the channel"""
        # print channel.id
        # channel.play(media='sound:asterisk-friend')
        print "Answering channel %s" % channel.json.get('name')
        playback.stop()
        channel.answer()

        timer = threading.Timer(1, hangup_channel, [channel])
        channel_timers[channel.id] = timer
        timer.start()

    def hangup_channel(channel):
        """Callback that will actually hangup the channel"""
        print "Hanging up channel %s" % channel.json.get('name')
        channel.hangup()

    channel = channel_obj.get('channel')
    print "Channel %s has entered the application" % channel.json.get('name')

    playback_id = str(uuid.uuid4())
    # print(playback_id)
    print "Playing beep tones to channel: %s" % channel.json.get('name')
    playback = channel.playWithId(playbackId=playback_id,
                                  media='tone:ring')
    timer = threading.Timer(8, answer_channel, [channel, playback])
    channel_timers[channel.id] = timer
    timer.start()


client.on_channel_event('StasisStart', stasis_start_cb)
client.on_channel_event('StasisEnd', stasis_end_cb)

client.run(apps='channel-tones')