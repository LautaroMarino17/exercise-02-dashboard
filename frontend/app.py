import os
import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

API_URL = os.getenv("API_URL", "http://api:8080")

st.set_page_config(page_title="Node Registry nodes")
st_autorefresh(interval=3000, key="autorefresh")

st.title("Node Registry Dashboard")

# Health indicator
try:
    health = requests.get(f"{API_URL}/health", timeout=3).json()
    st.success(f"API: {health['status']} | DB: {health['db']} | Active nodes: {health['nodes_count']}")
except Exception:
    st.error("API unreachable")

# Node list
st.header("Registered Nodes")
try:
    nodes = requests.get(f"{API_URL}/api/nodes", timeout=3).json()
    if nodes:
        st.table(nodes)
    else:
        st.info("No nodes registered yet.")
except Exception:
    st.error("Could not fetch nodes.")

# Register form
st.header("Register Node")
with st.form("register"):
    name = st.text_input("Name")
    host = st.text_input("Host")
    port = st.number_input("Port", min_value=1, max_value=65535, value=8080)
    submitted = st.form_submit_button("Register")
    if submitted:
        try:
            r = requests.post(f"{API_URL}/api/nodes", json={"name": name, "host": host, "port": int(port)}, timeout=3)
            if r.status_code == 201:
                st.success(f"Node '{name}' registered!")
                st.rerun()
            else:
                st.error(r.json().get("detail", "Error"))
        except Exception as e:
            st.error(str(e))

# Delete node
st.header("Delete Node")
del_name = st.text_input("Node name to delete")
if st.button("Delete"):
    try:
        r = requests.delete(f"{API_URL}/api/nodes/{del_name}", timeout=3)
        if r.status_code == 204:
            st.success(f"Node '{del_name}' deleted.")
            st.rerun()
        else:
            st.error(r.json().get("detail", "Error"))
    except Exception as e:
        st.error(str(e))
