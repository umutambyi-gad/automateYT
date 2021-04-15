import pytest
from autoYT.__main__ import Automate
import math
import time
import json
import yaml
import os
import requests


class TestMain:
	@pytest.fixture
	def automate(self):
		urls = (
			'https://www.youtube.com/watch?v=vFWv44Z4Jhk',
			'https://www.youtube.com/watch?v=Kx68g1rLbbU'
		)

		urls_with_res = {
			'https://www.youtube.com/watch?v=TgItkJCm09c': '144p',
		}

		return Automate(urls, urls_with_res=urls_with_res)

	
	@pytest.mark.parametrize(
		'obj, result',
		[
			(Automate(urls_with_res={}), 'urls_with_res'),
			(Automate(urls_with_resolution={}), 'urls_with_resolution'),
			(Automate(watchUrls_with_resolution={}), 'watchUrls_with_resolution'),
			(Automate(add_resolution={}), 'add_resolution'),
			(Automate(watchUrls_and_resolution={}), 'watchUrls_and_resolution')
		]
	)
	def test__get(self, obj, result):
		assert obj._Automate__get() == result

	
	