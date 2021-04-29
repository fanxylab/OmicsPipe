#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
***********************************************************
* Author  : Zhou Wei                                      *
* Date    : 2020/09/09 10:42:02                           *
* E-mail  : welljoea@gmail.com                            *
* Version : --                                            *
* You are using the program scripted by Zhou Wei.         *
* If you find some bugs, please                           *
* Please let me know and acknowledge in your publication. *
* Thank you!                                              *
* Best wishes!                                            *
***********************************************************
'''
import pandas as pd
import numpy as  np
import re
import os
import sys
import time
import traceback
from Logger  import Logger
from ArgsPipe import Args

'''
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 100000)
pd.set_option('display.width', 100000)
'''

from joblib import Parallel, delayed
class MakeFlow:
    def __init__(self, arg, log,  *array, **dicts):
        self.arg = arg
        self.log = log
        self.array  = array
        self.dicts  = dicts
        self.scriptdir = os.path.dirname(os.path.realpath(__file__))
        self.wdir = self.arg.outdir + '/WorkShell'
        os.makedirs(self.wdir, exist_ok=True)
        self.Pipeline={
            'ATAC': self.scriptdir + '/OMICS/ATAC',
            'CHIP': self.scriptdir + '/OMICS/CHIP',
            'SS2' : self.scriptdir + '/OMICS/SS2',
            '10XRNA'  : self.scriptdir +'/OMICS/Genom10XRNA',
            'PLASMID' : '/share/home/share/Pipeline/01NGSDNA/PlasmidPipe',
        }

    def mkinfo(self, d ):
        infors='''
SID={Sampleid}
RID={Uniqueid}
CID={Control}
Lane={Lane}
Rep={Rep}
AID={AID}
TID={TID}
LID={LID}
AIDs=({AIDs})
TIDs=({TIDs})
LIDs=({LIDs})
Group={Group}
R1={R1}
R2={R2}
OUT={Outdir}
AUT={Outdir}/{Sampleid}/{Module}/
Species={Species}
Module={Module}
WORKFLOW_DIR={WORKFLOW_DIR}'''.format(**d).strip()
        f=open('%s/%s_%s.input'%(self.wdir, d['AID'], d['Module'] ), 'w')
        f.write(infors)
        f.close()

    def mk10xinfo(self, d ):
        infors='''
