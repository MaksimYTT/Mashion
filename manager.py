from flask import Flask

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="theme-color" content="#0a0e14">
<title>Mashion — Проект закрыт</title>
<style>
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    -webkit-tap-highlight-color: transparent;
  }
  html, body {
    height: 100%;
    width: 100%;
  }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #0a0e14;
    background-image:
      radial-gradient(circle at 20% 0%, rgba(255, 68, 68, 0.15), transparent 50%),
      radial-gradient(circle at 80% 100%, rgba(77, 157, 255, 0.1), transparent 50%);
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px 16px;
    min-height: 100vh;
    overflow-x: hidden;
  }
  .box {
    width: 100%;
    max-width: 440px;
    background: rgba(23, 33, 43, 0.85);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 68, 68, 0.25);
    border-radius: 24px;
    padding: 44px 24px 32px;
    text-align: center;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5), 0 0 40px rgba(255, 68, 68, 0.08);
    animation: fadeIn 0.8s ease-out;
  }
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px) scale(0.96); }
    to { opacity: 1; transform: translateY(0) scale(1); }
  }
  .icon {
    width: 88px;
    height: 88px;
    border-radius: 50%;
    background: linear-gradient(135deg, #ff4444, #c92b2b);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 44px;
    margin: 0 auto 24px;
    box-shadow: 0 8px 32px rgba(255, 68, 68, 0.4);
    animation: pulse 2.5s infinite;
  }
  @keyframes pulse {
    0%, 100% { transform: scale(1); box-shadow: 0 8px 32px rgba(255, 68, 68, 0.4); }
    50% { transform: scale(1.05); box-shadow: 0 8px 48px rgba(255, 68, 68, 0.6); }
  }
  .icon svg { width: 44px; height: 44px; stroke: #fff; stroke-width: 3; }
  h1 {
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 8px;
    color: #ff4444;
    letter-spacing: -0.5px;
  }
  .divider {
    width: 60px;
    height: 3px;
    background: linear-gradient(90deg, #ff4444, #c92b2b);
    border-radius: 2px;
    margin: 16px auto 24px;
  }
  p {
    color: #8b949e;
    font-size: 15px;
    line-height: 1.6;
    margin-bottom: 12px;
    padding: 0 4px;
    text-align: left;
  }
  p.center { text-align: center; }
  p.highlight { color: #e6edf3; font-weight: 500; }
  .reason {
    background: rgba(255, 68, 68, 0.08);
    border-left: 3px solid #ff4444;
    padding: 14px 16px;
    border-radius: 8px;
    margin: 18px 0;
    text-align: left;
  }
  .reason p { margin-bottom: 8px; }
  .reason p:last-child { margin-bottom: 0; }
  .support {
    margin-top: 28px;
    padding-top: 20px;
    border-top: 1px solid rgba(255, 68, 68, 0.15);
  }
  .support .label {
    color: #6c7883;
    font-size: 12px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 10px;
  }
  .support a {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(135deg, #4d9dff, #2b6bc9);
    color: #fff;
    text-decoration: none;
    padding: 12px 22px;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 600;
    box-shadow: 0 4px 16px rgba(77, 157, 255, 0.3);
    transition: transform 0.2s, box-shadow 0.2s;
  }
  .support a:active {
    transform: scale(0.96);
    box-shadow: 0 2px 8px rgba(77, 157, 255, 0.4);
  }
  .footer {
    margin-top: 24px;
    padding-top: 16px;
    border-top: 1px solid rgba(255, 68, 68, 0.1);
    color: #6c7883;
    font-size: 12px;
    letter-spacing: 1px;
    text-transform: uppercase;
  }
</style>
</head>
<body>
  <div class="box">
    <div class="icon">
      <svg viewBox="0 0 24 24" fill="none" stroke-linecap="round" stroke-linejoin="round">
        <line x1="18" y1="6" x2="6" y2="18"></line>
        <line x1="6" y1="6" x2="18" y2="18"></line>
      </svg>
    </div>

    <h1>Мы закрываемся</h1>
    <div class="divider"></div>

    <p class="center highlight">Спасибо, кто был с нами. 🤝</p>

    <div class="reason">
      <p class="highlight">Причина закрытия:</p>
      <p>Наш сервис уже не актуален.</p>
      <p>В нём есть критические баги.</p>
      <p>Проще создать новый проект.</p>
      <p>Мы не можем его поддерживать.</p>
    </div>

    <p class="center">Возможно, мы не вернёмся.</p>

    <div class="support">
      <div class="label">Подробная информация</div>
      <a href="https://t.me/mashion_support_bot" target="_blank">
        🤝 @mashion_support_bot
      </a>
    </div>

    <div class="footer">Mashion</div>
  </div>
</body>
</html>
"""

@app.route('/')
def closed():
    return HTML

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)