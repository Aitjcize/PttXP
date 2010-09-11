# process.py
#
# Copyright (C) 2010 -  Wei-Ning Huang (AZ) <aitjcize@gmail.com>
# All Rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import re
import time

HELPTEXT = """PttXP Help

Macros:
1. #connect HOST
   - connect to HOST
2. #login HOST,USER,PASSWD
   - login to host with USER and PASSWD
3. #enter
   - emulate pressing 'Enter'
4. #up
   - emulate pressing 'Key Up'
5. #down
   - emulate pressing 'Key Down'
6. #left
   - emulate pressing 'Key Left'
7. #right
   - emulate pressing 'Key Right'
8. #pagedown
   - emulate pressing 'Key PageDown'
9. #pageup
   - emulate pressing 'Key PageUp'
10. #home
   - emulate pressing 'Key Home'
11. #end
   - emulate pressing 'Key End'
12. #ctrl-KEY
   - emulate pressing 'Ctrl+KEY'
13. #goboard BOARD
   - go to board named BOARD
14. #postfile TITLE,FILENAME
   - post a article titled TITLE, file content from FILENAME
15. #fromfile FILENAME
   - Write content from file with FILENAME
16. #crosspost CP_LIMIT,BOARDLIST_FILENAME,TITLE,FILENAME
   - Cross posting:
      CP_LIMIT: the number of the posts that you will get caught
      BOARDLIST_FILENAME: list of board names you want to post
      TITLE: title of the article
      FILENAME: file name of the content to be post

Example:
1. Login to PTT:
   - The easy way:
       #login ptt.cc,user,passwd

   - The hard way:
       #connect ptt.cc
       user
       #enter
       passwd
       #enter

2. Post an article in a board:
    - The easy way:
        #goboard BOARD
        #postfile The is a testing article,content.txt

    - The hard way:
        #goboard BOARD
        #ctrl-p
        #enter
        This is a testing article
        #enter
        #fromfile content.txt
        #ctrl-x
        s
        #enter
        #enter
"""

class PttXPScriptRunner:
    def __init__(self, client, showterm=False):
        self.client = client
        self.showterm = showterm
        self.stop = False
        self.cmds = {}
        self.cmds['^#connect (.*)'] = self.client.connect
        self.cmds['^#login ([^,]*),([^,]*),(.*)'] = self.client.login
        self.cmds['^#logout'] = self.client.logout
        self.cmds['^#enter'] = self.client.key_enter
        self.cmds['^#up'] = self.client.key_up
        self.cmds['^#down'] = self.client.key_down
        self.cmds['^#left'] = self.client.key_left
        self.cmds['^#right'] = self.client.key_right
        self.cmds['^#pageup'] = self.client.key_pageup
        self.cmds['^#pagedown'] = self.client.key_pagedown
        self.cmds['^#home'] = self.client.key_home
        self.cmds['^#end'] = self.client.key_end
        self.cmds['^#ctrl-([a-z])'] = self.client.key_control
        self.cmds['^#goboard (.*)'] = self.client.go_board
        self.cmds['^#postfile ([^,]*),(.*)'] = self.client.postfile
        self.cmds['^#fromfile (.*)'] = self.client.write_content_from_file
        self.cmds['^#crosspost ([^,]*),([^,]*),([^,]*),(.*)'] = \
                self.client.crosspost

    def run(self, script):
        controls = script.split('\n')
        for term in controls:
            if self.showterm:
                self.client.print_message("Executing '%s' ..." % term)
            # stop if signaled
            if self.stop: return

            time.sleep(0.3)
            for key in self.cmds:
                got = re.findall(key, term)
                var = key.count('(')
                if got:
                    if var == 0:
                        self.cmds[key]()
                        break;
                    elif var == 1:
                        self.cmds[key](got[0])
                        break;
                    elif var == 2:
                        self.cmds[key](*got[0])
                        break;
                    elif var == 3:
                        self.cmds[key](*got[0])
                        break;
                    elif var == 4:
                        self.cmds[key](*got[0])
                        break;
            else:
                self.client.write(term)