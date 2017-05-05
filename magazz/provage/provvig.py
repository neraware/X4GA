#!/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         magazz/provage/provvig.py
# Author:       Fabio Cassini <fabio.cassini@gmail.com>
# Copyright:    (C) 2011 Astra S.r.l. C.so Cavallotti, 122 18038 Sanremo (IM)
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

import magazz.provage.dbtables as dbp

import magazz.provage.provvig_wdr as wdr

import Env
bt = Env.Azienda.BaseTab

import report as rpt


FRAME_TITLE = "Provvigioni Agenti"


class ProvvigAgentiDetGrid(dbglib.DbGridColoriAlternati):
    rpt_name = 'Provvigioni Agenti - Dettaglio Movimenti'
    
    def __init__(self, parent, dbprov):
        
        self.dbprov = dbprov
        
        coldef = self.GetColDef()
        sizes =  [c[0] for c in coldef]
        colmap = [c[1] for c in coldef]
        
        dbglib.DbGridColoriAlternati.__init__(self, 
                                              parent, 
                                              size=parent.GetClientSizeTuple())
        
        self.SetData(dbprov.GetRecordset(), colmap)
        
        self.SetTotali()
        
        for c,s in enumerate(sizes):
            self.SetColumnDefaultSize(c,s)
        self._SetFitColumn()
        self.AutoSizeColumns()
        sz = wx.FlexGridSizer(1,0,0,0)
        sz.AddGrowableCol( 0 )
        sz.AddGrowableRow( 0 )
        sz.Add(self, 0, wx.GROW|wx.ALL, 0)
        parent.SetSizer(sz)
        sz.SetSizeHints(parent)
    
    def GetColDef(self):
        
        def cn(col):
            return self.dbprov._GetFieldIndex(col, inline=True)
        
        _STR = gl.GRID_VALUE_STRING
        _DAT = gl.GRID_VALUE_DATETIME
        _QTA = bt.GetMagQtaMaskInfo()
        _PRE = bt.GetMagPreMaskInfo()
        _SCO = bt.GetMagScoMaskInfo()
        _VAL = bt.GetValIntMaskInfo()
        
        cols = []
        a = cols.append
        a(( 40, (cn('age_codice'),     "Cod.",         _STR, False)))
        a((120, (cn('age_descriz'),    "Agente",       _STR, False)))
        a(( 40, (cn('tipdoc_codice'),  "Cod.",         _STR, False)))
        a((110, (cn('tipdoc_descriz'), "Documento",    _STR, False)))
        a(( 50, (cn('doc_numdoc'),     "Num.",         _STR, False)))
        a(( 80, (cn('doc_datdoc'),     "Data",         _DAT, False)))
        a(( 40, (cn('pdc_codice'),     "Cod.",         _STR, False)))
        a((200, (cn('pdc_descriz'),    "Cliente",      _STR, False)))
        a((100, (cn('prod_codice'),    "Cod.",         _STR, False)))
        a((200, (cn('mov_descriz'),    "Descrizione",  _STR, False)))
        a(( 90, (cn('mov_qta'),        "Qta",          _QTA, False)))
        a(( 90, (cn('mov_prezzo'),     "Prezzo",       _PRE, False)))
        if bt.MAGNUMSCO >= 1:
            a(( 50, (cn('mov_sconto1'),    "Sc.%"+'1'*int(bt.MAGNUMSCO>1), _SCO, False)))
        if bt.MAGNUMSCO >= 2:
            a(( 50, (cn('mov_sconto2'),    "Sc.%2",    _SCO, False)))
        if bt.MAGNUMSCO >= 3:
            a(( 50, (cn('mov_sconto3'),    "Sc.%3",    _SCO, False)))
        if bt.MAGNUMSCO >= 4:
            a(( 50, (cn('mov_sconto4'),    "Sc.%4",    _SCO, False)))
        if bt.MAGNUMSCO >= 5:
            a(( 50, (cn('mov_sconto5'),    "Sc.%5",    _SCO, False)))
        if bt.MAGNUMSCO >= 6:
            a(( 50, (cn('mov_sconto6'),    "Sc.%6",    _SCO, False)))
        a((110, (cn('total_vendita'),  "Vendita",      _VAL, False)))
        a(( 40, (cn('aliqiva_codice'), "Aliq.",        _STR, False)))
        a(( 50, (cn('avg_perpro'),     "Prov.%.",      _SCO, False)))
        a((110, (cn('total_provvig'),  "Provvig.",     _VAL, False)))
        a(( 40, (cn('dest_codice'),    "Cod.",         _STR, False)))
        a((200, (cn('dest_descriz'),   "Destinatario", _STR, False)))
        a((  1, (cn('mov_id'),         "#mov",         _STR, False)))
        a((  1, (cn('mov_id_doc'),     "#doc",         _STR, False)))
        a((  1, (cn('pdc_id'),         "#pdc",         _STR, False)))
        a((  1, (cn('prod_id'),        "#pro",         _STR, False)))
        
        return cols
    
    def _SetFitColumn(self):
        self.SetFitColumn(7)
    
    def SetTotali(self):
        def cn(col):
            return self.dbprov._GetFieldIndex(col)
        self.AddTotalsRow(1, 'Totali', (cn('total_vendita'),
                                        cn('total_provvig'),))
    
    def AskForPageEject(self):
        return aw.awu.MsgDialog(self, "Vuoi un solo agente per ogni pagina?",
                                style=wx.ICON_QUESTION|wx.YES_NO|wx.YES_DEFAULT)


