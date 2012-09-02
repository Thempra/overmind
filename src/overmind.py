"""
    Copyright (c) 2012 Jose Carlos Temprado <thempra@thempra.net>
     
    Based on plotalot by Jose Roquette <josertt@gmail.com>
     
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
import sys
from application_window import ApplicationWindow

from matplotlib import rc

from definitions_utils import which
from monitor import *

if __name__ == "__main__":

    if len(sys.argv)>1:
	for arg in sys.argv:
		#Params from command line
		if arg == '-monitor' or arg == '-m':
			print "Monitor section, under development. Please use overmind_monitor"
			mon = Monitor()
			mon.connect('/dev/rfcomm0')
		if arg == '-monitordev' or arg == '-md':
			print "Monitor section, under development. Please use overmind_monitor"
			mon = Monitor()
			mon.connectDev('/dev/rfcomm0')
		if arg == '-V':
			print "Theeeg 0.1"
    else:

	    qApp = QtGui.QApplication(sys.argv)
	    
	    # Determine if we can use Latex or not for text
	    if which('dvipng') != None:
		#rc('text', usetex=True)
		#rc('font', family='serif')
		rc('axes', labelsize=10)
		rc('font', size=10)
		rc('legend', fontsize=10)
		rc('xtick', labelsize=8)
		rc('ytick', labelsize=8) 
		rc('text', usetex=True)
	    else:
		QtGui.QMessageBox.warning(None, "TeX support disabled", "Missing dvipng")

	    if len(sys.argv) < 2:
		filename = ""
	    elif len(sys.argv) == 2:
		filename = sys.argv[1]
	    else:
		QtGui.QMessageBox.critical(None, "Missing File", "The file to parse was not provided.")
		exit(-1)

	    aw = ApplicationWindow(filename)
	    aw.setWindowTitle("OverMind 0.1")
	    aw.show()

	    timer = QtCore.QTimer()
	    timer.timeout.connect(aw.redrawfilePlot)
	    timer.start(500)
	   

	    sys.exit(qApp.exec_())

