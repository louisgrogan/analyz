from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as ScrolledText
from sklearn.linear_model import Ridge
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
import time
import pandas as pd
import xlrd
import tkinter.filedialog
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statistics
import scipy
from PIL import *
import pygame
from keras.models import Sequential
from keras.layers import Dense, LSTM
from sklearn.datasets import make_regression
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor

def read_recent_files():
	global recent_files_list_new
	recent_files_list = []
	recent_files_list_new = []
	with open('recentfiles.txt') as file:
		recent_file_length = 0
		for line in file:
			recent_file_length += 1
			recent_files_list.append(line[0:len(line)-1])
		print(recent_file_length)
		print(recent_files_list)
	
	if recent_file_length >= 5:
		for n in range(5):
			recent_files_list_new.append(recent_files_list[n])
	elif recent_file_length >= 1 and recent_file_length <= 4:
		for n in range(recent_file_length):
			recent_files_list_new.append(recent_files_list[n])
		while len(recent_files_list_new) != 5:
			recent_files_list_new.append('')
	else:
		recent_files_list_new = ['','','','','']
	print(recent_files_list_new)

def open_recent_files(filename):
	global dftextPad
	global df
	global file_path_display
	global file_path_label2
	global file_path_label1
	file_path_display = ""
	file = filename
	file_path_string = str(file)
	file_path_display = file_path_display + "'" + file_path_string + "'"
	file_path_label2.config(text=file_path_display, fg="black")
	file_path_label1.config(text="File Path:")
	print(file_path_display)
	df = pd.read_csv(file)
	print(df)
	edit_dftextPad("DF")

def append_recent_files(filename):
	global recent_files_list_new
	with open("recentfiles.txt", 'r+') as fp:
		lines = fp.readlines()
		lines.insert(0, (filename + "\n"))
		fp.seek(0)
		fp.writelines(lines)
	fp.close()
	read_recent_files()
	create_menubar(root)

def edit_dftextPad(data_type):
	global df
	global equation_str
	global dftextPad
	if data_type == "DF":
		dftextPad.config(state='normal')
		dftextPad.delete('1.0', END)
		dftextPad.insert('1.0', df.to_string(index = False))
		dftextPad.config(state='disabled')
	elif data_type == "Equation":
		dftextPad.config(state='normal')
		dftextPad.delete('1.0', END)
		dftextPad.insert('1.0', equation_str)
		dftextPad.config(state='disabled')

def create_csv_data():
	global df
	global file_path_display
	global file_path_label2
	global file_path_label1
	global dftextPad
	create_csv_window = Tk()
	create_csv_window.geometry("750x600")
	create_csv_window.title("Create CSV Data")
	create_csv_window.resizable(False, False)
	create_csv_window.configure(background="White")
	create_csv_window.focus_force()
	
	textPad=Text(create_csv_window, bd=3)
	textPad.pack(fill=X, expand = YES)
	
	def save_command():
		global df
		global file_path_display
		global file_path_label2
		global file_path_label1
		global dftextPad
		file_path_display = ""
		file = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=".csv")
		if file != None:
			data = textPad.get('1.0', END+'-1c')
			file.write(data)
			file_path_string = str(file)
			file_path_index1 = file_path_string.find('name')
			file_path_index2 = file_path_string.find('mode')
			file_path_string = file_path_string[(file_path_index1+5):(file_path_index2-1)]
			file_path_display = file_path_display + file_path_string
			file_path_label1.config(text="File Path:")
			file_path_label2.config(text=file_path_display, fg="black")
			print(str(file_path_display[1:len(file_path_display)-1]))
			create_csv_window.destroy()
			file.close()
			df = pd.read_csv(str(file_path_display[1:len(file_path_display)-1]))
			print(df)
			edit_dftextPad("DF")
			append_recent_files(str(file_path_display[1:len(file_path_display)-1]))
	
	submitButton = Button(create_csv_window, text="Save CSV Data", width=15, height=1, font=('Arial', 13), 					command=save_command)
	submitButton.place(relx=0.50, rely=0.92, anchor=CENTER)

def open_excel_command():
	global dftextPad
	global x1
	global df
	global file_path_display
	global file_path_label2
	global file_path_label1
	file_path_display = ""
	file = tkinter.filedialog.askopenfile(parent=root,mode='rb',title='Select a file')
	file_path_string = str(file)
	file_path_index = file_path_string.find('name')
	file_path_string = file_path_string[(file_path_index+5):len(file_path_string)-1]
	file_path_display = file_path_display + file_path_string
	file_path_label2.config(text=file_path_display, fg="black")
	file_path_label1.config(text="File Path:")
	print(file_path_display)
	df = pd.read_excel(open(file_path_display[1:len(file_path_display)-1],'rb'), sheetname='Sheet 1')
	print(df)
	edit_dftextPad("DF")
	append_recent_files(str(file_path_display[1:len(file_path_display)-1]))
	
