from web_page.aux_functions import *

def mlfq_simulation(st):

    col_exec, col_finish = st.columns(2)

    with col_exec:
        st.subheader("🚀 Executando")

        for p in st.session_state.simulation_vars["executing"]:
            show_process(st, p, "🟢")

    with col_finish:
        st.subheader("✅ Finalizados")

        with st.expander("Expandir"):
            for p in st.session_state.simulation_vars["finish"]:
                show_process(st, p, "⚪", finish=True)

    st.markdown("---")

    col_ready, col_wait = st.columns(2)
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col_ready:
        st.subheader("🎯 Filas MLFQ")

        with col1:
            st.subheader("🐇 Alta Prioridade")
            for p in st.session_state.simulation_vars["ready_1"]:
                show_process(st, p, "🔵")
        
        with col2:
            st.subheader("🐕 Média Prioridade")
            for p in st.session_state.simulation_vars["ready_2"]:
                show_process(st, p, "🔵")
            
        with col3:
            st.subheader("🐢 Baixa Prioridade")
            for p in st.session_state.simulation_vars["ready_3"]:
                show_process(st, p, "🔵")

    with col_wait:
        st.subheader("🔄 Tipos de E/S")

        with col4:
            st.subheader("🖨️ Impressora")
            for p in st.session_state.simulation_vars["waiting_1"]:
                show_process(st, p, "🟡")
        
        with col5:
            st.subheader("📼 Fita Magnética")
            for p in st.session_state.simulation_vars["waiting_2"]:
                show_process(st, p, "🟡")

        with col6:
            st.subheader("💽 Disco")
            for p in st.session_state.simulation_vars["waiting_3"]:
                show_process(st, p, "🟡")

    st.markdown("---")
