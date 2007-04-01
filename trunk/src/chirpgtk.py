try:
	import pygtk
	pygtk.require('2.0')
	import gtk
	import gtk.glade
except:
	print 'You need to have GTK+ 2.x and PyGTK 2.x installed!'
	sys.exit(1)

"""try:
	import gtkspell
	HAS_GTKSPELL = True
except:
	HAS_GTKSPELL = False
"""

class ChirpGTK:
	def __init__(self):
		self.mainTree = gtk.glade.XML('chirp.glade', 'mainWindow')

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
			'on_menuItemTabs_toggled': pass,
			'on_menuItemStatusbar_toggled': pass,
			'on_menuItemRefresh_activate': pass,
			# Go menu
			'on_menuItemProfile_activate': pass,
			'on_menuItemFriends_activate': pass,
			'on_menuItemPublic_activate': pass,
			
			'on_updateEntry_changed': pass,
			'on_updateButton_activate': pass,
		"""
			
		#self.signInTree = gtk.glade.XML('chirp.glade', 'signInDialog')
		#self.signInDialog = self.signInTree.get_widget('signInDialog')
		#self.signInDialog.run()
		
		gtk.main()