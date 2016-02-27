# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         contab/incpagdet_db.py
# Copyright:    (C) 2015 Fabio Cassini <fc@f4b10.org>
# ------------------------------------------------------------------------------


import stormdb as adb


def get_cassa_filter(id_cassa, 
                     datmin, datmax, 
                     is_entrate, is_uscite, id_reg=None):
    if id_reg:
        and_filter = ' AND reg.id=%d' % id_reg
    else:
        f = []
        if id_cassa:
            f.append('pca.id=%s' % id_cassa)
        if datmin:
            f.append('reg.datreg>="%s"' % datmin.Format('%Y-%m-%d'))
        if datmax:
            f.append('reg.datreg<="%s"' % datmax.Format('%Y-%m-%d'))
        if not is_entrate and not is_uscite:
            f.append('0')
        elif not is_entrate:
            f.append('mva.segno<>"D"')
        elif not is_uscite:
            f.append('mva.segno<>"A"')
        and_filter = ''
        if f:
            and_filter = ' AND %s' % ' AND '.join([x for x in f])
    return and_filter


class ElencoRegistrazioni(adb.DbMem):
    
    def __init__(self):
        adb.DbMem.__init__(self, 'id_reg,id_cassa,codcassa,descassa,datreg,id_causale,codcausale,descausale,id_anag,codanag,desanag,dare,avere')
        self.Reset()


class SottocontiCassaBanca(adb.DbMem):
    
    def __init__(self):
        adb.DbMem.__init__(self, 'id,codice,descriz,id_tipana,codtipana,destipana')
        self.Reset()


