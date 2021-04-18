from pytube import YouTube
from pytube import Playlist
import os
import platform
import re
from automateYT.exceptions import (
	EmptyLookUpListError,
	ResolutionAbsenceError,
	NonExistLocationError,
	InvalidFormatError
)


class Timing:
	"""class for converting string time looks like (2h:30m, 2h30m, or 2h-30m) into seconds"""

	def after(self, time: str):
		"""Method for delaying time which are in format of human readable time (2h:30m)
		
		:param: str time
			string time for delaying which written in human readable format - ex.
			`2h:30m` or `2h-30m` or `30s` where `h` -> `hours`, `m` -> `minutes` and `s` -> `second`

		:rtype: None

		"""

		delay_sec = 0
		h, m, s = ('', '', '')
		timeList = []

		# sanitizing time string so far
		time = re.match(
			re.compile("(\\d+[h]{1}[-,:]?)?(\\d+[m]{1}[-,:]?)?(\\d+[s]{1}[-,:]?)?"),
			time
		).group()

		dash_delimeter = True if '-' in time else False # check for the `-` delimeter
		colon_delimeter = True if ':' in time else False # check for the `:` delimeter
		no_delimeter = not dash_delimeter and not colon_delimeter # assume to be no delimeter

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

		__import__('time').sleep(delay_sec) # delaying
		

		

