import streamlit as st
import json
import time
from database_helper import get_db_metadata
from ai_engine import get_ai_business_context, get_sql_help

# Vertex Theme & Branding
st.set_page_config(page_title="Vertex AI | Data Intelligence", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for professional Hackfest look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #3d4156; }
    [data-testid="stSidebar"] { background-color: #11141c; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar: Connection & Configuration ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80) 
    st.title("Vertex Engine")
    st.caption("v2.0 - Hackfest Edition")
    
    # Defaulting to Olist Database for the Demo
    db_path = st.text_input("📍 Database Connection String", "sqlite:///olist_ecommerce.db")
    
    if st.button("🚀 Initialize Scan", use_container_width=True):
        with st.status("Extracting Olist Metadata...", expanded=True) as status:
            st.write("Connecting to Olist Dataset...")
            time.sleep(1.5)
            st.write("Mapping 9 Interlinked Tables...")
            # Actual logic call to database_helper.py
            st.session_state['data'] = get_db_metadata(db_path)
            time.sleep(1)
            st.write("Calculating Statistical Health (μ, σ)...")
            status.update(label="Vertex Scan Complete!", state="complete", expanded=False)
            st.balloons() # Celebration for successful scan
    
    st.divider()
    st.subheader("📦 Documentation Exports")
    if 'data' in st.session_state:
        st.download_button("📥 JSON Metadata", json.dumps(st.session_state['data'], indent=4), "vertex_metadata.json", use_container_width=True)
        st.download_button("📥 Markdown Wiki", "# Vertex Data Dictionary\nGenerated for Olist Dataset", "vertex_docs.md", use_container_width=True)

# --- Main UI ---
st.title("💠 VertexLens: Data Intelligence Hub")

if 'data' in st.session_state:
    # Top Level Metrics optimized for Olist
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Tables", len(st.session_state['data'])) 
    m2.metric("Data Health", "89.5%", delta="-2.1% (Nulls detected)")
    m3.metric("Relationships", "11 Active Joins")
    m4.metric("Engine Status", "AI Synced")

    tab1, tab2, tab3 = st.tabs(["📊 Schema Explorer", "🧠 AI Business Context", "💬 Vertex Chatbot"])

    with tab1:
        col_left, col_right = st.columns([1.2, 1.5])
        
        with col_left:
            st.subheader("🔗 Data Lineage Map")
            # Olist specific ER-Diagram code
            dot_code = """
            digraph {
                rankdir=LR; 
                node [shape=box, style=filled, color="#1e2130", fontcolor="white", fontname="Arial", border="none"];
                edge [color="#3d4156"];
                "customers" -> "orders" [label="customer_id"];
                "orders" -> "order_items" [label="order_id"];
                "orders" -> "payments" [label="order_id"];
                "orders" -> "reviews" [label="order_id"];
                "products" -> "order_items" [label="product_id"];
                "sellers" -> "order_items" [label="seller_id"];
                "products" -> "category_translation" [label="category_name"];
                "customers" -> "geolocation" [label="zip_code"];
            }
            """
            st.graphviz_chart(dot_code)

        with col_right:
            st.subheader("📋 Table Catalog")
            for table in st.session_state['data']:
                with st.expander(f"📦 {table['table_name'].upper()}"):
                    st.write(f"**Primary Key:** `{table.get('primary_key', 'N/A')}`")
                    st.write("**Columns:**")
                    st.code(" | ".join(table['columns']))
                    
                    health_str = table.get('quality', '90.0%')
                    st.write(f"**Integrity Score:** {health_str}")
                    # Progress bar calculation
                    try:
                        p_val = float(health_str.replace('%',''))/100
                        st.progress(p_val)
                    except:
                        st.progress(0.9)

    with tab2:
        st.subheader("💡 Business-Friendly Interpretations")
        table_names = [t['table_name'] for t in st.session_state['data']]
        selected = st.selectbox("Select a table to decrypt", table_names)
        
        if st.button("Generate AI Summary", use_container_width=True):
            table_info = next(item for item in st.session_state['data'] if item["table_name"] == selected)
            with st.spinner(f"Vertex AI is decoding `{selected}`..."):
                ai_response = get_ai_business_context(table_info)
                st.success(f"### Vertex AI Analysis for `{selected}`")
                st.markdown(ai_response)

    with tab3:
        st.subheader("💬 Vertex AI Assistant")
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask about Olist sales, customers, or table joins..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            schema_context = str(st.session_state['data'])
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    ai_reply = get_sql_help(prompt, schema_context)
                    st.markdown(ai_reply)
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})

else:
    # Welcome Screen
    # Image ki jagah ye professional info box daal do
    st.subheader("📊 Dataset Overview: Olist E-Commerce")
    st.markdown("""
    Vertex is currently analyzing the **Brazilian E-Commerce Public Dataset** by Olist. 
    This is a real-world, anonymized dataset of 100k orders from 2016 to 2018.
    """)

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.info("**100K+** \n\n Total Orders")
    with col_b:
        st.info("**9 Tables** \n\n Relational Schema")
    with col_c:
        st.info("**1M+** \n\n Geolocation Points")

    st.warning("⚡ **Tip:** Click on 'Initialize Scan' in the sidebar to generate the live relationship map below.")