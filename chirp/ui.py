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

import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import gobject
import pango

from pkg_resources import resource_filename
GLADE_MAIN = resource_filename(__name__, 'glade/chirp.glade')
GLADE_PREFS = resource_filename(__name__, 'glade/prefs.glade')
GLADE_SIGNIN = resource_filename(__name__, 'glade/signin.glade')

class MainWindow(object):
    def __init__(self, parent):
        self.parent = parent

        self.xml = gtk.glade.XML(GLADE_MAIN, 'mainWindow')
        self.window = self.xml.get_widget('mainWindow')

        self.__initTreeView()
        self.__initAccelerators()

        self.connectEvents()

    def __initTreeView(cls):
        treeview = cls.xml.get_widget('mainTreeView')
        
        # avatar, name, status
        cls.liststore = gtk.ListStore(gobject.TYPE_OBJECT, gobject.TYPE_STRING, gobject.TYPE_STRING)
        treeview.set_model(cls.liststore)

        # make cellrenderers
        avatar_cr = gtk.CellRendererPixbuf()
        user_cr = gtk.CellRendererText()
        status_cr = gtk.CellRendererText()
        
        # set renderer properties
        status_cr.set_property('ellipsize', pango.ELLIPSIZE_END)

        # make columns
        user_column = gtk.TreeViewColumn('User', None)
        status_column = gtk.TreeViewColumn('Status', status_cr, text=2)
       
        # add renderers to user column
        user_column.pack_start(avatar_cr, False)
        user_column.pack_start(user_cr, True)
        user_column.add_attribute(avatar_cr, 'pixbuf', 0)
        user_column.add_attribute(user_cr, 'text', 1)
        
        # add cols to treeview
        treeview.append_column(user_column)
        treeview.append_column(status_column)

    def __initAccelerators(cls):
        """accels = gtk.AccelGroup()
        accels.connect_group(gtk.gdk.keyval_from_name('f5'), None, gtk.ACCEL_VISIBLE, self.refresh) # f5
        self.window.add_accel_group(accels)"""
        pass

    def connectEvents(cls):
        events = {
            'on_mainWindow_delete_event': cls.parent.hide,
            'on_updateButton_clicked': cls.parent.refresh
            }
        cls.xml.signal_autoconnect(events)

    def addTweet(cls, tweet):
        cls.liststore.append([None, tweet.user.screen_name, tweet.text])

    def clearTweets(cls):
        cls.liststore.clear()

    def show(cls, widget=None, event=None):
        cls.window.show()

    def hide(cls, widget=None, event=None):
        cls.window.hide()

    def toggleStatusbar(cls, widget=None, event=None):
        statusbar = cls.xml.get_widget('statusbar')
        checkbox = cls.xml.get_widget('menuitemStatusbar')
        if checkbox.active == False:
            statusbar.hide()
        else:
            statusbar.show()

class PreferencesDialog(object):
    def __init__(self, parent):
        self.parent = parent
        self.xml = gtk.glade.XML(GLADE_PREFS, 'prefsDialog')
        self.dialog = self.xml.get_widget('prefsDialog')

    def run(cls):
        self.dialog.run()
