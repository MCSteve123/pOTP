"""
pOTP-Cilent(offline-edition)

? 可以存储OTP，且可以同时查看多个
? 多窗口功能，无缝切换OTP
? 6位密码，方便有效，重启时自动登录，无需再输入
? 使用加密API[1]，无密钥无法识别

! 密码暂时无法修改，只有welcome界面[2]可以设置
! 普通密码无法存储

* [1]加密API:API来源：https://github.com/MCSteve123/PyEncry-API，API开源协议：Apache license 2.0
* [2]welcome界面:指标题为“pOTP-welcome”的页面（只有检测到没有otp文件时才出现，一般情况调不出来）

* 版本：v0.6-offl
* 属于pOTP-offline
* 使用VSCode并装载Better comment扩展查看代码注释效果更佳
"""

#* 导入库
from base64 import b32decode
import functions as func
import pyotp
from pyperclip import paste
from restart import restart as rs
from threading import Thread
from tkinter import *
from tkinter.messagebox import showerror, askyesno
from tkinter.ttk import Combobox

FONT = func.FONT

def restart(last_delete = False):
    func.write_otps(otps, func.password, last_delete)
    thread = Thread(target=rs)
    thread.start()
    exit(0x01)

def get_dict_keys(dict: dict) -> list:
    """获取字典键"""
    a = dict.keys()
    temp = []
    for i in a:
        temp.append(i)
    return temp

def create_new_otp() -> None:
    """创建新OTP"""
    global otps
    root = Tk()
    root['bg'] = 'white'
    root.geometry('400x270+200+100')
    root.title('pOTP-create new OTP')
    root.resizable(False, False)
    root.iconbitmap('icon.ico')

    name = StringVar(root)
    note = StringVar(root)
    code = StringVar(root)

    def create():
        if name.get() == 'no password' or name.get() in otps.keys():
            showerror('pOTP-CreateOTP-Error', 'Nullity name, please change it.')
            return
        try: b32decode(code.get())
        except:
            showerror('pOTP-CreateOTP-Error', 'Nullity base32, please change it.')
            return
        otps[name.get()] = '%s-%s'%(code.get(), note.get())
        restart()

    Label(root, text='pOTP-create', bg='white', fg='green', font=FONT[2]).place(x=107, y=0)
    Label(root, text='name:', bg='white', fg='blue', font=FONT[0]).place(x=0, y=50)
    Entry(root, textvariable=name, width=15, bg='white', fg='blue', font=FONT[0]).place(x=65, y=52)
    Label(root, text='note:', bg='white', fg='blue', font=FONT[0]).place(x=0, y=80)
    Entry(root, textvariable=note, width=15, bg='white', fg='blue', font=FONT[0]).place(x=65, y=82)
    Label(root, text='code:', bg='white', fg='blue', font=FONT[0]).place(x=0, y=110)
    Entry(root, textvariable=code, width=32, bg='white', fg='blue', font=FONT[0]).place(x=5, y=142)
    Button(root, 
           text='Paste from clipboard', 
           command=lambda: code.set(paste()), 
           fg='skyblue', bg='white', 
           font=FONT[1]).place(x=10, y=180)
    Button(root, 
           text='Create and restart', 
           command=create, 
           bg='green', fg='white', 
           font=FONT[4]).place(x=183, y=220)

    root.mainloop()

def alter(old_name: str, old_note: str, old_code: str) -> None:
    """修改OTP"""
    global otps
    root = Tk()
    root['bg'] = 'white'
    root.geometry('400x270+200+100')
    root.title('pOTP-alter OTP-%s'%old_name)
    root.resizable(False, False)
    root.iconbitmap('icon.ico')

    name = StringVar(root)
    name.set(old_name)
    note = StringVar(root)
    note.set(old_note)
    code = StringVar(root)
    code.set(old_code)

    def set():
        try: b32decode(code.get())
        except:
            showerror('pOTP-CreateOTP-Error', 'Nullity base32, please change it.')
            return
        del otps[old_name]
        otps[name.get()] = '%s-%s'%(code.get(), note.get())
        restart()

    Label(root, text='pOTP-alter', bg='white', fg='green', font=FONT[2]).place(x=107, y=0)
    Label(root, text='name:', bg='white', fg='blue', font=FONT[0]).place(x=0, y=50)
    Entry(root, textvariable=name, width=15, bg='white', fg='blue', font=FONT[0]).place(x=65, y=52)
    Label(root, text='note:', bg='white', fg='blue', font=FONT[0]).place(x=0, y=80)
    Entry(root, textvariable=note, width=15, bg='white', fg='blue', font=FONT[0]).place(x=65, y=82)
    Label(root, text='code:', bg='white', fg='blue', font=FONT[0]).place(x=0, y=110)
    Entry(root, textvariable=code, width=32, bg='white', fg='blue', font=FONT[0]).place(x=5, y=142)
    Button(root, 
           text='Paste from clipboard', 
           command=lambda: code.set(paste()), 
           fg='skyblue', bg='white', 
           font=FONT[1]).place(x=10, y=180)
    Button(root, 
           text='Alter and restart', 
           command=set, 
           bg='green', fg='white', 
           font=FONT[4]).place(x=200, y=220)

    root.mainloop()

