import streamlit as st


def session_check():
    if hasattr(st.session_state, "create_success"):
        st.success(st.session_state.create_success)
        del st.session_state.create_success
    if hasattr(st.session_state, "update_success"):
        st.sidebar.success(st.session_state.update_success)
        del st.session_state.update_success
    if hasattr(st.session_state, "delete_success"):
        st.sidebar.success(st.session_state.delete_success)
        del st.session_state.delete_success
