## autoYT
autoYT is lightweight library that automates downloading of youtube videos, subtitles (if available) and playlist.

## Installation
autoYT requires an installation of python 3.6 or greater, as well as pip. <br>
To install from pypi with pip:
```
pip install autoYT
```

## Usage
First of all import `Automate` class from `autoYT`

```python
from autoYT import Automate
```
**Quick demo:** let's say you want to download three videos and their subtitles after two hours and half and when it's done the computer shuts down itself
```python
from autoYT import Automate

Automate().after('2h-30m')
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
info = Automate('https://www.youtube.com/watch?v=XqZsoesa55w').info()
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
            "360p"
        ],
        "highest_resolution": "360p",
        "lowest_resolution": "360p",
        "views": "8,343,725,340",
        "rating": 3.7,
        "age_restricted": false
    }
]
```
As you can see the output above is in `json` format but what if you prefer `yaml` format than `json` just pass keyword string `yaml` as an argument in the `info` like -

```python
info = Automate(('https://www.youtube.com/watch?v=XqZsoesa55w',)).info('yaml')
print(info)
```
Output will be in `yaml` format -

```yaml
-   age_restricted: false
    author: Pinkfong! Kids' Songs & Stories
    available_resolution:
    - 360p
    filesize: 11.4MiB
    highest_resolution: 360p
    lowest_resolution: 360p
    publish_date: '2016-06-17'
    rating: 3.7
    thumbnail_url: https://i.ytimg.com/vi/XqZsoesa55w/maxresdefault.jpg
    title: 'Baby Shark Dance | #babyshark Most Viewed Video | Animal Songs | PINKFONG Songs for Children'
    type: video/mp4
    video_id: XqZsoesa55w
    views: 8,343,725,340
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
Automate("https://www.youtube.com/playlist?list=PLS1QulWo1RIaJECMeUT4LFwJ-ghgoSH6n").download_playlist(limit=10)
```
Remember if you don't specify `location` by default will be in `Downloads` don't worry about on what platform you are on. and also you can download their subtitles to by passing this `subtitle=True` argument

## Overview
#### main class:
- **[Automate](#automate)**

#### available methods:
- **[after()](#after)**
- **[info()](#info)**
- **[generate_watch_url_from_playlist()](#generate_watch_url_from_playlist)**
- **[download()](#download)**
- **[download_subtitle()](#download_subtitle)**
- **[download_playlist()](#download_playlist)**
- **[shutdown()](#shutdown)**

### Automate
Class for automating youtube videos or audios downloading
```python
Automate(*urls: tuple or list,**urls_with_res: dict)
```
`:param:` *list or tuple urls:*<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; valid list or tuple of YouTube watch URLs.

`:param:` *dict urls_with_res:*<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; dict where keys are valid YouTube watch URLs and values are valid video resolutions.

### after
Method for delaying time which are in format of human readable time (2h:30m).
```python
Automate().after('20m:15s')
```
`:param:` *str time*<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; string time for delaying which written in human readable format - ex.
`2h:30m` or `2h-30m` or `30s` where `h` -> `hours`, `m` -> `minutes` and `s` -> `second`

### info 
Method for giving some useful information about the videos or audios.
```python
Automate('https://www.youtube.com/watch?v=XqZsoesa55w').info()
```
-- OR --
```python
Automate('https://www.youtube.com/watch?v=XqZsoesa55w').info('yaml')
```
`:param:` *str fmt*<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; String ftm (format) controls the return type by default is `json` and other available format is `yaml`<br>
`:rtype:` *yaml or json*

### generate_watch_url_from_playlist
Method for generating watch_url from playlist <br>

```python
Automate(
    'https://www.youtube.com/playlist?list=PLS1QulWo1RIaJECMeUT4LFwJ-ghgoSH6n'
).generate_watch_url_from_playlist()
```
`:rtype:` *list*
### download
Method for automating the downloading of YouTube videos
```

```