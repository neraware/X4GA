#!/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         anag/clifor_datifisc.py
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

import awc.controls.windows as aw
import awc.controls.dbgrid as dbgrid

import anag.pdcrel_wdr as wdr

import stormdb as adb

import Env
bt = Env.Azienda.BaseTab

from anag.clienti import ClientiDialog
from anag.fornit import FornitDialog

from awc.lib import ControllaPIVA, ControllaCodFisc

import report as rpt


FRAME_TITLE = "Dati fiscali"


class _CliFor_DatiFiscaliGrid(dbgrid.ADB_Grid):
    
    _AnagClass = None
    
    def __init__(self, parent, dbana):
        
        self.dbana = anag = dbana
        pdc = anag.pdc
        stato = anag.stato
        
        dbgrid.ADB_Grid.__init__(self, parent, db_table=dbana, can_edit=True, on_menu_select='row')
        
        AC = self.AddColumn
        self.COL_DESCRIZ = AC(pdc,   'descriz', label='Descrizione', col_width=300, is_fittable=True)
        self.COL_STATO =   AC(stato, 'codice', label='Stato', col_width=60)
        self.COL_CAP =     AC(anag,  'cap', label='CAP', col_width=60, is_editable=True)
        self.COL_CITTA =   AC(anag,  'citta', label='Città', col_width=120, is_editable=True)
        self.COL_PROV =    AC(anag,  'prov', label='Prov.', col_width=50, is_editable=True)
        self.COL_NAZIONE = AC(anag,  'nazione', label='St.PI', col_width=60)
        self.COL_PIVA =    AC(anag,  'piva', label='P.IVA', col_width=100, is_editable=True)
        self.COL_CODFISC = AC(anag,  'codfisc', label='Cod.Fiscale', col_width=140, is_editable=True)
        self.COL_ALLEGCF = AC(anag,  'allegcf', label='All.', col_width=50, col_type=self.TypeCheck())
        self.COL_AZIPER =  AC(anag,  'aziper', label='A/P', col_width=50, is_editable=True)
        self.COL_ANAG_BL = AC(anag,  'is_blacklisted', label='B/L', col_width=50, col_type=self.TypeCheck())
        
        def gfi(tab, col):
            return tab._GetFieldIndex(col, inline=True)
        
        self._col_cap =     gfi(anag, 'cap')
        self._col_citta =   gfi(anag, 'citta')
        self._col_prov =    gfi(anag, 'prov')
        self._col_aziper =  gfi(anag, 'aziper')
        self._col_nazione = gfi(anag, 'nazione')
        self._col_piva =    gfi(anag, 'piva')
        self._col_codfisc = gfi(anag, 'codfisc')
        
        self.CreateGrid()
    
    def GetAttr(self, row, col, rscol, attr):
        attr = dbgrid.ADB_Grid.GetAttr(self, row, col, rscol, attr)
        rs = self.db_table.GetRecordset()
        if 0 <= row < len(rs):
            r = rs[row]
            if (r[self._col_nazione] or "IT") == "IT":
                if (r[self._col_aziper] == "A" and len(r[self._col_piva] or '') == 0) or \
                   (r[self._col_aziper] == "P" and len(r[self._col_codfisc] or '') == 0):
                    attr.SetBackgroundColour('red')
                elif not r[self._col_cap] or not r[self._col_citta] or not r[self._col_prov]:
                    attr.SetBackgroundColour('yellow')
        return attr
    
    def ApriScheda(self, row):
        anag = self.dbana
        anag.MoveRow(row)
        dlg = self._AnagClass(None, onecodeonly=anag.id)
        dlg.OneCardOnly(anag.id)
        dlg.CenterOnScreen()
        dlg.ShowModal()
        dlg.Destroy()
        anag.Retrieve()
        self.ChangeData(anag.GetRecordset())
    
    def OnCellDoubleClicked(self, event):
        row = event.GetRow()
        self.ApriScheda(row)
    
    def ShowContextMenu(self, position, row, col):
        
        self.ResetContextMenu()
        
        def ApriScheda(event):
            self.ApriScheda(row)
        self.AppendContextMenuVoice('Apri scheda anagrafica', ApriScheda)
        
        return dbgrid.ADB_Grid.ShowContextMenu(self, position, row, col)
    
    def CellEditBeforeUpdate(self, row, gridcol, col, value):
        
        anag = self.dbana
        anag.MoveRow(row)
        
        def cc(tab, colname):
            return tab._GetFieldIndex(colname, inline=True)
        
        if col == cc(anag, 'aziper'):
            valid = (value in 'APCZE')
            if not valid:
                aw.awu.MsgDialog(self, 'Valori contentiti: A, P', style=wx.ICON_ERROR)
            return valid
        
        elif col == cc(anag, 'piva') and len(value)>0:
            ctr = ControllaPIVA()
            ctr.SetPIva(value, anag.nazione or "IT")
            valid = ctr.Controlla()
            if not valid:
                aw.awu.MsgDialog(self, ctr.GetStatus(), style=wx.ICON_ERROR)
            return valid
        
        elif col == cc(anag, 'codfisc') and len(value)>0:
            ctr = ControllaCodFisc()
            ctr.SetCodFisc(value)
            valid = ctr.Controlla()
            if not valid:
                aw.awu.MsgDialog(self, ctr.GetStatus(), style=wx.ICON_ERROR)
            return valid
            
        elif col == cc(anag, 'cap') and len(value)>0:
            return True
            
        elif col == cc(anag, 'citta') and len(value)>0:
            return True
            
        elif col == cc(anag, 'prov') and len(value)>0:
            return True
        
        return True


