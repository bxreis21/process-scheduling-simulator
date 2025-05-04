import streamlit as st
from schedule_module.fcfs import schedule_simulator as fcfs
from schedule_module.mlfq import schedule_simulator as mlfq
from web_page.fcfs_page import fcfs_simulation
from web_page.mlfq_page import mlfq_simulation
from web_page.aux_functions import *

# ---------------------------------------
# Inicialização
# ---------------------------------------

if "clock" not in st.session_state:
    st.session_state.clock = 1

if "level" not in st.session_state:
    st.session_state.level = "FCFS"

if "level_running" not in st.session_state:
    st.session_state.level_running = st.session_state.level

if "simulator" not in st.session_state:
    if st.session_state.level == "FCFS":
        st.session_state.simulator = fcfs()
    elif st.session_state.level == "MLFQ":
        st.session_state.simulator = mlfq()

if "simulation_vars" not in st.session_state: 
    st.session_state.simulation_vars = {
            "ready": [],
            "execute": [],
            "waiting": [],
            "finish": []
        }

# ---------------------------------------
# SideBar
# --------------------------------------
st.set_page_config(page_title="Simulador de Escalonamento", layout="wide")

st.sidebar.title("Simulação")

st.session_state.level = st.sidebar.selectbox("Escolha o escalonador", ["FCFS", "MLFQ"])

processes = st.sidebar.number_input("Número de Processos", value=3, step=1)

if st.sidebar.button("Iniciar Simulação"):
    new_env(st)

    st.session_state.running = True
    st.session_state.level_running = st.session_state.level

    for i in range(processes):
        st.session_state.simulator.create_process()
    
    st.session_state.simulator.initialize()
    st.session_state.simulation_vars = st.session_state.simulator.simulation_report()
    st.rerun()

st.sidebar.title("⏱️ Controle")
st.session_state.clock = st.sidebar.number_input("Ciclos por vez:", value=1, step=1)

if st.sidebar.button("Rodar Ciclo de Clock"):
    if st.session_state.running:
        for i in range(st.session_state.clock):
            st.session_state.simulator.execute()
            st.session_state.simulator.wait()
            if st.session_state.level_running == "MLFQ":
                st.session_state.simulator.update_processes_statistics()
                st.session_state.simulator.log_simulation_report(st.session_state.simulator.simulation_report(), 0)

            st.session_state.simulation_vars = st.session_state.simulator.simulation_report()
            
            if st.session_state.simulator.check_finish():
                    st.session_state.running = False
    st.rerun()

if st.sidebar.button("Finalizar Simulação"):
    st.session_state.running = False
    st.rerun()

# ---------------------------------------
# Página
# ---------------------------------------

st.title("⚙️ Simulador de Escalonamento de Processos")
st.write("Acompanhe em tempo real o estado das filas e métricas dos processos.")

if st.session_state.level == "FCFS":
    if st.session_state.level_running != st.session_state.level:
        new_env(st)
        st.session_state.running = False
        st.session_state.level_running = st.session_state.level
        st.rerun()
        
    fcfs_simulation(st)

elif st.session_state.level == "MLFQ":
    if st.session_state.level_running != st.session_state.level:
        new_env(st)
        st.session_state.running = False
        st.session_state.level_running = st.session_state.level
        st.rerun()    

    mlfq_simulation(st)

else:
    st.write("page error")