def open_csv_command():
	global dftextPad
	global df
	global file_path_display
	global file_path_label2
	global file_path_label1
	file_path_display = ""
	file = tkinter.filedialog.askopenfile(parent=root,mode='rb',title='Select a file')
	file_path_string = str(file)
	file_path_index = file_path_string.find('name')
	file_path_string = file_path_string[(file_path_index+5):len(file_path_string)-1]
	file_path_display = file_path_display + file_path_string
	file_path_label2.config(text=file_path_display, fg="black")
	file_path_label1.config(text="File Path:")
	print(file_path_display)
	df = pd.read_csv(file)
	print(df)
	edit_dftextPad("DF")
	append_recent_files(str(file_path_display[1:len(file_path_display)-1]))

def open_equation_command():
	global equation_window
	global equation_str
	global equation_entry
	global file_path_display
	global file_path_label2
	global file_path_label1
	global df
	equation_str = ""
	equation_window = Tk()
	equation_window.geometry("400x200")
	equation_window.title("Enter Equation")
	equation_window.resizable(False, False)
	equation_window.configure(background="White")
	equation_window.focus_force()
	
	degree_label = Label(equation_window, text="Degree: ", width=9, height=2,
		              font=('Arial',11))
	degree_label.place(relx=0.17, rely=0.23, anchor=CENTER)
	
	degree_entry = Entry(equation_window, width=20)
	degree_entry.place(relx=0.51, rely=0.23, anchor=CENTER)
	
	equation_label = Label(equation_window, text="Equation: ", width=10, height=2,
		              font=('Arial',11))
	equation_label.place(relx=0.17, rely=0.51, anchor=CENTER)
	
	equation_entry = Entry(equation_window, text=equation_str, width=33, state=DISABLED)
	equation_entry.place(relx=0.64, rely=0.51, anchor=CENTER)

	def equation_confirm():
		global file_path_display
		global file_path_label2
		global file_path_label1
		global df
		global y_equation
		global equation_str
		file_path_display = str(equation_entry.get())
		file_path_label2.config(text=file_path_display, fg="black")
		file_path_label1.config(text="Equation:")
		df = ""
		y_equation = file_path_display[4:(len(file_path_display))]
		equation_str = file_path_display
		equation_window.destroy()
		print(equation_str)
		print(file_path_display)
		print(y_equation)
		edit_dftextPad("Equation")
	
	def degree_confirm():
		global equation_entry
		global equation_str
		global equation_confirm_button
		equation_str = "y = "
		equation_entry.config(state=NORMAL)
		degree = int(degree_entry.get())
		degree_count = degree
		for n in range(1, (degree+1)): 
			if degree_count == 1:
				equation_str = equation_str + "1*x +"
			else:
				equation_str = equation_str + "1*(x**" + str(degree_count) + ") + "
				degree_count -= 1
		
		equation_entry.delete(0, END)
		equation_entry.insert(END, equation_str)
		
		equation_confirm_button = Button(equation_window, text="Confirm", font = ("Arial", 11),
				width=4, height=1, bg="white", 
				activebackground="light grey", 
				bd="3", highlightbackground="black", 
				command = equation_confirm)
		equation_confirm_button.place(relx=0.50, rely=0.83, anchor=CENTER)
	
	degree_confirm_button = Button(equation_window, text="Go", font = ("Arial", 11),
				width=2, height=1, bg="white", 
				activebackground="light grey", 
				bd="3", highlightbackground="black", 
				command = degree_confirm)
	degree_confirm_button.place(relx=0.82, rely=0.23, anchor=CENTER)

#Defines configure_window(): function (Configures Window)

def configure_window(x, title_text):
	x.geometry("750x500")
	x.title(title_text)
	x.resizable(False, False)
	x.configure(background="White")
	x.focus_force()
	
def edit_db_launch():
	global dftextPad
	global edit_db_window
	global df
	global file_path_label1
	global file_path_label2
	
	if (file_path_label1.cget("text")) == "Equation:" or file_path_display == "" or 				file_path_label2.cget("text") == "Please import file data":
		file_path_label1.config(text="File Path:")
		file_path_label2.config(text="Please import file data", fg="red")
	else:
		edit_db_window = Tk()
		configure_window(edit_db_window, "Edit Data")
		textPad=ScrolledText.ScrolledText(edit_db_window, bd=3, height=18)
		textPad.pack(fill=X, expand = YES)
		dbFile = open(str(file_path_display[1:len(file_path_display)-1]), "r+")
		contents = dbFile.read()
		textPad.insert('1.0',contents)
		
		def edit_db():
			data = textPad.get('1.0', END+'-1c')
			dbFile.seek(0)
			dbFile.truncate()
			dbFile.write(data)
			edit_db_window.destroy()
			dbFile.close()
			df = pd.read_csv(str(file_path_display[1:len(file_path_display)-1]))
			print(df)
			root.destroy()
			tempfile = str(file_path_display[1:len(file_path_display)-1])
			root_launch()
			open_recent_files(tempfile)
			edit_dftextPad("DF")
			append_recent_files(str(file_path_display[1:len(file_path_display)-1]))
		
		def reset_textPad():
			textPad.delete('1.0', END)
			textPad.insert('1.0', contents)

		editdbLabel = Label(edit_db_window, text="Edit Data", width=17, height=2, font=('Arial', 13))
		editdbLabel.place(relx=0.5, rely=0.10, anchor=CENTER)
		submitButton = Button(edit_db_window, text="Submit", width=7, height=1, font=('Arial', 12), 
					command=edit_db)
		submitButton.place(relx=0.41, rely=0.90, anchor=CENTER)
		resetButton = Button(edit_db_window, text="Reset", width=7, height=1, font=('Arial', 12), 					command=reset_textPad)
		resetButton.place(relx=0.60, rely=0.90, anchor=CENTER)

