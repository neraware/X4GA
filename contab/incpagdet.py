# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         contab/incpagdet.py
# Copyright:    (C) 2015 Fabio Cassini <fc@f4b10.org>
# ------------------------------------------------------------------------------


import wx

import awc.controls.windows as aw
import awc.controls.dbgrid as dbglib

import contab.incpagdet_db as dbc
import contab.incpagdet_wdr as wdr

import report as rpt

import Env


FRAME_TITLE = "Dettaglio delle operazioni in saldaconto"


class ElencoSottocontiGrid(dbglib.ADB_Grid):
    
    def __init__(self, parent, dbcas):
        
        dbglib.ADB_Grid.__init__(self, parent, db_table=dbcas,
                                 can_edit=False, can_insert=False)
        
        cas = self.dbcas = dbcas
        
        def ci(tab, col):
            return tab._GetFieldIndex(col, inline=True)
        
        bt = Env.Azienda.BaseTab
        _IVI, _DVI = bt.VALINT_INTEGERS, bt.VALINT_DECIMALS
        
        self.COL_CODCAS = self.AddColumn(cas, 'codtipana', 'Tipo', col_width=35)
        self.COL_CODCAS = self.AddColumn(cas, 'codice', 'Cod.', col_width=35)
        self.COL_DESCAS = self.AddColumn(cas, 'descriz', 'Sottoconto', col_width=50, is_fittable=True)
        self.COL_ID_CAS = self.AddColumn(cas, 'id', '#cas', col_width=1)
        
        self.CreateGrid()



class ElencoRegistrazioniGrid(dbglib.ADB_Grid):
    
    def __init__(self, parent, dbreg):
        
        dbglib.ADB_Grid.__init__(self, parent, db_table=dbreg,
                                 can_edit=False, can_insert=False)
        
        reg = self.dbreg = dbreg
        
        def ci(tab, col):
            return tab._GetFieldIndex(col, inline=True)
        
        bt = Env.Azienda.BaseTab
        _IVI, _DVI = 8, bt.VALINT_DECIMALS
        
        self.COL_DATREG = self.AddColumn(reg, 'datreg',     'Data reg.', col_type=self.TypeDate())
#         self.COL_CODCAU = self.AddColumn(reg, 'codcausale', 'Cod.', col_width=30)
        self.COL_DESCAU = self.AddColumn(reg, 'descausale', 'Causale', col_width=100)
        self.COL_CODANA = self.AddColumn(reg, 'codanag',    'Cod.', col_width=50)
        self.COL_DESANA = self.AddColumn(reg, 'desanag',    'Anagrafica', col_width=200, is_fittable=True)
        self.COL_DARE =   self.AddColumn(reg, 'dare',       'Dare', col_type=self.TypeFloat(_IVI, _DVI))
        self.COL_AVERE =  self.AddColumn(reg, 'avere',      'Avere', col_type=self.TypeFloat(_IVI, _DVI))
        self.COL_ID_REG = self.AddColumn(reg, 'id_reg',     '#reg', col_width=1)
        self.COL_ID_CAS = self.AddColumn(reg, 'id_cassa',   '#cas', col_width=1)
        self.COL_ID_ANA = self.AddColumn(reg, 'id_anag',    '#ana', col_width=1)
        
        self.CreateGrid()


class DettaglioOperazioniGrid(dbglib.ADB_Grid):
    
    def __init__(self, parent, dbcas):
        
        dbglib.ADB_Grid.__init__(self, parent, db_table=dbcas,
                                 can_edit=False, can_insert=False)
        
        cas = self.dbcas = dbcas
        
        def ci(tab, col):
            return tab._GetFieldIndex(col, inline=True)
        
        bt = Env.Azienda.BaseTab
        _IVI, _DVI = 7, bt.VALINT_DECIMALS
        
        self.COL_OPERAZ = self.AddColumn(cas, 'importo',   'Importo', col_type=self.TypeFloat(_IVI, _DVI))
        self.COL_CODCAP = self.AddColumn(cas, 'descaudoc', 'Caus.', col_width=90)
        self.COL_DATREG = self.AddColumn(cas, 'numdoc',    'Num.', col_width=50)
        self.COL_DATDOC = self.AddColumn(cas, 'datdoc',    'Data doc.', col_type=self.TypeDate())
        self.COL_ABBUON = self.AddColumn(cas, 'abbuono',   'Abb.', col_type=self.TypeFloat(3, _DVI))
        self.COL_TIPABB = self.AddColumn(cas, 'tipabb',    'AP', col_width=20)
        self.COL_SPESE =  self.AddColumn(cas, 'spesa',     'Spese', col_type=self.TypeFloat(3, _DVI))
        
        self.CreateGrid()


