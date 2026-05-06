# CQRS-example
Example of a product inventory system using CQRS for the subject of software development III

Estructura del ejemplo
cqrs_example.py
│
├── Modelos
│   └── Producto                  ← entidad de dominio
│
├── Base de datos simulada
│   ├── write_db                  ← BD de escritura (Commands)
│   └── read_db                   ← BD de lectura optimizada (Queries)
│
├── COMMANDS (solo escriben)
│   ├── AgregarProductoCommand
│   ├── ActualizarStockCommand
│   └── EliminarProductoCommand
│
├── CommandHandler                ← ejecuta los Commands
│
├── QUERIES (solo leen)
│   ├── ObtenerProductoQuery
│   ├── ListarProductosQuery
│   └── BuscarPorNombreQuery
│
└── QueryHandler                  ← ejecuta las Queries

Separación total: CommandHandler y QueryHandler son clases distintas que nunca se mezclan.
Commands no retornan datos: solo ejecutan la acción y sincronizan la vista de lectura.
Dos "bases de datos": write_db guarda los objetos de dominio; read_db guarda vistas desnormalizadas (con campos calculados como subtotal). Esto es lo que hace a CQRS escalable en sistemas reales.
Proyección (_sincronizar_read_db): después de cada Command, actualizamos la vista de lectura. En sistemas reales esto se hace con eventos asincrónicos.

