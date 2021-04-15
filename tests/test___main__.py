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

	