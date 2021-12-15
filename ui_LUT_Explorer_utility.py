#! /usr/bin/env python
# -*- coding: utf-8 -*-

# LUT Explorer Utility. Requires DaVinci Resolve Studio 17
# Copyright (c) 2021 Bryan Randell

import sys
import os


if sys.platform.startswith('win'):
    # lut_folder = "C:\\ProgramData\\Blackmagic Design\\DaVinci Resolve\\Support\\LUT"
    lut_folder = "C:\\ProgramData\\Blackmagic Design\\DaVinci Resolve\\Support\\LUT\\Film Looks"
else:
    lut_folder = "Library/Application Support/Blackmagic Design/DaVinci Resolve/LUT"

"""
Useless in Davinci because the resolve object is already called natively
import DaVinciResolveScript
try:
    import DaVinciResolveScript as dvr
    resolve = dvr.scriptapp('Resolve')
except:
    from python_utils.python_get_resolve import GetResolve
    resolve = GetResolve()
"""

from lut_file_reader import lut

# Row Creation

def list_lut_row_creation(lut_path, tree_item, tree_LutID, img_thumbnail):
    item_num = 1
    for root, dir, files in os.walk(lut_path):
        for file in files:
            if file.endswith('cube') or file.endswith('dat'):

                item_row = tree_item[tree_LutID].NewItem()
                # item_row.Icon[0] = ui.Icon({'File': 'C:\\ProgramData\\Blackmagic Design\\DaVinci Resolve\\Support\\Workflow Integration Plugins\\img\\icon.png'})
                # item_row.Text[0] = ui.Icon({'File': 'C:\\ProgramData\\Blackmagic Design\\DaVinci Resolve\\Support\\Workflow Integration Plugins\\img\\icon.png'})
                # item_row.Icon[0] = ui.Icon({'File': lut(os.path.join(root, file), file.split('.')[0])})
                item_row.Icon[0] = ui.Icon({'File': lut(img_thumbnail, os.path.join(root, file))})
                item_row.Text[0] = '{:03d}'.format(item_num)
                item_row.Text[1] = '{}'.format(file)
                item_row.Text[2] = '{}'.format(os.path.join(root, file))
                tree_item[tree_LutID].AddTopLevelItem(item_row)
                item_num += 1

def list_lut_row_creation_filtered(lut_path, tree_item, tree_LutID, filter_string,img_thumbnail):
    item_num = 1
    for root, dir, files in os.walk(lut_path):
        for file in files:
            if file.endswith('cube') or file.endswith('dat'):
                if file.lower().find(filter_string.lower()) != -1:

                    item_row = tree_item[tree_LutID].NewItem()
                    item_row.Icon[0] = ui.Icon({'File': lut(img_thumbnail, os.path.join(root, file))})
                    item_row.Text[0] = '{:03d}'.format(item_num)
                    item_row.Text[1] = '{}'.format(file)
                    item_row.Text[2] = '{}'.format(os.path.join(root, file))
                    print(file)
                    print(filter_string)
                    tree_item[tree_LutID].AddTopLevelItem(item_row)
                    item_num += 1

                    # if file.lower().find(filter_string.lower()) != -1:
                    #     print(item_num)

# the method .GetCurrentClipThumbnailImage() only works in the color page
if resolve.GetCurrentPage() != 'color':
    resolve.OpenPage('color')
project_manager = resolve.GetProjectManager()
current_project = project_manager.GetCurrentProject()
print(current_project.GetName())
timeline = current_project.GetCurrentTimeline()
img_thumbnail = timeline.GetCurrentClipThumbnailImage()

# some element IDs
winID = "com.blackmagicdesign.resolve.LUT_utility"
# should be unique for single instancing
line_edit_searchID = 'LineEditSearch'
button_refreshID = 'Button_Refresh'
button_explorerID = "Button_Explorer"
tree_LutID = 'Tree_LUT'

# calling DavinciResolve UI in Workflow Integration
ui = fusion.UIManager
dispatcher = bmd.UIDispatcher(ui)

# # check for existing instance
# main_window = ui.FindWindow(winID)
# if main_window:
#     main_window.Show()
#     main_window.Raise()
#     exit()

# otherwise, we set up a new window, with HTML header (using the Examples logo.png)
header = '<html><body><h1 style="horizontal-align:middle;">'
header = header + '<b>DaVinci Resolve LUT Explorer Utility</b>'
header = header + '</h1></body></html>'

explication_text = "Left click on the LUT from the list above\nto add it on your active Timeline Clip first node"




