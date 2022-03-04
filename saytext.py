# thanks to Jeff Wintersinger for doing most of the work here
# see https://github.com/jwintersinger/groceryslots

import pychromecast
import gtts
import os
import sys
import argparse
import time

CHROMECAST_DEVICE = 'Bedroom speaker'
HTTP_IP = '192.168.109.102'
HTTP_PORT = 8000
HTTP_PATH = '/out.mp3'
AUDIO_PATH = '/tmp/out.mp3'

def say(text, volume=1.0):
	speech = gtts.gTTS(text = text, lang = 'en', slow = False)
	speech.save(AUDIO_PATH)

	services, browser = pychromecast.discovery.discover_chromecasts()

	pychromecast.discovery.stop_discovery(browser)
	chromecasts, browser = pychromecast.get_chromecasts()
	print(cc)
	cast = next(C for C in cc if C.device.friendly_name == CHROMECAST_DEVICE)
	cast.wait()
	cast.set_volume(volume)
	cast.wait()

	mc = cast.media_controller
	mc.play_media('http://%s:%s%s' % (HTTP_IP, HTTP_PORT, HTTP_PATH), 'audio/mp3')
	mc.block_until_active()

def main():
	parser = argparse.ArgumentParser(
	description='LOL HI THERE',
	formatter_class=argparse.ArgumentDefaultsHelpFormatter
	)
	parser.add_argument('--volume', type=float, default=0.5)
	parser.add_argument('text')
	args = parser.parse_args()

	say(args.text, args.volume)

if __name__ == '__main__':
	main()