# ------------------------------------------------------------------------------


class ProvvigAgentiTotGrid(ProvvigAgentiDetGrid):
    rpt_name = 'Provvigioni Agenti - Totali Documento'
    
    def GetColDef(self):
        
        def cn(col):
            return self.dbprov._GetFieldIndex(col, inline=True)
        
        _STR = gl.GRID_VALUE_STRING
        _DAT = gl.GRID_VALUE_DATETIME
        _VAL = bt.GetValIntMaskInfo()
        _SCO = bt.GetPerGenMaskInfo()
        
        return (\
            ( 40, (cn('age_codice'),     "Cod.",         _STR, False)),
            (120, (cn('age_descriz'),    "Agente",       _STR, False)),
            ( 40, (cn('tipdoc_codice'),  "Cod.",         _STR, False)),
            (110, (cn('tipdoc_descriz'), "Documento",    _STR, False)),
            ( 50, (cn('doc_numdoc'),     "Num.",         _STR, False)),
            ( 80, (cn('doc_datdoc'),     "Data",         _DAT, False)),
            ( 40, (cn('pdc_codice'),     "Cod.",         _STR, False)),
            (200, (cn('pdc_descriz'),    "Cliente",      _STR, False)),
            ( 40, (cn('dest_codice'),    "Cod.",         _STR, False)),
            (200, (cn('dest_descriz'),   "Destinatario", _STR, False)),
            (110, (cn('total_vendita'),  "Vendita",      _VAL, False)),
            ( 50, (cn('avg_perpro'),     "Prov.%.",      _SCO, False)),
            (110, (cn('total_provvig'),  "Provvig.",     _VAL, False)),
            (  1, (cn('doc_id'),         "#doc",         _STR, False)),
            (  1, (cn('pdc_id'),         "#pdc",         _STR, False)),
        )
    
    def AskForPageEject(self):
        return aw.awu.MsgDialog(self, "Vuoi un solo agente per ogni pagina?",
                                style=wx.ICON_QUESTION|wx.YES_NO|wx.NO_DEFAULT)


# ------------------------------------------------------------------------------


class ProvvigAgentiPanel(wx.Panel):
    
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        wdr.ProvvigAgentiFunc(self)
        cn = self.FindWindowByName
        self.gridmov = None
        self.InitGrid()
        for name, func in (('butupdate', self.OnUpdateData),
                           ('butprint', self.OnPrintData),):
            self.Bind(wx.EVT_BUTTON, func, cn(name))
    
    def InitGrid(self):
        if self.gridmov is not None:
