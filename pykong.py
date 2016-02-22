#!/usr/bin/env python

import urllib2, json
import subprocess as sp

def getadd(ch):
    response = urllib2.urlopen("http://kong.kbs.co.kr/live_player/channelMini.php?id=kbs&channel=%s" % ch)
    st = response.read()
    index1 = st.find("mms:")
    address = st[index1:]
    return address

def main():
    with open ("config.json", "r") as config_file:
        config_json = config_file.read()
    
    config = json.loads(config_json)
    mms = getadd(1)
    command = config['player'] + ' ' + mms
    p = sp.Popen(command, stdout=sp.PIPE)

if __name__ == "__main__":
	main()
    