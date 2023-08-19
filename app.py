from enum import Enum

import streamlit as st

from streamlit_util.bookings_page import show_bookings_page
from streamlit_util.rooms_page import show_room_page
from streamlit_util.users_page import show_user_page


class PageType(Enum):
    USER = "users"
    ROOM = "rooms"
    BOOKING = "bookings"


st.sidebar.title("Choose your page")
page = st.sidebar.selectbox("pages", [page.value for page in PageType])


if page == PageType.USER.value:
    show_user_page(page)

elif page == PageType.ROOM.value:
    show_room_page(page)

elif page == PageType.BOOKING.value:
    show_bookings_page(page)