#            self.gridmov.Destroy()
            wx.CallAfter(self.gridmov.Destroy)
        cn = self.FindWindowByName
        if cn('dettrighe').IsChecked():
            self.dbprov = dbp.ProvvigAgentiDetTable()
            self.gridmov = ProvvigAgentiDetGrid(cn('pangridmov'), self.dbprov)
        else:
            self.dbprov = dbp.ProvvigAgentiTotTable()
            self.gridmov = ProvvigAgentiTotGrid(cn('pangridmov'), self.dbprov)
        
    def OnUpdateData(self, event):
        self.InitGrid()
        self.UpdateData()
        event.Skip()
    
    def OnPrintData(self, event):
        self.PrintData()
    
    def UpdateData(self):
        dbprov = self.dbprov
        dbprov.ClearFilters()
        cn = self.FindWindowByName
        v = cn('agente1').GetValueCod()
        if v:
            dbprov.AddFilter('age.codice>=%s', v)
        v = cn('agente2').GetValueCod()
        if v:
            dbprov.AddFilter('age.codice<=%s', v)
        v = cn('datdoc1').GetValue()
        if v:
            dbprov.AddFilter('doc.datdoc>=%s', v)
        v = cn('datdoc2').GetValue()
        if v:
            dbprov.AddFilter('doc.datdoc<=%s', v)
        if cn('solosaldati').IsChecked():
            dbprov.AddHaving('total_saldo IS NULL OR total_saldo=0')
        wx.BeginBusyCursor()
        try:
            dbprov.Retrieve()
        finally:
            wx.EndBusyCursor()
        self.gridmov.ChangeData(dbprov.GetRecordset())
    
    def PrintData(self):
#        db = self.dbprov
#        cn = self.FindWindowByName
#        for name in 'datdoc1 datdoc2 solosaldati'.split():
#            db.SetPrintValue(name, cn(name).GetValue())
#        cpp = self.gridmov.AskForPageEject() == wx.ID_YES
#        def setCPP(rptdef, dbt):
#            groups = rptdef.lGroup
#            for g in groups:
#                if groups[g].name == 'agente':
#                    if cpp:
#                        snp = 'true'
#                    else:
#                        snp = 'false'
#                    groups[g].isStartNewPage = snp
#        rpt.Report(self, db, self.gridmov.rpt_name, startFunc=setCPP)
        db = self.dbprov
        cn = self.FindWindowByName
        for name in 'datdoc1 datdoc2 solosaldati'.split():
            db.SetPrintValue(name, cn(name).GetValue())
        def setCPP(rptdef, dbt):
            groups = rptdef.lGroup
            for g in groups:
                if groups[g].name == 'agente':
                    if cn('agepag').IsChecked():
                        snp = 'true'
                    else:
                        snp = 'false'
                    groups[g].isStartNewPage = snp
        rpt.Report(self, db, self.gridmov.rpt_name, startFunc=setCPP)


# ------------------------------------------------------------------------------


class ProvvigAgentiFrame(aw.Frame):
    
    def __init__(self, *args, **kwargs):
        if not 'title' in kwargs:
            kwargs['title'] = FRAME_TITLE
        aw.Frame.__init__(self, *args, **kwargs)
        self.panel = ProvvigAgentiPanel(self)
        self.AddSizedPanel(self.panel)



import anag.lib as alib

_evtDOC_CHANGED = wx.NewEventType()
EVT_DOC_CHANGED = wx.PyEventBinder(_evtDOC_CHANGED, 0)
class DocChangedEvent(wx.PyCommandEvent):
    def __init__(self, id_doc):
        wx.PyCommandEvent.__init__(self, _evtDOC_CHANGED)
        self.id_doc = id_doc

