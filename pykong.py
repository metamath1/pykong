#!/usr/bin/env python

import urllib2
import subprocess as sp

def getadd(ch):
	
    response = urllib2.urlopen("http://kong.kbs.co.kr/live_player/channelMini.php?id=kbs&channel=%s" % ch)
	st = response.read()
	
    index1 = st.find("mms:")
    address = st[index1:]
	
    return address

def main():
	#run_wsgi_app(application)
    mms = getadd(1)
    
    command = "C:/PROGRA~2/Daum/PotPlayer/PotPlayerMini "+ mms
    p = sp.Popen(command, stdout=sp.PIPE)

if __name__ == "__main__":
	main()
    