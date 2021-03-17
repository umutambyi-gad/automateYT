from pytube import YouTube
import os
import time
import platform
from exceptions import (
	NoVideosError,
	NoResolutionError
)


class Automate:
	def __init__(
		self,
		*urls: list or tuple,
		**urls_with_res: dict
	):
		self.urls = urls
		self.urls_with_res = urls_with_res

		if len(self.urls_with_res.keys()) == 0 and len(self.urls) == 0:
			raise NoVideosError("List of videos can not be empty")
	
	
	def __playList(self, urls: list or tuple) -> list:
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
		if highest_res:
			lowest_res = False
		elif lowest_res:
			highest_res = False

		time.sleep(after)
		if len(self.urls_with_res.keys()) > 0:
			for video, resolution in self.urls_with_res['urls_with_res'].items():
				YouTube(video.strip()).youtube.streams.get_by_resolution(resolution.strip()).download(location)
		for url in self.__playList(self.urls):
			if highest_res and not lowest_res:
				YouTube(url).youtube.streams.get_highest_resolution().download(location)
			elif lowest_res and not highest_res:
				YouTube(url).youtube.streams.get_lowest_resolution().download(location)
			else:
				raise NoResolutionError("Neither highest nor lowest resolution specified")
		if shutdown:
			if platform.system() == 'Windows':
				os.system('shutdown /s /t 1')
			elif platform.system() == 'Linux':
				os.system('shutdown now -h') # notice that you have root privileges
			elif platform.system() == 'Darwin':
				os.system('shutdown -h now') # notice that you have root privileges
