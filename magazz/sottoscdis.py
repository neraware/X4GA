#!/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         magazz/sottosc.py
# Author:       Fabio Cassini <fabio.cassini@gmail.com>
# Copyright:    (C) 2015 Fabio Cassini <fabio.cassini@gmail.com>
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

import magazz.dbtables as dbm

import magazz.invent_wdr as wdr

import report as rpt

Env = dbm.Env
bt = Env.Azienda.BaseTab
stdcolor = Env.Azienda.Colours

import magazz


FRAME_TITLE = "Sottoscorta da disponibilità"
FRAME_ORDPROD_TITLE = "Ordini e backorders del prodotto"


class BackOrdersGrid(dbglib.ADB_Grid):
    
    def __init__(self, parent, dbmov):
        
        dbglib.ADB_Grid.__init__(self, parent, db_table=dbmov, on_menu_select='row')
        
        self.dbmov = mov = dbmov
        
        DQM = bt.MAGQTA_DECIMALS
        IQM = bt.MAGQTA_INTEGERS
        col_qta = self.TypeFloat(IQM, DQM)
        
        self.COL_TPDCOD = self.AddColumn(mov, 'tpd_cod', 'Doc.', col_width=35)
        self.COL_NUMDOC = self.AddColumn(mov, 'numdoc',  'Num.', col_width=50)
        self.COL_DATDOC = self.AddColumn(mov, 'datdoc',  'Data', col_type=self.TypeDate())
        self.COL_PDCCOD = self.AddColumn(mov, 'pdc_cod', 'Cod.', col_width=50)
        self.COL_PDCDES = self.AddColumn(mov, 'pdc_des', 'Anagrafica', col_width=200, is_fittable=True)
        self.COL_DSTIND = self.AddColumn(mov, 'dst_ind', 'Indirizzo', col_width=120)
        self.COL_DSTCIT = self.AddColumn(mov, 'dst_cit', 'Città', col_width=90)
        self.COL_QTAORD = self.AddColumn(mov, 'qtaord',  'Ordinato', col_type=col_qta)
        self.COL_QTAEVA = self.AddColumn(mov, 'qtaeva',  'Evaso', col_type=col_qta)
        self.COL_QTABKO = self.AddColumn(mov, 'qtarim',  'Backorder', col_type=col_qta)
        self.AddColumn(mov, 'doc_id', '#doc', col_width=1)
        self.AddColumn(mov, 'mov_id', '#mov', col_width=1)
        
        self.CreateGrid()


class BackOrdersPanel(aw.Panel):
    
    def __init__(self, *args, **kwargs):
        aw.Panel.__init__(self, *args, **kwargs)
        wdr.OrdiniProdottoFunc(self)
        cn = self.FindWindowByName
        self.dbmov = dbm.OrdiniProdotto()
        self.gridmov = BackOrdersGrid(cn('pangridmov'), self.dbmov)


class BackOrdersDialog(aw.Dialog):
    
    def __init__(self, *args, **kwargs):
        if not 'title' in kwargs:
            kwargs['title'] = FRAME_ORDPROD_TITLE
        aw.Dialog.__init__(self, *args, **kwargs)
        self.panel = BackOrdersPanel(self)
        self.AddSizedPanel(self.panel)


class SottoscortaGrid(dbglib.ADB_Grid):
    
    def __init__(self, parent, dbssc):
        
        dbglib.ADB_Grid.__init__(self, parent, db_table=dbssc, on_menu_select='row')
        
        self.dbssc = ssc = dbssc
        
        def cn(tab, col):
            return tab._GetFieldIndex(col, inline=True)
        
        DQM = bt.MAGQTA_DECIMALS
        IQM = bt.MAGQTA_INTEGERS
        col_qta = self.TypeFloat(IQM, DQM)
        
        self.COL_IDX = self.AddColumn(ssc, 'codice',    'Cod.', col_width=80)
        self.COL_DES = self.AddColumn(ssc, 'descriz',   'Descrizione', col_width=200, is_fittable=True)
        self.COL_GIA = self.AddColumn(ssc, 'tot_giac',  'Giacenza', col_type=col_qta)
        self.COL_BKC = self.AddColumn(ssc, 'tot_bkcli', 'Ord.Cli.', col_type=col_qta)
        self.COL_BKF = self.AddColumn(ssc, 'tot_bkfor', 'Ord.For.', col_type=col_qta)
        self.COL_DIS = self.AddColumn(ssc, 'tot_disp',  'Disponib.', col_type=col_qta)
        self.COL_FAB = self.AddColumn(ssc, 'scomin',    'Scorta min.', col_type=col_qta)
        self.AddColumn(ssc, 'tot_fabb',  'Fabb.', col_type=col_qta)
        self.AddColumn(ssc, 'id', '#pro', col_width=1)
        
        self.CreateGrid()
    
    def OnCellDoubleClicked(self, event):
        def cn(name):
            f = aw.awu.GetParentFrame(self)
            return f.FindWindowByName(name)
        row, col = event.GetRow(), event.GetCol()
        if col in (self.COL_BKC, self.COL_BKF):
            ssc = self.dbssc
            ssc.MoveRow(row)
            mov = dbm.OrdiniProdotto()
            if col == self.COL_BKC:
                mov.update_ordini_prodotto(ssc.id, mags=ssc._mags, 
                                           bkc=cn('backordcli').IsChecked(), 
                                           datbkc=cn('datbkc').GetValue(), 
                                           bkf=False)
            else:
                mov.update_ordini_prodotto(ssc.id, mags=ssc._mags, 
                                           bkf=cn('backordfor').IsChecked(), 
                                           datbkf=cn('datbkf').GetValue(), 
                                           bkc=False)
            if mov.IsEmpty():
                aw.awu.MsgDialog(self, "Nessun ordine trovato")
            else:
                f = aw.awu.GetParentFrame(self)
                pos = f.GetPosition()
                dlg = BackOrdersDialog(self)
                dlg.SetPosition(pos)
                dlg.panel.gridmov.ChangeData(mov.GetRecordset())
                dlg.ShowModal()
                dlg.Destroy()
        event.Skip()


