"""pOTP-functions"""

import json
import os
from tkinter import *
from tkinter.messagebox import showerror, showinfo, askyesno
from tkinter.simpledialog import askstring
from subprocess import Popen
import PyEncryAPI as api

FONT = [('Yahei', 18), ('Yahei', 15), ('Arial', 25), ('Arial', 50), ('Arial', 18), ('Arial', 14), ('Arial', 8)]  # 字体列表，文件共用
password = 0

def reset():
    if askyesno('pOTP-Reset', 'Your password and OTPs will also be reset. Do you want to continue?'):
        if askstring('pOTP-Reset', 'To reset, please enter "I have decided to reset".') == 'I have decided to reset':
            showinfo('pOTP-Reset', 'Resetting, please wait.')
            try: os.remove('files/passwords/otps.json.encrypted')
            except: pass
            try: os.remove('files/hotlogin.txt')
            except: pass
            finally:
                os.rmdir('files/passwords')
                os.rmdir('files')
                Popen(['python', 'main.py'])
                exit(0x01)

def create_dirs() -> None:
    """创建文件夹"""
    if not os.path.exists('files/passwords'):
        os.makedirs('files/passwords')

def read_jsons() -> dict:
    global password
    """读取json"""
    try:
        a = open('files/passwords/otps.json.encrypted', 'r')
        b = a.read()
        otps = json.loads(api.decry(b, password))
        if not(len(otps)) or type(otps) != dict:
            raise FileNotFoundError()
        a.close()
    except FileNotFoundError:
        while True:
            a = askstring('pOTP-welcome', '''
Hi, you are new here. Please choose a 6-digit password there.
This will be the only password you need to remember. All other passwords are kept by us.

Tips: This password cannot contain "0".''')
            if not a:
                exit(0x00)
            if ('0' in a) or (len(a) != 6):
                showerror('pOTP-welcome', 'The password is illegal, please try again.')
            else:
                password = int(a)
                break
        
        a = open('files/passwords/otps.json.encrypted', 'w')
        a.write(api.encry('{"no password" : "LFO4ISD6GDOKT3RVLMD3UG7N24VZNEB3-test password"}', password))
        a.close()
        a = open('files/passwords/otps.json.encrypted', 'r')
        b = a.read()
        otps = json.loads(api.decry(b, password))
        a.close()

    return otps

def write_otps(otps: dict, the_password: int, last_delete: bool = False) -> None:
    """写入OTP"""
    a = open('files/passwords/otps.json.encrypted', 'w')
    if not(last_delete) and 'no password' in otps.keys():
        del otps['no password']
    a.write(api.encry(json.dumps(otps), the_password))
    a.close()

def login() -> None:
    global password
    """登录"""
    try:
        open('files/passwords/otps.json.encrypted', 'r').close()
    except:
        read_jsons()
    try:
        a = open('files/hotlogin.txt', 'r')
        b = a.read()
        a.close()
        os.remove('files/hotlogin.txt')
        password = int(b)
    except FileNotFoundError:
        root = Tk()
        root['bg'] = 'white'
        root.geometry('270x200+100+100')
        root.title('pOTP-LoginPage')
        root.resizable(False, False)
        root.iconbitmap('icon.ico')
        root.protocol('WM_DELETE_WINDOW', lambda: exit(0x00))

        test_password = StringVar()

        def s_password():
            global password
            try:
                password = int(test_password.get())
                if len(test_password.get()) != 6:
                    raise Exception()
                root.destroy()
            except: showerror('pOTP-LoginPage-Error', 'Password error, please try again.')

        Label(root, text='pOTP', fg='blue', bg='white', font=FONT[2]).place(x=87, y=0)
        Label(root, text='your OTP manager', fg='blue', bg='white', font=FONT[5]).place(x=50, y=40)
        Label(root, text='Password:', fg='orange', bg='white', font=FONT[4]).place(x=10, y=85)
        Entry(root, textvariable=test_password, width=6, fg='skyblue', bg='white', font=FONT[2]).place(x=140, y=80)
        Button(root, 
               text='RESET ALL', 
               command=reset, 
               fg='red', bg='white', 
               font=FONT[4]).place(x=10, y=148)
        Button(root, 
               text='Login', 
               command=s_password, 
               fg='white', bg='green', 
               font=FONT[4]).place(x=185, y=148)

        root.mainloop()
