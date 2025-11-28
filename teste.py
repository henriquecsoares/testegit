import streamlit as st
import shutil
import threading
from tkinter import Tk
from tkinter.filedialog import askdirectory

def select_folder_fixed() -> str | None:
    folder_selected = [None]

    def _choose_folder():
        root = Tk()
        root.withdraw()                    # Esconde janela principal
        root.wm_attributes('-topmost', True)  # Força ficar por cima
        root.focus_force()                 # Força foco
        folder = askdirectory(title="Selecione a Pasta para APAGAR")
        folder_selected[0] = folder if folder else None
        root.destroy()

    # Executa o Tkinter numa thread separada e espera
    thread = threading.Thread(target=_choose_folder, daemon=True)
    thread.start()
    thread.join(timeout=60)  # Máximo 60 segundos para escolher

    return folder_selected[0]

# ====================== APP STREAMLIT ======================
st.set_page_config(page_title="Apagador de Pastas", layout="centered")
st.title("Apagador de Pastas")

st.warning("CUIDADO! Esta app apaga pastas inteiras PERMANENTEMENTE!")

# Estado da sessão
if "path" not in st.session_state:
    st.session_state.path = None
if "confirm" not in st.session_state:
    st.session_state.confirm = False

# Botão para selecionar pasta
if st.button("Selecionar Pasta", type="primary", use_container_width=True):
    with st.spinner("A abrir seletor de pastas..."):
        folder = select_folder_fixed()
        if folder:
            st.session_state.path = folder
            st.session_state.confirm = False
            st.success(f"Pasta selecionada: {folder}")
            st.rerun()
        else:
            st.info("Nenhuma pasta selecionada ou cancelado.")

# Mostra pasta atual
if st.session_state.path:
    st.error(f"PRONTO PARA APAGAR: `{st.session_state.path}`")

    if st.button("APAGAR ESTA PASTA AGORA", type="secondary"):
        st.session_state.confirm = True

if st.session_state.confirm:
    st.error("ÚLTIMA CHANCE! Esta ação NÃO pode ser desfeita!")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("SIM, APAGAR TUDO", type="primary"):
            try:
                shutil.rmtree(st.session_state.path)
                st.success("Pasta apagada com sucesso!")
                st.balloons()
                st.session_state.path = None
                st.session_state.confirm = False
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao apagar: {e}")
    with col2:
        if st.button("Cancelar"):
            st.session_state.confirm = False
            st.rerun()