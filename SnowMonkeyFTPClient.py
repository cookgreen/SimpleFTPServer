from socket import *
from threading import *
from SnowMonkeyFTPClientCommand import *

class SnowMonkeyFTPClientRecvThread(Thread):
	def __init__(self, client):
		Thread.__init__(self)
		self.client = client

	def run(self):
		while True:
			if(self.client.quit):
				break
			
			if(self.client.connected):
				try:
					ret = self.client.clientSock.recv(1024)
					print
					for r in ret.split('|'):
						print r
				except:
					break
					
class SnowMonkeyFTPClient(object):
	def __init__(self):
		self.connected = False
		self.clientSock = socket(AF_INET, SOCK_STREAM)
		self.version = "0.0.1"
		connectCmd = SnowMonkeyFTPClientCommandConnect(self)
		connectCmd.Init(self.clientSock)
		showServerCmd = SnowMonkeyFTPClientCommandShowServerCommands(self)
		showServerCmd.Init(self.clientSock)
		self.avaliableCommands = {
				"help":SnowMonkeyFTPClientCommandHelp(self),
				"quit":SnowMonkeyFTPClientCommandQuit(self),
				"version":SnowMonkeyFTPClientCommandVersion(self),
				"connect":connectCmd,
				"show_srv_cmd":showServerCmd,
			}
		self.quit = False

	def run(self):
		print """SnowMonkeyFTPClient Version %s \ntype 'help' show help """ % self.version
		self.recvThread = SnowMonkeyFTPClientRecvThread(self)
		self.recvThread.setDaemon(True)
		self.recvThread.start();
		while True:
			if(self.quit):
				break
				
			if(not self.connected):
				data = raw_input("> ")
			else:
				data = raw_input("ftp> ")

			tokens = data.split(' ')
			args = tokens[1:len(tokens)]
			
			if(tokens[0] in self.avaliableCommands):
				self.avaliableCommands[tokens[0]].Execute(args)
			elif(self.connected):
				try:
					self.clientSock.send(data)
				except:
					break
			else:
				print "Command not found"

	def connect(self):
		self.connected = True
		
	def exit(self):
		self.quit = True
		self.connected = False
		self.clientSock.close()
		
		
if __name__ == '__main__':
	app = SnowMonkeyFTPClient()
	app.run()
