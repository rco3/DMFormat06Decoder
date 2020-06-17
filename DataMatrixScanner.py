#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 20:27:57 2020

@author: robolsen3
"""
import tkinter as tk
import re


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.entrythingy = tk.Entry(width=100)
        self.entrythingy.pack()

        # here is the application variable
        self.contents = tk.StringVar()
        # set it to some value
        self.contents.set("")
        # tell the entry widget to watch this variable
        self.entrythingy["textvariable"] = self.contents

        # and here we get a callback when the user hits return.
        # we will have the program print out the value of the
        # application variable when the user hits return
        self.entrythingy.bind('<Return>',
                              self.decode_DM_ScanAvenger)

    def print_contents(self, event):
        print("hi. contents of entry is now ---->",
              self.contents.get())

    def write_contents(self, event):
        file1 = open("barcodecapture.raw", "w")
        file1.write(self.contents.get())
        file1.close()


    def decode_DM_ScanAvenger(self, event):
        
        data = bytes(self.contents.get(), encoding='utf_8')
        # print ((data))
        # print(hex(data[3:4]))
        if  b'[)>300629' in data or b'>[)>06'  in data :
            hdr = re.compile('29([0-9]{0,2}[DJKLPQTVZ])')
            #It's a normal Format06 barcode with 30 for RS
            fields=hdr.split(str(data, encoding='utf8'))
            print(fields)
            # for item in fields[1:]:
                
            #     print(item)
            self.contents.set("")

        
        
    def decode_DM_Teemi(self, event):
        hdr = re.compile('([0-9]*[DJKLPQTVZ])')
        data = bytes(self.contents.get(), encoding='utf_8')
        # print ((data))
        # print(hex(data[3:4]))
        if b'\xef\x9c\x8b' in data:
            #\xEF9C8B is the group separator character \u241D
            fields = re.split(b'(\xef\x9c[\x81-\x8e])', data)
            # and there are Record Separator and (I believe ) Record End
            # characters \xEF9C8C and \xEF9C81 as well.
            for item in fields:
                entry=hdr.split(str(item, encoding='utf8'),1)
                print(entry)
        # self.contents.set("")

    def on_closing():
        print("stopping")
        app.stop()
        print('destroy')
        root.destroy()


root = tk.Tk()
app = Application(master=root)
app.mainloop()
