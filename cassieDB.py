"""
CassieDB - Almacenamiento simple de objetos por identificador en un archivo JSON.

Autor:    Cassie Cass
Versión:  1.0
Licencia: MIT

Copyright (c) 2026 Cassie Cass

Se concede permiso, libre de cargos, a cualquier persona que obtenga una copia
de este software y de los archivos de documentación asociados (el "Software"),
para utilizar el Software sin restricción, incluyendo sin limitación los
derechos de usar, copiar, modificar, fusionar, publicar, distribuir,
sublicenciar y/o vender copias del Software, y para permitir a las personas a
quienes se les proporcione el Software hacer lo mismo, sujeto a las siguientes
condiciones:

El aviso de copyright anterior y este aviso de permiso se incluirán en todas
las copias o partes sustanciales del Software.

EL SOFTWARE SE PROPORCIONA "TAL CUAL", SIN GARANTÍA DE NINGÚN TIPO, EXPRESA O
IMPLÍCITA, INCLUYENDO PERO NO LIMITADO A GARANTÍAS DE COMERCIALIZACIÓN,
IDONEIDAD PARA UN PROPÓSITO PARTICULAR Y NO INFRACCIÓN. EN NINGÚN CASO LOS
AUTORES O TITULARES DEL COPYRIGHT SERÁN RESPONSABLES DE NINGUNA RECLAMACIÓN,
DAÑOS U OTRAS RESPONSABILIDADES, YA SEA EN UNA ACCIÓN DE CONTRATO, AGRAVIO O
DE OTRO MODO, QUE SURJA DE, FUERA DE O EN CONEXIÓN CON EL SOFTWARE O EL USO U
OTRO TIPO DE ACCIONES EN EL SOFTWARE.

Descripción
-----------
Cada objeto tiene un identificador único y un conjunto de propiedades
(clave-valor). Todos los objetos se guardan en un único archivo JSON legible,
y la escritura es segura: se usa un archivo temporal que reemplaza al
original solo cuando el guardado terminó correctamente.

Limitaciones
------------
Cada operación carga y reescribe el archivo completo, por lo que está pensado
para scripts, prototipos, configuraciones y proyectos pequeños. No es seguro
para varios procesos escribiendo al mismo tiempo.

Ejemplo de uso
--------------
    gestor = GestorObjetosSimple()
    estudiante = Objeto("ES_001", "Cassie Cass")
    gestor.nuevoObjeto(estudiante)
    gestor.manejarObjeto("ES_001", "correo", "ejemplo@cass.com")
    print(gestor.lecturaPorLLave("ES_001", "correo"))
"""

import json
import os

__author__ = "Cassie Cass"
__version__ = "1.0"
__license__ = "MIT"


class Objeto:
    """Representa un objeto que se puede guardar en la base de datos.

    Internamente guarda sus propiedades en el diccionario ``data``, que
    siempre incluye las claves ``identificador`` y ``nombre``.
    """

    def __init__(self, identificador, nombre):
        """Crea un objeto nuevo.

        Args:
            identificador: Identificador único del objeto (ej. "ES_001").
            nombre: Nombre descriptivo del objeto.
        """
        self.data = {}

        self.data["identificador"] = identificador
        self.data["nombre"] = nombre

    def lectura(self):
        """Devuelve el diccionario completo con las propiedades del objeto."""
        return self.data

    def escritura(self, identificador, key, valor):
        """Agrega o modifica una propiedad del objeto en memoria.

        Args:
            identificador: Parámetro reservado por compatibilidad; no se
                utiliza en esta versión.
            key: Nombre de la propiedad.
            valor: Valor que se asignará a la propiedad.

        Nota:
            El cambio solo afecta al objeto en memoria. Para guardarlo en
            disco se debe usar ``nuevoObjeto`` o ``manejarObjeto``.
        """
        self.data[key] = valor


