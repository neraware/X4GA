# -*- coding: UTF-8 -*-

#-----------------------------------------------------------------------------
# Python source generated by wxDesigner from file: agenti.wdr
# Do not modify this file, all changes will be lost!
#-----------------------------------------------------------------------------

# Include wxPython modules
import wx
import wx.grid
import wx.animate

# Custom source
from awc.controls.textctrl import TextCtrl
from awc.controls.numctrl import NumCtrl
from awc.controls.linktable import LinkTable

from anag.basetab import AnagCardPanel, WorkZoneNotebook, UnoZeroCheckBox

from awc.controls.entries import PhoneEntryCtrl, MailEntryCtrl, FolderEntryCtrl, HttpEntryCtrl

import Env
bt = Env.Azienda.BaseTab


# Window functions

ID_ANAGMAIN = 16000
ID_WORKZONE = 16001

def AgentiCardFunc( parent, call_fit = True, set_sizer = True ):
    item0 = wx.FlexGridSizer( 0, 1, 0, 0 )
    
    item1 = AnagCardPanel(parent, -1)
    item0.Add( item1, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

    item3 = WorkZoneNotebook( parent, ID_WORKZONE, wx.DefaultPosition, [200,160], 0 )
    item2 = item3
    
    item4 = wx.Panel( item3, -1 )
    AgentiCardAnagFunc(item4, False)
    item3.AddPage( item4, "Dati anagrafici" )

    item0.Add( item2, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

    item0.AddGrowableCol( 0 )

    item0.AddGrowableRow( 1 )

    if set_sizer == True:
        parent.SetSizer( item0 )
        if call_fit == True:
            item0.SetSizeHints( parent )
    
    return item0

ID_TEXT = 16002
ID_TXT_INDIRIZZO = 16003
ID_TXT_CAP = 16004
ID_TXT_CITTA = 16005
ID_TXT_PROVINCIA = 16006
ID_LINE = 16007
ID_TXT_CODFISC = 16008
ID_TXT_PIVA = 16009
ID_PERPRO = 16010
ID_NOPROVVIG = 16011
ID_TXT_NUMTEL = 16012
ID_TXT_NUMTEL2 = 16013
ID_TXT_NUMFAX = 16014
ID_TXT_NUMCEL = 16015
ID_TXT_EMAIL = 16016
ID_TXT_SITEURL = 16017

def AgentiCardAnagFunc( parent, call_fit = True, set_sizer = True ):
    item0 = wx.FlexGridSizer( 1, 0, 0, 0 )
    
    item2 = wx.StaticBox( parent, -1, "Anagrafica" )
    item1 = wx.StaticBoxSizer( item2, wx.VERTICAL )
    
    item3 = wx.FlexGridSizer( 4, 0, 0, 0 )
    
    item4 = wx.FlexGridSizer( 0, 1, 0, 0 )
    parent.sizersede = item4
    
    item5 = wx.StaticText( parent, ID_TEXT, "Indirizzo:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item4.Add( item5, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item6 = TextCtrl( parent, ID_TXT_INDIRIZZO, "", wx.DefaultPosition, [80,-1], 0 )
    item6.SetName( "indirizzo" )
    item4.Add( item6, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM, 5 )

    item7 = wx.FlexGridSizer( 0, 3, 0, 0 )
    
    item8 = wx.StaticText( parent, ID_TEXT, "CAP", wx.DefaultPosition, wx.DefaultSize, 0 )
    item7.Add( item8, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item9 = wx.StaticText( parent, ID_TEXT, "Città", wx.DefaultPosition, wx.DefaultSize, 0 )
    item7.Add( item9, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item10 = wx.StaticText( parent, ID_TEXT, "Prov.", wx.DefaultPosition, wx.DefaultSize, 0 )
    item7.Add( item10, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item11 = TextCtrl( parent, ID_TXT_CAP, "", wx.DefaultPosition, [50,-1], 0 )
    item11.SetName( "cap" )
    item7.Add( item11, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.BOTTOM, 5 )

    item12 = TextCtrl( parent, ID_TXT_CITTA, "", wx.DefaultPosition, [80,-1], 0 )
    item12.SetName( "citta" )
    item7.Add( item12, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.BOTTOM, 5 )

    item13 = TextCtrl( parent, ID_TXT_PROVINCIA, "", wx.DefaultPosition, [30,-1], 0 )
    item13.SetName( "prov" )
    item7.Add( item13, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM, 5 )

    item7.AddGrowableCol( 1 )

    item4.Add( item7, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 0 )

    item4.AddGrowableCol( 0 )

    item3.Add( item4, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

    item3.AddGrowableCol( 0 )

    item1.Add( item3, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 0 )

    item14 = wx.StaticLine( parent, ID_LINE, wx.DefaultPosition, [20,-1], wx.LI_HORIZONTAL )
    item1.Add( item14, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 0 )

    item15 = wx.FlexGridSizer( 0, 3, 0, 0 )
    
    item16 = wx.StaticText( parent, ID_TEXT, "Cod. Fiscale:", wx.DefaultPosition, [90,-1], 0 )
    item15.Add( item16, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.TOP, 5 )

    item17 = wx.StaticText( parent, ID_TEXT, "Stato:", wx.DefaultPosition, [40,-1], 0 )
    item15.Add( item17, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.TOP, 5 )

    item18 = wx.StaticText( parent, ID_TEXT, "P.IVA:", wx.DefaultPosition, [40,-1], 0 )
    item15.Add( item18, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.TOP, 5 )

    item19 = TextCtrl( parent, ID_TXT_CODFISC, "", wx.DefaultPosition, [100,-1], 0 )
    item19.SetName( "codfisc" )
    item15.Add( item19, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.BOTTOM, 5 )

    item20 = TextCtrl( parent, ID_TXT_PIVA, "", wx.DefaultPosition, [35,-1], 0 )
    item20.SetName( "nazione" )
    item15.Add( item20, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.BOTTOM, 5 )

    item21 = TextCtrl( parent, ID_TXT_PIVA, "", wx.DefaultPosition, [80,-1], 0 )
    item21.SetName( "piva" )
    item15.Add( item21, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM, 5 )

    item15.AddGrowableCol( 0 )

    item15.AddGrowableCol( 2 )

    item1.Add( item15, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5 )

    item22 = wx.StaticLine( parent, ID_LINE, wx.DefaultPosition, [20,-1], wx.LI_HORIZONTAL )
    item1.Add( item22, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM, 5 )

    item23 = wx.FlexGridSizer( 1, 0, 0, 0 )
    
    item24 = wx.StaticText( parent, ID_TEXT, "%Provvigione:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item24.SetName( "labelpro" )
    item23.Add( item24, 0, wx.ALIGN_CENTER|wx.LEFT|wx.BOTTOM, 5 )

    item25 = NumCtrl(parent, ID_PERPRO, integerWidth=2, fractionWidth=2, allowNegative=False, name='perpro')
    item23.Add( item25, 0, wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item26 = UnoZeroCheckBox( parent, ID_NOPROVVIG, "Escludi da calcolo", wx.DefaultPosition, wx.DefaultSize, 0 )
    item26.SetName( "noprovvig" )
    item23.Add( item26, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item1.Add( item23, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item0.Add( item1, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

    item28 = wx.StaticBox( parent, -1, "Recapiti" )
    item27 = wx.StaticBoxSizer( item28, wx.VERTICAL )
    
    item29 = wx.FlexGridSizer( 0, 2, 0, 0 )
    
    item30 = wx.StaticText( parent, ID_TEXT, "Telefono #1:", wx.DefaultPosition, [50,-1], 0 )
    item29.Add( item30, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.TOP, 5 )

    item31 = wx.StaticText( parent, ID_TEXT, "Telefono #2:", wx.DefaultPosition, [50,-1], 0 )
    item29.Add( item31, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item32 = PhoneEntryCtrl( parent, ID_TXT_NUMTEL, "", wx.DefaultPosition, wx.DefaultSize, 0 )
    item32.SetName( "numtel" )
    item29.Add( item32, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item33 = PhoneEntryCtrl( parent, ID_TXT_NUMTEL2, "", wx.DefaultPosition, wx.DefaultSize, 0 )
    item33.SetName( "numtel2" )
    item29.Add( item33, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item34 = wx.StaticText( parent, ID_TEXT, "FAX #1:", wx.DefaultPosition, [40,-1], 0 )
    item29.Add( item34, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.TOP, 5 )

    item35 = wx.StaticText( parent, ID_TEXT, "Cellulare:", wx.DefaultPosition, [40,-1], 0 )
    item29.Add( item35, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item36 = PhoneEntryCtrl( parent, ID_TXT_NUMFAX, "", wx.DefaultPosition, wx.DefaultSize, 0 )
    item36.SetName( "numfax" )
    item29.Add( item36, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item37 = PhoneEntryCtrl( parent, ID_TXT_NUMCEL, "", wx.DefaultPosition, wx.DefaultSize, 0 )
    item37.SetName( "numcel" )
    item29.Add( item37, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item29.AddGrowableCol( 0 )

    item29.AddGrowableCol( 1 )

    item27.Add( item29, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item38 = wx.FlexGridSizer( 0, 1, 0, 0 )
    
    item39 = wx.StaticText( parent, ID_TEXT, "E-Mail:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item38.Add( item39, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5 )

    item40 = MailEntryCtrl( parent, ID_TXT_EMAIL, "", wx.DefaultPosition, wx.DefaultSize, 0 )
    item40.SetName( "email" )
    item38.Add( item40, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM, 5 )

    item38.AddGrowableCol( 0 )

    item27.Add( item38, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item41 = wx.FlexGridSizer( 0, 1, 0, 0 )
    
    item42 = wx.StaticText( parent, ID_TEXT, "Url Sito Internet:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item41.Add( item42, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5 )

    item43 = HttpEntryCtrl( parent, ID_TXT_SITEURL, "", wx.DefaultPosition, wx.DefaultSize, 0 )
    item43.SetName( "siteurl" )
    item41.Add( item43, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM, 5 )

    item41.AddGrowableCol( 0 )

    item27.Add( item41, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item0.Add( item27, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP|wx.BOTTOM, 5 )

    item0.AddGrowableCol( 0 )

    item0.AddGrowableCol( 1 )

    if set_sizer == True:
        parent.SetSizer( item0 )
        if call_fit == True:
            item0.SetSizeHints( parent )
    
    return item0

# Menubar functions

# Toolbar functions

# Bitmap functions


# End of generated file
