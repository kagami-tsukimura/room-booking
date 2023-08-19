import streamlit as st

from streamlit_util.get_response import convert_rooms_to_df, get_rooms
from streamlit_util.post_response import show_response
from streamlit_util.session import session_check


def show_room_page(page_title):
    st.title("会議室登録")
    st.write("#### 会議室一覧")
    rooms = get_rooms()
    df_rooms = convert_rooms_to_df(rooms)
    st.table(df_rooms)

    with st.form(key=page_title):
        room_name: str = st.text_input("会議室名", max_chars=12)
        capacity: int = st.number_input("定員", 1, step=1)
        data = {"room_name": room_name, "capacity": capacity}
        submit_button = st.form_submit_button(label="登録")

    if submit_button:
        show_response(page_title, data)

    session_check()
