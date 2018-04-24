#!/usr/bin/env python3
# coding=UTF-8

#Syntax kicknock.py POSCAR/CONTCAR 

import sys,os
import numpy as np
import vasp_io as vio


def assign_mode(vibinfo):
    #Show frequecies infomation
    freqs = [line.replace(' f  =', 'f =').replace(' f/i=','i =') for line in vibinfo if 'f' in line]
    for line in freqs:
        print(line)
    mode = input('Please assign a mode e.g 2i: ').strip()
    return mode
         
def assign_multiplier():
    mul = input('Please assign a multiplier [dafalut: 0.15]: ').strip()
    if mul == '':
        mul = 0.15
    else:
        mul=float(mul)
    return mul

def addict(dictarray, purearray):
    pair = zip(dictarray.keys(), dictarray.values())
    start = 0; end = 0
    for key, value in pair:
        num = len(value)
        start, end = end, end + num 
        dictarray[key] = dictarray[key] + purearray[start:end]
    return dictarray
    

#
if len(sys.argv) == 1:
    filename = 'POSCAR'
else:
    filename = sys.argv[1] 
if os.path.exists(filename):
    poscar = vio.Poscar(filename)
    coordinates = poscar.coordinates
else:
    raise IOError('%s file does not exist' %(filename))

if os.path.exists('OUTCAR'):
    vibinfo = vio.extra_vibinfo('OUTCAR')
else:
    raise IOError('OUTCAR file does not exist' %(filename))

mode = assign_mode(vibinfo)
mul = assign_multiplier()
dymatrix = vio.get_dymatrix(vibinfo)
shiftmatrix = mul * np.array(dymatrix[mode])
poscar.coordinates = addict(coordinates, shiftmatrix)  
poscar.write_poscar()
