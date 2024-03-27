import streamlit as st


import datetime
import pandas as pd
import json
# from signals import Core
from backend import *
from userbackend import *
from boot import *

st.sidebar.title("Karthik's Dashboard")

# reader = Core()
backend = userRepo()
ubk = userBackend()
if 'login_state' not in st.session_state:
    st.session_state.login_state = False
if 'add_new_user_state' not in st.session_state:
    st.session_state.add_new_user_state = False
if 'save_state' not in st.session_state:
    st.session_state.save_state = False
if 'user_form_data' not in st.session_state:
    st.session_state.user_form_data = {
        'userName': '',
        'password': '',
        'phone': '',
        'appKey': '',
        'token': '',
        'vc': '',
        'imei': '',
    }

aUser = "A"
aPass = "B"

left_column, right_column = st.columns(2)
adminUserName = st.text_input(label='Admin User Name', value="A")
adminUserPassword = st.text_input(label='Admin User Password', value="B")

if st.button('Login'):
    if adminUserName == aUser and adminUserPassword == aPass:
        st.success("Login successful!")
        st.session_state.login_state = True
    else:
        st.error("Login failed!")

if st.session_state.login_state:
    spy = ShoonyaApiPy()
    # addNewUser = st.button('Add New User')
    # submitted = False
    # if addNewUser:
    #     print("Trying to add")
    #
    #     with st.form("user_data_form"):
    #         print("Form open")
    #
    #         user_name = st.text_input("User Name")
    #         password = st.text_input("Password")#, type="password")
    #         phone = st.text_input("Phone")#, value="1234512345")
    #         app_key = st.text_input("App Key")#, value="632b447eada0340705dd4318db03ce5f")
    #         token = st.text_input("Token")#, value="6755I3PZ6L6GE2K7KBU2G2373Y2565H6")
    #         vc = st.text_input("Vendor Code")
    #         imei = st.text_input("IMEI")#, value="abcd1234")
    #
    #         submitted = st.form_submit_button(label="Save")
    #         print("SUBMIT23456", submitted)
    #         submitted=True
    #
    #     print("SUBMIT", submitted)
    # all_fields_filled = False
    # if submitted:
    #     print("CLickeededed")
    #     st.session_state.save_state = True
    #     all_fields_filled = all([user_name, password, phone, app_key, token, vc, imei]) and not any(
    #         len(field) == 0 for field in [user_name, password, phone, app_key, token, vc, imei])
    #     all_fields_filled=True
    #     # all_fields_filled = len(user_name) !=0 and len(password) !=0
    #
    # print("State - ", st.session_state.save_state, "All fields ", all_fields_filled)
    # if st.session_state.save_state and all_fields_filled:
    #     print("State - ", st.session_state.save_state, "All fields ", all_fields_filled)
    #
    #     print("Submitting")
    #     print("Token is ", token)
    #
    #     backend.saveNewUser(user_name, password, phone, app_key, token)
    #     st.success("Credentials saved successfully.")

    allUsers = backend.findAllUsers()
    accounts = st.sidebar.selectbox("Select Account", (
        allUsers))

    selectedUser = accounts[0]
    # selectedUserPositions = accounts[0]

    loginUser = st.button('Test login to user ', selectedUser)
    positionsUser = st.button('Fetch Live Positions ')
    killSwtich = st.button('Kill Strategy/SQ Off ')
    pnl = st.button('P&L ')
    orderBook = st.button('OrderBook ')

    if loginUser:
        details = backend.findByUserName(selectedUser)
        totp = spy.generateTotp(details.token)
        st.write("Live TOTP ->", totp)

    if positionsUser:
        details = backend.findByUserName(selectedUser)
        user_name = details.username
        password = details.password
        token = details.token
        vc = details.username + "_U"
        app_key = details.key
        imei = "abcd1234"
        api = ubk.login(user_name, password, token, vc, app_key, imei)

        print("Logging", api)

        # st.write("POSITIONS ->",ubk.positions(user_name))
        # st.write("OBK ->",ubk.orderBook(user_name))

# option = st.sidebar.selectbox("Looking for Strategy?", (
#     '5-EMA', 'Iron Fly', 'Short Straddle', 'Short Strangle', 'Call Ladder', 'Put Ladder'))
#

#
#
# if option == '5-EMA':
#     stock = st.text_input(label='user name', value='FA137726')
#     # ssp1=st.text_input(label='Strike Price',value='15000')
#     qty = st.text_input(label='Qty', value='75')
#     # exp=st.text_input(label='Expiry',value='20210708')
#     type = st.selectbox("Intraday/Delivery?", ('I', 'D'))
#     pr = st.button('Kill Strategy New')
#     lc, rc = st.columns(2)
#     premium = lc.button('Kill Strategy')
#     livePosition = rc.button('Check Live Positions Levels')
#     # if livePosition:
#     #     livePositions = reader.getOrderMap()
#     #     st.write("Today's active positions are ", livePositions)
#     if pr:
#         print("Killing all existing positions ")
#         st.write("Killing all existing positions ")
#
# elif option == 'Iron Fly':
#     left_column, right_column = st.columns(2)
#     premium = left_column.button('Kill Strategy')
#     livePosition = left_column.button('Check Live Positions Levels')
#     if livePosition:
#         st.title("Welcome to the Next Page")
#         # livePositions = reader.getOrderMap()
#         st.write("Today's active positions are ", "TRRRR")
#     if premium:
#         print("Killing all existing positions ")
#         st.title("Welcome to the Next Page")
#         st.write("Killing all existing positions ")
