
import pandas as pd
from HomoOP import HomoOP
      

# =================================================================
# Fase 1 - Creacion DataFrame original
# =================================================================
X=pd.DataFrame([['A',100],['A',200],['B',300],['C',100],['C',100]])
X.columns=['Categoria','Secreto']
print(X)
X.to_csv("D:\\PycharmProjects\\testHomo\\fase1_original.csv")

# =================================================================
# Fase 2 - Creacion Contexto y creacion DF codificado
# =================================================================
hop=HomoOP()
hop.create_context()
hop.write_context("D:\\PycharmProjects\\testHomo")

X_codificado=hop.codificaPD(X, "Secreto")
print(X_codificado)
hop.serializaPD(X_codificado,"D:\\PycharmProjects\\testHomo\\fase2_codificado.csv")

# =================================================================
# Fase 3 - Agregaciones con DataFrame codificado
# =================================================================
hop=HomoOP()
hop.read_private_context("D:\\PycharmProjects\\testHomo")
X_codificado=hop.deserializaPD("D:\\PycharmProjects\\testHomo\\fase2_codificado.csv",['Secreto'])
print(X_codificado)
agr=hop.sumariza(X_codificado,'Categoria','Secreto')
print(agr)
hop.serializaPD(agr,"D:\\PycharmProjects\\testHomo\\fase3_codificado_agregado.csv")

# =================================================================
# Fase 4 - Decodificar DataFrame agregado
# =================================================================
hop=HomoOP()
hop.read_private_context("D:\\PycharmProjects\\testHomo")
agr=hop.deserializaPD("D:\\PycharmProjects\\testHomo\\fase3_codificado_agregado.csv",['Secreto'])
X_decode_agr=hop.decodificaPD(agr, "Secreto")
print(X_decode_agr)




