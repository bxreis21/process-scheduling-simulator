from schedule_module.fcfs import schedule_simulator as fcfs
from schedule_module.mlfq import schedule_simulator as mlfq

# ---------------------------------------
# Funções
# ---------------------------------------

def show_process(st, p, emoji="🔵"):
    st.markdown(f"""
    <div style="border: 1px solid #ccc; border-radius: 10px; padding: 10px; margin-bottom: 10px;
                background-color: #000000">
        <strong>{emoji} {p['PID']}</strong><br>
        🧮 Execução: {p['Exec']}<br>
        ⌛ Espera: {p['Wait']}<br>
        {'🚫 Event At: ' + str(p['Event_at']) if 'Event_at' in p else ''}
    </div>
    """, unsafe_allow_html=True)

def new_env(st) -> None:
    if st.session_state.level == "FCFS":
        st.session_state.simulator = fcfs()
        st.session_state.simulation_vars = {
            "ready": [],
            "execute": [],
            "waiting": [],
            "finish": []
        }

    elif st.session_state.level == "MLFQ":
        st.session_state.simulator = mlfq()
        st.session_state.simulation_vars = {
            "ready_1": [],
            "ready_2": [],
            "ready_3": [],
            "executing": [],
            "waiting_1": [],
            "waiting_2": [],
            "waiting_3": [],
            "finish": [],
        }
    
