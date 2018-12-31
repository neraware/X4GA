#!/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         ftel/acquisti/ricevi.py
# Author:       Fabio Cassini <fabio.cassini@gmail.com>
# Copyright:    (C) 2018 Evolvia S.r.l.
# ------------------------------------------------------------------------------
# This file is part of X4GA
# 
# X4GA is free software: you can redistribute it and/or modify
# it under the terms of the Affero GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# X4GA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with X4GA.  If not, see <http://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------------

import wx
import awc.controls.windows as aw
import ftel.acquisti.acquis_wdr as wdr
import ftel.acquisti.dbtables as dbftel
from ftel.acquisti.acquis import FtelAcquisFrame

from Env import Azienda
bt = Azienda.BaseTab

FRAME_TITLE = "Importazione Fatture Elettroniche"


class FtelRiceviPanel(aw.Panel):
    
    def __init__(self, *args, **kwargs):
        aw.Panel.__init__(self, *args, **kwargs)
        wdr.RiceviFunc(self)
        cn = self.FindWindowByName
        self.dblist = dbftel.ElencoFiles()
        self.update_data()
        self.Bind(wx.EVT_BUTTON, self.OnRiceviFiles, cn('butric'))
    
    doc_ids = None
    
    def update_data(self):
        cn = self.FindWindowByName
        wx.BeginBusyCursor()
        try:
            info = self.dblist.gateway_get_info()
            cn('numdocs').SetLabel(str(info['numdocs']))
            cn('butric').Enable(info['numdocs']>0)
            self.doc_ids = info['doc_ids']
            print self.doc_ids
        except Exception, e:
            aw.awu.MsgDialog(self, repr(e.args), style=wx.ICON_ERROR)
            cn('butric').Disable()
        finally:
            wx.EndBusyCursor()
    
    def OnRiceviFiles(self, event):
        n = self.RiceviFiles()
        if n:
            aw.awu.MsgDialog(self, '%d file ricevuti' % n, style=wx.ICON_INFORMATION)
            event.Skip()
    
    def RiceviFiles(self):
        if not self.doc_ids:
            return
        wait = aw.awu.WaitDialog(self, message="Download files XML in corso...", maximum=len(self.doc_ids))
        try:
            for n, id_doc in enumerate(self.doc_ids):
                wait.SetValue(n)
                filename = self.dblist.gateway_get_documento(id_doc)
                wait.SetMessage(filename)
            return len(self.doc_ids)
        except Exception, e:
            aw.awu.MsgDialog(self, repr(e.args), style=wx.ICON_ERROR)
        finally:
            wait.Destroy()


class FtelRiceviFrame(aw.Frame):
    
    def __init__(self, *args, **kwargs):
        if not kwargs.has_key('title') and len(args) < 3:
            kwargs['title'] = FRAME_TITLE
        aw.Frame.__init__(self, *args, **kwargs)
        self.AddSizedPanel(FtelRiceviPanel(self))
        cn = self.FindWindowByName
        self.Bind(wx.EVT_BUTTON, self.OnShowFiles, cn('butric'))
    
    def OnShowFiles(self, event):
        f = FtelAcquisFrame()
        f.Show()
        self.Close()
