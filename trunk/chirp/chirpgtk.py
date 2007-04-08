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

try:
	import pygtk
	pygtk.require('2.0')
	import gtk
	import gtk.glade
except:
	print 'You need to have GTK+ 2.x and PyGTK 2.x installed!'
	sys.exit(1)

from pkg_resources import resource_filename

GLADE_MAIN = resource_filename(__name__, 'glade/chirp.glade')
GLADE_PREFS = resource_filename(__name__, 'glade/prefs.glade')
GLADE_SIGNIN = resource_filename(__name__, 'glade/signin.glade')

class ChirpGTK:
	def __init__(self):
		self.mainTree = gtk.glade.XML(GLADE_MAIN, 'mainWindow')

		self.mainWindow = self.mainTree.get_widget('mainWindow')
		self.updateEntry = self.mainTree.get_widget('updateEntry')
		
		mainEvents = {
			'on_mainWindow_destroy': gtk.main_quit
			}
		self.mainTree.signal_autoconnect(mainEvents)

		"""# File menu
			'on_menuitemSignIn_activate': pass,
			'on_menuitemQuit_activate': pass,
			# Edit menu
			'on_menuitemPreferences_activate': pass,
			# View menu
			'on_menuItemStatusbar_toggled': pass,
			'on_menuItemRefresh_activate': pass,
			# Go menu
			'on_menuItemProfile_activate': pass,
			'on_menuItemFriends_activate': pass,
			'on_menuItemPublic_activate': pass,
			
			'on_updateEntry_changed': pass,
			'on_updateButton_activate': pass,
		"""
			
		gtk.main()
