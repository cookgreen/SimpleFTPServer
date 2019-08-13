import os
from abc import ABCMeta,abstractmethod

class SnowMonkeyFTPServerCommand(object):
	__metaclass__ = ABCMeta
	def __init__(self, ftpServer):
		self.ftpServer = ftpServer

	@abstractmethod
	def GetCommandName(self):
		pass

	def GetCommandDescription(self):
		pass

	def Execute(self, *args):
		pass

class SnowMonkeyFTPServerCommandListDir(SnowMonkeyFTPServerCommand):
	def GetCommandName(self):
		return "ls"

	def GetCommandDescription(self):
		return "list the current server work directory"

	def Execute(self, *args):
		ret = ""
		filelst = os.listdir(os.getcwd())
		lstnum = len(filelst)
		idx = 0
		for f in filelst:
			if(idx != lstnum - 1):
				ret = ret + f+"|"
			else:
				ret = ret + f
			idx = idx + 1
		return ret

class SnowMonkeyFTPServerCommandChangeDir(SnowMonkeyFTPServerCommand):
	def GetCommandName(self):
		return "cd"

	def GetCommandDescription(self):
		return "change current work directory to another directory"

	def Execute(self, *args):
		return os.chdir(os.getcwd())

class SnowMonkeyFTPServerCommandGetCurrentWorkDirectory(SnowMonkeyFTPServerCommand):
	def GetCommandName(self):
		return "cwd"

	def GetCommandDescription(self):
		return "Get current work directory"

	def Execute(self, *args):
		return os.getcwd()
		
class SnowMonkeyFTPServerCommandEcho(SnowMonkeyFTPServerCommand):
	def GetCommandName(self):
		return "echo"

	def GetCommandDescription(self):
		return "Echo message"

	def Execute(self, *args):
		print args
		return "Echo from server: " + args[0][0]