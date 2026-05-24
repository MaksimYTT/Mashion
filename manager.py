from flask import Flask, request, redirect, session, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit, join_room
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "mashion_secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mashion.db"

db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")


# ===== STYLE =====
STYLE = """
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{
    margin:0;
    font-family:Arial,sans-serif;
    background:#f5f5f5;
    max-width:700px;
    margin:auto;
    padding:20px;
}
h1,h2{
    text-align:center;
}
.card{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0 2px 10px rgba(0,0,0,.1);
}
input,button{
    width:100%;
    padding:14px;
    margin:8px 0;
    border-radius:10px;
    border:1px solid #ccc;
    box-sizing:border-box;
    font-size:16px;
}
button{
    background:#0084ff;
    color:white;
    border:none;
}
a{
    text-decoration:none;
    color:#0084ff;
}
.user{
    display:block;
    background:white;
    padding:15px;
    margin:8px 0;
    border-radius:10px;
}
#chat{
    border:1px solid #ddd;
    background:white;
    height:60vh;
    overflow:auto;
    padding:10px;
    border-radius:12px;
}
.msg{
    padding:10px;
    margin:8px 0;
    border-radius:12px;
    background:#e9e9eb;
}
</style>
"""


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

    return STYLE + """
    <div class="card">
      <h1>Mashion Register</h1>
      <form method="post">
        <input name="username" placeholder="логин">
        <input name="password" type="password" placeholder="пароль">
        <button>Создать</button>
      </form>
      <a href="/login">Войти</a>
    </div>
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

    return STYLE + """
    <div class="card">
      <h1>Mashion Login</h1>
      <form method="post">
        <input name="username" placeholder="логин">
        <input name="password" type="password" placeholder="пароль">
        <button>Войти</button>
      </form>
      <a href="/register">Регистрация</a>
    </div>
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

    html = STYLE + "<div class='card'>"
    html += "<h1>Mashion Users</h1>"
    html += "<a href='/logout'>Выйти</a><br><br>"
    html += """
    <form action="/search">
      <input name="q" placeholder="найти по логину">
      <button>Найти</button>
    </form>
    """

    for u in users:
        html += f"<a class='user' href='/chat/{u.username}'>{u.username}</a>"

    html += "</div>"
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

    return render_template_string(STYLE + """
    <div class="card">
      <h2>Чат с {{ username }}</h2>
      <a href="/users">← Назад</a><br><br>

      <div id="chat"></div><br>

      <input id="msg" placeholder="Введите сообщение">
      <button onclick="send()">Send</button>
    </div>

<script src="https://cdn.socket.io/4.0.1/socket.io.min.js"></script>
<script>
let socket = io();
let room = "{{ room }}";

socket.emit("join", room);

socket.on("message", function(data){
    let box = document.getElementById("chat");
    box.innerHTML += "<div class='msg'>"+data+"</div>";
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
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
