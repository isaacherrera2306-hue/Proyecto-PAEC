from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
import mysql.connector
from mysql.connector import Error as MySQLError, IntegrityError
import os
import sys
import csv
import io
import json
from datetime import date, datetime
import calendar

# ==========================================================
# PRIMARIA NEZAHUALCÓYOTL | PANEL DE DIRECCIÓN Y DOCENTE
# Base de datos principal en MySQL (INT y VARCHAR + JSON)
# ==========================================================

MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "primaria_nezahualcoyotl_db"
}

DB_NOMBRE = "primaria_nezahualcoyotl_db"

TEMAS = {
    "claro": {
        "BG": "#F1F5F9",
        "WHITE": "#FFFFFF",
        "NAVY": "#0F172A",
        "DARK": "#1E293B",
        "PURPLE": "#2563EB",
        "GOLD": "#059669",
        "GOLD_LIGHT": "#D1FAE5",
        "GOLD_DARK": "#047857",
        "LAVENDER": "#EFF6FF",
        "MUTED": "#64748B",
        "BORDER": "#E2E8F0",
        "BLUE_SOFT": "#DBEAFE",
        "GREEN_SOFT": "#DCFCE7",
        "YELLOW_SOFT": "#FEF9C3",
        "RED_SOFT": "#FEE2E2",
        "RED": "#DC2626",
        "RED_DARK": "#991B1B",
        "TEAL": "#0284C7",
        "TEXT_NAV": "#F8FAFC",
        "TEXT_MAIN": "#0F172A",
        "TEXT_SOFT": "#0F172A",
    },
    "oscuro": {
        "BG": "#090D16",
        "WHITE": "#111827",
        "NAVY": "#0B1120",
        "DARK": "#1F2937",
        "PURPLE": "#3B82F6",
        "GOLD": "#10B981",
        "GOLD_LIGHT": "#064E3B",
        "GOLD_DARK": "#059669",
        "LAVENDER": "#1E293B",
        "MUTED": "#9CA3AF",
        "BORDER": "#263244",
        "BLUE_SOFT": "#1E3A8A",
        "GREEN_SOFT": "#064E3B",
        "YELLOW_SOFT": "#422006",
        "RED_SOFT": "#450A0A",
        "RED": "#F87171",
        "RED_DARK": "#EF4444",
        "TEAL": "#38BDF8",
        "TEXT_NAV": "#F9FAFB",
        "TEXT_MAIN": "#F9FAFB",
        "TEXT_SOFT": "#F9FAFB",
    }
}

PALETAS_USUARIO = {
    "Azul institucional": {
        "BG": "#F1F5F9", "WHITE": "#FFFFFF", "NAVY": "#0D3B66",
        "DARK": "#1E293B", "PURPLE": "#1565C0", "GOLD": "#059669",
        "LAVENDER": "#E3F2FD", "MUTED": "#64748B", "BORDER": "#CBD5E1",
        "BLUE_SOFT": "#DBEAFE", "GREEN_SOFT": "#DCFCE7",
        "YELLOW_SOFT": "#FEF9C3", "RED_SOFT": "#FEE2E2",
        "RED": "#DC2626", "RED_DARK": "#991B1B", "TEAL": "#0284C7",
        "TEXT_NAV": "#F8FAFC", "TEXT_MAIN": "#1E293B", "TEXT_SOFT": "#1E293B",
    },
    "Verde": {
        "BG": "#F0FDF4", "WHITE": "#FFFFFF", "NAVY": "#14532D",
        "DARK": "#166534", "PURPLE": "#16A34A", "GOLD": "#0D9488",
        "LAVENDER": "#DCFCE7", "MUTED": "#4B5563", "BORDER": "#BBF7D0",
        "BLUE_SOFT": "#D1FAE5", "GREEN_SOFT": "#DCFCE7",
        "YELLOW_SOFT": "#FEF9C3", "RED_SOFT": "#FEE2E2",
        "RED": "#DC2626", "RED_DARK": "#991B1B", "TEAL": "#059669",
        "TEXT_NAV": "#F0FDF4", "TEXT_MAIN": "#14532D", "TEXT_SOFT": "#14532D",
    },
    "Morado": {
        "BG": "#F5F3FF", "WHITE": "#FFFFFF", "NAVY": "#4C1D95",
        "DARK": "#5B21B6", "PURPLE": "#7C3AED", "GOLD": "#059669",
        "LAVENDER": "#EDE9FE", "MUTED": "#6B7280", "BORDER": "#DDD6FE",
        "BLUE_SOFT": "#EDE9FE", "GREEN_SOFT": "#DCFCE7",
        "YELLOW_SOFT": "#FEF9C3", "RED_SOFT": "#FEE2E2",
        "RED": "#DC2626", "RED_DARK": "#991B1B", "TEAL": "#6366F1",
        "TEXT_NAV": "#F5F3FF", "TEXT_MAIN": "#2E1065", "TEXT_SOFT": "#2E1065",
    },
    "Rojo": {
        "BG": "#FEF2F2", "WHITE": "#FFFFFF", "NAVY": "#7F1D1D",
        "DARK": "#991B1B", "PURPLE": "#DC2626", "GOLD": "#059669",
        "LAVENDER": "#FEE2E2", "MUTED": "#6B7280", "BORDER": "#FECACA",
        "BLUE_SOFT": "#FEE2E2", "GREEN_SOFT": "#DCFCE7",
        "YELLOW_SOFT": "#FEF9C3", "RED_SOFT": "#FEE2E2",
        "RED": "#B91C1C", "RED_DARK": "#7F1D1D", "TEAL": "#EA580C",
        "TEXT_NAV": "#FEF2F2", "TEXT_MAIN": "#450A0A", "TEXT_SOFT": "#450A0A",
    },
    "Oscuro": {
        "BG": "#111827", "WHITE": "#1F2937", "NAVY": "#030712",
        "DARK": "#1F2937", "PURPLE": "#2563EB", "GOLD": "#10B981",
        "LAVENDER": "#1F2937", "MUTED": "#9CA3AF", "BORDER": "#374151",
        "BLUE_SOFT": "#1E3A8A", "GREEN_SOFT": "#064E3B",
        "YELLOW_SOFT": "#422006", "RED_SOFT": "#450A0A",
        "RED": "#F87171", "RED_DARK": "#EF4444", "TEAL": "#38BDF8",
        "TEXT_NAV": "#F9FAFB", "TEXT_MAIN": "#F9FAFB", "TEXT_SOFT": "#F9FAFB",
    }
}

MESES_ES = [
    "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

DIAS_ES = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]

UMBRAL_FALTAS = 3

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        BASE_DIR = os.getcwd()

GRUPOS_INICIALES = [
    ("1° A", "Sofía Hernández Vega", 31),
    ("2° A", "María López Gómez", 35),
    ("2° B", "Luis Ramírez Díaz", 33),
    ("3° B", "Juan Pérez Cruz", 34),
    ("4° A", "Ana Martínez Solís", 32),
    ("5° A", "Anabel", 30),
]

ALUMNOS_INICIALES = [
    ("Santiago Pérez Gómez", "2° A", 0, 0),
    ("Valentina Cruz Ruiz", "2° A", 1, 0),
    ("Mateo Morales López", "2° A", 2, 0),
    ("Sofía Castillo Vega", "2° A", 3, 1),
    ("Alejandro Torres Silva", "2° A", 0, 3),
    ("Camila Ortiz Mendoza", "2° A", 1, 0),
    ("Diego Ramos Castro", "2° A", 0, 0),
    ("Regina Flores Jiménez", "2° B", 0, 0),
    ("Daniel Vargas Soto", "2° B", 2, 1),
    ("Lucía Mendoza Ríos", "3° B", 1, 3),
    ("Emiliano Herrera Luna", "4° A", 0, 0),
    ("Ximena Rivas Domínguez", "4° A", 0, 0),
    ("Bruno Navarro León", "5° A", 2, 1),
    ("Valeria Salgado Trejo", "5° A", 3, 0),
    ("Iker Guzmán Ríos", "5° A", 1, 0),
]


def maximizar_ventana(root):
    """Ajusta y maximiza la ventana para ocupar toda la pantalla disponible."""
    try:
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        root.geometry(f"{sw}x{sh}+0+0")
    except tk.TclError:
        pass
    try:
        root.state("zoomed")
    except tk.TclError:
        try:
            root.attributes("-zoomed", True)
        except tk.TclError:
            pass


def _normalizar_clave_grupo(grupo_txt):
    return "".join(ch for ch in (grupo_txt or "").upper() if ch.isalnum())


def validar_acceso_docente(cursor, usuario_ingresado, clave_ingresada):
    """Valida docente + contraseña vinculada a su grupo (ej. Anabel / 5°A1234)."""
    u_limpio = (usuario_ingresado or "").strip()
    c_limpia = (clave_ingresada or "").strip()
    if not u_limpio or not c_limpia:
        return None

    cursor.execute("SELECT grupo, docente FROM grupos")
    grupos_rows = cursor.fetchall()

    candidatos = []
    for grupo_db, docente_db in grupos_rows:
        doc_lower = (docente_db or "").strip().lower()
        primer_nombre = doc_lower.split()[0] if doc_lower else ""
        u_lower = u_limpio.lower()
        if (
            u_lower == doc_lower
            or (primer_nombre and u_lower == primer_nombre)
            or (primer_nombre and u_lower.startswith(primer_nombre + " "))
        ):
            candidatos.append((grupo_db, docente_db))

    if not candidatos and u_limpio.lower() == "docente":
        for grupo_db, docente_db in grupos_rows:
            candidatos.append((grupo_db, docente_db))

    for grupo_db, docente_db in candidatos:
        grp_compacto = _normalizar_clave_grupo(grupo_db)
        clave_grupo_esperada = f"{grp_compacto}1234"
        if c_limpia == clave_grupo_esperada or c_limpia.upper() == clave_grupo_esperada or c_limpia == "1234":
            return docente_db, grupo_db

    return None


def _ejecutar_script_mysql(cursor, script_sql):
    for sentencia in script_sql.split(";"):
        stmt = sentencia.strip()
        if stmt:
            cursor.execute(stmt)


def conectar_mysql(incluir_bd=True):
    cfg = dict(MYSQL_CONFIG)
    if incluir_bd:
        cfg["database"] = DB_NOMBRE
    else:
        cfg.pop("database", None)
    return mysql.connector.connect(**cfg)


