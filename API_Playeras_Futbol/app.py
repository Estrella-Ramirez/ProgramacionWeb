import streamlit as st
import requests

st.set_page_config(page_title="Football Store", layout="wide")

if "carrito" not in st.session_state:
    st.session_state.carrito = []
if "filtro" not in st.session_state:
    st.session_state.filtro = "TODOS"

st.markdown("""
<style>
.stApp { 
    background: linear-gradient(rgba(0,0,0,0.40), rgba(0,0,0,0.60)), url("https://images.unsplash.com/photo-1489944440615-453fc2b6a9a9?q=80&w=2000");
    background-size: cover; background-attachment: fixed; background-position: center;
}
#MainMenu, header, footer {visibility:hidden;}
.card { background: rgba(18,18,18,0.88); border:1px solid #333; border-radius:16px; padding:16px; }
.card-img { background:#0e0e0e; height:260px; display:flex; align-items:center; justify-content:center; border-radius:10px; }
.card-img img { max-height:90%; max-width:90%; }
.stButton>button { width:100%; border-radius:20px!important; border:1px solid #E8C76A!important; color:#E8C76A!important; background:transparent!important; }
.stButton>button:hover { background:#E8C76A!important; color:black!important; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:white; letter-spacing:3px;'>TIENDA DE FUTBOL</h1>", unsafe_allow_html=True)

c1,c2,c3,c4,c5 = st.columns(5)
with c1:
    if st.button("INICIO", use_container_width=True): st.session_state.filtro="TODOS"
with c2:
    if st.button("CAMISETAS", use_container_width=True): st.session_state.filtro="CAMISETAS"
with c3:
    if st.button("NUEVO", use_container_width=True): st.session_state.filtro="NUEVO"
with c4:
    if st.button("COLECCIONES", use_container_width=True): st.session_state.filtro="COLECCIONES"
with c5:
    st.markdown(f"<div style='text-align:right; color:white; margin-top:8px;'>Carrito: {len(st.session_state.carrito)}</div>", unsafe_allow_html=True)

st.markdown(f"<h2 style='text-align:center; color:white;'>Playeras Deportivas</h2><p style='text-align:center; color:#ddd;'>Filtro actual: {st.session_state.filtro} • Coleccion 24/25 • Envio gratis</p>", unsafe_allow_html=True)

try:
    playeras = requests.get("http://127.0.0.1:8000/playeras", timeout=2).json()
except:
    playeras = []

if st.session_state.filtro != "TODOS":
    playeras = [p for p in playeras if p["tipo"] == st.session_state.filtro]

cols = st.columns(3, gap="large")
for i, p in enumerate(playeras):
    with cols[i % 3]:
        st.markdown(f'''
        <div class="card">
            <div class="card-img"><img src="{p["imagen"]}"></div>
            <div style="color:white; margin-top:12px;"><b>{p["nombre"]}</b></div>
            <div style="display:flex; justify-content:space-between; margin-top:10px; margin-bottom:12px;">
                <span style="color:white; font-weight:800;">€{p["precio"]}</span>
                <span style="color:#6fcf97; font-size:10px;">Stock: {p["stock"]}</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        if st.button(f"Agregar - €{p['precio']}", key=f"btn_{p['id']}"):
            st.session_state.carrito.append(p)
            st.toast(f"{p['equipo']} agregada!")
            st.rerun()

if len(st.session_state.carrito) > 0:
    st.markdown("---")
    st.markdown(f"<h2 style='color:white;'>Tu Carrito ({len(st.session_state.carrito)} productos)</h2>", unsafe_allow_html=True)
    resumen = {}
    for item in st.session_state.carrito:
        id_item = item['id']
        if id_item not in resumen:
            resumen[id_item] = {"nombre": item['nombre'], "precio": item['precio'], "cantidad": 0}
        resumen[id_item]["cantidad"] += 1

    total_final = 0
    for id_item, data in resumen.items():
        subtotal = data['precio'] * data['cantidad']
        total_final += subtotal
        st.markdown(f"""
        <div style='color:white; background:rgba(0,0,0,0.6); padding:12px; border-radius:10px; margin-bottom:8px; display:flex; justify-content:space-between;'>
            <span><b>{data['nombre']}</b> x{data['cantidad']}</span>
            <span>€{data['precio']} c/u | <b style='color:#E8C76A;'>Subtotal: €{round(subtotal,2)}</b></span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"<h2 style='color:#E8C76A; text-align:right;'>TOTAL A PAGAR: €{round(total_final,2)}</h2>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Vaciar Carrito", use_container_width=True):
            st.session_state.carrito = []
            st.rerun()
    with col_b:
        if st.button("Pagar Ahora", use_container_width=True):
            st.balloons()
            st.success(f"¡Compra realizada! Total pagado: €{round(total_final,2)}")
            st.session_state.carrito = []
            