# -*- coding: utf-8 -*-
import sys
import urllib.parse
import xbmcplugin
import xbmcgui
import xbmcaddon
import requests

addon = xbmcaddon.Addon()
handle = int(sys.argv[1])
TMDB_API_KEY = '78e5fd786504cce2f45126a53c490c2a'

def build_url(query):
    return sys.argv[0] + '?' + urllib.parse.urlencode(query)

def list_main_menu():
    xbmcplugin.setPluginCategory(handle, 'Main Menu')
    xbmcplugin.addDirectoryItem(handle, build_url({'action': 'search'}), xbmcgui.ListItem('Search for Movies/TV Shows'), True)
    xbmcplugin.addDirectoryItem(handle, build_url({'action': 'custom_links'}), xbmcgui.ListItem('Live Channels and Direct Links'), True)
    xbmcplugin.endOfDirectory(handle)

def search_tmdb():
    keyboard = xbmcgui.Dialog().input('Enter movie or TV show name:', type=xbmcgui.INPUT_ALPHANUM)
    if not keyboard:
        return

    url = f'https://api.themoviedb.org/3/search/multi?api_key={TMDB_API_KEY}&query={urllib.parse.quote(keyboard)}&language=en-US'
    data = requests.get(url).json()

    for item in data.get('results', []):
        id = item['id']
        title = item.get('title') or item.get('name')
        type_ = item.get('media_type')
        thumb = item.get('poster_path')
        img_url = f'https://image.tmdb.org/t/p/w500{thumb}' if thumb else ''

        li = xbmcgui.ListItem(label=title)
        li.setArt({'thumb': img_url, 'icon': img_url})
        url = build_url({'action': 'play', 'id': id, 'type': type_})
        xbmcplugin.addDirectoryItem(handle, url, li, True)

    xbmcplugin.endOfDirectory(handle)

def play_stream(params):
    id = params.get('id')
    type_ = params.get('type')

    sources = {
        'Vidsrc': f'https://vidsrc.to/embed/{ "movie" if type_ == "movie" else "tv" }/{id}?sub=heb',
        'Strime': f'https://strime.to/embed/{type_}/{id}?sub=heb',
        'SuperEmbed': f'https://multiembed.mov/embed/{type_}?id={id}&lang=he'
    }

    for name, url in sources.items():
        li = xbmcgui.ListItem(label=name)
        li.setProperty('IsPlayable', 'true')
        play_url = build_url({'action': 'direct', 'url': url})
        xbmcplugin.addDirectoryItem(handle, play_url, li, False)

    xbmcplugin.endOfDirectory(handle)

def play_direct(params):
    url = params.get('url')
    li = xbmcgui.ListItem(path=url)
    li.setProperty('IsPlayable', 'true')
    xbmcplugin.setResolvedUrl(handle, True, li)

