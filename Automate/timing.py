class TimeFormatting:
	def __init__(self, time):
		self.time = time

	def convert(self):
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