class ModificaProvvigAgentiDocGrid(dbglib.ADB_Grid):
    
    def __init__(self, parent, dbdoc):
        
        dbglib.ADB_Grid.__init__(self, parent, db_table=dbdoc, can_edit=True, can_insert=False)
        
        self.dbdoc = dbdoc
        doc = dbdoc
        tpd = doc.tipdoc
        age = doc.agente
        pdc = doc.pdc
        
        def ci(tab, col):
            return tab._GetFieldIndex(col, inline=True)
        
        self.COL_CODCAU = self.AddColumn(tpd, 'codice', 'Cod.', col_width=35)
        self.COL_DESCAU = self.AddColumn(tpd, 'descriz', 'Documento', col_width=120)
        self.COL_NUMDOC = self.AddColumn(doc, 'numdoc', 'Num.', col_type=self.TypeInteger(5))
        self.COL_DATDOC = self.AddColumn(doc, 'datdoc', 'Data', col_type=self.TypeDate())
        self.COL_CODPDC = self.AddColumn(pdc, 'codice', 'Cod.', col_width=50)
        self.COL_DESPDC = self.AddColumn(pdc, 'descriz', 'Cliente', col_width=200, is_fittable=True)
        
        self.COL_CODAGE = self.AddColumn(age, 'codice',  'Cod.', col_width=40, is_editable=True, 
                                           linktable_info={'class':   alib.LinkTableAgente,
                                                           'col_id':  ci(doc, 'id_agente'),
                                                           'col_cod': ci(age, 'codice'),
                                                           'col_des': ci(age, 'descriz')})
        
        self.COL_DESAGE = self.AddColumn(age, 'descriz', 'Agente', col_width=120)
        
        self.COL_ID_DOC = self.AddColumn(doc, 'id', '#doc', col_width=1)
        self.COL_ID_AGE = self.AddColumn(age, 'id', '#age', col_width=1)
        
        self.CreateGrid()
        
        self._last_row = -1
    
    def OnCellSelect(self, event):
        dbglib.ADB_Grid.OnCellSelect(self, event)
        row = event.GetRow()
        if row != self._last_row:
            self._last_row = row
            doc = self.dbdoc
            doc.MoveRow(row)
            e = DocChangedEvent(doc.id)
            self.GetEventHandler().AddPendingEvent(e)
            self.SelectRow(row)
    
    def ChangeData(self, *args, **kwargs):
        dbglib.ADB_Grid.ChangeData(self, *args, **kwargs)
        self._last_row = -1
    
    def CellEditAfterUpdate(self, row, gridcol, col, value):
        if gridcol == self.COL_CODAGE:
            doc = self.dbdoc
            doc.MoveRow(row)
            db = dbp.adb.db.get_db()
            if not db.Execute("UPDATE movmag_h SET id_agente=%d WHERE id=%d" % (value, doc.id)):
                aw.awu.MsgDialog(self, repr(db.dbError.description), style=wx.ICON_ERROR)
        return dbglib.ADB_Grid.CellEditAfterUpdate(self, row, gridcol, col, value)


class ModificaProvvigAgentiMovGrid(dbglib.ADB_Grid):
    
    def __init__(self, parent, dbmov):
        
        dbglib.ADB_Grid.__init__(self, parent, db_table=dbmov, can_edit=True, can_insert=False)
        
        self.dbmov = dbmov
        mov = dbmov
        tpm = mov.tipmov
        pro = mov.prod
        iva = mov.aliqiva
        
        def ci(tab, col):
            return tab._GetFieldIndex(col, inline=True)
        
        IQM, DQM = bt.MAGQTA_INTEGERS, bt.MAGQTA_DECIMALS
        IPM, DPM = bt.MAGPRE_INTEGERS, bt.MAGPRE_DECIMALS
        IVI, DVI = bt.VALINT_INTEGERS, bt.VALINT_DECIMALS
        
        self.COL_CODTPM = self.AddColumn(tpm, 'codice', 'TPM', col_width=35)
        self.COL_CODART = self.AddColumn(pro, 'codice', 'Cod.', col_width=90)
        self.COL_DESCRI = self.AddColumn(mov, 'descriz', 'Descrizione', col_width=150, is_fittable=True)
        self.COL_QTA =    self.AddColumn(mov, 'qta', 'Qta', col_type=self.TypeFloat(IQM, DQM))
        self.COL_PREZZO = self.AddColumn(mov, 'prezzo', 'Prezzo', col_type=self.TypeFloat(IPM, DPM))
        
        if bt.MAGNUMSCO >= 1:
            self.COL_SCONTO1 = self.AddColumn(mov, 'sconto1', 'Sc.%1', col_type=self.TypeFloat(2, 2))
        else:
            self.COL_SCONTO1 = -1
        
        if bt.MAGNUMSCO >= 2:
            self.COL_SCONTO2 = self.AddColumn(mov, 'sconto2', 'Sc.%2', col_type=self.TypeFloat(2, 2))
        else:
            self.COL_SCONTO2 = -1
        
        if bt.MAGNUMSCO >= 3:
            self.COL_SCONTO3 = self.AddColumn(mov, 'sconto3', 'Sc.%3', col_type=self.TypeFloat(2, 2))
        else:
            self.COL_SCONTO3 = -1
        
        if bt.MAGNUMSCO >= 4:
            self.COL_SCONTO4 = self.AddColumn(mov, 'sconto4', 'Sc.%4', col_type=self.TypeFloat(2, 2))
        else:
            self.COL_SCONTO4 = -1
        
        if bt.MAGNUMSCO >= 5:
            self.COL_SCONTO5 = self.AddColumn(mov, 'sconto5', 'Sc.%5', col_type=self.TypeFloat(2, 2))
        else:
            self.COL_SCONTO5 = -1
        
        if bt.MAGNUMSCO >= 6:
            self.COL_SCONTO6 = self.AddColumn(mov, 'sconto6', 'Sc.%6', col_type=self.TypeFloat(2, 2))
        else:
            self.COL_SCONTO6 = -1
        
        self.COL_CODIVA = self.AddColumn(iva, 'codice', 'IVA', col_width=35)
        self.COL_PERPRO = self.AddColumn(mov, 'perpro', 'Prov.%', col_type=self.TypeFloat(2, 2), is_editable=True)
        
        self.COL_ID_MOV = self.AddColumn(mov, 'id', '#mov', col_width=1)
        self.COL_ID_PRO = self.AddColumn(pro, 'id', '#pro', col_width=1)
        
        self.CreateGrid()
    
    def CellEditAfterUpdate(self, row, gridcol, col, value):
        if gridcol == self.COL_PERPRO:
            mov = self.dbmov
            mov.MoveRow(row)
            db = dbp.adb.db.get_db()
            if not db.Execute("UPDATE movmag_b SET perpro=%s WHERE id=%d" % (value, mov.id)):
                aw.awu.MsgDialog(self, repr(db.dbError.description), style=wx.ICON_ERROR)
        return dbglib.ADB_Grid.CellEditAfterUpdate(self, row, gridcol, col, value)


