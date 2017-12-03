from socket import *
from SimpleFTPClientCommand import *

class SimpleFTPClient(object):
	def __init__(self):
		self.connected = False
		self.clientSock = socket(AF_INET, SOCK_STREAM)
		self.version = "0.0.1"
		self.avaliableCommands = {
				"help":SimpleFTPClientCommandHelp(self),
				"quit":SimpleFTPClientCommandQuit(self),
				"version":SimpleFTPClientCommandVersion(self),
				"connect":SimpleFTPClientCommandConnect(self)
			}
		self.quit = False

	def run(self):
		print """SimpleFTPClient Version %s \ntype 'help' show help """ % self.version
		while True:
			if(self.quit):
				break
				
			if(not self.connected):
				data = raw_input("> ")
			else:
				data = raw_input("ftp> ")

			if(data in self.avaliableCommands):
				self.avaliableCommands[data].Execute()
			elif(self.connected):
				self.clientSock.send(data)
				ret = self.clientSock.recv(1024)
				for r in ret.split(':'):
					print r
	def exit(self):
		self.quit = True
		
if __name__ == '__main__':
	app = SimpleFTPClient()
	app.run()
