class TimeFormatting:
	"""class for formating string time related (2h:30m or 2h-30m) into seconds"""
	def __init__(self, time: str):
		"""Construct a :class:`TimeFormatting <TimeFormatting>`.

		:param str time
			string that is related to time format ex. `2h:30m`
		"""
		self.time = time

	def convert(self) -> int:
		"""Function for converting hours, minutes, seconds into seconds.

		:rtype: int

		"""
		delay_sec = 0
		h, m, s = ('', '', '')
		timeList = []
		dash_delimeter = True if '-' in self.time else False
		colon_delimeter = True if ':' in self.time else False
		no_delimeter = not dash_delimeter and not colon_delimeter
		if dash_delimeter and not colon_delimeter:
			timeList = [i for i in self.time.split('-') if i]
		elif colon_delimeter and not dash_delimeter:
			timeList = [i for i in self.time.split(':') if i]
		elif no_delimeter:
			timeList = [self.time]

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
		return delay_sec
