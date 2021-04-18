class AutomateError(Exception):
	"""Base Automate exception that all relevant others inherent from"""


class EmptyLookUpListError(AutomateError):
	"""Empty list of videos to download"""


class ResolutionAbsenceError(AutomateError):
	"""key video(s) without coresponding resolution value(s)"""


class NonExistLocationError(AutomateError):
	"""Invalid provided location (path doesn't exists)"""


class InvalidFormatError(AutomateError):
	"""Invalid format of output file (neither json or yaml)"""

