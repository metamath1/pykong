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
import urllib2, json


    
def getadd(url, ch):
    response = urllib2.urlopen(url % ch)
    st = response.read()
    index1 = st.find("mms:")
    address = st[index1:]
    return address

    
def draw_menu(stdscr):
    k = 0
    cursor_x = 0
    cursor_y = 0
    
    # ##################################################################
    # READ CONFIG FILE
    with open ("config.json", "r") as config_file:
        config_json = config_file.read()
    
    config = json.loads(config_json)
    # ##################################################################
    
    # ##################################################################
    # Create vlc player
    instance = vlc.Instance() #define VLC instance
    player   = instance.media_player_new() #Define VLC player
    
    # ##################################################################
    # Init. state variable
    media = None
    select_ch = 0
    current_volume = -1
    mute = False
    
    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)
    
    # Loop where k is the last character pressed
    while (k != ord('q')):

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        # channel and volume key 
        if k == 49 :
            select_ch = 1
        elif k == 50 :
            select_ch = 2
        elif k == 51 :
            select_ch = 3
        elif k == curses.KEY_UP :
            current_volume += 5
            player.audio_set_volume(current_volume)
        elif k == curses.KEY_DOWN :
            current_volume -= 5
            player.audio_set_volume(current_volume)
        elif k == ord('m') :
            mute = not mute
            player.audio_set_mute(mute)
            
        # play selected station
        if select_ch == 0 or (select_ch != 0 and ch != select_ch) :
            if select_ch != 0 :
                ch = str(select_ch)
            else :
                ch = '1' #default
                
            #change ch to str
            if ch in ['1', '2'] :    
                url = getadd(config['stream_url'], ch)
            else :
                url = config[ch]
            
            if media != None :
                media.release()
                
            media=instance.media_new(url) #Define VLC media
            player.set_media(media)  #Set player media
            player.play() #Play the media
            
            # set play channel to select channel
            select_ch = ch
            
            #get current
            current_volume = player.audio_get_volume()

        # Declaration of strings
        title = "Pykong"[:width-1]
        subtitle = "Written by metamath"[:width-1]
        
        # config 파일 읽어오기..
        channel_strs = [ "[1] KBS 1 FM", "[2] KBS 2 FM", "[3] CBS MUSIC FM" ]
        
        #statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {}".format(cursor_x, cursor_y)
        statusbarstr = "Press 'q' to exit | Current Station : {} | Vol. : {} | Mute : {}".format(channel_strs[int(ch)-1], current_volume, mute)
        
        if k == 0:
            keystr = "No key press detected..."[:width-1]

        # Centering calculations
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
        start_y = int((height // 2) - 2)

        # Rendering some text
        whstr = "Width: {}, Height: {}".format(width, height)
        stdscr.addstr(0, 0, whstr, curses.color_pair(1))

        # Render status bar
        if mute :
            stdscr.attron(curses.color_pair(4))
            stdscr.addstr(height-1, 0, statusbarstr)
            stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
            stdscr.attroff(curses.color_pair(4))
        else :
            stdscr.attron(curses.color_pair(3))
            stdscr.addstr(height-1, 0, statusbarstr)
            stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
            stdscr.attroff(curses.color_pair(3))
            
            
        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)

        # Rendering title
        stdscr.addstr(start_y, start_x_title, title)

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
        stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
        
        init_ch_start_y = start_y + 4
        ch_str_offset = 2
        for i, channel_str in enumerate(channel_strs) :
            if int(ch) == i+1 :
                stdscr.attron(curses.color_pair(1))
                stdscr.attron(curses.A_BOLD)
                stdscr.addstr(init_ch_start_y + ch_str_offset*(i+1), start_x_keystr, channel_str)
                stdscr.attroff(curses.color_pair(1))
                stdscr.attroff(curses.A_BOLD)
            else :
                stdscr.addstr(init_ch_start_y + ch_str_offset*(i+1), start_x_keystr, channel_str)
        
        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()
    
    # free player, media
    media.release()
    instance.release()
    
def main():
    # external player or its own
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()