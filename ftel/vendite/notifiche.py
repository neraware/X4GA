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
import datetime
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

from ftel.vendite.export import ExportGrid, ExportPanel, DettaglioScartoDialog

FRAME_TITLE = "Esportazione documenti in formato Fattura Elettronica"


class NotifichePanel(ExportPanel):
    
    window_filler = wdr.FtelNotificheFunc
    report_name = "Documenti fattura elettronica"
    
    def __init__(self, parent):
        
        aw.Panel.__init__(self, parent)
        self.window_filler(self)
        cn = self.FindWindowByName
        
        self.dbdocs = dbfe.FatturaElettronica()
        self.gridocs = ExportGrid(cn('pangridocs'), self.dbdocs)
        
        self.init_colors()
        
        self.UpdateData()
        
        for name, func in (('butric', self.OnRiceviNotifiche),):
            c = cn(name)
            if c:
                self.Bind(wx.EVT_BUTTON, func, c)
        
        self.gridocs.Bind(EVT_GRID_CELL_LEFT_DCLICK, self.OnCellDoubleClicked)
    
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
        date_start_pa = datetime.date.today() - datetime.timedelta(days=30)
        cn = self.FindWindowByName
        docs = self.dbdocs
        docs.ClearFilters()
        docs.AddFilter('doc.ftel_eeb_status IN ("A", "Q", "E") ' \
                    + 'OR (doc.ftel_eeb_status="C" ' \
                    + '    AND LENGTH(pdc.ftel_codice)=6 ' \
                    + '    AND doc.datdoc>="%s")' % date_start_pa.strftime('%Y-%m-%d'))
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
            docids = [r[col] for r in self.dbdocs._info.rs]
            
            wait = aw.awu.WaitDialog(self, title="Ricezione in corso...", maximum=len(docids))
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
                        elif status_gw == "Z":
                            status = doc.STATUS_PA_ACCETTATI
                        elif status_gw == "K":
                            status = doc.STATUS_PA_RIFIUTATI
                        elif status_gw == "T":
                            status = doc.STATUS_PA_DECOTERM
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
    
    def OnCellDoubleClicked(self, event):
        row, col = event.GetRow(), event.GetCol()
        doc = self.dbdocs
        doc.MoveRow(row)
        if Env.Azienda.BaseTab.is_eeb_enabled() and col == self.gridocs.COL_MESSAG:
            if doc.ftel_eeb_status == "E":
                dettaglio_scarto = doc.gateway_receive_dettaglio_scarto()
                dlg = DettaglioScartoDialog(self, dettaglio_scarto=[ds['error_desc'] for ds in dettaglio_scarto])
                dlg.ShowModal()
                dlg.Destroy()
        event.Skip()


class NotificheFrame(aw.Frame):
    
    Panel = NotifichePanel
    
    def __init__(self, *args, **kwargs):
        if not 'title' in kwargs:
            kwargs['title'] = FRAME_TITLE
        aw.Frame.__init__(self, *args, **kwargs)
        self.panel = self.Panel(self)
        self.AddSizedPanel(self.panel)
