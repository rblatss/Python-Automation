# Read and Record
# Search "Cracking the Coding Interview" folder (of Interview Prep repository)
# and subfolders to read "MISCELLANEOUS STUFF I LEARNED" sections of .cc files
# and consolidate text into a single file
import os, re

root = "C:\\Users\\Robert\\Documents\\job\\coding\\Interview Prep" #os.getcwd()
begin = re.compile(r'\s*(MISC)[A-Z\s]* | (STUFF)[A-Z\s]*')
end = re.compile(r"\*/")

with open('..\\data\\stuff ive learned.txt', 'wb') as out:
	out.write("STUFF IVE LEARNED\n---------------------------------\n")
	for curr_dir, dirs, files in os.walk(root): # recurse thru subdirs
		for file in files:
			if file[-3:] == ".cc":
				with open(curr_dir + "\\" + file, 'rb') as ccfile:
					
					copy = False
					text = ""
					line = ccfile.readline()
					
					while line:
						
						if copy:
							text += line
							
						# Get to MISC. section
						if re.match(begin, line):
							copy = True
							
						# Copy until '*\', which marks end of copy
						elif re.match(end, line):
							break
											
						line = ccfile.readline()
					
					# Write text read from .cc file if available
					if text != "":
						out.write(file + "\n")
						out.write(text)