class DB:
    """Capa de persistencia: lee y escribe el archivo JSON.

    Attributes:
        archivo: Ruta del archivo donde se guardan los datos.
    """

    def __init__(self, archivo="lite.cassiedb"):
        """Abre la base de datos, creando el archivo si no existe.

        Args:
            archivo: Ruta del archivo de datos (por defecto "lite.cassiedb").
        """
        self.archivo = archivo
        if not os.path.exists(archivo):
            self._guardar({})

    def _cargar(self):
        """Lee el archivo y devuelve todos los datos como diccionario.

        Raises:
            json.JSONDecodeError: Si el archivo está corrupto. Se propaga el
                error a propósito para no sobrescribir datos por accidente.
        """
        with open(self.archivo, "r", encoding="utf-8") as f:
            return json.load(f)

    def _guardar(self, data):
        """Guarda el diccionario completo de forma segura (escritura atómica).

        Escribe primero en un archivo temporal y luego lo reemplaza con
        ``os.replace``, de modo que un fallo a mitad del guardado no
        corrompe el archivo original.
        """
        tmp = self.archivo + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp, self.archivo)

    def nuevo(self, objeto):
        """Guarda un objeto. Si ya existe uno con el mismo id, lo sobrescribe.

        Args:
            objeto: Instancia de ``Objeto`` a guardar.

        Returns:
            Mensaje de confirmación.
        """
        data = self._cargar()
        data[str(objeto.data["identificador"])] = objeto.lectura()
        self._guardar(data)
        return "Guardado exitosamente"

    def actualizar(self, id, llave, valor):
        """Agrega o modifica una propiedad de un objeto ya guardado.

        Args:
            id: Identificador del objeto.
            llave: Nombre de la propiedad.
            valor: Nuevo valor de la propiedad.

        Returns:
            "Actualizado exitosamente" o "Objeto no encontrado".
        """
        data = self._cargar()
        id_str = str(id)
        if id_str not in data:
            return "Objeto no encontrado"
        data[id_str][llave] = valor
        self._guardar(data)
        return "Actualizado exitosamente"

    def obtenerTodo(self, id):
        """Devuelve todas las propiedades de un objeto.

        Args:
            id: Identificador del objeto.

        Returns:
            Diccionario con el objeto, o "Objeto no encontrado".
        """
        return self._cargar().get(str(id), "Objeto no encontrado")

    def query(self, id, llave):
        """Devuelve el valor de una sola propiedad de un objeto.

        Args:
            id: Identificador del objeto.
            llave: Nombre de la propiedad a consultar.

        Returns:
            El valor, "Llave no encontrada" u "Objeto no encontrado".
        """
        data = self._cargar()
        id_str = str(id)
        if id_str not in data:
            return "Objeto no encontrado"
        return data[id_str].get(llave, "Llave no encontrada")


class LecturaDB:
    """Operaciones de solo lectura sobre la base de datos."""

    def __init__(self):
        pass

    def lecturaCompleta(self, id):
        """Devuelve el objeto completo con el identificador dado."""
        return DB().obtenerTodo(id)

    def lecturaPorLLave(self, id, llave: str):
        """Devuelve una propiedad específica del objeto con el id dado."""
        return DB().query(id, llave)


class EscrituraDB:
    """Operaciones de escritura sobre la base de datos."""

    def __init__(self):
        pass

    def nuevoObjeto(self, objeto: Objeto):
        """Guarda un objeto nuevo (o sobrescribe uno con el mismo id)."""
        return DB().nuevo(objeto)

    def manejarObjeto(self, id, llave: str, valor):
        """Agrega o modifica una propiedad de un objeto existente."""
        return DB().actualizar(id, llave, valor)


class GestorObjetosSimple:
    """Interfaz principal de la librería.

    Combina lectura y escritura en un solo punto de acceso, de modo que
    basta con crear un gestor para trabajar con la base de datos.
    """

    def __init__(self):
        self.lector = LecturaDB()
        self.escritor = EscrituraDB()

    def lecturaCompleta(self, id):
        """Devuelve el objeto completo con el identificador dado."""
        return self.lector.lecturaCompleta(id)

    def lecturaPorLLave(self, id, llave: str):
        """Devuelve una propiedad específica del objeto con el id dado."""
        return self.lector.lecturaPorLLave(id, llave)

    def nuevoObjeto(self, objeto: Objeto):
        """Guarda un objeto nuevo en la base de datos."""
        return self.escritor.nuevoObjeto(objeto)

    def manejarObjeto(self, id, llave: str, valor):
        """Agrega o modifica una propiedad de un objeto existente."""
        return self.escritor.manejarObjeto(id, llave, valor)


if __name__ == "__main__":

    gestor = GestorObjetosSimple()

    print("Creacion de el primer objeto de la base de datos")

    estudiante = Objeto("ES_001", "Cassie Cass")
    print(gestor.nuevoObjeto(estudiante))

    print("Lectura completa del objeto creado")
    print(gestor.lecturaCompleta("ES_001"))

    print("Actualizar propiedades del objeto")
    print(gestor.manejarObjeto("ES_001", "Edad", 20))
    print(gestor.manejarObjeto("ES_001", "correo", "ejemplo@cass.com"))

    print("Leemos un atributo individual de nuestro estudiante")
    print(gestor.lecturaPorLLave("ES_001", "correo"))
