import re
import shlex
cueFile = ("/home/user/Downloads/Eject Project - Real Time/Eject Project - Real Time.cue")
sourcePath = ("/home/user/Downloads/Eject Project - Real Time/Eject Project - Real Time.ape")

print "!!!!!!!!!!!!!!!!!!!!!!"
print cueFile

tracks = (open(cueFile,"r").read()).split("TRACK")

full_lenght = shlex.escape(sourcePath)


#print full_lenght
maker = []
#del tracks[0]
for track in tracks:
    for data in track.split("\r\n"):
        if data.find("INDEX")!=-1:
            pass
            #print "INDEX -> "+str(re.findall('\d{,2}:*\d{,2}:\d{,2}', data)[0])
        if data.find("TITLE")!=-1:
            pass
            #print "TITLE -> "+str(re.findall('".{,}."', data)[0])[1:-1]
            
        
#print maker