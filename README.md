SublimeLinter-contrib-fileExists
================================

![example](/example.png?raw=true)

Prevent filename argument typos and accidentally overwriting old outputs (especially for batch queue scripts). This linter plugin for [SublimeLinter][docs] lints file name arguments within user specified commands. It is intended to be used with derivatives of the “__shell__” syntax. Filename arguments are checked against files in the same directory as the script. Input files will be highlighted as "warnings" if present, otherwise as "errors". Existing output files will be highligted as "errors", or left blank otherwise.

Json with the .fileArgs extenion are used to specifiy which programs and associated flags are to be linted.

## Installation
SublimeLinter 3 must be installed in order to use this plugin. If SublimeLinter 3 is not installed, please follow the instructions [here][installation].

### Linter installation
No installation needed, linting is internal to this plugin.

### Plugin installation
Download from this repository to the Packages/User folder of your local Sublime Text config

## Settings
For general information on how SublimeLinter works with settings, please see [Settings][settings]. For information on generic linter settings, please see [Linter Settings][linter-settings].

## Contributing
If you would like to contribute enhancements or fixes, please do the following:

1. Fork the plugin repository.
1. Hack on a separate topic branch created from the latest `master`.
1. Commit and push the topic branch.
1. Make a pull request.
1. Be patient.  ;-)

Thank you for helping out!

[docs]: http://sublimelinter.readthedocs.org
[installation]: http://sublimelinter.readthedocs.org/en/latest/installation.html
[locating-executables]: http://sublimelinter.readthedocs.org/en/latest/usage.html#how-linter-executables-are-located
[pc]: https://sublime.wbond.net/installation
[cmd]: http://docs.sublimetext.info/en/sublime-text-3/extensibility/command_palette.html
[settings]: http://sublimelinter.readthedocs.org/en/latest/settings.html
[linter-settings]: http://sublimelinter.readthedocs.org/en/latest/linter_settings.html
[inline-settings]: http://sublimelinter.readthedocs.org/en/latest/settings.html#inline-settings
