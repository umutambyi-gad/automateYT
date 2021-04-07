from pytube import YouTube
import os
import platform
from .exceptions import (
	PlayListError,
	ResolutionError,
	LocationError
)


class Timing:
	"""class for formating string time related (2h:30m or 2h-30m) into seconds"""

	def after(self, time: str) -> None:
		"""Method for converting hours, minutes, seconds into seconds.
		
		:param str after
			string time for delaying which written in human readable format - ex.
			`2h:30m` or `2h-30m` or `30s` where `h` -> `hours`, `m` -> `minutes` and `s` -> `second`

		:rtype: None

		"""
		delay_sec = 0
		h, m, s = ('', '', '')
		timeList = []
		dash_delimeter = True if '-' in time else False
		colon_delimeter = True if ':' in time else False
		no_delimeter = not dash_delimeter and not colon_delimeter
		if dash_delimeter and not colon_delimeter:
			timeList = [i for i in time.split('-') if i]
		elif colon_delimeter and not dash_delimeter:
			timeList = [i for i in time.split(':') if i]
		elif no_delimeter:
			time = [*time]
			diff = lambda arr_1, arr_2: [x for x in arr_1 if x not in arr_2]
			for i in time:
				if i.isalpha():
					timeList.append(''.join(time[:time.index(i)+1]))
					time = diff(time, time[:time.index(i)+1])	

		for t in timeList:
			if t[-1] == 'h':
				h = int(t[:-1])
			elif t[-1] == 'm':
				m = int(t[:-1])
			elif t[-1] == 's':
				s = int(t[:-1])
		if h:
			delay_sec += h*60*60
		if m:
			delay_sec += m*60
		if s:
			delay_sec += s

		__import__('time').sleep(delay_sec)
		

		

class Automate(Timing):
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
	
	
	def __playList(self, urls: tuple or list) -> list:
		"""Method for converting (tuple or list) or nested tuple of videos into list.

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
		return [*{*collections}] # removing dublicates

	def __shutdown(self):
		"""Method for shutting down the computer using API command"""
		if platform.system() == 'Windows':
			os.system('shutdown /s /t 1')
		elif platform.system() == 'Linux':
			os.system('shutdown now -h') # notice that you have root privileges
		elif platform.system() == 'Darwin':
			os.system('shutdown -h now') # notice that you have root privileges

	def download(
		self,
		location: str = os.path.join(os.path.expanduser('~'), 'Downloads'),
		shutdown: bool = False,
		highest_res: bool = True,
		lowest_res: bool = False,
	) -> None:
		"""Method for automating the downloading of YouTube videos

		:param str location
			location on your computer to save the downloads
		:param bool shutdown
			if shutdown is True the computer shuts down after downloading is completely done
		:param bool highest_res
			if highest_res is True the script gets the highest resolution available
		:param bool lowest_res
			if lowest_res is True the script gets the lowest resolution available
        :rtype: None

        """	
		if len(self.urls_with_res.keys()) == 0 and len(self.urls) == 0:
			raise PlayListError("List or dict of videos can not be empty")
		if os.path.exists(location):
			raise LocationError("provided location (path) doesn't exists")

		if highest_res:
			lowest_res = False
		elif lowest_res:
			highest_res = False

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
				raise ResolutionError("Neither highest nor lowest resolution specified")
		if shutdown:
			self.__shutdown()
	def download_subtitle(
		self,
		lang_code: str = 'en',
		auto_generate_version: bool = True,
		location: str = os.path.join(os.path.expanduser('~'), 'Downloads'),
		shutdown: bool = False
	) -> None:
		"""Method for automating the downloading of YouTube video's subtitles
		
		:param str lang_code
			language code of the subtitle to automate its downloading notice that the default is
			'en' (English)
		:param str auto_generate_version
			by default True, this downloads auto generated version of the same language
			code in absence of offical one.
		:param str location
			location on your computer to save the downloaded videos by default is in `../Downloads`
		:param bool shutdown
			if shutdown is True the computer shuts down after downloading is completely done

        :rtype: None

		"""
		if len(self.urls_with_res.keys()) == 0 and len(self.urls) == 0:
			raise PlayListError("List or dict of videos can not be empty")

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