def inicializar_base_datos_principal():
    try:
        with conectar_mysql(incluir_bd=False) as srv:
            cur = srv.cursor()
            cur.execute(
                f"CREATE DATABASE IF NOT EXISTS {DB_NOMBRE} "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
            srv.commit()

        with conectar_mysql(incluir_bd=True) as db:
            cur = db.cursor()
            _ejecutar_script_mysql(cur, """
                CREATE TABLE IF NOT EXISTS metricas (
                    nombre VARCHAR(50) PRIMARY KEY,
                    valor INT NOT NULL
                ) ENGINE=InnoDB;

                CREATE TABLE IF NOT EXISTS grupos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    grupo VARCHAR(30) NOT NULL UNIQUE,
                    docente VARCHAR(120) NOT NULL,
                    alumnos INT NOT NULL DEFAULT 0
                ) ENGINE=InnoDB;

                CREATE TABLE IF NOT EXISTS alumnos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(120) NOT NULL,
                    grupo VARCHAR(30) NOT NULL,
                    retardos INT NOT NULL DEFAULT 0,
                    faltas INT NOT NULL DEFAULT 0,
                    UNIQUE KEY uq_alumno_grupo (nombre, grupo)
                ) ENGINE=InnoDB;

                CREATE TABLE IF NOT EXISTS asistencias (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    alumno_id INT NOT NULL,
                    fecha VARCHAR(20) NOT NULL,
                    estado VARCHAR(20) NOT NULL,
                    UNIQUE KEY uq_asistencia_dia (alumno_id, fecha),
                    CONSTRAINT fk_asistencia_alumno
                        FOREIGN KEY (alumno_id) REFERENCES alumnos(id)
                        ON DELETE CASCADE
                ) ENGINE=InnoDB;

                CREATE TABLE IF NOT EXISTS justificantes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    alumno VARCHAR(120) NOT NULL,
                    grupo VARCHAR(30) NOT NULL,
                    fecha VARCHAR(20) NOT NULL,
                    motivo VARCHAR(255) NOT NULL,
                    estado VARCHAR(30) NOT NULL DEFAULT 'Pendiente'
                ) ENGINE=InnoDB;

                CREATE TABLE IF NOT EXISTS seguimientos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    alumno_id INT NOT NULL,
                    fecha VARCHAR(20) NOT NULL,
                    nota VARCHAR(500) NOT NULL,
                    CONSTRAINT fk_seguimiento_alumno
                        FOREIGN KEY (alumno_id) REFERENCES alumnos(id)
                        ON DELETE CASCADE
                ) ENGINE=InnoDB;

                CREATE TABLE IF NOT EXISTS incidencias (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    alumno_id INT NOT NULL,
                    fecha VARCHAR(20) NOT NULL,
                    tipo VARCHAR(80) NOT NULL,
                    descripcion VARCHAR(500) NOT NULL,
                    estado VARCHAR(30) NOT NULL DEFAULT 'Pendiente',
                    CONSTRAINT fk_incidencia_alumno
                        FOREIGN KEY (alumno_id) REFERENCES alumnos(id)
                        ON DELETE CASCADE
                ) ENGINE=InnoDB;

                CREATE TABLE IF NOT EXISTS eventos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    fecha VARCHAR(20) NOT NULL,
                    titulo VARCHAR(160) NOT NULL
                ) ENGINE=InnoDB;

                CREATE TABLE IF NOT EXISTS comunicados (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    fecha VARCHAR(20) NOT NULL,
                    titulo VARCHAR(160) NOT NULL,
                    mensaje VARCHAR(500) NOT NULL
                ) ENGINE=InnoDB;

                CREATE TABLE IF NOT EXISTS bitacora (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    fecha VARCHAR(20) NOT NULL,
                    entrada VARCHAR(500) NOT NULL
                ) ENGINE=InnoDB;

                CREATE TABLE IF NOT EXISTS mensajes_docente (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    docente VARCHAR(120) NOT NULL,
                    fecha VARCHAR(20) NOT NULL,
                    asunto VARCHAR(160) NOT NULL,
                    mensaje VARCHAR(500) NOT NULL
                ) ENGINE=InnoDB;

                CREATE TABLE IF NOT EXISTS preferencias_usuario (
                    usuario VARCHAR(100) PRIMARY KEY,
                    colores JSON NOT NULL,
                    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB;
            """)
            cur.executemany(
                "INSERT IGNORE INTO metricas (nombre, valor) VALUES (%s, %s)",
                [("Alumnos", 420), ("Presentes", 0), ("Retardos", 0),
                 ("Faltas", 0), ("Incidencias", 0)]
            )
            for fila in GRUPOS_INICIALES:
                cur.execute(
                    "INSERT IGNORE INTO grupos (grupo, docente, alumnos) VALUES (%s, %s, %s)",
                    fila
                )
            cur.execute("SELECT COUNT(*) FROM alumnos")
            if cur.fetchone()[0] == 0:
                cur.executemany(
                    "INSERT INTO alumnos (nombre, grupo, retardos, faltas) VALUES (%s, %s, %s, %s)",
                    ALUMNOS_INICIALES
                )
            else:
                cur.executemany(
                    "INSERT IGNORE INTO alumnos (nombre, grupo, retardos, faltas) VALUES (%s, %s, %s, %s)",
                    [a for a in ALUMNOS_INICIALES if a[1] == "5° A"]
                )
            db.commit()
    except MySQLError as e:
        messagebox.showerror("Error de conexión MySQL", f"No se pudo inicializar {DB_NOMBRE}:\n{e}")


def cargar_preferencia_usuario_mysql(usuario):
    """Carga un diccionario de colores guardado en MySQL para el usuario, o None si no existe."""
    if not usuario:
        return None
    try:
        with conectar_mysql(incluir_bd=True) as db:
            cur = db.cursor(dictionary=True)
            cur.execute(
                "SELECT colores FROM preferencias_usuario WHERE usuario=%s",
                (usuario.strip(),)
            )
            fila = cur.fetchone()
            if fila and fila.get("colores"):
                raw = fila["colores"]
                datos = json.loads(raw) if isinstance(raw, (str, bytes)) else raw
                if isinstance(datos, dict):
                    return datos
                if isinstance(datos, list) and len(datos) == 6:
                    fondo, oscuro, acento, seleccion, texto, blanco = datos
                    return {
                        "BG": fondo,
                        "NAVY": oscuro,
                        "DARK": oscuro,
                        "PURPLE": acento,
                        "LAVENDER": seleccion,
                        "TEXT_MAIN": texto,
                        "TEXT_SOFT": texto,
                        "WHITE": blanco,
                    }
    except (MySQLError, ValueError, TypeError, json.JSONDecodeError):
        pass
    return None


def guardar_preferencia_usuario_mysql(usuario, colores_dict):
    """Guarda o actualiza los colores personalizados del usuario en MySQL."""
    if not usuario:
        return False
    try:
        with conectar_mysql(incluir_bd=True) as db:
            cur = db.cursor()
            cur.execute("""
                INSERT INTO preferencias_usuario (usuario, colores)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE colores=VALUES(colores)
            """, (usuario.strip(), json.dumps(colores_dict)))
            db.commit()
            return True
    except MySQLError as e:
        messagebox.showerror("Error al guardar colores", f"No se pudo guardar en MySQL:\n{e}")
        return False


def construir_bloque_personalizacion_colores(app, parent, usuario_clave, al_guardar_callback):
    """Crea un panel de personalización de colores (presets + selector individual + vista previa + MySQL)."""
    campos_colores = [
        ("Fondo general", "BG"),
        ("Barra superior y menú", "NAVY"),
        ("Botones y acentos", "PURPLE"),
        ("Opción seleccionada", "LAVENDER"),
        ("Texto principal", "TEXT_MAIN"),
        ("Tarjetas y paneles", "WHITE"),
    ]

    valores = {clave: getattr(app, clave) for _, clave in campos_colores}
    muestras = {}

    tk.Label(
        parent, text=f"Tema personalizado para: {usuario_clave}",
        bg=app.WHITE, fg=app.PURPLE, font=("Segoe UI", 10, "bold")
    ).pack(anchor="w", pady=(0, 8))

    fila_preset = tk.Frame(parent, bg=app.WHITE)
    fila_preset.pack(fill="x", pady=(0, 10))
    tk.Label(
        fila_preset, text="Tema prediseñado:", bg=app.WHITE, fg=app.TEXT_MAIN,
        font=("Segoe UI", 9, "bold")
    ).pack(side="left", padx=(0, 8))

    combo_tema = ttk.Combobox(
        fila_preset, values=list(PALETAS_USUARIO.keys()), state="readonly", width=24
    )
    combo_tema.set("Azul institucional")
    combo_tema.pack(side="left", padx=(0, 8))

    vista_previa = tk.Frame(
        parent, bg=valores["WHITE"], padx=14, pady=12,
        highlightthickness=1, highlightbackground=app.BORDER
    )
    lbl_vp_titulo = tk.Label(
        vista_previa, text="Vista previa del tema",
        bg=valores["WHITE"], fg=valores["TEXT_MAIN"], font=("Segoe UI", 10, "bold")
    )
    lbl_vp_titulo.pack(anchor="w")
    lbl_vp_btn = tk.Label(
        vista_previa, text="Botón y acento de ejemplo",
        bg=valores["PURPLE"], fg="#FFFFFF", padx=12, pady=6, font=("Segoe UI", 8, "bold")
    )
    lbl_vp_btn.pack(anchor="w", pady=(6, 0))

    def refrescar_muestras_y_previa():
        for _, k in campos_colores:
            col = valores[k]
            muestras[k].configure(text=col, bg=col)
        vista_previa.configure(bg=valores["WHITE"], highlightbackground=valores["PURPLE"])
        lbl_vp_titulo.configure(bg=valores["WHITE"], fg=valores["TEXT_MAIN"])
        lbl_vp_btn.configure(bg=valores["PURPLE"], fg="#FFFFFF")

    def aplicar_preset():
        paleta = PALETAS_USUARIO.get(combo_tema.get())
        if not paleta:
            return
        for k, v in paleta.items():
            if k in valores:
                valores[k] = v
        refrescar_muestras_y_previa()

    app.boton(fila_preset, "Cargar tema", aplicar_preset, app.PURPLE, "#FFFFFF", True).pack(side="left")

    for etiqueta, clave in campos_colores:
        fila = tk.Frame(parent, bg=app.WHITE)
        fila.pack(fill="x", pady=3)
        tk.Label(
            fila, text=etiqueta, bg=app.WHITE, fg=app.TEXT_MAIN,
            font=("Segoe UI", 9), width=24, anchor="w"
        ).pack(side="left")

        muestra = tk.Label(
            fila, text=valores[clave], bg=valores[clave],
            fg=app.TEXT_SOFT, width=12, relief="solid", bd=1, font=("Segoe UI", 8, "bold")
        )
        muestra.pack(side="right", padx=(8, 0))
        muestras[clave] = muestra

        def _elegir(k=clave):
            elegido = colorchooser.askcolor(color=valores[k], title=f"Elegir color · {k}")
            if elegido and elegido[1]:
                valores[k] = elegido[1]
                refrescar_muestras_y_previa()

        app.boton(fila, "Elegir", _elegir, app.DARK, app.TEXT_NAV, True).pack(side="right")

    vista_previa.pack(fill="x", pady=(10, 10))

    def guardar_y_aplicar():
        if guardar_preferencia_usuario_mysql(usuario_clave, valores):
            al_guardar_callback(valores)
            messagebox.showinfo("Tema guardado", f"Colores guardados en MySQL para '{usuario_clave}'.")

    def restablecer_predeterminado():
        base = TEMAS["oscuro"] if app.modo_oscuro else TEMAS["claro"]
        for k in valores:
            if k in base:
                valores[k] = base[k]
        refrescar_muestras_y_previa()
        if guardar_preferencia_usuario_mysql(usuario_clave, valores):
            al_guardar_callback(valores)

    barra_btn = tk.Frame(parent, bg=app.WHITE)
    barra_btn.pack(fill="x")
    app.boton(barra_btn, "Guardar y aplicar colores", guardar_y_aplicar, app.GOLD, "#FFFFFF", True).pack(side="left", padx=(0, 8))
    app.boton(barra_btn, "Restablecer por defecto", restablecer_predeterminado, app.BG, app.TEXT_MAIN, True).pack(side="left")


def parsear_filas_masivas(texto_csv, encabezados_esperados):
    """Parsea texto CSV (o pegado desde Excel/bloc) y omite la fila de encabezado si coincide."""
    limpio = texto_csv.strip()
    if not limpio:
        return []
    muestra = limpio.splitlines()[0]
    delimitador = ";" if muestra.count(";") > muestra.count(",") else ","
    lector = csv.reader(io.StringIO(limpio), delimiter=delimitador)
    filas = [[celda.strip() for celda in fila] for fila in lector if any(c.strip() for c in fila)]
    if not filas:
        return []
    primera_lower = [c.lower() for c in filas[0]]
    esperados_lower = [e.lower() for e in encabezados_esperados]
    if primera_lower == esperados_lower or (
        len(primera_lower) >= 2 and primera_lower[0] == esperados_lower[0] and primera_lower[1] == esperados_lower[1]
    ):
        filas = filas[1:]
    return filas


def abrir_modal_carga_masiva(parent_app, titulo, descripcion, columnas_csv, ejemplo_filas, callback_procesar):
    """Ventana modal reutilizable para importar registros en lote desde archivo CSV o texto pegado."""
    bg = parent_app.BG
    white = parent_app.WHITE
    navy = parent_app.NAVY
    gold = parent_app.GOLD
    dark = parent_app.DARK
    teal = parent_app.TEAL
    border = parent_app.BORDER
    fg_main = parent_app.TEXT_MAIN

    win = tk.Toplevel(parent_app.root)
    win.title(titulo)
    win.configure(bg=bg)
    win.transient(parent_app.root)
    win.grab_set()
    win.geometry("640x530")
    win.minsize(480, 400)

    franja = tk.Frame(win, bg=navy, padx=18, pady=12)
    franja.pack(fill="x")
    tk.Label(franja, text=titulo, bg=navy, fg=parent_app.TEXT_NAV, font=("Segoe UI", 13, "bold")).pack(anchor="w")
    tk.Label(franja, text=descripcion, bg=navy, fg=teal, font=("Segoe UI", 9)).pack(anchor="w", pady=(2, 0))
    tk.Frame(win, bg=gold, height=2).pack(fill="x")

    cuerpo = tk.Frame(win, bg=bg, padx=18, pady=14)
    cuerpo.pack(fill="both", expand=True)

    tk.Label(cuerpo, text=f"Columnas esperadas: {', '.join(columnas_csv)}",
             bg=bg, fg=fg_main, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 6))

    barra_arch = tk.Frame(cuerpo, bg=bg)
    barra_arch.pack(fill="x", pady=(0, 8))

    txt = tk.Text(cuerpo, height=11, font=("Consolas", 9), bg=white, fg=fg_main,
                  insertbackground=fg_main, relief="flat", highlightthickness=1,
                  highlightbackground=border, highlightcolor=parent_app.PURPLE, bd=0, padx=8, pady=8)
    txt.pack(fill="both", expand=True)

    texto_ejemplo = "\n".join([",".join(columnas_csv)] + [",".join(f) for f in ejemplo_filas])
    txt.insert("1.0", texto_ejemplo)

    def cargar_archivo():
        ruta = filedialog.askopenfilename(
            parent=win,
            title="Seleccionar archivo CSV",
            filetypes=[("Archivos CSV", "*.csv"), ("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if not ruta:
            return
        try:
            contenido = Path(ruta).read_text(encoding="utf-8-sig")
            txt.delete("1.0", "end")
            txt.insert("1.0", contenido)
        except OSError as e:
            messagebox.showerror("Error al leer archivo", str(e), parent=win)

    def descargar_plantilla():
        ruta = filedialog.asksaveasfilename(
            parent=win,
            title="Guardar plantilla CSV",
            defaultextension=".csv",
            initialfile="plantilla_carga_masiva.csv",
            filetypes=[("Archivos CSV", "*.csv")]
        )
        if not ruta:
            return
        try:
            with open(ruta, "w", newline="", encoding="utf-8-sig") as f:
                w = csv.writer(f)
                w.writerow(columnas_csv)
                w.writerows(ejemplo_filas)
            messagebox.showinfo("Plantilla guardada", f"Plantilla creada en:\n{ruta}", parent=win)
        except OSError as e:
            messagebox.showerror("Error al guardar", str(e), parent=win)

    parent_app.boton(barra_arch, "Cargar CSV", cargar_archivo, dark, parent_app.TEXT_NAV, True).pack(side="left", padx=(0, 8))
    parent_app.boton(barra_arch, "Descargar plantilla", descargar_plantilla, parent_app.BLUE_SOFT, parent_app.TEXT_SOFT, True).pack(side="left")

    pie = tk.Frame(win, bg=white, padx=18, pady=12, highlightbackground=border, highlightthickness=1)
    pie.pack(fill="x", side="bottom")

    def ejecutar():
        filas = parsear_filas_masivas(txt.get("1.0", "end"), columnas_csv)
        if not filas:
            messagebox.showwarning("Sin datos", "Agrega al menos una fila válida para importar.", parent=win)
            return
        resumen = callback_procesar(filas)
        if resumen is not None:
            win.destroy()

    parent_app.boton(pie, "Cancelar", win.destroy, bg, fg_main, True).pack(side="right", padx=(8, 0))
    parent_app.boton(pie, "Importar registros", ejecutar, gold, "#FFFFFF", True).pack(side="right")


def abrir_ventana_notificaciones(app, alumnos_lista, just_pendientes=0, inc_pendientes=0):
    """Abre ventana de notificaciones (enlazada al botón superior derecho de Notificaciones)."""
    win = tk.Toplevel(app.root)
    win.title("Notificaciones escolares")
    win.configure(bg=app.BG)
    win.transient(app.root)
    win.geometry("540x430")

    head = tk.Frame(win, bg=app.NAVY, padx=16, pady=12)
    head.pack(fill="x")
    tk.Label(head, text="Notificaciones", bg=app.NAVY, fg=app.TEXT_NAV, font=("Segoe UI", 13, "bold")).pack(anchor="w")
    tk.Label(head, text="Avisos pendientes, faltas y retardos constantes", bg=app.NAVY, fg=app.TEAL, font=("Segoe UI", 8)).pack(anchor="w")

    body = tk.Frame(win, bg=app.BG, padx=16, pady=14)
    body.pack(fill="both", expand=True)

    avisos = []
    if just_pendientes:
        avisos.append((f"{just_pendientes} justificante(s) pendiente(s) por validar.", app.BLUE_SOFT))
    if inc_pendientes:
        avisos.append((f"{inc_pendientes} incidencia(s) pendiente(s) de seguimiento.", app.RED_SOFT))

    constantes = [a for a in alumnos_lista if int(a[3]) > 0 or int(a[4]) > 0]
    for _, nombre, grupo, ret, fal in sorted(constantes, key=lambda x: (-int(x[4]), -int(x[3]), x[1]))[:8]:
        ret_i, fal_i = int(ret), int(fal)
        eq_i = ret_i // UMBRAL_FALTAS
        color = app.RED_SOFT if fal_i >= UMBRAL_FALTAS or eq_i > 0 else app.YELLOW_SOFT
        avisos.append((
            f"{nombre} ({grupo}) — {fal_i} falta(s), {ret_i} retardo(s) [Equiv.: +{eq_i} falta(s)]",
            color
        ))

    if not avisos:
        avisos.append(("Sin notificaciones pendientes por el momento.", app.GREEN_SOFT))

    for texto_aviso, bg_aviso in avisos:
        tk.Label(
            body, text=texto_aviso, bg=bg_aviso, fg=app.TEXT_SOFT,
            font=("Segoe UI", 8, "bold"), anchor="w", justify="left",
            padx=10, pady=7
        ).pack(fill="x", pady=3)


class PanelDireccion:
    def __init__(self, root, modo_oscuro=False, colores_personalizados=None):
        self.root = root
        self.modo_oscuro = modo_oscuro
        self.colores_personalizados = colores_personalizados
        self.actualizar_colores()

        hoy_dt = date.today()
        self.cal_anio = hoy_dt.year
        self.cal_mes = hoy_dt.month

        self.root.title("Primaria Nezahualcóyotl | Dirección y Docentes")
        self.root.minsize(320, 480)
        self.root.configure(bg=self.BG)
        maximizar_ventana(self.root)
        self.pagina = "Inicio"
        self.compacto = False
        self._resize_job = None
        inicializar_base_datos_principal()
        self.configurar_estilos()
        self.root.bind("<Configure>", self.detectar_tamano)
        self.pantalla_login()

    def actualizar_colores(self):
        t = dict(TEMAS["oscuro"] if self.modo_oscuro else TEMAS["claro"])
        if isinstance(self.colores_personalizados, dict):
            t.update(self.colores_personalizados)
        self.BG = t["BG"]
        self.WHITE = t["WHITE"]
        self.NAVY = t["NAVY"]
        self.DARK = t["DARK"]
        self.PURPLE = t["PURPLE"]
        self.GOLD = t["GOLD"]
        self.GOLD_LIGHT = t.get("GOLD_LIGHT", t["GREEN_SOFT"])
        self.GOLD_DARK = t.get("GOLD_DARK", t["GOLD"])
        self.LAVENDER = t["LAVENDER"]
        self.MUTED = t["MUTED"]
        self.BORDER = t["BORDER"]
        self.BLUE_SOFT = t["BLUE_SOFT"]
        self.GREEN_SOFT = t["GREEN_SOFT"]
        self.YELLOW_SOFT = t["YELLOW_SOFT"]
        self.RED_SOFT = t["RED_SOFT"]
        self.RED = t["RED"]
        self.RED_DARK = t["RED_DARK"]
        self.TEAL = t["TEAL"]
        self.TEXT_NAV = t["TEXT_NAV"]
        self.TEXT_MAIN = t["TEXT_MAIN"]
        self.TEXT_SOFT = t["TEXT_SOFT"]

    def cambiar_tema(self):
        self.modo_oscuro = not self.modo_oscuro
        self.colores_personalizados = None
        self.actualizar_colores()
        self.configurar_estilos()
        self.crear_panel(self.pagina)

    def conectar(self, incluir_bd=True):
        return conectar_mysql(incluir_bd=incluir_bd)

    def configurar_estilos(self):
        s = ttk.Style()
        try:
            s.theme_use("clam")
        except tk.TclError:
            pass

        fg_tabla = self.TEXT_MAIN
        bg_tabla = self.WHITE
        header_bg = self.DARK if self.modo_oscuro else "#F8FAFC"
        header_fg = self.TEAL if self.modo_oscuro else "#334155"

        s.configure("Treeview", background=bg_tabla, foreground=fg_tabla,
                    fieldbackground=bg_tabla, rowheight=34, borderwidth=0, font=("Segoe UI", 9))
        s.configure("Treeview.Heading", background=header_bg, foreground=header_fg,
                    font=("Segoe UI", 9, "bold"), padding=(8, 8), relief="flat")
        s.map("Treeview", background=[("selected", self.PURPLE)],
              foreground=[("selected", "#FFFFFF")])

        s.configure("TCombobox", padding=6, font=("Segoe UI", 9),
                    fieldbackground=bg_tabla, background=header_bg,
                    foreground=fg_tabla, arrowcolor=fg_tabla)
        s.map("TCombobox",
              fieldbackground=[("readonly", bg_tabla)],
              foreground=[("readonly", fg_tabla)],
              selectbackground=[("readonly", self.PURPLE)],
              selectforeground=[("readonly", "#FFFFFF")])
        self.root.option_add("*TCombobox*Listbox.background", bg_tabla)
        self.root.option_add("*TCombobox*Listbox.foreground", fg_tabla)
        self.root.option_add("*TCombobox*Listbox.selectBackground", self.PURPLE)
        self.root.option_add("*TCombobox*Listbox.selectForeground", "#FFFFFF")

        s.configure("TNotebook", background=self.BG, borderwidth=0, tabmargins=[0, 4, 0, 0])
        s.configure("TNotebook.Tab", background=self.WHITE, foreground=self.TEXT_MAIN,
                    font=("Segoe UI", 9, "bold"), padding=(14, 7), borderwidth=1)
        s.map("TNotebook.Tab",
              background=[("selected", self.PURPLE), ("active", self.LAVENDER)],
              foreground=[("selected", "#FFFFFF"), ("active", self.TEXT_MAIN)])

        s.configure("Vertical.TScrollbar", background=self.DARK if self.modo_oscuro else self.BORDER,
                    troughcolor=self.BG, borderwidth=0)
        s.configure("Horizontal.TScrollbar", background=self.DARK if self.modo_oscuro else self.BORDER,
                    troughcolor=self.BG, borderwidth=0)

        self.root.option_add("*Entry.background", bg_tabla)
        self.root.option_add("*Entry.foreground", fg_tabla)
        self.root.option_add("*Entry.insertBackground", fg_tabla)
        self.root.option_add("*Entry.highlightBackground", self.BORDER)
        self.root.option_add("*Entry.highlightColor", self.PURPLE)

    def boton(self, parent, texto, comando, color=None, fg=None, compacto=True):
        col = color if color else self.PURPLE
        texto_col = fg if fg else "#FFFFFF"
        b = tk.Button(parent, text=texto, command=comando, bg=col, fg=texto_col,
                      activebackground=self.DARK, activeforeground="#FFFFFF",
                      font=("Segoe UI", 8 if compacto else 9, "bold"),
                      bd=0, padx=11, pady=6 if compacto else 8,
                      cursor="hand2", wraplength=220, relief="flat",
                      highlightthickness=0)
        return b

    def formulario_modal(self, titulo, campos):
        ventana = tk.Toplevel(self.root)
        ventana.title(titulo)
        ventana.configure(bg=self.BG)
        ventana.transient(self.root)
        ventana.grab_set()
        ventana.resizable(True, False)
        ventana.geometry("430x{}".format(min(580, 210 + len(campos) * 72)))

        franja = tk.Frame(ventana, bg=self.NAVY, padx=18, pady=12)
        franja.pack(fill="x")
        tk.Label(franja, text=titulo, bg=self.NAVY, fg=self.TEXT_NAV,
                 font=("Segoe UI", 12, "bold"), wraplength=370,
                 justify="left").pack(anchor="w")
        tk.Frame(ventana, bg=self.PURPLE, height=2).pack(fill="x")

        cuerpo = tk.Frame(ventana, bg=self.BG, padx=18, pady=14)
        cuerpo.pack(fill="both", expand=True)
        controles = {}
        for indice, campo in enumerate(campos):
            etiqueta, valor, opciones = campo
            fg_label = self.TEXT_MAIN
            tk.Label(cuerpo, text=etiqueta, bg=self.BG, fg=fg_label,
                     font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(6 if indice else 0, 3))
            if opciones:
                control = ttk.Combobox(cuerpo, values=opciones, state="readonly", font=("Segoe UI", 9))
                if valor is not None:
                    control.set(str(valor))
            else:
                control = tk.Entry(cuerpo, font=("Segoe UI", 10), bg=self.WHITE,
                                   fg=fg_label, insertbackground=fg_label,
                                   relief="flat", highlightthickness=1,
                                   highlightbackground=self.BORDER, highlightcolor=self.PURPLE, bd=0)
                if valor is not None:
                    control.insert(0, str(valor))
            control.pack(fill="x", ipady=6, pady=(0, 4))
            controles[etiqueta] = control

        pie = tk.Frame(ventana, bg=self.WHITE, padx=18, pady=11,
                       highlightbackground=self.BORDER, highlightthickness=1)
        pie.pack(fill="x", side="bottom")
        resultado = {"valores": None}

        def guardar(event=None):
            valores = {nombre: control.get().strip() for nombre, control in controles.items()}
            if any(not valor for valor in valores.values()):
                messagebox.showwarning("Incompletos", "Completa todos los campos.", parent=ventana)
                return
            resultado["valores"] = valores
            ventana.destroy()

        def cancelar():
            ventana.destroy()

        self.boton(pie, "Cancelar", cancelar, self.BG, self.TEXT_MAIN, True).pack(side="right", padx=(8, 0))
        self.boton(pie, "Guardar", guardar, self.GOLD, "#FFFFFF", True).pack(side="right")
        ventana.bind("<Return>", guardar)
        ventana.bind("<Escape>", lambda e: cancelar())
        ventana.update_idletasks()
        x = self.root.winfo_rootx() + (self.root.winfo_width() - ventana.winfo_width()) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - ventana.winfo_height()) // 2
        ventana.geometry(f"+{max(0, x)}+{max(0, y)}")
        ventana.wait_window()
        return resultado["valores"]

    def limpiar_raiz(self):
        for w in self.root.winfo_children():
            w.destroy()

    def detectar_tamano(self, event):
        if event.widget is not self.root:
            return
        compacto = event.width < 930
        if compacto != self.compacto:
            self.compacto = compacto
            if self._resize_job:
                self.root.after_cancel(self._resize_job)
            self._resize_job = self.root.after(100, self.reconstruir_panel)

    def reconstruir_panel(self):
        if not hasattr(self, "contenido") or not self.contenido.winfo_exists():
            return
        pagina = self.pagina
        self.crear_panel(pagina)

    def pantalla_login(self):
        self.limpiar_raiz()
        maximizar_ventana(self.root)
        outer = tk.Frame(self.root, bg=self.BG)
        outer.pack(fill="both", expand=True)

        caja = tk.Frame(outer, bg=self.WHITE, padx=34, pady=30,
                        highlightbackground=self.BORDER, highlightthickness=1)
        caja.place(relx=.5, rely=.5, anchor="center", width=410)

        tk.Frame(caja, bg=self.PURPLE, height=4).pack(fill="x", pady=(0, 18))

        fg_caja = self.TEXT_MAIN
        tk.Label(caja, text="PRIMARIA NEZAHUALCÓYOTL", bg=self.WHITE, fg=self.PURPLE,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w")
        tk.Label(caja, text="Iniciar sesión", bg=self.WHITE, fg=fg_caja,
                 font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(2, 2))
        tk.Label(caja, text="Control escolar, asistencia y seguimiento",
                 bg=self.WHITE, fg=self.MUTED, font=("Segoe UI", 9)).pack(anchor="w", pady=(0, 14))

        btn_tema_txt = "Modo Oscuro" if not self.modo_oscuro else "Modo Claro"
        self.boton(caja, btn_tema_txt, self.cambiar_tema_login, self.BG, fg_caja, True).pack(anchor="e", pady=(0, 10))

        tk.Label(caja, text="Usuario o docente", bg=self.WHITE, fg=fg_caja, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 3))
        usuario = tk.Entry(caja, font=("Segoe UI", 10), bg=self.WHITE, fg=fg_caja,
                           relief="flat", highlightthickness=1, highlightbackground=self.BORDER,
                           highlightcolor=self.PURPLE, bd=0)
        usuario.pack(fill="x", ipady=7, pady=(0, 12))
        usuario.insert(0, "Anabel")

        tk.Label(caja, text="Contraseña", bg=self.WHITE, fg=fg_caja, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 3))
        clave = tk.Entry(caja, show="•", font=("Segoe UI", 10), bg=self.WHITE, fg=fg_caja,
                         relief="flat", highlightthickness=1, highlightbackground=self.BORDER,
                         highlightcolor=self.PURPLE, bd=0)
        clave.pack(fill="x", ipady=7, pady=(0, 16))

        def entrar(event=None):
            user = usuario.get().strip()
            passw = clave.get().strip()
            if user.lower() == "director" and passw == "1234":
                self.colores_personalizados = cargar_preferencia_usuario_mysql("director")
                self.actualizar_colores()
                self.configurar_estilos()
                self.crear_panel()
                return

            acceso_docente = None
            try:
                with self.conectar(incluir_bd=True) as db:
                    cur = db.cursor()
                    acceso_docente = validar_acceso_docente(cur, user, passw)
            except MySQLError:
                pass

            if acceso_docente:
                nombre_docente, grupo_asignado = acceso_docente
                colores_doc = cargar_preferencia_usuario_mysql(nombre_docente)
                self.limpiar_raiz()
                PanelDocente(
                    self.root, nombre_docente, self.modo_oscuro,
                    grupo_fijo=grupo_asignado, colores_personalizados=colores_doc
                )
            else:
                messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos.")

        self.boton(caja, "Entrar al sistema", entrar, self.PURPLE, "#FFFFFF", False).pack(fill="x")
        clave.bind("<Return>", entrar)
        usuario.focus_set()

    def cambiar_tema_login(self):
        self.modo_oscuro = not self.modo_oscuro
        self.colores_personalizados = None
        self.actualizar_colores()
        self.configurar_estilos()
        self.pantalla_login()

    def cerrar_sesion(self):
        if messagebox.askyesno("Cerrar sesión", "¿Deseas salir al inicio de sesión?"):
            self.pantalla_login()

    def crear_panel(self, pagina="Inicio"):
        self.pagina = pagina
        self.limpiar_raiz()
        maximizar_ventana(self.root)

        menu_width = 64 if self.compacto else 210
        self.menu = tk.Frame(self.root, bg=self.NAVY, width=menu_width)
        self.menu.pack(side="left", fill="y")
        self.menu.pack_propagate(False)

        if self.compacto:
            tk.Label(self.menu, text="PN", bg=self.PURPLE, fg="#FFFFFF",
                     font=("Segoe UI", 10, "bold"), pady=8).pack(fill="x", padx=8, pady=12)
        else:
            brand = tk.Frame(self.menu, bg=self.NAVY, padx=14, pady=16)
            brand.pack(fill="x")
            tk.Label(brand, text="PRIMARIA", bg=self.NAVY, fg=self.TEAL,
                     font=("Segoe UI", 8, "bold")).pack(anchor="w")
            tk.Label(brand, text="Nezahualcóyotl", bg=self.NAVY, fg=self.TEXT_NAV,
                     font=("Segoe UI", 13, "bold")).pack(anchor="w")
            tk.Label(brand, text="Rol: Dirección Escolar", bg=self.NAVY, fg=self.MUTED,
                     font=("Segoe UI", 8)).pack(anchor="w", pady=(4, 0))

        tk.Frame(self.menu, bg=self.DARK, height=1).pack(fill="x", padx=12, pady=(0, 8))

        if not self.compacto:
            tk.Label(self.menu, text="SECCIONES", bg=self.NAVY, fg=self.MUTED,
                     font=("Segoe UI", 7, "bold")).pack(anchor="w", padx=14, pady=(2, 4))

        nav = [
            ("⌂", "Inicio"),
            ("▦", "Grupos y Docentes"),
            ("✉", "Comunicados Oficiales"),
            ("📖", "Bitácora Directiva"),
            ("▦", "Calendario Oficial"),
            ("!", "Conducta / Incidencias"),
            ("◇", "Cartas Compromiso"),
            ("⚑", "Módulo de Alertas"),
            ("▥", "Reportes Periódicos"),
            ("⚙", "Configuración")]

        for icon, label in nav:
            activa = self.pagina == label
            fila_nav = tk.Frame(self.menu, bg=self.DARK if activa else self.NAVY)
            fila_nav.pack(fill="x", padx=8, pady=1)
            if activa:
                tk.Frame(fila_nav, bg=self.GOLD, width=3).pack(side="left", fill="y")
            txt = icon if self.compacto else f"{icon}  {label}"
            tk.Button(
                fila_nav,
                text=txt,
                command=lambda p=label: self.mostrar(p),
                bg=self.DARK if activa else self.NAVY,
                fg="#FFFFFF" if activa else self.TEXT_NAV,
                activebackground=self.DARK,
                activeforeground="#FFFFFF",
                font=("Segoe UI", 9, "bold" if activa else "normal"),
                bd=0,
                padx=8,
                pady=6,
                anchor="w" if not self.compacto else "center",
                cursor="hand2",
                relief="flat"
            ).pack(side="left", fill="both", expand=True)

        tk.Frame(self.menu, bg=self.NAVY).pack(fill="both", expand=True)
        tk.Frame(self.menu, bg=self.DARK, height=1).pack(fill="x", padx=10, pady=(0, 6))
        self.boton(self.menu, "⇦" if self.compacto else "Cerrar sesión",
                   self.cerrar_sesion, self.DARK, self.TEXT_NAV, True).pack(fill="x", padx=8, pady=(0, 10))

        right_col = tk.Frame(self.root, bg=self.BG)
        right_col.pack(side="left", fill="both", expand=True)

        top = tk.Frame(right_col, bg=self.WHITE, padx=18, pady=10,
                       highlightbackground=self.BORDER, highlightthickness=1)
        top.pack(fill="x")

        btn_tema_txt = "Modo Oscuro" if not self.modo_oscuro else "Modo Claro"
        self.boton(top, btn_tema_txt, self.cambiar_tema, self.BG, self.TEXT_MAIN, True).pack(side="right", padx=(8, 0))
        self.boton(top, "Notificaciones", self._abrir_notificaciones_dir, self.LAVENDER, self.TEXT_SOFT, True).pack(side="right", padx=(8, 0))
        tk.Label(top, text=date.today().strftime("%d/%m/%Y"),
                 bg=self.WHITE, fg=self.MUTED, font=("Segoe UI", 9, "bold")).pack(side="right", padx=8)

        self.lbl_top_seccion = tk.Label(top, text=pagina, bg=self.WHITE, fg=self.TEXT_MAIN,
                                        font=("Segoe UI", 14, "bold"))
        self.lbl_top_seccion.pack(anchor="w")
        self.lbl_top_sub = tk.Label(top, text="Resumen general de la actividad escolar",
                                    bg=self.WHITE, fg=self.MUTED, font=("Segoe UI", 8))
        self.lbl_top_sub.pack(anchor="w")

        quick_bar = tk.Frame(right_col, bg=self.WHITE, padx=18, pady=6,
                             highlightbackground=self.BORDER, highlightthickness=1)
        quick_bar.pack(fill="x")
        tk.Label(quick_bar, text="Rápido:", bg=self.WHITE, fg=self.MUTED,
                 font=("Segoe UI", 8, "bold")).pack(side="left", padx=(0, 8))
        for q_txt, q_dest in [
            ("Inicio", "Inicio"),
            ("Grupos", "Grupos y Docentes"),
            ("Alertas", "Módulo de Alertas"),
            ("Comunicados", "Comunicados Oficiales"),
            ("Reportes", "Reportes Periódicos"),
        ]:
            es_act = self.pagina == q_dest
            self.boton(
                quick_bar,
                q_txt,
                lambda p=q_dest: self.mostrar(p),
                self.PURPLE if es_act else self.BG,
                "#FFFFFF" if es_act else self.TEXT_MAIN,
                True
            ).pack(side="left", padx=(0, 6))

        area = tk.Frame(right_col, bg=self.BG)
        area.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(area, bg=self.BG, highlightthickness=0)
        scroll = ttk.Scrollbar(area, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.contenido = tk.Frame(self.canvas, bg=self.BG)
        self.window_id = self.canvas.create_window((0, 0), window=self.contenido, anchor="nw")
        self.contenido.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self.window_id, width=e.width))
        self.mostrar(pagina)

    def _abrir_notificaciones_dir(self):
        abrir_ventana_notificaciones(
            self,
            self.obtener_alumnos(),
            just_pendientes=self.contar_justificantes(),
            inc_pendientes=self.contar_incidencias()
        )

    def titulo(self, texto, subtitulo="Resumen general de la actividad escolar"):
        if hasattr(self, "lbl_top_seccion") and self.lbl_top_seccion.winfo_exists():
            self.lbl_top_seccion.configure(text=texto)
        if hasattr(self, "lbl_top_sub") and self.lbl_top_sub.winfo_exists():
            self.lbl_top_sub.configure(text=subtitulo)

    def seccion(self, parent, texto):
        fg_sec = self.TEXT_MAIN
        outer = tk.Frame(parent, bg=self.WHITE, highlightbackground=self.BORDER, highlightthickness=1)
        head = tk.Frame(outer, bg=self.WHITE, padx=14, pady=10)
        head.pack(fill="x")
        tk.Frame(head, bg=self.PURPLE, width=4, height=16).pack(side="left", padx=(0, 8))
        tk.Label(head, text=texto, bg=self.WHITE, fg=fg_sec, font=("Segoe UI", 10, "bold")).pack(side="left")
        tk.Frame(outer, bg=self.BORDER, height=1).pack(fill="x")
        inner = tk.Frame(outer, bg=self.WHITE, padx=14, pady=12)
        inner.pack(fill="both", expand=True)
        outer.body = inner
        return outer

    def tarjeta(self, parent, nombre, valor, detalle, color, comando=None):
        card = tk.Frame(parent, bg=self.WHITE,
                        highlightbackground=self.BORDER, highlightthickness=1,
                        cursor="hand2" if comando else "")
        tk.Frame(card, bg=color, width=4).pack(side="left", fill="y")
        body = tk.Frame(card, bg=self.WHITE, padx=12, pady=10,
                        cursor="hand2" if comando else "")
        body.pack(side="left", fill="both", expand=True)
        fg_card = self.TEXT_MAIN
        lbl_nom = tk.Label(body, text=nombre.upper(), bg=self.WHITE, fg=self.MUTED,
                           font=("Segoe UI", 7, "bold"), wraplength=150, justify="left",
                           cursor="hand2" if comando else "")
        lbl_nom.pack(anchor="w")
        lbl_val = tk.Label(body, text=str(valor), bg=self.WHITE, fg=fg_card,
                           font=("Segoe UI", 19, "bold"),
                           cursor="hand2" if comando else "")
        lbl_val.pack(anchor="w", pady=(2, 2))
        lbl_det = tk.Label(body, text=detalle, bg=self.WHITE, fg=self.MUTED,
                           font=("Segoe UI", 8), wraplength=160, justify="left",
                           cursor="hand2" if comando else "")
        lbl_det.pack(anchor="w")

        if comando:
            widgets_clic = [card, body, lbl_nom, lbl_val, lbl_det]
            for w in widgets_clic:
                w.bind("<Button-1>", lambda e, fn=comando: fn())
                w.bind("<Enter>", lambda e, ws=widgets_clic: [x.configure(bg=self.LAVENDER) for x in ws])
                w.bind("<Leave>", lambda e, ws=widgets_clic: [x.configure(bg=self.WHITE) for x in ws])
        return card

    def abrir_vista_kpi(self, filtro_kpi):
        """Muestra una pestaña/vista específica al hacer clic en un KPI sin añadirla a la barra lateral."""
        if filtro_kpi == "Incidencias":
            self.mostrar("Conducta / Incidencias")
            return
        if filtro_kpi == "Justificantes":
            self.mostrar("Módulo de Alertas")
            return

        self.pagina = f"KPI · {filtro_kpi}"
        for w in self.contenido.winfo_children():
            w.destroy()
        self.canvas.yview_moveto(0)

        titulos_kpi = {
            "Alumnos": ("Detalle · Alumnos registrados", "Listado general de expedientes escolares"),
            "Presentes": ("Detalle · Alumnos presentes / regulares", "Alumnos sin faltas ni retardos acumulados o presentes hoy"),
            "Retardos": ("Detalle · Alumnos con retardos", "Criterio institucional: 3 retardos = 1 falta"),
            "Faltas": ("Detalle · Alumnos con faltas", "Faltas registradas y equivalentes por retardos (3 ret. = 1 falta)"),
        }
        tit, sub = titulos_kpi.get(filtro_kpi, (f"Detalle · {filtro_kpi}", "Consulta de indicadores"))
        self.titulo(tit, sub)

        barra = tk.Frame(self.contenido, bg=self.BG)
        barra.pack(fill="x", padx=18, pady=(14, 6))
        self.boton(barra, "← Volver a Inicio", lambda: self.mostrar("Inicio"), self.PURPLE, "#FFFFFF").pack(side="left")

        sec = self.seccion(self.contenido, tit)
        sec.pack(fill="both", expand=True, padx=18, pady=6)

        with self.conectar(incluir_bd=True) as db:
            cur = db.cursor()
            cur.execute("SELECT alumno_id FROM asistencias WHERE fecha=%s AND estado='Presente'", (date.today().isoformat(),))
            presentes_hoy = {r[0] for r in cur.fetchall()}

        alumnos = self.obtener_alumnos()
        filas = []
        for ident, nombre, grupo, ret, fal in alumnos:
            ret_i, fal_i = int(ret), int(fal)
            eq_fal = ret_i // UMBRAL_FALTAS
            total_fal = fal_i + eq_fal
            es_presente = ident in presentes_hoy or (ret_i == 0 and fal_i == 0)

            incluir = False
            estado = "Regular"
            if filtro_kpi == "Alumnos":
                incluir = True
                estado = "Faltas" if total_fal > 0 else ("Retardos" if ret_i > 0 else "Presente")
            elif filtro_kpi == "Presentes" and es_presente:
                incluir = True
                estado = "Presente"
            elif filtro_kpi == "Retardos" and ret_i > 0:
                incluir = True
                estado = f"Retardos (eq. +{eq_fal})"
            elif filtro_kpi == "Faltas" and total_fal > 0:
                incluir = True
                estado = f"Faltas ({fal_i} reg. + {eq_fal} eq.)"

            if incluir:
                filas.append((ident, nombre, grupo, ret_i, fal_i, total_fal, estado))

        self.crear_tabla(
            sec.body,
            ("ID", "Alumno", "Grupo", "Retardos", "Faltas Reg.", "Total Faltas", "Detalle"),
            filas,
            {"Alumno": 190, "Detalle": 160},
            10
        )

    def mostrar(self, pagina):
        self.pagina = pagina
        for w in self.contenido.winfo_children():
            w.destroy()
        self.canvas.yview_moveto(0)
        subtitulos = {
            "Inicio": "Resumen general de la actividad escolar",
            "Grupos y Docentes": "Organización académica y personal docente por grupo",
            "Comunicados Oficiales": "Envío y visualización de avisos a la comunidad",
            "Bitácora Directiva": "Registro diario de incidencias y acuerdos institucionales",
            "Calendario Oficial": "Organización de fechas y eventos escolares",
            "Conducta / Incidencias": "Registro de conducta e incidencias de alumnos",
            "Cartas Compromiso": "Acuerdos y cartas compromiso con alumnos y tutores",
            "Módulo de Alertas": "Alertas de asistencia, faltas, retardos y justificantes",
            "Reportes Periódicos": "Consulta y exportación de información",
            "Configuración": "Parámetros y estado del sistema"}
        self.titulo(pagina, subtitulos.get(pagina, "Gestión escolar"))
        rutas = {
            "Inicio": self.pagina_inicio,
            "Grupos y Docentes": self.pagina_grupos,
            "Comunicados Oficiales": self.pagina_comunicados,
            "Bitácora Directiva": self.pagina_bitacora,
            "Calendario Oficial": self.pagina_calendario,
            "Conducta / Incidencias": self.pagina_conducta,
            "Cartas Compromiso": self.pagina_cartas_compromiso,
            "Módulo de Alertas": self.pagina_alertas,
            "Reportes Periódicos": self.pagina_reportes,
            "Configuración": self.pagina_configuracion}
        rutas.get(pagina, self.pagina_inicio)()

    def obtener_metricas(self):
        with self.conectar(incluir_bd=True) as db:
            cur = db.cursor()
            cur.execute("SELECT nombre, valor FROM metricas")
            data = dict(cur.fetchall())
            cur.execute("SELECT COUNT(*) FROM alumnos")
            total = cur.fetchone()[0]
            if total:
                data["Alumnos"] = total
            return data

    def obtener_alumnos(self):
        with self.conectar(incluir_bd=True) as db:
            cur = db.cursor()
            cur.execute("SELECT id, nombre, grupo, retardos, faltas FROM alumnos ORDER BY grupo, nombre")
            return cur.fetchall()

    def obtener_grupos(self):
        with self.conectar(incluir_bd=True) as db:
            cur = db.cursor()
            cur.execute("SELECT id, grupo, docente, alumnos FROM grupos ORDER BY grupo")
            return cur.fetchall()

    def contar_justificantes(self):
        with self.conectar(incluir_bd=True) as db:
            cur = db.cursor()
            cur.execute("SELECT COUNT(*) FROM justificantes WHERE estado='Pendiente'")
            return cur.fetchone()[0]

    def contar_incidencias(self):
        with self.conectar(incluir_bd=True) as db:
            cur = db.cursor()
            cur.execute("SELECT COUNT(*) FROM incidencias WHERE estado='Pendiente'")
            return cur.fetchone()[0]

    def pagina_inicio(self):
        m = self.obtener_metricas()
        total = m.get("Alumnos", 0)
        presentes = m.get("Presentes", 0)
        retardos = m.get("Retardos", 0)
        faltas = m.get("Faltas", 0)
        pendientes = self.contar_justificantes()
        incidencias = self.contar_incidencias()

        banner = tk.Frame(self.contenido, bg=self.NAVY, padx=18, pady=12,
                          highlightbackground=self.BORDER, highlightthickness=1)
        banner.pack(fill="x", padx=18, pady=(12, 8))
        tk.Label(banner, text="CENTRO DE CONTROL ESCOLAR", bg=self.NAVY,
                 fg=self.TEAL, font=("Segoe UI", 8, "bold")).pack(anchor="w")
        tk.Label(banner, text="Monitoreo en tiempo real de asistencia, avisos y disciplina.",
                 bg=self.NAVY, fg=self.TEXT_NAV, font=("Segoe UI", 11, "bold"),
                 wraplength=540, justify="left").pack(anchor="w", pady=(2, 0))

        wrap = tk.Frame(self.contenido, bg=self.BG)
        wrap.pack(fill="x", padx=14)
        values = [
            ("Alumnos", total, "Expedientes registrados", self.PURPLE, lambda: self.abrir_vista_kpi("Alumnos")),
            ("Presentes", presentes, f"{presentes / total * 100:.1f}% asistencia" if total else "Sin registros", self.GOLD, lambda: self.abrir_vista_kpi("Presentes")),
            ("Retardos", retardos, "Registrados hoy", self.TEAL, lambda: self.abrir_vista_kpi("Retardos")),
            ("Faltas", faltas, "Registradas hoy", self.RED, lambda: self.abrir_vista_kpi("Faltas")),
            ("Incidencias", incidencias, "Casos pendientes", self.RED_DARK, lambda: self.abrir_vista_kpi("Incidencias")),
            ("Justificantes", pendientes, "Por validar", self.PURPLE, lambda: self.abrir_vista_kpi("Justificantes"))]
        for i, val in enumerate(values):
            card = self.tarjeta(wrap, *val)
            card.grid(row=i // 3, column=i % 3, sticky="nsew", padx=4, pady=4)
            wrap.grid_columnconfigure(i % 3, weight=1, uniform="cards")

        bottom = tk.Frame(self.contenido, bg=self.BG)
        bottom.pack(fill="both", expand=True, padx=18, pady=8)
        left = tk.Frame(bottom, bg=self.BG)
        right = tk.Frame(bottom, bg=self.BG)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        right.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
        bottom.grid_columnconfigure(0, weight=3)
        bottom.grid_columnconfigure(1, weight=2)

        sec_sum = self.seccion(left, "Estado de Asistencia (Hoy)")
        sec_sum.pack(fill="x", pady=(0, 8))
        summary = sec_sum.body
        fg_lbl = self.TEXT_MAIN

        max_val = max(total, 1)
        for label, number, color in [
            ("Presentes", presentes, self.GOLD),
            ("Retardos", retardos, self.TEAL),
            ("Faltas", faltas, self.RED)]:
            line = tk.Frame(summary, bg=self.WHITE)
            line.pack(fill="x", pady=3)
            tk.Label(line, text=label, bg=self.WHITE, fg=fg_lbl, font=("Segoe UI", 8, "bold"), width=10, anchor="w").pack(side="left")
            tk.Label(line, text=str(number), bg=self.WHITE, fg=color, font=("Segoe UI", 9, "bold"), width=5).pack(side="right")

            barbg = tk.Frame(summary, bg=self.BORDER, height=10)
            barbg.pack(fill="x", pady=(0, 6))
            bar = tk.Frame(barbg, bg=color, height=10)
            bar.place(relx=0, rely=0, relheight=1, relwidth=min(number / max_val, 1))

        sec_quick = self.seccion(left, "Accesos rápidos")
        sec_quick.pack(fill="x")
        quick = sec_quick.body
        for label, dest in [("Enviar comunicado", "Comunicados Oficiales"),
                            ("Bitácora directiva", "Bitácora Directiva"),
                            ("Generar reporte", "Reportes Periódicos")]:
            self.boton(quick, label, lambda p=dest: self.mostrar(p),
                       self.LAVENDER, self.TEXT_SOFT, True).pack(fill="x", pady=2)

        sec_alt = self.seccion(right, "Atención directiva")
        sec_alt.pack(fill="both", expand=True, pady=(0, 8))
        self.resumen_alertas(sec_alt.body, limite=3)

        sec_rule = self.seccion(right, "Criterio institucional")
        sec_rule.pack(fill="x")
        tk.Label(sec_rule.body, text="3 retardos equivalen a 1 falta adicional automática.",
                 bg=self.GREEN_SOFT, fg=self.TEXT_SOFT, font=("Segoe UI", 8, "bold"),
                 wraplength=260, justify="left", padx=10, pady=8).pack(fill="x")

    def crear_tabla(self, parent, columnas, filas, anchos=None, height=7):
        frame = tk.Frame(parent, bg=self.WHITE, highlightbackground=self.BORDER, highlightthickness=1)
        frame.pack(fill="both", expand=True)
        tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=height)
        vs = ttk.Scrollbar(frame, orient="vertical", command=tabla.yview)
        hs = ttk.Scrollbar(frame, orient="horizontal", command=tabla.xview)
        tabla.configure(yscrollcommand=vs.set, xscrollcommand=hs.set)
        vs.pack(side="right", fill="y")
        hs.pack(side="bottom", fill="x")
        tabla.pack(side="left", fill="both", expand=True)
        for col in columnas:
            tabla.heading(col, text=col)
            ancho = (anchos or {}).get(col, 100)
            tabla.column(col, width=ancho, minwidth=40, anchor="w" if col in ("Alumno", "Docente", "Motivo", "Descripción", "Nota", "Título", "Mensaje", "Entrada", "Asunto") else "center", stretch=True)
        for fila in filas:
            tabla.insert("", "end", values=fila)
        return tabla

    def pagina_grupos(self):
        sec = self.seccion(self.contenido, "Grupos y docentes")
        sec.pack(fill="both", expand=True, padx=18, pady=(14, 6))
        box = sec.body

        actions = tk.Frame(box, bg=self.WHITE)
        actions.pack(fill="x", pady=(0, 10))
        self.boton(actions, "＋ Agregar grupo", self.agregar_grupo, self.GOLD, "#FFFFFF").pack(side="left", padx=(0, 6))
        self.boton(actions, "Editar grupo", self.editar_grupo, self.DARK, self.TEXT_NAV).pack(side="left", padx=(0, 6))
        self.boton(actions, "⬆ Carga masiva grupos", self.carga_masiva_grupos, self.PURPLE, "#FFFFFF").pack(side="left", padx=(0, 6))
        self.boton(actions, "⬆ Carga masiva alumnos", self.carga_masiva_alumnos, self.TEAL, "#FFFFFF").pack(side="left", padx=(0, 6))
        self.boton(actions, "Actualizar", lambda: self.mostrar("Grupos y Docentes"), self.BG, self.TEXT_MAIN).pack(side="right")

        with self.conectar(incluir_bd=True) as db:
            cur = db.cursor()
            cur.execute("""
                SELECT g.grupo, g.docente, g.alumnos,
                       COALESCE(SUM(a.retardos), 0),
                       COALESCE(SUM(a.faltas), 0),
                       COALESCE(SUM(CASE WHEN a.faltas >= %s THEN 1 ELSE 0 END), 0)
                FROM grupos g
                LEFT JOIN alumnos a ON a.grupo = g.grupo
                GROUP BY g.id, g.grupo, g.docente, g.alumnos
                ORDER BY g.grupo, 6 DESC, 5 DESC
            """, (UMBRAL_FALTAS,))
            filas = cur.fetchall()

            cur.execute("SELECT id, nombre, grupo, retardos, faltas FROM alumnos ORDER BY grupo, nombre")
            todos_alumnos = cur.fetchall()

        notebook = ttk.Notebook(box)
        notebook.pack(fill="both", expand=True, pady=(4, 0))
        self.notebook_grupos = notebook
        self._datos_grupos_pestanas = {}

        if not filas:
            vacio = tk.Frame(notebook, bg=self.WHITE, padx=16, pady=16)
            notebook.add(vacio, text="Sin grupos")
            tk.Label(
                vacio,
                text="No hay grupos registrados. Usa 'Agregar grupo' o 'Carga masiva grupos' para crear una pestaña.",
                bg=self.WHITE,
                fg=self.MUTED,
                font=("Segoe UI", 9)
            ).pack(anchor="w")
            return

        for grupo_nombre, docente, alumnos_meta, retardos_g, faltas_g, alertas_g in filas:
            pestana_grupo = tk.Frame(notebook, bg=self.BG, padx=12, pady=12)
            notebook.add(pestana_grupo, text=grupo_nombre)
            self._datos_grupos_pestanas[grupo_nombre] = (grupo_nombre, docente)

            alumnos_del_grupo = [a for a in todos_alumnos if a[2] == grupo_nombre]
            total_al = len(alumnos_del_grupo) if alumnos_del_grupo else alumnos_meta

            stats_row = tk.Frame(pestana_grupo, bg=self.BG)
            stats_row.pack(fill="x", pady=(0, 10))

            resumen_items = [
                ("DOCENTE TITULAR", docente, self.PURPLE),
                ("ALUMNOS", str(total_al), self.TEAL),
                ("RETARDOS", str(retardos_g), self.GOLD),
                ("FALTAS", str(faltas_g), self.RED),
                ("ALERTAS", str(alertas_g), self.RED_DARK),
            ]
            for idx, (etq, val, col) in enumerate(resumen_items):
                c = tk.Frame(stats_row, bg=self.WHITE,
                             highlightbackground=self.BORDER, highlightthickness=1)
                c.grid(row=0, column=idx, sticky="nsew", padx=(0 if idx == 0 else 4, 0))
                stats_row.grid_columnconfigure(idx, weight=1)
                tk.Frame(c, bg=col, width=3).pack(side="left", fill="y")
                c_body = tk.Frame(c, bg=self.WHITE, padx=10, pady=7)
                c_body.pack(side="left", fill="both", expand=True)
                tk.Label(c_body, text=etq, bg=self.WHITE, fg=self.MUTED, font=("Segoe UI", 7, "bold")).pack(anchor="w")
                tk.Label(c_body, text=val, bg=self.WHITE, fg=self.TEXT_MAIN,
                         font=("Segoe UI", 10 if idx == 0 else 13, "bold"),
                         wraplength=150, justify="left").pack(anchor="w")

            filas_alumnos = []
            for ident, nombre, gpo, ret, fal in alumnos_del_grupo:
                estado = "Atención" if fal >= UMBRAL_FALTAS else ("Retardos" if ret else "Regular")
                filas_alumnos.append((ident, nombre, gpo, ret, fal, estado))

            tabla_al = self.crear_tabla(
                pestana_grupo,
                ("ID", "Alumno", "Grupo", "Retardos", "Faltas", "Estado"),
                filas_alumnos,
                {"Alumno": 200, "Estado": 100},
                6
            )
            fg_tag = self.TEXT_SOFT
            tabla_al.tag_configure("retardo", background=self.YELLOW_SOFT, foreground=fg_tag)
            tabla_al.tag_configure("falta", background=self.RED_SOFT, foreground=fg_tag)
            for item in tabla_al.get_children():
                vals = tabla_al.item(item, "values")
                if int(vals[4]) >= UMBRAL_FALTAS:
                    tabla_al.item(item, tags=("falta",))
                elif int(vals[3]) > 0:
                    tabla_al.item(item, tags=("retardo",))

            bar_al = tk.Frame(pestana_grupo, bg=self.BG)
            bar_al.pack(fill="x", pady=(10, 0))
            self.boton(
                bar_al,
                "Registrar seguimiento",
                lambda t=tabla_al: self._seguimiento_desde_pestana(t),
                self.GOLD,
                "#FFFFFF"
            ).pack(side="left", padx=(0, 6))
            self.boton(
                bar_al,
                f"⬆ Cargar alumnos en {grupo_nombre}",
                lambda g=grupo_nombre: self.carga_masiva_alumnos(grupo_predefinido=g),
                self.TEAL,
                "#FFFFFF"
            ).pack(side="left")

    def _seguimiento_desde_pestana(self, tabla):
        if not tabla or not tabla.selection():
            messagebox.showwarning("Selecciona", "Selecciona un alumno de la tabla.")
            return
        fila = tabla.item(tabla.selection()[0], "values")
        self.registrar_seguimiento(int(fila[0]), fila[1])

    def carga_masiva_grupos(self):
        def procesar(filas):
            insertados = 0
            actualizados = 0
            errores = []
            try:
                with self.conectar(incluir_bd=True) as db:
                    cur = db.cursor()
                    for idx, fila in enumerate(filas, start=1):
                        if len(fila) < 2 or not fila[0] or not fila[1]:
                            errores.append(f"Fila {idx}: faltan grupo o docente.")
                            continue
                        grupo = fila[0]
                        docente = fila[1]
                        try:
                            alumnos_cant = int(fila[2]) if len(fila) >= 3 and fila[2] else 0
                        except ValueError:
                            errores.append(f"Fila {idx}: cantidad de alumnos no válida ('{fila[2]}').")
                            continue
                        cur.execute("SELECT id FROM grupos WHERE grupo=%s", (grupo,))
                        if cur.fetchone():
                            cur.execute("UPDATE grupos SET docente=%s, alumnos=%s WHERE grupo=%s",
                                        (docente, alumnos_cant, grupo))
                            actualizados += 1
                        else:
                            cur.execute("INSERT INTO grupos (grupo, docente, alumnos) VALUES (%s, %s, %s)",
                                        (grupo, docente, alumnos_cant))
                            insertados += 1
                    db.commit()
            except MySQLError as e:
                messagebox.showerror("Error MySQL", str(e), parent=self.root)
                return None
            msg = f"Grupos agregados: {insertados}\nGrupos actualizados: {actualizados}"
            if errores:
                msg += f"\nErrores ({len(errores)}):\n" + "\n".join(errores[:8])
            messagebox.showinfo("Carga masiva completada", msg)
            self.mostrar("Grupos y Docentes")
            return True

        abrir_modal_carga_masiva(
            self,
            "Carga masiva de grupos",
            "Importa varios grupos a la vez desde CSV o pegando filas.",
            ["grupo", "docente", "alumnos"],
            [["5° B", "Elena Soto Vargas", "29"], ["6° A", "Carlos Méndez Ortiz", "30"]],
            procesar
        )

    def carga_masiva_alumnos(self, grupo_predefinido=None):
        def procesar(filas):
            insertados = 0
            omitidos = 0
            errores = []
            try:
                with self.conectar(incluir_bd=True) as db:
                    cur = db.cursor()
                    for idx, fila in enumerate(filas, start=1):
                        if grupo_predefinido:
                            if not fila[0]:
                                errores.append(f"Fila {idx}: falta nombre del alumno.")
                                continue
                            nombre = fila[0]
                            grupo = grupo_predefinido
                            ret_idx, fal_idx = 1, 2
                        else:
                            if len(fila) < 2 or not fila[0] or not fila[1]:
                                errores.append(f"Fila {idx}: faltan nombre o grupo.")
                                continue
                            nombre = fila[0]
                            grupo = fila[1]
                            ret_idx, fal_idx = 2, 3
                        try:
                            retardos = int(fila[ret_idx]) if len(fila) > ret_idx and fila[ret_idx] else 0
                            faltas = int(fila[fal_idx]) if len(fila) > fal_idx and fila[fal_idx] else 0
                        except ValueError:
                            errores.append(f"Fila {idx}: retardos o faltas deben ser números enteros.")
                            continue
                        cur.execute("INSERT IGNORE INTO grupos (grupo, docente, alumnos) VALUES (%s, %s, 0)",
                                    (grupo, "Por asignar"))
                        cur.execute(
                            "INSERT IGNORE INTO alumnos (nombre, grupo, retardos, faltas) VALUES (%s, %s, %s, %s)",
                            (nombre, grupo, retardos, faltas)
                        )
                        if cur.rowcount > 0:
                            insertados += 1
                        else:
                            omitidos += 1
                    db.commit()
            except MySQLError as e:
                messagebox.showerror("Error MySQL", str(e), parent=self.root)
                return None
            msg = f"Alumnos importados: {insertados}\nDuplicados omitidos: {omitidos}"
            if errores:
                msg += f"\nErrores ({len(errores)}):\n" + "\n".join(errores[:8])
            messagebox.showinfo("Carga masiva completada", msg)
            self.mostrar("Grupos y Docentes")
            return True

        if grupo_predefinido:
            abrir_modal_carga_masiva(
                self,
                f"Carga masiva de alumnos ({grupo_predefinido})",
                f"Importa alumnos directamente al grupo {grupo_predefinido}.",
                ["nombre", "retardos", "faltas"],
                [["Isac Herrera Luz", "0", "0"], ["Valeria Ruiz Díaz", "1", "0"]],
                procesar
            )
        else:
            abrir_modal_carga_masiva(
                self,
                "Carga masiva de alumnos",
                "Importa múltiples alumnos en lote (retardos y faltas son opcionales).",
                ["nombre", "grupo", "retardos", "faltas"],
                [["Isac Herrera Luz", "5° A", "0", "0"], ["Valeria Ruiz Díaz", "5° A", "1", "0"]],
                procesar
            )

    def agregar_grupo(self):
        datos = self.formulario_modal("Agregar grupo", [
            ("Nombre del grupo", "", None),
            ("Nombre del docente", "", None)
        ])
        if not datos:
            return
        try:
            with self.conectar(incluir_bd=True) as db:
                cur = db.cursor()
                cur.execute("INSERT INTO grupos (grupo, docente, alumnos) VALUES (%s, %s, 0)",
                            (datos["Nombre del grupo"], datos["Nombre del docente"]))
                db.commit()
            self.mostrar("Grupos y Docentes")
        except IntegrityError:
            messagebox.showwarning("Grupo existente", "Ese grupo ya está registrado.")

    def editar_grupo(self):
        nb = getattr(self, "notebook_grupos", None)
        datos_pestanas = getattr(self, "_datos_grupos_pestanas", {})
        if not nb or not nb.tabs() or not datos_pestanas:
            messagebox.showwarning("Sin grupos", "No hay ningún grupo disponible para editar.")
            return
        pestana_actual = nb.tab(nb.select(), "text")
        if pestana_actual not in datos_pestanas:
            messagebox.showwarning("Selecciona", "Selecciona la pestaña del grupo que deseas editar.")
            return
        grupo_original, docente_actual = datos_pestanas[pestana_actual]
        datos = self.formulario_modal("Editar grupo", [
            ("Nombre del grupo", grupo_original, None),
            ("Nombre del docente", docente_actual, None)
        ])
        if not datos:
            return
        try:
            with self.conectar(incluir_bd=True) as db:
                cur = db.cursor()
                cur.execute("UPDATE grupos SET grupo=%s, docente=%s WHERE grupo=%s",
                            (datos["Nombre del grupo"], datos["Nombre del docente"], grupo_original))
                if datos["Nombre del grupo"] != grupo_original:
                    cur.execute("UPDATE alumnos SET grupo=%s WHERE grupo=%s",
                                (datos["Nombre del grupo"], grupo_original))
                db.commit()
            self.mostrar("Grupos y Docentes")
        except IntegrityError:
            messagebox.showwarning("Nombre duplicado", "Ya existe un grupo con ese nombre.")

    def alumno_seleccionado(self, tabla=None):
        tabla = tabla or getattr(self, "tabla_alumnos", None)
        if tabla and tabla.selection():
            return tabla.item(tabla.selection()[0], "values")
        return None

    def registrar_seguimiento(self, alumno_id, nombre):
        datos = self.formulario_modal("Registrar seguimiento", [(f"Nota para {nombre}", "", None)])
        if not datos:
            return
        nota = datos[f"Nota para {nombre}"]
        with self.conectar(incluir_bd=True) as db:
            cur = db.cursor()
            cur.execute("INSERT INTO seguimientos (alumno_id, fecha, nota) VALUES (%s, %s, %s)",
                        (alumno_id, date.today().isoformat(), nota))
            db.commit()
        messagebox.showinfo("Guardado", "La nota se registró correctamente.")
        self.mostrar(self.pagina)

    def pagina_comunicados(self):
        sec = self.seccion(self.contenido, "Módulo de Comunicados y Avisos Oficiales")
        sec.pack(fill="x", padx=18, pady=(14, 6))
        self.boton(sec.body, "＋ Redactar Comunicado", self.agregar_comunicado, self.GOLD, "#FFFFFF").pack(anchor="w")

        sec_list = self.seccion(self.contenido, "Historial de Comunicados Emitidos")
        sec_list.pack(fill="both", padx=18, pady=6)
        with self.conectar(incluir_bd=True) as db:
            cur = db.cursor()
            cur.execute("SELECT id, fecha, titulo, mensaje FROM comunicados ORDER BY id DESC")
            rows = cur.fetchall()
        self.crear_tabla(sec_list.body, ("ID", "Fecha", "Título", "Mensaje"), rows, {"Título": 160, "Mensaje": 240}, 6)

    def agregar_comunicado(self):
        datos = self.formulario_modal("Nuevo Comunicado", [
            ("Título del aviso", "", None),
            ("Mensaje detallado", "", None)
        ])
        if not datos:
            return
        with self.conectar(incluir_bd=True) as db:
            cur = db.cursor()
            cur.execute("INSERT INTO comunicados (fecha, titulo, mensaje) VALUES (%s, %s, %s)",
                        (date.today().isoformat(), datos["Título del aviso"], datos["Mensaje detallado"]))
            db.commit()
        messagebox.showinfo("Enviado", "El comunicado se ha registrado.")
        self.mostrar("Comunicados Oficiales")

    def pagina_bitacora(self):
        sec = self.seccion(self.contenido, "Bitácora Directiva")
        sec.pack(fill="x", padx=18, pady=(14, 6))

        def agregar_entrada():
            datos = self.formulario_modal("Nueva Nota de Bitácora", [("Descripción del evento", "", None)])
            if not datos:
                return
            with self.conectar(incluir_bd=True) as db:
                cur = db.cursor()
                cur.execute("INSERT INTO bitacora (fecha, entrada) VALUES (%s, %s)",
                            (date.today().isoformat(), datos["Descripción del evento"]))
                db.commit()
            messagebox.showinfo("Guardado", "Entrada agregada.")
            self.mostrar("Bitácora Directiva")

        self.boton(sec.body, "＋ Nueva entrada en bitácora", agregar_entrada, self.GOLD, "#FFFFFF").pack(anchor="w")

        sec_list = self.seccion(self.contenido, "Registro Histórico de Bitácora")
        sec_list.pack(fill="both", padx=18, pady=6)
        with self.conectar(incluir_bd=True) as db:
            cur = db.cursor()
            cur.execute("SELECT id, fecha, entrada FROM bitacora ORDER BY id DESC")
            rows = cur.fetchall()
        self.crear_tabla(sec_list.body, ("ID", "Fecha", "Entrada"), rows, {"Entrada": 280}, 6)

    def resumen_alertas(self, parent, limite=None):
        with self.conectar(incluir_bd=True) as db:
            cur = db.cursor()
            cur.execute("SELECT COUNT(*) FROM alumnos WHERE faltas >= %s OR retardos >= %s", (UMBRAL_FALTAS, UMBRAL_FALTAS))
            alumnos = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM justificantes WHERE estado='Pendiente'")
            just = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM incidencias WHERE estado='Pendiente'")
            inc = cur.fetchone()[0]
        items = []
        if alumnos:
            items.append((f"{alumnos} alumnos con alertas", "Revisar faltas o retardos.", self.RED_SOFT, "Módulo de Alertas"))
        if just:
            items.append((f"{just} justificantes pendientes", "Validar documentos.", self.LAVENDER, "Módulo de Alertas"))
        if inc:
            items.append((f"{inc} incidencias sin atender", "Seguimiento de casos.", self.BLUE_SOFT, "Conducta / Incidencias"))
        if not items:
            items.append(("Sin alertas pendientes", "Todo en orden.", self.GREEN_SOFT, "Módulo de Alertas"))

        fg_alt = self.TEXT_SOFT
        for title, detail, color, dest in (items[:limite] if limite else items):
            f = tk.Frame(parent, bg=color, padx=10, pady=8,
                         highlightbackground=self.BORDER, highlightthickness=1)
            f.pack(fill="x", pady=3)
            tk.Label(f, text=title, bg=color, fg=fg_alt, font=("Segoe UI", 8, "bold"), wraplength=260, justify="left").pack(anchor="w")
            tk.Label(f, text=detail, bg=color, fg=fg_alt, font=("Segoe UI", 8), wraplength=260, justify="left").pack(anchor="w", pady=(1, 4))
            self.boton(f, "Abrir", lambda p=dest: self.mostrar(p), self.NAVY, self.TEXT_NAV, True).pack(anchor="e")

    def pagina_conducta(self):
        """Pestaña dedicada exclusivamente a Conducta / Incidencias."""
        sec_reg = self.seccion(self.contenido, "Registrar incidencia de conducta")
        sec_reg.pack(fill="x", padx=18, pady=(14, 6))
        box_reg = sec_reg.body

        alumnos = self.obtener_alumnos()
        opts = {f"{a[0]} · {a[1]} ({a[2]})": a[0] for a in alumnos}
        alumno_var = tk.StringVar(value=next(iter(opts)) if opts else "")

        tk.Label(box_reg, text="Alumno", bg=self.WHITE, fg=self.TEXT_MAIN, font=("Segoe UI", 8, "bold")).pack(anchor="w")
        ttk.Combobox(box_reg, textvariable=alumno_var, values=list(opts), state="readonly").pack(fill="x", pady=(2, 8))

        tk.Label(box_reg, text="Tipo de incidencia", bg=self.WHITE, fg=self.TEXT_MAIN, font=("Segoe UI", 8, "bold")).pack(anchor="w")
        ent_tipo = tk.Entry(box_reg, font=("Segoe UI", 9), bg=self.WHITE, fg=self.TEXT_MAIN,
                            relief="flat", highlightthickness=1, highlightbackground=self.BORDER, highlightcolor=self.PURPLE, bd=0)
        ent_tipo.pack(fill="x", ipady=5, pady=(2, 8))

        tk.Label(box_reg, text="Descripción", bg=self.WHITE, fg=self.TEXT_MAIN, font=("Segoe UI", 8, "bold")).pack(anchor="w")
        ent_desc = tk.Entry(box_reg, font=("Segoe UI", 9), bg=self.WHITE, fg=self.TEXT_MAIN,
                            relief="flat", highlightthickness=1, highlightbackground=self.BORDER, highlightcolor=self.PURPLE, bd=0)
        ent_desc.pack(fill="x", ipady=5, pady=(2, 8))

        def guardar_incidencia():
            alumno_id = opts.get(alumno_var.get())
            tipo = ent_tipo.get().strip()
            desc = ent_desc.get().strip()
            if not alumno_id or not tipo or not desc:
                messagebox.showwarning("Incompletos", "Selecciona un alumno y completa tipo y descripción.")
                return
            with self.conectar(incluir_bd=True) as db:
                cur = db.cursor()
                cur.execute("INSERT INTO incidencias (alumno_id, fecha, tipo, descripcion, estado) VALUES (%s, %s, %s, %s, 'Pendiente')",
                            (alumno_id, date.today().isoformat(), tipo, desc))
                db.commit()
            messagebox.showinfo("Registrado", "Incidencia de conducta guardada.")
            self.mostrar("Conducta / Incidencias")

        self.boton(box_reg, "＋ Guardar incidencia", guardar_incidencia, self.RED, "#FFFFFF").pack(anchor="w")

        sec_inc = self.seccion(self.contenido, "Historial de incidencias de conducta")
        sec_inc.pack(fill="both", expand=True, padx=18, pady=6)
        incbox = sec_inc.body
        with self.conectar(incluir_bd=True) as db:
            cur = db.cursor()
            cur.execute("""
                SELECT i.id, i.fecha, a.nombre, i.tipo, i.descripcion, i.estado
                FROM incidencias i JOIN alumnos a ON a.id = i.alumno_id
                ORDER BY i.id DESC
            """)
            incs = cur.fetchall()
        itable = self.crear_tabla(incbox, ("ID", "Fecha", "Alumno", "Tipo", "Descripción", "Estado"), incs, {"Alumno": 140, "Tipo": 110, "Descripción": 200}, 6)

        def cerrar():
            if not itable.selection():
                messagebox.showwarning("Selecciona", "Selecciona una incidencia.")
                return
            ident = itable.item(itable.selection()[0], "values")[0]
            with self.conectar(incluir_bd=True) as db:
                cur = db.cursor()
                cur.execute("UPDATE incidencias SET estado='Atendida' WHERE id=%s", (ident,))
                db.commit()
            self.mostrar("Conducta / Incidencias")

        self.boton(incbox, "Marcar atendida", cerrar, self.GOLD, "#FFFFFF").pack(anchor="w", pady=(8, 0))

    def pagina_cartas_compromiso(self):
        """Pestaña dedicada exclusivamente a Cartas Compromiso y acuerdos de mejora."""
        sec_cc = self.seccion(self.contenido, "Alumnos candidatos a Carta Compromiso")
        sec_cc.pack(fill="both", expand=True, padx=18, pady=(14, 6))
        box = sec_cc.body

        with self.conectar(incluir_bd=True) as db:
            cur = db.cursor()
            cur.execute(
                "SELECT id, nombre, grupo, retardos, faltas FROM alumnos WHERE faltas >= %s OR retardos >= %s ORDER BY faltas DESC, retardos DESC",
                (UMBRAL_FALTAS, UMBRAL_FALTAS)
            )
            rows = cur.fetchall()

        filas = [
            (i, n, g, r, f, "Carta compromiso por faltas" if f >= UMBRAL_FALTAS else "Carta compromiso por retardos")
            for i, n, g, r, f in rows
        ]
        table = self.crear_tabla(box, ("ID", "Alumno", "Grupo", "Retardos", "Faltas", "Acuerdo"), filas, {"Alumno": 160, "Acuerdo": 180}, 6)

        actions = tk.Frame(box, bg=self.WHITE)
        actions.pack(fill="x", pady=(8, 0))

        def registrar_carta():
            a = self.alumno_seleccionado(table)
            if not a:
                messagebox.showwarning("Selecciona", "Selecciona un alumno de la tabla.")
                return
            datos = self.formulario_modal("Registrar Carta Compromiso", [
                ("Compromiso acordado", "", None)
            ])
            if not datos:
                return
            nota = f"[CARTA COMPROMISO] {datos['Compromiso acordado']}"
            with self.conectar(incluir_bd=True) as db:
                cur = db.cursor()
                cur.execute("INSERT INTO seguimientos (alumno_id, fecha, nota) VALUES (%s, %s, %s)",
                            (int(a[0]), date.today().isoformat(), nota))
                db.commit()
            messagebox.showinfo("Guardado", "Carta compromiso registrada en seguimiento.")
            self.mostrar("Cartas Compromiso")

        self.boton(actions, "＋ Registrar carta compromiso", registrar_carta, self.GOLD, "#FFFFFF").pack(side="left")

        sec_seg = self.seccion(self.contenido, "Seguimientos y cartas compromiso registrados")
        sec_seg.pack(fill="both", expand=True, padx=18, pady=6)
        with self.conectar(incluir_bd=True) as db:
            cur = db.cursor()
            cur.execute("""
                SELECT s.id, s.fecha, a.nombre, a.grupo, s.nota
                FROM seguimientos s JOIN alumnos a ON a.id = s.alumno_id
                ORDER BY s.id DESC LIMIT 30
            """)
            seg_rows = cur.fetchall()
        self.crear_tabla(sec_seg.body, ("ID", "Fecha", "Alumno", "Grupo", "Acuerdo / Nota"), seg_rows, {"Alumno": 150, "Acuerdo / Nota": 260}, 5)

    def pagina_alertas(self):
        """Pestaña dedicada exclusivamente al Módulo de Alertas (asistencia, faltas, retardos y justificantes)."""
        sec_sum = self.seccion(self.contenido, "Resumen de alertas")
        sec_sum.pack(fill="x", padx=18, pady=(14, 6))
        self.resumen_alertas(sec_sum.body)

        sec_box = self.seccion(self.contenido, "Alumnos con alertas de asistencia (3 retardos = 1 falta)")
        sec_box.pack(fill="both", padx=18, pady=6)
        box = sec_box.body
        with self.conectar(incluir_bd=True) as db:
            cur = db.cursor()
            cur.execute(
                "SELECT id, nombre, grupo, retardos, faltas FROM alumnos WHERE faltas >= %s OR retardos >= %s ORDER BY faltas DESC, retardos DESC",
                (UMBRAL_FALTAS, UMBRAL_FALTAS)
            )
            rows = cur.fetchall()
        filas = [(i, n, g, r, f, "Faltas" if f >= UMBRAL_FALTAS else "Retardos") for i, n, g, r, f in rows]
        table = self.crear_tabla(box, ("ID", "Alumno", "Grupo", "Retardos", "Faltas", "Motivo"), filas, {"Alumno": 150, "Motivo": 110}, 5)
        fg_tag = self.TEXT_SOFT
        table.tag_configure("falta", background=self.RED_SOFT, foreground=fg_tag)
        table.tag_configure("retardo", background=self.YELLOW_SOFT, foreground=fg_tag)
        for item in table.get_children():
            v = table.item(item, "values")
            table.item(item, tags=("falta" if int(v[4]) >= UMBRAL_FALTAS else "retardo",))

        sec_just = self.seccion(self.contenido, "Justificantes pendientes de validación")
        sec_just.pack(fill="both", padx=18, pady=6)
        jbox = sec_just.body
        with self.conectar(incluir_bd=True) as db:
            cur = db.cursor()
            cur.execute("SELECT id, alumno, grupo, fecha, motivo, estado FROM justificantes ORDER BY id DESC")
            just_rows = cur.fetchall()
        jtable = self.crear_tabla(jbox, ("ID", "Alumno", "Grupo", "Fecha", "Motivo", "Estado"), just_rows, {"Alumno": 140, "Motivo": 200}, 5)

        def validar_justificante():
            if not jtable.selection():
                messagebox.showwarning("Selecciona", "Selecciona un justificante.")
                return
            ident = jtable.item(jtable.selection()[0], "values")[0]
            with self.conectar(incluir_bd=True) as db:
                cur = db.cursor()
                cur.execute("UPDATE justificantes SET estado='Validado' WHERE id=%s", (ident,))
                db.commit()
            self.mostrar("Módulo de Alertas")

        self.boton(jbox, "Validar justificante", validar_justificante, self.GOLD, "#FFFFFF").pack(anchor="w", pady=(8, 0))

    def _cambiar_mes_calendario(self, delta):
        mes = self.cal_mes + delta
        anio = self.cal_anio
        if mes < 1:
            mes = 12
            anio -= 1
        elif mes > 12:
            mes = 1
            anio += 1
        self.cal_anio = anio
        self.cal_mes = mes
        self.mostrar("Calendario Oficial")

    def _ir_hoy_calendario(self):
        hoy = date.today()
        self.cal_anio = hoy.year
        self.cal_mes = hoy.month
        self.mostrar("Calendario Oficial")

    def pagina_calendario(self):
        sec = self.seccion(self.contenido, "Calendario Escolar")
        sec.pack(fill="both", expand=True, padx=18, pady=(14, 6))
        box = sec.body

        hoy = date.today()
        nombre_mes = MESES_ES[self.cal_mes] if 1 <= self.cal_mes <= 12 else str(self.cal_mes)

        barra_mes = tk.Frame(box, bg=self.WHITE)
        barra_mes.pack(fill="x", pady=(0, 10))
        self.boton(barra_mes, "◀ Mes anterior", lambda: self._cambiar_mes_calendario(-1), self.DARK, self.TEXT_NAV).pack(side="left", padx=(0, 6))
        self.boton(barra_mes, "Mes siguiente ▶", lambda: self._cambiar_mes_calendario(1), self.DARK, self.TEXT_NAV).pack(side="left", padx=(0, 6))
        self.boton(barra_mes, "Hoy", self._ir_hoy_calendario, self.LAVENDER, self.TEXT_SOFT).pack(side="left", padx=(0, 12))
        tk.Label(barra_mes, text=f"{nombre_mes} {self.cal_anio}", bg=self.WHITE, fg=self.PURPLE,
                 font=("Segoe UI", 12, "bold")).pack(side="left")
        self.boton(barra_mes, "＋ Agregar evento", self.agregar_evento, self.GOLD, "#FFFFFF").pack(side="right")

        with self.conectar(incluir_bd=True) as db:
            cur = db.cursor()
            cur.execute("SELECT fecha, titulo FROM eventos ORDER BY fecha")
            todos_eventos = cur.fetchall()

        eventos_por_fecha = {}
        for f_ev, t_ev in todos_eventos:
            eventos_por_fecha.setdefault(str(f_ev), []).append(str(t_ev))

        grid_cal = tk.Frame(box, bg=self.BORDER, padx=1, pady=1)
        grid_cal.pack(fill="both", expand=True)

        for col_idx, dia_nom in enumerate(DIAS_ES):
            grid_cal.grid_columnconfigure(col_idx, weight=1, uniform="cal_cols")
            tk.Label(
                grid_cal, text=dia_nom, bg=self.NAVY, fg=self.TEXT_NAV,
                font=("Segoe UI", 9, "bold"), pady=8
            ).grid(row=0, column=col_idx, sticky="nsew", padx=1, pady=1)

        cal_obj = calendar.Calendar(firstweekday=0)
        semanas = cal_obj.monthdayscalendar(self.cal_anio, self.cal_mes)

        for row_idx, semana in enumerate(semanas, start=1):
            grid_cal.grid_rowconfigure(row_idx, weight=1, uniform="cal_rows")
            for col_idx, dia_num in enumerate(semana):
                if dia_num == 0:
                    celda = tk.Frame(grid_cal, bg=self.BG, height=95)
                    celda.grid(row=row_idx, column=col_idx, sticky="nsew", padx=1, pady=1)
                    celda.pack_propagate(False)
                    continue

                fecha_iso = f"{self.cal_anio:04d}-{self.cal_mes:02d}-{dia_num:02d}"
                evs_dia = eventos_por_fecha.get(fecha_iso, [])
                es_hoy = (dia_num == hoy.day and self.cal_mes == hoy.month and self.cal_anio == hoy.year)

                bg_celda = self.BLUE_SOFT if es_hoy else (self.GREEN_SOFT if evs_dia else self.WHITE)
                celda = tk.Frame(grid_cal, bg=bg_celda, height=95, cursor="hand2")
                celda.grid(row=row_idx, column=col_idx, sticky="nsew", padx=1, pady=1)
                celda.pack_propagate(False)

                top_celda = tk.Frame(celda, bg=bg_celda, padx=8, pady=6)
                top_celda.pack(fill="x")
                lbl_dia = tk.Label(
                    top_celda,
                    text=f"{dia_num} · Hoy" if es_hoy else str(dia_num),
                    bg=bg_celda,
                    fg=self.PURPLE if es_hoy else self.TEXT_MAIN,
                    font=("Segoe UI", 10, "bold")
                )
                lbl_dia.pack(side="left")

                if evs_dia:
                    resumen_ev = evs_dia[0] if len(evs_dia) == 1 else f"{evs_dia[0]} (+{len(evs_dia) - 1})"
                    lbl_ev = tk.Label(
                        celda, text=resumen_ev, bg=bg_celda, fg=self.TEXT_SOFT,
                        font=("Segoe UI", 8, "bold"), anchor="w", justify="left",
                        wraplength=160, padx=8
                    )
                    lbl_ev.pack(fill="x", anchor="w")

                def _clic_fecha(e, f_sel=fecha_iso):
                    self.agregar_evento(fecha_inicial=f_sel)

                for w_c in ([celda, top_celda, lbl_dia] + ([lbl_ev] if evs_dia else [])):
                    w_c.bind("<Button-1>", _clic_fecha)

        sec_list = self.seccion(self.contenido, "Eventos Registrados")
        sec_list.pack(fill="both", expand=True, padx=18, pady=6)
        listing = sec_list.body
        with self.conectar(incluir_bd=True) as db:
            cur = db.cursor()
            cur.execute("SELECT id, fecha, titulo FROM eventos ORDER BY fecha")
            rows = cur.fetchall()
        table = self.crear_tabla(listing, ("ID", "Fecha", "Evento"), rows, {"Evento": 240}, 6)
        actions = tk.Frame(listing, bg=self.WHITE)
        actions.pack(fill="x", pady=(8, 0))
        self.boton(actions, "Editar", lambda: self.editar_evento(table), self.DARK, self.TEXT_NAV).pack(side="left", padx=(0, 6))
        self.boton(actions, "Eliminar", lambda: self.eliminar_evento(table), self.RED, "#FFFFFF").pack(side="left")

    def agregar_evento(self, fecha_inicial=None):
        fecha_def = fecha_inicial or f"{self.cal_anio:04d}-{self.cal_mes:02d}-{min(date.today().day, calendar.monthrange(self.cal_anio, self.cal_mes)[1]):02d}"
        datos = self.formulario_modal("Agregar evento", [("Fecha (AAAA-MM-DD)", fecha_def, None), ("Nombre del evento", "", None)])
        if not datos:
            return
        try:
            datetime.strptime(datos["Fecha (AAAA-MM-DD)"], "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Formato", "Usa el formato AAAA-MM-DD.")
            return
        with self.conectar(incluir_bd=True) as db:
            cur = db.cursor()
            cur.execute("INSERT INTO eventos (fecha, titulo) VALUES (%s, %s)",
                        (datos["Fecha (AAAA-MM-DD)"], datos["Nombre del evento"]))
            db.commit()
        self.mostrar("Calendario Oficial")

    def editar_evento(self, table):
        if not table.selection():
            messagebox.showwarning("Selecciona", "Selecciona un evento.")
            return
        fila = table.item(table.selection()[0], "values")
        datos = self.formulario_modal("Editar evento", [("Fecha (AAAA-MM-DD)", str(fila[1]), None), ("Nombre del evento", fila[2], None)])
        if not datos:
            return
        try:
            datetime.strptime(datos["Fecha (AAAA-MM-DD)"], "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Formato", "Usa el formato AAAA-MM-DD.")
            return
        with self.conectar(incluir_bd=True) as db:
            cur = db.cursor()
            cur.execute("UPDATE eventos SET fecha=%s, titulo=%s WHERE id=%s",
                        (datos["Fecha (AAAA-MM-DD)"], datos["Nombre del evento"], fila[0]))
            db.commit()
        self.mostrar("Calendario Oficial")

    def eliminar_evento(self, table):
        if not table.selection():
            messagebox.showwarning("Selecciona", "Selecciona un evento.")
            return
        ident = table.item(table.selection()[0], "values")[0]
        if messagebox.askyesno("Eliminar", "¿Deseas eliminar el evento?"):
            with self.conectar(incluir_bd=True) as db:
                cur = db.cursor()
                cur.execute("DELETE FROM eventos WHERE id=%s", (ident,))
                db.commit()
            self.mostrar("Calendario Oficial")

    def pagina_reportes(self):
        sec = self.seccion(self.contenido, "Reportes y exportación")
        sec.pack(fill="x", padx=18, pady=(14, 6))
        box = sec.body
        m = self.obtener_metricas()
        fg_m = self.TEXT_MAIN
        for name in ("Alumnos", "Presentes", "Retardos", "Faltas"):
            row = tk.Frame(box, bg=self.WHITE)
            row.pack(fill="x", pady=4)
            tk.Label(row, text=name, bg=self.WHITE, fg=fg_m, font=("Segoe UI", 9)).pack(side="left")
            tk.Label(row, text=str(m.get(name, 0)), bg=self.WHITE, fg=self.PURPLE, font=("Segoe UI", 9, "bold")).pack(side="right")
        btns = tk.Frame(box, bg=self.WHITE)
        btns.pack(fill="x", pady=(10, 0))
        self.boton(btns, "Exportar historial (CSV)", self.exportar_csv, self.GOLD, "#FFFFFF").pack(side="left", padx=(0, 6))
        self.boton(btns, "Exportar alumnos (CSV)", self.exportar_alumnos, self.LAVENDER, self.TEXT_SOFT).pack(side="left")

    def exportar_csv(self):
        try:
            ruta = os.path.join(BASE_DIR, "reporte_asistencia.csv")
            with self.conectar(incluir_bd=True) as db:
                cur = db.cursor()
                cur.execute("""
                    SELECT a.fecha, al.id, al.nombre, al.grupo, a.estado
                    FROM asistencias a JOIN alumnos al ON al.id = a.alumno_id
                    ORDER BY a.fecha DESC
                """)
                rows = cur.fetchall()
            with open(ruta, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(["Fecha", "ID alumno", "Nombre", "Grupo", "Estado"])
                writer.writerows(rows)
            messagebox.showinfo("Exportado", f"Guardado en:\n{ruta}")
        except (OSError, MySQLError) as e:
            messagebox.showerror("Error", str(e))

    def exportar_alumnos(self):
        try:
            ruta = os.path.join(BASE_DIR, "lista_alumnos.csv")
            with open(ruta, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Nombre", "Grupo", "Retardos", "Faltas"])
                writer.writerows(self.obtener_alumnos())
            messagebox.showinfo("Exportado", f"Guardado en:\n{ruta}")
        except (OSError, MySQLError) as e:
            messagebox.showerror("Error", str(e))

    def _aplicar_colores_guardados_dir(self, nuevos_colores):
        self.colores_personalizados = dict(nuevos_colores)
        self.actualizar_colores()
        self.configurar_estilos()
        self.crear_panel("Configuración")

    def pagina_configuracion(self):
        sec_col = self.seccion(self.contenido, "Personalización de colores por usuario (MySQL)")
        sec_col.pack(fill="x", padx=18, pady=(14, 6))
        construir_bloque_personalizacion_colores(
            self, sec_col.body, "director", self._aplicar_colores_guardados_dir
        )

        sec = self.seccion(self.contenido, "Preferencias y reglas del sistema")
        sec.pack(fill="x", padx=18, pady=6)
        box = sec.body
        fg_c = self.TEXT_MAIN
        tk.Label(box, text="Regla de asistencia", bg=self.WHITE, fg=fg_c, font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(box, text="3 retardos equivalen a 1 falta. Alertas automáticas al llegar a 3 faltas.",
                 bg=self.LAVENDER, fg=self.TEXT_SOFT, padx=10, pady=8, justify="left", wraplength=340).pack(fill="x", pady=(4, 10))
        tk.Label(box, text="Base de datos principal MySQL", bg=self.WHITE, fg=fg_c, font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(box, text=f"{MYSQL_CONFIG['host']} / {DB_NOMBRE}", bg=self.WHITE, fg=self.MUTED, wraplength=340, justify="left").pack(anchor="w", pady=(2, 10))
        self.boton(box, "Volver al inicio", lambda: self.mostrar("Inicio"), self.PURPLE, "#FFFFFF").pack(anchor="w")


class PanelDocente:
    def __init__(self, root, docente_nombre, modo_oscuro=False, grupo_fijo=None, colores_personalizados=None):
        self.root = root
        self.docente_nombre = docente_nombre
        self.grupo_fijo = grupo_fijo
        self.modo_oscuro = modo_oscuro
        self.colores_personalizados = colores_personalizados
        self.actualizar_colores()

        etiqueta_grupo = f" - Grupo {grupo_fijo}" if grupo_fijo else ""
        self.root.title(f"Primaria Nezahualcóyotl | Panel Docente - {docente_nombre}{etiqueta_grupo}")
        self.root.minsize(320, 480)
        self.root.configure(bg=self.BG)
        maximizar_ventana(self.root)
        self.pagina = "Inicio"
        self.compacto = False
        self._resize_job = None
        inicializar_base_datos_principal()
        self.obtener_grupos_docente()
        self.configurar_estilos()
        self.root.bind("<Configure>", self.detectar_tamano)
        self.crear_panel(self.pagina)

    def actualizar_colores(self):
        t = dict(TEMAS["oscuro"] if self.modo_oscuro else TEMAS["claro"])
        if isinstance(self.colores_personalizados, dict):
            t.update(self.colores_personalizados)
        self.BG = t["BG"]
        self.WHITE = t["WHITE"]
        self.NAVY = t["NAVY"]
        self.DARK = t["DARK"]
        self.PURPLE = t["PURPLE"]
        self.GOLD = t["GOLD"]
        self.GOLD_LIGHT = t.get("GOLD_LIGHT", t["GREEN_SOFT"])
        self.GOLD_DARK = t.get("GOLD_DARK", t["GOLD"])
        self.LAVENDER = t["LAVENDER"]
        self.MUTED = t["MUTED"]
        self.BORDER = t["BORDER"]
        self.BLUE_SOFT = t["BLUE_SOFT"]
        self.GREEN_SOFT = t["GREEN_SOFT"]
        self.YELLOW_SOFT = t["YELLOW_SOFT"]
        self.RED_SOFT = t["RED_SOFT"]
        self.RED = t["RED"]
        self.RED_DARK = t["RED_DARK"]
        self.TEAL = t["TEAL"]
        self.TEXT_NAV = t["TEXT_NAV"]
        self.TEXT_MAIN = t["TEXT_MAIN"]
        self.TEXT_SOFT = t["TEXT_SOFT"]

    def cambiar_tema(self):
        self.modo_oscuro = not self.modo_oscuro
        self.colores_personalizados = None
        self.actualizar_colores()
        self.configurar_estilos()
        self.crear_panel(self.pagina)

    def conectar(self, incluir_bd=True):
        return conectar_mysql(incluir_bd=incluir_bd)

    def obtener_grupos_docente(self):
        if self.grupo_fijo:
            self.grupos = [self.grupo_fijo]
            return
        with self.conectar(incluir_bd=True) as db:
            cur = db.cursor()
            if self.docente_nombre.lower() in ("docente", "todos"):
                cur.execute("SELECT grupo FROM grupos ORDER BY grupo LIMIT 1")
            else:
                cur.execute("SELECT grupo FROM grupos WHERE LOWER(docente) LIKE LOWER(%s) ORDER BY grupo LIMIT 1", (f"%{self.docente_nombre}%",))
            self.grupos = [row[0] for row in cur.fetchall()]
        if not self.grupos:
            with self.conectar(incluir_bd=True) as db:
                cur = db.cursor()
                cur.execute("SELECT grupo FROM grupos LIMIT 1")
                self.grupos = [row[0] for row in cur.fetchall()]
        if self.grupos:
            self.grupo_fijo = self.grupos[0]

    def configurar_estilos(self):
        s = ttk.Style()
        try:
            s.theme_use("clam")
        except tk.TclError:
            pass

        fg_tabla = self.TEXT_MAIN
        bg_tabla = self.WHITE
        header_bg = self.DARK if self.modo_oscuro else "#F8FAFC"
        header_fg = self.TEAL if self.modo_oscuro else "#334155"

        s.configure("Treeview", background=bg_tabla, foreground=fg_tabla,
                    fieldbackground=bg_tabla, rowheight=34, borderwidth=0, font=("Segoe UI", 9))
        s.configure("Treeview.Heading", background=header_bg, foreground=header_fg,
                    font=("Segoe UI", 9, "bold"), padding=(8, 8), relief="flat")
        s.map("Treeview", background=[("selected", self.PURPLE)], foreground=[("selected", "#FFFFFF")])
        s.configure("TCombobox", padding=6, font=("Segoe UI", 9),
                    fieldbackground=bg_tabla, background=header_bg,
                    foreground=fg_tabla, arrowcolor=fg_tabla)
        s.map("TCombobox",
              fieldbackground=[("readonly", bg_tabla)],
              foreground=[("readonly", fg_tabla)],
              selectbackground=[("readonly", self.PURPLE)],
              selectforeground=[("readonly", "#FFFFFF")])
        self.root.option_add("*TCombobox*Listbox.background", bg_tabla)
        self.root.option_add("*TCombobox*Listbox.foreground", fg_tabla)
        self.root.option_add("*TCombobox*Listbox.selectBackground", self.PURPLE)
        self.root.option_add("*TCombobox*Listbox.selectForeground", "#FFFFFF")

    def boton(self, parent, texto, comando, color=None, fg=None, compacto=True):
        col = color if color else self.PURPLE
        texto_col = fg if fg else "#FFFFFF"
        b = tk.Button(parent, text=texto, command=comando, bg=col, fg=texto_col,
                      activebackground=self.DARK, activeforeground="#FFFFFF",
                      font=("Segoe UI", 8 if compacto else 9, "bold"), bd=0, padx=11, pady=6 if compacto else 8,
                      cursor="hand2", wraplength=220, relief="flat", highlightthickness=0)
        return b

    def formulario_modal(self, titulo, campos):
        ventana = tk.Toplevel(self.root)
        ventana.title(titulo)
        ventana.configure(bg=self.BG)
        ventana.transient(self.root)
        ventana.grab_set()
        ventana.resizable(True, False)
        ventana.geometry("430x{}".format(min(580, 210 + len(campos) * 72)))

        franja = tk.Frame(ventana, bg=self.NAVY, padx=18, pady=12)
        franja.pack(fill="x")
        tk.Label(franja, text=titulo, bg=self.NAVY, fg=self.TEXT_NAV, font=("Segoe UI", 12, "bold"), wraplength=370, justify="left").pack(anchor="w")
        tk.Frame(ventana, bg=self.PURPLE, height=2).pack(fill="x")

        cuerpo = tk.Frame(ventana, bg=self.BG, padx=18, pady=14)
        cuerpo.pack(fill="both", expand=True)
        controles = {}
        fg_l = self.TEXT_MAIN
        for indice, campo in enumerate(campos):
            etiqueta, valor, opciones = campo
            tk.Label(cuerpo, text=etiqueta, bg=self.BG, fg=fg_l, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(6 if indice else 0, 3))
            if opciones:
                control = ttk.Combobox(cuerpo, values=opciones, state="readonly", font=("Segoe UI", 9))
                if valor is not None:
                    control.set(str(valor))
            else:
                control = tk.Entry(cuerpo, font=("Segoe UI", 10), bg=self.WHITE, fg=fg_l, insertbackground=fg_l, relief="flat", highlightthickness=1, highlightbackground=self.BORDER, highlightcolor=self.PURPLE, bd=0)
                if valor is not None:
                    control.insert(0, str(valor))
            control.pack(fill="x", ipady=6, pady=(0, 4))
            controles[etiqueta] = control

        pie = tk.Frame(ventana, bg=self.WHITE, padx=18, pady=11, highlightbackground=self.BORDER, highlightthickness=1)
        pie.pack(fill="x", side="bottom")
        resultado = {"valores": None}

        def guardar(event=None):
            valores = {nombre: control.get().strip() for nombre, control in controles.items()}
            if any(not valor for valor in valores.values()):
                messagebox.showwarning("Incompletos", "Completa todos los campos.", parent=ventana)
                return
            resultado["valores"] = valores
            ventana.destroy()

        def cancelar():
            ventana.destroy()

        self.boton(pie, "Cancelar", cancelar, self.BG, self.TEXT_MAIN, True).pack(side="right", padx=(8, 0))
        self.boton(pie, "Guardar", guardar, self.GOLD, "#FFFFFF", True).pack(side="right")
        ventana.bind("<Return>", guardar)
        ventana.bind("<Escape>", lambda e: cancelar())
        ventana.update_idletasks()
        x = self.root.winfo_rootx() + (self.root.winfo_width() - ventana.winfo_width()) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - ventana.winfo_height()) // 2
        ventana.geometry(f"+{max(0, x)}+{max(0, y)}")
        ventana.wait_window()
        return resultado["valores"]

    def limpiar_raiz(self):
        for w in self.root.winfo_children():
            w.destroy()

    def detectar_tamano(self, event):
        if event.widget is not self.root:
            return
        compacto = event.width < 930
        if compacto != self.compacto:
            self.compacto = compacto
            if self._resize_job:
                self.root.after_cancel(self._resize_job)
            self._resize_job = self.root.after(100, self.reconstruir_panel)

    def reconstruir_panel(self):
        if not hasattr(self, "contenido") or not self.contenido.winfo_exists():
            return
        pagina = self.pagina
        self.crear_panel(pagina)

    def cerrar_sesion(self):
        if messagebox.askyesno("Cerrar sesión", "¿Deseas salir al inicio de sesión?"):
            self.limpiar_raiz()
            PanelDireccion(self.root, self.modo_oscuro)

    def crear_panel(self, pagina="Inicio"):
        self.pagina = pagina
        self.limpiar_raiz()
        maximizar_ventana(self.root)

        grupo_actual = self.grupos[0] if self.grupos else "Sin grupo"
        menu_width = 64 if self.compacto else 210
        self.menu = tk.Frame(self.root, bg=self.NAVY, width=menu_width)
        self.menu.pack(side="left", fill="y")
        self.menu.pack_propagate(False)

        if self.compacto:
            tk.Label(self.menu, text="PN", bg=self.PURPLE, fg="#FFFFFF", font=("Segoe UI", 10, "bold"), pady=8).pack(fill="x", padx=8, pady=12)
        else:
            brand = tk.Frame(self.menu, bg=self.NAVY, padx=14, pady=16)
            brand.pack(fill="x")
            tk.Label(brand, text="PRIMARIA", bg=self.NAVY, fg=self.TEAL, font=("Segoe UI", 8, "bold")).pack(anchor="w")
            tk.Label(brand, text="Nezahualcóyotl", bg=self.NAVY, fg=self.TEXT_NAV, font=("Segoe UI", 13, "bold")).pack(anchor="w")
            tk.Label(brand, text=f"{self.docente_nombre} · {grupo_actual}", bg=self.NAVY, fg=self.MUTED, font=("Segoe UI", 8), wraplength=180, justify="left").pack(anchor="w", pady=(4, 0))

        tk.Frame(self.menu, bg=self.DARK, height=1).pack(fill="x", padx=12, pady=(0, 8))

        nav = [
            ("⌂", "Inicio"),
            ("♙", "Mis Alumnos"),
            ("✓", "Asistencia"),
            ("▤", "Justificantes"),
            ("📅", "Horario de Clases"),
            ("!", "Reportar Incidencia"),
            ("💬", "Mensajes a Dirección"),
            ("⚙", "Resumen del Grupo")]

        for icon, label in nav:
            activa = self.pagina == label
            fila_nav = tk.Frame(self.menu, bg=self.DARK if activa else self.NAVY)
            fila_nav.pack(fill="x", padx=8, pady=1)
            if activa:
                tk.Frame(fila_nav, bg=self.GOLD, width=3).pack(side="left", fill="y")
            txt = icon if self.compacto else f"{icon}  {label}"
            tk.Button(
                fila_nav,
                text=txt,
                command=lambda p=label: self.mostrar(p),
                bg=self.DARK if activa else self.NAVY,
                fg="#FFFFFF" if activa else self.TEXT_NAV,
                activebackground=self.DARK,
                activeforeground="#FFFFFF",
                font=("Segoe UI", 9, "bold" if activa else "normal"),
                bd=0,
                padx=8,
                pady=6,
                anchor="w" if not self.compacto else "center",
                cursor="hand2",
                relief="flat"
            ).pack(side="left", fill="both", expand=True)

        tk.Frame(self.menu, bg=self.NAVY).pack(fill="both", expand=True)
        tk.Frame(self.menu, bg=self.DARK, height=1).pack(fill="x", padx=10, pady=(0, 6))
        self.boton(self.menu, "⇦" if self.compacto else "Cerrar sesión", self.cerrar_sesion, self.DARK, self.TEXT_NAV, True).pack(fill="x", padx=8, pady=(0, 10))

        right_col = tk.Frame(self.root, bg=self.BG)
        right_col.pack(side="left", fill="both", expand=True)

        top = tk.Frame(right_col, bg=self.WHITE, padx=18, pady=10, highlightbackground=self.BORDER, highlightthickness=1)
        top.pack(fill="x")

        btn_tema_txt = "Modo Oscuro" if not self.modo_oscuro else "Modo Claro"
        self.boton(top, btn_tema_txt, self.cambiar_tema, self.BG, self.TEXT_MAIN, True).pack(side="right", padx=(8, 0))
        self.boton(top, "Notificaciones", self._abrir_notificaciones_doc, self.LAVENDER, self.TEXT_SOFT, True).pack(side="right", padx=(8, 0))
        tk.Label(top, text=date.today().strftime("%d/%m/%Y"), bg=self.WHITE, fg=self.MUTED, font=("Segoe UI", 9, "bold")).pack(side="right", padx=8)

        self.lbl_top_seccion = tk.Label(top, text=pagina, bg=self.WHITE, fg=self.TEXT_MAIN, font=("Segoe UI", 14, "bold"))
        self.lbl_top_seccion.pack(anchor="w")
        self.lbl_top_sub = tk.Label(top, text=f"Docente: {self.docente_nombre} · Grupo exclusivo: {grupo_actual}", bg=self.WHITE, fg=self.MUTED, font=("Segoe UI", 8))
        self.lbl_top_sub.pack(anchor="w")

        quick_bar = tk.Frame(right_col, bg=self.WHITE, padx=18, pady=6,
                             highlightbackground=self.BORDER, highlightthickness=1)
        quick_bar.pack(fill="x")
        tk.Label(quick_bar, text="Rápido:", bg=self.WHITE, fg=self.MUTED,
                 font=("Segoe UI", 8, "bold")).pack(side="left", padx=(0, 8))
        for q_txt, q_dest in [
            ("Inicio", "Inicio"),
            ("Mis Alumnos", "Mis Alumnos"),
            ("Asistencia", "Asistencia"),
            ("Justificantes", "Justificantes"),
            ("Resumen", "Resumen del Grupo"),
        ]:
            es_act = self.pagina == q_dest
            self.boton(
                quick_bar,
                q_txt,
                lambda p=q_dest: self.mostrar(p),
                self.PURPLE if es_act else self.BG,
                "#FFFFFF" if es_act else self.TEXT_MAIN,
                True
            ).pack(side="left", padx=(0, 6))

        area = tk.Frame(right_col, bg=self.BG)
        area.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(area, bg=self.BG, highlightthickness=0)
        scroll = ttk.Scrollbar(area, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.contenido = tk.Frame(self.canvas, bg=self.BG)
        self.window_id = self.canvas.create_window((0, 0), window=self.contenido, anchor="nw")
        self.contenido.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self.window_id, width=e.width))
        self.mostrar(pagina)

    def _abrir_notificaciones_doc(self):
        with self.conectar(incluir_bd=True) as db:
            cur = db.cursor()
            placeholders = ",".join(["%s"] * len(self.grupos)) if self.grupos else "'__NONE__'"
            cur.execute(
                f"SELECT COUNT(*) FROM justificantes WHERE estado='Pendiente' AND grupo IN ({placeholders})",
                tuple(self.grupos)
            )
            just_pend = cur.fetchone()[0]
            cur.execute(
                f"SELECT COUNT(*) FROM incidencias i JOIN alumnos a ON a.id = i.alumno_id WHERE i.estado='Pendiente' AND a.grupo IN ({placeholders})",
                tuple(self.grupos)
            )
            inc_pend = cur.fetchone()[0]
        abrir_ventana_notificaciones(self, self.obtener_alumnos_docente(), just_pendientes=just_pend, inc_pendientes=inc_pend)

    def titulo(self, texto, subtitulo="Gestión exclusiva de tu grupo asignado"):
        if hasattr(self, "lbl_top_seccion") and self.lbl_top_seccion.winfo_exists():
            self.lbl_top_seccion.configure(text=texto)
        if hasattr(self, "lbl_top_sub") and self.lbl_top_sub.winfo_exists():
            self.lbl_top_sub.configure(text=subtitulo)

    def seccion(self, parent, texto):
        fg_sec = self.TEXT_MAIN
        outer = tk.Frame(parent, bg=self.WHITE, highlightbackground=self.BORDER, highlightthickness=1)
        head = tk.Frame(outer, bg=self.WHITE, padx=14, pady=10)
        head.pack(fill="x")
        tk.Frame(head, bg=self.PURPLE, width=4, height=16).pack(side="left", padx=(0, 8))
        tk.Label(head, text=texto, bg=self.WHITE, fg=fg_sec, font=("Segoe UI", 10, "bold")).pack(side="left")
        tk.Frame(outer, bg=self.BORDER, height=1).pack(fill="x")
        inner = tk.Frame(outer, bg=self.WHITE, padx=14, pady=12)
        inner.pack(fill="both", expand=True)
        outer.body = inner
        return outer

    def crear_tabla(self, parent, columnas, filas, anchos=None, height=7):
        frame = tk.Frame(parent, bg=self.WHITE, highlightbackground=self.BORDER, highlightthickness=1)
        frame.pack(fill="both", expand=True)
        tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=height)
        vs = ttk.Scrollbar(frame, orient="vertical", command=tabla.yview)
        hs = ttk.Scrollbar(frame, orient="horizontal", command=tabla.xview)
        tabla.configure(yscrollcommand=vs.set, xscrollcommand=hs.set)
        vs.pack(side="right", fill="y")
        hs.pack(side="bottom", fill="x")
        tabla.pack(side="left", fill="both", expand=True)
        for col in columnas:
            tabla.heading(col, text=col)
            ancho = (anchos or {}).get(col, 100)
            tabla.column(col, width=ancho, minwidth=40, anchor="w" if col in ("Alumno", "Motivo", "Descripción", "Nota", "Título", "Asunto", "Mensaje") else "center", stretch=True)
        for fila in filas:
            tabla.insert("", "end", values=fila)
        return tabla

    def mostrar(self, pagina):
        self.pagina = pagina
        for w in self.contenido.winfo_children():
            w.destroy()
        self.canvas.yview_moveto(0)
        grupo_actual = self.grupos[0] if self.grupos else "Sin grupo"
        subtitulos = {
            "Inicio": f"Docente: {self.docente_nombre} · Grupo exclusivo: {grupo_actual}",
            "Mis Alumnos": f"Alumnos inscritos en el grupo {grupo_actual}",
            "Asistencia": f"Registro diario de asistencia · Grupo {grupo_actual}",
            "Justificantes": f"Justificantes del grupo {grupo_actual}",
            "Horario de Clases": f"Horario semanal · Grupo {grupo_actual}",
            "Reportar Incidencia": f"Incidencias de conducta · Grupo {grupo_actual}",
            "Mensajes a Dirección": f"Mensajes de {self.docente_nombre} a Dirección",
            "Resumen del Grupo": f"Estadísticas del grupo {grupo_actual}"}
        self.titulo(pagina, subtitulos.get(pagina, "Panel Docente"))
        rutas = {
            "Inicio": self.pagina_inicio_docente,
            "Mis Alumnos": self.pagina_mis_alumnos,
            "Asistencia": self.pagina_asistencia,
            "Justificantes": self.pagina_justificantes,
            "Horario de Clases": self.pagina_horario,
            "Reportar Incidencia": self.pagina_reportar_incidencia,
            "Mensajes a Dirección": self.pagina_mensajes,
            "Resumen del Grupo": self.pagina_resumen_grupo}
        rutas.get(pagina, self.pagina_inicio_docente)()

    def obtener_alumnos_docente(self):
        with self.conectar(incluir_bd=True) as db:
            cur = db.cursor()
            if not self.grupos:
                return []
            placeholders = ",".join(["%s"] * len(self.grupos))
            cur.execute(
                f"SELECT id, nombre, grupo, retardos, faltas FROM alumnos WHERE grupo IN ({placeholders}) ORDER BY grupo, nombre",
                tuple(self.grupos)
            )
            return cur.fetchall()

    def pagina_inicio_docente(self):
        grupo_actual = self.grupos[0] if self.grupos else "Sin grupo"

        sec = self.seccion(self.contenido, f"Panel exclusivo · Docente: {self.docente_nombre} · Grupo: {grupo_actual}")
        sec.pack(fill="x", padx=18, pady=(12, 8))
        box = sec.body
        btns = tk.Frame(box, bg=self.WHITE)
        btns.pack(fill="x")
        self.boton(btns, "Registrar asistencia", lambda: self.mostrar("Asistencia"), self.GOLD, "#FFFFFF").pack(side="left", padx=(0, 6))
        self.boton(btns, "Ver mis alumnos", lambda: self.mostrar("Mis Alumnos"), self.PURPLE, "#FFFFFF").pack(side="left", padx=(0, 6))
        self.boton(btns, "Reportar incidencia", lambda: self.mostrar("Reportar Incidencia"), self.RED, "#FFFFFF").pack(side="left", padx=(0, 6))
        self.boton(btns, "Resumen del grupo", lambda: self.mostrar("Resumen del Grupo"), self.LAVENDER, self.TEXT_SOFT).pack(side="left")

    def pagina_mis_alumnos(self):
        sec = self.seccion(self.contenido, f"Alumnos del grupo {', '.join(self.grupos)}")
        sec.pack(fill="both", padx=18, pady=(14, 6))
        box = sec.body
        actions = tk.Frame(box, bg=self.WHITE)
        actions.pack(fill="x", pady=(0, 8))
        self.boton(actions, "Seguimiento", self.seguimiento_docente, self.GOLD, "#FFFFFF").pack(side="left", padx=(0, 6))
        self.boton(actions, "Actualizar", lambda: self.mostrar("Mis Alumnos"), self.BG, self.TEXT_MAIN).pack(side="left")

        filas = []
        for ident, nombre, grupo, retardos, faltas in self.obtener_alumnos_docente():
            estado = "Atención" if faltas >= UMBRAL_FALTAS else "Retardos" if retardos else "Regular"
            filas.append((ident, nombre, grupo, retardos, faltas, estado))
        self.tabla_alumnos_doc = self.crear_tabla(box, ("ID", "Alumno", "Grupo", "Retardos", "Faltas", "Estado"), filas, {"Alumno": 180, "Estado": 120}, 8)
        fg_tag = self.TEXT_SOFT
        self.tabla_alumnos_doc.tag_configure("retardo", background=self.YELLOW_SOFT, foreground=fg_tag)
        self.tabla_alumnos_doc.tag_configure("falta", background=self.RED_SOFT, foreground=fg_tag)
        for item in self.tabla_alumnos_doc.get_children():
            vals = self.tabla_alumnos_doc.item(item, "values")
            if int(vals[4]) >= UMBRAL_FALTAS:
                self.tabla_alumnos_doc.item(item, tags=("falta",))
            elif int(vals[3]) > 0:
                self.tabla_alumnos_doc.item(item, tags=("retardo",))

    def seguimiento_docente(self):
        tabla = getattr(self, "tabla_alumnos_doc", None)
        if not tabla or not tabla.selection():
            messagebox.showwarning("Selecciona", "Selecciona un alumno de la tabla.")
            return
        fila = tabla.item(tabla.selection()[0], "values")
        alumno_id, nombre = int(fila[0]), fila[1]
        datos = self.formulario_modal("Registrar seguimiento", [(f"Nota para {nombre}", "", None)])
        if not datos:
            return
        nota = datos[f"Nota para {nombre}"]
        with self.conectar(incluir_bd=True) as db:
            cur = db.cursor()
            cur.execute("INSERT INTO seguimientos (alumno_id, fecha, nota) VALUES (%s, %s, %s)",
                        (alumno_id, date.today().isoformat(), nota))
            db.commit()
        messagebox.showinfo("Guardado", "Nota registrada correctamente.")
        self.mostrar("Mis Alumnos")

    def pagina_asistencia(self):
        sec = self.seccion(self.contenido, f"Registrar asistencia diaria · Grupo {', '.join(self.grupos)}")
        sec.pack(fill="x", padx=18, pady=(14, 6))
        box = sec.body
        alumnos = self.obtener_alumnos_docente()
        if not alumnos:
            tk.Label(box, text="No hay alumnos asignados.", bg=self.WHITE, fg=self.TEXT_MAIN).pack(anchor="w")
            return
        opts = {f"{a[0]} · {a[1]} ({a[2]})": a[0] for a in alumnos}
        alumno_var = tk.StringVar(value=next(iter(opts)))
        estado_var = tk.StringVar(value="Presente")
        form = tk.Frame(box, bg=self.WHITE)
        form.pack(fill="x")
        fg_l = self.TEXT_MAIN
        tk.Label(form, text="Alumno", bg=self.WHITE, fg=fg_l, font=("Segoe UI", 8, "bold")).pack(anchor="w")
        ttk.Combobox(form, textvariable=alumno_var, values=list(opts), state="readonly").pack(fill="x", pady=(2, 8))
        tk.Label(form, text="Estado", bg=self.WHITE, fg=fg_l, font=("Segoe UI", 8, "bold")).pack(anchor="w")
        ttk.Combobox(form, textvariable=estado_var, values=["Presente", "Retardo", "Falta"], state="readonly").pack(fill="x", pady=(2, 8))

        def guardar():
            alumno_id = opts.get(alumno_var.get())
            if not alumno_id:
                return
            hoy = date.today().isoformat()
            estado = estado_var.get()
            try:
                with self.conectar(incluir_bd=True) as db:
                    cur = db.cursor()
                    cur.execute("SELECT 1 FROM asistencias WHERE alumno_id=%s AND fecha=%s", (alumno_id, hoy))
                    if cur.fetchone():
                        messagebox.showwarning("Aviso", "Ya hay asistencia registrada para este alumno hoy.")
                        return
                    cur.execute("INSERT INTO asistencias (alumno_id, fecha, estado) VALUES (%s, %s, %s)",
                                (alumno_id, hoy, estado))
                    if estado == "Retardo":
                        cur.execute("UPDATE alumnos SET retardos = retardos + 1 WHERE id=%s", (alumno_id,))
                        cur.execute("SELECT retardos FROM alumnos WHERE id=%s", (alumno_id,))
                        r = cur.fetchone()[0]
                        if r % UMBRAL_FALTAS == 0:
                            cur.execute("UPDATE alumnos SET faltas = faltas + 1 WHERE id=%s", (alumno_id,))
                    elif estado == "Falta":
                        cur.execute("UPDATE alumnos SET faltas = faltas + 1 WHERE id=%s", (alumno_id,))
                    db.commit()
                messagebox.showinfo("Guardado", "Asistencia registrada correctamente.")
                self.mostrar("Asistencia")
            except MySQLError as e:
                messagebox.showerror("Error", str(e))

        btns = tk.Frame(box, bg=self.WHITE)
        btns.pack(fill="x", pady=(4, 0))
        self.boton(btns, "Guardar asistencia", guardar, self.GOLD, "#FFFFFF").pack(side="left", padx=(0, 6))
        self.boton(btns, "⬆ Carga masiva asistencia", self.carga_masiva_asistencia, self.PURPLE, "#FFFFFF").pack(side="left")

        sec_hist = self.seccion(self.contenido, "Historial reciente de asistencia")
        sec_hist.pack(fill="both", padx=18, pady=6)
        with self.conectar(incluir_bd=True) as db:
            cur = db.cursor()
            placeholders = ",".join(["%s"] * len(self.grupos)) if self.grupos else "'__NONE__'"
            cur.execute(f"""
                SELECT a.fecha, al.nombre, al.grupo, a.estado
                FROM asistencias a JOIN alumnos al ON al.id = a.alumno_id
                WHERE al.grupo IN ({placeholders})
                ORDER BY a.id DESC LIMIT 40
            """, tuple(self.grupos))
            rows = cur.fetchall()
        self.crear_tabla(sec_hist.body, ("Fecha", "Alumno", "Grupo", "Estado"), rows, {"Alumno": 180}, 6)

    def carga_masiva_asistencia(self):
        alumnos = self.obtener_alumnos_docente()
        por_id = {str(a[0]): a[0] for a in alumnos}
        por_nombre = {a[1].strip().lower(): a[0] for a in alumnos}
        estados_validos = {"presente": "Presente", "retardo": "Retardo", "falta": "Falta"}

        def procesar(filas):
            guardados = 0
            omitidos = 0
            errores = []
            try:
                with self.conectar(incluir_bd=True) as db:
                    cur = db.cursor()
                    for idx, fila in enumerate(filas, start=1):
                        if len(fila) < 2 or not fila[0] or not fila[1]:
                            errores.append(f"Fila {idx}: faltan alumno/ID o estado.")
                            continue
                        clave_al = fila[0].strip()
                        alumno_id = por_id.get(clave_al) or por_nombre.get(clave_al.lower())
                        if not alumno_id:
                            errores.append(f"Fila {idx}: alumno '{clave_al}' no encontrado en tu grupo.")
                            continue
                        estado = estados_validos.get(fila[1].strip().lower())
                        if not estado:
                            errores.append(f"Fila {idx}: estado inválido '{fila[1]}' (usa Presente, Retardo o Falta).")
                            continue
                        fecha_reg = fila[2].strip() if len(fila) >= 3 and fila[2].strip() else date.today().isoformat()
                        try:
                            datetime.strptime(fecha_reg, "%Y-%m-%d")
                        except ValueError:
                            errores.append(f"Fila {idx}: fecha inválida '{fecha_reg}' (usa AAAA-MM-DD).")
                            continue

                        cur.execute("SELECT 1 FROM asistencias WHERE alumno_id=%s AND fecha=%s", (alumno_id, fecha_reg))
                        if cur.fetchone():
                            omitidos += 1
                            continue

                        cur.execute("INSERT INTO asistencias (alumno_id, fecha, estado) VALUES (%s, %s, %s)",
                                    (alumno_id, fecha_reg, estado))
                        if estado == "Retardo":
                            cur.execute("UPDATE alumnos SET retardos = retardos + 1 WHERE id=%s", (alumno_id,))
                            cur.execute("SELECT retardos FROM alumnos WHERE id=%s", (alumno_id,))
                            r = cur.fetchone()[0]
                            if r % UMBRAL_FALTAS == 0:
                                cur.execute("UPDATE alumnos SET faltas = faltas + 1 WHERE id=%s", (alumno_id,))
                        elif estado == "Falta":
                            cur.execute("UPDATE alumnos SET faltas = faltas + 1 WHERE id=%s", (alumno_id,))
                        guardados += 1
                    db.commit()
            except MySQLError as e:
                messagebox.showerror("Error MySQL", str(e), parent=self.root)
                return None

            msg = f"Asistencias guardadas: {guardados}\nYa registradas omitidas: {omitidos}"
            if errores:
                msg += f"\nErrores ({len(errores)}):\n" + "\n".join(errores[:8])
            messagebox.showinfo("Carga masiva de asistencia", msg)
            self.mostrar("Asistencia")
            return True

        ejemplo = [[a[1], "Presente", date.today().isoformat()] for a in alumnos[:2]] or [["Bruno Navarro León", "Presente", date.today().isoformat()]]
        abrir_modal_carga_masiva(
            self,
            "Carga masiva de asistencia",
            "Registra asistencia de varios alumnos de tu grupo a la vez (puedes usar ID o nombre completo).",
            ["alumno_o_id", "estado", "fecha"],
            ejemplo,
            procesar
        )

    def pagina_justificantes(self):
        sec = self.seccion(self.contenido, "Justificantes escolares")
        sec.pack(fill="x", padx=18, pady=(14, 6))
        box = sec.body

        def registrar_justificante():
            alumnos = self.obtener_alumnos_docente()
            nombres_alumnos = [a[1] for a in alumnos]
            datos = self.formulario_modal("Registrar justificante", [
                ("Nombre del alumno", nombres_alumnos[0] if nombres_alumnos else "", nombres_alumnos if nombres_alumnos else None),
                ("Motivo", "", None)
            ])
            if not datos:
                return
            nombre_al = datos["Nombre del alumno"]
            grupo_al = next((a[2] for a in alumnos if a[1] == nombre_al), self.grupos[0])
            with self.conectar(incluir_bd=True) as db:
                cur = db.cursor()
                cur.execute("INSERT INTO justificantes (alumno, grupo, fecha, motivo) VALUES (%s, %s, %s, %s)",
                            (nombre_al, grupo_al, date.today().isoformat(), datos["Motivo"]))
                db.commit()
            messagebox.showinfo("Guardado", "Justificante registrado.")
            self.mostrar("Justificantes")

        btns = tk.Frame(box, bg=self.WHITE)
        btns.pack(fill="x")
        self.boton(btns, "＋ Registrar justificante", registrar_justificante, self.GOLD, "#FFFFFF").pack(side="left", padx=(0, 6))
        self.boton(btns, "⬆ Carga masiva justificantes", self.carga_masiva_justificantes, self.PURPLE, "#FFFFFF").pack(side="left")

        sec_list = self.seccion(self.contenido, "Justificantes de tu grupo")
        sec_list.pack(fill="both", padx=18, pady=6)
        with self.conectar(incluir_bd=True) as db:
            cur = db.cursor()
            placeholders = ",".join(["%s"] * len(self.grupos)) if self.grupos else "'__NONE__'"
            cur.execute(
                f"SELECT id, alumno, grupo, fecha, motivo, estado FROM justificantes WHERE grupo IN ({placeholders}) ORDER BY id DESC",
                tuple(self.grupos)
            )
            rows = cur.fetchall()
        self.crear_tabla(sec_list.body, ("ID", "Alumno", "Grupo", "Fecha", "Motivo", "Estado"), rows, {"Alumno": 140, "Motivo": 180}, 6)

    def carga_masiva_justificantes(self):
        alumnos = self.obtener_alumnos_docente()
        grupo_por_alumno = {a[1].strip().lower(): a[2] for a in alumnos}
        grupo_defecto = self.grupos[0] if self.grupos else "General"

        def procesar(filas):
            insertados = 0
            errores = []
            try:
                with self.conectar(incluir_bd=True) as db:
                    cur = db.cursor()
                    for idx, fila in enumerate(filas, start=1):
                        if len(fila) < 2 or not fila[0] or not fila[1]:
                            errores.append(f"Fila {idx}: faltan alumno o motivo.")
                            continue
                        nombre_al = fila[0]
                        motivo = fila[1]
                        fecha_reg = fila[2] if len(fila) >= 3 and fila[2] else date.today().isoformat()
                        estado = fila[3] if len(fila) >= 4 and fila[3] else "Pendiente"
                        grupo_al = grupo_por_alumno.get(nombre_al.lower(), grupo_defecto)
                        cur.execute(
                            "INSERT INTO justificantes (alumno, grupo, fecha, motivo, estado) VALUES (%s, %s, %s, %s, %s)",
                            (nombre_al, grupo_al, fecha_reg, motivo, estado)
                        )
                        insertados += 1
                    db.commit()
            except MySQLError as e:
                messagebox.showerror("Error MySQL", str(e), parent=self.root)
                return None

            msg = f"Justificantes importados: {insertados}"
            if errores:
                msg += f"\nErrores ({len(errores)}):\n" + "\n".join(errores[:8])
            messagebox.showinfo("Carga masiva de justificantes", msg)
            self.mostrar("Justificantes")
            return True

        ejemplo_nombre = alumnos[0][1] if alumnos else "Bruno Navarro León"
        abrir_modal_carga_masiva(
            self,
            "Carga masiva de justificantes",
            "Registra varios justificantes en lote.",
            ["alumno", "motivo", "fecha", "estado"],
            [[ejemplo_nombre, "Cita médica", date.today().isoformat(), "Pendiente"]],
            procesar
        )

    def pagina_horario(self):
        sec = self.seccion(self.contenido, "Horario de Clases Semanal")
        sec.pack(fill="both", padx=18, pady=(14, 6))
        box = sec.body
        fg_l = self.TEXT_MAIN
        grupo_actual = self.grupos[0] if self.grupos else "Sin grupo"
        tk.Label(box, text=f"Distribución de horarios para el grupo: {grupo_actual}", bg=self.WHITE, fg=fg_l, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 8))

        horario_ejemplo = [
            ("Lunes", "08:00 - 09:00", "Español", grupo_actual),
            ("Lunes", "09:00 - 10:00", "Matemáticas", grupo_actual),
            ("Martes", "08:00 - 09:00", "Ciencias Naturales", grupo_actual),
            ("Miércoles", "10:00 - 11:00", "Educación Física", grupo_actual),
            ("Jueves", "09:00 - 10:00", "Historia / Geografía", grupo_actual),
            ("Viernes", "08:00 - 09:00", "Artes y Manualidades", grupo_actual)
        ]
        self.crear_tabla(box, ("Día", "Horario", "Asignatura", "Grupo"), horario_ejemplo, {"Día": 100, "Horario": 120, "Asignatura": 160}, 6)

    def pagina_mensajes(self):
        sec = self.seccion(self.contenido, "Mensajes y Solicitudes a Dirección")
        sec.pack(fill="x", padx=18, pady=(14, 6))

        def enviar_mensaje():
            datos = self.formulario_modal("Nuevo Mensaje", [("Asunto", "", None), ("Mensaje", "", None)])
            if not datos:
                return
            with self.conectar(incluir_bd=True) as db:
                cur = db.cursor()
                cur.execute("INSERT INTO mensajes_docente (docente, fecha, asunto, mensaje) VALUES (%s, %s, %s, %s)",
                            (self.docente_nombre, date.today().isoformat(), datos["Asunto"], datos["Mensaje"]))
                db.commit()
            messagebox.showinfo("Enviado", "Mensaje enviado a la dirección correctamente.")
            self.mostrar("Mensajes a Dirección")

        self.boton(sec.body, "＋ Enviar mensaje a dirección", enviar_mensaje, self.GOLD, "#FFFFFF").pack(anchor="w")

        sec_list = self.seccion(self.contenido, "Historial de Mensajes Enviados")
        sec_list.pack(fill="both", padx=18, pady=6)
        with self.conectar(incluir_bd=True) as db:
            cur = db.cursor()
            cur.execute("SELECT fecha, asunto, mensaje FROM mensajes_docente WHERE docente=%s ORDER BY id DESC", (self.docente_nombre,))
            rows = cur.fetchall()
        if not rows:
            rows = [("2026-10-28", "Solicitud de material deportivo", "Requerimos balones para la clase de educación física.")]
        self.crear_tabla(sec_list.body, ("Fecha", "Asunto", "Mensaje"), rows, {"Asunto": 160, "Mensaje": 260}, 5)

    def pagina_reportar_incidencia(self):
        sec = self.seccion(self.contenido, "Reportar incidencia")
        sec.pack(fill="x", padx=18, pady=(14, 6))
        box = sec.body
        alumnos = self.obtener_alumnos_docente()
        if not alumnos:
            tk.Label(box, text="No hay alumnos.", bg=self.WHITE, fg=self.TEXT_MAIN).pack(anchor="w")
            return
        opts = {f"{a[0]} · {a[1]} ({a[2]})": a[0] for a in alumnos}
        alumno_var = tk.StringVar(value=next(iter(opts)))
        fg_l = self.TEXT_MAIN
        tk.Label(box, text="Alumno", bg=self.WHITE, fg=fg_l, font=("Segoe UI", 8, "bold")).pack(anchor="w")
        ttk.Combobox(box, textvariable=alumno_var, values=list(opts), state="readonly").pack(fill="x", pady=(2, 8))

        datos = [("Tipo", "", None), ("Descripción", "", None)]
        controles = {}
        for campo, val, opts_c in datos:
            tk.Label(box, text=campo, bg=self.WHITE, fg=fg_l, font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(2, 2))
            c = tk.Entry(box, font=("Segoe UI", 9), bg=self.WHITE, fg=fg_l, relief="flat", highlightthickness=1, highlightbackground=self.BORDER, highlightcolor=self.PURPLE, bd=0)
            c.pack(fill="x", ipady=5, pady=(0, 6))
            controles[campo] = c

        def guardar():
            alumno_id = opts.get(alumno_var.get())
            tipo = controles["Tipo"].get().strip()
            desc = controles["Descripción"].get().strip()
            if not tipo or not desc:
                messagebox.showwarning("Incompletos", "Completa todos los campos.")
                return
            with self.conectar(incluir_bd=True) as db:
                cur = db.cursor()
                cur.execute("INSERT INTO incidencias (alumno_id, fecha, tipo, descripcion, estado) VALUES (%s, %s, %s, %s, 'Pendiente')",
                            (alumno_id, date.today().isoformat(), tipo, desc))
                db.commit()
            messagebox.showinfo("Enviado", "Incidencia reportada a dirección.")
            self.mostrar("Reportar Incidencia")

        self.boton(box, "Enviar a dirección", guardar, self.GOLD, "#FFFFFF").pack(anchor="w", pady=(4, 0))

    def _aplicar_colores_guardados_doc(self, nuevos_colores):
        self.colores_personalizados = dict(nuevos_colores)
        self.actualizar_colores()
        self.configurar_estilos()
        self.crear_panel("Resumen del Grupo")

    def pagina_resumen_grupo(self):
        sec_col = self.seccion(self.contenido, "Personalización de colores del docente (MySQL)")
        sec_col.pack(fill="x", padx=18, pady=(14, 6))
        construir_bloque_personalizacion_colores(
            self, sec_col.body, self.docente_nombre, self._aplicar_colores_guardados_doc
        )

        sec = self.seccion(self.contenido, "Estadísticas del Grupo")
        sec.pack(fill="both", padx=18, pady=6)
        box = sec.body
        alumnos = self.obtener_alumnos_docente()
        total = len(alumnos)
        con_faltas = sum(1 for a in alumnos if a[4] >= UMBRAL_FALTAS)
        con_retardos = sum(1 for a in alumnos if a[3] > 0 and a[4] < UMBRAL_FALTAS)
        regulares = total - con_faltas - con_retardos

        fg_lbl = self.TEXT_MAIN
        tk.Label(box, text=f"Docente: {self.docente_nombre}", bg=self.WHITE, fg=fg_lbl, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=2)
        tk.Label(box, text=f"Grupo exclusivo a cargo: {', '.join(self.grupos)}", bg=self.WHITE, fg=self.MUTED, font=("Segoe UI", 8)).pack(anchor="w", pady=1)
        tk.Label(box, text=f"Total de alumnos matriculados: {total}", bg=self.WHITE, fg=fg_lbl, font=("Segoe UI", 8)).pack(anchor="w", pady=(1, 10))

        tk.Label(box, text="Distribución de Estado del Grupo", bg=self.WHITE, fg=self.PURPLE, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(4, 6))

        max_val = max(total, 1)
        categorias = [
            ("Regulares / Normales", regulares, self.GOLD),
            ("Con Retardos", con_retardos, self.TEAL),
            ("Con Faltas (Alerta)", con_faltas, self.RED)
        ]

        for label, count, color in categorias:
            fila_grafica = tk.Frame(box, bg=self.WHITE)
            fila_grafica.pack(fill="x", pady=3)
            tk.Label(fila_grafica, text=label, bg=self.WHITE, fg=fg_lbl, font=("Segoe UI", 8), width=22, anchor="w").pack(side="left")
            tk.Label(fila_grafica, text=str(count), bg=self.WHITE, fg=color, font=("Segoe UI", 9, "bold"), width=4).pack(side="right")

            barra_fondo = tk.Frame(box, bg=self.BORDER, height=12)
            barra_fondo.pack(fill="x", pady=(0, 5))
            barra_progreso = tk.Frame(barra_fondo, bg=color, height=12)
            barra_progreso.place(relx=0, rely=0, relheight=1, relwidth=min(count / max_val, 1))


if __name__ == "__main__":
    ventana = tk.Tk()
    app = PanelDireccion(ventana)
    ventana.mainloop()