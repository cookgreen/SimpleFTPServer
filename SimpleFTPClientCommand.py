from abc import ABCMeta,abstractmethod

class SimpleFTPClientCommand(object):
	__metaclass__ = ABCMeta
	def __init__(self, ftpClient, **kwargs):
		self.ftpClient = ftpClient

	@abstractmethod
        def Init(self, *args):
                pass
	
	def GetCommandName(self):
		pass

	def GetCommandDescription(self):
		pass

	def Execute(self, *args):
		pass

class SimpleFTPClientCommandHelp(SimpleFTPClientCommand):
        def Init(self, *args):
                return True
        
	def GetCommandName(self):
		return "help"

	def GetCommandDescription(self):
		return "Show help"

	def Execute(self, **kwargs):
		commands = self.ftpClient.avaliableCommands
		for key in commands:
			print "%s - %s" % (key, commands[key].GetCommandDescription())

class SimpleFTPClientCommandQuit(SimpleFTPClientCommand):
        def Init(self, *args):
                return True
        
	def GetCommandName(self):
		return "quit"

	def GetCommandDescription(self):
		return "Exit application"

	def Execute(self, **kwargs):
		self.ftpClient.exit()

class SimpleFTPClientCommandVersion(SimpleFTPClientCommand):
        def Init(self, *args):
                return True
        
	def GetCommandName(self):
		return "version"

	def GetCommandDescription(self):
		return "Show version"

	def Execute(self, **kwargs):
		print self.ftpClient.version

class SimpleFTPClientCommandConnect(SimpleFTPClientCommand):
        def Init(self, *args):
                self.clientSock = args[0]
                return True
        
	def GetCommandName(self):
		return "connect"

	def GetCommandDescription(self):
		return "connect <host> <port> [username] [password] connect to specific server"

	def Execute(self, **kwargs):
		try:
			self.clientSock.connect(("localhost",21))
			self.ftpClient.connect()
		except:
			print "connection failed! server maybe unreachable"