def search_db_launch():
	global search_db_window
	global df
	global file_path_label1
	global file_path_label2
	global column_headings_list
	global querytextPad
	global filtered_df
	
	if (file_path_label1.cget("text")) == "Equation:" or file_path_display == "" or 				file_path_label2.cget("text") == "Please import file data":
		file_path_label1.config(text="File Path:")
		file_path_label2.config(text="Please import file data", fg="red")
	else:
		search_db_window = Tk()
		configure_window(search_db_window, "Search/Sort Data")
		column_headings_list = []
		for n in list(df.columns.values):
			column_headings_list.append(n)
		print(column_headings_list)
		filtered_df = pd.DataFrame(columns=column_headings_list)
		#vscrollbar = Scrollbar(search_db_window)
		#vscrollbar.pack(side = RIGHT, fill = Y)
		#hscrollbar = Scrollbar(search_db_window)
		#hscrollbar.pack(side = BOTTOM, fill = X)
		querytextPad=ScrolledText.ScrolledText(search_db_window, bd=3, height=10, font=('Arial', 14), 					state='disabled', wrap='none')
		querytextPad.pack(fill=X, expand = YES)
		findLabel = Label(search_db_window, text="Find", width=10, height=2, font=('Arial', 12))
		findLabel.place(relx=0.13, rely=0.09, anchor=CENTER)
		queryEntry = Entry(search_db_window, text="", width=14)
		queryEntry.place(relx=0.31, rely=0.09, anchor=CENTER)
		inLabel = Label(search_db_window, text="in", width=7, height=2, font=('Arial', 12))
		inLabel.place(relx=0.475, rely=0.09, anchor=CENTER)
		columnEntry = ttk.Combobox(search_db_window, state='readonly', width=10, text = "", 
				font = ('Arial', 12))
		columnEntry.place(relx=0.63, rely=0.09, anchor=CENTER)
		columnEntry.config(values = column_headings_list)
		
		sortLabel = Label(search_db_window, text="Sort", width=10, height=2, font=('Arial', 12))
		sortLabel.place(relx=0.13, rely=0.21, anchor=CENTER)
		sortcolumnEntry = ttk.Combobox(search_db_window, state='readonly', width=10, text = "", 
				font = ('Arial', 12))
		sortcolumnEntry.place(relx=0.31, rely=0.21, anchor=CENTER)
		sortcolumnEntry.config(values = column_headings_list)
		inLabel2 = Label(search_db_window, text="in", width=7, height=2, font=('Arial', 12))
		inLabel2.place(relx=0.475, rely=0.21, anchor=CENTER)
		sortorderEntry = ttk.Combobox(search_db_window, state='readonly', width=10, text = "", 
				font = ('Arial', 12))
		sortorderEntry.place(relx=0.63, rely=0.21, anchor=CENTER)
		sortorderEntry.config(values = ['Ascending Order', 'Descending Order'])
		
		def save_df_to_csv():
			save_df_to_csv_FilePath = tkinter.filedialog.asksaveasfile(mode='w', 									defaultextension=".csv")
			filtered_df.to_csv(save_df_to_csv_FilePath, index=False)
		
		save_df_to_csvButton = Button(search_db_window, text="Save Data to CSV", width=18, height=2, 
					font=('Arial', 12), command=save_df_to_csv)
		save_df_to_csvButton.place(relx=0.30, rely=0.925, anchor=CENTER)
		
		def print_querytextPad():
			print("Mip")
		
		print_querytextPad_Button = Button(search_db_window, text="Print", width=18, height=2, 
					font=('Arial', 12), command=print_querytextPad)
		print_querytextPad_Button.place(relx=0.70, rely=0.925, anchor=CENTER)
		
		def sort_db():
			global filtered_df
			sortcolumnvalue = str(sortcolumnEntry.get())
			sortordervalue = str(sortorderEntry.get())
			if sortordervalue == "Ascending Order":
				filtered_df.sort_values(by=[sortcolumnvalue], inplace=True)
			elif sortordervalue == "Descending Order":
				filtered_df.sort_values(by=[sortcolumnvalue], inplace=True, ascending=False)
			querytextPad.config(state='normal')
			querytextPad.delete('1.0', END)
			querytextPad.insert('1.0', filtered_df.to_string(index=False))
			print(filtered_df)
		
		sortButton = Button(search_db_window, text="Sort", width=12, height=2, font=('Arial', 12), 						command=sort_db)
		sortButton.place(relx=0.83, rely=0.21, anchor=CENTER)
		
		def search_db():
			global filtered_df
			querytextPad.config(state='normal')
			querytextPad.delete('1.0', END)
			search_word = str(queryEntry.get())
			column_value = str(columnEntry.get())
			print(search_word)
			for index, row in df.iterrows():
				if str(row[column_value]) == search_word:
					filtered_df = filtered_df.append(row, ignore_index=True)
			querytextPad.insert('1.0', filtered_df.to_string(index=False))
			print(filtered_df)
		
		searchButton = Button(search_db_window, text="Add", width=12, height=2, font=('Arial', 12), 						command=search_db)
		searchButton.place(relx=0.83, rely=0.09, anchor=CENTER)
		
		def reset_db_search():
			global filtered_df
			global querytextPad
			querytextPad.config(state='normal')
			filtered_df = pd.DataFrame(columns=column_headings_list)
			querytextPad.delete('1.0', END)
			print(filtered_df)
		
		reset_search_Button = Button(search_db_window, text="Reset", width=18, height=2, 
					font=('Arial', 12), command=reset_db_search)
		reset_search_Button.place(relx=0.70, rely=0.80, anchor=CENTER)
		
		def add_all_to_db():
			global filtered_df
			global querytextPad
			querytextPad.config(state='normal')
			filtered_df = pd.DataFrame(columns=column_headings_list)
			for index, row in df.iterrows():
				filtered_df = filtered_df.append(row, ignore_index=True)
			querytextPad.delete('1.0', END)
			querytextPad.insert('1.0', filtered_df.to_string(index=False))
			print(filtered_df)
		
		reset_search_Button = Button(search_db_window, text="Find All", width=18, height=2, 
					font=('Arial', 12), command=add_all_to_db)
		reset_search_Button.place(relx=0.30, rely=0.80, anchor=CENTER)
		print(filtered_df)

