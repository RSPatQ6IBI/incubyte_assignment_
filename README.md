"""# 💼 Incubyte Assignment: Salary Management Tool 🚀

## 📝 This is a submission to the assignment by Incubyte

---

### 🎯 Problem Statement 

#### ✨ Expectations 
This exercise is intentionally designed to assess how you think, design, and build software in an AI‑driven environment.   
   
You are required to use AI tools to accelerate your work. We care about how you use them, the clarity of your thinking, and the quality of your engineering decisions.   
   
We expect you to:   
* 🧠 **Demonstrate clarity** in thought and structured problem solving  
* 🛠️ **Show strong engineering fundamentals** & product thinking 
* 🏗️ **Make thoughtful architectural** and design decisions  
* 🧪 **Write production‑quality code** and tests  
* 🤖 **Use AI intentionally** while maintaining correctness and quality  
   
📂 *Please make incremental commits so we can understand how your solution evolved.* 🏁 **Goal:** Build a minimal yet usable salary management tool for an organization with 10,000 employees. 

#### 👥 User Persona
* 🧑‍💼 **HR Manager** of the organization 

#### 📋 Requirements
* 👤 **Managing Employees:**
    * Add, View, update, and delete employees via UI 
    * *Note:* The employee must have a full name, job title, country, salary, along with any other meaningful data that you believe should be captured.
* 📊 **Salary Insights via UI:**
    * Minimum, maximum, and average salary of employees in a country. 
    * Average salary for the given Job Title in a country. 
    * Any other meaningful metrics you believe are helpful for the user persona. 

---

### 💡 Proposed Solution 

* 🌟 Built an MVP with **Streamlit** (UI), **Python** (Backbone), and **ClickHouse** (Database).

#### 🎨 Frontend (UI)
* 💻 Built with **Streamlit**, featuring a login page (with roles for HR Manager and Guests).
* 🔓 Once logged in with proper credentials, it leads to the **Employee Management Page**.
* ➕ The UI displays options to **add and delete** desired employees. 
* 📈 The UI also displays **salary insights** and related metrics using visual representations.

#### ⚙️ Backend 
* 🐍 Built with **Python**.
    * 🔌 Manages connections with the database and handles operations such as add, delete, etc.
    * 🛠️ All adapters are maintained in `db_utils_`.

#### 🗄️ ClickHouse (DB)
* 📊 Built a database using dummy employee information contained in `employee_data_raw_txt_`.
* 🔑 Connection management is handled through user details mentioned in `pyproject.toml`.

🔒 `.env` file contains login passwords which are masked in GIT uploads using the `.gitignore` file.

---

### 🔄 Overall Flow
The application follows these illustrated routes:

Code output
File created successfully: README.md

```mermaid
graph TD;
    py_login_page_streamlit_ -->app;
    app -->establish_connection_clickhouse_
    establish_connection_clickhouse_-->prepare_data_for_table_;
    prepare_data_for_table_ -->insert_data_to_clickhouse_table_
    establish_connection_clickhouse_-->import_data_from_clickhouse_;
    app-->data_fetcher_streamlit_;
    data_fetcher_streamlit_-->UI;