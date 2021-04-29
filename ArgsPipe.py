#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
***********************************************************
* Author  : Zhou Wei                                      *
* Date    : 2020/09/09 10:54:33                           *
* E-mail  : welljoea@gmail.com                            *
* Version : --                                            *
* You are using the program scripted by Zhou Wei.         *
* If you find some bugs, please                           *
* Please let me know and acknowledge in your publication. *
* Thank you!                                              *
* Best wishes!                                            *
***********************************************************
'''

import argparse
import os
def Args():
    parser = argparse.ArgumentParser(
                formatter_class=argparse.RawDescriptionHelpFormatter,
                prefix_chars='-+',
                conflict_handler='resolve',
                description="",
                epilog="")

    parser.add_argument('-V','--version',action ='version',
                version='NGS pipeline version 0.1')
    parser.add_argument("-i", "--input",type=str,
                    help='''the input file. You can use comma, semicolon or at to split multiple files''')
    parser.add_argument("-o", "--outdir", type=str, default=os.getcwd(),
                    help="output file dir. [Default: %(default)s]")
    parser.add_argument("-p", "--prefix",type=str,default='',
                    help="output file header, default=None.")
    parser.add_argument("-T", "--jobway",type=str, default='sge',
                    help="select your desired batch system. [Default: %(default)s]")
    parser.add_argument("-q", "--qsub", action='store_true' , default=False,
                    help='''whether submition the task. [Default: %(default)s]''')
    parser.add_argument("-ff", "--flowfile", type=str,
                    help="Input makeflow files. You can use comma, semicolon or at to split multiple files")

    args  = parser.parse_args()
    return args
