import streamlit as pd
import streamlit as st
##------------------------------------
## ADD PARENT DIR AND SUBDIR TO PATH 
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
for root, dirs, files in os.walk(parent_dir):
    if root not in sys.path:
        sys.path.append(root)
##------------------------------------
## FUNCTION TO CHECK LOGIN 
def check_login(username, password):
    """Helper function to validate credentials."""
    if not username.strip() or not password.strip():
        return "blank"
    if username in USER_DB and USER_DB[username] == password:
        return "success"
    return "invalid"
##------------------------------------

### Page Configuration 
st.header('Login')
st.set_page_config(page_title="Secure Login", page_icon="🔐", layout="centered")
# Sidebar navigation
st.sidebar.page_link('py_login_page_streamlit_.py', label='Login')
# st.sidebar.page_link('pages/app.py', label='Application')
### Database for portal login 
USER_DB = {"HR_1": "HR_1", "admin": "pwd123", "temp_usr": "temp_pass"}

### Prepare UI 
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown(
        "<h1 style='text-align: center;'>Welcome Back</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; color: gray;'>Please sign in to continue</p>",
        unsafe_allow_html=True,
    )
    st.write("---")

    # st.form : bundle inputs and prevent page rerenders on every keystroke
    with st.form(key="login_form", clear_on_submit=False):
        username_input = st.text_input(
            label="Username or Email",
            placeholder="Enter your username",
            autocomplete="username",
        )

        password_input = st.text_input(
            label="Password",
            placeholder="Enter your password",
            type="password",
            autocomplete="current-password",
        )

        ### Added some spacing before the button
        st.write("")
        submit_button = st.form_submit_button(
            label="Sign In", use_container_width=True
        )

    #### Processing Logic after the click
    if submit_button:
        status = check_login(username_input, password_input)
        if status == "blank":
            st.error("⚠️ Fields cannot be left blank. Please try again.")
        elif status == "invalid":
            st.error("❌ Invalid username or password. Please try again.")
        elif status == "success":
            st.success(f"🎉 Login Successful! Welcome back, {username_input}.")
            st.balloons()

            ### Store the login state in Streamlit's session state for later pages
            st.session_state["authenticated"] = True
            st.session_state["username"] = username_input

            st.success("🎉 Login Successful! Redirecting...")
            st.switch_page("pages/app.py")