class DettaglioIncassiPagamentiPanel(aw.Panel):
    
    _id_cassa = None
    _id_reg = None
    
    def __init__(self, *args, **kwargs):
        
        aw.Panel.__init__(self, *args, **kwargs)
        wdr.DettaglioIncassiPagamentiFunc(self)
        cn = self.FindWindowByName
        
        datmin = Env.DateTime.Date(Env.Azienda.Login.dataElab.year, 1, 1)
        cn('datmin').SetValue(datmin)
        
        self.dbcas = dbc.SottocontiCassaBanca()
        self.gridcas = ElencoSottocontiGrid(cn('pangridcas'), self.dbcas)
        
        self.dbreg = dbc.ElencoRegistrazioni()
        self.gridreg = ElencoRegistrazioniGrid(cn('pangridreg'), self.dbreg)
        
        self.dbdet = dbc.DettaglioIncassiPagamenti()
        self.griddet = DettaglioOperazioniGrid(cn('pangriddet'), self.dbdet)
        
        for grid, func in ((self.gridcas, self.OnGridCasseCellSelected),
                           (self.gridreg, self.OnGridRegCellSelected),):
            self.Bind(dbglib.gridlib.EVT_GRID_CMD_SELECT_CELL, func, grid)
        
        for name, func in (('butupd', self.OnUpdateData),
                           ('butprt', self.OnPrintData),):
            self.Bind(wx.EVT_BUTTON, func, cn(name))
        
        for name in 'is_entrate is_uscite'.split():
            self.Bind(wx.EVT_CHECKBOX, self.OnUpdateData, cn(name))
    
    def OnGridCasseCellSelected(self, event):
        row = event.GetRow()
        cas = self.dbcas
        if cas.RowNumber() != row:
            cas.MoveRow(row)
        if cas.id != self._id_cassa:
            self._id_cassa = cas.id
            self.UpdateRegistrazioni()
            self.UpdateOperazioni()
        event.Skip()
    
    def UpdateRegistrazioni(self):
        cn = self.FindWindowByName
        det = self.dbdet
        wx.BeginBusyCursor()
        try:
            reg = det.get_registrazioni(self._id_cassa,
                                        cn('datmin').GetValue(), 
                                        cn('datmax').GetValue(),
                                        is_entrate=cn('is_entrate').IsChecked(),
                                        is_uscite=cn('is_uscite').IsChecked(),)
        finally:
            wx.EndBusyCursor()
        rs = reg.GetRecordset()
        self.dbreg.SetRecordset(rs)
        self.gridreg.ChangeData(rs)
    
    def OnGridRegCellSelected(self, event):
        row = event.GetRow()
        reg = self.dbreg
        if 0 <= row < reg.RowsCount():
            if reg.RowNumber() != row:
                reg.MoveRow(row)
            if reg.id_reg != self._id_reg:
                self._id_reg = reg.id_reg
                self.UpdateOperazioni()
        event.Skip()
    
    def UpdateOperazioni(self):
        cn = self.FindWindowByName
        det = self.dbdet
        wx.BeginBusyCursor()
        try:
            det.get_data(self._id_cassa,
                         cn('datmin').GetValue(), 
                         cn('datmax').GetValue(),
                         is_entrate=cn('is_entrate').IsChecked(),
                         is_uscite=cn('is_uscite').IsChecked(),
                         id_reg=self._id_reg)
        finally:
            wx.EndBusyCursor()
        self.griddet.ChangeData(det.GetRecordset())
    
    def OnUpdateData(self, event):
        self.UpdateData()
        event.Skip()
    
    def UpdateData(self):
        cn = self.FindWindowByName
        self._id_cassa = None
        wx.BeginBusyCursor()
        try:
            sm = self.dbdet.get_sottoconti_movimentati
            cas = sm(cn('datmin').GetValue(), 
                     cn('datmax').GetValue(),
                     is_entrate=cn('is_entrate').IsChecked(),
                     is_uscite=cn('is_uscite').IsChecked(),)
        finally:
            wx.EndBusyCursor()
        rs = cas.GetRecordset()
        self.dbcas.SetRecordset(rs)
        self.gridcas.ChangeData(rs)
        if len(rs) == 0:
            self.gridreg.ChangeData(())
            self.griddet.ChangeData(())
    
    def OnPrintData(self, event):
        self.PrintData()
        event.Skip()
    
    def PrintData(self):
        cn = self.FindWindowByName
        det = dbc.DettaglioIncassiPagamenti()
        datmin = cn('datmin').GetValue()
        datmax = cn('datmax').GetValue()
        is_entrate = cn('is_entrate').IsChecked()
        is_uscite = cn('is_uscite').IsChecked()
        det.get_data(self._id_cassa, datmin, datmax, is_entrate, is_uscite)
        rpt.Report(self, det, "Dettaglio operazioni in saldaconto")


class DettaglioIncassiPagamentiFrame(aw.Frame):
    
    def __init__(self, *args, **kwargs):
        if not 'title' in kwargs:
            kwargs['title'] = FRAME_TITLE
        aw.Frame.__init__(self, *args, **kwargs)
        self.panel = DettaglioIncassiPagamentiPanel(self)
        self.AddSizedPanel(self.panel)
