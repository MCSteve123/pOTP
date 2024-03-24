"""pOTP-restart"""

from subprocess import Popen
from time import sleep
import functions as func

def restart():
    a = open('files/hotlogin.txt', 'w')
    a.write(str(func.password))
    a.close()
    sleep(0.5) #* 让程序有时间exit(0x01)，两个一起开有风险
    Popen(['python', 'main.py'])

#// 电脑爆炸小惊喜（别试，得用任务管理器抢救）
#// if __name__ == '__main__':
#//     restart()