class SottoscortaPanel(aw.Panel):
    """
    Panel Prodotti sottoscorta.
    """
    def __init__(self, *args, **kwargs):
        
        aw.Panel.__init__(self, *args, **kwargs)
        wdr.SottoscortaDaDisponibFunc(self)
        cn = self.FindWindowByName
        dm = magazz.GetDefaultMagazz()
        if dm:
            lm = self.FindWindowByName('magazzini')
            if dm in lm.magid:
                lm.Check(lm.magid.index(dm), True)
        
        self.dbssc = dbm.SottoscortaDaDisponib()
        self.gridssc = SottoscortaGrid(cn('pangridssc'), self.dbssc)
        
        cn('datinv').SetValue(Env.Azienda.Login.dataElab)
        datmin = Env.Azienda.Login.dataElab-30
        cn('datbkc').SetValue(datmin)
        cn('datbkf').SetValue(datmin)
        for name, func in (('butupd', self.OnUpdateData),
                           ('butprt', self.OnPrintData),):
            self.Bind(wx.EVT_BUTTON, func, cn(name))
    
    def OnUpdateData(self, event):
        self.UpdateData()
        event.Skip()
    
    def UpdateData(self):
        
        cn = self.FindWindowByName
        
        i = self.dbssc
        i.ClearFilters()
        
        v1 = cn('codice1').GetValue()
        v2 = cn('codice2').GetValue()
        if v1 or v2:
            if v1: i.AddFilter(r"prod.codice>=%s", v1)
            if v2: i.AddFilter(r"prod.codice<=%s", v2.rstrip()+'Z')
        
        for name in 'tipart catart gruart marart fornit'.split():
            v1 = cn(name+'1').GetValueCod()
            v2 = cn(name+'2').GetValueCod()
            if v1 or v2:
                if v1 == v2:
                    i.AddFilter("%s.codice=%%s" % name, v1)
                else:
                    if v1:
                        i.AddFilter("%s.codice>=%%s" % name, v1)
                    if v2:
                        i.AddFilter("%s.codice<=%%s" % name, v2.rstrip()+'Z')
        
        #aggiorna prodotti
        i.Retrieve()
        
        wait = aw.awu.WaitDialog(self, maximum=i.RowsCount())
        wx.BeginBusyCursor()
        
        try:
            
            #filtro su magazzino
            mag = cn("magazzini")
            mags = []
            for n, mid in enumerate(mag.magid):
                if mag.IsChecked(n):
                    mags.append(mid)
            if len(mags) == 0:
                aw.awu.MsgDialog(self, "Selezionare almeno un magazzino")
                return False
            i.set_mags(mags)
            
            #aggiorna inventario
            val = cn("datinv").GetValue()
            if val is not None:
                i.set_data_inv(val)
            
            tgia, tbkc, tbkf, tdis, tfab =\
                    i.update_disponib(bkcli=cn('backordcli').IsChecked(), datbkc=cn('datbkc').GetValue(),
                                      bkfor=cn('backordfor').IsChecked(), datbkf=cn('datbkf').GetValue(),
                                      progress=lambda *x: wait.SetValue(i.RowNumber()))
            
            cn('totgia').SetValue(tgia)
            cn('totbkc').SetValue(tbkc)
            cn('totbkf').SetValue(tbkf)
            cn('totdis').SetValue(tdis)
            cn('totfab').SetValue(tfab)
            
        finally:
            wx.EndBusyCursor()
            wait.Destroy()
        
        self.gridssc.ChangeData(i.GetRecordset())
    
    def SetMagFilter(self):
        mag = self.FindWindowByName("magazzini")
        mags = []
        for n, mid in enumerate(mag.magid):
            if mag.IsChecked(n):
                mags.append(mid)
        if len(mags) == 0:
            aw.awu.MsgDialog(self, "Selezionare almeno un magazzino")
            return False
        self.dbssc.set_mags(mags)
        return True
    
    def OnPrintData(self, event):
        self.PrintData()
        event.Skip()
    
    def PrintData(self):
        rpt.Report(self, self.dbssc, 'Sottoscorta da disponibilita')


class SottoscortaFrame(aw.Frame):
    def __init__(self, *args, **kwargs):
        if not kwargs.has_key('title') and len(args) < 3:
            kwargs['title'] = FRAME_TITLE
        aw.Frame.__init__(self, *args, **kwargs)
        self.panel = SottoscortaPanel(self, -1)
        self.AddSizedPanel(self.panel)
        self.CenterOnScreen()
