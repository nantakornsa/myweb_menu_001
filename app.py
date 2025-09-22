import json
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "secret_key"

MENU_FILE = "menu.json"
ADMIN_FILE = "admin.json"

# --- ฟังก์ชันช่วยเหลือ ---
def load_menu():
    try:
        with open(MENU_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_menu(menu_items):
    with open(MENU_FILE, "w", encoding="utf-8") as f:
        json.dump(menu_items, f, ensure_ascii=False, indent=4)

def get_next_id(menu_items):
    return max((item["id"] for item in menu_items), default=0) + 1

def load_admin():
    """โหลดข้อมูล admin จาก admin.json"""
    try:
        with open(ADMIN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"username": "admin", "password": "1234"}  # default

# --- หน้าแรก (ลูกค้า) ---
@app.route("/")
def index():
    sort_by = request.args.get("sort")
    items = load_menu()
    if sort_by == "asc":
        items.sort(key=lambda x: x["price"])
    elif sort_by == "desc":
        items.sort(key=lambda x: x["price"], reverse=True)
    return render_template("index.html", menu_items=items)

# --- หน้า login admin ---
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    admin_data = load_admin()  # โหลด admin จาก JSON

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == admin_data.get("username") and password == admin_data.get("password"):
            return redirect(url_for("admin"))
        flash("Invalid username or password", "error")
    return render_template("login.html")

# --- หน้า admin ---
@app.route("/admin", methods=["GET", "POST"])
def admin():
    menu_items = load_menu()

    if request.method == "POST":
        # เพิ่มเมนู
        new_name = request.form.get("name")
        new_price = request.form.get("price")
        new_category = request.form.get("category")

        if new_name and new_price and new_category:
            try:
                new_price = int(new_price)
                new_item = {
                    "id": get_next_id(menu_items),
                    "name": new_name,
                    "price": new_price,
                    "category": new_category
                }
                menu_items.append(new_item)
                save_menu(menu_items)
                flash(f"Added '{new_name}' successfully.", "success")
            except ValueError:
                flash("Price must be a number.", "error")

        # ลบเมนู
        delete_id = request.form.get("delete_id")
        if delete_id:
            menu_items = [item for item in menu_items if str(item["id"]) != delete_id]
            save_menu(menu_items)
            flash(f"Deleted item ID {delete_id}.", "success")

    return render_template("admin.html", menu_items=menu_items)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)