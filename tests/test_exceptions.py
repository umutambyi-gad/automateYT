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

	@pytest.mark.this
	def test_ResolutionAbsenceError(self):
		with pytest.raises(ResolutionAbsenceError) as exc_info:
			Automate('https://www.youtube.com/watch?v=XqZsoesa55w').download(highest_res=False, lowest_res=False)

		assert str(exc_info.value) == "Neither highest nor lowest resolution specified"

		with pytest.raises(ResolutionAbsenceError) as exc_info:
			Automate('https://www.youtube.com/playlist?list=PLS1QulWo1RIaJECMeUT4LFwJ-ghgoSH6n').download_playlist(highest_res=False, lowest_res=False)

		assert str(exc_info.value) == "Neither highest nor lowest resolution specified"
