#!/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         contab/spesometro_2017.py
# Author:       Fabio Cassini <fabio.cassini@gmail.com>
# Copyright:    (C) 2017 Neraware Sas di Fabio Cassini & C. <fc@neraware.com>
# Copyright:    (C) 2013 Fabio Cassini <fabio.cassini@gmail.com>
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
import os

import awc.controls.windows as aw
import awc.controls.dbgrid as dbgrid

import contab
import contab.spesometro_2017_wdr as wdr

import contab.dbtables as dbc

import Env
bt = Env.Azienda.BaseTab

from awc.controls import EVT_DATECHANGED

import report as rpt


FRAME_TITLE = "Spesometro"


class SpesometroGrid(dbgrid.ADB_Grid):
    
    def __init__(self, parent, dbspe):
        
        dbgrid.ADB_Grid.__init__(self, parent, db_table=dbspe, can_edit=True, on_menu_select='row')
        
        s = dbspe
        _float = self.TypeFloat(6, bt.VALINT_DECIMALS)
        
        self.COL_ANAG_COD = self.AddColumn(s, 'pdc_codice',     'Cod.', col_width=50)
        self.COL_ANAG_DES = self.AddColumn(s, 'pdc_descriz',    'Cliente', col_width=300)
        self.COL_ANAG_CFS = self.AddColumn(s, 'anag_codfisc',   'Cod.Fiscale', col_width=140)
        self.COL_ANAG_STT = self.AddColumn(s, 'anag_nazione',   'Naz.', col_width=40)
        self.COL_ANAG_PIV = self.AddColumn(s, 'anag_piva',      'P.IVA', col_width=100)
        
        self.COL_DOCU_DAT = self.AddColumn(s, 'reg_datdoc',     'Doc.', col_type=self.TypeDate())
        self.COL_DOCU_NUM = self.AddColumn(s, 'reg_numdoc',     'Num.', col_width=60)
        self.COL_RIVA_COD = self.AddColumn(s, 'riv_codice',     'Reg.', col_width=40)
        self.COL_RIVA_NIV = self.AddColumn(s, 'reg_numiva',     'Prot.', col_type=self.TypeInteger(6), col_width=50)
        self.COL_TIVA_IMP = self.AddColumn(s, 'total_imponib',  'Imponibile', col_type=_float)
        self.COL_TIVA_IVA = self.AddColumn(s, 'total_imposta',  'Imposta', col_type=_float)
        self.COL_TIVA_TOT = self.AddColumn(s, 'iva_natura',     'Natura IVA', col_width=60)
        
        self.COL_REG_ID =   self.AddColumn(s, 'reg_id',         '#reg', col_width=1)
        
        self.SetColorsByColumn(self.COL_ANAG_COD)
        
        self.CreateGrid()
        
        self.SetRowLabelSize(40)
        self.SetRowLabelAlignment(wx.ALIGN_RIGHT, wx.ALIGN_BOTTOM)
        self.SetRowDynLabel(self.GetRowLabel)
    
    def GetRowLabel(self, row):
        if 0 <= row < self.db_table.RowsCount():
            return str(row+1)
        return ''
    
    def AlterColor(self, color, delta):
        
        r, g, b = color.Red(), color.Green(), color.Blue()
        
        def AlterChannel(channel, delta):
            channel += delta
            if channel > 255:
                channel -= 255
            elif channel < 0:
                channel = -channel
            return channel
        
        colors = map(lambda channel: AlterChannel(channel, delta), [r, g, b])
        
        return wx.Colour(colors[0], colors[1], b)
    
#     def GetAttr(self, row, col, rscol, attr):
#          
#         attr = dbgrid.ADB_Grid.GetAttr(self, row, col, rscol, attr)
#          
#         if col in (self.COL_FAAT_CNT,
#                    self.COL_FAAT_TOT,
#                    self.COL_FAAT_IVA,
#                    self.COL_FAAT_VAR,
#                    self.COL_FAAT_VIV,):
#             bg = self.AlterColor(attr.GetBackgroundColour(), -32)
#             attr.SetBackgroundColour(bg)
#              
#         elif col in (self.COL_FAPA_CNT,
#                      self.COL_FAPA_TOT,
#                      self.COL_FAPA_IVA,
#                      self.COL_FAPA_VAR,
#                      self.COL_FAPA_VIV,):
#             bg = self.AlterColor(attr.GetBackgroundColour(), -64)
#             attr.SetBackgroundColour(bg)
#             
#         elif col in (self.COL_BLAT_CNT,
#                      self.COL_BLAT_TOT,
#                      self.COL_BLAT_IVA,):
#             bg = self.AlterColor(attr.GetBackgroundColour(), -96)
#             attr.SetBackgroundColour(bg)
#             
#         elif col in (self.COL_BLPA_CNT,
#                      self.COL_BLPA_TOT,
#                      self.COL_BLPA_IVA,):
#             bg = self.AlterColor(attr.GetBackgroundColour(), -128)
#             attr.SetBackgroundColour(bg)
#             
#         elif col in (self.COL_SAAT_CNT,
#                      self.COL_SAAT_TOT,):
#             bg = self.AlterColor(attr.GetBackgroundColour(), -160)
#             attr.SetBackgroundColour(bg)
#          
#         return attr


