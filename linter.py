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

    def scanRegex(self,prog,arg,code,input=True):

        regex = re.compile(
            r'%s(.+\\\n)*'
            r'.+(?P<arg>%s\s+[a-zA-Z_][\w\._-]+).*\n' %(prog,arg)
            ,re.M)

        alllints = ''
        path = os.path.dirname(self.view.file_name())
        linted = None

        for f in regex.finditer(code):        
            match = re.search(r'(?P<flag>-\w+)\s+(?P<value>[a-zA-Z_][\w\._-]*)', f.group('arg'))

            filenameStart = match.start('value')
            filename = match.group('value')
            pos = self.linearToRowCol(f.start('arg')+filenameStart,code)

            if (os.path.isfile(path+"/"+filename)):
                if input:
                    linted = 'W:%s:%s:warning:File exists'%(pos[0],pos[1]) 
                else: 
                    linted = 'E:%s:%s:error:File exists, will be overwritten'%(pos[0],pos[1]) 
            else: 
                if input:
                    linted = 'E:%s:%s:error:File not found'%(pos[0],pos[1]) 

            if linted:
                alllints += '\n'+linted

        return alllints

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

        alllints = ''

        alllints += self.scanRegex('\$SCHRODINGER', '-c',code)
        alllints += self.scanRegex('\$SCHRODINGER', '-in',code)
        alllints += self.scanRegex('\$SCHRODINGER', '-m',code)
        alllints += self.scanRegex('\$SCHRODINGER', '-o',code,input=False)

        print (alllints)

        return(alllints)

