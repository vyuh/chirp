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

import pygtk
pygtk.require('2.0')
import gtk, gtk.gdk
import gobject

import threading

import uiext, cache

from pkg_resources import resource_filename
UI_MAIN = resource_filename(__name__, 'ui/chirp.ui')
UI_PREFS = resource_filename(__name__, 'ui/prefs.ui')
UI_SIGNIN = resource_filename(__name__, 'ui/signin.ui')

gobject.threads_init()

class MainWindow(object):
    VIEW_PUBLIC = 1
    VIEW_FRIENDS = 2
    VIEW_USER = 3

    class refreshThread(threading.Thread):
        def __init__(self, window):
            threading.Thread.__init__(self)
            self.window = window
        
        def run(self):
            self.window.clearTweets()

            if self.window.view == self.window.VIEW_PUBLIC:
                statuses = self.window.parent.api.GetPublicTimeline()
            elif self.window.view == self.window.VIEW_FRIENDS:
                statuses = self.window.parent.api.GetFriendsTimeline()
            elif self.window.view == self.window.VIEW_USER:
                statuses = self.window.parent.api.GetUserTimeline('twitter')

            for status in statuses:
                gobject.idle_add(self.window.addTweet, status)

    class avatarUpdateThread(threading.Thread):
        def __init__(self, window, url, iter):
            threading.Thread.__init__(self)
            self.window = window
            self.url = url
            self.iter = iter
        
        def run(self):
            loader = gtk.gdk.PixbufLoader()
            loader.set_size(48, 48)
        
            data = self.window.cachefetcher.fetch(self.url, 900)
            loader.write(data)
            loader.close()

            self.window.model.set_value(self.iter, 0, loader.get_pixbuf())

    def __init__(self, parent):
        self.parent = parent

        self.parent.apiAuthenticate()

        self.cachefetcher = cache.DiskCacheFetcher()

        self.builder = gtk.Builder()
        self.builder.add_from_file(UI_MAIN)
        self.window = self.builder.get_object('mainWindow')

        self.__initTreeView()
        #self.__initAccelerators()
        self.__connectSignals()

        self.tweets = []
        self.view = self.VIEW_FRIENDS

        self.rthread = self.refreshThread(window=self)
        self.refresh()

    def __initTreeView(self):
        treeview = self.builder.get_object('mainTreeView')
        
        # avatar, name, status
        self.model = gtk.ListStore(gobject.TYPE_OBJECT, gobject.TYPE_STRING, gobject.TYPE_STRING)
        treeview.set_model(self.model)

        avatar_cr = uiext.CellRendererRoundedPixbuf()
        user_cr = gtk.CellRendererText()
        status_cr = gtk.CellRendererText()
        
        user_column = gtk.TreeViewColumn('User', None)
        status_column = gtk.TreeViewColumn('Status', status_cr, markup=2)
       
        user_column.pack_start(avatar_cr, False)
        user_column.add_attribute(avatar_cr, 'pixbuf', 0)

        user_column.pack_start(user_cr, True)
        #user_column.add_attribute(user_cr, 'text', 1)
        
        treeview.append_column(user_column)
        treeview.append_column(status_column)

        # get loading icon

        icon_theme = gtk.icon_theme_get_default()
        try:
            self.loading_image = icon_theme.load_icon("image-loading", 48, 0)
        except gobject.GError, exc:
            self.loading_image = None

    def __initAccelerators(self):
        accels = gtk.AccelGroup()

        key, modifier = gtk.accelerator_parse('f5')
        accels.connect_group(key, modifier, gtk.ACCEL_VISIBLE, self.refresh) # f5

        self.window.add_accel_group(accels)

    def __connectSignals(self):
        self.builder.connect_signals({
            'on_mainWindow_delete_event': self.hide,
            'on_updateButton_clicked': self.refresh
        })

    def addTweet(self, status):
        tweettext = '<b>' + status.user.screen_name + '</b>\n' + status.text
        #'<small>' + tweet.created_at + '</small>'

        data = [self.loading_image,
                status.user.screen_name,
                tweettext]

        listiter = self.model.append(data)

        authread = self.avatarUpdateThread(self, status.user.profile_image_url, listiter)
        authread.start()

    def clearTweets(self):
        self.model.clear()

    def sendUpdate(self, widget=None, event=None):
        pass

    def refresh(self, widget=None, event=None):
        if not self.rthread.isAlive():
            self.rthread = self.refreshThread(window=self)
            self.rthread.start()

    def show(self, widget=None, event=None):
        self.parent.show()
        self.window.show()

    def hide(self, widget=None, event=None):
        self.parent.hide()
        self.window.hide()

    """
    def pushStatus(self, context, text):
        statusbar = self.builder.get_object('statusbar')
        contextid = gtk.Statusbar.get_context_id(statusbar, context)
        statusbar.push(contextid, text)
        return contextid

    def popStatus(self, contextid):
        statusbar = self.builder.get_object('statusbar')
        statusbar.pop(contextid)

    def toggleStatusbar(self, widget=None, event=None):
        statusbar = self.builder.get_object('statusbar')
        checkbox = self.builder.get_object('menuitemStatusbar')
        if checkbox.active == False:
            statusbar.hide()
        else:
            statusbar.show()
    """

class PreferencesDialog(object):
    def __init__(self, parent):
        self.parent = parent
        self.dialog = self.builder.get_object('prefsDialog')

    def run(self):
        self.dialog.run()
