--1.1

DROP TABLE IF EXISTS proceso.PtSRM_extraccionTipoProducto;
CREATE TABLE proceso.PtSRM_extraccionTipoProducto STORED AS PARQUET AS
WITH ExtraccionTipoProducto AS (
SELECT DISTINCT t1.radicado,
        t1.num_documento,
        t1.cod_segm_tasa,
        t1.cod_subsegm_tasa,
        t1.cal_interna_tasa,
        t1.id_producto,
        t1.tipo_id_producto,
        t1.valor_inicial,
        t1.fecha_desembolso,
        t1.plazo,
        t1.cod_periodicidad,
        t1.periodicidad,
        t1.saldo_deuda,
        t1.modalidad,
        t1.tipo_plazo,
        LOWER(TRIM(REVERSE(SUBSTRING(reverse(id_producto),1,INSTR(reverse(id_producto),"-")-1)))) AS Tipo_Producto_Extraido --Extraer la ultima parte antes del ultimo - 
FROM proceso.PtSRM_Obligaciones_Clientes AS t1
                            )
SELECT  t3.radicado,
        t3.num_documento,
        t3.cod_segm_tasa,
        t3.cod_subsegm_tasa,
        t3.cal_interna_tasa,
        t3.id_producto,
        t3.tipo_id_producto,
        t3.valor_inicial,
        t3.fecha_desembolso,
        t3.plazo,
        t3.cod_periodicidad,
        t3.periodicidad,
        t3.saldo_deuda,
        t3.modalidad,
        t3.tipo_plazo,
        CASE WHEN t3.Tipo_Producto_Extraido LIKE "% %" THEN SUBSTRING (t3.Tipo_Producto_Extraido,1,INSTR(t3.Tipo_Producto_Extraido," ")-1) --Extraer la                  primera parte del tipo de producto
             ELSE t3.Tipo_Producto_Extraido
        END AS Tipo_Producto_Extraido
FROM ExtraccionTipoProducto AS t3;

COMPUTE STATS proceso.PtSRM_extraccionTipoProducto;

DROP TABLE IF EXISTS proceso.PtSRM_asignarTasaInicial;
CREATE TABLE proceso.PtSRM_asignarTasaInicial STORED AS PARQUET AS
SELECT t1.radicado,
        t1.num_documento,
        t1.cod_segm_tasa,
        t1.cod_subsegm_tasa,
        t1.cal_interna_tasa,
        t1.id_producto,
        t1.tipo_id_producto,
        t1.valor_inicial,
        t1.fecha_desembolso,
        t1.plazo,
        t1.cod_periodicidad,
        t1.periodicidad,
        t1.saldo_deuda,
        t1.modalidad,
        t1.tipo_plazo,
        CASE WHEN t1.Tipo_Producto_Extraido = "cartera" THEN t2.tasa_cartera
             WHEN t1.Tipo_Producto_Extraido = "operacion_especifica" THEN t2.tasa_operacion_especifica
             WHEN t1.Tipo_Producto_Extraido = "hipotecario" THEN t2.tasa_hipotecario
             WHEN t1.Tipo_Producto_Extraido = "leasing" THEN t2.tasa_leasing
             WHEN t1.Tipo_Producto_Extraido = "sufi" THEN t2.tasa_sufi
             WHEN t1.Tipo_Producto_Extraido = "factoring" THEN t2.tasa_factoring
             WHEN t1.Tipo_Producto_Extraido = "tarjeta" THEN tasa_tarjeta
        END AS Tasa_inicial,
        t1.Tipo_Producto_Extraido
FROM proceso.PtSRM_extraccionTipoProducto AS t1
LEFT JOIN proceso.PtSRM_tasa_productos AS t2
ON t1.cod_segm_tasa = t2.cod_segmento AND t1.cod_subsegm_tasa=t2.cod_subsegmento AND t1.cal_interna_tasa = t2.calificacion_riesgos;

COMPUTE STATS proceso.PtSRM_asignarTasaInicial;
--- 1.2

DROP TABLE IF EXISTS proceso.PtSRM_AsignacionTasaEfectiva;
CREATE TABLE proceso.PtSRM_AsignacionTasaEfectiva STORED AS PARQUET AS
SELECT  radicado,
        num_documento,
        cod_segm_tasa,
        cod_subsegm_tasa,
        cal_interna_tasa,
        id_producto,
        tipo_id_producto,
        valor_inicial,
        fecha_desembolso,
        plazo,
        cod_periodicidad,
        periodicidad,
        saldo_deuda,
        modalidad,
        tipo_plazo,
        tasa_inicial,
        (
                (POWER((1+CAST(tasa_inicial AS DOUBLE)),(1 / CAST(cod_periodicidad AS DOUBLE)))-1)
                * CAST(cod_periodicidad AS DOUBLE)
                                                        )
        /CAST(cod_periodicidad AS DOUBLE)
        AS Tasa_Efectiva,
        Tipo_Producto_Extraido
FROM proceso.PtSRM_asignarTasaInicial;

COMPUTE STATS proceso.PtSRM_AsignacionTasaEfectiva;
---1.3

DROP TABLE IF EXISTS proceso.PtSRM_AsignacionValorFinal;
CREATE TABLE proceso.PtSRM_AsignacionValorFinal STORED AS PARQUET AS
SELECT  radicado,
        num_documento,
        cod_segm_tasa,
        cod_subsegm_tasa,
        cal_interna_tasa,
        id_producto,
        tipo_id_producto,
        valor_inicial,
        fecha_desembolso,
        plazo,
        cod_periodicidad,
        periodicidad,
        saldo_deuda,
        modalidad,
        tipo_plazo,
        tasa_inicial,
        Tasa_Efectiva,
        Tasa_Efectiva*valor_inicial AS valor_final,
        Tipo_Producto_Extraido
FROM proceso.PtSRM_AsignacionTasaEfectiva;

COMPUTE STATS proceso.PtSRM_AsignacionValorFinal;


--1.4
DROP TABLE IF EXISTS proceso.PtSRM_SumaValorFinal;
CREATE TABLE proceso.PtSRM_SumaValorFinal STORED AS PARQUET AS 
SELECT  
        num_documento,
        SUM(valor_final) AS suma_ValorFinal ,
        count(id_producto) As Cantidad_Productos
FROM proceso.PtSRM_AsignacionValorFinal
GROUP BY 
        num_documento
HAVING count(id_producto)>1 ;

COMPUTE STATS proceso.PtSRM_SumaValorFinal;








