class TimeFormatting:
	"""class for formating string time related (2h:30m) into seconds"""
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
		timeList = [i for i in self.time.split(':') if i]

		for time in timeList:
			if time[-1] == 'h':
				h = int(time[:-1])
			elif time[-1] == 'm':
				m = int(time[:-1])
			elif time[-1] == 's':
				s = int(time[:-1])
		if h:
			delay_sec += h*60*60
		if m:
			delay_sec += m*60
		if s:
			delay_sec += s
		return delay_sec
