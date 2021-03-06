'''
A simple file deduper
Usage: python file-deduper.py /path/to/test

Written using:
	Python 2.7.12 (default, Oct 11 2016, 05:24:00)
	[GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.38)] on darwin
'''

import hashlib	# For calculating hashes
import os	# For reading directory contents
import sys	# For command-line args
import csv	# For writing results file

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
				fileSize = os.path.getsize(hashlist[foundHash][i])
				fileCreateTime = os.path.getctime(hashlist[foundHash][i])
				if i == 0:
					duplicates[foundHash] = {'numFiles': numFiles, 'filePaths': []}
				duplicates[foundHash]['filePaths'].append({'fileCategory': 'Original', 'filePath': hashlist[foundHash][i], 'fileSize': fileSize, 'fileCreateTime': fileCreateTime})
	
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
			print('\t' + k['fileCategory'] + ': ' + str(k['filePath']) + '\t\t(' + str(k['fileSize']) + " bytes)")
		print('\n')

def write_results(folderPath):
	a = get_duplicates(folderPath)

	rows = [['filehash', 'numfiles', 'filepath', 'filecategory', 'filesize_in_bytes', 'file_creation_time']]
	for fileHash in a.keys():
		for f in a[fileHash]['filePaths']:
			row = []
			row.append(fileHash)
			row.append(a[fileHash]['numFiles'])
			row.append(f['filePath'])
			row.append(f['fileCategory'])
			row.append(f['fileSize'])
			row.append(f['fileCreateTime'])
			rows.append(row)

	with open('found.csv', 'wb') as csvfile:
		for i in rows:
			writer = csv.writer(csvfile)
			writer.writerow(i)
	
	return rows

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print >> sys.stderr, "FATAL Unsupported execution mode (expected filepath)"
		sys.exit(1)
	
	directory = sys.argv[1]
	print_results(directory)
	write_results(directory)
