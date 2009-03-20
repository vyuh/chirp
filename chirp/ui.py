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
import pango

import string
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
                statuses = self.window.parent.api.GetUserTimeline(self.window.view_user)

            for status in statuses:
                self.window.addTweet(status)

    class avatarUpdateThread(threading.Thread):
        def __init__(self, window, url, iter):
            threading.Thread.__init__(self)
            self.window = window
            self.url = url
            self.iter = iter

        def run(self):
            loader = gtk.gdk.PixbufLoader()

            size = self.window.parent.config.getAvatarPixelSize()
            loader.set_size(size, size)
        
            data = self.window.cachefetcher.fetch(self.url, 900)
            loader.write(data)
            loader.close()

            self.window.model.set_value(self.iter, 0, loader.get_pixbuf())

    def __init__(self, parent):
        self.parent = parent

        self.parent.authenticate()

        self.cachefetcher = cache.DiskCacheFetcher()

        self.builder = gtk.Builder()
        self.builder.add_from_file(UI_MAIN)
        self.window = self.builder.get_object('mainWindow')

        self.__initTreeView()
        #self.__initAccelerators()
        self.__connectSignals()

        self.tweets = []
        self.view = self.VIEW_FRIENDS
        self.view_user = 'chirp'

        self.rthread = self.refreshThread(window=self)
        self.refresh()

    def __initTreeView(self):
        def resize_callback(treeview, allocation, column, cell):
            otherColumns = (c for c in treeview.get_columns() if c != column)
            newWidth = allocation.width - sum(c.get_width() for c in otherColumns)
            newWidth -= treeview.style_get_property('horizontal-separator') * 2

            if cell.props.wrap_width == newWidth or newWidth <= 0: return

            cell.props.wrap_width = newWidth
            store = treeview.get_model()
            iter = store.get_iter_first()

            while iter and store.iter_is_valid(iter):
                store.row_changed(store.get_path(iter), iter)
                iter = store.iter_next(iter)
                treeview.set_size_request(0,-1)

        treeview = self.builder.get_object('mainTreeView')

        if self.parent.config.get('appearance', 'list_striped', bool):
            treeview.set_property('rules-hint', True)
        
        # avatar, name, status
        self.model = gtk.ListStore(gobject.TYPE_OBJECT, gobject.TYPE_STRING, gobject.TYPE_STRING)
        treeview.set_model(self.model)

        if self.parent.config.get('appearance', 'avatar_rounded', bool):
            avatar_cr = uiext.CellRendererRoundedPixbuf()
        else:
            avatar_cr = gtk.CellRendererPixbuf()

        user_cr = gtk.CellRendererText()
        status_cr = gtk.CellRendererText()
        
        user_column = gtk.TreeViewColumn('User', None)
        user_column.pack_start(avatar_cr, False)
        user_column.add_attribute(avatar_cr, 'pixbuf', 0)
        user_column.pack_start(user_cr, True)
        #user_column.add_attribute(user_cr, 'text', 1)

        status_column = gtk.TreeViewColumn('Status', status_cr, markup=2)
        status_cr.set_property('wrap-mode', pango.WRAP_WORD)
        
        treeview.append_column(user_column)
        treeview.append_column(status_column)

        treeview.connect_after('size-allocate', resize_callback, status_column, status_cr)

        # get loading icon

        icon_theme = gtk.icon_theme_get_default()
        try:
            size = self.parent.config.getAvatarPixelSize()
            self.loading_image = icon_theme.load_icon('image-loading', size, 0)
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

            'on_updateButton_clicked': self.sendUpdate,
            'on_refreshButton_clicked': self.refresh,
            'on_prefsButton_clicked': self.parent.showPrefs
        })

    def addTweet(self, status):
        tpl = string.Template(self.parent.config.get('appearance', 'format'))
        text = tpl.safe_substitute({
            'username': status.user.screen_name,
            'message': status.text
        })

        data = [self.loading_image,
                status.user.screen_name,
                text]

        listiter = self.model.append(data)

        authread = self.avatarUpdateThread(self, status.user.profile_image_url, listiter)
        authread.start()

    def clearTweets(self):
        self.model.clear()

    def sendUpdate(self, widget=None, event=None):
        print 'hello world'

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

class PreferencesDialog(object):
    def __init__(self, parent):
        self.parent = parent
        self.builder = gtk.Builder()
        self.builder.add_from_file(UI_PREFS)
        self.dialog = self.builder.get_object('prefsDialog')

        self.__connectSignals()

    def __connectSignals(self):
        self.builder.connect_signals({
            'on_prefsDialog_response': self.handleResponse
        })

    def handleResponse(self, dialog, response_id):
        if response_id == gtk.RESPONSE_CLOSE or response_id == gtk.RESPONSE_DELETE_EVENT:
            self.hide()

    def show(self):
        self.dialog.run()

    def hide(self):
        self.dialog.hide()

class SignInDialog(object):
    def __init__(self, parent):
        self.parent = parent
        self.builder = gtk.Builder()
        self.builder.add_from_file(UI_SIGNIN)
        self.dialog = self.builder.get_object('signInDialog')

    def show(self):
        self.dialog.run()
