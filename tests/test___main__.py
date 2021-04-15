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


	def test_info(self):
		information_in_json = Automate(
			'https://www.youtube.com/watch?v=XqZsoesa55w'
		).info()

		information_in_json = json.loads(information_in_json)
		information_in_json = information_in_json[0]

		assert information_in_json['author'] == "Pinkfong! Kids' Songs & Stories"
		assert information_in_json['title'] == "Baby Shark Dance | #babyshark Most Viewed Video | Animal Songs | PINKFONG Songs for Children"
		assert information_in_json['video_id'] == 'XqZsoesa55w'
		assert information_in_json['publish_date'] == '2016-06-17'

		information_in_yaml = Automate(
			'https://www.youtube.com/watch?v=F4tHL8reNCs'
		).info('yaml')

		information_in_yaml = yaml.load(information_in_yaml)
		information_in_yaml = information_in_yaml[0]

		assert information_in_yaml['author'] == "LooLoo Kids - Nursery Rhymes and Children's Songs"
		assert information_in_yaml['title'] == "Johny Johny Yes Papa 👶 THE BEST Song for Children | LooLoo Kids"
		assert information_in_yaml['video_id'] == "F4tHL8reNCs"
		assert information_in_yaml['publish_date'] == '2016-10-08'

