#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 13:46:56 2019

@author: ocan
"""

import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk,GLib,Gdk
import time
import datetime
import os
import csv


				 
software_main_list = [] #create a list for the devices on the main list#
history_list = [] ##create history data
unselect_model = []	

## example list of devices ##
		
software_list1 = [["Firefox", 1,  "C++", 100,  "port2",False],
		 ["Eclipse", 2, "Java" , 100,  "port3",False],
		 ["Pitivi", 3, "Python", 100,  "port5",False],
		 ["Netbeans", 4, "Java", 100,  "port27",False],
		 ["Chrome", 5, "C++", 100,  "port240",False],
		 ["Filezilla", 6, "C++", 100,  "port60",False],
		 ["Bazaar", 7, "Python", 100,  "port18",False],
		 ["Git", 8, "C", 100,  "port5",False],
		 ["Linux Kernel", 9, "C", 100,  "port8",False],
		 ["GCC", 10, "C", 100,  "port90",False],
		 ["Frostwire", 11, "Java", 100,  "port72",False]]

## 


main_Devices_2 = []


## create directory to safe all the data in ##

def create_project_dir(directory):
		if not os.path.exists(directory):
			print('Creating directory ' + directory )
			os.makedirs(directory)
	

## create file for the history and the main device (if not created) ##

def create_data_files(project_name):
	history = project_name + '/history.csv'
	main_devices = project_name + '/main_devices.csv'
	
	if not os.path.isfile(history):
		write_file(history, '')
	if not os.path.isfile(main_devices):
		write_file(main_devices, '')
	
	
	
## create a new file ##

def write_file(path, data):
	with open(path, 'a') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerow(data)
	csvFile.close()
	
	
	
## add data onto an existing file ##

def append_to_file(path, data):
	with open(path, 'a') as file:
		file.write(data + '\n')
		
## delete the contents of a file ##

def delete_file_contents(path):
	with open(path, 'w'):
		pass
	
## read a file and convert each line to set items ##

def file_to_set(file_name):
	results = set()
	with open(file_name, 'rt') as f:
		for line in f:
			results.add(line.replace('\n', ''))
	return results

## iterate thorugh a set, each item will be a new line in the file ##

def set_to_file(links, file):
	delete_file_contents(file)
	for link in sorted(links):
		append_to_file(file,link)
		
## write list from file ###

def file_to_list(path):
	with open(path, 'r') as f:
		reader = csv.reader(f, delimiter=',')
		your_list = list(reader)
		new_list=[]
		for row in your_list:
			new_list.append( [int(i) if i.isdigit() else i for i in row])
		#print(new_list)
	return new_list


directory = 'USLA' #file name
create_project_dir(directory) #create file directory
create_data_files(directory) create the csv file
HISTORY_FILE = directory + '/history.csv' ## history file
MAIN_DEVICES_FILE = directory + '/main_devices.csv' ##main devices file

## main function ##

class MyWindow(Gtk.Window):

	def __init__(self):
		## setup main window ##

		Gtk.Window.__init__(self, title="USLA")
		self.set_size_request(1024,600) ## window size ##
		self.set_border_width(10)
		
		
    


		################################
		#### CSS design for the Tab ####
		################################

		
		cssprovider = Gtk.CssProvider()
		css = b"""
.myNotebook{
    background-color: inherit;
}
.myNotebook tab {
	border-style: solid;
	border-color: transparent;
    border-width: 1px;
    background-color: transparent;
}
.myNotebook tab:active{
	border-color: #c0c0c0;
}

