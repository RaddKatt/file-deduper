import hashlib	# For calculating hashes
import os	# For reading directory contents
import sys	# For command-line args

def get_md5(filePath):
	with open(filePath, 'rb') as fileToCheck:
		data = fileToCheck.read()
		returnedMd5 = hashlib.md5(data).hexdigest()

	return returnedMd5

def get_folder_filenames(folderPath):
	for fileName in os.listdir(folderPath):
		fullFilePath = os.path.join(folderPath, fileName)
		if os.path.isfile(fullFilePath):
			yield os.path.abspath(fullFilePath)

def get_hashes(folderPath):
	hashlist = {}
	for f in get_folder_filenames(folderPath):
		md5Hash = get_md5(f)

		if md5Hash != 'b6a68923cea360c9cea4708ada7fe3dd':  #Exclude Mac Metadata files
			if md5Hash in hashlist:
				hashlist[md5Hash].append(f)
			else:
				hashlist[md5Hash] = []
				hashlist[md5Hash].append(f)
	return hashlist

def get_duplicates(folderPath):
	hashlist = get_hashes(folderPath)
	duplicates = {}	
	for foundHash in hashlist:
		numFiles = len(hashlist[foundHash])
		if numFiles > 1:
			'''print(foundHash + ': ' + str(numFiles))
			for file in hashlist[foundHash]:
				print('\t' + str(file))'''
			duplicates[foundHash] = {'numFiles': numFiles, 'filePaths': hashlist[foundHash]}
	return duplicates

if __name__ == '__main__':
	directory = sys.argv[1]
	dupes = get_duplicates(directory)
	for dupe in dupes:
		print(dupes[dupe]['filePaths'])
