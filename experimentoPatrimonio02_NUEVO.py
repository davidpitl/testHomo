
import pandas as pd
from HomoOP import HomoOP
import sys

# =================================================================
# Fase 1 - Lectura DataFrame original
# =================================================================
X=pd.read_csv("D:\\PycharmProjects\\testHomo\\Patri2019_D.txt",delimiter="&",usecols=[0,1,2,5])
X.columns=['NIU','CCAA','SEXO','IMPORTE']
X['IMPORTE']=X['IMPORTE']//1000
print(X.head(3))
print(X.info())
print(X.groupby(by='CCAA')['IMPORTE'].sum())


# =================================================================
# Fase 2 - Creacion Contexto y creacion DF codificado
# =================================================================
hop=HomoOP()
hop.create_context()
hop.write_context("D:\\PycharmProjects\\testHomo")

X_codificado=hop.codificaPD(X, "IMPORTE")
print(X_codificado)
hop.serializaPD(X_codificado,"D:\\PycharmProjects\\testHomo\\patri_fase2_codificado.csv")

# =================================================================
# Fase 3 - Agregaciones con DataFrame codificado
# =================================================================
hop=HomoOP()
hop.read_private_context("D:\\PycharmProjects\\testHomo")
X_codificado=hop.deserializaPD("D:\\PycharmProjects\\testHomo\\patri_fase2_codificado.csv",['IMPORTE'])
print(X_codificado)
agr=hop.sumariza(X_codificado,'CCAA','IMPORTE')
print(agr)
hop.serializaPD(agr,"D:\\PycharmProjects\\testHomo\\patri_fase3_codificado_agregado.csv")

# =================================================================
# Fase 4 - Decodificar DataFrame agregado
# =================================================================
hop=HomoOP()
hop.read_private_context("D:\\PycharmProjects\\testHomo")
agr=hop.deserializaPD("D:\\PycharmProjects\\testHomo\\patri_fase3_codificado_agregado.csv",['IMPORTE'])
X_decode_agr=hop.decodificaPD(agr, "IMPORTE")
print(X_decode_agr)


