# Lazy Buttons 2
# Demonstrates using a class with Tkinter

from Tkinter import *
import threading
import os
from ffmpy import FFmpeg
import time

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
        self.sourcePath = "/home/user/python/mp3cutter/11.mp4"
        self.cueFile = "/home/user/python/mp3cutter/how_cutting"
        self.resultPath = os.getcwd()
        self.frame1 = Button(text = "flac to mp3 cut", command = lambda: self.flackTrackToMP3())
        self.frame2 = Button(text = "mp4 to mp3 cut", command = lambda: self.trackMP4ToMP3())
        self.frame3 = Button(text = "source", command = lambda: self.create_widgets())
        self.frame1.grid()
        self.frame2.grid()
        self.frame3.grid()
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
            self.bttn3.destroy()
        except:
            pass
        
    def trackMP4ToMP3(self):
        self.frame1.configure(state=NORMAL)
        self.frame2.configure(state=DISABLED)
        self.frame3.configure(state=NORMAL)
        try:            
            self.title1.destroy()
            self.title2.destroy()
            self.title3.destroy()
        
            self.bttn1.destroy()
            self.bttn2.destroy()
            self.bttn3.destroy()
        except:
            pass
        
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
        
        self.check_button = Button(text = "check", command = lambda: self.checkConvertTrackMP4ToMP3())
        self.check_button.grid()
        
        self.start_button = Button(text = "start", command = lambda: self.startConvertTrackMP4ToMP3 ())
        self.start_button.grid()
    
    def checkConvertTrackMP4ToMP3(self):
        print self.sourcePath,self.cueFile,self.resultPath
        
        if self.checkfile(self.sourcePath) and self.checkfile(self.cueFile) and self.checkdir(self.resultPath):
            i = 0    
            tmp_text = ""
            for stroke in self.prepareTask("mp4tomp3"):
                i+=1
                tmp_text += str(i)+stroke[0]['track_name']+" "+stroke[0]['track_lenght']+"\n"
        else:
            tmp_text = "error"
        
        textInfo.update(tmp_text)
        
    def startConvertTrackMP4ToMP3(self):
        if self.checkfile(self.sourcePath) and self.checkfile(self.cueFile) and self.checkdir(self.resultPath):
            Dzinnn(self.prepareTask("mp4tomp3"),self.sourcePath,self.resultPath)
            
            
    def prepareTask(self,type_task):
        if type_task == "mp4tomp3":      
            maker = []
            f = open(self.cueFile)
            full_lenght = (os.popen(r'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 '+str(self.sourcePath).replace(' ', '\ ')+'').read())[:-8]
            for track in f:
                result = re.findall('\d{,2}:*\d{,2}:\d{,2}', track)
                if result!=None:
                    start_time = self.secondsCreate(result[0])
                    maker.append([{"start_time":result[0],"track_name":[x for x in track.split(result[0]) if x][0][:-1],"track_lenght":"0"}])
                    if start_time!=0:
                        maker[len(maker)-2][0]['track_lenght'] = self.tracktimeCreate(int(start_time) - int(self.secondsCreate(maker[len(maker)-2][0]['start_time'])))
                        maker[len(maker)-1][0]['track_lenght'] = self.tracktimeCreate(int(full_lenght) - int(self.secondsCreate(maker[len(maker)-1][0]['start_time'])))
        return maker
    
    def secondsCreate(self,trackTime):
        return sum(map(lambda a:a[0]*a[1],zip([1,60,3600],map(int,reversed(trackTime.split(":"))))))
        
    def tracktimeCreate(self,seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d" % (h, m, s)
    
    def checkfile(self,file_path):
        import os
        return True if os.path.isfile(file_path) else False
        
    def checkdir(self,dir_path):
        import os
        return True if os.path.isdir(dir_path) else False

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
    
    def putSourceInRAM(self):
        path = ""                
        return path

class Dzinnn(object):
    def __init__(self, maker,source,targetpath):
        from Queue import Queue
        self.maker = maker
        self.source = source
        self.targetpath = targetpath
        self.q = Queue()
        self.cutInThread()
        
    def worker(self):
        while True:
            task = self.q.get()
            self.calc(task) 
            self.q.task_done()

    def calc(self,values):
        source = values[0]
        target = values[1]
        cmd = values[2]
        song_name = values[3]
        ff = FFmpeg(
            inputs={source: cmd},
            outputs={target: None }
        )
        tmp_text = song_name + " started...\n"
        textInfo.insert(tmp_text)
        ff.run()
        textInfo.find_and_set(tmp_text, song_name + " done\n")
    
    def cutInThread(self):
        from threading import Thread
        for task in self.maker:
            cmd = "-loglevel quiet -ss "+task[0]['start_time']+" -t "+task[0]['track_lenght']
            target = self.targetpath + "/"+task[0]['track_name']+".mp3"
            song_name = task[0]['track_name']+".mp3"
            put_task = [self.source,target,cmd,song_name,song_name]
            self.q.put(put_task)
        for i in range(4):
            thread = threading.Thread(target=self.worker)
            thread.daemon = True 
            thread.start()

def main():
    mainapp = Application("title frame","400x600")
    
main()