"""
Copyright (c) 2007 George Pomortsev <illicium@gmail.com>

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
import ui

VIEW_PUBLIC = 1
VIEW_FRIENDS = 2
VIEW_USER = 3

class ChirpGTK(object):
    def __init__(self, parent):
        self.parent = parent
        self.mainwindow = ui.MainWindow(parent=self)

        self.view = VIEW_PUBLIC
        
        self.mainwindow.show()
        self.refresh()
        gtk.main()

    def refresh(cls, widget=None, event=None):
        cls.mainwindow.clearTweets()
        if cls.view == VIEW_PUBLIC:
            for tweet in cls.parent.api.GetPublicTimeline():
                cls.mainwindow.addTweet(tweet)

    def show(cls, widget=None, event=None):
        cls.mainwindow.show()

    def hide(cls, widget=None, event=None):
        cls.mainwindow.hide()
        cls.quit()

    def showPrefs(cls, widget=None, event=None):
        prefs = ui.PreferencesDialog(parent=cls)
        prefs.show()

    def quit(cls):
        gtk.main_quit()
        cls.parent.quit()


