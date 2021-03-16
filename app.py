from pytube import YouTube
import os
import time
import platform

class Automate:
	def __init__(self, *urls):
		self.urls = urls
		if not len([i for i in self.urls if i]) > 0:
			raise Exception("List of urls can not be empty")
	
	@classmethod
	def playList(cls, urls):
		collections = []
		for url in urls:
			if isinstance(url, tuple) or isinstance(url, list):
				for nested in url:
					collections.append(nested.strip())
			else:
				collections.append(url.strip())
		return collections

	def download(self, after=0, dir=os.path.dirname(__file__), shutdown=False):
		time.sleep(after)
		for url in Automate.playList(self.urls):
			YouTube(url).youtube.streams.first().download(dir)
		if shutdown:
			if platform.system() == 'Windows':
				os.system('shutdown /s /t 1')
			elif platform.system() == 'Linux':
				os.system('shutdown now -h') # notice that you have root privileges
			elif platform.system() == 'Darwin':
				os.system('shutdown -h now') # notice that you have root privileges

