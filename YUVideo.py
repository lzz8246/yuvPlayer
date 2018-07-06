import os
from PIL import Image
import numpy as np
from numpy import uint8
from numpy import fromfile
from numpy import zeros, repeat
import cv2


class YUVideo(object):

	def __init__(self, videoFile, videoSize,framerate):
		self.vf = videoFile
		self.width = videoSize[0]
		self.height = videoSize[1]
		self.fps=framerate
		self.blkSize = self.width * self.height * 3 // 2
		fileSize = os.path.getsize(videoFile)
		self.frmCount = fileSize // self.blkSize
		self.videoData=[]

	def open(self):
		self.fp = open(self.vf, 'rb')
		self.videoData=np.fromfile(self.vf,np.uint8,-1)


	def close(self):
		self.fp.close()

	def getYuvFrm(self, frmnum):
		halfWidth = self.width // 2
		halfHeight = self.height // 2
		sizeuv = self.width * self.height // 4
		offset=self.blkSize * frmnum
		y = self.videoData[offset:(offset+self.width*self.height)].reshape(self.height,self.width)
		u = self.videoData[(offset+self.width*self.height):(offset+self.width*self.height + sizeuv)].reshape(halfHeight,halfWidth)
		v = self.videoData[(offset+self.width*self.height + sizeuv):(offset+self.width*self.height + 2*sizeuv)].reshape(halfHeight,halfWidth)
		return (y, u, v)
		###the below is the version get frame from the file while the above first load all data into memories
		#self.fp.seek(self.blkSize * frmnum, 0)
		#y = fromfile(self.fp, uint8, self.width * self.height).reshape(self.width, self.height)
		#u = fromfile(self.fp, uint8, halfWidth * halfHeight).reshape(halfWidth, halfHeight)
		#v = fromfile(self.fp, uint8, halfWidth * halfHeight).reshape(halfWidth, halfHeight)
		#return (y, u, v)

	def yuv2rgb(self, y, u, v):
		u=cv2.resize(u,(self.width,self.height))
		v=cv2.resize(v,(self.width,self.height))
		yuv = np.dstack((y,u,v))
		rgb=cv2.cvtColor(yuv,cv2.COLOR_YCrCb2RGB)
		return rgb
		###the below is the version without opencv, but the processing speed is much slower
		#subSampleMat = np.array([(1,1),(1,1)])
		#u = np.kron(u, subSampleMat)
		#v = np.kron(v, subSampleMat)
		#v=misc.imresize(v,(self.height,self.width),"bilinear",mode="F")

		#y = y.astype(np.float)-16
		#u = u.astype(np.float)
		#v = v.astype(np.float)
		#r = 1.1644*y + 1.596 * (v - 128.0)+0.5
		#r[r<0]=0
		#r[r>255]=255
		#g = 1.1644*y - 0.3918 * (u - 128.0) - 0.813 * (v - 128.0)+0.5
		#g[g<0]=0
		#g[g>255]=255
		#b = 1.1644*y + 2.0172 * (u - 128.0)+0.5
		#b[b<0]=0
		#b[b>255]=255
		#rgb = (r.astype(uint8), g.astype(uint8), b.astype(uint8))
		#return rgb

	def getFrm(self, frmnum):
		if frmnum >= self.frmCount:
			frmnum = self.frmCount -1
			print('the last frame')
		if frmnum < 0:
			frmnum = 0
			print('the first frame')
		
		(y, u, v) = self.getYuvFrm(frmnum)
		img=self.yuv2rgb(y, u, v)
		#(r, g, b) = self.yuv2rgb(y, u, v)
		#imgr=Image.fromarray(r)
		#imgg=Image.fromarray(g)
		#imgb=Image.fromarray(b)
		#img = Image.merge('RGB', (imgr, imgg, imgb))
		#img=Image.fromarray(img)
		return img