SID={Sampleid}
UIDs=({UIDs})
HIDs=({HIDs})
R1s=({R1s})
R2s=({R2s})
OUT={Outdir}
AUT={Outdir}/{Sampleid}/{Module}/
Species={Species}
Module={Module}
WORKFLOW_DIR={WORKFLOW_DIR}'''.format(**d).strip()
        f=open('%s/%s_%s.input'%(self.wdir, d['Sampleid'], d['Module'] ), 'w')
        f.write(infors)
        f.close()

    def mkshell(self, df):
        allmf = []
        for _, _d in df[['Sampleid','Module','WORKFLOW_DIR','Outdir']].drop_duplicates().iterrows():
            os.system('sh %s/Create_Makeflow.sh %s %s %s'%(_d['WORKFLOW_DIR'], self.wdir, _d['Sampleid'], _d['Module']) )
            allmf.append( '{0}/{1}/{2}/WorkShell/{1}_{2}.mf'.format(_d.Outdir, _d.Sampleid, _d.Module))
        try:
            os.remove('%s/all_makeflow.mf.makeflowlog'%self.wdir)
            os.remove('%s/all_makeflow.mf'%self.wdir)
        except FileNotFoundError:
            pass
        else:
            pass

        os.system( 'cat %s > %s/all_makeflow.mf'%(' '.join(allmf), self.wdir) )
        if self.arg.qsub:
            os.system( 'nohup makeflow -T sge %s/all_makeflow.mf &'%self.wdir )

    def _getinfo(self):
        infodf = pd.read_csv(self.arg.input, sep='\t', comment='#')
        infodf.columns = infodf.columns.str.capitalize()

        infodf['Outdir'] = infodf['Outdir'].fillna(self.arg.outdir)
        infodf['Module'] = infodf.Module.str.upper()
        infodf['WORKFLOW_DIR'] = infodf.Module.map(self.Pipeline)
        infodf[['R1','R2']] = infodf['Fastq'].str.split('[;,]',expand=True).iloc[:,:2]
        return infodf

    def _addinfo(self, _G):
        _G['AID'] = _G['Sampleid'].str.cat( _G[['Rep', 'Lane']].astype(str),sep='__')
        _G['TID'] = _G['Sampleid'].str.cat( _G[['Rep' ]].astype(str),sep='__')
        _G['LID'] = _G['Sampleid'].str.cat( _G[['Lane']].astype(str),sep='__')

        _G['LIDs'] = _G.groupby(['Sampleid', 'Rep'])['AID'].transform(lambda x : ' '.join(x)) 
        _G['AIDs'] = _G.groupby(['Sampleid'])['AID'].transform(lambda x : ' '.join(x))
        _G['TIDs'] = _G.groupby(['Sampleid'])['TID'].transform(lambda x : ' '.join(np.unique(x)))
        _G = _G.astype(str).fillna('nan')
        Parallel( n_jobs=-1 )\
                ( delayed( self.mkinfo )(_d.to_dict()) for _, _d in _G.iterrows() )

        return _G[['Sampleid','Module','WORKFLOW_DIR','Outdir']]

    def _10xinfo(self, _G):
        #_G['I1'] = I1
        _G['HID']  =  _G.Uniqueid.str.cat( _G[['Rep', 'Lane']], sep='_')
        _G['UIDs'] =  _G.groupby(['Sampleid'])['Uniqueid'].transform(lambda x : ' '.join(x))
        _G['HIDs'] =  _G.groupby(['Sampleid'])['HID'].transform(lambda x : ' '.join(x))
        _G['R1s']  =  _G.groupby(['Sampleid'])['R1'].transform(lambda x : ' '.join(x))
        _G['R2s']  =  _G.groupby(['Sampleid'])['R2'].transform(lambda x : ' '.join(x))

        _G.drop(['Uniqueid', 'Lane', 'Rep', 'HID', 'Fastq', 'R1', 'R2'], axis=1, inplace=True)
        _G.drop_duplicates(keep='first', inplace=True)
        Parallel( n_jobs=-1 )\
                ( delayed( self.mk10xinfo )(_d.to_dict()) for _, _d in _G.iterrows() )
        return _G[['Sampleid','Module','WORKFLOW_DIR','Outdir']]

    def mkflow(self):
        infodf = self._getinfo()
        if 'Control' in infodf.columns  :
            infodf.sort_values(by='Control', ascending=True,  na_position='first', inplace=True)

        infos  = []
        for _m, _g in infodf.groupby('Module', sort=False):
            if not _m in ['10XRNA']:
                infos.append(self._addinfo(_g))
            else:
                infos.append(self._10xinfo(_g))
        infos = pd.concat(infos, axis=0)
        self.mkshell(infos)

class Pipeline():
    def __init__(self, arg, log,  *array, **dicts):
        self.arg = arg
        self.log = log
        self.array  = array
        self.dicts  = dicts

    def Pipe(self):
        MakeFlow(self.arg, self.log).mkflow()

def Commands():
    info ='''
***********************************************************
* Author : Zhou Wei                                       *
* Date   : %s                       *
* E-mail : welljoea@gmail.com                             *
* You are using The scripted by Zhou Wei.                 *
* If you find some bugs, please email to me.              *
* Please let me know and acknowledge in your publication. *
* Sincerely                                               *
* Best wishes!                                            *
***********************************************************
'''%(time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()))

    args = Args()
    Log = Logger( '%s/Pipelog.log'%(args.outdir) ) #, args.commands
    os.makedirs( os.path.dirname(args.outdir) , exist_ok=True)

    Log.NI(info.strip())
    Log.NI("The argument you have set as follows:".center(59, '*'))
    for i,k in enumerate(vars(args),start=1):
        Log.NI('**%s|%-13s: %s'%(str(i).zfill(2), k, str(getattr(args, k))) )
    Log.NI(59 * '*')

    try:
        Pipeline(args, Log).Pipe()
        Log.CI('Success!!!')
    except Exception:
        Log.CW('Failed!!!')
        traceback.print_exc()
    finally:
        Log.CI('You can check your progress in log file.')
Commands()
