#
# linter.py
# Linter r SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by 
# Copyright (c) 2015 
#
# License: MIT
#

"""This module exports the FileExists plugin class."""

from SublimeLinter.lint import Linter, util
import re
import os
import sublime

class FileExists(Linter):

    """Provides an interface to fileExists."""

    syntax = ('pbs','source.pbs')
    # syntax = ('source.pbs','pbs')
    # cmd = 'fileExists.py'
    cmd = None
    # executable = None
    # version_args = '--version'
    # version_re = r'(?P<version>\d+\.\d+\.\d+)'
    # version_requirement = '>= 1.0'
    # regex = r''
    regex = (
        r'^.+?:(?P<line>\d+):(?P<col>\d+):'
        r'(?:(?P<error>error)|(?P<warning>(warning|note))):'
        r'(?P<message>.+)$'
    )
    word_re = r'(^[-\w\.]+)'
    multiline = False
    line_col_base = (1, 1)
    # error_stream = util.STREAM_BOTH
    # selectors = {
    #     'source.pbs': 'schrodinger.input'
    # }
    # word_re = None
    defaults = {}
    inline_settings = None
    inline_overrides = None
    comment_re = None

    def linearToRowCol(self,pos,code,tablength=4):
    	untabbed = code.replace('\t',' '*tablength)
    	# print ('00000'+' '*tablength+'`````````')
    	row = 1
    	currentlen = 0
    	lastlen = 0
    	print ("###"+str(pos))
    	splitcode = untabbed.split('\n')
    	print (len(untabbed))
    	print (len(code))

    	for line in splitcode:
    		lastlen = currentlen
    		currentlen += len(line)+1
    		# print (currentlen)
    		if currentlen >= pos:
    			return((row,pos-lastlen+1))
    		row += 1


    def run(self,cmd,code):
        untabbed = code.replace('\t',' '*4)
        untabbed = code
        splitcode = code.split('\n')
        found_schrod = False

        schrod_regex = re.compile(
            '\$SCHRODINGER(\/\w+)+'
            '(.+(?P<config>-c\s+[a-zA-Z_][\w\.-_]+)?.+\\\\\n)+'
            '.+(?P<config2>-c\s+[a-zA-Z_][\w\.-_]+)?.+\n',
            re.M)


        config_regex = re.compile(
            r'\$SCHRODINGER(.+\\\n)*'
            r'.+(?P<config>-c\s+[a-zA-Z_][\w\._-]+).+\n'
            ,re.M)

        for f in config_regex.finditer(untabbed):        
            print (f.group('config'))
            match = re.search("[a-zA-Z_][\w\._-]*$", f.group('config'))
            filenameStart = match.start(0)
            # matchInLine = re.search(filename, line)
            print (self.linearToRowCol(f.start('config')+filenameStart,untabbed))


        cms_regex = re.compile(
            r'\$SCHRODINGER(.+\\\n)*'
            r'.+(?P<config>-in\s+[a-zA-Z_][\w\._-]+).+\n'
            ,re.M)

        for f in cms_regex.finditer(untabbed):        
            print (f.group('config'))
            match = re.search("[a-zA-Z_][\w\._-]*$", f.group('config'))
            filenameStart = match.start(0)
            print (self.linearToRowCol(f.start('config')+filenameStart,untabbed))


        alllints = ''

        lineNum = 1
        for line in splitcode:
            if re.search('\$SCHRODINGER', line):
                found_schrod = True

            fileArgRe = re.compile("-([dcm]|in)\s+[a-zA-Z_][\w_\.-]*")            
            # fileArg = re.search("-[dcm(in)]\s+[a-zA-Z_][a-zA-Z0-9_\.-]*", line)            
            # if fileArg and found_schrod:                
            if found_schrod:                
            	print (line)
            	for fileArg in fileArgRe.finditer(line):
	                match = re.search("[a-zA-Z_][\w\._-]*$", fileArg.group(0))
	                print (fileArg)	                
	                print (fileArg.group(0))
	                filename = match.group(0)
	                print (filename)
	                path = os.path.dirname(self.view.file_name())

	                if (os.path.isfile(path+"/"+filename)):
	                    matchInLine = re.search(filename, line)
	                    print (matchInLine.group(0))
	                    pos = matchInLine.start(0)
	                    linted = 'W:%s:%s:warning:File exists'%(lineNum,pos+1) 
	                    alllints += '\n'+linted
            else: 
                pass
            lineNum += 1

        print(alllints)
        return(alllints)

