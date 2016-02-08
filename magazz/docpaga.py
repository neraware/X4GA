# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         magazz/docpaga.py
# Author:       Fabio Cassini <fabio.cassini@gmail.com>
# Copyright:    (C) 2016 Neraware s.a.s. di Fabio Cassini & C.
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
import wx.grid as gl
import awc.controls.dbgrid as dbglib
import awc.controls.windows as aw
from awc.controls.linktable import EVT_LINKTABCHANGED

import magazz.docint_wdr as wdr

import magazz
import magazz.dbtables as dbm

import report as rpt

import Env
bt = Env.Azienda.BaseTab


FRAME_TITLE = "Documenti stato pagamento"


class DocPagaGrid(dbglib.ADB_Grid):
    
    def __init__(self, parent, dbdoc):
        
        dbglib.ADB_Grid.__init__(self, parent, db_table=dbdoc, on_menu_select='row')
        
        self.dbdoc = doc = dbdoc
        
        IVI = bt.VALINT_INTEGERS
        DVI = bt.VALINT_DECIMALS
        col_imp = self.TypeFloat(IVI, DVI)
        
        self.COL_TPDCOD = self.AddColumn(doc, 'tpd_cod', 'Cod.', col_width=35)
        self.COL_TPDCOD = self.AddColumn(doc, 'tpd_des', 'Causale', col_width=120)
        self.COL_NUMDOC = self.AddColumn(doc, 'numdoc',  'Num.', col_width=50)
        self.COL_DATDOC = self.AddColumn(doc, 'datdoc',  'Data', col_type=self.TypeDate())
        self.COL_PDCCOD = self.AddColumn(doc, 'pdc_cod', 'Cod.', col_width=50)
        self.COL_PDCDES = self.AddColumn(doc, 'pdc_des', 'Anagrafica', col_width=200, is_fittable=True)
        self.COL_DSTIND = self.AddColumn(doc, 'dst_ind', 'Indirizzo', col_width=120)
        self.COL_DSTCIT = self.AddColumn(doc, 'dst_cit', 'Città', col_width=90)
        self.COL_QTAORD = self.AddColumn(doc, 'totdare',  'Tot.Dare', col_type=col_imp)
        self.COL_QTAORD = self.AddColumn(doc, 'saldo',    'Saldo', col_type=col_imp)
        self.AddColumn(doc, 'doc_id', '#doc', col_width=1)
        
        self.CreateGrid()


class DocPagaPanel(aw.Panel):
    
    def __init__(self, *args, **kwargs):
        aw.Panel.__init__(self, *args, **kwargs)
        wdr.DocumentiPagatiFunc(self)
        cn = self.FindWindowByName
        self.dbdoc = dbm.DocumentiPagati()
        self.gridocs = DocPagaGrid(cn('pangridocs'), self.dbdoc)
        tpd = dbm.adb.DbTable('cfgmagdoc', 'tpd')
        cau = tpd.AddJoin('cfgcontab', 'cau', idLeft='id_caucg')
        cau.AddJoin('regiva', 'riv', idLeft='id_regiva')
        tpd.AddFilter('riv.tipo="V"')
        tpd.Retrieve()
        if tpd.IsEmpty():
            f = 'FALSE'
        else:
            f = 'id IN (%s)' % ','.join(map(str, [tpd.id for _ in tpd]))
        cn('id_tipdoc').SetFilter(f)
        for name, func in (('butupd', self.OnUpdateData),
                           ('butprt', self.OnPrintData),):
            self.Bind(wx.EVT_BUTTON, func, cn(name))
    
    def OnUpdateData(self, event):
        if self.Validate():
            self.UpdateData()
            event.Skip()
    
    def Validate(self):
        cn = self.FindWindowByName
        datdoc1 = cn('datdoc1').GetValue()
        datdoc2 = cn('datdoc2').GetValue()
        id_tipdoc = cn('id_tipdoc').GetValue()
        paga_si = cn('paga_si').IsChecked()
        paga_no = cn('paga_no').IsChecked()
        err = None
        if datdoc1 is None or datdoc2 is None:
            err = 'Definire entrambe le date documento'
        elif id_tipdoc is None:
            err = 'Definire la causale'
        elif not paga_si and not paga_no:
            err = 'Selezionare almeno una delle scelte documenti pagati si/no'
        if err:
            aw.awu.MsgDialog(self, err, style=wx.ICON_ERROR)
        return bool(not err)
    
    def UpdateData(self):
        cn = self.FindWindowByName
        datdoc1 = cn('datdoc1').GetValue()
        datdoc2 = cn('datdoc2').GetValue()
        id_tipdoc = cn('id_tipdoc').GetValue()
        id_agente = cn('id_agente').GetValue()
        id_catcli = cn('id_catcli').GetValue()
        paga_si = cn('paga_si').IsChecked()
        paga_no = cn('paga_no').IsChecked()
        doc = self.dbdoc
        wx.BeginBusyCursor()
        try:
            doc.update_data(id_tipdoc, datdoc1, datdoc2, paga_si, paga_no, id_agente, id_catcli)
            self.gridocs.ChangeData(doc.GetRecordset())
        finally:
            wx.EndBusyCursor()
    
    def OnPrintData(self, event):
        if self.Validate():
            self.PrintData()
            event.Skip()
    
    def PrintData(self):
        cn = self.FindWindowByName
        doc = self.dbdoc
        info = doc._info
        info._tpd_cod = cn('id_tipdoc').GetValueCod()
        info._tpd_des = cn('id_tipdoc').GetValueDes()
        info._age_cod = cn('id_agente').GetValueCod()
        info._age_des = cn('id_agente').GetValueDes()
        info._catcli_cod = cn('id_catcli').GetValueCod()
        info._catcli_des = cn('id_catcli').GetValueDes()
        info._datdoc1 = cn('datdoc1').GetValue()
        info._datdoc2 = cn('datdoc2').GetValue()
        rpt.Report(self, doc, 'Stato pagamento documenti')


class DocPagaFrame(aw.Frame):
    def __init__(self, *args, **kwargs):
        if not kwargs.has_key('title') and len(args) < 3:
            kwargs['title'] = FRAME_TITLE
        aw.Frame.__init__(self, *args, **kwargs)
        self.AddSizedPanel(DocPagaPanel(self, -1))
        self.CenterOnScreen()
