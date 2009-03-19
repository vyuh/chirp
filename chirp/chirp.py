"""
Copyright (c) 2007-2009 Egor Pomortsev <illicium@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import gtk
import twitter
import sys

import config
import ui

VERSION = '0.1'

class Chirp:
    def __init__(self):
        self.api = twitter.Api()
        self.api.SetXTwitterHeaders('Chirp', '', VERSION)

        self.config = config.ChirpConfig()
        
        self.mainwindow = ui.MainWindow(parent=self)
        self.mainwindow.show()

        gtk.main()

    def apiAuthenticate(self, username=None, password=None):
        if not username: username = self.config.getUsername()
        if not password: password = self.config.getPassword()
        
        self.api = twitter.Api(username, password)

    def apiSignout(self):
        self.api.ClearCredentials()

    def showPrefs(self, widget=None, event=None):
        prefs = ui.PreferencesDialog(parent=self)
        prefs.show()

    def show(self):
        pass

    def hide(self):
        self.quit()

    def quit(self, widget=None):
        gtk.main_quit()
        sys.exit(1)