"""


		cssprovider.load_from_data(css)
		screen = Gdk.Screen.get_default()
		stylecontext = Gtk.StyleContext()
		stylecontext.add_provider_for_screen(screen, cssprovider,
                                             Gtk.STYLE_PROVIDER_PRIORITY_USER)
		
		
		## setup notebook ##

		self.notebook = Gtk.Notebook()
		context = self.notebook.get_style_context()
		context.add_class("myNotebook")
		
		self.add(self.notebook)
		
		
		## setup the first page ##

		self.page1 = Gtk.Box()
		#label first page
		label_page1 = Gtk.Label()
		label_page1.set_text ('Main')
		
		#add the label on page tab
		#self.notebook.append_page(self.page1, label_page1)
		
		### create vertical box for button ###

		vbox_btn = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

		## Add button ##

		self.add_btn = Gtk.Button(label="Add")
		self.add_btn.connect("clicked",self.add_page_redirect)
		vbox_btn.pack_start(self.add_btn, False, False, 3)

		## Setting button ##

		self.set_btn = Gtk.Button(label="Setting")
		self.set_btn.connect("clicked",self.set_page_redirect)
		vbox_btn.pack_start(self.set_btn, False, False, 3)

		## history button ##

		self.his_btn = Gtk.Button(label = "History")
		self.his_btn.connect("clicked", self.his_page_redirect)
		vbox_btn.pack_start(self.his_btn, False, False, 3)

		## logout button ##

		self.logout_btn = Gtk.Button(label = "Logout")
		self.logout_btn.connect("clicked", self.logout_sys)
		vbox_btn.pack_start(self.logout_btn, False, False, 3)
		
		## create main horizontal box ##
		
		hbox_main = Gtk.Box( spacing=6)
		
		## convert main device file to list ##

		software_main_list = file_to_list(MAIN_DEVICES_FILE)
		
		## create grid ##
		
		self.grid = Gtk.Grid()
		self.grid.set_column_homogeneous(True)
		self.grid.set_row_homogeneous(True)

		## create software main list ##

		self.software_main_liststore1 = Gtk.ListStore(str, int, str,int,str,bool)
		
		## if the list from the file empty skip ##

		if len(software_main_list) == 0 :
			pass
		else:
			for software_ref in software_main_list :
				self.software_main_liststore1.append(list(software_ref))
		
		## create the treeview ##
		
		
		self.treeview = Gtk.TreeView.new_with_model(self.software_main_liststore1)
		
		for i, column_title in enumerate(["Device Name","ID","Attr","Bat Level", "RSSI"]):
			renderer = Gtk.CellRendererText()
			column = Gtk.TreeViewColumn(column_title, renderer, text=i)
			self.treeview.append_column(column)
			
		
			
		self.scrolledwindow = Gtk.ScrolledWindow()
		self.scrolledwindow.set_hexpand(True)
		self.scrolledwindow.set_vexpand(True)
		
		self.grid.attach(self.scrolledwindow,0,0,8,10)
		
		
		## add the treeview to the window ##
		
			
		self.scrolledwindow.add(self.treeview)
		
		## add the button and the grid in the window ##		

		hbox_main.pack_start(self.grid, True, True, 3)
		hbox_main.pack_start(vbox_btn, False, False, 3)
		hbox_main.set_border_width(10)
		
		self.page1.add(hbox_main)
		
		## add the notebook to the window ##

		self.notebook.append_page(self.page1, label_page1)
		
		
		####################################
		  ########## ADD PAGE #############
		####################################
		
		
		#setup the add page ##

		self.page2 = Gtk.Box()
		label_page2 = Gtk.Label()
		label_page2.set_text ('Add Device')
		
		## treeview ##
		
		self.grid = Gtk.Grid()
		self.grid.set_column_homogeneous(True)
		self.grid.set_row_homogeneous(True)
		
		self.software_liststore1 = Gtk.ListStore(str, int, str,int,str,bool)
		
		## check all in main device list ##

		list1=[]
		list2=[]
		size_list =(sum(len(x) for x in software_main_list))
		print(size_list)
		if size_list > 0 :
			for i in range (len(software_list1)):
				list1.append(software_list1[i][1])
				for j in range(len(software_main_list)):
					list2.append(software_main_list[j][1])
			diff = (list(set(list1)-set(list2)))
			for k in range (len(software_list1)):
				if (software_list1[k][1]) not in diff:
					software_list1[k][5] = not software_list1[k][5]
				
		else:
			pass
			
			
		## add the device to the list ##
	
		for software_ref in software_list1 :
			self.software_liststore1.append(list(software_ref))
		
		
		self.treeview = Gtk.TreeView.new_with_model(self.software_liststore1)
		
		for i, column_title in enumerate(["Device Name","ID","Attr","Bat Level", "RSSI"]):
			renderer = Gtk.CellRendererText()
			column = Gtk.TreeViewColumn(column_title, renderer, text=i)
			self.treeview.append_column(column)
		
		renderer_toggle = Gtk.CellRendererToggle()
		renderer_toggle.connect("toggled",self.add_to_list,self.software_liststore1 )
		column_toggle = Gtk.TreeViewColumn("Toggle",renderer_toggle,active=5)
		self.treeview.append_column(column_toggle)
		print(len(self.software_liststore1))
		
		
			
		self.scrolledwindow = Gtk.ScrolledWindow()
		self.scrolledwindow.set_hexpand(True)
		self.scrolledwindow.set_vexpand(True)
		
		self.grid.attach(self.scrolledwindow,0,0,8,10)
	
		
			
		self.scrolledwindow.add(self.treeview)
		
		## end treeview ##
		
		
		#add the label on page tab
		#self.notebook.append_page(self.page1, label_page1)
		
		#create vertical box for button
		vbox_btn = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		#Refresh button
		self.refresh_btn = Gtk.Button(label="Refresh")
		self.refresh_btn.connect("clicked",self.refresh_device)
		vbox_btn.pack_start(self.refresh_btn, False, False, 3)
		#Add device button
		self.add_device_btn = Gtk.Button(label="Add Device")
		self.add_device_btn.connect("clicked",self.add_device,self.software_liststore1)
		print(main_Devices_2)
		vbox_btn.pack_start(self.add_device_btn, False, False, 3)
		#Back button
		self.main_btn = Gtk.Button(label = "Main")
		self.main_btn.connect("clicked", self.main_page_redirect)
		vbox_btn.pack_start(self.main_btn, False, False, 3)
		
		hbox_main = Gtk.Box( spacing=6)
		
		
		## set the table##
		
		
		
	
		
	
		hbox_main.pack_start(self.grid, True, True, 3)
		hbox_main.pack_start(vbox_btn, False, False, 3)
		hbox_main.set_border_width(10)
		
		self.page2.add(hbox_main)
		
		
		self.notebook.append_page(self.page2, label_page2)
		
		####################################
		  ########## SETTING PAGE #########
		####################################
		
		
		#setup the setting page
		
		
		self.page3 = Gtk.Box()
		label_page3 = Gtk.Label()
		label_page3.set_text ('Setting')
		main_id =[]
		
		country_store = Gtk.ListStore(int)
		
		size_list =(sum(len(x) for x in software_main_list))
		print(size_list)
		if size_list > 0 :
			for software_id in range (len(software_main_list)) :
				main_id.append(software_main_list[software_id][1])
				
				
		else:
			pass
		
		for id in (main_id):
			country_store.append([id])
				
				
		## combo list for device list ID ##

		country_combo = Gtk.ComboBox.new_with_model(country_store)
		country_combo.connect("changed", self.on_country_combo_changed)
		renderer_text = Gtk.CellRendererText()
		country_combo.pack_start(renderer_text, True)
		country_combo.add_attribute(renderer_text, "text", 0)
		
		vbox_entry = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		vbox_entry.set_border_width(10)
		hbox_entry1 = Gtk.Box(spacing=6)
		entry1 = Gtk.Entry()
		entry1.set_text("")
		entry1.connect("changed", self.entry_change)
		label_entry1 = Gtk.Label()
		label_entry1.set_text ('Test')
		hbox_entry1.pack_start(label_entry1,False,False,3)
		hbox_entry1.pack_start(entry1,True,True,3)
		
		
		hbox_entry2 = Gtk.Box(spacing=6)
		entry2 = Gtk.Entry()
		entry2.set_text("")
		entry2.connect("changed", self.entry_change)
		label_entry2 = Gtk.Label()
		label_entry2.set_text ('Test 2')
		hbox_entry2.pack_start(label_entry2,False,False,3)
		hbox_entry2.pack_start(entry2,True,True,3)
		
		vbox_entry.pack_start(country_combo, False, False, 0)
		vbox_entry.pack_start(hbox_entry1, False, False, 0)
		vbox_entry.pack_start(hbox_entry2, False, False, 0)
		
		vbox_btn = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		vbox_btn.set_border_width(10)
		#Refresh button
		self.refresh_btn = Gtk.Button(label="Update")
		self.refresh_btn.connect("clicked",self.update_set)
		vbox_btn.pack_start(self.refresh_btn, False, False, 3)
		#Back button
		self.main_btn = Gtk.Button(label = "Main")
		self.main_btn.connect("clicked", self.main_page_redirect)
		vbox_btn.pack_start(self.main_btn, False, False, 3)
		
		hbox_main = Gtk.Box( spacing=6)
		hbox_main.pack_start(vbox_entry,True,True,3)
		hbox_main.pack_start(vbox_btn,True,True,3)
		
		self.page3.add(hbox_main)
		self.notebook.append_page(self.page3, label_page3)
		
		
		
		####################################
		  ########## HISTORY PAGE #########
		####################################
		
		history_list = file_to_list(HISTORY_FILE)

		#setup the history page#

		self.page4 = Gtk.Box()
		label_page4 = Gtk.Label()
		label_page4.set_text ('History')
		
		
		#create vertical box for button#

		vbox_btn = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

		#Refresh button#

		self.refresh_btn = Gtk.Button(label="Refresh")
		self.refresh_btn.connect("clicked",self.refresh_history)
		vbox_btn.pack_start(self.refresh_btn, False, False, 3)

		#Add device button#

		self.add_history_btn = Gtk.Button(label="Add History")
		self.add_history_btn.connect("clicked",self.add_history)
		vbox_btn.pack_start(self.add_history_btn, False, False, 3)

		#Back button##

		self.main_btn = Gtk.Button(label = "Main")
		self.main_btn.connect("clicked", self.main_page_redirect)
		vbox_btn.pack_start(self.main_btn, False, False, 3)
		
		hbox_main = Gtk.Box( spacing=6)
		
		## start treeview ##
		
		self.grid = Gtk.Grid()
		self.grid.set_column_homogeneous(True)
		self.grid.set_row_homogeneous(True)
		
		
		self.history_liststore = Gtk.ListStore(str, str)
		
		if (len(history_list))==0 :
			pass
		else:
			for history_ref in history_list :
				self.history_liststore.append(list(history_ref))

		
		self.history_treeview = Gtk.TreeView.new_with_model(self.history_liststore)
		
		for i, column_title in enumerate(["Date","Event"]):
			renderer = Gtk.CellRendererText()
			column = Gtk.TreeViewColumn(column_title, renderer, text=i)
			column.set_sort_column_id(0)
			self.history_treeview.append_column(column)
		
		
		self.scrolledwindow = Gtk.ScrolledWindow()
		self.scrolledwindow.set_hexpand(True)
		self.scrolledwindow.set_vexpand(True)
		
		self.grid.attach(self.scrolledwindow,0,0,8,10)
			
		self.scrolledwindow.add(self.history_treeview)
		

		hbox_main.pack_start(self.grid, True, True, 3)
		hbox_main.pack_start(vbox_btn, False, False, 3)
		hbox_main.set_border_width(10)
		
		self.page4.add(hbox_main)
		
		self.notebook.append_page(self.page4, label_page4)

	## activate all button to redirect to the specific page ##
		
	def main_page_redirect(self,widget):
		self.notebook.set_current_page(0)
		
	def add_page_redirect(self,widget):
		self.notebook.set_current_page(1)
		
	def set_page_redirect(self,widget):
		self.notebook.set_current_page(2)
		
	def his_page_redirect(self,widget):
		self.notebook.set_current_page(3)
	
	## update device list ##
	
	def refresh_device(self):
		pass
	## update history list ##
	
	def refresh_history(self):
		pass

	## update the combo box list ##

	def update_set(self,widget):
		self.on_country_combo_changed
		
	def on_country_combo_changed(self, combo):
		tree_iter = combo.get_active_iter()
		if tree_iter is not None:
			model = combo.get_model()
			country = model[tree_iter][0]
			print("Selected: country=%s" % country)
		return country
			
	def entry_change(self, entry):
		tree_iter = entry.get_text()
		if tree_iter is not None:
			output = entry.get_text()
			print("Entered: %s" % entry.get_text())
		else:
			pass
		return output
	
	## add device to the main device list ##
			
	def add_device(self,widget,model):

		main_Devices_2 = []
		history_ram = []
		
		self.software_main_liststore1.clear()
		delete_file_contents(MAIN_DEVICES_FILE)
		for devices in range (len(model)):
			if model[devices][5] == True :
				main_Devices_2.append(model[devices][:]) 
			

		for main in range (len(main_Devices_2)):
			self.software_main_liststore1.append(main_Devices_2[main][:])
			write_file(MAIN_DEVICES_FILE,main_Devices_2[main][:])
		
		## add the list to temporary array ##

		history_ram.append([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"Updated Main Device List"])
		self.history_liststore.append(history_ram[0][:])
		write_file(HISTORY_FILE,history_ram[0][:])
		
	## add new history ##

	def add_history(self):
		pass
	## logout from the system ###
		
	def logout_sys(self,widget):
		pass
	
				
## run the main function ##	
		
win = MyWindow()

## add the close window button ##

win.connect("delete-event",Gtk.main_quit)

## display all ##

win.show_all()
Gtk.main()