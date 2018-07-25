import cv2
import numpy as np
import glob
import csv
import os
import shutil	#can delete the folder and all the files under this folder
''''''
#library written by yentse
#import str2list.py
''''''

def str2list(text, sp):
	_list = []
	a = ''
	rowNum = 0
	for row in text:
		_list.append([])
		for ch in row:
			if(ch not in sp):
				a += ch
			else:
				_list[rowNum].append(a)
				a = ''
		rowNum += 1
	return _list
			

#the path where this python code exists
path = os.path.abspath('.')		

#if folder(name:output) exists, delete it
#shutil.rmtree : delete all the files in the folder, and also delete this folder
if os.path.isdir(path+'/output'):	
	shutil.rmtree(path+'/output')	

#list all the files(inculde folder) under the path
folderlist = glob.glob(path+'/*')
print(folderlist)

#create folder, name output
os.makedirs(path+'/output')
#init first number of each line in the .txt, means the frame num that have labeled
#output file name : outname
num = ''
outname = 0

#scan folder under the path
for folder in folderlist:
	
	#list all the .txt in this folder
	files = glob.glob(folder+'/*.txt')

	#scan .txt
	for fpath in files:
		
		#vapath : the video's path corresponding to the .txt
		vpath = fpath.replace('_gt.txt', '.mp4')
		
		#open .txt
		f = open(fpath, 'r', encoding = 'big5')
		#read .txt
		text = f.readlines()
		f.close()
		
		#scan line
		for l in text:
			c = 0
			#scan character
			for i in l:		#find the first number(frame) in the txt
				if i != ',':
					num += i
					c += 1
				else:
					break
			#we want to change the frame number of each lines
			#in order to make it corresponding to the new video(output.mp4) we make 
			ll = l[c+1:]
			text_file = open(path+'/output/'+str(outname)+'.txt', 'w')	#output .txt
			text_file.write(str(outname) + ',' + ll)
			text_file.close()

			#open video
			cap = cv2.VideoCapture(vpath)	#output .jpg
			#set to the specific frame
			cap.set(1, int(num))
			#ret??, frame is an list of the photo imformation
			ret, frame = cap.read()
			#save new photo, name:  ex. 0.jpg
			cv2.imwrite(path+'/output/'+str(outname)+'.jpg', frame)
			#release the memory?
			cap.release()
			#name the photo, 0.jpg, 1.jpg, 2.jpg, 3.jpg ...
			outname += 1
			num = ''

#where the new photo and .txt exists
img_path = path + '/output/'
txt_path = path + '/output/'
img = cv2.imread(img_path+'0.jpg')
#size of the photo
height = np.size(img, 0)
width = np.size(img, 1)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#write new video file
video_out = cv2.VideoWriter('output.mp4',fourcc, 10.0, (width,height))
#write new txt
text_out = open('output.txt', 'w')

#merge all the photo/txt in the folder(output) into a video/txt
for i in range(outname):
	img = cv2.imread(img_path + str(i) + '.jpg')
	video_out.write(img)

	f = open(txt_path + str(i) + '.txt')
	txt = f.read()
	text_out.write(txt)
	f.close()

video_out.release()
text_out.close()	

#read output.txt
f = open('output.txt', 'r', encoding = 'big5')
_text = f.readlines()
_text = str2list(_text, [',', '\n'])
f.close()

#statistic the area of bounding box
area = np.zeros((100, ))
for row in _text:
	n = row[1]
	pos = 2
	for i in range(int(n)):
		X = int(row[pos+2]) - int(row[pos])
		Y = int(row[pos+3]) - int(row[pos+1])
		pos += 5
		area[int((X * Y * 100) / (height * width))] += 1
f = open('area_statistics.txt', 'w') 
for i in range(100):
	f.write(str(i) + '%~' + str(i+1) + '%:' + str(area[i]) + '\n')
f.close()
