import streamlit as st
import psycopg2
import pandas as pd

# ---- APP LAYOUT ---- #
st.set_page_config(page_title="University Dashboard", layout="wide")
st.title("🎓 University Data Dashboard")

# ---- DATABASE CONNECTION ---- #
connection_string = "postgresql://postgres:Shishir25@db.wflynxobpzhvylqdkupe.supabase.co:5432/postgres"

def get_connection():
    return psycopg2.connect(connection_string)

def run_query(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

st.title("Supabase PostgreSQL Connection Test")

try:
    conn = get_connection()
    st.success("Connected to Supabase successfully!")
    conn.close()
except Exception as e:
    st.error("Connection failed!")
    st.error(e)


# ---- SIDEBAR NAVIGATION ---- #
page = st.sidebar.selectbox("Choose Page", [
    "Home",
    "View Students",
    "Course Statistics",
    "Attendance Overview",
    "Custom Query Explorer"
])

# ---- PAGES ---- #

if page == "Home":
    st.subheader("Welcome!")
    st.write("""
        This dashboard lets you explore student data, course enrollments, attendance insights, 
        and more from a PostgreSQL-backed university database.
    """)

elif page == "View Students":
    st.subheader("📘 Students List")
    major_filter = st.text_input("Filter by Major (optional):")
    query = "SELECT * FROM Students"
    if major_filter:
        query += f" WHERE Major ILIKE '%{major_filter}%'"
    st.dataframe(run_query(query))

elif page == "Course Statistics":
    st.subheader("📊 Course Enrollment Stats")
    df = run_query("""
        SELECT c.Title, COUNT(e.StudentID) AS Enrolled_Students
        FROM Courses c
        LEFT JOIN Enrollments e ON c.CourseID = e.CourseID
        GROUP BY c.Title
        ORDER BY Enrolled_Students DESC
        LIMIT 20;
    """)
    st.bar_chart(df.set_index("title"))

elif page == "Attendance Overview":
    st.subheader("📅 Attendance Summary")
    date = st.date_input("Pick a Date")
    df = run_query(f"""
        SELECT s.Name, c.Title, a.Status
        FROM Attendance a
        JOIN Students s ON a.StudentID = s.StudentID
        JOIN Courses c ON a.CourseID = c.CourseID
        WHERE a.Date = '{date}';
    """)
    st.dataframe(df)

elif page == "Custom Query Explorer":
    st.subheader("🧪 Custom Query")
    custom_query = st.text_area("Enter your SQL Query", height=150)
    if st.button("Run Query"):
        try:
            result = run_query(custom_query)
            st.dataframe(result)
        except Exception as e:
            st.error(f"Error: {e}")
