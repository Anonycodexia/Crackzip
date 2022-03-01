#!/usr/bin/env python3

import sys
from threading import Thread
from queue import Queue
from zipfile import ZipFile, BadZipFile
from tempfile import mkdtemp
from blessings import Terminal

TMPDIR = mkdtemp()
passwords = Queue()
z = ZipFile("crack.zip")

with open("passwords.txt") as wordlist:
	for password in wordlist:
		passwords.put(password.strip())
		pass
	pass

def worker(y):
	while not passwords.empty():
		password = passwords.get()
		try:
			z.extractall(path=TMPDIR, pwd=password.encode())
			print(t.move(y, 0) + "{}: Password Found:\033[1;32m {}".format(y, password, TMPDIR) + t.clear_eol)
			with passwords.mutex:
				passwords.queue.clear()
			return
		except:
			print(t.move(y, 0) + "{}: Cracking Password:\033[1;34m {}".format(y, password) + t.clear_eol)
	print(t.move(y, 0) + "{}: Failed to crack zip file".format(y) + t.clear_eol)
	pass

t = Terminal()

with t.fullscreen():
	threads = []
	for i in range(1, 2):
		thread = Thread(target=worker, args=(i, ), daemon=True)
		thread.start()
		threads.append(thread)
	
	for thread in threads:
		thread.join()
		
	msg = "Password Cracked, Enter to exit."
	print(t.move(len(threads) + 1, (t.width - len(msg)) // 2) + msg)	
	input()	
    
z.close()
