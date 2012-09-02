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

import serial, sys, socket
import os
import shutil, time

MINDSET_SYNC = 170
MINDSET_PACKET_LENGTH = 32
MINDSET_POWER_BANDS = 8

class Monitor ():


	def Parse (self, package):
		#print package
#		print "PACKAGE: ", (len(package))
		for i in range(MINDSET_PACKET_LENGTH):
			print "PACKAGE len: ", len(package)
			print  package
#, packet[i]
#			switch (packet[i]) {
#				case 2:
#				        signal = packet[++i];
#				        break;
#				case 4:
#				        attention = packet[++i];
#				        break;
#				case 5:
#				        meditation = packet[++i];
#				        break;
#				case 131:
#				        eeg_length = packet[++i];
#				        for(j = 0; j < MINDSET_POWER_BANDS; j++) {
#				                eeg_power[j] = ((unsigned long)packet[++i] << 16) | ((unsigned long)packet[++i] << 8) | (unsigned long)packet[++i];
#				        }
#				        break;
#				default:
#				       	 printf("huh what %02X\n", packet[i]);
#				        return;
		


	def connect(self, port):
		#Save a backup of last brain scan 
		if  os.path.isfile('samples/overmind.csv'):
			filedate=time.strftime("%Y%m%d-%H%M%S",time.localtime(os.path.getctime('samples/overmind.csv')))
			shutil.copy2('samples/overmind.csv', ('samples/overmind-%s.csv' % filedate))

		#Kill all monitors and launch again
		os.system ("killall -9 overmind_monitor.sh")
		os.system ("./overmind_monitor.sh %s &" %port)
		
	def connectDev(self, port):
		s = serial.Serial()
		s.port = port
		s.baudrate = 9600
		s.parity = 'N'
		s.writeTimeout = 0
		s.open()

		while 1:
		     try:
			byte = s.readline(4)
			if byte is  255:
				print "return"
				return 1; 
			if byte is not MINDSET_SYNC:
				print "No sync-1:  " , byte
				continue

			byte = s.readline(4)
			if byte is not MINDSET_SYNC:
				print "No sync-2"
				continue
			sread = s.readline(MINDSET_PACKET_LENGTH)
			if len(sread) is not MINDSET_PACKET_LENGTH:
				print "no lenght"
				continue

			self.Parse(sread)

		     except:
			 print "connection at %s lost" % s.port
			 break


