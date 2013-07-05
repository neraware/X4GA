#!/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         awc/layout/factory.py
# Copyright:    (C) 2013 Fabio Cassini <fc@f4b10.org>
# ------------------------------------------------------------------------------


import wx
import awc.controls.windows as aw


class FC_FactoryPanel(wx.Panel):
    
    filler = None
    
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.filler(self)


class _FC_FactoryContainerMixin(object):
    
    PanelClass = None
    
    def __init__(self, *args, **kwargs):
        object.__init__(self)
        self.panel = self.PanelClass(self)
        self.AddSizedPanel(self.panel)
    
    def get_control(self, name, exception_if_notfount=True):
        obj = self.FindWindowByName(name)
        if obj is None and exception_if_notfount:
            raise Exception, "Not found"
        return obj
    
    def get_value(self, name, exception_if_notfount=True):
        obj = self.get_control(name, exception_if_notfount)
        if obj:
            return obj.GetValue()
        return None

class FC_FactoryFrame(aw.Frame, _FC_FactoryContainerMixin):
    
    def __init__(self, *args, **kwargs):
        aw.Frame.__init__(self, *args, **kwargs)
        _FC_FactoryContainerMixin.__init__(self)

class FC_FactoryDialog(aw.Dialog, _FC_FactoryContainerMixin):
    
    def __init__(self, *args, **kwargs):
        aw.Dialog.__init__(self, *args, **kwargs)
        _FC_FactoryContainerMixin.__init__(self)

def _make_container(AwClass, name=None, title='', filler=None, parent=None, center='screen', default_values=None):
    
    if issubclass(AwClass, aw.Frame):
        FC_ContainerClass = FC_FactoryFrame
    elif issubclass(AwClass, aw.Dialog):
        FC_ContainerClass = FC_FactoryDialog
    else:
        raise Exception, "Tipo errato"
                      
    PanelClass = type(name, (FC_FactoryPanel,), {'filler': filler})
    
    ContainerClass = type(name, (FC_ContainerClass,), {'PanelClass': PanelClass})
    
    container = ContainerClass(parent, title=title)
    if center == 'screen':
        container.CenterOnScreen()
    elif center == 'parent':
        container.CenterOnParent()
    
    if default_values:
        for name in default_values:
            container.get_control(name).SetValue(default_values[name])
    
    return container

def make_frame(name=None, title='', filler=None, parent=None, center='screen', default_values=None):
    return _make_container(aw.Frame, '%sFrame'%name, title, filler, parent, center, default_values)

def make_dialog(name=None, title='', filler=None, parent=None, center='screen', default_values=None, validation=None, modal_exit_button=None):
    
    dlg = _make_container(aw.Dialog, '%sDialog'%name, title, filler, parent, center, default_values)
    
    if modal_exit_button:
        for name in modal_exit_button:
            exit_value = modal_exit_button[name]
            def on_endmodal_if_validates(event):
                do = True
                if validation:
                    msg, do = validation(dlg)
                    if msg:
                        aw.awu.MsgDialog(dlg, msg, style=wx.ICON_ERROR)
                if do:
                    dlg.EndModal(exit_value)    
            dlg.Bind(wx.EVT_BUTTON, on_endmodal_if_validates, dlg.get_control(name))
    
    return dlg
