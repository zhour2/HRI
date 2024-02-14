from __future__ import print_function

import sys
import subprocess
import argparse
import shutil
import signal
from config import RobotConfig
from src import robot, sequence
from src.server import server
from src import server as srvr
import threading
import re
from serial.serialutil import SerialException
from pypot.dynamixel.controller import DxlError
import random
import time
import uuid
import requests
import logging
import gesture_loader
import os
import socket


current_dir = os.path.dirname(os.path.realpath(__file__))
gesture_config_filename = 'gestures.config'

gesture_config_path = os.path.join(current_dir, gesture_config_filename)

gesture_config = gesture_loader.load_config(gesture_config_path)

master_robot = None
robots = []
second_robot = None
speed = 1.0
amp = 1.0
post = 0.0

loaded_seq = []

class SequenceRobot(robot.Robot):
    def __init__(self, name, config):
        br = 57600
        super(SequenceRobot, self).__init__(config, br, name)
        self.config = config
        self.seq_thread = self.seq_stop = None
        self.rec_thread = self.rec_stop = None

        self.load_seq()

        self.speed = 1.0
        self.amp = 1.0
        self.post = 0.0
    
    def load_seq(self):
        seq_dir = os.path.join(current_dir, './src/sequences/%s' % self.name)

        if not os.path.exists(seq_dir):
            print("seq_dir not existed.")
            os.makedirs(seq_dir)

        seq_names = os.listdir(seq_dir)
        seq_names.sort()

        for seq in seq_names:
            subseq_dir = seq_dir + '/' + seq

            if (seq[-5:] == '.json' and subseq_dir not in loaded_seq):
                self.load_sequence(subseq_dir)
            elif os.path.isdir(subseq_dir) and not ('ignore' in subseq_dir):
                for s in os.listdir(subseq_dir):
                    seq_name = "%s\%s"%(subseq_dir,s)
                    if (s[-5:] == '.json' and seq_name not in loaded_seq):
                        self.load_sequence(seq_name)
    def assign_time_length(self, keys, vals):
        timeMap = [None] * len(keys)
        for i in range(0, len(keys)):
            frameLst = vals[i].frames
            if len(frameLst) != 0:
                timeAmnt = frameLst[-1].millis
                timeMap[i] = [keys[i], str(timeAmnt / 1000)]
        return timeMap

    def get_time_sequence(self):
        tempKeys = list(self.seq_list.keys())
        tempVals = list(self.seq_list.values())
        tempMap = self.assign_time_length(tempKeys, tempVals)
        return tempMap

    def get_sequences(self):
        return self.seq_list.keys()

    def play_seq_json(self, seq_json):
        seq = sequence.Sequence.from_json_object(seq_json, rad=True)
        self.seq_stop = threading.Event()
        self.seq_thread = robot.sequence.SequencePrimitive(
            self, seq, self.seq_stop, speed=speed, amp=amp, post=post)
        self.seq_thread.seq

        return self.seq_thread
    
    def play_recording(self, seq, idler=False, speed=speed, amp=amp, post=post):
        self.seq_stop = threading.Event()

        if ('idle' in seq):
            seq = seq.replace('idle', '').replace(' ', '').replace('/', '')
            idler = True
        
        self.seq_thread = robot.sequence.SequencePrimitive(
            self, self.seq_list[seq], self.seq_stop, idler=idler, speed=self.speed, amp=self.amp, post=self.post)
        self.seq_thread.start()

        return self.seq_thread

    def start_recording(self):
        self.rec_stop = threading.Event()

        self.rec_thread = robot.sequence.RecorderPrimitive(self, self.rec_stop)
        self.rec_thread.start()

def parse_args(args):
    """
    Parse arguments from starting in terminal
    args:
        args    the arguments from terminal
    returns:
        parsed arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--names', '-n', type=str, nargs='+',
                        help='Name of the robot.', default=["woody"])
    parser.add_argument('--port', '-p', type=int,
                        help='Port to start server on.', default=8000)
    parser.add_argument('--host', '-i', type=str, help='IP address of webserver',
                        default=srvr.get_ip_address())
    parser.add_argument('--browser-disable', '-b',
                        help='prevent a browser window from opening with the blossom UI', 
                        action='store_true')
    parser.add_argument('--list-robots', '-l',
                        help='list all robot names', action='store_true')
    return parser.parse_args(args)

def start_server(host, port, hide_browser):
    import prettytable as pt
    sentence = "%s:%d" % (host, port)
    width = 26

    t = pt.PrettyTable()

    t.field_names = ['IP ADDRESS']
    [t.add_row([sentence[i:i + width]]) for i in range(0, len(sentence), width)]
    print(t)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = "127.0.0.1"
    sock.bind((host, port))

    print(f"Listening for UDP messags on {host}:{port}...")
    try:
        while True:
            data, addr = sock.recvfrom(1024)

            try:
                message = int(data.decode())
                gesture = gesture_loader.getGesture(gesture_config, message)
                print(f"Gesture Triggered: {gesture}")
                handle_input(master_robot, gesture)
            except ValueError:
                print("Received non-integer message")
    except KeyboardInterrupt:
        print("UDP server is shutting down.")
    finally:
        sock.close()

last_cmd, last_args = 'rand', []

def handle_input(robot, cmd, args=[]):
    global last_cmd, last_args
    idle_seq = ''
    if cmd in robot.seq_list:
        for bot in robots:
            if not bot.seq_stop:
                bot.seq_stop = threading.Event()
            bot.seq_stop.set()
            seq_thread = bot.play_recording(cmd, idler=False)

        if (idle_seq != ''):
            while (seq_thread.is_alive()):
                time.sleep(0.1)
                continue
                
            for bot in robots:
                if not bot.seq_stop:
                    bot.seq_stop = threading.Event()
                bot.seq_stop.set()
                bot.play_recording(idle_seq, idler=True)
    else:
        print("Unknown sequence naem:", cmd)
        return



def main(args):
    """
    Start robots
    """
    global master_robot
    global robots

    configs = RobotConfig().get_configs(args.names)
    master_robot = safe_init_robot(args.names[0], configs[args.names[0]])
    configs.pop(args.names[0])
    robots = [safe_init_robot(name, config)
              for name, config in configs.items()]
    robots.append(master_robot)

    master_robot.reset_position()

    start_server(args.host, args.port, args.browser_disable)

def safe_init_robot(name, config):
    bot = None
    attempts = 10
    while bot is None:
        try:
            bot = SequenceRobot(name, config)
        except (DxlError, NotImplementedError, RuntimeError, SerialException) as e:
            if attempts <= 0:
                raise e
            print(e, "retrying...")
            attempts -= 1
    return bot

if __name__ == "__main__":
    main(parse_args(sys.argv[1:]))


