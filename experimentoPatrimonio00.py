
import pandas as pd
from HomoOP import HomoOP
      
base_dir = 'C:\\Users\\chugs\\PycharmProjects\\testHomo'

# =================================================================
# Fase 1 - Creacion DataFrame original
# =================================================================
X=pd.DataFrame([['A',100],['A',200],['B',300],['C',100],['C',100]])
X.columns=['Categoria','Secreto']
print
X.to_csv(base_dir + "\\fase1_original.csv")

# =================================================================
# Fase 2 - Creacion Contexto y creacion DF codificado
# =================================================================
hop=HomoOP()
hop.create_context()
hop.write_context(base_dir)

X_codificado=hop.codificaPD(X, "Secreto")
print(X_codificado)
hop.serializaPD(X_codificado,base_dir + "\\fase2_codificado.csv")

# =================================================================
# Fase 3 - Agregaciones con DataFrame codificado
# =================================================================
hop=HomoOP()
hop.read_private_context(base_dir)
X_codificado=hop.deserializaPD(base_dir + "\\fase2_codificado.csv", ['Secreto'])
print(X_codificado)
agr=hop.sumariza(X_codificado,'Categoria','Secreto')
print(agr)
hop.serializaPD(agr,base_dir + "\\fase3_codificado_agregado.csv")

# =================================================================
# Fase 4 - Decodificar DataFrame agregado
# =================================================================
hop=HomoOP()
hop.read_private_context(base_dir)
agr=hop.deserializaPD(base_dir + "\\fase3_codificado_agregado.csv", ['Secreto'])
X_decode_agr=hop.decodificaPD(agr, "Secreto")
print(X_decode_agr)




