# DaVinci-Resolve-LUT-Explorer

## Description
Another way to preview LUTs on your footage.\
With icon corresponding to the timeline active clip thumbnail. 

## Needs Davinci Resolve 17

## Installation
If you never installed a Workflow Itegration Plugin in Davinci, 
create a folder named "Workflow Integration Plugin" in "%PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\" (On Windows) or 
"/Library/Application Support/Blackmagic Design/DaVinci Resolve" (on Mac OS). If you have already a Workflow Integration Plugin folder,
put the "ui_timeline_utility.py" file inside the latter.\
You need to install Pillow from **pip install pillow**.\
Then finally restart Davinci Resolve if it was already opened.

## Usage 
In Davinci Resolve go to Workspace > Workflow Integration click on ui_LUT_Explorer_utility it will open a window.\
Does not support 1D LUTs.

