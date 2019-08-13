import os
import sys
from socket import *
from threading import *
from SnowMonkeyFTPServerCommand import *

wxFound = False
try:
	import wx
	wxFound = True
except ImportError as e:
	wxFound = False

class SnowMonkeyFTPServerThread(Thread):
	def __init__(self, host, port):
		Thread.__init__(self)
		self.stopped = False
		self.host = host
		self.port = port

	def run(self):
		s = SnowMonkeyFTPServer(self.host, self.port)
		s.Start()

class SnowMonkeyFTPClientThread(Thread):
	def __init__(self, sockettuple, commands):
		Thread.__init__(self)
		self.clientSock, addr = sockettuple
		print "client from " + addr[0] + " connected"
		self.stopped = False
		self.commands = commands

	def run(self):
		while True:
			if(self.stopped):
				break
			try:
				self.data = self.clientSock.recv(1024)
				tokens = self.data.split(' ')
				args = tokens[1:len(tokens)]
				
				if(tokens[0] in self.commands):
					self.clientSock.send(self.commands[tokens[0]].Execute(args))
				elif(self.data=="show_srv_cmd"):
					str = ""
					index = 0
					for cmd in self.commands:
						str += cmd
						if(index!=len(self.commands)-1):
							str += "|"
						index = index + 1
					self.clientSock.send(str)
				else:
					self.clientSock.send("command not found")
			except:
				break
		self.clientSock.close()

	def close(self):
		self.stopped = True

if(wxFound):
	class SnowMonkeyFTPServerConfigDlg(wx.Dialog):
		def __init__(self):
			wx.Dialog.__init__(self, None, -1, "FTP Configuration")

			panel = wx.Panel(self, -1, style = wx.TAB_TRAVERSAL
				 | wx.CLIP_CHILDREN
				 | wx.FULL_REPAINT_ON_RESIZE)
			self.sizer = wx.GridBagSizer(6,2)

			self.sizer.Add(wx.StaticText(panel, -1, "Server Address:"), (0,0), flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.ALL, border = 5)
			self.sizer.Add(wx.StaticText(panel, -1, "Server Port:"), (1,0), flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.ALL, border = 5)
			self.addresstext = wx.TextCtrl(panel, -1, "localhost")
			self.porttext = wx.TextCtrl(panel, -1, "21")
			self.sizer.Add(self.addresstext, (0,1), flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.EXPAND|wx.ALL, border = 5)
			self.sizer.Add(self.porttext, (1,1), flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.EXPAND|wx.ALL, border = 5)
			self.usepasswordCheckBox = wx.CheckBox(panel, -1, "Anonymous")
			self.usepasswordCheckBox.SetValue(True)
			self.sizer.Add(self.usepasswordCheckBox, (2,0), flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.ALL, border = 5)
			self.sizer.Add(wx.StaticText(panel, -1, "User Name:"), (3,0), flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.ALL, border = 5)
			self.sizer.Add(wx.StaticText(panel, -1, "Password:"), (4,0), flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.ALL, border = 5)
			self.usernametext = wx.TextCtrl(panel, -1, "")
			self.passwordtext = wx.TextCtrl(panel, -1, "")
			self.usernametext.Disable()
			self.passwordtext.Disable()
			self.sizer.Add(self.usernametext, (3,1), flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.EXPAND|wx.ALL, border = 5)
			self.sizer.Add(self.passwordtext, (4,1), flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.EXPAND|wx.ALL, border = 5)
			self.buttonSizer = wx.GridBagSizer(1,2)
			self.okBtn = wx.Button(panel, -1, "OK")
			self.cancelBtn = wx.Button(panel, -1, "Cancel")
			self.buttonSizer.Add(self.okBtn, (0,0), flag = wx.ALL, border = 5)
			self.buttonSizer.Add(self.cancelBtn, (0,1), flag = wx.ALL, border = 5)
			self.sizer.Add(self.buttonSizer, (5,1), flag = wx.EXPAND, border = 5)

			self.Bind(wx.EVT_BUTTON, self.OnStartServer, self.okBtn)
			self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancelBtn)
			self.Bind(wx.EVT_CHECKBOX, self.OnUsePasswordChecked, self.usepasswordCheckBox)

			panel.SetSizer(self.sizer)
			self.sizer.Fit(self)

		def OnStartServer(self, evt):
			self.server = SnowMonkeyFTPServerThread(self.addresstext.GetValue(), int(self.porttext.GetValue()))
			self.server.start()
			self.Hide()

		def OnUsePasswordChecked(self, evt):
			if(not self.usepasswordCheckBox.IsChecked()):
				self.usernametext.Enable()
				self.passwordtext.Enable()
			else:
				self.usernametext.Disable()
				self.passwordtext.Disable()

		def OnCancel(self, evt):
			self.Destroy()

	class SnowMonkeyFTPServerConfigApp(wx.App):
		def OnInit(self):
			f = SnowMonkeyFTPServerConfigDlg()
			f.Show()
			return True

class SnowMonkeyFTPServer(object):
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.clients = []
		self.s = socket(AF_INET, SOCK_STREAM)
		self.s.bind((self.host, self.port))
		self.s.listen(5)
		self.stopped = False
		self.avaliableCommands = {
			"ls":SnowMonkeyFTPServerCommandListDir(self),
			"cd":SnowMonkeyFTPServerCommandChangeDir(self),
			"cwd":SnowMonkeyFTPServerCommandGetCurrentWorkDirectory(self),
			"echo":SnowMonkeyFTPServerCommandEcho(self),
		}

	def Start(self):
		print "Server started on %s:%s" % (self.host, self.port)
		while True:
			if(self.stopped):
				break
			self.client = SnowMonkeyFTPClientThread(self.s.accept(),self.avaliableCommands)
			self.client.start()
			self.clients.append(self.client)
		self.server.close()

	def Stop(self):
		print "Stopping..."

		for client in self.clients:
			client.close()
			client.stop()
		self.stopped = True


if __name__ == '__main__':
	if(wxFound):
		app = SnowMonkeyFTPServerConfigApp()
		app.MainLoop()
	else:
		if(len(sys.argv) > 1 and len(sys.argv[1:]) >= 2 and len(sys.argv[1:] <= 4)):
			if(len(sys.argv[1:]) == 2):
				server = SnowMonkeyFTPServerThread(sys.argv[1:][0],int(sys.argv[1:][1]))
				server.start()
			else:
				server = SnowMonkeyFTPServerThread(sys.argv[1:][0],int(sys.argv[1:][1]))
				server.start()
		while True:
			print "Please input infomation <serveraddr>:<serverport>|<username>:<password>"
			data = raw_input("input> ")
			if(data != ""):
				server = SnowMonkeyFTPServerThread(data.split('|')[0].split(':')[0], 
									   int(data.split('|')[0].split(':')[1]))
				server.start()
				break



		
