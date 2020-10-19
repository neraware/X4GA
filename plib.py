#!/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         plib.py
# Copyright:    (C) 2015 Fabio Cassini <fc@f4b10.org>
# ------------------------------------------------------------------------------


import version
import glob

def get_ext_ver(module):
    return getattr(module, 'min_require_x4', 
           getattr(module, '__min_require_x4__', None))


def test_ext_req(module):
    x4min = get_ext_ver(module)
    return x4min is None or version.VERSION_STRING >= x4min


def get_reqfail_msg(_type, _name, _module):
    assert type(_type) is str and _type in 'PC'
    x4min = get_ext_ver(_module)
    if _type == "C":
        desc = "la personalizzazione '%s'" % _name
    else:
        desc = "il plugin '%s'" % _name
    msg = u"La versione di X4GA non è compatibile con %s.\n\n" % desc
    msg += u"E' richiesta almeno la versione %s, e' installata la %s.\n\n"\
                % (x4min, version.VERSION_STRING)
    msg += u"Alcune parti del programma potrebbero avere problemi, aggiornare X4GA quanto prima."
    return msg



class PluginException(Exception):
    pass


def load_plugin(plugin_name):
    if plugin_name.startswith('fatturapa'):
        return None
    import Env
    plugins = Env.plugins
    plugin_name = plugin_name.replace('_plugin', '')
    if plugin_name in plugins:
        return plugins[plugin_name]
    plugin_func = plugin_name+'_plugin'
    m = __import__(plugin_func, {}, {}, False)
    plugins[plugin_name] = m
    if not test_ext_req(m):
        raise PluginException, get_reqfail_msg("P", plugin_name, m)
    if hasattr(m, 'TabStru'):
        m.TabStru(Env.Azienda.BaseTab)
    return m


def load_plugins(plugin_names):
    for plugin_name in plugin_names:
        load_plugin(plugin_name)


def clear_plugins():
    import Env
    Env.plugins.clear()


def get_plugin_names(enabled=True):
    import Env
    setup = Env.adb.DbTable('cfgsetup', 'setup')
    setup.AddFilter('setup.chiave LIKE "%_plugin_version"')
    if enabled:
        setup.AddFilter('(setup.flag="1" OR setup.flag IS NULL)')
    else:
        setup.AddFilter('setup.flag="0"')
    setup.AddOrder('setup.importo')
    setup.Retrieve()
    return [setup.chiave.split('_')[0] for _ in setup if not 'fatturapa' in setup.chiave]


def init_plugins():
    import Env
    for name in get_plugin_names():
        if not name in Env.plugins:
            try:
                if name.startswith('fatturapa'):
                    continue
                load_plugin(name)
            except PluginException:
                cap = u"Questa versione di X4GA è obsoleta!"
                msg = get_reqfail_msg("P", name, Env.plugins[name])
                raise Exception, cap+' '+msg
            except Exception, e:
                cap = u"Errore in caricamento plugin!"
                msg = ' -'.join(map(str, e.args))
                raise Exception, cap+' '+msg



def check_new_plugins(read_setup=True):
    import Env
    files = glob.glob(Env.opj(Env.plugin_base_path, '*.zip'))
    files.sort()
    new_plugins = []
    for _file in files:
        _file = _file.replace('\\','/')
        n = _file.rindex('/')
        name = _file[n+1:-4]
        if not name in Env.plugins and not 'fatturapa' in name:
            if read_setup:
                #test plugin disabilitato sull'azienda
                setup = Env.adb.DbTable('cfgsetup', 'setup')
                setup.AddFilter('setup.chiave="%s_plugin_version" AND setup.flag=0' % name)
                setup.Retrieve()
                append = setup.IsEmpty()
            else:
                append = True
            if append:
                new_plugins.append(name)
    return new_plugins


def load_new_plugins(write_changes=True):
    import wx
    import awc.controls.windows as aw
    for new_plugin in check_new_plugins(read_setup=write_changes):
        msg = "E' disponibile il nuovo plugin '%s': lo vuoi attivare ?" % new_plugin
        stl = wx.ICON_QUESTION|wx.YES_NO|wx.YES_DEFAULT
        resp = aw.awu.MsgDialog(None, msg, style=stl)
        if resp == wx.ID_YES:
            try:
                load_plugin(new_plugin)
                if write_changes:
                    activate_new_plugin(new_plugin)
            except Exception, e:
                msg = "Errore durante il caricamento del plugin:\n%s" % ' - '.join(e.args)
                aw.awu.MsgDialog(None, msg, style=wx.ICON_ERROR)
        elif resp == wx.ID_NO and write_changes:
            msg = "Il plugin '%s' verrà disattivato su tutte le postazioni dell'azienda." % new_plugin
            msg += "\nConfermi la disattivazione ?" 
            stl = wx.ICON_QUESTION|wx.YES_NO|wx.NO_DEFAULT
            resp = aw.awu.MsgDialog(None, msg, style=stl)
            if resp == wx.ID_YES:
                enable_plugin(new_plugin, False)
                msg = "Il plugin '%s' è stato disattivato su tutte le postazioni dell'azienda." % new_plugin
                msg += "\nPotrà essere riattivato in fase di login selezionando l'azienda"
                msg += "\ncon la combinazione di tasti Ctrl-Invio." 
                aw.awu.MsgDialog(None, msg, style=wx.ICON_INFORMATION)


def activate_new_plugin(plugin_name):
    import Env
    setup = Env.adb.DbTable('cfgsetup', 'setup')
    setup.AddFilter('setup.chiave LIKE "%s_plugin_version"' % plugin_name)
    setup.Retrieve()
    if setup.IsEmpty():
        setup.CreateNewRow()
        setup.chiave = '%s_plugin_version' % plugin_name
        setup.flag = '1'
    setup.Save()


def enable_plugin(plugin_name, enable=True):
    import Env
    setup = Env.adb.DbTable('cfgsetup', 'setup')
    setup.AddFilter('setup.chiave LIKE "%s_plugin_version"' % plugin_name)
    setup.Retrieve()
    if setup.IsEmpty():
        setup.CreateNewRow()
        setup.chiave = '%s_plugin_version' % plugin_name
    setup.flag = str(int(enable))
    setup.Save()