class ModificaProvvigAgentiPanel(wx.Panel):
    
    def __init__(self, *args, **kwargs):
        
        wx.Panel.__init__(self, *args, **kwargs)
        wdr.ModificaProvvigioniFunc(self)
        cn = self.FindWindowByName
        
        self.dbdoc = dbp.ModificaProvvigAgentiDocTable()
        self.griddoc = ModificaProvvigAgentiDocGrid(cn('pangriddoc'), self.dbdoc)
        
        self.dbmov = dbp.ModificaProvvigAgentiMovTable()
        self.gridmov = ModificaProvvigAgentiMovGrid(cn('pangridmov'), self.dbmov)
        
        self.Bind(EVT_DOC_CHANGED, self.OnDocChanged)
        for name, func in (('butupdate', self.OnUpdateData),):
            self.Bind(wx.EVT_BUTTON, func, cn(name))
    
    def OnDocChanged(self, event):
        mov = self.dbmov
        mov.Retrieve('mov.id_doc=%s' % event.id_doc)
        self.gridmov.ChangeData(mov.GetRecordset())
    
    def OnUpdateData(self, event):
        self.UpdateData()
        event.Skip()
    
    def UpdateData(self):
        doc = self.dbdoc
        doc.ClearFilters()
        cn = self.FindWindowByName
        v = cn('agente1').GetValueCod()
        if v:
            doc.AddFilter('agente.codice>=%s', v)
        v = cn('agente2').GetValueCod()
        if v:
            doc.AddFilter('agente.codice<=%s', v)
        v = cn('datdoc1').GetValue()
        if v:
            doc.AddFilter('doc.datdoc>=%s', v)
        v = cn('datdoc2').GetValue()
        if v:
            doc.AddFilter('doc.datdoc<=%s', v)
        td = cn('id_tipdoc').GetValue()
        if td:
            doc.AddFilter('doc.id_tipdoc=%s' % td)
        wx.BeginBusyCursor()
        try:
            doc.Retrieve()
        finally:
            wx.EndBusyCursor()
        self.griddoc.ChangeData(doc.GetRecordset())


class ModificaProvvigAgentiFrame(aw.Frame):
    
    def __init__(self, *args, **kwargs):
        if not 'title' in kwargs:
            kwargs['title'] = "Modifica %s" % FRAME_TITLE
        aw.Frame.__init__(self, *args, **kwargs)
        self.panel = ModificaProvvigAgentiPanel(self)
        self.AddSizedPanel(self.panel)
