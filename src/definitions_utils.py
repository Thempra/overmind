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

import os

# Definitions
# Symbols
symbols = ['-','--','-.',':','.',',','o','^','v','<','>','s','+','x','D','d','1','2','3','4','h','H','p']
# Symbols + line
lps = [k+'-' for k in [',','.','o','^','v','<','>','s','+','x','D','d','1','2','3','4','h','H','p']]
# Colors
colors= ['b','g','r','c','m','y','k','w']
colorsfull= ['blue','green','red','cyan','magenta','yellow','k','white']

# Signals
signals= ['signal strength', 'attention', 'meditation', 'delta', 'theta', 'low alpha', 'high alpha', 'low beta', 'high beta', 'low gamma', 'high gamma']

#Devices
devices= ['/dev/rfcomm0','/dev/rfcomm1','/dev/rfcomm2','/dev/ttyUSB0','/dev/ttyUSB1','/dev/ttyUSB2','/dev/ttyS0','/dev/ttyS1']

# Utils
def which(program):
    def is_exe(fpath):
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None
