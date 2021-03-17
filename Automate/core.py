from pytube import YouTube
import os
import time
import platform
from automate.exceptions import (
	NoVideosError,
	NoResolutionError
)


class Automate:
	"""class for automating youtube videos downloading"""
	def __init__(
		self,
		*urls: list or tuple,
		**urls_with_res: dict
	):
		"""Construct a :class:`Automate <Automate>`.

        :param list or tuple urls:
            valid list or tuple of YouTube watch URL.
        :param dict urls_with_res:
            dict where keys are valid YouTube watch URL and values are valid resolution.

        """
		self.urls = urls
		self.urls_with_res = urls_with_res

		if len(self.urls_with_res.keys()) == 0 and len(self.urls) == 0:
			raise NoVideosError("List of videos can not be empty")
	
	
	def __playList(self, urls: list or tuple) -> list:
		"""Convert (tuple or list) or nested tuple of videos into list.

		:param tuple or list urls
			list or tuple of YouTube watch URL they can be nested or not

        :rtype: list

        """
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
		"""Function for downloading YouTube videos

		:param int after
			number of seconds to delay before download
		:param str location
			location on your computer to save the downloads
		:param bool shutdown
			if shutdown is True computer shuts down after downloading
		:param bool highest_res
			if highest_res is True the script downloads highest resolution
		:param bool lowest_res
			if lowest_res is True the script downloads lowest resolution

        :rtype: None

        """
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