# -----------------------------------------------------------------------------


class _CliFor_DatiFiscaliPanel(aw.Panel):
    
    _GridClass = None
    tabanag = None
    
    def __init__(self, *args, **kwargs):
        
        aw.Panel.__init__(self, *args, **kwargs)
        wdr.CliFor_DatiFiscaliFunc(self)
        cn = self.FindWindowByName
        
        cn('panlegerr1').SetBackgroundColour('red')
        cn('panlegerr2').SetBackgroundColour('yellow')
        
        self.dbana = adb.DbTable(self.tabanag, 'anag')
        self.dbana.AddJoin(bt.TABNAME_PDC, 'pdc', idLeft='id')
        self.dbana.AddJoin('x4.stati', 'stato', join=adb.JOIN_LEFT)
        self.dbana.AddOrder('pdc.descriz')
        self.dbana.Reset()
        
        self.gridpdc = self._GridClass(cn('pangridpdc'), self.dbana)
        
        self.Bind(wx.EVT_BUTTON, self.OnUpdateData, cn('butupd'))
        self.Bind(wx.EVT_BUTTON, self.OnSaveData, cn('butsave'))
    
    def OnUpdateData(self, event):
        self.UpdateData()
        event.Skip()
    
    def UpdateData(self):
        cn = self.FindWindowByName
        ana = self.dbana
        ana.ClearFilters()
        checks = map(lambda x: cn(x), 'is_pri is_azi is_con is_ass is_ent'.split())
        pri, azi, con, ass, ent = map(lambda x: x.IsChecked(), checks)
        if not (pri and azi and con and ass and ent):
            tipi = ''
            if pri: tipi += 'P'
            if azi: tipi += 'A'
            if con: tipi += 'C'
            if ass: tipi += 'Z'
            if ent: tipi += 'E'
            if tipi:
                ana.AddFilter('anag.aziper IN (%s)' % ','.join(['"%s"' % t for t in tipi]))
            else:
                ana.AddFilter('0')
        d1, d2 = cn('datreg1').GetValue(), cn('datreg2').GetValue()
        if d1 or d2:
            if d1 and d2:
                flt = 'reg.datreg>="%s" AND reg.datreg<="%s"' % (d1.FormatANSI(),
                                                                 d2.FormatANSI(),)
            elif d1:
                flt = 'reg.datreg>="%s"' % d1.FormatANSI()
            elif d2:
                flt = 'reg.datreg<="%s"' % d1.FormatANSI()
            ana.AddFilter("(SELECT COUNT(*) FROM contab_b mov JOIN contab_h reg ON reg.id=mov.id_reg WHERE mov.id_pdcpa=anag.id AND %s)>0" % flt)
        self.dbana.Retrieve()
        self.gridpdc.ChangeData(self.dbana.GetRecordset())
    
    def OnSaveData(self, event):
        anag = self.dbana
        if anag.Save():
            aw.awu.MsgDialog(self, 'I dati sono stati correttamente salvati', style=wx.ICON_INFORMATION)
            event.Skip()
        else:
            aw.awu.MsgDialog(self, repr(anag.GetError()), style=wx.ICON_ERROR)


# ------------------------------------------------------------------------------


class Clienti_DatiFiscaliGrid(_CliFor_DatiFiscaliGrid):
    _AnagClass = ClientiDialog

class Clienti_DatiFiscaliPanel(_CliFor_DatiFiscaliPanel):
    _GridClass = Clienti_DatiFiscaliGrid
    tabanag = bt.TABNAME_CLIENTI

class Clienti_DatiFiscaliFrame(aw.Frame):
    
    def __init__(self, *args, **kwargs):
        if not 'title' in kwargs:
            kwargs['title'] = '%s %s' % (FRAME_TITLE, 'clienti')
        aw.Frame.__init__(self, *args, **kwargs)
        self.AddSizedPanel(Clienti_DatiFiscaliPanel(self))


# ------------------------------------------------------------------------------


class Fornitori_DatiFiscaliGrid(_CliFor_DatiFiscaliGrid):
    _AnagClass = FornitDialog

class Fornitori_DatiFiscaliPanel(_CliFor_DatiFiscaliPanel):
    _GridClass = Fornitori_DatiFiscaliGrid
    tabanag = bt.TABNAME_FORNIT

class Fornitori_DatiFiscaliFrame(aw.Frame):
    
    def __init__(self, *args, **kwargs):
        if not 'title' in kwargs:
            kwargs['title'] = '%s %s' % (FRAME_TITLE, 'fornitori')
        aw.Frame.__init__(self, *args, **kwargs)
        self.AddSizedPanel(Fornitori_DatiFiscaliPanel(self))
