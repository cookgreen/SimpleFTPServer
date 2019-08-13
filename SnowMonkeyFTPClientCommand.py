from abc import ABCMeta,abstractmethod

class SnowMonkeyFTPClientCommand(object):
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

class SnowMonkeyFTPClientCommandHelp(SnowMonkeyFTPClientCommand):
        def Init(self, *args):
                return True
        
	def GetCommandName(self):
		return "help"

	def GetCommandDescription(self):
		return "Show help"

	def Execute(self, *args):
		commands = self.ftpClient.avaliableCommands
		for key in commands:
			print "%s - %s" % (key, commands[key].GetCommandDescription())

class SnowMonkeyFTPClientCommandQuit(SnowMonkeyFTPClientCommand):
        def Init(self, *args):
                return True
        
	def GetCommandName(self):
		return "quit"

	def GetCommandDescription(self):
		return "Exit application"

	def Execute(self, *args):
		self.ftpClient.exit()

class SnowMonkeyFTPClientCommandVersion(SnowMonkeyFTPClientCommand):
        def Init(self, *args):
                return True
        
	def GetCommandName(self):
		return "version"

	def GetCommandDescription(self):
		return "Show version"

	def Execute(self, *args):
		print self.ftpClient.version

class SnowMonkeyFTPClientCommandConnect(SnowMonkeyFTPClientCommand):
        def Init(self, *args):
                self.clientSock = args[0]
                return True
        
	def GetCommandName(self):
		return "connect"

	def GetCommandDescription(self):
		return "connect <host> <port> [username] [password] connect to specific server"

	def Execute(self, *args):
		try:
			serverPortTokens = args[0]
			self.clientSock.connect((serverPortTokens[0], int(serverPortTokens[1])))
			self.ftpClient.connect()
		except Exception, err:
			print "connection failed! server maybe unreachable"
			print err

class SnowMonkeyFTPClientCommandShowServerCommands(SnowMonkeyFTPClientCommand):
		
        def Init(self, *args):
			self.clientSock = args[0]
			return True
        
	def GetCommandName(self):
		return "show_srv_cmd"

	def GetCommandDescription(self):
		return "Show avaliable server commands"

	def Execute(self, *args):
		self.clientSock.send("show_srv_cmd")