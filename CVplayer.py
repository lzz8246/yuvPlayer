from YUVideo import YUVideo
import cv2
import time
import tkinter as tk
from createFileData import yuvFile
import numpy as np
from PIL import ImageTk 
import os
import screeninfo

class initWindow:
	def __init__(self,mainWin):
		self.mainWin=mainWin
		self.initComponent()
	def initComponent(self):
		self.mainWin.bind('<Return>',self.keyReturn)
		
		self.LabelInfo=tk.Label(self.mainWin,text='please enter your name in English')
		self.EntryName=tk.Entry(self.mainWin)
		self.BtnOK=tk.Button(self.mainWin,text='Ok',command=self.ensure)
		self.LabelInfo.pack()
		self.EntryName.pack()
		self.BtnOK.pack()
	def keyReturn(self,event):
		self.ensure()
	def ensure(self):
		self.userName=self.EntryName.get()
		if self.userName=='':
			return
		else:
			#playMainWin=mainWindow(self.mainWin,self.fileList)
			self.mainWin.quit()
			self.mainWin.destroy()

class mainWindow:
	def __init__(self,mainWin,fileList):
		self.mainWin=mainWin
		self.fileList=fileList
		initWin=tk.Toplevel()
		initWin.resizable(0,0)
		initWin.attributes("-toolwindow", 1)
		initWin.wm_attributes("-topmost", 1)
		self.initWin=initWindow(initWin)
		initWin.mainloop()
		
		self.userName=self.initWin.userName
		if not os.path.exists('./result/'):
			os.mkdir('./result/')
		self.resultFilePath=os.path.join('./result/',self.userName+'.txt')
		self.resultFid=open(self.resultFilePath,'w')
		#self.userName=userName
		self.iFile=0
		self.Scores=np.zeros(len(fileList))
		self.currScore=1
		self.initComponent()
	def initComponent(self):
		
		self.mainWin.bind("<Left>",self.keyLeft)
		self.mainWin.bind("<Right>",self.keyRight)
		self.mainWin.bind("<space>",self.keySpace)
		
		self.FrameTitle=tk.Frame(self.mainWin,bd=1,width=520,height=25)
		self.FrameTitle.pack_propagate(0)
		self.LabelTitle=tk.Label(self.FrameTitle,text='press left or right to select score ')
		self.FrameStar=tk.Frame(self.mainWin,width=520,height=100)
		self.FrameStar.pack_propagate(0)
		
		self.ImgStarOn=ImageTk.PhotoImage(file = './imgs/starOn.png',size=(100,100))
		self.ImgStarOff=ImageTk.PhotoImage(file = './imgs/starOff.png',size=(100,100))
		self.LabelStars=[]
		
		self.LabelStar1=tk.Label(self.FrameStar,width=100,image=self.ImgStarOn)
		self.LabelStars.append(self.LabelStar1)
		self.LabelStar2=tk.Label(self.FrameStar,width=100,image=self.ImgStarOff)
		self.LabelStars.append(self.LabelStar2)
		self.LabelStar3=tk.Label(self.FrameStar,width=100,image=self.ImgStarOff)
		self.LabelStars.append(self.LabelStar3)
		self.LabelStar4=tk.Label(self.FrameStar,width=100,image=self.ImgStarOff)
		self.LabelStars.append(self.LabelStar4)
		self.LabelStar5=tk.Label(self.FrameStar,width=100,image=self.ImgStarOff)
		self.LabelStars.append(self.LabelStar5)
		
		self.FrameScoreBtn=tk.Frame(self.mainWin,width=520,height=30)
		#self.FrameScoreBtn.pack_propagate(0)
		
		self.btnPlus=tk.Button(self.FrameScoreBtn,width=10,text='+',command=self.ScorePlus)
		self.btnMinus=tk.Button(self.FrameScoreBtn,width=10,text='-',command=self.ScoreMinus)
		
		self.btnPlay=tk.Button(self.mainWin,text='next',command=self.playNext)
		self.FrameTitle.pack()
		self.LabelTitle.pack()
		self.FrameStar.pack()
		self.LabelStar1.pack(side='left')
		self.LabelStar2.pack(side='left')
		self.LabelStar3.pack(side='left')
		self.LabelStar4.pack(side='left')
		self.LabelStar5.pack(side='left')
		self.FrameScoreBtn.pack()
		self.btnMinus.pack(side='left')
		self.btnPlus.pack(side='left')

		self.btnPlay.pack()
	
	def keyLeft(self,event):
		self.ScoreMinus()
	
	def keyRight(self,event):
		self.ScorePlus()
		
	def keySpace(self,event):
		if self.iFile>0:
			self.Scores[self.iFile-1]=self.currScore
		self.playNext()
	
	def ScorePlus(self):
		self.currScore=self.currScore+1
		if self.currScore==6:
			self.currScore=1
		for i in range(self.currScore):
			self.LabelStars[i].configure(image=self.ImgStarOn)
		for i in range(4,self.currScore-1,-1):
			self.LabelStars[i].configure(image=self.ImgStarOff)
		
	def ScoreMinus(self):
		self.currScore=self.currScore-1
		if self.currScore==0:
			self.currScore=5
		for i in range(self.currScore):
			self.LabelStars[i].configure(image=self.ImgStarOn)
		for i in range(4,self.currScore-1,-1):
			self.LabelStars[i].configure(image=self.ImgStarOff)
			
	def playNext(self):
		if self.iFile<len(self.fileList):
			yuvFile=self.fileList[self.iFile]
			self.play(yuvFile)
			self.iFile=self.iFile+1
		else:
			self.LabelTitle.configure(text='the last video')
			print(self.Scores)
			self.resultFid.write(str(self.Scores))
			self.resultFid.close()
			self.mainWin.quit()
			
	#frame by frame
	def play2(self,yuvFile):
		yuv2play=YUVideo(yuvFile.fname, yuvFile.size,yuvFile.fps)
		yuv2play.open();
		screen = screeninfo.get_monitors()[0]
		cv2.namedWindow('lena',cv2.WINDOW_AUTOSIZE)
		cv2.moveWindow('lena', screen.x - 1, screen.y - 1)
		#cv2.setWindowProperty('lena', cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
		#cv2.namedWindow('lena',cv2.WND_PROP_FULLSCREEN)
		print(time.time())
		for i in range(yuv2play.frmCount):
			begin = time.time()
			img = yuv2play.getFrm(i)
			cv2.imshow('lena',img)
			duration = time.time() - begin
			#print(duration)
			offset = 1/float(yuv2play.fps) - duration
			#print(offset)
			if offset>0:
				k=cv2.waitKey(int(offset*840+0.5))
				#k=cv2.waitKey(1)
		cv2.destroyAllWindows()
		print(time.time())
		
	#play by time
	def play(self,yuvFile):
		yuv2play=YUVideo(yuvFile.fname, yuvFile.size,yuvFile.fps)
		yuv2play.open();
		screen = screeninfo.get_monitors()[0]
		cv2.namedWindow('lena',cv2.WINDOW_AUTOSIZE)
		cv2.moveWindow('lena', screen.x - 1, screen.y - 1)
		print(time.time())
		begin=time.time()
		while True:
			offset=time.time()-begin
			#calculate the frame num
			frameNum=int(offset//(1/yuv2play.fps))
			if frameNum>yuv2play.frmCount:
				break
			img = yuv2play.getFrm(frameNum)
			cv2.imshow('lena',img)
			k=cv2.waitKey(1)
		cv2.destroyAllWindows()
		print(time.time())
		
if __name__=="__main__":
	fileList=np.load('test.npz')
	fileList=fileList['yuvList']
	win=tk.Tk();
	playMainWin=mainWindow(win,fileList)
	#win.attributes("-toolwindow", 1)
	#win.wm_attributes("-topmost", 1)
	win.mainloop()

"""
fName="D:/coding/HM_WEIGAO/bin/vc10/x64/Release/BasketballPass_416x240_50.yuv"
videoSize=(416,240)
fps=50
yuv2play=YUVideo(fName, videoSize,fps)
yuv2play.open();

cv2.namedWindow('lena',cv2.WINDOW_AUTOSIZE)

print(time.time())
for i in range(yuv2play.frmCount):
	#print(i)
	begin = time.time()
	#print(begin)
	img = yuv2play.getFrm(i)
	cv2.imshow('lena',img)
	#print(time.time())
	druation = time.time() - begin
	offset = 1.0/float(yuv2play.fps) - druation
	if offset>0:
		k=cv2.waitKey(int(offset*840))
print(time.time())

"""














"""
fName="E:/coding_0208/HEVC-full-sequence/HEVCCLASSE/KristenAndSara_1280x720_60.yuv"
videoSize=(1280,720)
fps=50
yuv2play=YUVideo(fName, videoSize,fps)
yuv2play.open();

cv2.namedWindow('lena',cv2.WINDOW_AUTOSIZE)


for i in range(yuv2play.frmCount):
	begin = time.time()
	img = yuv2play.getFrm(i)
	cv2.imshow('lena',img)
	druation = time.time() - begin
	offset = 1/float(yuv2play.fps) - druation
	if offset>0:
		k=cv2.waitKey(int(offset*1000))
"""