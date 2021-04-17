import pytest
from autoYT.__main__ import Automate
from autoYT.exceptions import *


class TestExceptions:
	def test_EmptyLookUpListError(self):
		with pytest.raises(EmptyLookUpListError) as exc_info:
			Automate().info()

		assert str(exc_info.value) == "List or dict of (videos or audios) to access can not be empty"

		with pytest.raises(EmptyLookUpListError) as exc_info:
			Automate(urls_with_res={}).download()

		assert str(exc_info.value) == "List or dict of (videos or audios) to access can not be empty"

		with pytest.raises(EmptyLookUpListError) as exc_info:
			Automate().download_subtitle()

		assert str(exc_info.value) == "List or dict of (videos or audios) to access can not be empty"

		with pytest.raises(EmptyLookUpListError) as exc_info:
			Automate(urls_with_res={}).download_playlist()

		assert str(exc_info.value) == "List or dict of (videos or audios) to access can not be empty"


	def test_ResolutionAbsenceError(self):
		with pytest.raises(ResolutionAbsenceError) as exc_info:
			Automate('https://www.youtube.com/watch?v=XqZsoesa55w').download(highest_res=False, lowest_res=False)

		assert str(exc_info.value) == "Neither highest nor lowest resolution specified"

		with pytest.raises(ResolutionAbsenceError) as exc_info:
			Automate('https://www.youtube.com/playlist?list=PLS1QulWo1RIaJECMeUT4LFwJ-ghgoSH6n').download_playlist(highest_res=False, lowest_res=False)

		assert str(exc_info.value) == "Neither highest nor lowest resolution specified"


	def test_NonExistLocationError(self):
		with pytest.raises(NonExistLocationError) as exc_info:
			Automate('https://www.youtube.com/watch?v=XqZsoesa55w').download(location='C:/someNonExistPath')

		assert str(exc_info.value) == "provided location (path) doesn't exists"

		with pytest.raises(NonExistLocationError) as exc_info:
			Automate('https://www.youtube.com/playlist?list=PLS1QulWo1RIaJECMeUT4LFwJ-ghgoSH6n').download_playlist(location='home/someNonExistPath')

		assert str(exc_info.value) == "provided location (path) doesn't exists"

	
	def test_TypeError(self):
		with pytest.raises(TypeError) as exc_info:
			Automate({'https://www.youtube.com/watch?v=XqZsoesa55w'}).download()

		assert str(exc_info.value) == "tuple, list or string were expected but set was given"

		with pytest.raises(TypeError) as exc_info:
			Automate(urls_with_res='https://www.youtube.com/playlist?list=PLS1QulWo1RIaJECMeUT4LFwJ-ghgoSH6n').download_playlist()

		assert str(exc_info.value) == "dict were expected but str was given"


	def test_InvalidFormatError(self):
		with pytest.raises(InvalidFormatError) as exc_info:
			Automate('https://www.youtube.com/watch?v=XqZsoesa55w').info('otherThanJsonOrYaml')
		
		assert str(exc_info.value) == "fmt (format) should be json or yaml"
		

