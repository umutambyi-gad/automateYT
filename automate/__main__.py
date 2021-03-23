from pytube import YouTube
import os
import time
import platform
from warnings import (
	NoVideosError,
	NoResolutionError
)
from timing import TimeFormatting


class Automate:
	"""class for automating youtube videos downloading"""
	def __init__(
		self,
		*urls: tuple or list,
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
	
	
	def __playList(self, urls: tuple or list) -> list:
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

	def __shutdown(self):
		"""Function for shutting down the computer using API command"""
		if platform.system() == 'Windows':
			os.system('shutdown /s /t 1')
		elif platform.system() == 'Linux':
			os.system('shutdown now -h') # notice that you have root privileges
		elif platform.system() == 'Darwin':
			os.system('shutdown -h now') # notice that you have root privileges

	def download(
		self,
		after: str = '0s',
		location: str = os.path.join(os.path.expanduser('~'), 'Downloads'),
		shutdown: bool = False,
		highest_res: bool = True,
		lowest_res: bool = False,
		retry: int = 1
	) -> None:
		"""Function for automating the downloading of YouTube videos

		:param str after
			string time for delaying before the download starts that is writen like.
			`2h:30m` or `2h-30m` or `30s` where `h` -> `hours`, `m` -> `minutes` and `s` -> `second`
		:param str location
			location on your computer to save the downloads
		:param bool shutdown
			if shutdown is True the computer shuts down after downloading is completely done
		:param bool highest_res
			if highest_res is True the script gets the highest resolution available
		:param bool lowest_res
			if lowest_res is True the script gets the lowest resolution available
		:param int retry
			number of times to retry while there is something went wrong

        :rtype: None

        """
		if highest_res:
			lowest_res = False
		elif lowest_res:
			highest_res = False
		
		time.sleep(TimeFormatting(after).convert()) # delaying

		if len(self.urls_with_res.keys()) > 0:
			for video, resolution in self.urls_with_res['urls_with_res'].items():
				youtube = YouTube(video.strip())
				if youtube.streams:
					youtube.streams.get_by_resolution(resolution.strip()).download(location)
		
		playList = self.__playList(self.urls)
		for url in playList:
			youtube = YouTube(url.strip())
			if highest_res and not lowest_res:
				if youtube.streams:
					youtube.streams.get_highest_resolution().download(location)
			elif lowest_res and not highest_res:
				if youtube.streams:
					youtube.streams.get_lowest_resolution().download(location)
			else:
				raise NoResolutionError("Neither highest nor lowest resolution specified")
		if shutdown:
			self.__shutdown()
	def download_subtitle(
		self,
		lang_code: str = 'en',
		auto_generate_version: bool = True,
		after: str = '0s',
		location: str = os.path.join(os.path.expanduser('~'), 'Downloads'),
		shutdown: bool = False
	) -> None:
		"""Function for automating the downloading of YouTube video's subtitles
		
		:param str lang_code
			language code of the subtitle to automate its downloading notice that the default is
			'en' (English)
		:param str auto_generate_version
			by default True, this downloads auto generated version of the same language
			code in absence of offical one.
		:param str after
			string time for delaying before the download starts that is writen like.
			`2h:30m` or `2h-30m` or `30s` where `h` -> `hours`, `m` -> `minutes` and `s` -> `second`
		:param str location
			location on your computer to save the downloaded videos by default is in `../Downloads`
		:param bool shutdown
			if shutdown is True the computer shuts down after downloading is completely done

        :rtype: None

		"""
		time.sleep(TimeFormatting(after).convert())
		for url in self.__playList(self.urls):
			youtube = YouTube(url)
			if youtube.captions.__len__() > 0:
				if youtube.captions[lang_code].code == lang_code:
					youtube.captions[lang_code].download(youtube.title, output_path=location)
				elif auto_generate_version:
					if youtube.captions[lang_code].code == f"a.{lang_code}":
						lang_code = f"a.{lang_code}"
						youtube.captions[lang_code].download(youtube.title, output_path=location)
		if shutdown:
			self.__shutdown()
