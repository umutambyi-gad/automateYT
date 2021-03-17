from pytube import YouTube
import os
import time
import platform


class Automate:
	def __init__(
		self,
		*urls: tuple,
		**urls_with_res: dict
	):
		self.urls = urls
		self.urls_with_res = urls_with_res
	
	
	def __playList(self, urls: tuple) -> list:
		collections = []
		for url in urls:
			if isinstance(url, tuple) or isinstance(url, list):
				for nested in url:
					collections.append(nested.strip())
			else:
				collections.append(url.strip())
		return collections

	def download(
		self,
		after=0,
		location=os.path.dirname(__file__),
		shutdown=False,
		highest_res=True,
		lowest_res=False
	) -> None:
		time.sleep(after)
		if len(self.urls_with_res.keys()) > 0:
			for video, resolution in self.urls_with_res['urls_with_res'].items():
				YouTube(video.strip()).youtube.streams.get_by_resolution(resolution.strip()).download(location)
		for url in self.__playList(self.urls):
			if highest_res and not lowest_res:
				YouTube(url).youtube.streams.get_highest_res_resolution().download(location)
			elif lowest_res and not highest_res:
				YouTube(url).youtube.streams.get_lowest_res_resolution().download(location)
			else:
				raise Exception("Neither highest nor lowest resolution specified or both are specified")
		if shutdown:
			if platform.system() == 'Windows':
				os.system('shutdown /s /t 1')
			elif platform.system() == 'Linux':
				os.system('shutdown now -h') # notice that you have root privileges
			elif platform.system() == 'Darwin':
				os.system('shutdown -h now') # notice that you have root privileges

Automate().download()