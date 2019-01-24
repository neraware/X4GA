# -*- coding: UTF-8 -*-

#-----------------------------------------------------------------------------
# Python source generated by wxDesigner from file: export.wdr
# Do not modify this file, all changes will be lost!
#-----------------------------------------------------------------------------

# Include wxPython modules
import wx
import wx.grid
import wx.animate

# Custom source
from awc.controls.datectrl import DateCtrl
from awc.controls.numctrl import NumCtrl
from awc.controls.radiobox import RadioBox
import anag.lib as alib


class ColorsPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        ColorsFunc(self)

class TipiClientiRadioBox(RadioBox):
    def __init__(self, *args, **kwargs):
        RadioBox.__init__(self, *args, **kwargs)
        self.SetDataLink(values=('T','B','P'))



# Window functions

ID_TEXT = 10000
ID_CHECKBOX = 10001
ID_DATA1 = 10002
ID_DATA2 = 10003
ID_BUTSRC = 10004
ID_RADIOBOX = 10005
ID_NUMPROGR = 10006
ID_BUTGEN = 10007
ID_PANGRIDOCS = 10008
ID_PANEL = 10009

def FtelExportFunc( parent, call_fit = True, set_sizer = True ):
    item0 = wx.FlexGridSizer( 0, 1, 0, 0 )
    
    item1 = wx.FlexGridSizer( 1, 0, 0, 0 )
    
    item3 = wx.StaticBox( parent, -1, "Periodo documenti" )
    item2 = wx.StaticBoxSizer( item3, wx.HORIZONTAL )
    
    item4 = wx.FlexGridSizer( 0, 3, 0, 0 )
    
    item5 = wx.StaticText( parent, ID_TEXT, "Dal:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item4.Add( item5, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item6 = wx.StaticText( parent, ID_TEXT, "Al:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item4.Add( item6, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5 )

    item7 = wx.CheckBox( parent, ID_CHECKBOX, "Selez.Aut.", wx.DefaultPosition, wx.DefaultSize, 0 )
    item7.SetValue( True )
    item7.SetName( "selaut" )
    item4.Add( item7, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

    item8 = DateCtrl( parent, ID_DATA1, "", wx.DefaultPosition, [80,-1], 0 )
    item8.SetName( "data1" )
    item4.Add( item8, 0, wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item9 = DateCtrl( parent, ID_DATA2, "", wx.DefaultPosition, [80,-1], 0 )
    item9.SetName( "data2" )
    item4.Add( item9, 0, wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item10 = wx.Button( parent, ID_BUTSRC, "Cerca", wx.DefaultPosition, wx.DefaultSize, 0 )
    item10.SetDefault()
    item10.SetName( "butsrc" )
    item4.Add( item10, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item2.Add( item4, 0, wx.ALIGN_CENTER, 5 )

    item1.Add( item2, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP|wx.BOTTOM, 5 )

    item11 = TipiClientiRadioBox( parent, ID_RADIOBOX, "Clienti", wx.DefaultPosition, wx.DefaultSize, 
        ["Tutti","Solo B2B","Solo PA"] , 1, wx.RA_SPECIFY_COLS )
    item11.SetName( "tipicli" )
    item1.Add( item11, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

    item13 = wx.StaticBox( parent, -1, "Status" )
    item12 = wx.StaticBoxSizer( item13, wx.HORIZONTAL )
    
    item14 = wx.FlexGridSizer( 0, 3, 0, 0 )
    
    item15 = wx.CheckBox( parent, ID_CHECKBOX, "Da generare", wx.DefaultPosition, wx.DefaultSize, 0 )
    item15.SetValue( True )
    item15.SetName( "status_x" )
    item14.Add( item15, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item16 = wx.CheckBox( parent, ID_CHECKBOX, "Generato", wx.DefaultPosition, wx.DefaultSize, 0 )
    item16.SetName( "status_g" )
    item14.Add( item16, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item17 = wx.CheckBox( parent, ID_CHECKBOX, "Attesa esito", wx.DefaultPosition, wx.DefaultSize, 0 )
    item17.SetName( "status_aq" )
    item14.Add( item17, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item18 = wx.CheckBox( parent, ID_CHECKBOX, "Consegnato", wx.DefaultPosition, wx.DefaultSize, 0 )
    item18.SetName( "status_c" )
    item14.Add( item18, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item19 = wx.CheckBox( parent, ID_CHECKBOX, "Mancata cons.", wx.DefaultPosition, wx.DefaultSize, 0 )
    item19.SetName( "status_m" )
    item14.Add( item19, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item20 = wx.CheckBox( parent, ID_CHECKBOX, "Errore", wx.DefaultPosition, wx.DefaultSize, 0 )
    item20.SetName( "status_e" )
    item14.Add( item20, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item12.Add( item14, 0, wx.ALIGN_CENTER, 5 )

    item1.Add( item12, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP|wx.BOTTOM, 5 )

    item22 = wx.StaticBox( parent, -1, "Trasmissione documenti selezionati" )
    item21 = wx.StaticBoxSizer( item22, wx.HORIZONTAL )
    
    item23 = wx.FlexGridSizer( 1, 0, 0, 0 )
    
    item24 = wx.StaticText( parent, ID_TEXT, "Progressivo trasmissione:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item23.Add( item24, 0, wx.ALIGN_CENTER|wx.LEFT|wx.BOTTOM, 5 )

    item25 = NumCtrl(parent, integerWidth=5, fractionWidth=0, allowNegative=False); item25.SetName('numprogr')
    item23.Add( item25, 0, wx.ALIGN_CENTER|wx.LEFT|wx.BOTTOM, 5 )

    item26 = wx.Button( parent, ID_BUTGEN, "Genera file", wx.DefaultPosition, wx.DefaultSize, 0 )
    item26.SetName( "butgen" )
    item26.Enable(False)
    item23.Add( item26, 0, wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item21.Add( item23, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

    item1.Add( item21, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP|wx.BOTTOM, 5 )

    item1.AddGrowableCol( 3 )

    item0.Add( item1, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item27 = wx.StaticText( parent, ID_TEXT, "Documenti da esportare e trasmettere:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item27.SetForegroundColour( wx.BLUE )
    item0.Add( item27, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5 )

    item28 = wx.Panel( parent, ID_PANGRIDOCS, wx.DefaultPosition, [1050,250], wx.SUNKEN_BORDER )
    item28.SetName( "pangridocs" )
    item0.Add( item28, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item29 = ColorsPanel( parent, ID_PANEL, wx.DefaultPosition, wx.DefaultSize, 0 )
    item0.Add( item29, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item0.AddGrowableCol( 0 )

    item0.AddGrowableRow( 2 )

    if set_sizer == True:
        parent.SetSizer( item0 )
        if call_fit == True:
            item0.SetSizeHints( parent )
    
    return item0

ID_BUTRIC = 10010

def FtelNotificheFunc( parent, call_fit = True, set_sizer = True ):
    item0 = wx.FlexGridSizer( 0, 1, 0, 0 )
    
    item1 = wx.StaticText( parent, ID_TEXT, "Documenti in attesa di notifica:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item1.SetForegroundColour( wx.BLUE )
    item0.Add( item1, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

    item2 = wx.Panel( parent, ID_PANGRIDOCS, wx.DefaultPosition, [1000,250], wx.SUNKEN_BORDER )
    item2.SetName( "pangridocs" )
    item0.Add( item2, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item3 = wx.FlexGridSizer( 0, 2, 0, 0 )
    
    item4 = ColorsPanel( parent, ID_PANEL, wx.DefaultPosition, wx.DefaultSize, 0 )
    item3.Add( item4, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item5 = wx.Button( parent, ID_BUTRIC, "Avvia ricezione notifiche", wx.DefaultPosition, wx.DefaultSize, 0 )
    item5.SetName( "butric" )
    item5.Enable(False)
    item3.Add( item5, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item3.AddGrowableCol( 1 )

    item0.Add( item3, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item0.AddGrowableCol( 0 )

    item0.AddGrowableRow( 1 )

    if set_sizer == True:
        parent.SetSizer( item0 )
        if call_fit == True:
            item0.SetSizeHints( parent )
    
    return item0


def ColorsFunc( parent, call_fit = True, set_sizer = True ):
    item0 = wx.FlexGridSizer( 0, 1, 0, 0 )
    
    item1 = wx.FlexGridSizer( 1, 0, 0, 0 )
    
    item2 = wx.Panel( parent, ID_PANEL, wx.DefaultPosition, [20,20], wx.SUNKEN_BORDER )
    item2.SetName( "panel_status_x" )
    item1.Add( item2, 0, wx.ALIGN_CENTER, 5 )

    item3 = wx.StaticText( parent, ID_TEXT, "XML da generare", wx.DefaultPosition, wx.DefaultSize, 0 )
    item1.Add( item3, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

    item4 = wx.StaticText( parent, ID_TEXT, "", wx.DefaultPosition, [24,-1], 0 )
    item1.Add( item4, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

    item5 = wx.Panel( parent, ID_PANEL, wx.DefaultPosition, [20,20], wx.SUNKEN_BORDER )
    item5.SetName( "panel_status_g" )
    item1.Add( item5, 0, wx.ALIGN_CENTER, 5 )

    item6 = wx.StaticText( parent, ID_TEXT, "XML generato", wx.DefaultPosition, wx.DefaultSize, 0 )
    item1.Add( item6, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

    item7 = wx.StaticText( parent, ID_TEXT, "", wx.DefaultPosition, [24,-1], 0 )
    item1.Add( item7, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

    item8 = wx.Panel( parent, ID_PANEL, wx.DefaultPosition, [20,20], wx.SUNKEN_BORDER )
    item8.SetName( "panel_status_q" )
    item1.Add( item8, 0, wx.ALIGN_CENTER, 5 )

    item9 = wx.StaticText( parent, ID_TEXT, "In coda per SDI", wx.DefaultPosition, wx.DefaultSize, 0 )
    item1.Add( item9, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

    item10 = wx.StaticText( parent, ID_TEXT, "", wx.DefaultPosition, [24,-1], 0 )
    item1.Add( item10, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

    item11 = wx.Panel( parent, ID_PANEL, wx.DefaultPosition, [20,20], wx.SUNKEN_BORDER )
    item11.SetName( "panel_status_a" )
    item1.Add( item11, 0, wx.ALIGN_CENTER, 5 )

    item12 = wx.StaticText( parent, ID_TEXT, "Attesa esito", wx.DefaultPosition, wx.DefaultSize, 0 )
    item1.Add( item12, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

    item13 = wx.StaticText( parent, ID_TEXT, "", wx.DefaultPosition, [24,-1], 0 )
    item1.Add( item13, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

    item14 = wx.Panel( parent, ID_PANEL, wx.DefaultPosition, [20,20], wx.SUNKEN_BORDER )
    item14.SetName( "panel_status_c" )
    item1.Add( item14, 0, wx.ALIGN_CENTER, 5 )

    item15 = wx.StaticText( parent, ID_TEXT, "Consegnato", wx.DefaultPosition, wx.DefaultSize, 0 )
    item1.Add( item15, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

    item16 = wx.StaticText( parent, ID_TEXT, "", wx.DefaultPosition, [24,-1], 0 )
    item1.Add( item16, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

    item17 = wx.Panel( parent, ID_PANEL, wx.DefaultPosition, [20,20], wx.SUNKEN_BORDER )
    item17.SetName( "panel_status_m" )
    item1.Add( item17, 0, wx.ALIGN_CENTER, 5 )

    item18 = wx.StaticText( parent, ID_TEXT, "Mancata consegna", wx.DefaultPosition, wx.DefaultSize, 0 )
    item1.Add( item18, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

    item19 = wx.StaticText( parent, ID_TEXT, "", wx.DefaultPosition, [24,-1], 0 )
    item1.Add( item19, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

    item20 = wx.Panel( parent, ID_PANEL, wx.DefaultPosition, [20,20], wx.SUNKEN_BORDER )
    item20.SetName( "panel_status_e" )
    item1.Add( item20, 0, wx.ALIGN_CENTER, 5 )

    item21 = wx.StaticText( parent, ID_TEXT, "Errore", wx.DefaultPosition, wx.DefaultSize, 0 )
    item1.Add( item21, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

    item0.Add( item1, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    if set_sizer == True:
        parent.SetSizer( item0 )
        if call_fit == True:
            item0.SetSizeHints( parent )
    
    return item0

# Menubar functions

# Toolbar functions

# Bitmap functions


# End of generated file