class Automate(Timing):
	"""
	Class with methods for automating to download youtube videos as either videos or
	audios, subtitles (if available) and generating watch urls from youtube playlist.
	"""

	def __init__(
		self,
		*urls: tuple or list,
		**urls_with_res: dict
	):
		"""Construct a :class:`Automate <Automate>`.

        :param: list or tuple urls:
            valid list or tuple of YouTube watch URLs.

        :param: dict urls_with_res:
            dict where keys are valid YouTube watch URLs and values are valid video resolutions.

        """

		self.urls = urls
		self.urls_with_res = urls_with_res
		
	def __get(self) -> str:
		"""Private method for getting key name passed in the constructor - ``urls_with_res``"""

		if len(self.urls_with_res) > 0: return [*self.urls_with_res.keys()][0]

	def __playList(self, urls: tuple or list) -> list:
		"""Private method for converting (tuple or list) or nested tuple of videos into list.

		:param: tuple or list urls
			list or tuple of YouTube watch URL they can be nested or not

        :rtype: list

        """

		collections = []

		# convert one or two dimension list or tuple into one dimension list
		for url in urls:
			if isinstance(url, tuple) or isinstance(url, list):
				for nested in url:
					collections.append(nested.strip())
			else:
				collections.append(url.strip())
		return [*{*collections}] # removing dublicates

	def shutdown(self):
		"""Method for shutting down the computer using API from commandline"""

		if platform.system() == 'Windows':
			os.system('shutdown /s /t 1')

		elif platform.system() == 'Linux':
			os.system('shutdown now -h') # notice that you have root privileges

		elif platform.system() == 'Darwin':
			os.system('shutdown -h now') # notice that you have root privileges

	def __check_availabilty(self, location: str = None):
		"""Private method for checking if either self.urls_with_res or self.urls is empty and raise
		EmptyLookUpListError also checks if given location exists otherwise raise NonExistLocationError

		:param: str location
			string location gets the location where the downloads will be save on file system

		:rtype: None
		"""

		if isinstance(self.urls, tuple) and len(self.urls) > 0:
			if type(self.urls[0]) not in (tuple, list, str):
				raise TypeError(f'tuple, list or string were expected but {type(self.urls[0]).__name__} was given')

		if len(self.urls_with_res) > 0:
			if not isinstance(self.urls_with_res[self.__get()], dict):
				val = self.urls_with_res[self.__get()]
				raise TypeError(f'dict were expected but {type(val).__name__} was given')

		# check if urls_with_res and url are empty and raise an error
		if len(self.urls) == 0 and len(self.urls_with_res) == 0:
			raise EmptyLookUpListError("List or dict of (videos or audios) to access can not be empty")

		# check if urls_with_res values and url are empty and raise an error
		if len(self.urls) == 0 and len(self.urls_with_res) > 0:
			if len(self.urls_with_res[self.__get()].keys()) == 0:
				raise EmptyLookUpListError("List or dict of (videos or audios) to access can not be empty")
			 
		# check if provided location path is available otherwise raise an error
		if location is not None:
			if not os.path.exists(location):
				raise NonExistLocationError("provided location (path) doesn't exists")

	def info(self, fmt: str = 'json'):
		"""Method for giving some useful information about the youtube videos in easy and
		readable format.

		:param: str fmt
			String ftm (format) controls the return type by default is `json` and other
			available format is `yaml`

		:rtype: yaml or json
		"""

		def size_fmt(size, suffix='B'):
			"""converts bytes into human readable units"""

			for unit in ('','Ki','Mi','Gi','Ti','Pi','Ei','Zi'):
				if abs(size) < 1024.0:
					return "%3.1f%s%s" % (size, unit, suffix)

				size /= 1024.0

			return "%.1f%s%s" % (size, 'Yi', suffix)

		# check for requirements
		self.__check_availabilty()

		found = []

		if fmt.lower() not in ('json', 'yaml'):
			raise InvalidFormatError("fmt (format) should be json or yaml")

		# process for dict - self.urls_with_res
		if len(self.urls_with_res) > 0:
			if len(self.urls_with_res[self.__get()].keys()) > 0:
				for dict_url, dict_res in self.urls_with_res[self.__get()].items():
					youtube = YouTube(dict_url.strip())

					available_resolution = [
						*{i.resolution for i in youtube.streams.filter(subtype="mp4").order_by("resolution")}
					]

					vid_type = youtube.streams.get_by_resolution(dict_res)
					filesize = youtube.streams.get_by_resolution(dict_res)

					found.append({
						'watch_url': dict_url,
						'video_id': youtube.video_id,
						'title': youtube.title,
						'thumbnail_url': youtube.thumbnail_url,
						'author': youtube.author,
						'publish_date': str(youtube.publish_date.date()),
						'type': vid_type.mime_type if vid_type else youtube.streams.get_highest_resolution().mime_type,
						'filesize': size_fmt(filesize.filesize) if filesize else size_fmt(youtube.streams.get_highest_resolution().filesize),
						'available_resolution': [f'{i}p' for i in sorted([int(i[:-1]) for i in available_resolution])],
						'highest_resolution': youtube.streams.get_highest_resolution().resolution,
						'lowest_resolution': youtube.streams.get_lowest_resolution().resolution,
						'views': "{:,}".format(youtube.views),
						'rating': round(youtube.rating, 1),
						'age_restricted': youtube.age_restricted
					})

		# process for list or tuple - self.urls
		for url in self.__playList(self.urls):
			youtube = YouTube(url)

			available_resolution = [
				*{i.resolution for i in youtube.streams.filter(subtype="mp4").order_by("resolution")}
			]

			found.append({
				'watch_url': url,
				'video_id': youtube.video_id,
				'title': youtube.title,
				'thumbnail_url': youtube.thumbnail_url,
				'author': youtube.author,
				'publish_date': str(youtube.publish_date.date()),
				'type': youtube.streams.get_highest_resolution().mime_type,
				'filesize': size_fmt(youtube.streams.get_highest_resolution().filesize),
				'available_resolution': [f'{i}p' for i in sorted([int(i[:-1]) for i in available_resolution])],
				'highest_resolution': youtube.streams.get_highest_resolution().resolution,
				'lowest_resolution': youtube.streams.get_lowest_resolution().resolution,
				'views': "{:,}".format(youtube.views),
				'rating': round(youtube.rating, 1),
				'age_restricted': youtube.age_restricted
			})

		# returning json if fmt is json
		if fmt.lower() == 'json':
			return __import__('json').dumps(found, indent=4)

		# returning yaml if ftm is yaml
		elif fmt.lower() == 'yaml':
			return __import__('yaml').dump(found, indent=4)

	def generate_watch_url_from_playlist(self) -> list:
		"""Method for generating valid youtube watch urls from the youtube playlist"""

		# check for requirements
		self.__check_availabilty()

		watch_url = []

		# process for dict - self.urls_with_res
		if len(self.urls_with_res) > 0:
			if len(self.urls_with_res[self.__get()].keys()) > 0:
				for dict_url in self.urls_with_res[self.__get()].keys():
					for playlist_dict_url in Playlist(dict_url.strip()).video_urls:
						watch_url.append(playlist_dict_url)

		# process for list or tuple - self.urls
		for url in self.__playList(self.urls):
			for playlist_url in Playlist(url).video_urls:
				watch_url.append(playlist_url)

		return [*{*watch_url}] # removing duplicates

	def download(
		self,
		location: str = os.path.join(os.path.expanduser('~'), 'Downloads'), # get Downloads on every platform
		highest_res: bool = True,
		lowest_res: bool = False,
		subtitle: bool = False,
		shutdown: bool = False,
		only_audio: bool = False
	):
		"""Method for downloading of custom resolution YouTube videos as videos or audio and also subtitles
		(if available)

		:param: str location
			location path on your computer to save the downloads, by default is in Downloads

		:param: bool highest_res
			if highest_res is True the script gets the highest resolution available

		:param: bool lowest_res
			if lowest_res is True the script gets the lowest resolution available

		:param: bool subtitle
			if subtitle is True english version or english auto generated subtitle is downloaded within its video

		:param: bool shutdown
			if shutdown is True the computer shuts down after downloads is completely done

		:param: bool only_audio
			if only_audio is True audio only is downloaded
		
		:rtype: None

		"""

		# check for requirements
		self.__check_availabilty(location=location)

		if highest_res:
			lowest_res = False

		elif lowest_res:
			highest_res = False

		# process for dict - self.urls_with_res
		if len(self.urls_with_res) > 0:
			if len(self.urls_with_res[self.__get()].keys()) > 0:
				for dict_url, dict_res in self.urls_with_res[self.__get()].items():
					# assumes that if whatch is url that url is ready to go
					if 'watch' in dict_url.strip():
						youtube = YouTube(dict_url.strip())

						if youtube.streams:
							# get highest resolution due to unvailability of requested resolution
							if not only_audio and not youtube.streams.filter(progressive=True, res=dict_res.strip()):
								youtube.streams.get_highest_resolution().download(location)

							# get audio only if only_audio is True
							elif only_audio:
								youtube.streams.filter(only_audio=only_audio).first().download(location)

							else:
								youtube.streams.get_by_resolution(dict_res.strip()).download(location)

					# assumes that if there isn't watch in url that url could be playlist url
					else:
						self.download_playlist(
							location=location,
							highest_res=highest_res,
							lowest_res=lowest_res
						)
					

		# process for list or tuple - self.urls
		if len(self.urls) > 0:
			for url in self.__playList(self.urls):
				# assumes that if whatch is url that url is ready to go
				if 'watch' in url:
					youtube = YouTube(url)
					
					if highest_res and not lowest_res and not only_audio:
						if youtube.streams:
							youtube.streams.get_highest_resolution().download(location)

					elif lowest_res and not highest_res and not only_audio:
						if youtube.streams:
							youtube.streams.get_lowest_resolution().download(location)

					# get audio only if only_audio is True
					elif only_audio:
						youtube.streams.filter(only_audio=only_audio).first().download(location)

					# raise ResolutionAbsenceError error when neither highest nor lowest and not only_audio (is true)
					elif not only_audio and not highest_res and not lowest_res:
						raise ResolutionAbsenceError("Neither highest nor lowest resolution specified")

				# assumes that if there isn't watch in url that url could be playlist url
				else:
					self.download_playlist(
						location=location,
						highest_res=highest_res,
						lowest_res=lowest_res
					)

		if subtitle:
			self.download_subtitle(location=location)

		if shutdown:
			self.shutdown()

	def download_subtitle(
		self,
		lang_code: str = 'en',
		auto_generated: bool = True,
		location: str = os.path.join(os.path.expanduser('~'), 'Downloads'), # get Downloads on every platform
		shutdown: bool = False
	):
		"""Method for downloading YouTube video's subtitles (if available) or auto generated one
		in whatever language
		
		:param: str lang_code
			language code of the subtitle to automate its downloading notice that the default is
			'en' (English)

		:param: str auto_generated
			by default True, this downloads auto generated version of the same language
			code in absence of offical one.

		:param: str location
			location on your computer to save the downloads, by default is in Downloads

		:param: bool shutdown 
			if shutdown is True the computer shuts down after downloads is completely done

		:rtype: None

		"""

		# check for requirements
		self.__check_availabilty(location=location)

		# process for dict - self.urls_with_res
		if len(self.urls_with_res) > 0:
			if len(self.urls_with_res[self.__get()].keys()) > 0:
				for dict_url, dict_res in self.urls_with_res[self.__get()].items():
					# assumes that if whatch is url that url is ready to go
					if 'watch' in dict_url:
						youtube = YouTube(dict_url.strip())

						if youtube.captions.__len__() > 0:
							if youtube.captions[lang_code].code == lang_code:
								youtube.captions[lang_code].download(youtube.title, output_path=location)

						# get auto_generated version of requested one
						elif auto_generated:
							if youtube.captions[lang_code].code == f"a.{lang_code}":
								lang_code = f"a.{lang_code}"
								youtube.captions[lang_code].download(youtube.title, output_path=location)

					# assumes that if there isn't watch in url that url could be playlist url
					else:
						for watch_url in self.generate_watch_url_from_playlist():
							youtube = YouTube(watch_url)

							if youtube.captions.__len__() > 0:
								if youtube.captions[lang_code].code == lang_code:
									youtube.captions[lang_code].download(youtube.title, output_path=location)
							# get auto_generated version of requested one
							elif auto_generated:
								if youtube.captions[lang_code].code == f"a.{lang_code}":
									lang_code = f"a.{lang_code}"
									youtube.captions[lang_code].download(youtube.title, output_path=location)

		# process for list or tuple - self.urls
		for url in self.__playList(self.urls):
			# assumes that if whatch is url that url is ready to go
			if 'watch' in url:
				youtube = YouTube(url)

				if youtube.captions.__len__() > 0:
					if lang_code in youtube.captions:
						youtube.captions[lang_code].download(youtube.title, output_path=location)

					elif auto_generated:
						if f'a.{lang_code}' in youtube.captions:
							lang_code = f"a.{lang_code}"
							youtube.captions[lang_code].download(youtube.title, output_path=location)

			# assumes that if there isn't watch in url that url could be playlist url
			else:
				for watch_url in self.generate_watch_url_from_playlist():
					youtube = YouTube(watch_url)
					if youtube.captions.__len__() > 0:
						if youtube.captions[lang_code].code == lang_code:
							youtube.captions[lang_code].download(youtube.title, output_path=location)

						elif auto_generated:
							if youtube.captions[lang_code].code == f"a.{lang_code}":
								lang_code = f"a.{lang_code}"
								youtube.captions[lang_code].download(youtube.title, output_path=location)

		if shutdown:
			self.shutdown()

	def download_playlist(
		self,
		location: str = os.path.join(os.path.expanduser('~'), 'Downloads'), # get Downloads on every platform
		highest_res: bool = True,
		lowest_res: bool = False,
		limit: int = 25,
		subtitle: bool = False,
		shutdown: bool = False
	) -> bool:
		"""Method for downloading youtube playlist till the limit given is reached

		:param: str location
			location on your computer to save the downloads, by default is in Downloads

		:param: bool highest_res
			if highest_res is True the script gets the highest resolution available

		:param: bool lowest_res
			if lowest_res is True the script gets the lowest resolution available

		:param: int limit
			integer limit limits the number of the videos to be downloaded

		:param: bool subtitle
			if subtitle is True english version or english auto generated subtitle is downloaded within its video

		:param: bool shutdown
			if shutdown is True the computer shuts down after downloads is completely done 

		:rtype: bool

		"""

		rtype = False

		# check for requirements
		self.__check_availabilty(location=location)

		if highest_res:
			lowest_res = False
		elif lowest_res:
			highest_res = False

		# Raise ResolutionAbsenceError if none of lowest_res or highest_res is set to True
		if not highest_res and not lowest_res:
			raise ResolutionAbsenceError("Neither highest nor lowest resolution specified")

		# initialize count to 1
		count = 0


		# loop through list of watch url generated from playlist and download untill limit breaks it
		for url in self.generate_watch_url_from_playlist():
			youtube = YouTube(url)

			if highest_res and not lowest_res and not count == limit:
				if youtube.streams:
					youtube.streams.get_highest_resolution().download(location)
					rtype = True

			elif lowest_res and not highest_res and not count == limit:
				if youtube.streams:
					youtube.streams.get_lowest_resolution().download(location)
					rtype = True
			
			# termimates if count is equal to the limit
			elif count == limit:
				break

			count += 1

		if subtitle:
			self.download_subtitle(location=location)

		if shutdown:
			self.shutdown()

		return rtype

	def __len__(self) -> int:
		total = len(self.__playList(self.urls))

		if len(self.urls_with_res) > 0:
			total += len(self.urls_with_res[self.__get()])

		return total

	def __repr__(self) -> str:
		"""Printable object representation.

		:rtype: str
		"""

		# get json from list urls
		urls = __import__('json').dumps(self.__playList(self.urls), indent=4)

		if len(self.urls_with_res) > 0:
			self.__check_availabilty()
			
			# get json from dict urls_with_res
			urls_with_res = __import__('json').dumps(self.urls_with_res[self.__get()], indent=4)
		else:
			urls_with_res = self.urls_with_res

		return f"<Automate urls=\"{urls}\", urls_with_res=\"{urls_with_res}\">\n"
