# -*- coding: UTF-8 -*-

#-----------------------------------------------------------------------------
# Python source generated by wxDesigner from file: solpag.wdr
# Do not modify this file, all changes will be lost!
#-----------------------------------------------------------------------------

# Include wxPython modules
import wx
import wx.grid
import wx.animate

# Custom source
from awc.controls.datectrl import DateCtrl
from awc.controls.numctrl import NumCtrl

from anag.basetab import UnoZeroCheckBox
import anag.lib as alib



# Window functions

ID_TIPSOL = 10000
ID_TEXT = 10001
ID_GGSCAD = 10002
ID_DATSCA1 = 10003
ID_DATSCA2 = 10004
ID_DATDOC1 = 10005
ID_DATDOC2 = 10006
ID_ESC0 = 10007
ID_ESC1 = 10008
ID_ESC2 = 10009
ID_INS0 = 10010
ID_INS1 = 10011
ID_INS2 = 10012
ID_RIB0 = 10013
ID_RIB1 = 10014
ID_RIB2 = 10015
ID_RID0 = 10016
ID_RID1 = 10017
ID_RID2 = 10018
ID_LIVX = 10019
ID_AGENTE = 10020
ID_ZONA = 10021
ID_CATEG = 10022
ID_STATUS = 10023
ID_PANGRIDTOT = 10024
ID_PANGRIDPCF = 10025
ID_BUTUPDATE = 10026
ID_BUTPRTRIEP = 10027
ID_BUTEMAIL = 10028
ID_PANCOLORS = 10029

