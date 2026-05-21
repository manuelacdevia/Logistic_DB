import streamlit as st
import psycopg2
import pandas as pd

# =========================
# CONEXIÓN
# =========================
try:
    conn = psycopg2.connect(
        host="aws-1-us-east-1.pooler.supabase.com",
        database="postgres",
        user="postgres.hexlzmqtkahdmxsmwexq",
        password="LaQ5TWeZM9IoBRnK",
        port="6543",
        sslmode="require",
        connect_timeout=10
    )

    cursor = conn.cursor()
    st.success("✅ Conectado a Supabase")

except Exception as e:
    st.error(f"❌ Error de conexión: {e}")
    st.stop()

# =========================
# LOGIN
# =========================
st.title("Sistema Gestión Logístico")

if "user" not in st.session_state:

    st.subheader("Iniciar sesión")

    correo = st.text_input("Correo")
    clave = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):

        cursor.execute("""
            SELECT id_usuario, nombre, rol_usuario
            FROM usuarios
            WHERE correo=%s AND contrasena=%s
        """, (correo, clave))

        user = cursor.fetchone()

        if user:
            st.session_state["user"] = user
            st.rerun()
        else:
            st.error("Credenciales incorrectas")

    st.stop()

# =========================
# PROTECCIÓN DE SESIÓN (🔥 FIX IMPORTANTE)
# =========================
if "user" not in st.session_state:
    st.warning("Debes iniciar sesión primero")
    st.stop()

user = st.session_state["user"]

st.sidebar.success(f"Usuario: {user[1]}")
st.sidebar.info(f"Rol: {user[2]}")

rol = user[2]

# =========================
# MENÚ POR ROLES
# =========================
if rol == "admin_logistica":

    menu = st.sidebar.selectbox(
        "Menú",
        ["Inicio", "Ver Usuarios", "Registrar Usuario", "Ver Pedidos", "Auditoría"]
    )

elif rol == "operador_logistica":

    menu = st.sidebar.selectbox(
        "Menú",
        ["Inicio", "Registrar Usuario", "Ver Pedidos"]
    )

else:

    menu = st.sidebar.selectbox(
        "Menú",
        ["Inicio", "Ver Pedidos"]
    )

# =========================
# INICIO
# =========================
if menu == "Inicio":
    st.subheader("Bienvenido al sistema logístico")

# =========================
# VER USUARIOS (ADMIN)
# =========================
elif menu == "Ver Usuarios":

    st.subheader("Usuarios registrados")

    df = pd.read_sql("""
        SELECT id_usuario, nombre, correo, telefono
        FROM usuarios
    """, conn)

    st.dataframe(df)

# =========================
# REGISTRAR USUARIO
# =========================
elif menu == "Registrar Usuario":

    st.subheader("Registrar nuevo usuario")

    nombre = st.text_input("Nombre")
    correo = st.text_input("Correo")
    telefono = st.text_input("Teléfono")
    contrasena = st.text_input("Contraseña")

    if st.button("Guardar Usuario"):

        cursor.execute("""
            INSERT INTO usuarios
            (nombre, correo, telefono, contrasena, rol_usuario)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, correo, telefono, contrasena, "consulta_logistica"))

        conn.commit()
        st.success("Usuario registrado correctamente")

# =========================
# VER PEDIDOS
# =========================
elif menu == "Ver Pedidos":

    st.subheader("Pedidos registrados")

    df = pd.read_sql("""
        SELECT p.id_pedido, u.nombre, r.ciudad_origen, r.ciudad_destino, p.fecha_pedido
        FROM pedidos p
        JOIN usuarios u ON p.id_usuario = u.id_usuario
        JOIN rutas r ON p.id_ruta = r.id_ruta
    """, conn)

    st.dataframe(df)

# =========================
# AUDITORÍA (ADMIN)
# =========================
elif menu == "Auditoría":

    st.subheader("Registro de actividades")

    df = pd.read_sql("""
        SELECT *
        FROM auditoria
        ORDER BY fecha DESC
    """, conn)

    st.dataframe(df)

# =========================
# LOGOUT
# =========================
if st.sidebar.button("Cerrar sesión"):
    del st.session_state["user"]
    st.rerun()