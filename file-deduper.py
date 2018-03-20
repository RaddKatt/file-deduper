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
		if not fileName.startswith('._'):  #Exclude Mac Metadata files
			fullFilePath = os.path.join(folderPath, fileName)
			if os.path.isfile(fullFilePath):
				yield os.path.abspath(fullFilePath)

def get_hashes(folderPath):
	hashlist = {}
	for f in get_folder_filenames(folderPath):
		md5Hash = get_md5(f)

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
			duplicates[foundHash] = {'numFiles': numFiles, 'filePaths': hashlist[foundHash]}
	return duplicates

if __name__ == '__main__':
	directory = sys.argv[1]
	dupes = get_duplicates(directory)
	for dupe in dupes:
		for i in range(0, len(dupes[dupe]['filePaths'])):
			if i == 0:
				print('Original File: ' + dupes[dupe]['filePaths'][i])
			else:
				print('Duplicate File: ' + dupes[dupe]['filePaths'][i])
		print('\n')
