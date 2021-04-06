class AutomateError(Exception):
	"""Base Automate exception that all relevant others inherent from"""


class PlayListError(AutomateError):
	"""Empty list of videos to download"""


class ResolutionError(AutomateError):
	"""key video(s) without coresponding resolution value(s)"""


class LocationError(AutomateError):
	"""Invalid provided location (path doesn't exists)"""
