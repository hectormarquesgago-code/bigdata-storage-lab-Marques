# Diccionario de Datos - Esquema Canónico

Este laboratorio utiliza un **esquema canónico** para estandarizar la información proveniente de CSVs heterogéneos.  
Los campos normalizados son los siguientes:

| Campo   | Tipo       | Descripción                                      | Formato / Unidad      |
|---------|-----------|--------------------------------------------------|-----------------------|
| date    | `date`    | Fecha del registro                               | `YYYY-MM-DD`          |
| partner | `string`  | Nombre o identificador del socio/proveedor/actor | Texto libre            |
| amount  | `float`   | Valor monetario asociado a la transacción        | Euros (`EUR`)          |

---

## Mapeos de Origen → Canónico

Ejemplos de cómo diferentes archivos fuente pueden ser normalizados al esquema estándar:

| Archivo origen | Campo origen     | Campo canónico | Transformación aplicada                       |
|----------------|------------------|----------------|-----------------------------------------------|
| ventas_2023.csv | `fecha`         | `date`         | Convertir formato `DD/MM/YYYY` → `YYYY-MM-DD` |
| pagos.xls       | `Proveedor`     | `partner`      | Normalizar mayúsculas/minúsculas              |
| transacciones.csv | `importe`     | `amount`       | Convertir de string a float                   |
| movimientos.csv  | `partner_id`   | `partner`      | Mapear ID a nombre de socio                   |
| facturas.csv     | `monto_total`  | `amount`       | Convertir moneda USD → EUR (factor fx)        |
| registros.csv    | `created_at`   | `date`         | Extraer solo la fecha de un timestamp         |

> 🔑 **Nota:** El diccionario debe ampliarse a medida que aparezcan nuevos datasets de entrada.

