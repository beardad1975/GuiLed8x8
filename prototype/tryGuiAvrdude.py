from tkinter import *
from tkinter.messagebox import *
from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText


from serial.tools import list_ports
from subprocess import Popen, PIPE
from time import sleep

#燒錄命令
command = "firmware\\avrdude.exe -Cfirmware\\avrdude.conf   -patmega328p -carduino -P{port} -b115200 -D -Uflash:w:firmware\\max7219_v2.uno.standard.hex"

#傳送韌體    
def send():
    
    if not "Arduino" in var1.get():
        if not askyesno('確認','擇選的port好像不是Arduino Uno\n要繼續傳送嗎？'):
            return

    port = option_dict[var1.get()]


    #print("port: ", port)
    text.configure(state=NORMAL)
    btn.configure(state=DISABLED)
    drop_down.configure(state=DISABLED)
    root.update()
    
    text.delete('1.0', END)
    text.insert(END, str("韌體傳送中，請耐心等待...\r\n"))
    text.see(END)
    text.update()
    
    p = Popen(command.format(port=port), stderr=PIPE)
    _, msg = p.communicate()
    msg_list =  msg.decode("cp950").split("\r\n") 
    #print("msg decode: ",repr(msg.decode()))
        
    text.delete('1.0', END)
    text.update()
    
    for line in msg_list:
        text.insert(END, str(line+"\r\n"))
        text.see(END)
        text.update()
        #print("sleep")
        sleep(.1)
    if p.returncode == 0 :
        text.insert(END, str("傳送成功\r\n"))
        text.see(END)
        text.update()
    else:
        text.insert(END, str("傳送失敗\r\n"))
        text.see(END)
        text.update()
    
    text.configure(state=DISABLED)
    btn.configure(state=NORMAL)
    drop_down.configure(state=NORMAL)
    

root = Tk()

#按鈕
btn = Button(root, text="傳送韌體", command=send)
btn.pack()


option_dict = {}
default = ""

#偵測 com port
for port in  list_ports.comports():
    desc = port.description.encode("latin-1").decode("cp950")
    if "Arduino Uno" in desc:
        default = desc
    
    option_dict[desc] = port.device

tmp_list = list(option_dict.keys())
if not default:
    default = tmp_list[0]

    
var1 = StringVar()
#下拉選單
drop_down = OptionMenu(root,var1,default,*tmp_list)
drop_down.pack()

#文字區
text = ScrolledText(root, fg="white", bg="black",width=80, height=10)
text.pack()
text.configure(state=DISABLED)

# Gui主迴圈
root.mainloop()