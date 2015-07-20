# Script to replace cci prefix to ctci in filename
import os, re

dir = os.getcwd()
pattern = re.compile(r'^cci')
filenames = os.listdir(dir)
for n in filenames:
  if re.match(pattern, n):
    os.rename(n, "ctci" + n[3:])
 

