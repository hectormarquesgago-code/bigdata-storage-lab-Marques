# Gobernanza de Datos

Este documento define las políticas mínimas de gobernanza aplicadas en el laboratorio.

---

## 1. Origen y Linaje de Datos
- Todo dataset debe registrarse indicando:
  - Fuente (archivo, API, base de datos).
  - Fecha y responsable de la carga.
- El linaje debe documentar:
  - De dónde proviene cada campo canónico.
  - Qué transformaciones se aplicaron en cada capa (Raw → Bronze → Silver → Gold).

---

## 2. Validaciones Mínimas
- Verificación de formato de fechas (`YYYY-MM-DD`).
- Control de valores nulos en campos críticos (`date`, `partner`, `amount`).
- Eliminación o señalización de duplicados.
- Conversión de tipos de datos:
  - `amount` → float (2 decimales).
  - `date` → date.
- Registro de errores en un log accesible.

---

## 3. Política de Mínimos Privilegios
- Acceso **lectura-escritura** solo para quienes procesan datos en `raw/` y `bronze/`.
- Acceso **solo lectura** para usuarios analíticos en `silver/` y `gold/`.
- Restricciones adicionales:
  - Datos sensibles no deben ser cargados al repositorio.
  - Uso de credenciales debe estar gestionado fuera del código (ej. variables de entorno).

---

## 4. Trazabilidad
- Cada dataset debe tener un identificador único de ingesta.
- Mantener metadatos: fecha de carga, responsable, versión de script.
- Logs de ejecución deben permitir reproducir cada paso.

---

## 5. Roles
- **Data Engineer:** responsable de ingesta, validación y normalización.
- **Data Analyst:** consumo de datos en capas Silver/Gold y diseño de KPIs.
- **Data Steward:** supervisa la gobernanza, asegura cumplimiento de políticas y mantiene el diccionario de datos.

