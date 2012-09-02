"""
    Copyright (c) 2012 Jose Carlos Temprado <thempra@thempra.net>
         
    This file is part of OverMind.

    OverMind is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OverMind is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with OverMind.  If not, see <http://www.gnu.org/licenses/>.
"""

from PyQt4 import QtGui, QtCore
from definitions_utils import symbols, devices
import ConfigParser
import os.path

class SettingsDialog(QtGui.QDialog):

    def __init__(self):
	""" Change the setting, ports, devices, ..."""
        QtGui.QDialog.__init__(self)
        self.setWindowTitle("Settings")
	
        
        layout_dialog = QtGui.QVBoxLayout()
        
        # Place all the choices of devices for the current lines
        self.list_combo_devices = []
       

        
        layout_edit_props = QtGui.QHBoxLayout()
        line_label = QtGui.QLabel()
        line_label.setText('Device ')
            
        self.combo_devices = QtGui.QComboBox()
        self.combo_devices.insertItems(0, devices)
        #combo_devices.setCurrentIndex('Device')
        self.list_combo_devices.append(self.combo_devices)
           
            
        layout_edit_props.addWidget(line_label)
        layout_edit_props.addWidget(self.combo_devices)

            
        layout_dialog.addLayout(layout_edit_props)
            
        # Place the buttons
        buttons_layout = QtGui.QHBoxLayout()
        
	Search = QtGui.QPushButton()
        Search.setText("Search")
        self.connect(Search, QtCore.SIGNAL("clicked()"), self.search)

        OK = QtGui.QPushButton()
        OK.setText("OK")
        self.connect(OK, QtCore.SIGNAL("clicked()"), self.saveSettings)
        
        Cancel = QtGui.QPushButton()
        Cancel.setText("Cancel")
        self.connect(Cancel, QtCore.SIGNAL("clicked()"), self.reject)
        
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(Search)
        buttons_layout.addWidget(OK)
        buttons_layout.addWidget(Cancel)
        
        # Place the global layout
        layout_dialog.addLayout(buttons_layout)
        self.setLayout(layout_dialog)
        
        Cancel.setFocus()
        
        
    def run(self):
        if self.exec_() == True:
            return True
        else:
            return False


    def search(self):
	""" TO DO: """

	print "Searching ......"
	print "It needs to be developed."


    def loadSettings(self):

	self.config = ConfigParser.RawConfigParser()

	if not os.path.isfile('overmind.cfg'):
		self.saveSettings()

	
	self.config.read('overmind.cfg')

	if self.config.has_option('Hardware', 'port'):
		self.config.get('Hardware', 'port')
	else:
		if not self.config.has_section('Hardware'):
			self.config.add_section('Hardware')
		self.config.set('Hardware', 'port', '/dev/rfcomm0' ) # Default value

	return self.config


    def saveSettings(self):
	print "Save settings ...."
	if not self.config.has_section('Hardware'):
		self.config.add_section('Hardware')
		self.config.set('Hardware', 'port', '/dev/rfcomm0' ) # Default value
	else:
		self.config.set('Hardware', 'port', self.combo_devices.currentText() )


	with open('overmind.cfg', 'wb') as configfile:
	    self.config.write(configfile)

	return True

