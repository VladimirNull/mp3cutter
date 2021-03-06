class RollCase(object):
    def __init__(self,sourceFile,targetDir,cuttingFile,info):
        from Queue import Queue
     
        self.cuttingFile = cuttingFile
        self.sourceFile = sourceFile
        self.targetDir = targetDir
        """
        self.cuttingFile = cuttingFile
        self.sourceFile = sourceFile
        self.targetDir = targetDir
        """
        self.info = info
        self.q = Queue()
    
    def refreshPaths(self,sourceFile,targetDir,cuttingFile):
        self.cuttingFile = cuttingFile
        self.sourceFile = sourceFile
        self.targetDir = targetDir
        self.checkIsExists()
        
    def parceCue(self):
        import re,os
        tracks = (open(self.cuttingFile,"r").read()).split("TRACK")
        del tracks[0]
        maker = []        
        f = open(self.cuttingFile)
        full_lenght = (os.popen(r'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 '+str(self.sourceFile).replace(' ', '\ ')+'').read())[:-8]     
        title = []
        tr = 0
        time_vector = []
        for track in tracks:
            start_time = ""
            for data in track.split("\n\r"):
                if data.find("INDEX")!=-1:
                    start_time = self.tracktimeCreate(int(self.getSeconds(re.findall('\d{,2}:*\d{,2}:\d{,2}', data)[0])))
                    time_vector.append(start_time)
                if data.find("TITLE")!=-1:
                    tr += 1                  
                    title.append(str(tr)+"."+(re.findall('TITLE ".{,99}"',data)[0]).replace("TITLE \"","")[:-1]+str(".mp3"))
        time_vector.append(self.tracktimeCreate(int(full_lenght)))
        for i in xrange(int(len(time_vector))):
            if i!=0:
                #print str(self.tracktimeCreate(self.secondsCreate(time_vector[i]) - self.secondsCreate(time_vector[i-1])))
                maker.append([{"start_time":time_vector[i-1],"track_name":title[i-1],"track_lenght":str(self.tracktimeCreate(self.secondsCreate(time_vector[i]) - self.secondsCreate(time_vector[i-1])))}])
        return maker
        
    def addTarget(self,target):
        import os
        if self.checkfile(target)==True:
            try:
                os.remove(target)
                self.info.insert("old file "+target+" removed \n")
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
        from datetime import datetime
        self.info.clear()
        self.info.insert("jobs started at "+str(datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")+"\n"))
        import threading
        for task in self.parceCue():
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
                
    def getSeconds(self,val):
        return str(int(val.split(":")[0])*60+int(val.split(":")[1]))
        
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
        
    def checkIsExists(self,sourceFile=False, targetDir=False, cuttingFile=False):
        if sourceFile!=False and targetDir!=False and cuttingFile!=False:
            self.refreshPaths(sourceFile,targetDir,cuttingFile)
        
        error = "error\n"
        if self.checkfile(self.sourceFile):
            pass
        else:
            error += "wrong source \n"            
        if self.checkfile(self.cuttingFile):
            pass
        else:
            error += "wrong cue \n"
        if self.checkdir(self.targetDir):
            pass
        else:
            error += "wrong target dir \n"        
            
        if error == "error\n":                        
            i = 0    
            tmp_text = "ready to start\n"
            for stroke in self.parceCue():
                tmp_text += stroke[0]['track_name']+" "+stroke[0]['track_lenght']+"\n"
            self.info.update(tmp_text)
            return True
        else:       
            self.info.update(error)
            return False
            
    def startConverting(self,sourceFile=False, targetDir=False, cuttingFile=False):
        if sourceFile!=False and targetDir!=False and cuttingFile!=False:
            self.refreshPaths(sourceFile,targetDir,cuttingFile)
        if self.checkIsExists()==True:
            self.cutInThread()