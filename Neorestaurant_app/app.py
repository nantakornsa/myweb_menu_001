from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = "secret_key"

# Database จำลอง
menu_items = [
    {"id": 1, "name": "ข้าวกะเพรา", "price": 50, "category": "ข้าว"},
    {"id": 2, "name": "ข้าวผัดหมู", "price": 50, "category": "ข้าว"},
    {"id": 4, "name": "ข้าวแกงเขียวหวานไก่", "price": 50, "category": "ข้าว"},
    {"id": 5, "name": "ข้าวหมูกรอบ", "price": 50, "category": "ข้าว"},
    {"id": 6, "name": "ข้าวมันไก่", "price": 50, "category": "ข้าว"},
    {"id": 7, "name": "น้ำเปล่า(ขวดใหญ่)", "price": 20, "category": "เครื่องดื่ม"},
    {"id": 8, "name": "น้ำอัดลม(ขวดใหญ่)", "price": 30, "category": "เครื่องดื่ม"}
]

# Admin login ข้อมูลจำลอง
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

# หน้าแรก - ลูกค้า
@app.route("/")
def index():
    sort_by = request.args.get("sort")
    items = menu_items.copy()
    if sort_by == "asc":
        items.sort(key=lambda x: x["price"])
    elif sort_by == "desc":
        items.sort(key=lambda x: x["price"], reverse=True)
    return render_template("index.html", menu_items=items)

# หน้า login admin
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            return redirect(url_for("admin"))
        else:
            return "Invalid credentials"
    return render_template("login.html")

# หน้า admin - เพิ่ม/ลบเมนู
@app.route("/admin", methods=["GET", "POST"])
def admin():
    global menu_items
    if request.method == "POST":
        # เพิ่มเมนู
        new_name = request.form.get("name")
        new_price = request.form.get("price")
        new_category = request.form.get("category")
        if new_name and new_price and new_category:
            new_id = max(item["id"] for item in menu_items) + 1 if menu_items else 1
            menu_items.append({
                "id": new_id,
                "name": new_name,
                "price": int(new_price),
                "category": new_category
            })
        # ลบเมนู
        delete_id = request.form.get("delete_id")
        if delete_id:
            menu_items = [item for item in menu_items if str(item["id"]) != delete_id]
    return render_template("admin.html", menu_items=menu_items)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