class DettaglioIncassiPagamenti(adb.DbMem):
    
    def __init__(self):
        adb.DbMem.__init__(self, 'id_reg,id_cassa,codcassa,descassa,datreg,id_causale,codcausale,descausale,id_anag,codanag,desanag,note,importo,operazione,spesa,abbuono,tipabb,id_caudoc,codcaudoc,descaudoc,id_pcf,numdoc,datdoc,dare,avere')
        self.Reset()
    
    def get_sottoconti_movimentati(self, 
                                   datmin=None, datmax=None, 
                                   is_entrate=True, is_uscite=True):
        and_filter = get_cassa_filter(id_cassa=None, 
                                      datmin=datmin, datmax=datmax,
                                      is_entrate=is_entrate,
                                      is_uscite=is_uscite,)
        cmd = """
            SELECT
            pca.id         'id_cassa',
            pca.codice     'codcassa',
            pca.descriz    'descassa',
            tpa.id         'id_tipana',
            tpa.codice     'codtipana',
            tpa.descriz    'destipana'
            FROM contab_s  sca
            JOIN contab_h  reg ON reg.id=sca.id_reg
            JOIN contab_b  mvc ON mvc.id_reg=reg.id AND mvc.numriga=1
            JOIN contab_b  mva ON mva.id_reg=reg.id AND mva.numriga=2
            JOIN pdc       pcc ON pcc.id=mvc.id_pdcpa
            JOIN pdc       pca ON pca.id=mva.id_pdcpa
            JOIN pdctip    tpa ON tpa.id=pca.id_tipo
            JOIN cfgcontab cau ON cau.id=reg.id_caus
       LEFT JOIN           pcf ON pcf.id=sca.id_pcf
       LEFT JOIN cfgcontab cap ON cap.id=pcf.id_caus
            WHERE tpa.tipo IN ("A", "B", "D") 
              AND cau.pcfscon='1' %(and_filter)s
            GROUP BY pca.id, pca.codice, pca.descriz
            ORDER BY tpa.codice, pca.codice
        """ % locals()
        db = adb.db.__database__
        db.Retrieve(cmd)
        sm = SottocontiCassaBanca()
        sm.Reset()
        sm.SetRecordset([]+db.rs)
        return sm
    
    def get_registrazioni(self, id_cassa=None, 
                 datmin=None, datmax=None,
                 is_entrate=True, is_uscite=True):
        
        and_filter = get_cassa_filter(id_cassa, 
                                      datmin, datmax,
                                      is_entrate, is_uscite)
        cmd = """
            SELECT
            reg.id      'id_reg',
            pca.id      'id_cassa',
            pca.codice  'codcassa',
            pca.descriz 'descassa',
            reg.datreg  'datreg',
            cau.id      'id_causale',
            cau.codice  'codcausale',
            cau.descriz 'descausale',
            pcc.id      'id_anag',
            pcc.codice  'codanag',
            pcc.descriz 'desanag',
        SUM(IF(mva.segno="D", mva.importo, 0)) 'dare',
        SUM(IF(mva.segno="A", mva.importo, 0)) 'avere'
            FROM contab_b  mva
            JOIN contab_h  reg ON reg.id=mva.id_reg
            JOIN contab_b  mvc ON mvc.id_reg=reg.id AND mvc.numriga=1
            JOIN pdc       pca ON pca.id=mva.id_pdcpa
            JOIN pdc       pcc ON pcc.id=mvc.id_pdcpa
            JOIN cfgcontab cau ON cau.id=reg.id_caus
            WHERE cau.pcfscon='1' %(and_filter)s
            GROUP BY reg.id, pca.id, pca.codice, pca.descriz, reg.datreg, cau.id, cau.codice, cau.descriz, pcc.id, pcc.codice, pcc.descriz
            ORDER BY reg.datreg, reg.id
        """ % locals()
        db = adb.db.__database__
        db.Retrieve(cmd)
        er = ElencoRegistrazioni()
        er.SetRecordset([]+db.rs)
        return er
    
    def get_data(self, id_cassa=None, 
                 datmin=None, datmax=None,
                 is_entrate=True, is_uscite=True, id_reg=None):
        
        and_filter = get_cassa_filter(id_cassa, 
                                      datmin, datmax,
                                      is_entrate, is_uscite, id_reg)
        cmd = """
            SELECT
            reg.id      'id_reg',
            pca.id      'id_cassa',
            pca.codice  'codcassa',
            pca.descriz 'descassa',
            reg.datreg  'datreg',
            cau.id      'id_causale',
            cau.codice  'codcausale',
            cau.descriz 'descausale',
            pcc.id      'id_anag',
            pcc.codice  'codanag',
            pcc.descriz 'desanag',
            mvc.note    'note',
            sca.importo 'importo',
            sca.importo*
            IF(mva.segno="D",1,-1)
                        'operazione',
            sca.spesa   'spesa',
            sca.abbuono 'abbuono',
            sca.tipabb  'tipabb',
            cap.id      'id_caudoc',
            cap.codice  'codcaudoc',
            cap.descriz 'descaudoc',
            pcf.id      'id_pcf',
            pcf.numdoc  'numdoc',
            pcf.datdoc  'datdoc',
         IF(mva.segno="D", mva.importo, 0) 'dare',
         IF(mva.segno="A", mva.importo, 0) 'avere'
            FROM contab_s  sca
            JOIN contab_h  reg ON reg.id=sca.id_reg
            JOIN contab_b  mvc ON mvc.id_reg=reg.id AND mvc.numriga=1
            JOIN contab_b  mva ON mva.id_reg=reg.id AND mva.numriga=2
            JOIN pdc       pcc ON pcc.id=mvc.id_pdcpa
            JOIN pdc       pca ON pca.id=mva.id_pdcpa
            JOIN cfgcontab cau ON cau.id=reg.id_caus
       LEFT JOIN           pcf ON pcf.id=sca.id_pcf
       LEFT JOIN cfgcontab cap ON cap.id=pcf.id_caus
            WHERE cau.pcfscon='1' %(and_filter)s
            ORDER BY reg.datreg
        """ % locals()
        db = adb.db.__database__
        db.Retrieve(cmd)
        self.SetRecordset([]+db.rs)
        self._totali = self.get_totali()
    
    def get_conti_pareggiati(self):
        conti = []
        if self.id_pcf:
            id_pcf = self.id_pcf
            cmd = """
                SELECT pdc.descriz 'sottoconto'
                  FROM contab_b  mov
                  JOIN           pdc ON pdc.id=mov.id_pdcpa
                  JOIN contab_h  reg ON reg.id=mov.id_reg
                  JOIN cfgcontab cau ON cau.id=reg.id_caus
                 WHERE mov.numriga>1 AND mov.tipriga="C" AND reg.id IN (
                
                SELECT _sca.id_reg
                  FROM contab_s _sca
                  JOIN contab_h _reg ON _reg.id=_sca.id_reg AND _reg.id_regiva IS NOT NULL
                 WHERE _sca.id_pcf=%(id_pcf)s
                
                )
            """ % locals()
            db = adb.db.__database__
            db.Retrieve(cmd)
            conti = [x[0] for x in db.rs]
        return conti
    
    def get_totali(self):
        ci, cd, ca = map(lambda x: self._GetFieldIndex(x), 'id_reg dare avere'.split())
        td = ta = 0
        li = None
        for r in self.GetRecordset():
            if r[ci] != li:
                li = r[ci]
                td += r[cd]
                ta += r[ca]
        return {'tot_dare': td,
                'tot_avere': ta,
                'saldo_dare': max(0, td-ta),
                'saldo_avere': max(0, ta-td),}
