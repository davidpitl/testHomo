#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 17 12:41:02 2022

@author: ricardo
"""


from bfv.batch_encoder import BatchEncoder
from bfv.int_encoder import IntegerEncoder
from bfv.bfv_decryptor import BFVDecryptor
from bfv.bfv_encryptor import BFVEncryptor
from bfv.bfv_evaluator import BFVEvaluator
from bfv.bfv_key_generator import BFVKeyGenerator
from bfv.bfv_parameters import BFVParameters
from util.public_key import PublicKey
from util.secret_key import SecretKey
from util.polynomial import Polynomial
from util.ciphertext import Ciphertext
import util.number_theory as nbtheory
import numpy as np
import random
import sys
import math
from time import time
import math
import json
import os
import pandas as pd

class HomoOP:
    
    def __init__(self):
        self.BASE=16
        self.degree =16     
        plain_modulus = 2199023519041 #4398046061473 #536870849 #2199023519041 
        ciph_modulus =1 << 1000
        
    def create_context(self):
        print("Inicializando contexto...",end="")
        self.degree =16     
        plain_modulus = 4398046061473 #536870849 #2199023519041 
        ciph_modulus =1 << 1000
        self.params = BFVParameters(poly_degree=self.degree,plain_modulus=plain_modulus,ciph_modulus=ciph_modulus)
        
        self.key_generator = BFVKeyGenerator(self.params)
        self.public_key = self.key_generator.public_key
        self.secret_key = self.key_generator.secret_key
        #self.relin_key = self.key_generator.relin_key
        
        #self.encoder = BatchEncoder(self.params)
        self.encoder = IntegerEncoder(self.params,self.BASE)
        self.encryptor = BFVEncryptor(self.params, self.public_key)
        self.decryptor = BFVDecryptor(self.params, self.secret_key)        
        self.evaluator = BFVEvaluator(self.params)
        print(" OK")
    
    def read_private_context(self,ruta):
        print(f"Leyendo parametros desde {ruta}/private.txt")
        with open(ruta+os.sep+"private.txt", 'r') as f:
             data = json.load(f)
        self.params=BFVParameters.from_dict(data['params']) 
        self.secret_key=SecretKey.deserializa(data['secret_key'])
        self.public_key=PublicKey.deserializa(data['public_key'])
        #self.encoder = BatchEncoder(self.params)
        self.encoder = IntegerEncoder(self.params,self.BASE)
        self.encryptor = BFVEncryptor(self.params, self.public_key)
        self.decryptor = BFVDecryptor(self.params, self.secret_key)        
        self.evaluator = BFVEvaluator(self.params)
    
    def read_public_context(self,ruta):
        print(f"Leyendo parametros desde {ruta}/public.txt")
        with open(ruta+os.sep+"public.txt", 'r') as f:
             data = json.load(f)
        self.params=BFVParameters.from_dict(data['params'])  
        self.evaluator = BFVEvaluator(self.params)
      
        
    def encripta(self,v):
        #print(v,self.encoder.encode(v))
        return self.encryptor.encrypt(self.encoder.encode(v))
        m=[]
        x=[0]*self.degree
        for i in v:
            x[0]=i
            m.extend(x)
        return self.encriptaOLD(m)
                    
    def encriptaOLD(self,v):
        l=len(v)
        if l%self.degree!=0:
            f=self.degree-l%self.degree
            #v.extend([0]*f)
            for z in range(0,f):
                v.append(z)
        bloques=len(v)//self.degree
        r=[]
        for b in range(0,bloques):
            bloque=v[b*self.degree:(b+1)*self.degree]
            #print(bloque)
            be=self.encryptor.encrypt(self.encoder.encode(bloque))
            r.append(be)
        return r
    
    def desencripta(self,v):   
        r=[]
        if type(v)==list:
            for bloque in v:
                r.append(self.encoder.decode(self.decryptor.decrypt(bloque)))
            return r
        else:
             return self.encoder.decode(self.decryptor.decrypt(v))[0]
            
        
        # r=[]
        # for bloque in v:
        #     r.append(self.encoder.decode(self.decryptor.decrypt(bloque))[0])
        # return r
    
    def enc_acum(self,v):
        v=list(v)
        r=v[0]
        for i in range(1,len(v)):
            r = self.evaluator.add(r, v[i])
        return r
    
    
        while len(v)>1:
            r=[]
            #if len(v)%2!=0:
            #print("xxxxxxxxxxxxxxxxxxxxxxxxx",len(v))
            for i in range(0,len(v)-1,2):
                r.append(self.evaluator.add(v[i], v[i+1]))
            v=r
        #print("final")
        return v[0]
        
        
        r=v[0]
        #o=v[0]
        
        #print(len(v))
               
        #for i in range(1,len(v)):
        for i in range(1,30):
            r = self.evaluator.add(r, v[i])
            # for z in range(1,self.degree):
            #     r.c0.coeffs[z]=o.c0.coeffs[z]
            #     r.c1.coeffs[z]=o.c1.coeffs[z]
            
        return r

    
    def write_context(self,ruta):
        print(f"Salvando parametros a {ruta}/private.txt y public.txt")
        d={}
        d['params']=self.params.to_dict()
        with open(ruta+os.sep+"public.txt", 'w') as fich:
             fich.write(json.dumps(d, sort_keys=True))
        
        d['secret_key']=str(self.secret_key)     
        d['public_key']=str(self.public_key)
        with open(ruta+os.sep+"private.txt", 'w') as fich:
             fich.write(json.dumps(d, sort_keys=True))

    def codificaPD(self,pd,field):
        pd=pd.copy()
        #pd[field]=pd[field].apply(lambda x:self.encripta([x])[0])
        pd[field]=pd[field].apply(lambda x:self.encripta(x))
        return pd
    
    def decodificaPD(self,pd,field):
        pd=pd.copy()
        pd[field]=pd[field].apply(lambda x:self.desencripta([x])[0])
        return pd
    
    def sumariza(self,df,fields,field):
        agr=df.groupby(by=fields)[field].apply(lambda serie:self.enc_acum(serie))
        df=pd.DataFrame(agr)
        df.reset_index(inplace=True)
        return df
    
    def serializaPD(self,df,fichero):
        df=df.copy()
        df.reset_index(inplace=True,drop=True)
        df.to_csv(fichero,index=False)
        
    def deserializaPD(self,fichero,fields):
        df=pd.read_csv(fichero)
        for f in fields:
            df[f]=df[f].apply(lambda x:Ciphertext(s=x))
        return df