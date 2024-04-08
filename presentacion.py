
import pandas as pd
from HomoOP import HomoOP
      
#%%
# =================================================================
# Fase 1 - Creacion DataFrame original
# =================================================================
print("""=================================================================\nCreacion DataFrame de ejemplo\n=================================================================""")
X=pd.DataFrame([['A',100],['A',200],['B',300],['C',100],['C',100]])
X.columns=['Categoria','Secreto']
print(X)
X.reset_index(inplace=True,drop=True)
X.to_csv("fase1_original.csv",index=False)


# =================================================================
# Fase 2 - Creacion Contexto y creacion DF codificado
# =================================================================

#%%
print("""\n=================================================================\nCreacion Contexto\n=================================================================""")
hop=HomoOP()
hop.create_context()
hop.write_context("./")


#%%
print("""\n=================================================================\nCreacion DataFrame codificado\n=================================================================""")
X_codificado=hop.codificaPD(X, "Secreto")
print(X_codificado)
hop.serializaPD(X_codificado,"fase2_codificado.csv")



#%%
# =================================================================
# Fase 3 - Agregaciones con DataFrame codificado
# =================================================================
print("""\n=================================================================\nOperando sobre DataFrame codificado\n=================================================================""")
hop=HomoOP()
hop.read_public_context("./")
X_codificado=hop.deserializaPD("fase2_codificado.csv",['Secreto'])
print(X_codificado)
agr=hop.sumariza(X_codificado,'Categoria','Secreto')
print(agr)
hop.serializaPD(agr,"fase3_codificado_agregado.csv")



#%%
# =================================================================
# Fase 4 - Decodificar DataFrame agregado
# =================================================================
print("""\n=================================================================\nDecodifica el DataFrame resultado\n=================================================================""")
hop=HomoOP()
hop.read_private_context("./")
agr=hop.deserializaPD("fase3_codificado_agregado.csv",['Secreto'])
X_decode_agr=hop.decodificaPD(agr, "Secreto")
print(X_decode_agr)


