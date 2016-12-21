class RollCase(object):
    def __init__(self,sourceFile,targetDir,cuttingFile,info):
        from Queue import Queue
        self.sourceFile = sourceFile
        self.targetDir = targetDir
        self.cuttingFile = cuttingFile
        self.info = info
        self.q = Queue()
    
    def checkIsExists(self):        
        if self.checkfile(self.sourceFile) and self.checkfile(self.cuttingFile) and self.checkdir(self.targetDir):
            i = 0    
            tmp_text = ""
            for stroke in self.prepareTask():
                i+=1
                tmp_text += str(i)+stroke[0]['track_name']+" "+stroke[0]['track_lenght']+"\n"
            self.info.update(tmp_text)
            return True
        else:
            tmp_text = "error"        
            self.info.update(tmp_text)
            return False

    def prepareTask(self):
        import re, os
        import ffmpy
        maker = []
        f = open(self.cuttingFile)
        full_lenght = (os.popen(r'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 '+str(self.sourceFile).replace(' ', '\ ')+'').read())[:-8]     
        for track in f:
            result = re.findall('\d{,2}:*\d{,2}:\d{,2}', track)
            if result!=None:
                start_time = self.secondsCreate(result[0])
                maker.append([{"start_time":result[0],"track_name":[x for x in track.split(result[0]) if x][0][:-1],"track_lenght":"0"}])
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
        tmp_text = song_name + " started...\n"
        self.info.insert(tmp_text)
        ff.run()
        self.info.find_and_set(tmp_text, song_name + " done\n")
    
    def cutInThread(self):
        import threading
        for task in self.prepareTask():
            cmd = "-loglevel quiet -ss "+task[0]['start_time']+" -t "+task[0]['track_lenght']
            target = self.targetDir + "/"+task[0]['track_name']+".mp3"
            song_name = task[0]['track_name']+".mp3"
            put_task = [self.sourceFile,target,cmd,song_name,song_name]
            self.q.put(put_task)
        for i in range(4):
            thread = threading.Thread(target=self.worker)
            thread.daemon = True 
            thread.start()
            
    def startConverting(self):
        if self.checkIsExists()==True:
            self.cutInThread()
        