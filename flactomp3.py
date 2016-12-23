class RollCase(object):
    def __init__(self,sourceFile,targetDir,cuttingFile,info):
        import re
        import shlex
        self.cuttingFile = ("/home/user/Downloads/Eject Project - Real Time/Eject Project - Real Time.cue")
        self.sourceFile = ("/home/user/Downloads/Eject Project - Real Time/Eject Project - Real Time.ape")
        self.targetDir = targetDir
        self.info = info
        #self.q = Queue()
        
    def parceCue(self):
        tracks = (open(cueFile,"r").read()).split("TRACK")
        del tracks[0]
        maker = []        
        f = open(self.cuttingFile)
        full_lenght = (os.popen(r'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 '+str(self.sourceFile).replace(' ', '\ ')+'').read())[:-8]     
        title = []
        time_vector = []
        for track in tracks:
            start_time = ""
            for data in track.split("\n\r"):
                if data.find("INDEX")!=-1:
                    start_time = self.tracktimeCreate(int(self.getSeconds(re.findall('\d{,2}:*\d{,2}:\d{,2}', data)[0])))
                    time_vector.append(start_time)
                if data.find("TITLE")!=-1:
                    title.append((re.findall('TITLE ".{,99}"',data)[0]).replace("TITLE \"","")[:-1])
        time_vector.append(self.tracktimeCreate(int(full_lenght)))
        for i in xrange(int(len(time_vector))):
            if i!=0:
                #print str(self.tracktimeCreate(self.secondsCreate(time_vector[i]) - self.secondsCreate(time_vector[i-1])))
                maker.append([{"start_time":time_vector[i-1],"track_name":title[i-1],"track_lenght":str(self.tracktimeCreate(self.secondsCreate(time_vector[i]) - self.secondsCreate(time_vector[i-1])))}])
        print maker
                
    def getSeconds(self,val):
        return str(int(val.split(":")[0])*60+int(val.split(":")[1]))
        
    def secondsCreate(self,trackTime):
        return sum(map(lambda a:a[0]*a[1],zip([1,60,3600],map(int,reversed(trackTime.split(":"))))))
        
    def tracktimeCreate(self,seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d" % (h, m, s)
        
case = RollCase("","","","")
case.parceCue()