import csv
import random
from datetime import date, timedelta
from pathlib import Path

# Semilla fija: siempre genera los mismos datos (reproducibilidad)
random.seed(42)

TOTAL_ROWS = 300
OUTPUT_FILE = Path("data/raw/sales.csv")

COLUMNS = [
    "order_id", "order_date", "customer_id", "customer_name", "customer_email",
    "province", "product_id", "product_name", "category", "quantity",
    "unit_price", "status",
]

CUSTOMERS = [
    {"id": "C001", "name": "Ana Gómez", "email": "ana.gomez@example.com", "province": "Santiago del Estero"},
    {"id": "C002", "name": "Juan Pérez", "email": "juan.perez@example.com", "province": "Tucumán"},
    {"id": "C003", "name": "Lucía Fernández", "email": "lucia.fernandez@example.com", "province": "Salta"},
    {"id": "C004", "name": "Martín López", "email": "martin.lopez@example.com", "province": "Córdoba"},
    {"id": "C005", "name": "Sofía Rodríguez", "email": "sofia.rodriguez@example.com", "province": "Buenos Aires"},
    {"id": "C006", "name": "Diego Torres", "email": "diego.torres@example.com", "province": "Santa Fe"},
    {"id": "C007", "name": "Valentina Díaz", "email": "valentina.diaz@example.com", "province": "Mendoza"},
    {"id": "C008", "name": "Nicolás Ruiz", "email": "nicolas.ruiz@example.com", "province": "Jujuy"},
]

PRODUCTS = [
    {"id": "P001", "name": "Teclado mecánico", "category": "Accesorios", "price": 45000.00},
    {"id": "P002", "name": "Mouse inalámbrico", "category": "Accesorios", "price": 18500.00},
    {"id": "P003", "name": "Monitor 24 pulgadas", "category": "Monitores", "price": 210000.00},
    {"id": "P004", "name": "Notebook 15 pulgadas", "category": "Computación", "price": 950000.00},
    {"id": "P005", "name": "Auriculares", "category": "Audio", "price": 62000.00},
    {"id": "P006", "name": "Disco SSD 1TB", "category": "Almacenamiento", "price": 98000.00},
    {"id": "P007", "name": "Memoria RAM 16GB", "category": "Componentes", "price": 55000.00},
    {"id": "P008", "name": "Webcam HD", "category": "Accesorios", "price": 39000.00},
]

STATUSES = ["completed", "pending", "cancelled"]


def make_row(order_num):
    """Devuelve un diccionario con una fila de venta LIMPIA."""
    customer = random.choice(CUSTOMERS)
    product = random.choice(PRODUCTS)
    dias = random.randint(0, 364)
    fecha = date(2025, 1, 1) + timedelta(days=dias)

    return {
        "order_id": f"ORD-{order_num:05d}",
        "order_date": fecha.isoformat(),
        "customer_id": customer["id"],
        "customer_name": customer["name"],
        "customer_email": customer["email"],
        "province": customer["province"],
        "product_id": product["id"],
        "product_name": product["name"],
        "category": product["category"],
        "quantity": str(random.randint(1, 5)),
        "unit_price": f"{product['price']:.2f}",
        "status": random.choice(STATUSES),
    }


def break_row(row):
    """Le aplica UN error al azar que invalida la fila."""
    error = random.choice([
        "sin_cliente",
        "fecha_invalida",
        "cantidad_negativa",
        "fecha_futura",
        "precio_texto",
        "email_invalido",
        "estado_invalido",
    ])

    if error == "sin_cliente":
        row["customer_id"] = ""
    elif error == "fecha_invalida":
        row["order_date"] = "2025-13-45"
    elif error == "cantidad_negativa":
        row["quantity"] = "-2"
    elif error == "fecha_futura":
        row["order_date"] = "2030-01-01"
    elif error == "precio_texto":
        row["unit_price"] = "abc"
    elif error == "email_invalido":
        row["customer_email"] = "correo-invalido"
    elif error == "estado_invalido":
        row["status"] = "shipped??"

    return row


def dirty_row(row):
    """Ensucia la fila SIN invalidarla: la etapa de transformación la va a limpiar."""
    suciedad = random.choice([
        "nombre_mayusculas",
        "email_mayusculas",
        "categoria_minusculas",
        "estado_mayusculas",
    ])

    if suciedad == "nombre_mayusculas":
        row["customer_name"] = "  " + row["customer_name"].upper() + "  "
    elif suciedad == "email_mayusculas":
        row["customer_email"] = row["customer_email"].upper()
    elif suciedad == "categoria_minusculas":
        row["category"] = row["category"].lower()
    elif suciedad == "estado_mayusculas":
        row["status"] = row["status"].upper()

    return row


def main():
    rows = []
    order_num = 1

    while len(rows) < TOTAL_ROWS:
        row = make_row(order_num)
        order_num += 1

        dado = random.random()  
        if dado < 0.06:          
            row = break_row(row)
        elif dado < 0.16:        
            row = dirty_row(row)

        rows.append(row)

       
        if random.random() < 0.02 and len(rows) < TOTAL_ROWS:
            rows.append(dict(row))

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Listo: {len(rows)} filas guardadas en {OUTPUT_FILE}")


if __name__ == "__main__":
    main()