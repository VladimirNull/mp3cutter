class RollCase(object):
    def __init__(self,sourceFile,targetDir,info):
        from Queue import Queue
        
        self.cuttingFile = ""
        self.sourceFile = sourceFile
        self.targetDir = targetDir

        #self.sourceFile = ("/home/user/python/11.mp4")
        #self.targetDir = ("/home/user/python/")
        #self.cuttingFile = ("/home/user/python/how_cutting")        
        
        self.info = info
        self.q = Queue()
    
    def refreshPaths(self,sourceFile,targetDir,cuttingFile):
        self.cuttingFile = cuttingFile
        self.sourceFile = sourceFile
        self.targetDir = targetDir
        self.checkIsExists()
        
    def checkIsExists(self,sourceFile=False, targetDir=False,cuttingFile=False):
        if sourceFile!=False and targetDir!=False and cuttingFile!=False:
            self.refreshPaths(sourceFile,targetDir,cuttingFile)
        error = "error\n"
        if self.checkfile(self.sourceFile):
            pass
        else:
            error += "wrong source \n"            
        if self.cuttingFile!="":
            pass
        else:
            error += "empty tasks \n"
        if self.checkdir(self.targetDir):
            pass
        else:
            error += "wrong target dir \n"        
            
        if error == "error\n":                        
            i = 0    
            tmp_text = "ready to start\n"
            for stroke in self.prepareTask():
                tmp_text += stroke[0]['track_name']+" "+stroke[0]['track_lenght']+"\n"
            self.info.update(tmp_text)
            return True
        else:       
            self.info.update(error)
            return False

    def prepareTask(self):
        import re, os
        import ffmpy
        maker = []
        tr = 1
        #f = open(self.cuttingFile)
        f = self.cuttingFile.split("\n")
        full_lenght = (os.popen(r'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 '+str(self.sourceFile).replace(' ', '\ ')+'').read())[:-8]     
        for track in f:
            result = re.findall('\d{,2}:*\d{,2}:\d{,2}', track)
            if result!=None and result!=[]:
                start_time = self.secondsCreate(result[0])
                maker.append([{"start_time":result[0],"track_name":str(tr)+"."+([x for x in track.split(result[0]) if x][0][:-2])+str(".mp3"),"track_lenght":"0"}])
                tr += 1
                if start_time!=0:
                    maker[len(maker)-2][0]['track_lenght'] = self.tracktimeCreate(int(start_time) - int(self.secondsCreate(maker[len(maker)-2][0]['start_time'])))
                    maker[len(maker)-1][0]['track_lenght'] = self.tracktimeCreate(int(full_lenght) - int(self.secondsCreate(maker[len(maker)-1][0]['start_time'])))
        return maker
    
    def checkfile(self,file_path):
        import os
        return True if os.path.isfile(file_path) else False
        
    def checkdir(self,dir_path):
        import os
        return True if os.path.isdir(dir_path) else False
    
    def secondsCreate(self,trackTime):
        return sum(map(lambda a:a[0]*a[1],zip([1,60,3600],map(int,reversed(trackTime.split(":"))))))
        
    def tracktimeCreate(self,seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d" % (h, m, s)
    
    def addTarget(self,target):
        import os
        if self.checkfile(target)==True:
            try:
                os.remove(target)
                return True
            except:
                self.info.insert("cant add task "+target+"\n")
                return False
        else:
            return True
        
    def worker(self):
        while True:
            task = self.q.get()
            self.calc(task) 
            self.q.task_done()

    def calc(self,values):
        from ffmpy import FFmpeg
        source = values[0]
        target = values[1]
        cmd = values[2]
        song_name = values[3]
        ff = FFmpeg(
            inputs={source: cmd},
            outputs={target: None }
        )
        self.info.find_and_set(song_name + " waiting...\n", song_name + " started\n")
        ff.run()
        self.info.find_and_set(song_name + " started\n", song_name + " done\n")
    
    def cutInThread(self):
        import threading
        from datetime import datetime
        self.info.clear()
        self.info.insert("jobs started at "+str(datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")+"\n"))
        for task in self.prepareTask():
            target = self.targetDir + "/"+task[0]['track_name']
            if self.addTarget(target):
                pass
            else:
                continue
            cmd = "-loglevel quiet -ss "+task[0]['start_time']+" -t "+task[0]['track_lenght']
            song_name = task[0]['track_name']
            put_task = [self.sourceFile,target,cmd,song_name,song_name]
            self.info.insert(song_name + " waiting...\n")
            self.q.put(put_task)
        for i in range(4):
            thread = threading.Thread(target=self.worker)
            thread.daemon = True 
            thread.start()
            
    def startConverting(self,sourceFile=False, targetDir=False,cuttingFile=False):
        if sourceFile!=False and targetDir!=False and cuttingFile!=False:
            self.refreshPaths(sourceFile,targetDir,cuttingFile)
        if self.checkIsExists()==True:
            self.cutInThread()
