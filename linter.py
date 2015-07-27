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
    # cmd = 'fileExists.py'
    cmd = None
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
    # warning_color = '000000'

    def linearToRowCol(self,pos,code,tablength=4):
    	row = 1
    	currentlen = 0
    	lastlen = 0
    	splitcode = code.split('\n')

    	for line in splitcode:
    		lastlen = currentlen
    		currentlen += len(line)+1
    		if currentlen >= pos:
    			return((row,pos-lastlen+1))
    		row += 1

    def scanUnflagged(self,prog,ext,code,input=True):

        path = os.path.dirname(self.view.file_name())
        all_lints = ''
        linted = None

        regex = re.compile(
            r'%s(.+\\\n)*'
            r'.+\s+([\w\._-]+%s)+\s+.*\n' %(prog,ext)
            ,re.M)

        for prog_instance in regex.finditer(code):
            file_regex = re.compile (r'(?P<preceding>[\w_\.-]+)\s+(?P<fname>[\w_\.-]+%s)'%ext)
          
            for file_instance in file_regex.finditer(prog_instance.group(0)):
                filename = file_instance.group('fname')
                isflag = re.search('-{1,2}\w+',file_instance.group('preceding'))
                if not isflag:
                    filenameStart = file_instance.start('fname')
                    pos = self.linearToRowCol(prog_instance.start(0)+filenameStart, code)

                    if (os.path.isfile(path+"/"+filename)):
                        if input:
                            linted = 'W:%s:%s:warning:File exists (%s)'%(pos[0],pos[1],filename) 
                        else: 
                            linted = 'E:%s:%s:error:File exists, will be overwritten (%s)'%(pos[0],pos[1],filename) 
                    else: 
                        if input:
                            linted = 'E:%s:%s:error:File not found (%s)'%(pos[0],pos[1],filename) 

                    if linted:
                        all_lints += '\n'+linted

        return all_lints

 
    def scanFlagged(self,prog,arg,code,input=True):

        regex = re.compile(
            r'%s(.+\\\n)*'
            r'.+(?P<arg>%s\s+[\w\._-]+).*\n' %(prog,arg)
            ,re.M)

        all_lints = ''
        linted = None
        path = os.path.dirname(self.view.file_name())

        for prog_instance in regex.finditer(code):        
            file_regex = re.compile(r'(?P<flag>%s)\s+(?P<fname>[\w\._-]+)'%arg)
            print (prog_instance.group(0))

            for file_instance in file_regex.finditer(prog_instance.group(0)):
                filenameStart = file_instance.start('fname')
                filename = file_instance.group('fname')
                pos = self.linearToRowCol(prog_instance.start(0)+filenameStart,code)
                print (pos)

                if (os.path.isfile(path+"/"+filename)):
                    if input:
                        linted = 'W:%s:%s:warning:File exists'%(pos[0],pos[1]) 
                    else: 
                        linted = 'E:%s:%s:error:File exists, will be overwritten'%(pos[0],pos[1]) 
                else: 
                    if input:
                        linted = 'E:%s:%s:error:File not found'%(pos[0],pos[1]) 

                if linted:
                    all_lints += '\n'+linted

        return all_lints


    def run(self,cmd,code):
        untabbed = code.replace('\t',' '*4)
        untabbed = code
        splitcode = code.split('\n')
        found_schrod = False

        all_lints = ''

        all_lints += self.scanFlagged('\$SCHRODINGER', '-c',code)
        all_lints += self.scanFlagged('\$SCHRODINGER', '-in',code)
        all_lints += self.scanFlagged('\$SCHRODINGER', '-m',code)
        all_lints += self.scanFlagged('\$SCHRODINGER', '-o',code,input=False)
        all_lints += self.scanUnflagged('\$SCHRODINGER', '.cms', code)

        print (all_lints)

        return(all_lints)

