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
import sublime_plugin
import json
import logging

# PLUGIN_SETTINGS = sublime.load_settings("fileExists.sublime-settings")
# SYNTAX = PLUGIN_SETTINGS.get("syntax")
# DEBUG = PLUGIN_SETTINGS.get("debug", False)

# logging.basicConfig(format='[fileExists] %(message)s ')
# felogger = logging.getLogger(__name__)

# if (DEBUG):
#     felogger.setLevel(logging.DEBUG)
# else:
#     felogger.setLevel(logging.WARNING)

# SYNTAX = "source.shell"

SYNTAX = 'source.shell'

def plugin_loaded():
    global SYNTAX
    PLUGIN_SETTINGS = sublime.load_settings("fileExists.sublime-settings")
    print (sublime.find_resources("fileExists.sublime-settings"))
    SYNTAX = PLUGIN_SETTINGS.get("syntax")
    DEBUG = PLUGIN_SETTINGS.get("debug", False)

    logging.basicConfig(format='[fileExists] %(message)s ')
    global felogger 
    felogger = logging.getLogger(__name__)

    if (DEBUG):
        felogger.setLevel(logging.DEBUG)
    else:
        felogger.setLevel(logging.WARNING)

    print("=========================================================")
    # sublime_plugin.reload_plugin("SublimeLinter")

