import tkinter.messagebox
from pywifi import const
import pywifi
import time

class WIFI:
    def __init__(self,net_str):
        try:
            wifi = pywifi.PyWiFi()
            print(wifi.interfaces())
            #assert "Intel(R) Centrino(R) Advanced-N 6205 #2" == wifi.interfaces()[0].name()
            assert net_str == wifi.interfaces()[0].name()
        except:
            tkinter.messagebox.showinfo("错误提示","请检查您的网卡")
            exit()
    def test_scan(self):
        mywifiname = []
        try:
            wifi = pywifi.PyWiFi()
            iface = wifi.interfaces()[0]
            iface.scan()
            time.sleep(5)
            bsses = iface.scan_results()
            assert bsses
        except:
            tkinter.messagebox.showinfo("错误提示","没有检索到wifi")
        else:
            for p in bsses:
                mywifiname.append(p.ssid) # 名字  
            return mywifiname
        return None

    def test_status(self): #测试网卡状态
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]
        if iface.status() == const.IFACE_CONNECTED:    #状态
            return True
        else:
            return False

    def test_connect(self,name,password):
            wifi = pywifi.PyWiFi()
            iface = wifi.interfaces()[0]
            if self.test_status():
                try:
                    iface.disconnect()  #断开连接 
                    time.sleep(1)
                    assert iface.status() in [const.IFACE_DISCONNECTED,const.IFACE_INACTIVE]
                except:
                    tkinter.messagebox.showinfo("错误提示","无法断开当前wifi")
                    return 
            profile = pywifi.Profile() #创建链接文件
            profile.ssid = name
            profile.auth = const.AUTH_ALG_OPEN     #网卡开放性质
            profile.akm.append(const.AKM_TYPE_WPA2PSK)   #加密算法
            profile.cipher = const.CIPHER_TYPE_CCMP     #加密单元
            profile.key = password

            iface.remove_all_network_profiles()
            tmp_profile = iface.add_network_profile(profile)

            iface.connect(tmp_profile)
            time.sleep(8)

            if iface.status() == const.IFACE_CONNECTED: #assert iface.status() == const.IFACE_CONNECTED
                iface.disconnect()  #断开连接
                time.sleep(1)
                return True
            else:
                return False

            