def settings() -> None:
    """设置界面"""
    global otps
    root = Tk()
    root['bg'] = 'white'
    root.geometry('270x400+200+100')
    root.title('pOTP-settings')
    root.resizable(False, False)
    root.iconbitmap('icon.ico')

    Label(root, text='pOTP-settings', fg='green', bg='white', font=FONT[2]).place(x=30, y=0)

    root.mainloop()

def main() -> None:
    """主函数"""
    global otps

    def set_otp(a) -> None:
        """设置base32和备注"""
        temp = otps[cbox1.get()].split('-')
        the_otp_base32.set(temp[0])
        the_otp_note.set(temp[1])

    def show_otp() -> None:
        """OTP窗口"""

        #* 初始化窗口
        root = Tk()
        root['bg'] = 'white'
        root.geometry('270x350+250+100')
        root.title('OTP-Query-%s'%cbox1.get())
        root.resizable(False, False)
        root.iconbitmap('icon.ico')

        #* 设置OTP实例
        otp = StringVar(root)
        obj = pyotp.TOTP(the_otp_base32.get())
        otp.set(obj.now())

        #* GUI
        Label(root, text='Query OTP', bg='white', fg='green', font=FONT[2]).place(x=45, y=0)
        Label(root, text='name:%s'%cbox1.get(), bg='white', fg='blue', font=FONT[0]).place(x=0, y=40)
        Label(root, text='note:%s'%the_otp_note.get(), bg='white', fg='blue', font=FONT[0]).place(x=0, y=75)
        Label(root, text='------------------------', bg='white', fg='red', font=FONT[2]).place(x=0, y=170)
        Message(root, text='code:\n%s'%the_otp_base32.get(), width=200, bg='white', fg='blue', font=FONT[0]).place(x=-8, y=110)
        Label(root, text='Now:', bg='white', fg='blue', font=FONT[0]).place(x=0, y=200)
        Label(root, textvariable=otp, bg='white', fg='black', font=FONT[3]).place(x=0, y=230)
        Button(root, 
               text='Reload', 
               command=lambda: otp.set(obj.now()), 
               bg='green', fg='white', 
               font=FONT[4]).place(x=170, y=300)

        root.mainloop()  #* 启动窗口

    def delete():
        if askyesno('pOTP-DeleteOTP', 'Do you want to delete "%s"? This password will permanently disappear (really a long time)!'%cbox1.get()):
            del otps[cbox1.get()]
            if len(otps) == 0:
                otps['no password'] = 'LFO4ISD6GDOKT3RVLMD3UG7N24VZNEB3-test password'
            restart(True)

    root = Tk()
    root['bg'] = 'white'
    root.geometry('270x400+100+100')
    root.title('pOTP-Cilent')
    root.resizable(False, False)
    root.iconbitmap('icon.ico')
    root.protocol('WM_DELETE_WINDOW', lambda: exit(0x00))

    otps = dict(otps)
    the_otp_base32 = StringVar(root)
    the_otp_base32.set(otps[get_dict_keys(otps)[0]].split('-')[0])
    the_otp_note = StringVar(root)
    the_otp_note.set(otps[get_dict_keys(otps)[0]].split('-')[1])

    #* GUI
    Label(root, text='pOTP Cilent', bg='white', fg='green', font=FONT[2]).place(x=40, y=0)
    Label(root, text='Please choose your OTP:', bg='white', fg='blue', font=FONT[5]).place(x=5, y=50)
    if 'no password' in otps.keys(): s = ['disabled', 'disabled', 'green', 'white']
    else: s = ['readonly', 'normal', 'white', 'blue']
    cbox1 = Combobox(root, width=15, values=get_dict_keys(otps), state=s[0], font=FONT[0])
    cbox1.current(0)
    cbox1.bind('<<ComboboxSelected>>', set_otp)
    cbox1.place(x=5, y=80)
    Button(root, 
           text='Query this OTP', 
           state=s[1], command=show_otp, 
           bg='white', fg='green', 
           font=FONT[4]).place(x=5, y=120)
    Button(root, 
           text='Alter this OTP', 
           state=s[1], command=lambda: alter(cbox1.get(), the_otp_note.get(), the_otp_base32.get()), 
           bg='white', fg='blue', 
           font=FONT[4]).place(x=5, y=170)
    Button(root, text='Create new OTP', 
           command=create_new_otp, 
           bg=s[2], fg=s[3], 
           font=FONT[4]).place(x=5, y=240)
    Button(root, text='Delete this OTP', 
           state=s[1], 
           command=delete, 
           bg='white', fg='red', 
           font=FONT[4]).place(x=5, y=290)
    Button(root, 
           text='settings', 
           command=settings, 
           bg='white', fg='blue', 
           font=FONT[5]).place(x=5, y=355)

    root.mainloop()  #* 启动窗口

if __name__ == '__main__':
    """条件执行"""
    func.create_dirs()
    func.login()
    while True:
        try:
            otps = func.read_jsons()
            break
        except:
            showerror('pOTP-LoginPage-Error', 'Password error, please try again.')
            func.login()
    main()
