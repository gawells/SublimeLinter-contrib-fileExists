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


    def run(self,cmd,code):
        splitcode = code.split('\n')
        found_schrod = False

        tmp = code[0:10]
        # print (tmp)
        # schrod_regex = re.compile('\$SCHRODINGER[\/\w+]+(\s+[-\w+\.\:\$]+)+',re.M)
        schrod_regex = re.compile(
            '\$SCHRODINGER(\/\w+)+'
            '(.+(?P<config>-c\s+[a-zA-Z_][\w\.-_]+)?.+\\\\\n)+'
            '.+(?P<config2>-c\s+[a-zA-Z_][\w\.-_]+)?.+\n',
            re.M)

        config_regex = re.compile(
            r'\$SCHRODINGER(.+\\\n)*'
            r'(.+(?P<config>-c\s+[a-zA-Z_][\w\.-_]+).+)\n'
            ,re.M)
        # print (code)
        # schrodcmd = schrod_regex.search(code)
        # for f in schrod_regex.finditer(code):        
        for f in config_regex.finditer(code):        
            # print (f.group(0))
            # print (f.group())
            # print (f.group())
            print (f.group('config'))
            # print (f.groups())
            # print (f.group('config2'))
        # print (schrodcmd.group())
        # for match in schrod_regex.match(code):
        #     print(match)
        #     pass

        for line in splitcode:
            if re.search('\$SCHRODINGER', line):
                found_schrod = True

            fileArg = re.search("-[dcm(in)]\s+[a-zA-Z_][a-zA-Z0-9_\.-]*", line)            
            if fileArg and found_schrod:                
                match = re.search("[a-zA-Z_][a-zA-Z0-9._-]*$", fileArg.group(0))
                filename = match.group(0)
                path = os.path.dirname(self.view.file_name())

                if (os.path.isfile(path+"/"+filename)):
                    matchInLine = re.search(filename, line)
                    # print (matchInLine)
                    pos = matchInLine.start(0)
                    linted = 'W:%s:%s:warning:File exists'%(len(filename),pos+1) 
                    print (linted)
                    return (linted)
            else: 
                pass


        pass

