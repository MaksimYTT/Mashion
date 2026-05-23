from flask import Flask, request, redirect, session, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit, join_room
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "mashion_secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mashion.db"

db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")


# ===== DATABASE =====
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))


with app.app_context():
    db.create_all()


# ===== HOME =====
@app.route("/")
def home():
    if "user" in session:
        return redirect("/users")
    return redirect("/login")


# ===== REGISTER =====
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            return "Логин уже занят"

        user = User(
            username=username,
            password=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return """
    <h1>Mashion Register</h1>
    <form method="post">
      <input name="username" placeholder="логин"><br><br>
      <input name="password" type="password" placeholder="пароль"><br><br>
      <button>Создать</button>
    </form>
    <a href="/login">Войти</a>
    """


# ===== LOGIN =====
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user"] = username
            return redirect("/users")

        return "Неверный логин или пароль"

    return """
    <h1>Mashion Login</h1>
    <form method="post">
      <input name="username"><br><br>
      <input name="password" type="password"><br><br>
      <button>Войти</button>
    </form>
    <a href="/register">Регистрация</a>
    """


# ===== LOGOUT =====
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ===== USERS =====
@app.route("/users")
def users():
    if "user" not in session:
        return redirect("/login")

    me = session["user"]
    users = User.query.filter(User.username != me).all()

    html = "<h1>Mashion Users</h1>"
    html += "<a href='/logout'>Выйти</a><br><br>"
    html += """
    <form action="/search">
      <input name="q" placeholder="найти по логину">
      <button>Найти</button>
    </form><br>
    """

    for u in users:
        html += f"<a href='/chat/{u.username}'>{u.username}</a><br>"

    return html


# ===== SEARCH =====
@app.route("/search")
def search():
    q = request.args.get("q")

    if not q:
        return redirect("/users")

    user = User.query.filter_by(username=q).first()

    if user:
        return redirect(f"/chat/{q}")

    return "Пользователь не найден"


# ===== CHAT =====
@app.route("/chat/<username>")
def chat(username):
    if "user" not in session:
        return redirect("/login")

    me = session["user"]
    room = "_".join(sorted([me, username]))

    return render_template_string("""
    <h2>Чат с {{ username }}</h2>
    <a href="/users">Назад</a><br><br>

    <div id="chat" style="border:1px solid black;height:300px;overflow:auto;padding:10px;"></div><br>

    <input id="msg">
    <button onclick="send()">Send</button>

<script src="https://cdn.socket.io/4.0.1/socket.io.min.js"></script>
<script>
let socket = io();
let room = "{{ room }}";

socket.emit("join", room);

socket.on("message", function(data){
    let box = document.getElementById("chat");
    box.innerHTML += "<p>"+data+"</p>";
    box.scrollTop = box.scrollHeight;
});

function send(){
    let text = document.getElementById("msg").value;

    if(text.trim() === "") return;

    socket.emit("message", {
        room: room,
        text: text
    });

    document.getElementById("msg").value = "";
}
</script>
    """, username=username, room=room)


# ===== SOCKET =====
@socketio.on("join")
def on_join(room):
    join_room(room)


@socketio.on("message")
def on_message(data):
    username = session.get("user", "anon")

    emit(
        "message",
        f"{username}: {data['text']}",
        room=data["room"]
    )


# ===== START =====
if __name__ == "__main__":
    print("Mashion started 🚀")
    socketio.run(app, host="0.0.0.0", port=5000)
