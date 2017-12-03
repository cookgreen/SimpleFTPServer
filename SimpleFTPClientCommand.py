from abc import ABCMeta,abstractmethod

class SimpleFTPClientCommand(object):
	__metaclass__ = ABCMeta
	def __init__(self, ftpClient):
		self.ftpClient = ftpClient

	@abstractmethod
	def GetCommandName(self):
		pass

	def GetCommandDescription(self):
		pass

	def Execute(self, **kwargs):
		pass

class SimpleFTPClientCommandHelp(SimpleFTPClientCommand):
	def GetCommandName(self):
		return "help"

	def GetCommandDescription(self):
		return "Show help"

	def Execute(self, **kwargs):
		commands = self.ftpClient.avaliableCommands
		for key in commands:
			print "%s - %s" % (key, commands[key].GetCommandDescription())

class SimpleFTPClientCommandQuit(SimpleFTPClientCommand):
	def GetCommandName(self):
		return "quit"

	def GetCommandDescription(self):
		return "Exit application"

	def Execute(self, **kwargs):
		self.ftpClient.exit()

class SimpleFTPClientCommandVersion(SimpleFTPClientCommand):
	def GetCommandName(self):
		return "version"

	def GetCommandDescription(self):
		return "Show version"

	def Execute(self, **kwargs):
		print self.ftpClient.version

class SimpleFTPClientCommandConnect(SimpleFTPClientCommand):
	def GetCommandName(self):
		return "connect"

	def GetCommandDescription(self):
		return "connect <host> <port> [username] [password] connect to specific server"

	def Execute(self, **kwargs):
		try:
			self.clientSock.connect(("localhost",21))
			self.connected = True
		except:
			print "connection failed! server maybe unreachable"

