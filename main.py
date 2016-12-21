from Tkinter import *
import threading
import os
from ffmpy import FFmpeg
import time
import mp4tomp3cut

class Application(object):
    def __init__(self,title,geometry):
        self.root = Tk()
        self.root.title(title)
        self.root.geometry(geometry)
        self.app1 = MainFrame(self.root)
        self.app1.mainloop()
        
        
class InfoFrame(Frame):
    def __init__(self, master):
        import os
        Frame.__init__(self)
        self.info_window = Text(self, width = 20, height = 5, wrap = WORD)
        self.info_window.grid()
        self.grid()
        
    def refresh(self,text_info):
        self.info_window.delete('1.0', END)
        self.info_window.insert(0.0,text_info)

class TextInfo(object):
    def __init__(self):
        self.text = ""
    def __str__(self):
        return str(self.text)
    def update(self,text):
        self.text = text
    def insert(self,text):
        self.text += text
    def find_and_set(self,source,target):
        self.text = self.text.replace(source,target)

textInfo = TextInfo()
        

class MainFrame(Frame):
    def __init__(self, master):
        import os
        Frame.__init__(self)
        self.sourcePath = "/home/user/python/mp3cutter/tmp/source.mp4"
        self.cueFile = "/home/user/python/mp3cutter/tmp/cut"
        self.resultPath = "/home/user/python/mp3cutter/tmp/"
        #self.resultPath = os.getcwd()
        self.frame1 = Button(text = "flac to mp3 cut", command = lambda: self.flackTrackToMP3())
        self.frame2 = Button(text = "mp4 to mp3 cut", command = lambda: self.trackMP4ToMP3())
        self.frame1.grid()
        self.frame2.grid()
        self.text_area = Text(self, width = 100, height = 20, wrap = WORD)
        self.text_area.grid()
        self.refresh()
        self.grid()
        
        
    def refresh(self):
        self.text_area.delete('1.0', END)
        self.text_area.insert(0.0,textInfo)
        self.after(1500, self.refresh)
        
    def cleaner(self):
        try:            
            self.title1.destroy()
            self.title2.destroy()
            self.title3.destroy()
        
            self.bttn1.destroy()
            self.bttn2.destroy()
        except:
            pass
        
    def trackMP4ToMP3(self):
        self.frame1.configure(state=NORMAL)
        self.frame2.configure(state=DISABLED)
        try:            
            self.title1.destroy()
            self.title2.destroy()
            self.title3.destroy()
        
            self.bttn1.destroy()
            self.bttn2.destroy()
            self.bttn3.destroy()
        except:
            pass
        
        case = mp4tomp3cut.RollCase(self.sourcePath, self.resultPath, self.cueFile, textInfo)
        
        self.main_title = Label(self, text = "cutting MP4 to MP3")
        self.main_title.grid()        
        
        self.title1 = Label(self, text = "source file - " + self.sourcePath)
        self.title1.grid()
        
        self.bttn1 = Button(text = "source open", command = lambda: self.openfile("source file - ",self.title1,"self.sourcePath"))
        self.bttn1.grid()
        
        self.title2 = Label(self, text = "cue file - "+self.cueFile)
        self.title2.grid()
        self.bttn2 = Button(text = "cue file", command = lambda: self.openfile("cue file - ",self.title2,"self.cueFile"))
        self.bttn2.grid()
        
        self.title3 = Label(self, text = "result -"+self.resultPath)
        self.title3.grid()
        self.bttn3 = Button(text = "dir ", command = lambda: self.opendir("result -",self.title3,"self.resultPath"))
        self.bttn3.grid()
        
        self.check_button = Button(text = "check", command = lambda: case.checkIsExists())
        self.check_button.grid()
        
        self.start_button = Button(text = "start", command = lambda: case.startConverting())
        self.start_button.grid()


    def openfile(self,info, thing, type_v):
        import tkFileDialog as filedialog
        tmp_req = str(filedialog.askopenfile().name)
        thing["text"] = info+str(tmp_req)
        if type_v == "self.cueFile":
            self.cueFile = tmp_req
        if type_v == "self.sourcePath":
            self.sourcePath = tmp_req
        return True
    
    def opendir(self,info,thing,type_v):
        import tkFileDialog as filedialog
        tmp_req = str(filedialog.askdirectory())
        thing["text"] = info + tmp_req
        if type_v == "self.resultPath":
            self.resultPath = tmp_req
        return True
        
def main():
    mainapp = Application("title frame","400x600")
    
main()