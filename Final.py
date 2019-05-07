#Run for recently downloaded file
import cv2
from darkflow.net.build import TFNet
import numpy as np
import time
import array
import os
from pytube import YouTube
url = raw_input("enter URL of video to download")
try:
	vid = YouTube(url).streams.first().download('/home/yash/darkflow-master/videos/')
except:
	print "Error"
print "Video Downloaded Successfully"

option = {
    'model': 'cfg/yolo.cfg',
    'load': 'bin/yolo.weights',
    'threshold': 0.5,
    #'gpu': 1.0
}
#default yolo weights
"""option = {
    'model': 'cfg/tiny-yolo-voc-sports.cfg',
    'load': 1250,
    'threshold': 0.1
    #'gpu': 1.0
} trained yolo weights"""


tfnet = TFNet(option)
capture = cv2.VideoCapture(vid)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
frame_width = int( capture.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height =int( capture.get(cv2.CAP_PROP_FRAME_HEIGHT)) 
out = cv2.VideoWriter('outputs/output4.mp4',fourcc,2.0, (frame_width,frame_height)) # 5.0 is use to give speed by which video will save 
colors = [tuple(255 * np.random.rand(3)) for i in range(10)]

f = open("lcfile.txt","w")

def getFrame(sec):
	capture.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
	hasFrames,image = capture.read()
	return hasFrames   #to retrieve frame after specific interval from video 

sec = 0
frameRate = 1 ##it will capture image in each 1 second
frame = getFrame(sec)

while (capture.isOpened()):
    sec = sec + frameRate
    sec = round(sec, 2)
    frame = getFrame(sec)
    stime = time.time()
    arrlabel = []
    coordinates = []
    framecolor=[]
    ret, frame = capture.read()
    if ret:
	results = tfnet.return_predict(frame)
	for color, result in zip(colors, results):
	    tl = (result['topleft']['x'], result['topleft']['y'])#use to plot rectangle
	    br = (result['bottomright']['x'], result['bottomright']['y'])#use to plot rectangle
	    label = result['label']
	    coordinates.append(tl)
	    coordinates.append(br)
	    arrlabel.append(label)
	    framecolor.append(color)
	    frame = cv2.rectangle(frame, tl, br, color, 7)
	    frame = cv2.putText(frame, label, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
	    print arrlabel
	    print "\n"
	    print coordinates
	    print "\n"
	    with open("lcfile.txt","a") as f:
		for item in arrlabel:
			f.write("{}".format(item))
			f.write(",")
		for item in framecolor:
			f.write("{}".format(item))
			f.write(",")
		for item in coordinates:
			f.write("{}\t".format(item))
	    f.close()
	cv2.imshow('frame', frame)
	out.write(frame)

	#this code for removing brackets and saving output in text file
	with open("lcfile.txt",'r') as f:
		text = f.read()
		text = text.replace("(","")
		text = text.replace(")\t",",")
		text = text.replace(",","\n")
		text = text.replace(")","")
		text = text.replace(" ","")
	with open("lcfile.txt",'w') as ff:
		ff.write(text)	
	f.close()
	ff.close()

	print('FPS {:.1f}'.format(1 / (time.time() - stime)))
	if cv2.waitKey(1) & 0xFF == ord('q'):
	    break
    else:
	capture.release()
	out.release()
	cv2.destroyAllWindows()
	break

with open('lcfile.txt','r') as fp:
	lines = fp.readlines()
	eof = len(lines)

i=0
cnt = 0
cnt1 = 0
cnt2 = 0
flabellist = []
fcolorlist = []
fcolist = []
slabellist = []
scolist = []
scolorlist = []
extension = '.txt'
outputtextfile = vid+extension
with open(outputtextfile,'w') as fopen :
	class guessposition :

		def firstlist(obj,i): 
			cnt = i
			for element in lines :
				first = lines[i]
				first = first.strip()
				if first.isalpha():
					flabellist.append(first)
					i+= 1
					cnt+= 1	
				elif first.isdigit():
					fcolist.append(first)
					i+=1
					if i == eof :
						break
					else :
						check = lines[i]
						check = check.strip()
						if check.isalpha() :
							break
					cnt+= 1

				else :
					fcolorlist.append(first)
					i+= 1
					cnt+= 1
			return cnt

		def secondlist(obj,i) :
			cnt1 = i
			for j in lines :
				first = lines[i]
				first = first.strip()
				if first.isalpha():
					slabellist.append(first)
					i+= 1
					cnt1+= 1	
				elif first.isdigit():
					scolist.append(first)
					i+=1
					if i == eof :
						break
					else :
						check = lines[i]
						check = check.strip()
						if check.isalpha() :
							break
					cnt1+= 1
				else :
					scolorlist.append(first)
					i+= 1
					cnt1+= 1	
			return cnt1
		def rgb_to_hex(obj,red,green,blue) :
			return '#%02x%02x%02x' % (red,green,blue)				

		def compareframes(obj) :
			for j in range(len(flabellist)):
				for k in range(len(slabellist)):
					if flabellist[j] == slabellist[k]:
						indexfirst=j
						indexsecond=k
						item = flabellist[indexfirst]
						if fcolorlist[3*indexfirst]== scolorlist[3*indexsecond] and fcolorlist[(3*indexfirst)+1]== scolorlist[(3*indexsecond)+1] and fcolorlist[(3*indexfirst)+2] == scolorlist[(3*indexsecond)+2] :
							r = fcolorlist[3*indexfirst]
							r = r.strip()
							r = float(r)
							r = round(r)
							g = fcolorlist[3*indexfirst+1]
							g = g.strip()
							g = float(g)
							g = round(g)
							b = fcolorlist[3*indexfirst+2]
							b = b.strip()
							b = float(b)
							b = round(b)
							hexcol = obj.rgb_to_hex(int(r),int(g),int(b))
							if int(scolist[4*indexsecond])-int(fcolist[4*indexfirst])>50:
								if int(scolist[(4*indexsecond)+2])-int(fcolist[(4*indexfirst)+2])>50:
									if int(fcolist[(4*indexfirst)+1])-int(scolist[(4*indexsecond)+1])>50:
										fopen.write("{} with {} framecolor is moved forward in right direction\n".format(item,hexcol))
									else :
										fopen.write("{} with {} framecolor is moved in right direction\n".format(item,hexcol))
								elif int(fcolist[(4*indexfirst)+2])-int(scolist[(4*indexsecond)+2])>50:
									fopen.write("{} with {} framecolor is moved backward\n".format(item,hexcol))
								else :
									fopen.write("{} with {} framecolor is moved a little in right direction\n".format(item,hexcol))
							elif int(fcolist[4*indexfirst])-int(scolist[4*indexsecond])>50:
								if int(fcolist[(4*indexfirst)+2])-int(scolist[(4*indexsecond)+2])>50:
									if int(fcolist[(4*indexfirst)+1])-int(scolist[(4*indexsecond)+1])>50:
										fopen.write("{} with {} framecolor is moved forward in left direction\n".format(item,hexcol))
									else :
										fopen.write("{} with {} framecolor is moved in left direction\n".format(item,hexcol))
								elif int(scolist[(4*indexsecond)+2])-int(fcolist[(4*indexfirst)+2])>50:
									fopen.write("{} with {} framecolor is moved forward\n".format(item,hexcol))
								else :
									fopen.write("{} with {} framecolor is moved a little in left direction\n".format(item,hexcol))
							elif int(scolist[4*indexsecond])-int(fcolist[4*indexfirst])==0:
								fopen.write("{} with {} framecolor is stable\n".format(item,hexcol))
							else :
								fopen.write("{} with {} framecolor is moved slightly\n".format(item,hexcol))


		def result(obj,i) :
			count = obj.firstlist(i)
			count2 = obj.secondlist(count+1)
			itr = obj.compareframes()
			if count2 < eof-1 :
				flabellist[:]=[]
				fcolist[:]=[]
				slabellist[:]=[]
				scolist[:]=[]
				fcolorlist[:]=[]
				scolorlist[:]=[]
				obj.result(count+1)
			else :
				print 'all frames are traversed'
				print '========================================================'


	obj = guessposition()
	obj.result(i)

#following code to remove same action one after other
with open(outputtextfile,"r") as fp :
	mainlines = fp.read().split(' ')
	for item in mainlines:
		if item[0] == '#':
			framecolor.append(item)
with open(outputtextfile,"r") as fp :
	totallines = fp.readlines()
	def duplicate(h,k):
		if k== len(totallines):
			return totallines
			exit()
		if framecolor[h]==framecolor[k]:
			if totallines[h]==totallines[k]:
				totallines.pop(k)
				framecolor.pop(k)
				if h+1 == k:
					if k+1 < len(totallines):
						duplicate(h+1,k+1)
					else:
						if totallines[h]==totallines[k]:
							totallines.pop(k)
						return totallines
						exit()
				elif h == len(totallines)-1:
					return totallines
					exit()
				else:
					duplicate(h+1,k)
			else:
				duplicate(h+1,k+1)
		
		else :
			if k+1== len(totallines):
				return totallines
				exit()
			else :
				duplicate(h,k+1)
duplicate(0,1)	
with open(outputtextfile,"w") as fp :
	for item in totallines :
		fp.write(item)	