def dataframe_plot_launch(plot_window_title, plot_type):
	global dataframe_plot_window
	global graph_title_label
	global column_headings_list
	global file_path_label2
	global file_path_label1
	global prediction_range_entry1
	global prediction_range_entry2
	
	if (file_path_label1.cget("text")) == "Equation:" or file_path_display == "" or 				file_path_label2.cget("text") == "Please import file data":
		file_path_label1.config(text="File Path:")
		file_path_label2.config(text="Please import file data", fg="red")
	else:
		dataframe_plot_window = Tk()
		configure_window(dataframe_plot_window, plot_window_title)
		column_headings_list = []
		for n in list(df.columns.values):
			column_headings_list.append(n)
		print(column_headings_list)
		
		plotting_label = Label(dataframe_plot_window, text="Plotting", width=15, height=2,
		              font=('Arial',13))
		plotting_label.place(relx=0.14, rely=0.1, anchor=CENTER)
		
		x_axis_label = Label(dataframe_plot_window, text="X-Axis Variable: ", width=16, height=2,
		              font=('Arial',11))
		x_axis_label.place(relx=0.13, rely=0.23, anchor=CENTER)
		
		x_axis_entry = ttk.Combobox(dataframe_plot_window, state='readonly', width=10, text = "", 
				font = ('Arial', 11))
		x_axis_entry.place(relx=0.32, rely=0.23, anchor=CENTER)
		x_axis_entry.config(values = column_headings_list)
		
		if plot_type != "pie":
			x_axis_log_label = Label(dataframe_plot_window, text="Log Scale?", width=10, height=2,
				      font=('Arial',11))
			x_axis_log_label.place(relx=0.47, rely=0.23, anchor=CENTER)
			
			x_axis_log_entry = ttk.Combobox(dataframe_plot_window, state='readonly', width=10, 
					text = "", font = ('Arial', 11))
			x_axis_log_entry.place(relx=0.62, rely=0.23, anchor=CENTER)
			x_axis_log_entry.config(values = ["Yes", "No"])
			
			if plot_type != "hist":
				y_axis_log_label = Label(dataframe_plot_window, text="Log Scale?", width=10, 						height=2, font=('Arial',11))
				y_axis_log_label.place(relx=0.47, rely=0.36, anchor=CENTER)
			
				y_axis_log_entry = ttk.Combobox(dataframe_plot_window, state='readonly', width=10, 
					text = "", font = ('Arial', 11))
				y_axis_log_entry.place(relx=0.62, rely=0.36, anchor=CENTER)
				y_axis_log_entry.config(values = ["Yes", "No"])
		
		if plot_type != "hist":
			y_axis_label = Label(dataframe_plot_window, text="Y-Axis Variable: ", width=16, height=2,
				      font=('Arial',11))
			y_axis_label.place(relx=0.13, rely=0.36, anchor=CENTER)
			
			y_axis_entry = ttk.Combobox(dataframe_plot_window, state='readonly', width=10, text = "", 
					font = ('Arial', 11))
			y_axis_entry.place(relx=0.32, rely=0.36, anchor=CENTER)
			y_axis_entry.config(values = column_headings_list)
		else:
			bins_label = Label(dataframe_plot_window, text="Number of Bins: ", width=16, height=2,
				      font=('Arial',11))
			bins_label.place(relx=0.13, rely=0.36, anchor=CENTER)
			
			bins_entry = Entry(dataframe_plot_window, width=10, font = ('Arial', 11))
			bins_entry.place(relx=0.31, rely=0.36, anchor=CENTER)
	
		if plot_type == "pie":
			x_axis_label.config(text="Values")
			if plot_type != "hist":
				y_axis_label.config(text="Labels")
		
		graph_title_label = Label(dataframe_plot_window, text="Graph Title: ", width=16, height=2, 					font=('Arial', 11))
		graph_title_label.place(relx=0.13, rely=0.49, anchor=CENTER)
		
		graph_title_entry = Entry(dataframe_plot_window, width=20)
		graph_title_entry.place(relx=0.36, rely=0.49, anchor=CENTER)
		
		'''if plot_type == "line" or plot_type == "scatter":
			prediction_label = Label(dataframe_plot_window, text="Make Prediction?", width=16, height=2,
				      font=('Arial',11))
			prediction_label.place(relx=0.13, rely=0.62, anchor=CENTER)
			
			prediction_range_entry1 = Entry(dataframe_plot_window, width=10, state=DISABLED)
			prediction_range_entry1.place(relx=0.50, rely=0.62, anchor=CENTER)
			
			prediction_to_label = Label(dataframe_plot_window, text="to", width=6, height=1, 					font=('Arial', 10))
			prediction_to_label.place(relx=0.65, rely=0.62, anchor=CENTER)
			
			prediction_range_entry2 = Entry(dataframe_plot_window, width=10, state=DISABLED)
			prediction_range_entry2.place(relx=0.80, rely=0.62, anchor=CENTER)
			
			def prediction_rb_yes_sel():
				global prediction_range_entry1
				global prediction_to_label
				global prediction_range_entry2
				
				prediction_range_entry1.config(state=NORMAL)
				prediction_range_entry1.delete(0, END)
				prediction_range_entry1.insert(END,"0")
				prediction_range_entry2.config(state=NORMAL)
				prediction_range_entry2.delete(0, END)
				prediction_range_entry2.insert(END,"0")
			
			def prediction_rb_no_sel():
				global prediction_range_entry1
				global prediction_to_label
				global prediction_range_entry2
				
				prediction_range_entry1.config(state=DISABLED)
				prediction_range_entry2.config(state=DISABLED)
			
			prediction_var = IntVar()
			
			prediction_rb_yes = Radiobutton(dataframe_plot_window, variable=prediction_var, value=1, 
					text="Yes", command=prediction_rb_yes_sel)
			prediction_rb_yes.place(relx=0.287, rely=0.62, anchor=CENTER)
			prediction_rb_no = Radiobutton(dataframe_plot_window, variable=prediction_var, value=0, 
					text="No", command=prediction_rb_no_sel)
			prediction_rb_no.place(relx=0.367, rely=0.62, anchor=CENTER)'''
		
		def dataframe_plot():
			global x_value
			global y_value
			x_value = str(x_axis_entry.get())
			if plot_type != "hist":
				y_value = str(y_axis_entry.get())
			graph_title = str(graph_title_entry.get())
			if plot_type == "line" or plot_type == "scatter":
				pearsonr = str(scipy.stats.pearsonr(df.loc[ :, x_value], 
				df.loc[ :, y_value])[0])
				pearsonr = "r = " + pearsonr
				print(pearsonr)
				plt.plot([], [], ' ', label=pearsonr)
				if plot_type == "line":
					plt.plot(df.loc[ :, x_value], df.loc[ :, y_value], label="Recorded Data")
				elif plot_type == "scatter":
					plt.scatter(df.loc[ :, x_value], df.loc[ :, y_value], label="Recorded Data")
				'''if prediction_range_entry1.cget('state') == NORMAL and 						prediction_range_entry2.cget('state') == NORMAL:
					X = df.loc[ :, x_value]
					y = df.loc[ :, y_value]
					X_train = X
					y_train = y
					X_train= X_train.values.reshape(-1, 1)
					y_train= y_train.values.reshape(-1, 1)
					x_prediction_list = np.array(range(int(prediction_range_entry1.get()), 							int(prediction_range_entry2.get())+1))
					y_prediction_list = np.array([]) 
					global model
					for i in x_prediction_list:
						model = MLPRegressor(hidden_layer_sizes=(3), activation='tanh', 							solver='lbfgs')
						model = RandomForestRegressor(n_estimators=500, oob_score=True, 							random_state=100)
						model.fit(X_train, y_train)
						model = Sequential()
						model.add(LSTM(units=30, return_sequences= True, 							input_shape=(X.shape[1],2)))
						model.add(LSTM(units=30, return_sequences=True))
						model.add(LSTM(units=30))
						model.add(Dense(units=1))
						model.compile(optimizer='adam', loss='mean_squared_error')
						model.fit(X_train, y_train, epochs=200, batch_size=32)
						X_item = np.array([i])
						X_item = X_item.reshape(-1, 1)
						y_prediction_list = np.append(y_prediction_list, 							float(model.predict(X_item)))
						
					print(x_prediction_list)
					print(y_prediction_list)
					prediction_df = pd.DataFrame({x_value:x_prediction_list, 							y_value:y_prediction_list})
					pred_row_count = 0
					for pred_index, pred_row in prediction_df.iterrows():
						for index, row in df.iterrows():
							if int(row[x_value]) == int(pred_row[x_value]):
								prediction_df.loc[pred_row_count, 
								y_value] = row[y_value]
						pred_row_count += 1
					print(prediction_df)
					if plot_type == "line":
						plt.plot(prediction_df.loc[ :, x_value], prediction_df.loc[ :, 							y_value], label="Projected Data")
					elif plot_type == "scatter":
						plt.scatter(prediction_df.loc[ :, x_value], prediction_df.loc[ :, 							y_value], label="Projected Data")'''
				xneg_value = False
				xpos_value = False
				xzero_value = False
				yneg_value = False
				ypos_value = False
				yzero_value = False
				for index, row in df.iterrows():
					if row[x_value] < 0:
						xneg_value = True
					elif row[x_value] > 0:
						xpos_value = True
					elif row[x_value] == 0:
						xzero_value = True
				for index, row in df.iterrows():
					if row[y_value] < 0:
						yneg_value = True
					elif row[y_value] > 0:
						ypos_value = True
					elif row[y_value] == 0:
						yzero_value = True
				if xpos_value == True and xneg_value == True or xzero_value == True:
					plt.axvline(0, color='gray', linewidth=1)
				if ypos_value == True and yneg_value == True or yzero_value == True:
					plt.axhline(0, color='gray', linewidth=1)
			elif plot_type == "bar":
				plt.bar(df.loc[ :, x_value], df.loc[ :, y_value], align='center', alpha=0.5, 					label="Recorded Data")
			elif plot_type == "box":
				sns.boxplot(data=df, x=df.loc[ :, x_value], y=df.loc[ :, y_value])
			elif plot_type == "pie":
				def make_autopct(values):
					def my_autopct(pct):
						total = sum(values)
						val = int(round(pct*total/100.0))
						return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
					return my_autopct
				plt.pie(df.loc[ :, x_value], labels=df.loc[ :, y_value], 
				autopct=make_autopct(df.loc[ :, x_value]))
				plt.xlabel(x_value, labelpad=15)
				plt.ylabel(y_value, labelpad=15)
			elif plot_type == "hist":
				plt.hist(df.loc[ :, x_value], int(bins_entry.get()), alpha=0.5, ec='black')
			if plot_type != "pie":
				plt.xlabel(x_value)
				if x_axis_log_entry.get() == "Yes":
					plt.xscale('log')
				if plot_type != "hist":
					plt.ylabel(y_value)
					if y_axis_log_entry.get() == "Yes":
						plt.yscale('log')
				plt.legend(loc='best')
			plt.title(graph_title)	
			plt.show()
		
		line_plot_button = Button(dataframe_plot_window, text="Plot Graph", font = ("Arial", 12),
				width=10, height=3, bg="white", 
				activebackground="light grey", 
				bd="3", highlightbackground="black", 
				command = dataframe_plot)
		line_plot_button.place(relx=0.13, rely=0.79, anchor=CENTER)

