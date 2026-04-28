from flask import Flask, render_template_string
import pymysql

app = Flask(__name__)

def obtener_datos():
    try:
        db = pymysql.connect(
            host="localhost", 
            user="bazar_web_user", 
            password="Web_Client_99*", 
            database="bazar_premium",
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = db.cursor()
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        db.close()
        return productos
    except Exception as e:
        return str(e)

@app.route('/')
def index():
    productos = obtener_datos()
    
    html_template = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Panel de Control | Bazar Premium</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background-color: #f8f9fa; }
            .navbar { background: #2c3e50; }
            .card { border-radius: 15px; box-shadow: 0 10px 20px rgba(0,0,0,0.05); }
        </style>
    </head>
    <body>
        <nav class="navbar navbar-dark mb-4 p-3">
            <div class="container-fluid"><span class="navbar-brand h1">💎 BAZAR PREMIUM v2.0</span></div>
        </nav>
        <div class="container">
            <div class="card p-4">
                <h2 class="text-primary mb-4">Inventory Management</h2>
                {% if error %}
                    <div class="alert alert-danger">Error: {{ error }}</div>
                {% else %}
                    <table class="table table-hover">
                        <thead><tr><th>Product Name</th><th>Price</th><th>Status</th></tr></thead>
                        <tbody>
                            {% for p in productos %}
                            <tr>
                                <td class="fw-bold">{{ p.nombre }}</td>
                                <td><span class="badge bg-info text-dark">{{ p.precio }} €</span></td>
                                <td><span class="badge bg-success">In Stock</span></td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                {% endif %}
            </div>
        </div>
    </body>
    </html>
    """
    if isinstance(productos, str):
        return render_template_string(html_template, error=productos)
    return render_template_string(html_template, productos=productos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
