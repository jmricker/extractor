import os, sys, os.path

import os, fnmatch
import glob
import shutil
import subprocess
import sys

base = sys.argv[1]

try:
    shutil.rmtree('temp')
except Exception, e:
    pass

archivedirs = filter(os.path.isdir, glob.glob(base + '\\*.*'))
                     
print "Extracting from %d paths" % len(archivedirs)
print
                                       
for path in archivedirs:
    print 'Extracting', path
    
    os.mkdir('temp')
    os.mkdir('temp/temp2')
    
    rararchives = glob.glob(path + "\\*.r*")
    if rararchives:
        process = subprocess.Popen('unrar.exe x "' + path + '/*.r*"' + ' *.* temp',
                                  bufsize=1024, stdout=None)
        process.communicate()
        del process

    ziparchives = glob.glob(path + "\\*.zip")
    if ziparchives:
        process = subprocess.Popen('unzip.exe -q -o "' + path + '/*.zip"' + ' -d temp',
                                  bufsize=1024, stdout=None)
        process.communicate()
        del process

    rararchives = glob.glob('temp\\*.r*')
    if rararchives:
        #extract from '\temp\*.r*' and output to temp2
        process = subprocess.Popen('unrar.exe x "temp/*.r*" *.* temp/temp2',
                                  bufsize=1024, stdout=None)
        process.communicate()
        del process

    ziparchives = glob.glob('/temp\\*.zip')
    if ziparchives:
        #extract from '\temp\*.zip' and output to temp2
        process = subprocess.Popen('unzip.exe -qo "temp/*.zip"' + ' -d temp/temp2',
                                  bufsize=1024, stdout=None)
        process.communicate()
        del process
        pass

    #rename contents of temp\temp2 to basedir + basename + extension

    basefilename = path[path.rindex('\\'):]
    for filename in glob.glob('temp/temp2/*.*'):        
        extension = filename[filename.rindex('.'):]
        shutil.move(filename, base + basefilename + extension)
        print "Moving", filename, 'to', base + basefilename + extension
        print
        
    
    shutil.rmtree('temp')


