from web_page.aux_functions import *

def fcfs_simulation(st):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.subheader("📥 Prontos")
        for p in st.session_state.simulation_vars["ready"]:
            show_process(st, p, "🔵")

    with col2:
        st.subheader("⏳ Espera")
        for p in st.session_state.simulation_vars["waiting"]:
            show_process(st, p, "🟡")

    with col3:
        st.subheader("🚀 Executando")
        for p in st.session_state.simulation_vars["execute"]:
            show_process(st, p, "🟢")

    with col4:
        st.subheader("✅ Finalizados")
        for p in st.session_state.simulation_vars["finish"]:
            show_process(st, p, "⚪")

    st.markdown("---")