#!/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         ftel/acquisti/acquis.py
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
import awc.controls.dbgrid as dbglib
import wx.grid as gl

import ftel.acquisti.acquis_wdr as wdr
import ftel.acquisti.dbtables as dbftel

from Env import Azienda
from contab.dataentry_i_o import ContabDialogTipo_I_O
import Env
import cStringIO
import tempfile
import os
from ftel.acquisti.dbtables import RigheDbMem
bt = Azienda.BaseTab


FRAME_TITLE = "Importazione Fatture Elettroniche"


class ElencoFilesGrid(dbglib.ADB_Grid):
    
    def __init__(self, parent, dblist):
        
        dbglib.ADB_Grid.__init__(self, parent, db_table=dblist)
        
        self.dblist = dblist
        
        IVI, DVI = bt.VALINT_INTEGERS, bt.VALINT_DECIMALS
        
        self.AddColumn(dblist, 'filename',  'Nome file', col_width=150)
        self.AddColumn(dblist, 'pdc_codice',  'Cod.', col_width=50)
        self.AddColumn(dblist, 'pdc_descriz',  'Fornitore', col_width=200, is_fittable=True)
        self.AddColumn(dblist, 'tipdoc',  'Doc.', col_width=50)
        self.AddColumn(dblist, 'datdoc',  'Data', col_type=self.TypeDate())
        self.AddColumn(dblist, 'numdoc',  'Num.', col_width=60)
        self.AddColumn(dblist, 'totdoc',  'Tot.Documento', col_type=self.TypeFloat(IVI, DVI))
        
        self.CreateGrid()


class FtelAcquisPanel(aw.Panel):
    
    def __init__(self, *args, **kwargs):
        aw.Panel.__init__(self, *args, **kwargs)
        wdr.ElencoFilesFunc(self)
        cn = self.FindWindowByName
        self.dblist = dbftel.ElencoFiles()
        self.gridlist = ElencoFilesGrid(cn('pangridlist'), self.dblist)
        self.update_list()
        self.Bind(wx.EVT_BUTTON, self.OnUpdateList, cn('butrefresh'))
        self.Bind(gl.EVT_GRID_CELL_LEFT_DCLICK, self.OnAcquisFile, self.gridlist)
    
    def OnAcquisFile(self, event):
        row = event.GetRow()
        self.dblist.MoveRow(row)
        self.AcquisFile(self.dblist)
        event.Skip()
    
    def AcquisFile(self, rowlist):
        cf = rowlist.docxml.anag_cliente.codfisc
        pi = rowlist.docxml.anag_cliente.piva
        if (cf and cf != Env.Azienda.codfisc) or (pi and pi != Env.Azienda.piva):
            if cf:
                msg = "Il documento è destinato al cod.fiscale %s\nImpossibile procedere." % cf
            else:
                msg = "Il documento è destinato alla p.iva %s\nImpossibile procedere." % pi
            aw.awu.MsgDialog(self, msg, style=wx.ICON_ERROR)
            return
        show_pdf(rowlist.docxml, rowlist.filename)
        dlg = ContabDialogTipo_I_O(self, ftel_acq_info=rowlist)
        done = dlg.ShowModal() == wx.ID_OK
        dlg.Destroy()
        if done:
            rowlist.archive_file()
            self.update_list()
    
    def OnUpdateList(self, event):
        self.update_list()
        event.Skip()
    
    def update_list(self):
        wx.BeginBusyCursor()
        try:
            self.dblist.update_list()
            self.gridlist.ChangeData(self.dblist.GetRecordset())
        finally:
            wx.EndBusyCursor()


class FtelAcquisFrame(aw.Frame):
    
    def __init__(self, *args, **kwargs):
        if not kwargs.has_key('title') and len(args) < 3:
            kwargs['title'] = FRAME_TITLE
        aw.Frame.__init__(self, *args, **kwargs)
        self.AddSizedPanel(FtelAcquisPanel(self))


def show_pdf(xmldoc, filename):
    
    pdf_stream = None
    doc = xmldoc.docs[0]
    
    if doc.allegati:
        #pdf embedded
        pdf_stream = doc.allegati[0].stream
    
    if not pdf_stream:
        
        #pdf non presente nel file xml, ne genero uno al volo partendo da un layout generico
        
        doc.anag_fornit = xmldoc.anag_fornit
        doc.anag_cliente = xmldoc.anag_cliente
        doc.filename = filename
        doc._numdecqta, doc._numdecpre = doc.get_qta_prezzo_decimals()
        
        data = RigheDbMem()
        for riga in doc.righe:
            data.CreateNewRow()
            data.numriga = riga.numriga
            data.codart = riga.codart
            data.descriz = riga.descriz
            data.qta = riga.qta
            data.unimis = riga.unimis
            data.prezzo = riga.prezzo
            data.sconto_per = riga.sconto_per
            data.sconto_val = riga.sconto_val
            data.totale = riga.totale
            data.aliqiva = riga.aliqiva
        
        data.doc = doc
        
        pdf_out = cStringIO.StringIO()
        name = 'ftel_generic'
        import report as rpt
        rpt.Report(None, data, name, pdf_out, output="STORE")
        pdf_out.seek(0)
        pdf_stream = pdf_out.read()
        pdf_out.close()
    
    if not pdf_stream:
        raise Exception("No PDF")
    
    tmpfile = tempfile.NamedTemporaryFile(suffix='.pdf')
    tmpname = tmpfile.name
    tmpfile.close()
    wx.GetApp().AppendTempFile(tmpname)
    tmpfile = open(tmpname, 'wb')
    tmpfile.write(pdf_stream)
    tmpfile.close()
    os.startfile(tmpname)
