#!/usr/bin/env python3

########################################################################
# Python3                                                Quentin Petit #
# Text Editor                                             October 2019 #
#                                                                      #
#                            patina-gui.py                             #
#                                                                      #
# Current version: 0.3.1                                               #
# Status: Development in progress                                      #
#                                                                      #
# ...                                                                  #
#                                                                      #
# Version history:                                                     #
# +----------+---------+---------------------------------------------+ #
# |   Date   | Version | Comment                                     | #
# +----------+---------+---------------------------------------------+ #
# | 20191011 | 0.1.0   | First development                           | #
# | 20191012 | 0.1.1   | Bug: compatibility Lin/Win                  | #
# | 20191013 | 0.2.0   | New: icon and "New File" function           | #
# | 20191014 | 0.3.0   | UPG: gui sizing and new/open/save functions | #
# | 20200203 | 0.3.1   | New: important notes                        | #
# +----------+---------+---------------------------------------------+ #
#                                                                      #
########################################################################

#                                                                      #
#                              LIBRAIRIES                              #
#                                                                      #

# Importing modules.
import re
import os
import platform
import filecmp
import tkinter
from tkinter import filedialog, simpledialog, messagebox

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                                      #
#                               VARIABLES                              #
#                                                                      #

# Files and directories.
path_scp = os.path.dirname(os.path.abspath(__file__))
file_ico = os.path.join(path_scp, 'Patina.ico')
file_gif = os.path.join(path_scp, 'Patina.gif')

# Environment.
oper_sys = platform.system()

# Window dimensions.
width = 300
height = 300

# No opened or temporary files.
opened_file = None
tmp_file = None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                                      #
#                               FUNCTIONS                              #
#                                                                      #

# Function to open a file.
def action_open():
    global opened_file
    opened_file = filedialog.askopenfilename()
    if opened_file == "":
        opened_file = None
    else:
        text_area.delete(1.0, tkinter.END)
        file_to_open = open(opened_file, "r")
        text_area.insert(1.0,file_to_open.read())
        file_to_open.close()
        # Change window title with file name.
        root.title("Patina - " + os.path.basename(opened_file))

# Funtion to add a bullet.
def add_bullet():
    line = str(text_area.index(tkinter.INSERT)).split(".")[0] + ".0"
    text_area.insert(line, "   o  ")

# Function to add an enumeration.
def add_enumerate():
    line = str(text_area.index(tkinter.INSERT)).split(".")[0] + ".0"
    text_area.insert(line, "   1. ")

# Function to add note.
def add_note():
    line_nb = int(str(text_area.index(tkinter.INSERT)).split(".")[0])
    line = str(line_nb) + ".0"
    text_area.insert(line, " " * 3 + "+" * 66 + "\n"
                           + " " * 3 + "+ Note:" + " " * 58 + "+\n"
                           + "   +   " )

# Function to add important note.
def add_important():
    line = str(text_area.index(tkinter.INSERT)).split(".")[0] + ".0"
    text_area.insert(line, " " * 3 + "!" * 66 + "\n"
                           + " " * 3 + "!! Note:" + " " * 56 + "!!\n"
                           + "   !!   ")

# Function to add a sub-bullet.
def add_subbullet():
    line = str(text_area.index(tkinter.INSERT)).split(".")[0] + ".0"
    text_area.insert(line, "      -  ")

# Function to find a pattern.
def find():
    # Removing previous tags.
    for tag in text_area.tag_names():
        text_area.tag_delete(tag)
    # Opening text box to get pattern to search.
    str_to_find = simpledialog.askstring('Find', '')
    # Declaring some variables.
    start_index = "1.0"
    text_area.tag_configure("search", background="IndianRed1")
    if str_to_find:
        str_count = len(str_to_find)
        result_index = text_area.search(
            str_to_find, start_index, stopindex="end")
        # If pattern is found.
        if result_index:
            # Move cursor to first pattern.
            text_area.mark_set("insert", result_index)
            text_area.see("insert")
            # Loop to highlight all found patterns.
            while result_index:
                text_area.tag_add("search", result_index,
                    str(result_index) + " + " + str(str_count)  + "c")
                start_index = result_index.split(".")[0] \
                              + "." \
                              + str(int(result_index.split(".")[1]) \
                                    + int(str_count))
                result_index = text_area.search(
                    str_to_find, start_index, stopindex="end")
        # If pattern is not found, print warning message.
        else:
            messagebox.showwarning("Warning",
                "Pattern '" + str_to_find + "' not found.")

