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
import csv
import os 
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from dialogs import SettingsDialog

from definitions_utils import symbols, colors, colorsfull, signals

from monitor import *




class ApplicationWindow(QtGui.QMainWindow):
    """
    This is the main application window
    """

    def __init__(self, filename):

	self.canredraw = True
	os.system ("killall -9 overmind_monitor.sh")
        self.setting_dialog = SettingsDialog()
	self.config = self.setting_dialog.loadSettings()


        self.mainWindow()
        
        self.filename = filename
        
        #if len(self.filename) != 0:
        #	self.filePlot()

        self.check_boxes_signals = []
	self.createToolbar()
	self.leftMenu()

        self.show()
            
 

    


    def _readCSV(self, filename):
        """
        Given a file read the CSV and parse the fields using the default CSV dialect.
        The CSV format must respect the actual restrictions.
        """
        
        def verifyColumnNames(temp_row):
            for i in range(1,len(temp_row)):
                if temp_row[i-1].strip() != "y" + `i`:
                    return False
            return True
            
        
        values_read = csv.reader(open(filename))

        # Read the data from a CSV file (with previous know format)
        self.title = ""
        self.location_code = -1
        
        self.legend_names = []
        self.list_colors_plot = []
        self.list_symbols_plot = []
        self.list_signal_is_to_plot = []
        self.list_line_width = []
        
        self.x_values = []
        self.y_values = []
        self.x_label = ""
        self.y_label = ""
        temp_row = values_read.next()
        if temp_row[0].strip() == "x" and verifyColumnNames(temp_row[1:]):
            # For the case of a column CSV
            temp_row = values_read.next()
            self.x_label = temp_row[0].strip()
            self.y_label = temp_row[1].strip()
            
            self.y_values = [[] for i in range(len(temp_row)-1)]
            for temp_row in values_read:
                self.x_values.append(temp_row[0].strip())
                for i in range(1, len(temp_row)):
                    self.y_values[i-1].append(temp_row[i].strip())
                    
            for i in range(1, len(temp_row)):
                # Fill the line names for the legend
                self.legend_names.append("Line " + `i`)
		
		#print colors[i%8-1]
                # Default color and style
                self.list_colors_plot.append(colors[i%8-1])
                self.list_symbols_plot.append(symbols[0])
                # By default plot the signal and default line width
                self.list_signal_is_to_plot.append(True)
                self.list_line_width.append(0.75)
        else:
            # The CSV is organized by rows
            for i in temp_row[2:]:
                self.x_values.append(i.strip())
            self.x_label = temp_row[1]
            
            i = 1
            for temp_row in values_read:
                if i == 1:
                    self.y_label = temp_row[1]
                    
                if temp_row[0].strip() == "y" + `i`:
                    self.legend_names.append("Line " + `i`)
                    y_temp = []
                    for j in temp_row[2:]:
                        y_temp.append(j.strip())
                        
                    self.y_values.append(y_temp)
                    i+=1
                    
                    # Default color and style
                    self.list_colors_plot.append(colors[i-1])
                    self.list_symbols_plot.append(symbols[0])
                    # By default plot the signal and default line width
                    self.list_signal_is_to_plot.append(True)
                    self.list_line_width.append(0.75)
                else:                        
                    QtGui.QMessageBox.critical(None, "Data Error", "Incorrect data format.")
                    exit(-1)
        

    def _reDrawPlot(self):
        """
        Plot the signals after changes in the options
        """
        self.fig.clf()
        self.ax = self.fig.add_subplot(111)
        for i in range(0, len(self.y_values)):
            if self.list_signal_is_to_plot[i]:
                self.ax.plot(self.x_values, self.y_values[i], str(self.list_colors_plot[i] + self.list_symbols_plot[i]), linewidth=self.list_line_width[i])
        self.ax.set_xlabel(self.x_label)
        self.ax.set_ylabel(self.y_label)
        self.ax.set_title(self.title)
        if self.location_code != -1:
            # Determine which signals to put in legend
            curr_legend_names = []
            for i in range(0, len(self.list_signal_is_to_plot)):
                if self.list_signal_is_to_plot[i]:
                    curr_legend_names.append(self.legend_names[i])
            self.ax.legend(curr_legend_names, self.location_code)
            #self.ax.legend(self.legend_names, self.location_code)
        self.canvas.draw()


	
            

    def mainWindow(self):
        """
        Define the widgets of the main window
        """
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("Data Plot")

        # Create the menus
        self.file_menu = QtGui.QMenu('&File', self)
        self.file_menu.addAction('&Plot', self.filePlot,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_P)
	self.file_menu.addAction('&Refresh', self.redrawfilePlot,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_R)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)
        

	
	self.tools_menu = QtGui.QMenu('&Tools', self)
        self.tools_menu.addAction('&Disable all signals', self.uncheckAllSignals,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_D)

        self.tools_menu.addAction('&Enable all signals', self.checkAllSignals,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_E)
        self.tools_menu.addAction('&Settings', self.configureSetting,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_S)

      

        self.menuBar().addMenu(self.tools_menu)
    
        self.help_menu = QtGui.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)

        self.statusBar().showMessage("Ready", 2000)

    def createToolbar(self):
        """Create Toolbar"""
	self.conectAction = QtGui.QAction(QtGui.QIcon('img/statusOff.png'), 'Conect', self)
        self.conectAction.setShortcut('Ctrl+B')
        self.conectAction.triggered.connect(self.conectDevice)

	openAction = QtGui.QAction(QtGui.QIcon('img/open24.png'), 'Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.triggered.connect(self.filePlot)

	refreshAction = QtGui.QAction(QtGui.QIcon('img/refresh24.png'), 'Refresh', self)
        refreshAction.setShortcut('Ctrl+R')
        refreshAction.triggered.connect(self.redrawfilePlot)

	checkAction = QtGui.QAction(QtGui.QIcon('img/check.gif'), 'Check All', self)
        checkAction.setShortcut('Ctrl+A')
        checkAction.triggered.connect(self.checkAllSignals)

	uncheckAction = QtGui.QAction(QtGui.QIcon('img/uncheck.gif'), 'Uncheck All', self)
        uncheckAction.setShortcut('Ctrl+U')
        uncheckAction.triggered.connect(self.uncheckAllSignals)

        exitAction = QtGui.QAction(QtGui.QIcon('img/exit24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        #exitAction.triggered.connect(QtGui.qApp.quit)
        exitAction.triggered.connect(self.fileQuit)


	self.toolbar = self.addToolBar('Conect Bluethoot')
        self.toolbar.addAction(self.conectAction)

        self.toolbar = self.addToolBar('Open')
        self.toolbar.addAction(openAction)
        
        self.toolbar = self.addToolBar('Refresh')
        self.toolbar.addAction(refreshAction)

	
	self.toolbar = self.addToolBar('Check All')
        self.toolbar.addAction(checkAction)

	self.toolbar = self.addToolBar('Uncheck All')
        self.toolbar.addAction(uncheckAction)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)
        
        self.setGeometry(0, 0, 800, 800)
        self.setWindowTitle('Toolbar')


    def leftMenu(self):
        """Left Menu with all signal"""
	dock1 = QtGui.QDockWidget('Signals', self)   
        dock1.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea) 
	dock1.setMaximumWidth(140)
        self.widget1 = QtGui.QWidget(parent=dock1)   

        dock1.setWidget(self.widget1)	 

        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock1)   

	#Print once to get all signals to read their names
	self.redrawfilePlot()

	#Fill the names
	layout = QtGui.QVBoxLayout(self)        

        for i in range(0, len(self.list_signal_is_to_plot)):
            layout_signal_plot = QtGui.QHBoxLayout()
            signal_label = QtGui.QLabel()
	    signal_label.setText(signals[i])
	    signal_label.setStyleSheet("color:%s" % (colorsfull[i%8]))
            temp_check_box = QtGui.QCheckBox()
            temp_check_box.setChecked(self.list_signal_is_to_plot[i])
            self.check_boxes_signals.append(temp_check_box)
            
            # Horizontal organization of the signal name and checkbox
            layout_signal_plot.addWidget(signal_label)
            layout_signal_plot.addWidget(self.check_boxes_signals[i])
            
            # Vertical organization of all signal names
            layout.addLayout(layout_signal_plot)

	self.widget1.setLayout(layout) 

    def checkAllSignals(self):
	"""Check all signal from left panel"""
	for i in self.check_boxes_signals:
      		i.setChecked(True)
	

    def uncheckAllSignals(self):
	"""Uncheck all signal from left panel"""
	for i in self.check_boxes_signals:
      		i.setChecked(False)
	
    def conectDevice(self):
	""" Conect to bluetooth device """
	print "Conecting..."
	#os.system("/usr/bin/rfcomm connect 0 ")
	#self.conectAction = QtGui.QAction(QtGui.QIcon('img/statusConect.png'), 'Conect', self)
	mon = Monitor()
	mon.connect(self.config.get('Hardware', 'port'))


    def fileQuit(self):
        """Quit the program"""
	os.system ("killall -9 overmind_monitor.sh")
        self.close()
        
    def configureSetting(self):	
        """
        Change the setting, ports, devices, ...
        """
	self.canredraw = False

        print  self.setting_dialog.run()
	self.canredraw = True
	
       
            
    def filePlot(self):
        """
        Using a path provided by the command line or a filename chosed using the GUI,
        plot the data using matplotlib 
        """
        if len(self.filename) == 0:
            self.filename = QtGui.QFileDialog.getOpenFileName(None, \
                    "Open Data File (csv)", ".", "*.csv")
        
        self._readCSV(self.filename)
        
        self.main_widget = QtGui.QWidget(self)
        
        #fig = Figure(figsize=(5,4), dpi=100)
        self.resize(500, 500)

        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        for i in range(0, len(self.y_values)):
            self.ax.plot(self.x_values, self.y_values[i], linewidth=self.list_line_width[i])
        self.ax.set_xlabel(self.x_label)
        self.ax.set_ylabel(self.y_label)
        self.ax.set_title(self.title)

        self.canvas = FigureCanvas(self.fig)  # A Qt Drawing area
      
        l = QtGui.QVBoxLayout(self.main_widget)
        l.addWidget(self.canvas)
      
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        self.filename = ""
    
        
    def redrawfilePlot(self):
        """
        Using a path provided by the command line or a filename chosed using the GUI,
        plot the data using matplotlib 
        """
        if self.canredraw:
		self._readCSV("samples/overmind.csv")
		
		self.main_widget = QtGui.QWidget(self)
		
		#fig = Figure(figsize=(5,4), dpi=100)
		self.resize(1020, 700)
		self.fig = Figure()
		self.ax = self.fig.add_subplot(111)
		for i in range(0, len(self.y_values)):
		    self.ax.plot(self.x_values, self.y_values[i], linewidth=self.list_line_width[i])
		self.ax.set_xlabel(self.x_label)
		self.ax.set_ylabel(self.y_label)
		self.ax.set_title(self.title)

		self.canvas = FigureCanvas(self.fig)  # A Qt Drawing area
		#toolbar = NavigationToolbar(self.canvas, self)

		l = QtGui.QVBoxLayout(self.main_widget)
		l.addWidget(self.canvas)
		#l.addWidget(toolbar)

		self.main_widget.setFocus()
		self.setCentralWidget(self.main_widget)
		self.filename = ""
	     

		self.updateChooseSignalsPlot()

 

    def updateChooseSignalsPlot(self):
        """
        Choose the signals that are going to be in the plot
        """
        #choose_signals_to_plot = ChooseSignalsPlot(self.list_signal_is_to_plot)
        #new_signals_to_plot = choose_signals_to_plot.run()
	#if self.exec_():
        signals_to_plot = []
	if len(self.check_boxes_signals) > 0:
	        for i in self.check_boxes_signals:
        		signals_to_plot.append(i.isChecked())
            
        
        
        	if signals_to_plot != None:
        	    self.list_signal_is_to_plot = signals_to_plot
        	    self._reDrawPlot()        

    def about(self):
        """Program about"""
	self.canredraw = False
        QtGui.QMessageBox.about(self, "About OverMind", "OverMind 0.1 Alpha version\n\n   Reading and processing your brain waves at lowcost mode.\n\nAuthors: Jose Carlos Temprado Morales <thempra@thempra.net>")
	self.canredraw = True
