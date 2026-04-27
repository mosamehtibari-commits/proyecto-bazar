from flask import Flask, render_template_string
import mysql.connector

app = Flask(__name__)

def obtener_datos():
    try:
        db = mysql.connector.connect(
            host="10.0.2.15",
            user="bazar_web_user",
            password="Web_Client_99*",
            database="bazar_premium",
            connect_timeout=5
        )
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        db.close()
        return productos
    except Exception as e:
        return str(e)

@app.route('/')
def index():
    productos = obtener_datos()
    
    if isinstance(productos, str):
        return f"<h2 style='color:red;font-family:sans-serif;text-align:center;'>Error de conexión: {productos}</h2>"

    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Bazar Premium</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #f8f9fa; padding: 40px; }
            .container { max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
            h1 { color: #0d6efd; text-align: center; margin-bottom: 30px; border-bottom: 2px solid #0d6efd; padding-bottom: 10px; }
            table { width: 100%; border-collapse: collapse; }
            th { background-color: #0d6efd; color: white; padding: 12px; text-align: left; }
            td { padding: 12px; border-bottom: 1px solid #dee2e6; color: #333; }
            tr:hover { background-color: #f1f4f9; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Inventario Bazar Premium</h1>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Producto</th>
                        <th>Precio</th>
                        <th>Stock</th>
                    </tr>
                </thead>
                <tbody>
                    {% for p in lista %}
                    <tr>
                        <td>{{ p.id }}</td>
                        <td>{{ p.nombre }}</td>
                        <td>{{ p.precio }} €</td>
                        <td>{{ p.stock }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template, lista=productos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