# Function to create a new file.
def new_file():
    global tmp_file
    global opened_file
    if opened_file == None:
        if not text_area.compare("end-1c", "==", "1.0"):
            unsaved_aswer = messagebox.askokcancel("Unsaved data",
                "Would you like to save the data?")
            if unsaved_aswer == True:
                save_file_as()
            else:
                rm_content()
        else:
            rm_content()
    else:
        # Saving current text in tmp file.
        tmp_save()
        # Checking if modifications have been saved.
        if not filecmp.cmp(opened_file, tmp_file):
            os.remove(tmp_file)
            tmp_file = None
            unsaved_aswer = messagebox.askokcancel("Unsaved data",
                "Would you like to save the data?")
            if unsaved_aswer == True:
                save_file()
            else:
                rm_content()
        else:
            os.remove(tmp_file)
            tmp_file = None
            rm_content()

# Function to print 2 newlines /w correct indentation if enter pressed.
def new_line(event):
    cursor_index = str(text_area.index(tkinter.INSERT))
    previous_row = str(int(cursor_index.split(".")[0]) - 1)
    previous_line = text_area.get(previous_row + ".0",
        previous_row + ".72")
    # Continue if the previous line is not blank.
    if previous_line != '' and not previous_line.isspace():
        # Getting the first line of the paragraph.
        if previous_row == "1":
            last_block_start = previous_line
        else:
            while (previous_line != ''
                   and not previous_line.isspace()):
                previous_row = str(int(previous_row) - 1)
                previous_line = text_area.get(previous_row + ".0",
                    previous_row + ".72")
            last_block_row = str(int(previous_row) + 1)
            last_block_start = text_area.get(last_block_row + ".0",
                    last_block_row + ".72")
        if last_block_start.startswith("      -  "):
            text_area.insert(cursor_index, "\n      -  ")
        elif last_block_start.startswith("   o  "):
            text_area.insert(cursor_index, "\n   o  ")
        elif re.match(r"^   \d+\..*$", last_block_start):
            enumerate_nb = str(
                int(last_block_start.split(".")[0].lstrip()) + 1)
            text_area.insert(cursor_index,
                "\n   " + enumerate_nb + ". ")
        else:
            text_area.insert(cursor_index, "\n   ")

# Function launched by the "Open File..." button.
def open_file():
    global tmp_file
    global opened_file
    if opened_file == None:
        if not text_area.compare("end-1c", "==", "1.0"):
            unsaved_aswer = messagebox.askokcancel("Unsaved data",
                "Would you like to save the data?")
            if unsaved_aswer == True:
                save_file_as()
            else:
                action_open()
        else:
            action_open()
    else:
        # Saving current text in tmp file.
        tmp_save()
        # Checking if modifications have been saved.
        if not filecmp.cmp(opened_file, tmp_file):
            os.remove(tmp_file)
            tmp_file = None
            unsaved_aswer = messagebox.askokcancel("Unsaved data",
                "Would you like to save the data?")
            if unsaved_aswer == True:
                save_file()
            else:
                action_open()
        else:
            os.remove(tmp_file)
            tmp_file = None
            action_open()

# Function to launch actions when key is released.
def released_key(event):
    # Setting variables for status bar.
    val_status_bar.set("Characters: "
                       + str(len(text_area.get("1.0", 'end-1c')))
                       + ", Position: "
                       + str(text_area.index(tkinter.INSERT)))
    # Adding new line when we reach the end of the widget.
    column = int(str(text_area.index(tkinter.INSERT)).split(".")[1])
    if column > 72:
        
        # Finding last space to wrap words correctly.
        row = str(text_area.index(tkinter.INSERT)).split(".")[0]
        line_start = float(row + ".0")
        line_end = float(row + ".73")
        line_content = text_area.get(line_start, line_end)
        newline_position = row + "." + str(line_content.rfind(" "))
        # Removing the space before adding the newline.
        text_area.delete(newline_position)
        # Checking how starts the line to add the proper indentation.
        if line_content.startswith("      -  "):
            newline_content = "\n         "
        elif line_content.startswith("   o  "):
            newline_content = "\n      "
        elif re.match(r"^   \d+\..*$", line_content):
            lead_spaces_count = len(line_content.split(".")[0]) + 2
            newline_content = "\n" + " " * lead_spaces_count
        else:
            lead_spaces_count = len(line_content) \
                                - len(line_content.lstrip(' '))
            newline_content = "\n" + " " * lead_spaces_count
        text_area.insert(newline_position, newline_content)

