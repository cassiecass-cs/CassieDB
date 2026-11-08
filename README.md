# CassieDB
Mini base de datos en Python para guardar objetos por ID en un archivo JSON legible. Sin dependencias, escritura segura y API simple. Proyecto educativo para prototipos y scripts pequeños.
# CassieDB

Mini base de datos en Python para guardar objetos por identificador en un archivo JSON legible.
Sin dependencias, con escritura segura y una API pequeña. **Proyecto educativo** pensado para
prototipos, scripts y proyectos pequeños.

- **Versión:** 1.0
- **Autora:** Cassie Cass
- **Licencia:** MIT

---

## Características

- Cada objeto tiene un **identificador único** y propiedades clave-valor.
- Todo se guarda en un único archivo JSON que puedes abrir y revisar con cualquier editor.
- **Escritura segura:** se escribe primero en un archivo temporal y luego se reemplaza el original, para no corromper los datos si algo falla a mitad del guardado.
- Si el archivo está dañado, se muestra el error en lugar de sobrescribir los datos en silencio.
- Solo usa la biblioteca estándar de Python (`json` y `os`).

## Requisitos

- Python 3.6 o superior

## Instalación

CassieDB es un solo archivo. Copia `cassiedb.py` a tu proyecto, o clona el repositorio:

```bash
git clone https://github.com/TU_USUARIO/CassieDB.git
```

> Reemplaza `TU_USUARIO` por tu usuario de GitHub.

## Uso rápido

```python
from cassiedb import GestorObjetosSimple, Objeto

gestor = GestorObjetosSimple()

# 1. Crear y guardar un objeto
estudiante = Objeto("ES_001", "Cassie Cass")
print(gestor.nuevoObjeto(estudiante))             # Guardado exitosamente

# 2. Leer el objeto completo
print(gestor.lecturaCompleta("ES_001"))
# {'identificador': 'ES_001', 'nombre': 'Cassie Cass'}

# 3. Agregar o modificar propiedades
print(gestor.manejarObjeto("ES_001", "Edad", 20))
print(gestor.manejarObjeto("ES_001", "correo", "ejemplo@cass.com"))

# 4. Leer una sola propiedad
print(gestor.lecturaPorLLave("ES_001", "correo"))  # ejemplo@cass.com
```

Al ejecutarlo se crea el archivo `lite.cassiedb` en la carpeta actual, con este contenido:

```json
{
  "ES_001": {
    "identificador": "ES_001",
    "nombre": "Cassie Cass",
    "Edad": 20,
    "correo": "ejemplo@cass.com"
  }
}
```

También puedes correr el ejemplo incluido:

```bash
python cassiedb.py
```

## Referencia de la API

### `GestorObjetosSimple` (interfaz principal)

| Método | Qué hace | Devuelve |
|---|---|---|
| `nuevoObjeto(objeto)` | Guarda un objeto. Si ya existe uno con el mismo id, lo sobrescribe. | `"Guardado exitosamente"` |
| `lecturaCompleta(id)` | Devuelve todas las propiedades de un objeto. | Diccionario, o `"Objeto no encontrado"` |
| `lecturaPorLLave(id, llave)` | Devuelve el valor de una sola propiedad. | El valor, `"Llave no encontrada"` u `"Objeto no encontrado"` |
| `manejarObjeto(id, llave, valor)` | Agrega o modifica una propiedad de un objeto ya guardado. | `"Actualizado exitosamente"` o `"Objeto no encontrado"` |

### `Objeto`

| Método | Qué hace |
|---|---|
| `Objeto(identificador, nombre)` | Crea un objeto en memoria con esos dos campos. |
| `lectura()` | Devuelve el diccionario con sus propiedades. |
| `escritura(identificador, key, valor)` | Modifica una propiedad **solo en memoria** (el parámetro `identificador` está reservado y no se usa). Para guardar en disco usa `nuevoObjeto`. |

### `DB` (capa de persistencia)

Si quieres elegir el archivo de datos, usa `DB` directamente:

```python
from cassiedb import DB, Objeto

db = DB("mis_datos.cassiedb")
db.nuevo(Objeto("A1", "Ejemplo"))
print(db.obtenerTodo("A1"))
```

## Cosas que conviene saber

- Los identificadores se guardan como **texto**: `1` y `"1"` son el mismo objeto.
- Los valores deben poder convertirse a JSON (texto, números, booleanos, listas y diccionarios).
- `GestorObjetosSimple` usa siempre el archivo por defecto `lite.cassiedb`.
- Los errores de "no encontrado" se devuelven como texto, no como excepciones.

## Limitaciones

CassieDB carga y reescribe el archivo completo en cada operación, por eso:

- Está pensada para pocos datos (cientos o algunos miles de objetos pequeños).
- **No es segura para varios procesos escribiendo al mismo tiempo.**
- No tiene búsquedas por valor, filtros ni relaciones: solo acceso por id y por llave.
- Los datos se guardan en texto plano, sin cifrado.

Para proyectos más grandes, considera una base de datos completa como SQLite.

## Estudiar el código

El código está documentado con docstrings en español. Una buena forma de recorrerlo:

1. `Objeto`: cómo se representa un registro.
2. `DB`: cómo se lee y se guarda el JSON (`_cargar` y `_guardar`).
3. `LecturaDB` y `EscrituraDB`: la separación entre lectura y escritura.
4. `GestorObjetosSimple`: la interfaz que une todo.

## Aclaraciones

- CassieDB **no tiene relación** con Apache Cassandra ni con Amazon DynamoDB; solo comparten la idea general de guardar datos por clave.
- El proyecto no está afiliado a ninguna otra marca o producto.

## Créditos

Diseñado y escrito por **Cassie Cass**. Se utilizaron herramientas de inteligencia artificial como apoyo en algunas partes del proyecto.

## Licencia

Distribuido bajo la licencia [MIT](LICENSE). Consulta el archivo `LICENSE` para más detalles.
