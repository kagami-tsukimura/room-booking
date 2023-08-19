import streamlit as st

import streamlit_util.post_response as post_response


def show_room_page(page_title):
    st.title("会議室登録")
    with st.form(key=page_title):
        room_name: str = st.text_input("会議室名", max_chars=12)
        capacity: int = st.number_input("定員", 1, step=1)
        data = {"room_name": room_name, "capacity": capacity}
        submit_button = st.form_submit_button(label="登録")

    if submit_button:
        post_response.show_response(page_title, data)

    session_check()


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
