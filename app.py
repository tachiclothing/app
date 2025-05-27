from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Kết nối database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    return render_template('product.html', product=product)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        image = request.form['image']
        description = request.form['description']

        conn = get_db_connection()
        conn.execute('INSERT INTO products (name, price, image, description) VALUES (?, ?, ?, ?)',
                     (name, price, image, description))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)
