
## automateYT
<a href="" title="Python versions"><img src="https://img.shields.io/pypi/pyversions/automateYT?style=flat"></a>
<a href="" title="Pypi version"><img src="https://img.shields.io/pypi/v/automateYT?style=flat"></a>
<a href="" title="Contributions are welcome"><img src="https://img.shields.io/badge/contributions-welcome-blue.svg?style=flat"></a>
<a href="" title="Code size"><img src="https://img.shields.io/github/languages/code-size/umutambyi-gad/automateYT?color=blue&style=flat"></a>
<a href="" title="License"><img src="https://img.shields.io/pypi/l/automateYT?color=blue&style=flat"></a>


automateYT is lightweight library for automating to download youtube videos, subtitles (if available) and playlist.

## Installation
automateYT requires an installation of python 3.6 or greater and [pytube](https://github.com/pytube/pytube.git), as well as pip. Pip is typically bundled with python installations, and you can find options
for how to install python at [`https://python.org`](https://python.org). <br>
- To install from pypi with pip:
```bash
pip install automateYT
```
- Clone GitHub repository
```bash
git clone https://github.com/umutambyi-gad/automateYT
```

## Overview
####  Classes:
- **[`Timing`](#timing)**
- **[`Automate`](#automate)**

#### Methods:
- **[`after()`](#after)**
- **[`info()`](#info)**
- **[`generate_watch_url_from_playlist()`](#generate_watch_url_from_playlist)**
- **[`download()`](#download)**
- **[`download_subtitle()`](#download_subtitle)**
- **[`download_playlist()`](#download_playlist)**
- **[`shutdown()`](#shutdown)**

## Usage
First of all import `Automate` class from `automateYT`

```python
from automateYT import Automate
```
**Quick demo:** let's say you want to download three videos and their subtitles after two hours and half and when it's done the computer shuts down itself
```python
from automateYT import Automate
from automateYT import Timing

Timing().after('2h-30m') # or Automate().after('2h-30m') since Automate extends Timing
Automate([
	'https://www.youtube.com/watch?v=XqZsoesa55w',
	'https://www.youtube.com/watch?v=F4tHL8reNCs',
	'https://www.youtube.com/watch?v=F4tHL8reNCs'
]).download(subtitle=True, location='C:/Users/GentleMan/videos', shutdown=True)
```
The above script will download all given videos and output them on `C:/Users/GentleMan/videos` but if you didn't specify `location` by default will in the `Downloads` and also script will pick the `highest resolution` available
but what if you want to customize the videos' resolution just see the following example.

```python
Automate(url_with_res={
	'https://www.youtube.com/watch?v=XqZsoesa55w': '720p',
	'https://www.youtube.com/watch?v=F4tHL8reNCs': '1080p',
	'https://www.youtube.com/watch?v=F4tHL8reNCs': '144p'
}).download(subtitle=True, shutdown=True)
```
Watch closely before passing `dict` where `keys` are valid watch urls and `values` are valid resolution I passed an argument called `url_with_res` it's an obligation to pass argument before the `dict` otherwise it will raise an error but cool thing is that you don't have to memorize this `url_with_res` you can simply rename it to whatever you want without any further configurations just like.
```python
Automate(watchUrls_with_their_resolution={
    'https://www.youtube.com/watch?v=XqZsoesa55w': '720p',
    ...
})...

```
Now you saw how to download them but we have passed watch url on in `Automate` class like `Automate('https://www.youtube.com/watch?v=XqZsoesa55w')` so what makes you think it's the true watch url
here is how you can view major information about the watch url.
```python
info = Automate(
    'https://www.youtube.com/watch?v=XqZsoesa55w'
).info()
print(info)
```
Output will be something like - 

```json
[
    {
        "watch_url": "https://www.youtube.com/watch?v=XqZsoesa55w",
        "video_id": "XqZsoesa55w",
        "title": "Baby Shark Dance | #babyshark Most Viewed Video | Animal Songs | PINKFONG Songs for Children",
        "thumbnail_url": "https://i.ytimg.com/vi/XqZsoesa55w/maxresdefault.jpg",
        "author": "Pinkfong! Kids' Songs & Stories",
        "publish_date": "2016-06-17",
        "type": "video/mp4",
        "filesize": "11.4MiB",
        "available_resolution": [
            "144p",
            "240p",
            "360p",
            "480p",
            "720p",
            "1080p"
        ],
        "highest_resolution": "1080p",
        "lowest_resolution": "360p",
        "views": "8,350,191,773",
        "rating": 3.7,
        "age_restricted": false
    }
]
```
As you can see the output above is in `json` format but what if you prefer `yaml` format than `json` just pass keyword string `yaml` as an argument in the `info` like -

```python
info = Automate(
    ('https://www.youtube.com/watch?v=XqZsoesa55w',)
).info('yaml')
print(info)
```
Output will be in `yaml` format -

```yaml
-   age_restricted: false
    author: Pinkfong! Kids' Songs & Stories
    available_resolution:
    - 144p
    - 240p
    - 360p
    - 480p
    - 720p
    - 1080p
    filesize: 11.4MiB
    highest_resolution: 1080p
    lowest_resolution: 360p
    publish_date: '2016-06-17'
    rating: 3.7
    thumbnail_url: https://i.ytimg.com/vi/XqZsoesa55w/maxresdefault.jpg
    title: 'Baby Shark Dance | #babyshark Most Viewed Video | Animal Songs | PINKFONG
        Songs for Children'
    type: video/mp4
    video_id: XqZsoesa55w
    views: 8,350,191,773
    watch_url: https://www.youtube.com/watch?v=XqZsoesa55w


```
And we all know that youtube can have playlist which contains couple of videos, the following is how you can generate watch urls of every single video from the playlist.

```python
from pprint import pprint

watchUrls = Automate(
    "https://www.youtube.com/playlist?list=PLS1QulWo1RIaJECMeUT4LFwJ-ghgoSH6n"
).generate_watch_url_from_playlist()
pprint(watchUrls)
```
An output will be something like -
```python
[
    'https://www.youtube.com/watch?v=F9TZb0XBow0',
    'https://www.youtube.com/watch?v=26VtIlzEcmU',
    'https://www.youtube.com/watch?v=41qgdwd3zAg',
    ...
]
```

So not only you can generate watch urls from playlist url but also you can download them all or provide an integer `limit` argument to limit videos to be downloaded from the playlist.

```python
Automate(
    "https://www.youtube.com/playlist?list=PLS1QulWo1RIaJECMeUT4LFwJ-ghgoSH6n"
).download_playlist(limit=10)
```
Remember if you don't specify `location` by default will be in `Downloads` don't worry about on what platform you are on. and also you can download their subtitles to by passing this `subtitle=True` argument.

## Documentation

### Timing
class for converting string time looks like (`2h:30m`, `2h30m`, or `2h-30m`) into seconds and delay time 

### Automate
Class with methods for automating to download youtube videos as either videos or audios, subtitles (if available) and generating watch urls from youtube playlist.
```python
Automate(*urls: tuple or list,**urls_with_res: dict)
```
`:param:` *list or tuple urls:*<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; valid list or tuple of YouTube watch URLs.

`:param:` *dict urls_with_res:*<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; dict where keys are valid YouTube watch URLs and values are valid video resolutions.

### after
Method for delaying time which are in format of human readable time (`2h:30m`)
```python
Timing().after('20m:15s')
```
`:param:` *str time*<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; string time for delaying which written in human readable format - ex.
`2h:30m` or `2h-30m` or `30s` where `h` -> `hours`, `m` -> `minutes` and `s` -> `second`

### info
Method for giving some useful information about the youtube videos in easy and readable format.
```python
Automate('https://www.youtube.com/watch?v=XqZsoesa55w').info()
```
-- or --
```python
Automate('https://www.youtube.com/watch?v=XqZsoesa55w').info('yaml')
```
`:param:` *str fmt*<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; String ftm (format) controls the return type by default is `json` and other available format is `yaml`<br>
`:rtype:` *yaml or json*

### generate_watch_url_from_playlist
Method for generating valid youtube watch urls from the youtube playlist

```python
Automate(
    'https://www.youtube.com/playlist?list=PLS1QulWo1RIaJECMeUT4LFwJ-ghgoSH6n'
).generate_watch_url_from_playlist()
```
`:rtype:` *list*
### download
Method for downloading of custom resolution YouTube videos as videos or audio and also subtitles (if available) 

```python
Automate(
    'https://www.youtube.com/watch?v=XqZsoesa55w',
).download(
    subtitle=True,
    location='C:/Users/GentleMan/videos',
    only_audio=True,
    shutdown=True
)
```

`:param:` str location <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; location path on your computer to save the downloads, by default is in Downloads

`:param:` bool highest_res <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; if highest_res is True the script gets the highest resolution available

`:param:` bool lowest_res <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; if lowest_res is True the script gets the lowest resolution available

`:param:` bool subtitle <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; if subtitle is True english version or english auto generated subtitle is downloaded within its video

`:param:` bool shutdown <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; if shutdown is True the computer shuts down after downloads is completely done

`:param:` bool only_audio <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; if only_audio is True audio only is downloaded

### download_subtitle
Method for downloading YouTube video's subtitles (if available) or auto generated one in whatever language

```python
Automate(
    'https://www.youtube.com/watch?v=XqZsoesa55w',
).download(
    location='C:/Users/GentleMan/videos',
    lang_code='en',
    auto_generated=False,
    shutdown=True
)
```
`:param:` str lang_code <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; language code of the subtitle to automate its downloading notice that the default is 'en' (English).

`:param:` str auto_generated <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; by default True, this downloads auto generated version of the same language code in absence of offical one.

`:param:` str location <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; location on your computer to save the downloads, by default is in Downloads.

`:param:` bool shutdown <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; if shutdown is True the computer shuts down after downloads is completely done.

### download_playlist
Method for downloading youtube playlist till the limit given is reached

```python
Automate(
    "https://www.youtube.com/playlist?list=PLS1QulWo1RIaJECMeUT4LFwJ-ghgoSH6n"
).download_playlist(
    limit=30
)
```
`:param:` str location <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; location on your computer to save the downloads, by default is in Downloads.

`:param:` bool highest_res <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; if highest_res is True the script gets the highest resolution available.

`:param:` bool lowest_res <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; if lowest_res is True the script gets the lowest resolution available.

`:param:` int limit <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; integer limit limits the number of the videos to be downloaded.

`:param:` bool subtitle <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; if subtitle is True english version or english auto generated subtitle is downloaded within its video.

`:param:` bool shutdown <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; if shutdown is True the computer shuts down after downloads is completely done.
## License
This project is under the [MIT](https://github.com/umutambyi-gad/automateYT/blob/master/LICENSE) license
