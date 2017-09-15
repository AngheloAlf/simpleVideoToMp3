#! python3
# -*- coding: UTF-8 -*-

import moviepy.editor as mp
import os
import sys
print(sys.version)
try:
	import tkFileDialog as filedialog
except:
	from tkinter import filedialog as filedialog


folder1 = filedialog.askdirectory(title="Select videos folder")
if folder1 == "":
	exit(0)
folder2 = filedialog.askdirectory(title="Select output folder")
if folder2 == "":
	exit(0)

indice = 0
total = len([name for name in os.listdir(folder1) if os.path.isfile(os.path.join(folder1, name))])
print(total)

subResultFolder = os.path.split(folder1)[-1]
audioFolder = os.path.join(folder2, subResultFolder)
if not os.path.isdir(audioFolder):
	os.mkdir(audioFolder)

for videoName in os.listdir(folder1):
	folderAndVideo = os.path.join(folder1, videoName)
	if os.path.isfile(folderAndVideo):
		indice += 1

		subName = videoName.split(".")
		subName[-1] = "mp3"
		audioName = ".".join(subName)

		folderAndAudio = os.path.join(audioFolder, audioName)

		if os.path.isfile(folderAndAudio):
			continue
		
		print("\n")
		print(videoName+" -> "+audioName)
		print("\t"+folderAndVideo+" -> "+folderAndAudio)
		print("\n")

		clip = mp.VideoFileClip(folderAndVideo)
		clip.audio.write_audiofile(folderAndAudio)

		print("\t"+str(indice)+"/"+str(total)+" ~ "+str(100*indice/total)+"%")