class SpesometroPanel(aw.Panel):
    
    def __init__(self, *args, **kwargs):
        
        aw.Panel.__init__(self, *args, **kwargs)
        wdr.SpesometroPanelFunc(self)
        cn = self.FindWindowByName
        
        self.dbspe = dbc.Spesometro2017_AcquistiVendite(acqven="A")
        self.gridspe = SpesometroGrid(cn('pangridspe'), self.dbspe)
        
        self.acqven = None
        self.data1 = None
        self.data2 = None
        self.solo_anag_all = None
        self.solo_caus_all = None
        
#         cn('acqven').SetValue("V")
#         cn('data1').SetValue(Env.DateTime.Date(2014,1,1))
#         cn('data2').SetValue(Env.DateTime.Date(2014,1,15))
        
        for name, func in (('butupd', self.OnUpdateButton),
                           ('butgen', self.OnGeneraButton),):
            self.Bind(wx.EVT_BUTTON, func, cn(name))
    
    def OnUpdateButton(self, event):
        if not self.Validate():
            return
        self.UpdateData()
        event.Skip()
    
    def OnGeneraButton(self, event):
        self.GeneraFile()
        event.Skip()
    
    def GeneraFile(self):
        cn = self.FindWindowByName
        progr_invio = cn('numprogr').GetValue()
        if progr_invio < 1:
            aw.awu.MsgDialog(self, message="Progressivo errato", style=wx.ICON_ERROR)
            return
        defaultFile = 'IT%s_DF_%s.xml' % (Env.Azienda.piva, str(progr_invio).zfill(5))
        filename = None
        dlg = wx.FileDialog(self,
                            message="Digita il nome del file da generare",
#                            defaultDir=pathname,
                            defaultFile=defaultFile,
                            wildcard="File di esportazione (*.xml)|*.xml",
                            style=wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
        dlg.Destroy()
        if filename:
            if os.path.exists(filename):
                if aw.awu.MsgDialog(self, "Il file indicato è già esistente.\nVuoi sovrascriverlo ?", 
                                    style=wx.ICON_QUESTION|wx.YES_NO|wx.NO_DEFAULT) != wx.ID_YES:
                    return
            wait = aw.awu.WaitDialog(self, "Generazione file in corso", maximum=self.dbspe.RowsCount())
            def progress(row):
                wait.SetValue(row)
            err = None
            try:
                self.dbspe.xmlfile_make_file(filename, progr_invio, progress)
                aw.awu.MsgDialog(self, "Il file è stato generato:\n%s" % filename, style=wx.ICON_INFORMATION)
            except dbc.Spesometro2017_Exception, e:
                err = repr(e.args)
            finally:
                wait.Destroy()
            if err:
                aw.awu.MsgDialog(self, err, style=wx.ICON_ERROR)
    
    def Validate(self):
        cn = self.FindWindowByName
        data1 = cn('data1').GetValue()
        data2 = cn('data2').GetValue()
        wms = ''
        err = None
        dataElab = Env.Azienda.Login.dataElab
        if data1 is None or data2 is None:
            err = "Le date non possono essere nulle"
        elif data1.year != data2.year:
            err = "Le date si riferiscono ad anni diversi"
        if err:
            wms = err
        else:
            wms = ''
        cn('warning').SetLabel(wms)
        valid = not err
        TTS = wx.Button.SetToolTipString
        b = cn('butupd')
        TTS(b, wms)
#         b.Enable(valid)
        
        if valid:
            acqven = "acquisto vendita".split()[cn('acqven').GetSelection()]
            TTS(cn('butupd'), "Estrae tutte le operazioni di %(acqven)s del periodo, ordinate per cliente." % locals())
        
        return valid
    
    def UpdateData(self):
        
        cn = self.FindWindowByName
        
        acqven = cn('acqven').GetValue()
        
        self.dbspe = dbc.Spesometro2017_AcquistiVendite(acqven=acqven)
        spe = self.dbspe
        
        data1 = cn('data1').GetValue()
        data2 = cn('data2').GetValue()
        solo_anag_all = cn('solo_anag_all').IsChecked()
        solo_caus_all = cn('solo_caus_all').IsChecked()
        
        wx.BeginBusyCursor()
        try:
            numreg, numpdc, imponib, imposta, indeduc =\
                    spe.GetData(acqven, data1, data2, solo_anag_all, solo_caus_all)
            self.acqven = acqven
            self.data1 = data1
            self.data2 = data2
            self.solo_anag_all = solo_anag_all
            self.solo_caus_all = solo_caus_all
            cn('totnumope').SetLabel(str(numreg))
            cn('totnumpdc').SetLabel(str(numpdc))
            cn('totimponib').SetLabel(spe.sepnvi(imponib))
            cn('totimposta').SetLabel(spe.sepnvi(imposta))
            cn('totindeduc').SetLabel(spe.sepnvi(indeduc))
            cn('totimporto').SetLabel(spe.sepnvi(imponib+imposta+indeduc))
            self.gridspe.ChangeData(self.dbspe.GetRecordset())
            self.Layout()
        except Exception, e:
            aw.awu.MsgDialog(self, repr(e.args), style=wx.ICON_ERROR)
            self.gridspe.ChangeData([])
        finally:
            wx.EndBusyCursor()
    
    def PrintData(self):
        spe = self.dbspe
        cn = self.FindWindowByName
#         rpt.Report(self, self.dbspe, 'Spesometro XML')


class SpesometroFrame(aw.Frame):
    
    def __init__(self, *args, **kwargs):
        if not 'title' in kwargs:
            kwargs['title'] = FRAME_TITLE
        aw.Frame.__init__(self, *args, **kwargs)
        self.AddSizedPanel(SpesometroPanel(self))
