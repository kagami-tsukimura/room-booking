import streamlit as st

import streamlit_util.post_response as post_response


def show_user_page(page_title):
    st.title("ユーザー登録")
    with st.form(key=page_title):
        user_name: str = st.text_input("ユーザー名", max_chars=12)
        data = {"user_name": user_name}
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
