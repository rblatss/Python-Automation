# Script to merge two files containing lists, where each item of list is a line of file.

def merge():
  
  filenames = ""
  hashmap = {}
  content = []
  
  filenames = raw_input("Enter names of files to merge (eg file1.txt file2.txt\\n) ")
  filenames = filenames.split(' ')

  if len(filenames) > 2:
    print "Merge.py can only merge two files"
    return
  
  # Read first file
  with open(filenames[0], "r") as infile:
    for line in infile:
      line = line.lower()
      if line not in hashmap:
	hashmap[line] = 1
  
  # Read second file
  with open(filenames[1], "r") as infile:
    for line in infile:
      line = line.lower()
      if line not in hashmap:
	hashmap[line] = 1
  
  # Sort hashmap contents
  for i in hashmap:
    content.append(i)
  content.sort()
    
  # Write sorted contents to "result.txt"
  with open("result.txt", "w") as outfile:
    for i in content:
      outfile.write(i)

if __name__ == "__main__":
  merge()