# Function to empty the text area.
def rm_content():
    global opened_file
    text_area.delete('1.0', 'end')
    opened_file = None
    # Change window title with file name.
    root.title("Patina - Untitled")

# Function to save a file.
def save_file():
    global opened_file
    if opened_file:
        text_area_text = text_area.get('1.0', 'end-1c')
        save_text = open(opened_file, mode='w', encoding="UTF-8")
        save_text.write(text_area_text)
        save_text.close()
    else:
        save_file_as()

# Function to save a new file.
def save_file_as():
    global opened_file
    opened_file = filedialog.asksaveasfile(mode='w')
    if opened_file:
        text_area_text = text_area.get('1.0', 'end-1c')
        opened_file.write(text_area_text)
        opened_file.close()
        # opened_file is a _io.TextIOWrapper variable.
        # Transforming it into a str for future save.
        opened_file = str(opened_file)
        opened_file = opened_file.split(" ")[1].split("'")[1]
        # Change window title with file name.
        root.title("Patina - " + os.path.basename(opened_file))

# Function to save a file temporarily.
def tmp_save():
    global tmp_file
    global opened_file
    tmp_file = opened_file + "_tmp"
    text_area_text = text_area.get('1.0', 'end-1c')
    save_text = open(tmp_file, mode='w', encoding="UTF-8")
    save_text.write(text_area_text)
    save_text.close()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                                      #
#                               BEGINNING                              #
#                                                                      #

# Defining GUI window.
root = tkinter.Tk()
root.title("Patina - Untitled")
# Importing icon with a try block if icon missing or OS not specified.
try:
    if oper_sys == "Linux":
        root.tk.call('wm', 'iconphoto',
            root._w, tkinter.PhotoImage(file=file_gif))
    elif oper_sys == "Windows":
        root.iconbitmap(file_ico)
except:
    pass

val_src_type = tkinter.IntVar()

# Setting dimensions.
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
left = (screen_width / 2) - (width / 2)
top = (screen_height / 2) - (height /2)
root.geometry('%dx%d+%d+%d' % (width, height, left, top))

# Setting the menu.
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
# Setting the file menu.
file_menu = tkinter.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New File", command=new_file)
file_menu.add_command(label="Open File...", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As...", command=save_file_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)
# Setting the edit menu.
edit_menu = tkinter.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Find", command=find)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
# Setting the insert menu.
insert_menu = tkinter.Menu(menu_bar, tearoff=0)
insert_menu.add_command(label="Bullets", command=add_bullet)
insert_menu.add_command(label="Sub-bullets", command=add_subbullet)
insert_menu.add_command(label="Numbering", command=add_enumerate)
insert_menu.add_separator()
insert_menu.add_command(label="Note", command=add_note)
insert_menu.add_command(label="Important note", command=add_important)
#insert_menu.add_separator()
#insert_menu.add_command(label="Source", command=add_src)  # USE Toplevel()
menu_bar.add_cascade(label="Insert", menu=insert_menu)

# Make the textarea auto resizable.
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Defining text area and scrollbar.
text_area = tkinter.Text(height=30, width=72, wrap="none")
scrollbar = tkinter.Scrollbar(text_area)
text_area.grid(sticky = tkinter.N + tkinter.E + tkinter.S + tkinter.W)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
scrollbar.config(command=text_area.yview)
text_area.config(yscrollcommand=scrollbar.set)

# Defining status bar.
val_status_bar = tkinter.StringVar()
label_status_bar = tkinter.Label(root, textvariable=val_status_bar,
    bd=1, relief=tkinter.SUNKEN, anchor=tkinter.W)
label_status_bar.grid(row=1, column=0, sticky = tkinter.E + tkinter.W)

# Executing released_key function when a key is released.
text_area.bind("<KeyRelease>", released_key)
text_area.bind("<KeyRelease-Return>", new_line)

# Running the GUI window.
root.mainloop()

#                                                                      #
#                                  END                                 #
#                                                                      #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