def equation_plot_launch():
	global equation_plot_window
	global graph_title_label
	global file_path_label2
	global file_path_label1
	
	if (file_path_label1.cget("text")) == "File Path:" or file_path_display == "" or 				(file_path_label2.cget("text")) == "Please import equation data":
		file_path_label1.config(text="Equation:")
		file_path_label2.config(text="Please import equation data", fg="red")
	else:
		equation_plot_window = Tk()
		configure_window(equation_plot_window, "Line Plotting")
		
		plotting_label = Label(equation_plot_window, text="Plotting", width=15, height=2,
		              font=('Arial',13))
		plotting_label.place(relx=0.14, rely=0.1, anchor=CENTER)
		
		x_axis_label = Label(equation_plot_window, text="X-Axis Variable: ", width=16, height=2,
		              font=('Arial',11))
		x_axis_label.place(relx=0.13, rely=0.23, anchor=CENTER)
		
		x_axis_entry = ttk.Combobox(equation_plot_window, state='readonly', width=10, text = "x", 
				font = ('Arial', 11))
		x_axis_entry.place(relx=0.32, rely=0.23, anchor=CENTER)
		x_axis_entry.config(values = ["x"])
		
		y_axis_label = Label(equation_plot_window, text="Y-Axis Variable: ", width=16, height=2,
		              font=('Arial',11))
		y_axis_label.place(relx=0.13, rely=0.36, anchor=CENTER)
		
		y_axis_entry = ttk.Combobox(equation_plot_window, state='readonly', width=10, text = "y", 
				font = ('Arial', 11))
		y_axis_entry.place(relx=0.32, rely=0.36, anchor=CENTER)
		y_axis_entry.config(values = ["y"])
		
		x_range_label = Label(equation_plot_window, text="X-Axis Range: ", width=16, height=2, 					font=('Arial', 11))
		x_range_label.place(relx=0.13, rely=0.49, anchor=CENTER)
		
		x_range_entry1 = Entry(equation_plot_window, width=10)
		x_range_entry1.place(relx=0.34, rely=0.49, anchor=CENTER)
		
		to_label = Label(equation_plot_window, text="to", width=6, height=1, 					font=('Arial', 11))
		to_label.place(relx=0.49, rely=0.49, anchor=CENTER)
		
		x_range_entry2 = Entry(equation_plot_window, width=10)
		x_range_entry2.place(relx=0.64, rely=0.49, anchor=CENTER)
		
		graph_title_label = Label(equation_plot_window, text="Graph Title: ", width=16, height=2, 					font=('Arial', 11))
		graph_title_label.place(relx=0.13, rely=0.62, anchor=CENTER)
		
		graph_title_entry = Entry(equation_plot_window, width=20)
		graph_title_entry.place(relx=0.36, rely=0.62, anchor=CENTER)
		
		def equation_line_plot():
			global x_value
			global y_value
			x = np.array(range(int(x_range_entry1.get()), int(x_range_entry2.get())+1))
			print(x)
			y = eval(y_equation)
			x_value = str(x_axis_entry.get())
			y_value = str(y_axis_entry.get())
			graph_title = str(graph_title_entry.get())
			plt.plot(x, y)
			plt.axhline(0, color='gray', linewidth=1)
			plt.axvline(0, color='gray', linewidth=1)
			plt.xlabel("x")
			plt.ylabel("y")
			plt.title(graph_title)
			plt.show()
		
		line_plot_button = Button(equation_plot_window, text="Plot Graph", font = ("Arial", 12),
				width=10, height=3, bg="white", 
				activebackground="light grey", 
				bd="3", highlightbackground="black", 
				command = equation_line_plot)
		line_plot_button.place(relx=0.13, rely=0.80, anchor=CENTER)

