# CQRS-example
Example of a product inventory system using CQRS for the subject of software development III

## Estructura del ejemplo

```
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
```

