class RollCase(object):
    def __init__(self,sourceDir,targetDir, info):
        from Queue import Queue
        self.sourceDir = sourceDir
        self.targetDir = targetDir
        """
        self.cuttingFile = cuttingFile
        self.sourceFile = sourceFile
        self.targetDir = targetDir
        """
        self.info = info
        self.q = Queue()
        
    def getTargetFiles(self):
        from os import listdir
        from os.path import isfile, join
        import re
        onlyfiles = [f for f in listdir(self.sourceDir) if re.findall("\.flac$",(join(self.sourceDir, f)))!=[]]
        print self.sourceDir
        return onlyfiles
        
    def checkdir(self,dir_path):
        import os
        return True if os.path.isdir(dir_path) else False
        
    def checkfile(self,file_path):
        import os
        return True if os.path.isfile(file_path) else False

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
    
    def refreshPaths(self,sourceDir,resultPath):
        self.sourceDir = sourceDir
        self.targetDir = resultPath
        self.checkIsExists()
    
    def cutInThread(self):
        from datetime import datetime
        self.info.clear()
        self.info.insert("jobs started at "+str(datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")+"\n"))
        import threading
        for task in self.getTargetFiles():
            target = self.targetDir + "/"+task.split("flac")[0]+"mp3"
            if self.addTarget(target):
                pass
            else:
                continue
            source = self.sourceDir+"/"+task
            cmd = " -loglevel quiet "
            song_name = task
            put_task = [source,target,cmd,song_name]
            self.info.insert(song_name + " waiting...\n")
            self.q.put(put_task)
        for i in range(4):
            thread = threading.Thread(target=self.worker)
            thread.daemon = True 
            thread.start()
            
    def checkIsExists(self,sourceDir=False,resultPath=False):        
        error = "error\n"
        if sourceDir!=False and resultPath!=False:
            self.refreshPaths(sourceDir,resultPath)
        if self.checkdir(self.targetDir):
            pass
        else:
            error += "wrong target dir \n"
            
        if self.checkdir(self.sourceDir):
            pass
        else:
            error += "wrong source dir \n"
            
        if error == "error\n":                        
            i = 0    
            tmp_text = "ready to start\n"
            for stroke in self.getTargetFiles():
                tmp_text += stroke + "\n"
            self.info.update(tmp_text)
            return True
        else:       
            self.info.update(error)
            return False
            
    def startConverting(self,sourceDir=False,resultPath=False):
        if sourceDir!=False and resultPath!=False:
            self.refreshPaths(sourceDir,resultPath)
        if self.checkIsExists()==True:
            self.cutInThread()