def stat_summary_launch():
	global stat_summary_window
	global file_path_label1
	global file_path_label2
	
	if (file_path_label1.cget("text")) == "Equation:" or file_path_display == "" or 				file_path_label2.cget("text") == "Please import file data":
		file_path_label1.config(text="File Path:")
		file_path_label2.config(text="Please import file data", fg="red")
	else:
		stat_summary_window = Tk()
		configure_window(stat_summary_window, "Statistical Summary")
		stat_summary_window.geometry("300x400")
		column_headings_list = []
		for n in list(df.columns.values):
			column_headings_list.append(n)
		print(column_headings_list)
	
		stat_var_label = Label(stat_summary_window, text="Variable: ", width=10, height=2,
		              font=('Arial',11))
		stat_var_label.place(relx=0.20, rely=0.08, anchor=CENTER)
		
		stat_var_entry = ttk.Combobox(stat_summary_window, state='readonly', width=10, text = "", 
				font = ('Arial', 11))
		stat_var_entry.place(relx=0.56, rely=0.08, anchor=CENTER)
		stat_var_entry.config(values = column_headings_list)
	
		stat_text_pad = ScrolledText.ScrolledText(stat_summary_window, height=15)
		stat_text_pad.pack(expand=True, fill='x', side='bottom')
	
		def stat_var_calc():
			stat_text_pad.delete('1.0', END)
			stat_var = str(stat_var_entry.get())
			stat_var_list = df.loc[ :, stat_var]
			#stat_text_pad.insert('1.0', ("Kendall Rank Correlation Coefficient = " +  + "\n"))
			#stat_text_pad.insert('1.0', ("Spearman's Rank Correlation Coefficient = " +  + "\n"))
			#stat_text_pad.insert('1.0', ("Pearson Correlation Coefficient = " + 					str(scipy.stats.pearsonr(df.loc[ :, x_value], df.loc[ :, y_value])[0]) + "\n"))
			#stat_text_pad.insert('1.0', ("" + "\n"))
			stat_text_pad.insert('1.0', ("Range = " + str(round(max(stat_var_list)-min(stat_var_list), 				5)) + "\n"))
			stat_text_pad.insert('1.0', ("Max = " + str(round(max(stat_var_list), 5)) 				+ "\n"))
			stat_text_pad.insert('1.0', ("Min = " + str(round(min(stat_var_list), 5)) 				+ "\n"))
			q75, q25 = np.percentile(stat_var_list, [75 ,25])
			iqr = q75 - q25
			stat_text_pad.insert('1.0', ("Interquartile Range = " + 
				str(round(iqr, 5)) + "\n"))
			stat_text_pad.insert('1.0', ("Upper Quartile = " + str(round(q75, 5)) 				+ "\n"))
			stat_text_pad.insert('1.0', ("Lower Quartile = " + str(round(q25, 5)) 				+ "\n"))
			stat_text_pad.insert('1.0', ("Sample Variance = " + 						str(round(statistics.variance(stat_var_list), 5)) + "\n"))
			stat_text_pad.insert('1.0', ("Sample Std Dev = " + 						str(round(statistics.stdev(stat_var_list), 5)) + "\n"))
			stat_text_pad.insert('1.0', ("Population Variance = " + 					str(round(statistics.pvariance(stat_var_list), 5)) + "\n"))
			stat_text_pad.insert('1.0', ("Population Std Dev = " + 						str(round(statistics.pstdev(stat_var_list), 5)) + "\n"))
			stat_text_pad.insert('1.0', ("Median = " + str(round(statistics.median(stat_var_list), 5)) 				+ "\n"))
			stat_text_pad.insert('1.0', ("Mean = " + str(round(statistics.mean(stat_var_list), 5)) + 				"\n"))
		
		stats_var_submit = Button(stat_summary_window, text="Go", font = ("Arial", 11),
					width=2, height=1, bg="white", 
					activebackground="light grey", 
					bd="3", highlightbackground="black",
					command = stat_var_calc)
		stats_var_submit.place(relx=0.87, rely=0.08, anchor=CENTER)

