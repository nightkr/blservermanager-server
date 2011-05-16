import tornadio

from blmanager import models

import uuid

class BlManagerConnection(tornadio.SocketConnection):
	def on_message(self, message, *args, **kwargs):
		command_and_arguments = message.split(":", 1)
		command = command_and_arguments[0]
		arguments = ""
		if len(command_and_arguments) >= 2:
			arguments = command_and_arguments[1]
		if command != "key" and "key" not in dir(self):
			self.send("error:no key registered")
		else:
			try:
				{
					"key": self.setkey,
				}[command](arguments)
			except KeyError:
				self.server.send(message)
	def on_close(self, *args, **kwargs):
		if "key" in dir(self):
			del models.servers_and_webclients[self.key][models.servers_and_webclients[self.key].index(self)]

	def setkey(self, key):
		if key in models.servers_and_webclients:
			self.key = key
			models.servers_and_webclients[key].append(self)
			self.server = models.servers[key]
			self.server.send("newclient")
		else:
			self.close()

	def eval_line(self, line):
		self.server.send("eval:%s" % line)

class BlManagerDesktopClientConnection(tornadio.SocketConnection):
	def on_open(self, *args, **kwargs):
		while True:
			key = uuid.uuid1().__str__()
			if key not in models.servers_and_webclients:
				self.key = key
				models.servers_and_webclients[key] = []
				models.servers[key] = self
				self.send("key:%s" % key)
				break
	def on_message(self, message, *args, **kwargs):
		for webclient in models.servers_and_webclients[self.key]:
			webclient.send(message)
	def on_close(self, *args, **kwargs):
		for webclient in models.servers_and_webclients[self.key]:
			webclient.close()
		del models.servers_and_webclients[self.key]
		del models.servers[self.key]
