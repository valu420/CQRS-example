# ============================================================
#  EJEMPLO CQRS - Inventario de Productos
#  Patrón: Command Query Responsibility Segregation
#
#  La idea central:
#    COMMANDS  → cambian el estado (escribir)
#    QUERIES   → leen el estado   (leer)
#  Nunca mezclar ambas responsabilidades en el mismo objeto.
# ============================================================


# ─────────────────────────────────────────────
#  MODELOS
# ─────────────────────────────────────────────

class Producto:
    """Modelo de dominio (fuente de verdad para escritura)."""
    def __init__(self, id: str, nombre: str, cantidad: int, precio: float):
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio


# ─────────────────────────────────────────────
#  BASE DE DATOS SIMULADA
#  En CQRS real se pueden tener dos BDs separadas,
#  una para escritura y otra optimizada para lectura.
#  Aquí lo simplificamos con dos diccionarios.
# ─────────────────────────────────────────────

write_db: dict[str, Producto] = {}   # BD de escritura (Commands)
read_db:  dict[str, dict]    = {}    # BD de lectura  (Queries) — vista desnormalizada


def _sincronizar_read_db(producto: Producto):
    """
    Proyección: después de cada Command, actualizamos
    la vista de lectura. En sistemas reales esto se
    hace con eventos (Event Sourcing) o mensajería.
    """
    read_db[producto.id] = {
        "id":       producto.id,
        "nombre":   producto.nombre,
        "cantidad": producto.cantidad,
        "precio":   producto.precio,
        "subtotal": round(producto.cantidad * producto.precio, 2),  # campo calculado
    }


# ─────────────────────────────────────────────
#  COMMANDS  (solo escriben, no retornan datos)
# ─────────────────────────────────────────────

class AgregarProductoCommand:
    def __init__(self, id: str, nombre: str, cantidad: int, precio: float):
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio


class ActualizarStockCommand:
    def __init__(self, id: str, nueva_cantidad: int):
        self.id = id
        self.nueva_cantidad = nueva_cantidad


class EliminarProductoCommand:
    def __init__(self, id: str):
        self.id = id


# ─────────────────────────────────────────────
#  COMMAND HANDLERS  (ejecutan los Commands)
# ─────────────────────────────────────────────

class CommandHandler:
    """Maneja todos los Commands del sistema."""

    def handle_agregar(self, cmd: AgregarProductoCommand):
        if cmd.id in write_db:
            raise ValueError(f"Producto '{cmd.id}' ya existe.")
        producto = Producto(cmd.id, cmd.nombre, cmd.cantidad, cmd.precio)
        write_db[cmd.id] = producto
        _sincronizar_read_db(producto)
        print(f"[COMMAND] Producto '{cmd.nombre}' agregado.")

    def handle_actualizar_stock(self, cmd: ActualizarStockCommand):
        if cmd.id not in write_db:
            raise ValueError(f"Producto '{cmd.id}' no encontrado.")
        write_db[cmd.id].cantidad = cmd.nueva_cantidad
        _sincronizar_read_db(write_db[cmd.id])
        print(f"[COMMAND] Stock de '{cmd.id}' actualizado a {cmd.nueva_cantidad}.")

    def handle_eliminar(self, cmd: EliminarProductoCommand):
        if cmd.id not in write_db:
            raise ValueError(f"Producto '{cmd.id}' no encontrado.")
        nombre = write_db[cmd.id].nombre
        del write_db[cmd.id]
        del read_db[cmd.id]
        print(f"[COMMAND] Producto '{nombre}' eliminado.")


# ─────────────────────────────────────────────
#  QUERIES  (solo leen, no cambian nada)
# ─────────────────────────────────────────────

class ObtenerProductoQuery:
    def __init__(self, id: str):
        self.id = id


class ListarProductosQuery:
    """Sin parámetros: devuelve todo el inventario."""
    pass


class BuscarPorNombreQuery:
    def __init__(self, texto: str):
        self.texto = texto


# ─────────────────────────────────────────────
#  QUERY HANDLERS  (ejecutan las Queries)
# ─────────────────────────────────────────────

class QueryHandler:
    """Maneja todas las Queries del sistema."""

    def handle_obtener(self, query: ObtenerProductoQuery) -> dict | None:
        resultado = read_db.get(query.id)
        print(f"[QUERY]   Buscando producto '{query.id}'...")
        return resultado

    def handle_listar(self, query: ListarProductosQuery) -> list[dict]:
        print("[QUERY]   Listando todos los productos...")
        return list(read_db.values())

    def handle_buscar_por_nombre(self, query: BuscarPorNombreQuery) -> list[dict]:
        print(f"[QUERY]  Buscando productos con '{query.texto}'...")
        return [
            p for p in read_db.values()
            if query.texto.lower() in p["nombre"].lower()
        ]


# ─────────────────────────────────────────────
#  DEMO
# ─────────────────────────────────────────────

def imprimir(datos):
    if isinstance(datos, list):
        if not datos:
            print("  (sin resultados)")
        for item in datos:
            print(f"  {item}")
    elif datos:
        print(f"  {datos}")
    else:
        print("  (no encontrado)")


def main():
    cmd = CommandHandler()
    qry = QueryHandler()

    print("\n" + "="*55)
    print("  DEMO CQRS — Inventario de Productos")
    print("="*55)

    # ── Commands (escritura) ──────────────────
    print("\n--- Ejecutando Commands (escritura) ---")
    cmd.handle_agregar(AgregarProductoCommand("P01", "Teclado Mecánico", 15, 89900))
    cmd.handle_agregar(AgregarProductoCommand("P02", "Mouse Inalámbrico", 30, 45000))
    cmd.handle_agregar(AgregarProductoCommand("P03", "Monitor 27\"",       8, 650000))
    cmd.handle_actualizar_stock(ActualizarStockCommand("P02", 25))
    cmd.handle_eliminar(EliminarProductoCommand("P03"))

    # ── Queries (lectura) ─────────────────────
    print("\n--- Ejecutando Queries (lectura) ---")

    producto = qry.handle_obtener(ObtenerProductoQuery("P01"))
    imprimir(producto)

    todos = qry.handle_listar(ListarProductosQuery())
    imprimir(todos)

    encontrados = qry.handle_buscar_por_nombre(BuscarPorNombreQuery("mouse"))
    imprimir(encontrados)

    print("\n✔ Fin del demo CQRS\n")


if __name__ == "__main__":
    main()
