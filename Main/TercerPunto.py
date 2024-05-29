from flask import Flask, request, jsonify, render_template
from config import hp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/consultaProductos', methods=['GET'])
def consulta():
    num_documento = request.args.get('num_documento')
    
    if not num_documento:
        return jsonify({'error': 'num_documento es requerido'}), 400
    
    num_documento = str(num_documento)
    
    # Cargar los datos de productos
    df_infoProductos = hp.obtener_dataframe('''SELECT  
                                num_documento,
                                id_producto,
                                tipo_producto_extraido,
                                tipo_id_producto,
                                tasa_efectiva,
                                valor_final
                     FROM proceso.PtSRM_AsignacionValorFinal''')
    
    # Filtrar el DataFrame por el num_documento
    df_filtrado = df_infoProductos[df_infoProductos['num_documento'].astype(str) == num_documento]
    
    if df_filtrado.empty:
        return jsonify({'error': 'No se encontraron registros para el num_documento proporcionado'}), 404
    
    resultado = df_filtrado.to_dict(orient='records')
    
    return jsonify(resultado)

@app.route('/valor_total', methods=['GET'])
def valor_total():
    num_documento = request.args.get('num_documento')
    
    if not num_documento:
        return jsonify({'error': 'num_documento es requerido'}), 400
    
    num_documento = str(num_documento)
    
    # Cargar los datos de productos
    df_valorTotal = hp.obtener_dataframe('''SELECT num_documento, suma_valorfinal AS valor_total 
                                        FROM proceso.PtSRM_SumaValorFinal''')
    
    # Filtrar el DataFrame por el num_documento
    df_filtrado = df_valorTotal[df_valorTotal['num_documento'].astype(str) == num_documento]
    
    if df_filtrado.empty:
        return jsonify({'error': 'No se encontraron registros para el num_documento proporcionado'}), 404
    
    resultado = df_filtrado.to_dict(orient='records')
    
    return jsonify(resultado)

def create_app():
    return app

if __name__ == '__main__':
    app.run(debug=True)