#Defines create_menubar(): function (Configures Menu Bar)

def create_menubar(x):
	global recent_files_list_new
	menubar = Menu(x)
	importmenu = Menu(menubar, tearoff=0)
	importmenu.add_command(label="Create CSV Data", command=create_csv_data)
	importmenu.add_command(label="Import External CSV Data", command=open_csv_command)
	importmenu.add_command(label="Import External Excel Data", command=open_excel_command)
	importmenu.add_command(label="Import Equation Data", command=open_equation_command)
	menubar.add_cascade(label="Import", menu=importmenu)
	recentmenu = Menu(importmenu, tearoff = 0)
	print(recent_files_list_new)
	importmenu.add_cascade(label="Recent Files...", menu=recentmenu)
	recentmenu.add_command(label=recent_files_list_new[0], 								command=lambda:open_recent_files(recent_files_list_new[0]))
	recentmenu.add_command(label=recent_files_list_new[1], 								command=lambda:open_recent_files(recent_files_list_new[1]))
	recentmenu.add_command(label=recent_files_list_new[2], 								command=lambda:open_recent_files(recent_files_list_new[2]))
	recentmenu.add_command(label=recent_files_list_new[3], 								command=lambda:open_recent_files(recent_files_list_new[3]))
	recentmenu.add_command(label=recent_files_list_new[4], 								command=lambda:open_recent_files(recent_files_list_new[4]))
	dbmenu = Menu(menubar, tearoff=0)
	dbmenu.add_command(label="Edit Data", command=edit_db_launch)
	dbmenu.add_command(label="Search/Sort Data", command=search_db_launch)
	menubar.add_cascade(label="Data", menu=dbmenu)
	
	plotmenu = Menu(menubar, tearoff=0)
	plotmenu.add_command(label="Equation Plot", command=equation_plot_launch)
	plotmenu.add_command(label="Line Plot (DF)", command=lambda:dataframe_plot_launch("Line Plot (DF)", "line"))
	plotmenu.add_command(label="Scatter Plot (DF)", command=lambda:dataframe_plot_launch("Scatter Plot (DF)", 									"scatter"))
	plotmenu.add_command(label="Bar Plot (DF)", command=lambda:dataframe_plot_launch("Bar Plot (DF)", "bar"))
	plotmenu.add_command(label="Box Plot (DF)", command=lambda:dataframe_plot_launch("Box Plot (DF)", "box"))
	plotmenu.add_command(label="Pie Chart (DF)", command=lambda:dataframe_plot_launch("Pie Chart (DF)", "pie"))
	plotmenu.add_command(label="Histogram (DF)", command=lambda:dataframe_plot_launch("Histogram (DF)", "hist"))
	menubar.add_cascade(label="Plotting", menu=plotmenu)
	
	statsmenu = Menu(menubar, tearoff=0)
	statsmenu.add_command(label="Statistical Summary", command=stat_summary_launch)
	menubar.add_cascade(label="Statistics", menu=statsmenu)
	
	x.config(menu=menubar)

