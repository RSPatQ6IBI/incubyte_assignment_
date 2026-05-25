# # import streamlit as st

# # st.title("My Web Frontend")

# # # Create a text box
# # user_name = st.text_input("Enter your user name:")
# # user_pswd = st.text_input("Enter your password:")

# # # Create a button
# # if st.button("Login"):
# #     if user_name:
# #         st.write(f"Hello, {user_name}!")
# #     else:
# #         st.warning("Please enter a name first.")


import streamlit as pd
import streamlit as st

# 1. Page Configuration (Must be the first Streamlit command)
st.set_page_config(page_title="Secure Login", page_icon="🔐", layout="centered")

# Database for portal login 
USER_DB = {"HR_1": "HR_1", "admin": "pwd123", "temp_usr": "temp_pass"}


def check_login(username, password):
    """Helper function to validate credentials."""
    if not username.strip() or not password.strip():
        return "blank"
    if username in USER_DB and USER_DB[username] == password:
        return "success"
    return "invalid"


# 2. Centering the Login Box visually using columns
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Header Section
    st.markdown(
        "<h1 style='text-align: center;'>Welcome Back</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; color: gray;'>Please sign in to continue</p>",
        unsafe_allow_html=True,
    )
    st.write("---")

    # 3. Use st.form to bundle inputs and prevent page rerenders on every keystroke
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

        # Added some spacing before the button
        st.write("")

        # Every form needs a submit button
        submit_button = st.form_submit_button(
            label="Sign In", use_container_width=True
        )

    # 4. Processing Logic after the click
    if submit_button:
        status = check_login(username_input, password_input)

        if status == "blank":
            st.error("⚠️ Fields cannot be left blank. Please try again.")

        elif status == "invalid":
            st.error("❌ Invalid username or password. Please try again.")

        elif status == "success":
            st.success(f"🎉 Login Successful! Welcome back, {username_input}.")
            st.balloons()
            
            # Store the login state in Streamlit's session state for later pages
            st.session_state["authenticated"] = True
            st.session_state["username"] = username_input

            st.success("🎉 Login Successful! Redirecting...")
            # 2. Switch to the dashboard page instantly
            # st.switch_page("pages/dashboard.py")
            st.switch_page("pages/app.py")

            # Optional: Add a button to redirect or proceed to the main app dashboard
            # st.switch_page("pages/dashboard.py")