def list_custom_links():
    channels = [
        {
            'name': 'Kan Kids',
            'url': 'https://kan23.media.kan.org.il/hls/live/2024691/2024691/source1_2.5k/chunklist.m3u8',
            'logo': 'https://upload.wikimedia.org/wikipedia/he/thumb/e/e5/Kan_educational_2018.svg/200px-Kan_educational_2018.svg.png'
        },
        {
            'name': 'Kan 11',
            'url': 'https://kan11.media.kan.org.il/hls/live/2024514/2024514/master.m3u8',
            'logo': 'https://upload.wikimedia.org/wikipedia/he/thumb/5/5b/Kan11_logo_2023.svg/200px-Kan11_logo_2023.svg.png'
        },
        {
            'name': 'Channel 12',
            'url': 'http://stremioaddon.vercel.app/mako',
            'logo': 'https://upload.wikimedia.org/wikipedia/he/thumb/0/07/Keshet_12_logo_2017.svg/200px-Keshet_12_logo_2017.svg.png'
        },
        {
            'name': 'Channel 13',
            'url': 'https://reshet.g-mana.live/media/4607e158-e4d4-4e18-9160-3dc3ea9bc677/mainManifest.m3u8',
            'logo': 'https://upload.wikimedia.org/wikipedia/he/thumb/e/e2/Reshet13_logo.svg/200px-Reshet13_logo.svg.png'
        },
        {
            'name': 'Channel 14',
            'url': 'https://ch14-channel14-content.akamaized.net/hls/live/2104807/CH14_CHANNEL14/master.m3u8',
            'logo': 'https://upload.wikimedia.org/wikipedia/he/thumb/c/c3/Channel14_2021_logo.svg/200px-Channel14_2021_logo.svg.png'
        },
        {
            'name': 'i24NEWS',
            'url': 'https://bcovlive-a.akamaihd.net/d89ede8094c741b7924120b27764153c/eu-central-1/5377161796001/playlist.m3u8',
            'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/I24news_logo.svg/200px-I24news_logo.svg.png'
        },
        {
            'name': 'Channel 24 / Big Brother',
            'url': 'https://mako-streaming.akamaized.net/direct/hls/live/2035340/ch24live/video_7201280_p_1.m3u8',
            'logo': 'https://upload.wikimedia.org/wikipedia/he/thumb/3/36/Music_24_logo_2020.svg/200px-Music_24_logo_2020.svg.png'
        },
        {
            'name': 'Kan 33',
            'url': 'http://makan.media.kan.org.il/hls/live/2024680/2024680/master.m3u8',
            'logo': 'https://upload.wikimedia.org/wikipedia/he/thumb/3/39/Kan_33_logo.svg/200px-Kan_33_logo.svg.png'
        },
        {
            'name': 'Walla TV',
            'url': 'https://amg01742-walla-wallanews-ono-btlna.amagi.tv/playlist/amg01742-walla-wallanews-ono/playlist.m3u8',
            'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Walla%21_logo.svg/200px-Walla%21_logo.svg.png'
        },
        {
            'name': 'Hidabroot Channel',
            'url': 'https://cdn.cybercdn.live/HidabrootIL/Live97/playlist.m3u8',
            'logo': 'https://www.hidabroot.org/img/logo.svg'
        },
        {
            'name': 'Kabbalah Channel',
            'url': 'https://edge3.uk.kab.tv/live/tv66-heb-high/playlist.m3u8',
            'logo': 'https://kabbalahmedia.info/img/logo.png'
        },
        {
            'name': 'Musayof Channel',
            'url': 'http://wowza.media-line.co.il/Musayof-Live/livestream.sdp/playlist.m3u8',
            'logo': 'https://www.bhol.co.il/ImageGen.ashx?image=/images/archive/110x/1143300.jpg'
        },
        {
            'name': 'Sport 5 (Audio)',
            'url': 'https://rgelive.akamaized.net/hls/live/2043151/radiolive/playlist.m3u8',
            'logo': 'https://upload.wikimedia.org/wikipedia/he/thumb/9/90/Sport5_logo.svg/200px-Sport5_logo.svg.png'
        }
    ]

    for ch in channels:
        li = xbmcgui.ListItem(label=ch['name'])
        li.setArt({'icon': ch['logo'], 'thumb': ch['logo']})
        li.setProperty('IsPlayable', 'true')
        url = build_url({'action': 'direct', 'url': ch['url']})
        xbmcplugin.addDirectoryItem(handle, url, li, False)

    xbmcplugin.endOfDirectory(handle)

def router(paramstring):
    params = dict(urllib.parse.parse_qsl(paramstring))
    action = params.get('action')

    if action is None:
        list_main_menu()
    elif action == 'search':
        search_tmdb()
    elif action == 'play':
        play_stream(params)
    elif action == 'direct':
        play_direct(params)
    elif action == 'custom_links':
        list_custom_links()

if __name__ == '__main__':
    router(sys.argv[2][1:])
