#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2020 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
import time
from gnuradio import gr
memory=[]
class phase_offset(gr.sync_block):
    """
    docstring for block phase_offset
    """
    def __init__(self):
        gr.sync_block.__init__(self,
    	    name="diyblk",
            in_sig=[numpy.byte],
            out_sig=[numpy.byte])
    def work(self, input_items, output_items):
        ind=input_items[0]
	#print(numpy.array(input_items).shape,len(ind))
	global memory
	max_packet=16
	packets=[]
	cnt=0	
	dpackets=[]
	default=130
	for cnt in range(len(ind)):
		if ind[cnt] > 1 and len(packets)<4:
		    packets.append(ind[cnt+2:cnt+(max_packet)])
	for packet in packets:
	    flag=0
	    temp = packet[::2]
	    tempchang=''.join(str(i) for i in temp)
	    if tempchang !='':
		if len(tempchang)==7:
			for c in tempchang:
				if c=='2' or c=='3':
					flag=1
			if flag==0:
				dpackets.append(int(tempchang,2))
	#dpackets=numpy.tile(numpy.array(dpackets),int(len(ind)/len(dpackets))+1)
	#dpackets1=dpackets[len(ind)]
	if len(dpackets)==0:
		print('found nothing')
		output_items[0][:]=default
	else:
		if len(dpackets)>3:
			print('The first four nums %s, total num=%d' %(dpackets[0:4],len(dpackets)))
			print('memory',memory)
		if len(memory)==0:
			memory.append(dpackets[0])
			output_items[0][:]=dpackets[0]
		elif len(memory)==1:
			memory.append(dpackets[0])
			output_items[0][:]=memory[0]
		elif len(memory)==2 and memory[0]==memory[1]:
			output_items[0][:]=memory[0]
			memory[0]=memory[1]
			memory[1]=dpackets[0]
		elif len(memory)==2 and memory[0]!=memory[1]:
			output_items[0][:]=dpackets[0]
			memory[0]=memory[1]
			memory[1]=dpackets[0]
	print('output',output_items[0][0])
	#logic:
	#a->a, b->b, c->c
	#a-a->a, a-b->a, a-c->a
	#ab-a->a,ab-b>b ab-c->c
	#00-0->0, 00-1->0, 01-0->0, 01-1->1
	#11-0->1, 11-1->1, 10-0->0, 10-1->1
        return len(output_items[0])
	
