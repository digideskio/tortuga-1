# Copyright (C) 2007 Maryland Robotics Club
# Copyright (C) 2007 Joseph Lisee <jlisee@umd.edu>
# All rights reserved.
#
# Author: Joseph Lisee <jlisee@umd.edu>
# File:   tools/oci/src/frame.py

# Library Imports
import wx
import wx.aui
import wx.py

# Project Imports
from gui.view import IPanelProvider
from core import ExtensionPoint
import ext.core as core

import oci.view.panels  # Import needed for registration of IPanelProviders

class MainFrame(wx.aui.AuiMDIParentFrame):
    """
    @type panel_providers: iterable
    @cvar panel_providers: A list of all classes which can provide panels for 
                           the gui.
                           
    @type _panels: {core.Subsystem : [wx.Window]}
    @ivar _panels: Keeps track of which modules own which panel so they can be
                   cleaned up module shutdown.
    """
    
    
    panelProviders = ExtensionPoint(IPanelProvider)
    
    def __init__(self, config, subsystems):
        self._panels = []
    
        # Instantiate super class based on configuration settings
        #gui_node = config.get('GUI', {})
        #position = gui_node.get('window_position',wx.DefaultPosition)
        #size = gui_node.get('window_size', wx.Size(800,600))

        position = wx.DefaultPosition
        size = wx.Size(800,600)
        title = 'OCI'
        wx.aui.AuiMDIParentFrame.__init__(self, None, wx.ID_ANY, title, 
                                          position, size)

        # Add panels for all the current subsystems
        self._addSubsystemPanels(subsystems)
        self._addShell(subsystems)
        
        self.SetMinSize(self.GetSize())
        self.Bind(wx.EVT_CLOSE,self._onClose)            
    
    def _addShell(self, subsystems):
        # Build locals
        subsystemDict = {}
        for subsystem in subsystems:
            subsystemDict[subsystem.getName()] = subsystem
        locals = {}
        locals['subsystems'] = subsystemDict
        
        shell = wx.py.shell.Shell(self._createMDIChild(), locals = locals)
        paneInfo = wx.aui.AuiPaneInfo().Name("Shell")
        paneInfo = paneInfo.Caption("Shell").Left()
        self._addSubsystemPanel(paneInfo, shell, [])
    
    def _onClose(self, event):
        # TODO: Update this list based on whether the close or not
        for panel in self._panels:
            panel._onClose(wx.CloseEvent())
        event.Skip()
        
#    def _remove_module(self, mod):    
#        """
#        Close all panes attached to a module
#        """
#        for panel in self._panels[mod]:
#            self._mgr.DetachPane(panel)
#            panel.Close()
#        
#        del self._panels[mod]
        
    def _createMDIChild(self):
        return wx.aui.AuiMDIChildFrame(self, wx.ID_ANY, 'ERROR')
        
    def _addSubsystemPanels(self, subsystems):
        for provider in self.panelProviders:
            panelInfos = provider.getPanels(subsystems, self._createMDIChild)
            for paneInfo, panel, sys in panelInfos:
                self._panels.append(panel)
                self._addSubsystemPanel(paneInfo, panel, sys)

    def _addSubsystemPanel(self, paneInfo, panel, usedSubsystems):
        mdiFrame = panel.GetParent()
        mdiFrame.SetTitle(paneInfo.caption)
        mdiFrame.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOWFRAME)) 
        # Put the panel in a sizer which streches the panel over the entire 
        # AuiMDIChildFrame
        sizer = wx.BoxSizer()
        sizer.Add(panel, proportion = 1, flag = wx.EXPAND)
        mdiFrame.SetSizer(sizer)  
        sizer.Fit(panel) 
        mdiFrame.SetMinSize(sizer.GetMinSize())
        
