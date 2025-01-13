import streamlit as st

# Configuración principal de Streamlit
st.set_page_config(
    page_title="Análisis StatsBomb",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Función para verificar la contraseña
def check_password():
    """
    Controla el acceso a la aplicación mediante una contraseña.
    """
    def password_entered():
        # Verifica si la contraseña ingresada es correcta
        if st.session_state["password"] == "admin":  # la contraseña se puede colocar para cada uno
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Elimina la contraseña de la sesión por seguridad
        else:
            st.session_state["password_correct"] = False

    # Si el estado de la contraseña aún no se ha establecido
    if "password_correct" not in st.session_state:
        st.text_input(
            "Contraseña", type="password", on_change=password_entered, key="password"
        )
        return False
    # Si la contraseña es incorrecta
    elif not st.session_state["password_correct"]:
        st.text_input(
            "Contraseña", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Contraseña incorrecta")
        return False
    # Si la contraseña es correcta
    else:
        return True

# Página principal de la aplicación
def main():
    """
    Página principal que presenta el menú de navegación y las páginas de análisis.
    """
    st.sidebar.title("Menú de Navegación")
    st.sidebar.write("Selecciona una página desde el menú lateral.")
    st.title("Bienvenido al Análisis StatsBomb")
    st.write("Navega a las páginas de análisis para explorar los datos.")

# Ejecución principal
if __name__ == "__main__":
    # Solo permite el acceso si la contraseña es correcta
    if check_password():
        st.write("Bienvenido al análisis deportivo!")
        main()  # Ejecuta la página principal de la aplicación
