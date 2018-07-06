import numpy as np

class yuvFile:
	def __init__(self,fname,size,fps):
		self.fname=fname
		self.size=size
		self.fps=fps

if __name__ =="__main__":
	fileList=['D:/coding/HM_WEIGAO/bin/vc10/x64/Release/BasketballPass_416x240_50.yuv','E:/coding_0208/HEVC-full-sequence/HEVCCLASSE/KristenAndSara_1280x720_60.yuv']
	sizes=[(416,240),(1280,720)]
	fpss=[50,60]
	sizeDict={}
	fpsDict={}
	yuvList=[]
	i=0;
	for file in fileList:
		yuvList.append(yuvFile(file,sizes[i],fpss[i]))
		i=i+1
	
	np.savez('test.npz',yuvList=yuvList)