#Defines root_launch(): function

def root_launch():
	global root
	global file_path_display
	global file_path_label2
	global file_path_label1
	global dftextPad
	file_path_display = ""
	root = Tk()
	configure_window(root, "Analyz 1.0")
	create_menubar(root)
	dftextPad=ScrolledText.ScrolledText(root, bd=3, state='disabled')
	dftextPad.place(rely=0.4, relx=0.5, anchor=CENTER)
	dftextPad.config(height=20, width=80)
	file_path_label1 = Label(root, text="File Path:", width=10, height=2,
                      font=('Arial',12))
	file_path_label1.place(relx=0.1, rely=0.9, anchor=CENTER)
	file_path_label2 = Label(root, text=file_path_display, width=80, height=2,
                      font=('Arial',10))
	file_path_label2.place(relx=0.55, rely=0.9, anchor=CENTER)

#pygame.init()
#(width, height) = (750, 500)
#screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
#pygame.display.flip()
#globeImage = pygame.image.load("globe.jpg").convert()
#globeImage = pygame.transform.scale(globeImage, (750, 500))
#screen.blit(globeImage, (0, 0))
#pygame.display.flip()
#pygame.mixer.music.load('windows.mp3')
#pygame.mixer.music.play(0)
#time.sleep(4)
#pygame.quit()
read_recent_files()
root_launch()
root.mainloop()
