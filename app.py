import streamlit as st
import psycopg2
import pandas as pd

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

    st.success("✅ Conectado correctamente a Supabase")

except Exception as e:
    st.error(f" Error de conexión: {e}")
cursor = conn.cursor()

st.title("Sistema Gestión Logístico")

menu = st.sidebar.selectbox(
    "Menú",
    [
        "Inicio",
        "Ver Usuarios",
        "Registrar Usuario",
        "Ver Pedidos"
    ]
)

# =========================================
# INICIO
# =========================================

if menu == "Inicio":

    st.subheader("Bienvenido al sistema logístico")

    st.write("Proyecto Gestión de Bases de Datos")

# =========================================
# VER USUARIOS
# =========================================

elif menu == "Ver Usuarios":

    st.subheader("Usuarios registrados")

    query = """
    SELECT
        id_usuario,
        nombre,
        correo,
        telefono
    FROM usuarios
    """

    df = pd.read_sql(query, conn)

    st.dataframe(df)

# =========================================
# REGISTRAR USUARIO
# =========================================

elif menu == "Registrar Usuario":

    st.subheader("Registrar nuevo usuario")

    nombre = st.text_input("Nombre")
    correo = st.text_input("Correo")
    telefono = st.text_input("Teléfono")
    contrasena = st.text_input("Contraseña")

    if st.button("Guardar Usuario"):

        sql = """
        INSERT INTO usuarios
        (
            nombre,
            correo,
            telefono,
            contrasena,
            id_estado_usuario
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (
                nombre,
                correo,
                telefono,
                contrasena,
                1
            )
        )

        conn.commit()

        st.success("Usuario registrado correctamente")

# =========================================
# VER PEDIDOS
# =========================================

elif menu == "Ver Pedidos":

    st.subheader("Pedidos registrados")

    query = """
    SELECT
        p.id_pedido,
        u.nombre,
        r.ciudad_origen,
        r.ciudad_destino,
        p.fecha_pedido
    FROM pedidos p
    JOIN usuarios u
        ON p.id_usuario = u.id_usuario
    JOIN rutas r
        ON p.id_ruta = r.id_ruta
    """

    df = pd.read_sql(query, conn)

    st.dataframe(df)