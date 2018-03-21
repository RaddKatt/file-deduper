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
			for i in range(0, numFiles):
				if i == 0:
					duplicates[foundHash] = {'numFiles': numFiles, 'filePaths': []}
					duplicates[foundHash]['filePaths'].append({'fileCategory': 'Original', 'filePath': hashlist[foundHash][i]})
				else:
					duplicates[foundHash]['filePaths'].append({'fileCategory': 'Duplicate', 'filePath': hashlist[foundHash][i]})
	return duplicates

def print_results(folderPath):
	a = get_duplicates(folderPath)
	print('\n' + str(len(a)) + ' duplicated hash values:')
	for key in a.keys():
		print(key)
	print('\n')
	for k,v in a.items():
		print('-- ' + str(k) + ' - ' + str(v['numFiles']) + ' files found')
		for k in v['filePaths']:
			print('\t' + str(k['fileCategory']) + ': ' + str(k['filePath']))
		print('\n')

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print >> sys.stderr, "FATAL Unsupported execution mode (expected filepath)"
		sys.exit(1)
	
	directory = sys.argv[1]
	print_results(directory)
