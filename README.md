# PADAS - Adopciones Cesde Analytics

Dashboard de análisis de datos para el sistema de adopciones de mascotas.

## Requisitos

- Python 3.10+

## Instalación

1. **Crear entorno virtual** (recomendado):
   ```bash
   python -m venv .venv
   ```

2. **Activar el entorno virtual**:
   - Windows: `.venv\Scripts\activate`
   - Linux/macOS: `source .venv/bin/activate`

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

```bash
streamlit run app.py
```

La aplicación se abrirá en `http://localhost:8501`.

## Configuración

El proyecto viene configurado por defecto para conectarse a:
- **URL base**: `https://pi-deploy-ouni.onrender.com/api`
- **Autenticación**: `admin` / `admin123`

Para modificar estos valores, edita las variables en [app.py](app.py):
```python
USER = "admin"
PASS = "admin123"
BASE_URL = "https://pi-deploy-ouni.onrender.com/api"
```

## Funcionalidades

- **Gestión General**: CRUD de mascotas, adoptantes y solicitudes
- **Dashboard & Estadísticas**: Gráficos y análisis de datos
  - Métricas rápidas
  - Distribución por especie
  - Estado de mascotas
  - Filtros por nombre, tamaño y edad
  - Relación edad vs tamaño