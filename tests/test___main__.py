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

	
	@pytest.mark.parametrize(
		'dummyLookUpList, result',
		[
			(
				[
					['https://www.youtube.com/watch?v=vFWv44Z4Jhk']
				],
					['https://www.youtube.com/watch?v=vFWv44Z4Jhk']
			),

			(
				(
					['https://www.youtube.com/watch?v=aVAKT9UxJMI'],
				),
					['https://www.youtube.com/watch?v=aVAKT9UxJMI']
			),

			(
				(
					('https://www.youtube.com/watch?v=k3zimSRKqNw',),
				),
					['https://www.youtube.com/watch?v=k3zimSRKqNw']
			),

			(
				(
					(
						'https://www.youtube.com/watch?v=k3zimSRKqNw',
						'https://www.youtube.com/watch?v=aVAKT9UxJMI'
					)
				),
					[
						'https://www.youtube.com/watch?v=k3zimSRKqNw',
						'https://www.youtube.com/watch?v=aVAKT9UxJMI'
					]
			),

			(
				(
					(
						'https://www.youtube.com/watch?v=k3zimSRKqNw',
						'https://www.youtube.com/watch?v=TB-G1KqRb5o'
					),
					[
						'https://www.youtube.com/watch?v=aVAKT9UxJMI',
						'https://www.youtube.com/watch?v=CdltAssTMs8'
					]
				),
				[
					'https://www.youtube.com/watch?v=k3zimSRKqNw',
					'https://www.youtube.com/watch?v=TB-G1KqRb5o',
					'https://www.youtube.com/watch?v=aVAKT9UxJMI',
					'https://www.youtube.com/watch?v=CdltAssTMs8'
				]
			)
		]
	)
	def test__playList(self, dummyLookUpList, result):
		assert all(i in result for i in Automate()._Automate__playList(dummyLookUpList))


	def test_delay(self, automate):
		start = time.perf_counter()

		automate.after('2s')

		end = time.perf_counter()
		time_ellapsed = math.floor(end - start)

		assert time_ellapsed == 2
