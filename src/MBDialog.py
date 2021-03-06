#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
#
# X Audio Copy - GTK and GNOME application for ripping CD-Audio and encoding in lossy audio format.
# Copyright 2010 - 2013 Giorgio Franceschi
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

try:
	import pygtk
	pygtk.require("2.0")
except:
	print("PyGTK not available")
	sys.exit(1)
try:
	import gtk
	import gobject
except:
	print("GTK not available")
	sys.exit(1)


### Finestra di dialogo per la selezione dei CD da MusicBrainz ###
class MBDialog:

	# Costruttore della classe
	def __init__(self, main_window, MB_releases):

		self.main_window = main_window
		# Inizilizza la variabile
		self.selected_cd = None

		# Finestra di dialogo
		self.dlg = gtk.Dialog("Select CD from MusicBrainz DB...", self.main_window,
					gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)
		self.dlg.set_default_size(610, 410)
		self.dlg.set_border_width(5)
		self.dlg.vbox.set_homogeneous(False)

		scroll = gtk.ScrolledWindow()
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.dlg.vbox.pack_start(scroll, expand=True)
		scroll.show()

		# Etichetta
		self.labelDiscID = gtk.Label("""<span>{0}<i>{1}</i></span>""".format("Several exact matches found. Please select your CD.\nMusicBrainz Disc ID: ", MB_releases[0]["disc-id"]))
		self.labelDiscID.set_alignment(0, 0.5)
		self.labelDiscID.set_padding(10, 10)
		self.labelDiscID.set_use_markup(True)
		self.dlg.vbox.pack_start(self.labelDiscID, expand=False)
		self.labelDiscID.show()

		# TreeView
		self.tvSelectCD = gtk.TreeView()
		self.tvSelectCD.connect("row-activated", self.on_CD_selected)
		scroll.add(self.tvSelectCD)
		self.tvSelectCD.show()

		# Pulsante OK
		self.cmdOKCDDB = gtk.Button(label="_Ok", use_underline=True)
		self.cmdOKCDDB.connect("clicked", self.on_CD_selected)
		self.dlg.add_action_widget(self.cmdOKCDDB, 1)
		self.cmdOKCDDB.show()

		# Pulsante Reject
		self.cmdReject = gtk.Button(label="_Reject", use_underline=True)
		self.cmdReject.connect("clicked", self.on_Reject)
		self.dlg.add_action_widget(self.cmdReject, 1)
		self.cmdReject.show()

		# Pulsante Calcel
		self.cmdCancel = gtk.Button(label="_Cancel", use_underline=True)
		self.cmdCancel.connect("clicked", self.on_Cancel)
		self.dlg.add_action_widget(self.cmdCancel, 1)
		self.cmdCancel.show()

		# Colonne del TreeView
		cell = gtk.CellRendererText()
		column0 = gtk.TreeViewColumn("Artist", cell, text=0)
		column1 = gtk.TreeViewColumn("Title", cell, text=1)
		column2 = gtk.TreeViewColumn("Catalog", cell, text=2)
		column3 = gtk.TreeViewColumn("Date", cell, text=3)
		column4 = gtk.TreeViewColumn("Country", cell, text=4)
		column5 = gtk.TreeViewColumn("ID", cell, text=5)
		self.tvSelectCD.append_column(column0)
		self.tvSelectCD.append_column(column1)
		self.tvSelectCD.append_column(column2)
		self.tvSelectCD.append_column(column3)
		self.tvSelectCD.append_column(column4)
		self.tvSelectCD.append_column(column5)

		# Selezione
		self.selectCD = self.tvSelectCD.get_selection()

		# Crea il modello ListStore con il contenuto della tabella
		self.cdList = gtk.ListStore(str, str, str, str, str, str)
		# Lo collega al TreeView
		self.tvSelectCD.set_model(self.cdList)

		for cd in MB_releases:
			# Popola di dati le righe
			self.cdList.append([cd["artist"], 
					cd["album-title"],
					cd["catalog"][0]["label"] + " " +cd["catalog"][0]["catalog-number"],
					cd["date"],
					cd["country"],
					cd["album-id"]])
		# Attiva e visualizza la finestra di dialogo
		self.dlg.run()

	def on_CD_selected(self, *args):

		model, row_iter = self.selectCD.get_selected()
		print "model: ", model
		print "row: ", row_iter
		if not row_iter:
			row_iter = self.cdList.get_iter_root()
		self.selected_cd = self.cdList.get_string_from_iter(row_iter)
		print self.selected_cd

		self.dlg.destroy()

	def on_Reject(self, *args):
		self.selected_cd = "reject"
		self.dlg.destroy()

	def on_Cancel(self, *args):
		self.selected_cd = None
		self.dlg.destroy()
