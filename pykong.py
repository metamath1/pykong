#-*- coding: utf-8 -*-
#!/usr/bin/env python

# -----------------------------------------------------------------------------
# Copyright 
# Contributors: Jo,JoonWoo (metamath@gmail.com)
#
# PyKong is a simple KBS Classic FM streaming player using an external media player.
#
# This software is governed by the MIT license

import sys, os
import curses
import vlc
import json

    
# def getadd(url, ch):
#     response = urllib2.urlopen(url % ch)
#     st = response.read()
#     index1 = st.find("mms:")
#     address = st[index1:]
#     return address

    
def draw_menu(stdscr):
    k = 0
    cursor_x = 0
    cursor_y = 0
    
    ##################################################################
    # READ CONFIG FILE
    with open ("config.json", "r") as config_file:
        config_json = config_file.read()
    
    config = json.loads(config_json)
    ##################################################################
    
    ###################################################################
    # Init. state variable
    select_ch = '1'
    current_ch = '0'
    current_volume = 50
    mute = False
    ch_list = [ ord(station[0]) for station in config["stations"].items() ]

    # ##################################################################
    # Create vlc player https://github.com/oaubert/python-vlc/issues/61
    # http://olivieraubert.net/vlc/python-ctypes/doc/index.html
    # https://stackoverflow.com/questions/46346859/python-vlc-script-error-attributeerror-nonetype-object-has-no-attribute-med
    instance = vlc.Instance(["--prefetch-buffer-size=2000 --prefetch-read-size=5000 --network-caching=1000"]) #define VLC instance
    player = None
    media = None

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)
    
    ###############################################################################
    # Start Main Loop
    ###############################################################################
    # Loop where k is the last character pressed
    while (k != ord('q')):

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        ###############################################################################
        # Process for keys and player
        ###############################################################################

        # channel, volume key, and mute key
        #if k == ord('1'):
        #    select_ch = '1'
        #elif k == ord('2'):
        #    select_ch = '2'
        if k == curses.KEY_UP:
            current_volume += 5
        elif k == curses.KEY_DOWN:
            current_volume -= 5
        elif k == ord('m'):
            mute = not mute
        elif k in ch_list: 
            select_ch = chr(k)
        
        # change current ch.
        if current_ch != select_ch:
            if player != None:
                player.stop()
                player.release()
            
            #if media != None :
            #    media.release()

            # get url from config.json
            url = config["stations"][select_ch]["url"]

            if url[-3:] == "pls":
                player = instance.media_list_player_new()
                media_list = instance.media_list_new([url])
                player.set_media_list(media_list)
            else:
                player = instance.media_player_new() #Define VLC player
                # https://stackoverflow.com/questions/28440708/python-vlc-binding-playing-a-playlist    
                media = instance.media_new(url) #Define VLC media
                player.set_media(media)  #Set player media
                
            player.play() #Play the media

            current_ch = select_ch
        
        # vol and mute
        # https://stackoverflow.com/questions/45150694/how-to-change-the-volume-of-playback-in-medialistplayer-with-libvlc
        if url[-3:] == "pls":
            player.get_media_player().audio_set_volume(current_volume)
            player.get_media_player().audio_set_mute(mute)
        else:
            player.audio_set_volume(current_volume)
            player.audio_set_mute(mute)


        ###############################################################################
        # Draw Screen
        ###############################################################################

        # Declaration of strings
        title = "Pykong"[:width-1]
        title1 = "   ___         _                         "[:width-1]
        title2 = "  / _ \ _   _ | | __  ___   _ __    __ _ "[:width-1]
        title3 = " / /_)/| | | || |/ / / _ \ | '_ \  / _` |"[:width-1]
        title4 = "/ ___/ | |_| ||   < | (_) || | | || (_| |"[:width-1]
        title5 = "\/      \__, ||_|\_\ \___/ |_| |_| \__, |"[:width-1]
        title6 = "        |___/                      |___/ "[:width-1]
        
        subtitle = "Written by metamath"[:width-1]
        channel_strs = [ station[1]["name"] for station in config["stations"].items()  ]
        statusbar_str = "Press 'q' to exit | Current Station : {} | Vol. : {} | Mute : {}"\
                .format(channel_strs[int(select_ch)-1], current_volume, mute)
        
        if k == 0:
            keystr = "No key press detected..."[:width-1]

        # Centering calculations
        start_x_title = int((width // 2) - (len(title1) // 2) - len(title1) % 2)
        start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
        start_y = 3

        # Rendering some text
        whstr = "Width: {}, Height: {}".format(width, height)
        stdscr.addstr(0, 0, whstr, curses.color_pair(1))

        # Render status bar
        if mute:
            stdscr.attron(curses.color_pair(4))
            stdscr.addstr(height-1, 0, statusbar_str)
            stdscr.addstr(height-1, len(statusbar_str), " " * (width - len(statusbar_str) - 1))
            stdscr.attroff(curses.color_pair(4))
        else:
            stdscr.attron(curses.color_pair(3))
            stdscr.addstr(height-1, 0, statusbar_str)
            stdscr.addstr(height-1, len(statusbar_str), " " * (width - len(statusbar_str) - 1))
            stdscr.attroff(curses.color_pair(3))
            
            
        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)

        # Rendering title
        #stdscr.addstr(start_y, start_x_title, title)
        stdscr.addstr(start_y,   start_x_title, title1)
        stdscr.addstr(start_y+1, start_x_title, title2)
        stdscr.addstr(start_y+2, start_x_title, title3)
        stdscr.addstr(start_y+3, start_x_title, title4)
        stdscr.addstr(start_y+4, start_x_title, title5)
        stdscr.addstr(start_y+5, start_x_title, title6)

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print the rest of text
        stdscr.addstr(start_y + 6, start_x_subtitle, subtitle)
        stdscr.addstr(start_y + 8, (width // 2) - 2, '-' * 4)
        
        init_ch_start_y = start_y + 9
        ch_str_offset = 2
        for i, channel_str in enumerate(channel_strs):
            if int(select_ch) == i+1 :
                stdscr.attron(curses.color_pair(1))
                stdscr.attron(curses.A_BOLD)
                stdscr.addstr(init_ch_start_y + ch_str_offset*(i+1), start_x_keystr, channel_str)
                stdscr.attroff(curses.color_pair(1))
                stdscr.attroff(curses.A_BOLD)
            else:
                stdscr.addstr(init_ch_start_y + ch_str_offset*(i+1), start_x_keystr, channel_str)
        
        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()
    # while (k != ord('q')):


    # free player, media
    # media.release()
    player.stop()
    player.release()
    instance.release()
    
def main():
    # external player or its own
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()
