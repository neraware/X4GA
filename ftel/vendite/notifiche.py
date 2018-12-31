#!/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         ftel/vendite/notifiche.py
# Copyright:    (C) 2018 Evolvia S.r.l. <info@evolvia.srl>
# ------------------------------------------------------------------------------

import os
from ftel.vendite.dbtables import FTEL_NOCODE
from anag.clienti import ClientiDialog
from wx.grid import EVT_GRID_CELL_LEFT_DCLICK
def open_dir(f):
    if os.sys.platform.startswith('win'):
        f = f.replace('/', '\\')
    return os.startfile(f)  # @UndefinedVariable

import wx
import awc.controls.windows as aw
import awc.controls.dbgrid as dbglib
from awc.controls.linktable import EVT_LINKTABCHANGED

import ftel.vendite.export_wdr as wdr
import ftel.vendite.dbtables as dbfe

import Env
import report as rpt

from ftel.vendite.export import ExportGrid, ExportPanel

FRAME_TITLE = "Esportazione documenti in formato Fattura Elettronica"


class NotifichePanel(ExportPanel):
    
    GridClass = ExportGrid
    window_filler = wdr.FtelNotificheFunc
    report_name = "Documenti fattura elettronica"
    
    def __init__(self, parent):
        
        aw.Panel.__init__(self, parent)
        self.window_filler(self)
        cn = self.FindWindowByName
        
        self.dbdocs = dbfe.FatturaElettronica()
        self.gridocs = self.GridClass(cn('pangridocs'), self.dbdocs)
        
        self.init_colors()
        
        self.UpdateData()
        
        for name, func in (('butric', self.OnRiceviNotifiche),):
            c = cn(name)
            if c:
                self.Bind(wx.EVT_BUTTON, func, c)
    
    def OnRiceviNotifiche(self, event):
        self.RiceviNotifiche()
        self.UpdateData()
    
#     def _get_values(self):
#         cn = self.FindWindowByName
#         data1, data2 = map(lambda x: cn(x).GetValue(), 'data1 data2'.split())
#         if data1 is None:
#             err = 'Manca la data di partenza'
#         elif data2 is None:
#             err = 'Manca la data di fine'
#         else:
#             err = None
#         if err:
#             aw.awu.MsgDialog(self, "Dati errati:\n%s" % err, style=wx.ICON_ERROR)
#             return None
#         return data1, data2
#     
    def UpdateData(self):
        cn = self.FindWindowByName
        docs = self.dbdocs
        docs.ClearFilters()
        docs.AddFilter('doc.ftel_eeb_status IN ("A", "Q", "M", "E")')
        docs.ClearOrders()
        docs.AddOrder('doc.datdoc')
        docs.AddOrder('doc.id_tipdoc')
        docs.AddOrder('doc.numdoc')
        wx.BeginBusyCursor()
        try:
            docs.Retrieve()
        finally:
            wx.EndBusyCursor()
        self.gridocs.ChangeData(docs.GetRecordset())
        cn('butric').Enable(not docs.IsEmpty())
    
    def RiceviNotifiche(self):
        
        if self.dbdocs.IsEmpty():
            aw.awu.MsgDialog(self, "Nessun documento trovato\nper la ricezione delle notifiche")
            return False
        
        msg = """Confermando, verrà avviata la connessione al gateway per la ricezione """\
              """delle notifiche di avvenuta consegna dei documenti trasmessi.\n\n"""\
              """Confermi la connessione e l'acquisizione ?\n"""
        
        if aw.awu.MsgDialog(self, msg, style=wx.ICON_QUESTION | wx.YES_NO | wx.NO_DEFAULT) == wx.ID_YES:
            
            col = self.dbdocs._GetFieldIndex('id', inline=True)
            docids = [r[col] for r in self.dbdocs._info.rs]# if d.fe_sel]
            
            wait = aw.awu.WaitDialog(self, title="Trasmissione in corso...", maximum=len(docids))
            try:
                doc = dbfe.FatturaElettronica()
                for n, id_doc in enumerate(docids):
                    doc.Get(id_doc)
                    wait.SetMessage('%s n. %s del %s' % (doc.config.descriz,
                                                         doc.numdoc,
                                                         doc.datdoc.Format()))
                    response = doc.gateway_receive_notif()
                    if response['result'] == "OK":
                        status_gw = response['status']
                        if status_gw == "Q":
                            status = doc.STATUS_IN_CODA_X_SDI
                        elif status_gw == "A":
                            status = doc.STATUS_ATTESA_ESITO
                        elif status_gw == "C":
                            status = doc.STATUS_CONSEGNATO
                        elif status_gw == "M":
                            status = doc.STATUS_MANCATACONS
                        elif status_gw == "E":
                            status = doc.STATUS_ERRORE
                        else:
                            raise Exception("Status da gateway non riconosciuto: %s" % status_gw)
                        cmd = "UPDATE movmag_h SET ftel_eeb_status='%s' WHERE id=%s" % (status, doc.id)
                        doc._info.db.Execute(cmd)
                    else:
                        raise Exception("Errore su gateway:\n%s" % response['error'])
                    wait.SetValue(n)
            except Exception, e:
                aw.awu.MsgDialog(self, message=' '.join(map(str, e.args)), style=wx.ICON_ERROR)
            finally:
                wait.Destroy()
            
            return True
        
        return False


class NotificheFrame(aw.Frame):
    
    Panel = NotifichePanel
    
    def __init__(self, *args, **kwargs):
        if not 'title' in kwargs:
            kwargs['title'] = FRAME_TITLE
        aw.Frame.__init__(self, *args, **kwargs)
        self.panel = self.Panel(self)
        self.AddSizedPanel(self.panel)
