import streamlit as st
from schedule_module.fcfs import schedule_simulator
from schedule_module.mlfq import schedule_simulator

# ---------------------------------------
# Funções
# ---------------------------------------

def exibir_processo(p, emoji="🔵"):
    st.markdown(f"""
    <div style="border: 1px solid #ccc; border-radius: 10px; padding: 10px; margin-bottom: 10px;
                background-color: #000000">
        <strong>{emoji} {p['PID']}</strong><br>
        🧮 Execução: {p['Exec']}<br>
        ⌛ Espera: {p['Wait']}<br>
        {'🔁 Turnaround: ' + str(p['Turnaround']) if 'Turnaround' in p else ''}
    </div>
    """, unsafe_allow_html=True)

def new_env() -> None:
    st.session_state.simulator = schedule_simulator()
    st.session_state.simulation_vars = {
            "ready": [],
            "execute": [],
            "waiting": [],
            "finish": []
        }

# ---------------------------------------
# Inicialização
# ---------------------------------------

if "clock" not in st.session_state:
    st.session_state.clock = 1

if "simulator" not in st.session_state:
    st.session_state.simulator = schedule_simulator()

if "simulation_vars" not in st.session_state: 
    st.session_state.simulation_vars = {
            "ready": [],
            "execute": [],
            "waiting": [],
            "finish": []
        }

# ---------------------------------------
# Página
# ---------------------------------------

st.set_page_config(page_title="Simulador de Escalonamento", layout="wide")

st.title("⚙️ Simulador de Escalonamento de Processos")
st.markdown("Acompanhe em tempo real o estado das filas e métricas dos processos.")

st.subheader("Simulação")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("📥 Prontos")
    for p in st.session_state.simulation_vars["ready"]:
        exibir_processo(p, "🔵")

with col2:
    st.subheader("⏳ Espera")
    for p in st.session_state.simulation_vars["waiting"]:
        exibir_processo(p, "🟡")

with col3:
    st.subheader("🚀 Executando")
    for p in st.session_state.simulation_vars["execute"]:
        exibir_processo(p, "🟢")

with col4:
    st.subheader("✅ Finalizados")
    for p in st.session_state.simulation_vars["finish"]:
        exibir_processo(p, "⚪")

try:
    if not st.session_state.running:
        st.write("Simulação Finalizada.")
except AttributeError:
    pass

st.markdown("---")

# ---------------------------------------
# SideBar
# --------------------------------------

st.sidebar.title("Simulação")

processes = st.sidebar.number_input("Número de Processos", value=3, step=1)

if st.sidebar.button("Iniciar Simulação"):
    st.session_state.running = True
    new_env()

    for i in range(processes):
        st.session_state.simulator.create_process()

    st.session_state.simulator.start_simulation()
    st.session_state.simulation_vars = st.session_state.simulator.simulation_report()
    st.rerun()

st.sidebar.title("⏱️ Controle")
st.session_state.clock = st.sidebar.number_input("Ciclos por vez:", value=1, step=1)

if st.sidebar.button("Rodar Ciclo de Clock"):
    if st.session_state.running:
        for i in range(st.session_state.clock):
            st.session_state.simulator.execute()
            st.session_state.simulator.wait()
            st.session_state.simulation_vars = st.session_state.simulator.simulation_report()
            if st.session_state.simulator.check_finish():
                    st.session_state.running = False
    st.rerun()

if st.sidebar.button("Finalizar Simulação"):
    st.session_state.running = False
    st.rerun()

# ---------------------------------------
# Report
# --------------------------------------

# st.header("📊 Métricas de Desempenho")
# if finalizados:
#     avg_wait = sum(p["Wait"] for p in finalizados) / len(finalizados)
#     avg_turnaround = sum(p["Turnaround"] for p in finalizados) / len(finalizados)

#     st.metric("⏱️ Tempo Médio de Espera", f"{avg_wait:.2f}")
#     st.metric("🔁 Tempo Médio de Turnaround", f"{avg_turnaround:.2f}")
# else:
#     st.info("Nenhum processo finalizado ainda para calcular métricas.")

