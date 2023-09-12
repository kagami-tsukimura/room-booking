import streamlit as st


def session_check():
    if hasattr(st.session_state, "create_success"):
        st.toast(st.session_state.create_success, icon="📘")
        del st.session_state.create_success
    if hasattr(st.session_state, "update_success"):
        st.toast(st.session_state.update_success, icon="📗")
        del st.session_state.update_success
    if hasattr(st.session_state, "delete_success"):
        st.toast(st.session_state.delete_success, icon="📕")
        del st.session_state.delete_success
