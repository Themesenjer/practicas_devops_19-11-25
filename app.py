# app.py
from flask import Flask, request, redirect, url_for, render_template_string, flash
from markupsafe import escape

app = Flask(__name__)
app.secret_key = "cambia_esta_clave_por_una_segura"  # necesaria para flash

PAGE = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Mi Página Flask Bonita</title>

  <!-- Tipografía -->
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap" rel="stylesheet">

  <style>
    :root{
      --bg:#0f1724;
      --card:#0b1220;
      --accent:#7c3aed;
      --muted:#94a3b8;
      --glass: rgba(255,255,255,0.04);
    }
    *{box-sizing:border-box;font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto,'Helvetica Neue',Arial;}
    body {
      margin:0;
      background: radial-gradient(1200px 600px at 10% 10%, rgba(124,58,237,0.12), transparent),
                  linear-gradient(180deg, #071226 0%, #07162a 100%), var(--bg);
      color: #e6eef8;
      -webkit-font-smoothing:antialiased;
      -moz-osx-font-smoothing:grayscale;
      min-height:100vh;
      display:flex;
      align-items:center;
      justify-content:center;
      padding:32px;
    }
    .container{
      width:100%;
      max-width:1100px;
      display:grid;
      grid-template-columns: 1fr 420px;
      gap:28px;
      align-items:center;
    }
    .hero {
      background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
      border-radius:16px;
      padding:36px;
      box-shadow: 0 8px 30px rgba(2,6,23,0.6);
      border: 1px solid rgba(255,255,255,0.03);
    }
    h1{font-size:32px;margin:0 0 8px 0;letter-spacing:-0.3px;}
    p.lead{color:var(--muted);margin:0 0 18px 0;}
    .features{display:flex;gap:12px;flex-wrap:wrap;margin-top:18px;}
    .feat{background:var(--glass);padding:12px 14px;border-radius:10px;font-size:14px;color:var(--muted);border:1px solid rgba(255,255,255,0.02)}
    .accent {
      display:inline-block;
      background:linear-gradient(90deg,var(--accent),#4f46e5);
      padding:10px 16px;
      border-radius:10px;
      color:white;
      font-weight:600;
      text-decoration:none;
      margin-top:18px;
    }

    /* Card derecha: formulario */
    .card {
      background: linear-gradient(180deg, rgba(255,255,255,0.015), rgba(255,255,255,0.01));
      border-radius:14px;
      padding:22px;
      box-shadow: 0 6px 24px rgba(2,6,23,0.55);
      border: 1px solid rgba(255,255,255,0.03);
    }
    label{display:block;font-size:13px;color:var(--muted);margin-bottom:6px;}
    input[type="text"], input[type="email"], textarea {
      width:100%;
      padding:10px 12px;
      border-radius:8px;
      border:1px solid rgba(255,255,255,0.04);
      background:rgba(255,255,255,0.02);
      color:inherit;
      outline:none;
      font-size:14px;
    }
    textarea{min-height:120px;resize:vertical;}
    .btn {
      display:inline-block;
      padding:10px 14px;
      border-radius:10px;
      font-weight:600;
      text-decoration:none;
      border:none;
      cursor:pointer;
      background:linear-gradient(90deg,var(--accent),#4f46e5);
      color:white;
      box-shadow: 0 6px 18px rgba(79,70,229,0.18);
    }
    .muted{color:var(--muted);font-size:13px;margin-top:10px;}
    footer{margin-top:18px;color:var(--muted);font-size:13px;}
    .logo {
      display:inline-flex;
      align-items:center;
      gap:10px;
      font-weight:700;
      color:white;
      text-decoration:none;
      margin-bottom:12px;
    }
    .logo .dot {
      width:36px;height:36px;border-radius:8px;background:linear-gradient(90deg,var(--accent),#4f46e5);
      display:inline-flex;align-items:center;justify-content:center;font-weight:800;
      box-shadow: 0 6px 18px rgba(124,58,237,0.14);
    }

    @media (max-width:900px){
      .container{grid-template-columns:1fr; padding:0}
      .hero{order:2}
      .card{order:1}
    }

    /* small alert */
    .flash {
      background: rgba(34,197,94,0.12);
      color: #bbf7d0;
      border:1px solid rgba(34,197,94,0.18);
      padding:10px 12px;
      border-radius:8px;
      margin-bottom:12px;
      font-size:14px;
    }
  </style>
</head>
<body>
  <div class="container">
    <main class="hero" aria-labelledby="title">
      <a class="logo" href="/">
        <span class="dot">F</span>
        Flask Studio
      </a>

      <h1 id="title">Bienvenido a mi pagina BM</h1>
      <p class="lead">Plantilla minimalista, responsive y lista para personalizar. Incluye formulario de contacto (simulado) y estilos modernos sin archivos externos.</p>

      <div class="features" role="list">
        <div class="feat">Responsive</div>
        <div class="feat">Ligera</div>
        <div class="feat">HTML/CSS embebido</div>
        <div class="feat">Fácil de extender</div>
      </div>

      <p style="margin-top:18px;color:var(--muted)">Prueba a enviar un mensaje desde el formulario — el servidor mostrará una notificación de recepción.</p>

      <a class="accent" href="#contact">Contactar</a>

      <footer>
        <div>Creada con ♥ usando Flask • Ejecútala en tu servidor local o Docker.</div>
      </footer>
    </main>

    <aside class="card" id="contact" aria-labelledby="contact-title">
      <h3 id="contact-title" style="margin:0 0 10px 0;">Contacto rápido</h3>

      {% with messages = get_flashed_messages() %}
      {% if messages %}
        <div class="flash">{{ messages[0] }}</div>
      {% endif %}
      {% endwith %}

      <form method="post" action="{{ url_for('contact') }}">
        <div style="margin-bottom:12px;">
          <label for="name">Nombre</label>
          <input id="name" name="name" type="text" placeholder="Tu nombre" required>
        </div>

        <div style="margin-bottom:12px;">
          <label for="email">Correo</label>
          <input id="email" name="email" type="email" placeholder="tu@correo.com" required>
        </div>

        <div style="margin-bottom:12px;">
          <label for="message">Mensaje</label>
          <textarea id="message" name="message" placeholder="Escribe algo..."></textarea>
        </div>

        <div style="display:flex;gap:8px;align-items:center;">
          <button class="btn" type="submit">Enviar mensaje</button>
          <div class="muted">Respuesta simulada (no se envía email)</div>
        </div>
      </form>
    </aside>
  </div>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(PAGE)

@app.route("/contact", methods=["POST"])
def contact():
    # Sanitize simple inputs (escape to avoid XSS)
    name = escape(request.form.get("name", "").strip())
    email = escape(request.form.get("email", "").strip())
    message = escape(request.form.get("message", "").strip())

    # Aquí podrías guardar a una base de datos, enviar un email, etc.
    # Por ahora solo mostramos un mensaje y volvemos a la página principal.
    flash(f"Gracias {name or 'amigo'}, recibimos tu mensaje — correo: {email or 'no proporcionado'}")
    return redirect(url_for("index") + "#contact")


if __name__ == "__main__":
    # Nota: para escuchar en el puerto 80 normalmente necesitas permisos de root
    # Ejecuta: sudo python3 app.py   OR usa Docker y mappea el puerto 80
    app.run(host="0.0.0.0", port=1001, debug=False)