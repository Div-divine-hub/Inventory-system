from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import mysql.connector


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


# Connect to XAMPP MySQL
ds = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Use your MySQL password if any
    database="inventory_data"
)
cursor = ds.cursor(dictionary=True)

@app.route('/')
def index():
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add_item():
    data = (
        request.form['name'],
        request.form['category'],
        request.form['quantity'],
        request.form['price'],
        request.form['location']
    )
    cursor.execute(
        "INSERT INTO items (name, category, quantity, unit_price, location) VALUES (%s, %s, %s, %s, %s)", data)
    ds.commit()  # Use ds.commit() instead of db.commit()
    return redirect(url_for('index'))


@app.route('/edit/<int:id>')
def edit_item(id):
    cursor.execute("SELECT * FROM items WHERE id = %s", (id,))
    item = cursor.fetchone()
    return render_template('update.html', item=item)

@app.route('/update/<int:id>', methods=['POST'])
def update_item(id):
    data = (
        request.form['name'],
        request.form['category'],
        request.form['quantity'],
        request.form['price'],
        request.form['location'],
        id
    )
    cursor.execute("""
        UPDATE items SET name=%s, category=%s, quantity=%s,
        unit_price=%s, location=%s WHERE id=%s
    """, data)
    db.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_item(id):
    cursor.execute("DELETE FROM items WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)