import pandas as pd
from helper.helper import Helper
from sparky_bc import Sparky
import os


def punto21 ():
    # Se leen los df
    ruta_Obligaciones = "Excel/obligaciones_clientes.xlsx"
    ruta_Tasa_Productos = "Excel/tasas_productos.xlsx"
    Df_Obligaciones=pd.read_excel(ruta_Obligaciones)
    Df_Tasa_Productos = pd.read_excel(ruta_Tasa_Productos)
    
    #Se eliminan duplicados
    Df_Obligaciones_Sin_Duplicados=Df_Obligaciones.drop_duplicates(["radicado","num_documento","id_producto","valor_inicial","fecha_desembolso"])
    
    #Extraer y asignar nombre de productos
    ultimo_valor = Df_Obligaciones_Sin_Duplicados['id_producto'].str.split('-').str[-1]
    nombre_producto = ultimo_valor.str.split().str[0].copy()  
    Df_Obligaciones_Sin_Duplicados["nombre_producto"] = nombre_producto.str.lower()
    
    DfTasaProductos_completa = pd.merge(Df_Obligaciones_Sin_Duplicados, Df_Tasa_Productos,
                             left_on=["cod_segm_tasa","cod_subsegm_tasa","cal_interna_tasa"],
                             right_on=["cod_segmento","cod_subsegmento","calificacion_riesgos"],
                             how="inner")
    
    #Se asigna la tasa correspondiete a cada producto
    def asignar_tasa(row):
        if row['nombre_producto'] == 'cartera':
            return row['tasa_cartera']
        elif row['nombre_producto'] == 'operacion_especifica':
            return row['tasa_operacion_especifica']
        elif row['nombre_producto'] == 'leasing':
            return row['tasa_leasing']
        elif row['nombre_producto'] == 'sufi':
            return row['tasa_sufi']
        elif row['nombre_producto'] == 'factoring':
            return row['tasa_factoring']
        elif row['nombre_producto'] == 'tarjeta':
            return row['tasa_tarjeta']
        elif row['nombre_producto'] == 'hipotecario':
            return row['tasa_hipotecario']
        else:
            return None
    
    DfTasaProductos_completa['tasa_inicial'] = DfTasaProductos_completa.apply(asignar_tasa, axis=1)

    DfTasaProductos_completa = DfTasaProductos_completa.drop(['cod_segmento','segmento','cod_subsegmento','calificacion_riesgos','tasa_hipotecario','tasa_cartera', 'tasa_operacion_especifica', 'tasa_leasing','tasa_sufi','tasa_factoring','tasa_tarjeta'], axis=1)
    
    return DfTasaProductos_completa


def punto22(Df):
    Df["tasa_efectiva"]=((((1+Df["tasa_inicial"])**
                                          (1/Df["cod_periodicidad"]))-1)*Df["cod_periodicidad"])/Df["cod_periodicidad"]
                        
    return Df
    
def punto23(Df):
    Df["valor_final"]=Df["tasa_efectiva"]*Df["valor_inicial"]
    return Df

def punto24(Df):
    dataFrame = pd.DataFrame(Df)
    resultado_agrupado = dataFrame.groupby('num_documento').agg({'valor_final': 'sum', 'id_producto': 'count'}).reset_index()
    clientes_con_mas_de_dos_productos = resultado_agrupado[resultado_agrupado['id_producto'] >= 2]
    return clientes_con_mas_de_dos_productos


