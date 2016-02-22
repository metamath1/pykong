#!/usr/bin/env python

import urllib2, json, getopt, sys
import subprocess as sp

def help():
    print('USAGE: pykong -c [1|2] 1:KBS 1FM, 2:KBS 2FM')
    
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
    
    #default is kbs classic fm
    ch = 1
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:', ['channel='])
    except getopt.GetoptError as err:
        print str(err)
        help()
        sys.exit(1)
    
    for opt, arg in opts :
        if opt == '-c' or opt == '--channel':
            ch = arg
            
    mms = getadd(ch)
    command = config['player'] + ' ' + mms
    p = sp.Popen(command, stdout=sp.PIPE)

if __name__ == "__main__":
	main()
    