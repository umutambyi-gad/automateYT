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
