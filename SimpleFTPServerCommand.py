import os
from abc import ABCMeta,abstractmethod

class SimpleFTPServerCommand(object):
	__metaclass__ = ABCMeta
	def __init__(self, ftpServer):
		self.ftpServer = ftpServer

	@abstractmethod
	def GetCommandName(self):
		pass

	def GetCommandDescription(self):
		pass

	def Execute(self, **kwargs):
		pass

class SimpleFTPServerCommandListDir(SimpleFTPServerCommand):
	def GetCommandName(self):
		return "ls"

	def GetCommandDescription(self):
		return "list the current server work directory"

	def Execute(self, **kwargs):
		ret = ""
		filelst = os.listdir(os.getcwd())
		lstnum = len(filelst)
		idx = 0
		for f in filelst:
			if(idx != lstnum - 1):
				ret = ret + f+":"
			else:
				ret = ret + f
			idx = idx + 1
		return ret

class SimpleFTPServerCommandChangeDir(SimpleFTPServerCommand):
	def GetCommandName(self):
		return "cd"

	def GetCommandDescription(self):
		return "change current work directory to another directory"

	def Execute(self, **kwargs):
		return os.chdir(os.getcwd())

class SimpleFTPServerCommandGetCurrentWorkDirectory(SimpleFTPServerCommand):
	def GetCommandName(self):
		return "cwd"

	def GetCommandDescription(self):
		return "Get current work directory"

	def Execute(self, **kwargs):
		return os.getcwd()
		
