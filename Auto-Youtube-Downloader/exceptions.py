class AutomateError(Exception):
	"""Base Automate exception that all others inherent"""


class NoVideosError(AutomateError):
	"""Empty list of videos to download"""


class NoResolutionError(AutomateError):
	"""non of the resolution selected"""