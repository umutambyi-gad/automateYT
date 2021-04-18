import pytest
from automateYT.__main__ import Automate
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
			'https://www.youtube.com/watch?v=L0MK7qz13bU',
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


	@pytest.mark.req_net
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

		information_in_yaml = yaml.load(information_in_yaml, Loader=yaml.FullLoader)
		information_in_yaml = information_in_yaml[0]

		assert information_in_yaml['author'] == "LooLoo Kids - Nursery Rhymes and Children's Songs"
		assert information_in_yaml['title'] == "Johny Johny Yes Papa 👶 THE BEST Song for Children | LooLoo Kids"
		assert information_in_yaml['video_id'] == "F4tHL8reNCs"
		assert information_in_yaml['publish_date'] == '2016-10-08'

	@pytest.mark.req_net
	@pytest.mark.parametrize(
		'included',
		[
			('https://www.youtube.com/watch?v=TB-G1KqRb5o'),
			('https://www.youtube.com/watch?v=83Y2qZvWxdE'),
			('https://www.youtube.com/watch?v=CdltAssTMs8'),
			('https://www.youtube.com/watch?v=i0toy3zfUUk'),
			('https://www.youtube.com/watch?v=mVWQNeY1Pb4'),
			('https://www.youtube.com/watch?v=rQTJuCCCLVo'),
			('https://www.youtube.com/watch?v=XxRtj-GU5_8'),
			('https://www.youtube.com/watch?v=mPB2PyzkOfw')
		]
	)
	def test_generate_watch_url_from_playlist(self, included):
		watchUrls = Automate(
			"https://www.youtube.com/playlist?list=PLS1QulWo1RIaJECMeUT4LFwJ-ghgoSH6n"
		).generate_watch_url_from_playlist()

		assert type(watchUrls) is list
		assert len(watchUrls) > 0

		assert included in watchUrls


	@pytest.mark.req_net
	def test_download(self):
		obj_1 = Automate('https://www.youtube.com/watch?v=F4tHL8reNCs')

		information = json.loads(obj_1.info())[0]

		obj_1.download()

		for file in os.listdir(os.path.join(os.path.expanduser('~'), "Downloads")):
			if information['title'] in file and os.path.isfile(file):
				assert True

		obj_2 = Automate('https://www.youtube.com/watch?v=XqZsoesa55w')

		information = json.loads(obj_2.info())[0]

		obj_2.download(only_audio=True)

		for file in os.listdir(os.path.join(os.path.expanduser('~'), "Downloads")):
			if information['title'] in file and os.path.isfile(file):
				assert True

	
	@pytest.mark.req_net
	def test_download_subtitle(self):
		auto = Automate('https://www.youtube.com/watch?v=yg8116aeD7E')

		information = json.loads(auto.info())[0]

		auto.download_subtitle()

		for file in os.listdir(os.path.join(os.path.expanduser('~'), "Downloads")):
			if information['title'] in file and os.path.isfile(file) and file.endswith('srt'):
				assert True



	@pytest.mark.req_net
	def test_download_playlist(self):
		playlist = Automate(
			"https://www.youtube.com/playlist?list=PL9FUXHTBubp-_e0wyNu1jfVVJ2QVAi5NW"
		).download_playlist(limit=2)

		# equivalent to assert True or False because download_playlist returns bool
		assert playlist

	
	@pytest.mark.parametrize(
		'obj, total',
		[
			(
				Automate(
					'https://www.youtube.com/watch?v=vFWv44Z4Jhk',
					'https://www.youtube.com/watch?v=zK3PQ_KY_0s',
					'https://www.youtube.com/watch?v=Kx68g1rLbbU'
				),3),

			(Automate(
				urls_with_res={
				'https://www.youtube.com/watch?v=TgItkJCm09c': '480p',
				'https://www.youtube.com/watch?v=y3Z5EuJVFoU': '720p',
				'https://www.youtube.com/watch?v=vFWv44Z4Jhk': '1080p',
				'https://www.youtube.com/watch?v=XqZsoesa55w': '720p',
				}), 4),

			(Automate(
				(
					'https://www.youtube.com/watch?v=vFWv44Z4Jhk',
					'https://www.youtube.com/watch?v=zK3PQ_KY_0s',
					'https://www.youtube.com/watch?v=Kx68g1rLbbU'
				),
				urls_with_res={
				'https://www.youtube.com/watch?v=TgItkJCm09c': '480p',
				'https://www.youtube.com/watch?v=y3Z5EuJVFoU': '1080p',
				'https://www.youtube.com/watch?v=XqZsoesa55w': '720p',
				}), 6),

			(Automate(
				'https://www.youtube.com/watch?v=vFWv44Z4Jhk',
				'https://www.youtube.com/watch?v=zK3PQ_KY_0s',
				'https://www.youtube.com/watch?v=Kx68g1rLbbU',
				'https://www.youtube.com/watch?v=TgItkJCm09c',
				'https://www.youtube.com/watch?v=y3Z5EuJVFoU'
			), 5),

			(Automate(watchUrls_and_resolution={
				'https://www.youtube.com/watch?v=vFWv44Z4Jhk': '720p',
				'https://www.youtube.com/watch?v=zK3PQ_KY_0s': '144p',
				'https://www.youtube.com/watch?v=Kx68g1rLbbU': '1080p',
				'https://www.youtube.com/watch?v=TgItkJCm09c': '480p',
				'https://www.youtube.com/watch?v=y3Z5EuJVFoU': '360p'
			}), 5)
		]
	)
	def test__len__(self, obj, total):
		assert obj.__len__() == total


	@pytest.mark.parametrize(
		'obj, representation',
		[
			(
				Automate('https://www.youtube.com/watch?v=vFWv44Z4Jhk'),
				'<Automate urls="{}", urls_with_res="{}{}">\n'.format(json.dumps(['https://www.youtube.com/watch?v=vFWv44Z4Jhk'], indent=4), chr(123), chr(125))
			),

			(
				Automate(urls_with_res={'https://www.youtube.com/watch?v=vFWv44Z4Jhk': '720'}),
				'<Automate urls="[]", urls_with_res="{}">\n'.format(json.dumps({'https://www.youtube.com/watch?v=vFWv44Z4Jhk': '720'}, indent=4))
			),

			(
				Automate('https://www.youtube.com/watch?v=vFWv44Z4Jhk', urls_with_res={'https://www.youtube.com/watch?v=vFWv44Z4Jhk': '720'}),
				'<Automate urls="{}", urls_with_res="{}">\n'.format(json.dumps(['https://www.youtube.com/watch?v=vFWv44Z4Jhk'], indent=4), json.dumps({'https://www.youtube.com/watch?v=vFWv44Z4Jhk': '720'}, indent=4))
			),
		]
	)
	def test__repr__(self, obj, representation):
		assert repr(obj) == representation