def SollecitiPagamentoFunc( parent, call_fit = True, set_sizer = True ):
    item0 = wx.FlexGridSizer( 0, 1, 0, 0 )
    
    item1 = wx.FlexGridSizer( 1, 0, 0, 0 )
    
    item2 = wx.BoxSizer( wx.VERTICAL )
    
    item4 = wx.StaticBox( parent, -1, "Tipo di sollecito" )
    item3 = wx.StaticBoxSizer( item4, wx.VERTICAL )
    
    item5 = alib.LinkTableTipoSollecitoPagamento(parent, ID_TIPSOL, name='id_tipsol')
    item3.Add( item5, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item2.Add( item3, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

    item7 = wx.StaticBox( parent, -1, "Periodo" )
    item6 = wx.StaticBoxSizer( item7, wx.VERTICAL )
    
    item8 = wx.FlexGridSizer( 0, 2, 0, 0 )
    
    item9 = wx.StaticText( parent, ID_TEXT, "Estrai partite scadute da giorni:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item8.Add( item9, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item10 = NumCtrl(parent, ID_GGSCAD, integerWidth=4, fractionWidth=0, name='ggscad')
    item8.Add( item10, 0, wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT, 5 )

    item6.Add( item8, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

    item11 = wx.FlexGridSizer( 0, 3, 0, 0 )
    
    item12 = wx.StaticText( parent, ID_TEXT, "", wx.DefaultPosition, wx.DefaultSize, 0 )
    item11.Add( item12, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )

    item13 = wx.StaticText( parent, ID_TEXT, "Dal:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item11.Add( item13, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item14 = wx.StaticText( parent, ID_TEXT, "Al:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item11.Add( item14, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5 )

    item15 = wx.StaticText( parent, ID_TEXT, "Data scadenza:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item11.Add( item15, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item16 = DateCtrl( parent, ID_DATSCA1, "", wx.DefaultPosition, [80,-1], 0 )
    item16.SetName( "datsca1" )
    item11.Add( item16, 0, wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT, 5 )

    item17 = DateCtrl( parent, ID_DATSCA2, "", wx.DefaultPosition, [80,-1], 0 )
    item17.SetName( "datsca2" )
    item11.Add( item17, 0, wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT, 5 )

    item18 = wx.StaticText( parent, ID_TEXT, "Data documento:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item11.Add( item18, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP|wx.BOTTOM, 5 )

    item19 = DateCtrl( parent, ID_DATDOC1, "", wx.DefaultPosition, [80,-1], 0 )
    item19.SetName( "datdoc1" )
    item11.Add( item19, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

    item20 = DateCtrl( parent, ID_DATDOC2, "", wx.DefaultPosition, [80,-1], 0 )
    item20.SetName( "datdoc2" )
    item11.Add( item20, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

    item11.AddGrowableCol( 1 )

    item11.AddGrowableCol( 2 )

    item6.Add( item11, 0, wx.ALIGN_CENTER, 5 )

    item2.Add( item6, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

    item1.Add( item2, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item21 = wx.FlexGridSizer( 0, 1, 0, 0 )
    
    item23 = wx.StaticBox( parent, -1, "Partite" )
    item22 = wx.StaticBoxSizer( item23, wx.VERTICAL )
    
    item24 = wx.FlexGridSizer( 0, 1, 0, 0 )
    
    item25 = wx.FlexGridSizer( 0, 3, 0, 0 )
    
    item26 = UnoZeroCheckBox( parent, ID_ESC0, "Escludi escluse", wx.DefaultPosition, wx.DefaultSize, 0 )
    item26.SetValue( True )
    item26.SetName( "esc0" )
    item25.Add( item26, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

    item27 = UnoZeroCheckBox( parent, ID_ESC1, "Includi escluse", wx.DefaultPosition, wx.DefaultSize, 0 )
    item27.SetName( "esc1" )
    item25.Add( item27, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

    item28 = UnoZeroCheckBox( parent, ID_ESC2, "Solo escluse", wx.DefaultPosition, wx.DefaultSize, 0 )
    item28.SetName( "esc2" )
    item25.Add( item28, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

    item29 = UnoZeroCheckBox( parent, ID_INS0, "Escludi insolute", wx.DefaultPosition, wx.DefaultSize, 0 )
    item29.SetName( "ins0" )
    item25.Add( item29, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

    item30 = UnoZeroCheckBox( parent, ID_INS1, "Includi insolute", wx.DefaultPosition, wx.DefaultSize, 0 )
    item30.SetValue( True )
    item30.SetName( "ins1" )
    item25.Add( item30, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

    item31 = UnoZeroCheckBox( parent, ID_INS2, "Solo insolute", wx.DefaultPosition, wx.DefaultSize, 0 )
    item31.SetName( "ins2" )
    item25.Add( item31, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

    item32 = UnoZeroCheckBox( parent, ID_RIB0, "Escludi RIBA", wx.DefaultPosition, wx.DefaultSize, 0 )
    item32.SetName( "rib0" )
    item25.Add( item32, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

    item33 = UnoZeroCheckBox( parent, ID_RIB1, "Includi RIBA", wx.DefaultPosition, wx.DefaultSize, 0 )
    item33.SetValue( True )
    item33.SetName( "rib1" )
    item25.Add( item33, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

    item34 = UnoZeroCheckBox( parent, ID_RIB2, "Solo RIBA", wx.DefaultPosition, wx.DefaultSize, 0 )
    item34.SetName( "rib2" )
    item25.Add( item34, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

    item35 = UnoZeroCheckBox( parent, ID_RID0, "Escludi RID", wx.DefaultPosition, wx.DefaultSize, 0 )
    item35.SetName( "rid0" )
    item25.Add( item35, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

    item36 = UnoZeroCheckBox( parent, ID_RID1, "Includi RID", wx.DefaultPosition, wx.DefaultSize, 0 )
    item36.SetValue( True )
    item36.SetName( "rid1" )
    item25.Add( item36, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

    item37 = UnoZeroCheckBox( parent, ID_RID2, "Solo RID", wx.DefaultPosition, wx.DefaultSize, 0 )
    item37.SetName( "rid2" )
    item25.Add( item37, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

    item24.Add( item25, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item38 = UnoZeroCheckBox( parent, ID_LIVX, "Escludi se il sollecito del livello è già stato inviato", wx.DefaultPosition, wx.DefaultSize, 0 )
    item38.SetValue( True )
    item38.SetName( "livx" )
    item24.Add( item38, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

    item22.Add( item24, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item21.Add( item22, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

    item21.AddGrowableRow( 1 )

    item1.Add( item21, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item40 = wx.StaticBox( parent, -1, "Filtri" )
    item39 = wx.StaticBoxSizer( item40, wx.VERTICAL )
    
    item41 = wx.FlexGridSizer( 0, 2, 0, 0 )
    
    item42 = wx.StaticText( parent, ID_TEXT, "Agente:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item41.Add( item42, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.BOTTOM, 5 )

    item43 = alib.LinkTableAgente(parent, ID_AGENTE, name='id_agente')
    item41.Add( item43, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5 )

    item44 = wx.StaticText( parent, ID_TEXT, "Zona:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item41.Add( item44, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP|wx.BOTTOM, 5 )

    item45 = alib.LinkTableZona(parent, ID_ZONA, name='id_zona')
    item41.Add( item45, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

    item46 = wx.StaticText( parent, ID_TEXT, "Categoria:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item41.Add( item46, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP|wx.BOTTOM, 5 )

    item47 = alib.LinkTableCatCli(parent, ID_CATEG, name='id_categ')
    item41.Add( item47, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

    item48 = wx.StaticText( parent, ID_TEXT, "Status:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item41.Add( item48, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP|wx.BOTTOM, 5 )

    item49 = alib.LinkTableStatCli(parent, ID_STATUS, name='id_status')
    item41.Add( item49, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

    item41.AddGrowableCol( 1 )

    item39.Add( item41, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item1.Add( item39, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

    item1.AddGrowableCol( 2 )

    item0.Add( item1, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item50 = wx.FlexGridSizer( 0, 2, 0, 0 )
    
    item51 = wx.StaticText( parent, ID_TEXT, "Riepilogo clienti", wx.DefaultPosition, wx.DefaultSize, 0 )
    item51.SetForegroundColour( wx.BLUE )
    item50.Add( item51, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item52 = wx.StaticText( parent, ID_TEXT, "Partite scadute del cliente", wx.DefaultPosition, wx.DefaultSize, 0 )
    item52.SetForegroundColour( wx.BLUE )
    item50.Add( item52, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

    item53 = wx.Panel( parent, ID_PANGRIDTOT, wx.DefaultPosition, [500,400], wx.SUNKEN_BORDER )
    item53.SetName( "pangridtot" )
    item50.Add( item53, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item54 = wx.Panel( parent, ID_PANGRIDPCF, wx.DefaultPosition, [520,160], wx.SUNKEN_BORDER )
    item54.SetName( "pangridpcf" )
    item50.Add( item54, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5 )

    item55 = wx.FlexGridSizer( 0, 2, 0, 0 )
    
    item56 = wx.FlexGridSizer( 0, 2, 0, 0 )
    
    item55.Add( item56, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item57 = wx.FlexGridSizer( 1, 0, 0, 0 )
    
    item58 = wx.Button( parent, ID_BUTUPDATE, "Aggiorna dati", wx.DefaultPosition, wx.DefaultSize, 0 )
    item58.SetName( "butupdate" )
    item57.Add( item58, 0, wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM|wx.ALL, 5 )

    item59 = wx.Button( parent, ID_BUTPRTRIEP, "Stampa riepilogo", wx.DefaultPosition, wx.DefaultSize, 0 )
    item59.SetName( "butprtriep" )
    item57.Add( item59, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP|wx.BOTTOM, 5 )

    item60 = wx.Button( parent, ID_BUTEMAIL, "Invia email", wx.DefaultPosition, wx.DefaultSize, 0 )
    item60.SetName( "butemail" )
    item57.Add( item60, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP|wx.BOTTOM, 5 )

    item57.AddGrowableCol( 1 )

    item55.Add( item57, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item55.AddGrowableCol( 1 )

    item50.Add( item55, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item61 = wx.FlexGridSizer( 0, 2, 0, 0 )
    
    item62 = wx.Panel( parent, ID_PANCOLORS, wx.DefaultPosition, wx.DefaultSize, 0 )
    item62.SetName( "pancolors" )
    item61.Add( item62, 0, wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

    item61.AddGrowableCol( 1 )

    item50.Add( item61, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item50.AddGrowableCol( 0 )

    item50.AddGrowableCol( 1 )

    item50.AddGrowableRow( 1 )

    item0.Add( item50, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item0.AddGrowableCol( 0 )

    item0.AddGrowableRow( 1 )

    if set_sizer == True:
        parent.SetSizer( item0 )
        if call_fit == True:
            item0.SetSizeHints( parent )
    
    return item0

# Menubar functions

# Toolbar functions

# Bitmap functions


# End of generated file