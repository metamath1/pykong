#!/usr/bin/env python

# -----------------------------------------------------------------------------
# Copyright 
# Contributors: Jo,JoonWoo (metamath@gmail.com)
#
# PyKong is a simple KBS Classic FM streaming player using an external media player.
#
# This software is governed by the MIT license

import urllib2, json, getopt, sys
import subprocess as sp

def help():
    print('USAGE: pykong -c [1|2|3] 1:KBS 1FM, 2:KBS 2FM, 3:CBS MUSIC FM')
    
def getadd(url, ch):
    response = urllib2.urlopen(url % ch)
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
    
    if( opts == [] ) :
        print('Stream from default channel, KBS 1FM')
    else :
        for opt, arg in opts :
            if opt == '-c' or opt == '--channel':
                ch = arg
    
    if ch in ['1', '2'] :    
        mms = getadd(config['stream_url'], ch)
    else :
        mms = config[ch]
    
    command = config['player'] + ' ' + mms
    
    p = sp.Popen(command, stdout=sp.PIPE)

if __name__ == "__main__":
	main()
    