class FileExists(Linter):

    """Provides an interface to fileExists."""

    syntax = tuple(SYNTAX)
    print(syntax)
    cmd = None
    regex = (
        r'^.+?:(?P<line>\d+):(?P<col>\d+):'
        r'(?:(?P<error>error)|(?P<warning>(warning|note))):'
        r'(?P<message>.+)$'
    )
    word_re = r'(^[-\w\.\/]+)'
    multiline = False
    line_col_base = (1, 1)
    defaults = {}
    inline_settings = None
    inline_overrides = None
    comment_re = None

    @classmethod
    def posToRowCol(cls, pos, code):
        """
        Convert position in string to rectangular coordinates
        """

        row = 1
        currentlen = 0
        lastlen = 0
        splitcode = code.split('\n')

        for line in splitcode:
            lastlen = currentlen
            currentlen += len(line)+1
            if currentlen >= pos:
                return (row, pos-lastlen+1)
            row += 1
    
    def splitInterruptedLint(self,lint):
        """
        Split linted area interrupted by non-\w characters into multiple
        warnings/errors
        """

        linted = ""
        # felogger.debug(lint)
        fname = re.search("(?P<open>\()(?P<file>[\w\.\/_-]+)(?P<close>\))",lint).group('file')
        felogger.debug(fname)
        positions = lint.split(":")

        slash_search = re.compile("/")
        slashes = []
        for slash_instance in slash_search.finditer(fname):
            slashes.append(slash_instance.start())

        if len(slashes) > 0:
            for s in slashes:                
                # linted += '\nW:%s:%s:warning:File exists (%s)\n'%(positions[1], int(positions[2])+s+1, fname)
                linted += '\n%s:%s:%s:%s:%s'\
                %(positions[0],positions[1],int(positions[2])+s,positions[3], positions[4])
                linted += '\n%s:%s:%s:%s:%s'\
                %(positions[0],positions[1],int(positions[2])+s+1,positions[3], positions[4])

        return linted


    def checkForFile(self, code, path, filename_instance, prog_instance, inputfile=True):
        """
        Check whether P?<fname> in filename_instance regex find (within prog_instance
        regex find) exists in same directory as file. Return appropriate warning/error
        """


        filename = filename_instance.group('fname')
        filenameStart = filename_instance.start('fname')
        pos = self.posToRowCol(prog_instance.start(0)+filenameStart, code)
        if filename[0] == "/":
            fullpath = filename
        else:
            fullpath = path+"/"+filename

        if os.path.isfile(fullpath):
            if inputfile:
                linted = 'W:%s:%s:note:File exists (%s)\n'%(pos[0], pos[1], filename)
                # linted += self.splitInterruptedLint( linted)
            else:
                linted = 'E:%s:%s:error:File exists, will be overwritten (%s)\n'\
                %(pos[0], pos[1], filename)
                # linted += self.splitInterruptedLint(linted)
        else:
            if inputfile:
                linted = 'E:%s:%s:error:File not found (%s)\n'%(pos[0], pos[1], filename)
                # linted += self.splitInterruptedLint(linted)
            else:
                linted = ""

        return linted


    def scanUnflagged(self, prog, ext, code, inputfile=True):
        """
        Scan for file arguments not preceded by a -/-- type flag.
        Check if each file exists and return appropriate warning
        or error messages for each file
        """

        path = os.path.dirname(self.view.file_name())
        all_lints = ''
        linted = None

        regex = re.compile(
            r'(?<!#.)%s(.+\\\n)*'
            r'(.+([\w\._-]+%s).*(\n|\Z))' %(prog, ext)
            , re.M)

        for prog_instance in regex.finditer(code):
            file_regex = re.compile(r'(?<!-)(?P<preceding>[\']?\w[\w_\.-]+[\']?)[\n\\\s]+(?P<fname>[/\w_\.-]+%s)'%ext)

            for file_instance in file_regex.finditer(prog_instance.group(0)):
                filename = file_instance.group('fname')
                # felogger.debug(filename)
                isflag = re.search('^-{1,2}\w+',file_instance.group('preceding'))
                if not isflag:
                    linted = self.checkForFile(code, path, file_instance, \
                        prog_instance, inputfile)
                    all_lints += linted
                

        return all_lints

 
    def scanFlagged(self, prog, arg, code, inputfile=True):
        """
        Scan for file arguments preceded by -/-- type flags. 
        Check if each file exists and return appropriate warning
        or error messages for each file
        """

        # regex = re.compile(
        #     r'(?<!#.)%s(.+\\\n)*'
        #     r'(.+([\s\w\._-]*%s).*(\n|\Z))' %(prog, arg)
        #     , re.M)

        regex = re.compile(
            r'(?<!#.)%s(.+\\\s*\n)*'
            r'(.*(\n|\Z))' %(prog)
            )

        all_lints = ''
        linted = None
        path = os.path.dirname(self.view.file_name())        

        all = []

        for prog_instance in regex.finditer(code):
            all.append(prog_instance.group(0))
            file_regex = re.compile(r'(?P<flag>%s)[\s\\]+(?P<fname>[/\w\.\/_-]+)'%arg,
                re.M)

            for file_instance in file_regex.finditer(prog_instance.group(0)):
                print(file_instance.group(0))
                linted = self.checkForFile(code, path, file_instance, \
                    prog_instance, inputfile)
                linted = self.checkForFile(code, path, file_instance, prog_instance, inputfile)
                all_lints += linted

        # print("Total "+str(len(all)))

        return all_lints


    def readFileArgs(self, scope):
        """
        Read predefined program name and flag assocations from all
        *.fileArg files is sublime 3 config folder.
        """
        flagFiles = sublime.find_resources("*.fileArgs")       

        for flaglist in flagFiles:
            # felogger.debug(flaglist)
            flagdata = json.loads(sublime.load_resource(flaglist))

            if flagdata['scope'] in scope:
                return flagdata

        return False

    def run(self, cmd, code):
        """
        Return error and warning messages internally instead of
        running through external linter
        """

        scope_name = self.view.scope_name(0)
        felogger.debug(scope_name)
        fromFile = self.readFileArgs(scope_name)

        all_lints = ''

        for entry in fromFile['keywords']:
            # felogger.debug (entry['key'])
            # print (fromFile['keywords'][key]['unflaggedExts'])

            for inputFlag in entry['inputflags']:      
                all_lints += self.scanFlagged(entry['key'], inputFlag, code)

            for outputFlag in entry['outputflags']:
                all_lints += self.scanFlagged(entry['key'], outputFlag, code, False)

            for ext in entry['unflaggedInputs']:
                all_lints += self.scanUnflagged(entry['key'], ext, code)

            for ext in entry['unflaggedOutputs']:
                all_lints += self.scanUnflagged(entry['key'], ext, code, False)

        # print(all_lints)

        return all_lints

