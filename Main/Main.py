from SegundoPunto import punto21, punto22, punto23, punto24
from config import hp, sp
from TercerPunto import create_app

def ejecutar_primer_punto():
    # Ejecutar el primer punto SQL
    sp.subir_excel("Excel/obligaciones_clientes.xlsx", "PtSRM_Obligaciones_Clientes", "proceso", modo="overwrite")
    hp.ejecutar_consulta("COMPUTE STATS proceso.PtSRM_Obligaciones_Clientes")
    sp.subir_excel(r"Excel/tasas_productos.xlsx", "PtSRM_tasa_productos", "proceso", modo="overwrite")
    hp.ejecutar_consulta("COMPUTE STATS proceso.PtSRM_tasa_productos")
    hp.ejecutar_archivo("Main/PrimerPunto.SQL")
    print("Primer punto SQL ejecutado.")

def generar_excels():
    # Ejecutar el segundo punto y generar los excels
    Dfresultado_punto21 = punto21()
    Dfresultado_punto21.to_csv("ExcelGenerados/resultados_punto21.csv", index=False)
    Dfresultado_punto22 = punto22(Dfresultado_punto21)
    Dfresultado_punto22.to_csv("ExcelGenerados/resultados_punto22.csv", index=False)
    Dfresultado_punto23 = punto23(Dfresultado_punto22)
    Dfresultado_punto23.to_csv("ExcelGenerados/resultados_punto23.csv", index=False)
    Dfresultado_punto24 = punto24(Dfresultado_punto23)
    Dfresultado_punto24.to_csv("ExcelGenerados/resultados_punto24.csv", index=False)
    print('Resultados en la carpeta ExcelGenerados.')

def desplegar_api():
    app = create_app()
    print("API DESPLEGADA. POR FAVOR ABRIR EN SU NAVEGADOR LA DIRECCION http://127.0.0.1:5000")
    app.run(debug=False)

def main_menu():
    print("""-----------------------------------------------------
         -----      Prueba Tecnica -----------
        Seleccione la opción que desea ejecutar:
        1. Para ejecutar el primer punto SQL en la Lz y luego desplegar la API
        2. Para ejecutar el segundo punto y generar los excels
        0. Para salir
        -----------------------------------------------------""")
    
    opcion = input("Ingrese su opción: ")
    return opcion

def main():
    while True:
        opcion = main_menu()
        
        if opcion == '1':
            ejecutar_primer_punto()
            desplegar_api()
            break  
        elif opcion == '2':
            generar_excels()
        elif opcion == '0':
            print("Fin")
            break
        else:
            print("Opción inválida.")

if __name__ == '__main__':
    main()