# define the window UI layout
main_window = dispatcher.AddWindow({'ID': winID, 'Geometry': [100, 100, 1000, 500], 'WindowTitle': "DaVinci Resolve LUT Explorer Utility", },
    ui.VGroup([
      ui.Label({'Text': header, 'Weight': 0.2, 'Font': ui.Font({'Family': "Times New Roman"}), "Alignment" : { "AlignHCenter" : True , "AlignTop" : True }}),
    ui.HGroup({ 'Weight': 0.1 }, [
      ui.LineEdit({'ID': line_edit_searchID, 'Text': '', 'PlaceholderText': 'Filter LUTs by Name', 'Events': {'EditingFinished': True}}),
      ui.Button({'ID': button_refreshID, 'Text': 'Refresh List'},)
      ]),
    ui.HGroup({ 'Weight': 0.1 }, [
      ui.Label({'Text': 'LUT List', 'Weight': 0.1, 'Font': ui.Font({'Family': "Times New Roman", 'PixelSize': 20})}),
      ui.Button({'ID': button_explorerID, 'Text': 'Select LUT Folder'}, ),
        ]),
    # ui.HGroup({'Weight': 0.2}, [
    #   ui.Label({'Text': "Current LUT folder :{}".format(lut_folder), 'Weight': 0.1, 'Font': ui.Font({'Family': "Times New Roman", 'PixelSize': 14})}),
    #     ]),

      ui.Tree({'ID': tree_LutID, 'UniformRowHeights':False,'IconSize':[img_thumbnail['width'],img_thumbnail['height']],"ItemsExpandable":True, "ExpandsOnDoubleClick": True, 'SortingEnabled': True,'Events' : {'Move': True, 'ItemClicked': True}, }),

    ui.HGroup({ 'Weight': 0.2 }, [
      ui.Label({'Text': explication_text, 'Weight': 0.1, 'Font': ui.Font({'Family': "Times New Roman", 'PixelSize': 14}), "Alignment" : { "AlignHCenter" : True , "AlignTop" : True }}),
        ]),
    ]))


# Tree Item definition
main_window_item = main_window.GetItems()

# Header/Column Creation

column_header = main_window_item[tree_LutID].NewItem()
# column_header.Icon[0] = "Icon"
column_header.Text[0] = 'Index'
column_header.Text[1] = 'Name'
column_header.Text[2] = 'LUT PATH'

main_window_item[tree_LutID].SetHeaderItem(column_header)
main_window_item[tree_LutID].ColumnCount = 3
main_window_item[tree_LutID].ColumnWidth[0] = 300


main_window_item[tree_LutID].ColumnWidth[1] = 300
main_window_item[tree_LutID].ColumnWidth[2] = 100


list_lut_row_creation(lut_folder, main_window_item, tree_LutID,img_thumbnail)


# Functions for Event handlers
def OnClose(ev):
    dispatcher.ExitLoop()

def OnClickRefresh(ev):
    """
    Clear the timeline list and loop over timeline indexes
    :param ev:
    :return:
    """
    main_window_item[tree_LutID].Clear()
    timeline = current_project.GetCurrentTimeline()
    img_thumbnail = timeline.GetCurrentClipThumbnailImage()
    list_lut_row_creation(lut_folder, main_window_item, tree_LutID, img_thumbnail)
    print('List Refreshed')

# def OnClickFilter(ev):
#     print(tree_item['LineEditSearch'].SelectedText())

def OnTextChanged(ev):
    # print('test has changed')
    main_window_item[tree_LutID].Clear()
    timeline = current_project.GetCurrentTimeline()
    img_thumbnail = timeline.GetCurrentClipThumbnailImage()

    list_lut_row_creation_filtered(lut_folder,
                                   main_window_item,
                                   tree_LutID,
                                   main_window_item[line_edit_searchID].Text,
                                   img_thumbnail)

def OnClickTree(ev):
    print(main_window_item[tree_LutID].CurrentItem().Text[2])
    current_project.GetCurrentTimeline().GetCurrentVideoItem().SetLUT(1, main_window_item[tree_LutID].CurrentItem().Text[2])


def OnClickExplorer(ev):
    global lut_folder
    lut_folder = fusion.RequestDir('C:\\ProgramData\\Blackmagic Design\\DaVinci Resolve\\Support\\LUT')
    print(lut_folder)
    main_window_item[tree_LutID].Clear()
    timeline = current_project.GetCurrentTimeline()
    img_thumbnail = timeline.GetCurrentClipThumbnailImage()
    list_lut_row_creation(lut_folder, main_window_item, tree_LutID, img_thumbnail)

# assign event handlers
main_window.On[winID].Close = OnClose
main_window.On[line_edit_searchID].EditingFinished = OnTextChanged
main_window.On[tree_LutID].ItemClicked = OnClickTree
main_window.On[button_refreshID].Clicked = OnClickRefresh
main_window.On[button_explorerID].Clicked = OnClickExplorer
# main_window.On['Button_Filter'].Clicked = OnClickFilter

# main_window.On['Tree'].ItemDoubleClicked = OnDoubleClickTree


# Main dispatcher loop
main_window.Show()
dispatcher.RunLoop()
