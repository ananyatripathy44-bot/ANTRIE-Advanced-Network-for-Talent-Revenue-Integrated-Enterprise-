import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. SETTING THE STAGE ---
st.set_page_config(page_title="ANTRIE | Management Portal", layout="wide", page_icon="⚡")

# Custom CSS for the "ANTRIE" aesthetic (Dark Mode, High-End Corporate)
st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .antrie-header { color: #00ffcc; font-family: 'Helvetica', sans-serif; font-weight: 800; font-size: 42px; margin-bottom: -10px; }
    .rank-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #343a40;
        background: #161b22;
        text-align: center;
    }
    .gold { border-top: 5px solid #ffd700; box-shadow: 0px 4px 15px rgba(255, 215, 0, 0.2); }
    .silver { border-top: 5px solid #c0c0c0; }
    .bronze { border-top: 5px solid #cd7f32; }
    [data-testid="stMetricValue"] { color: #00ffcc !important; font-size: 32px !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 15px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #1e293b;
        border-radius: 6px 6px 0px 0px;
        padding: 10px 25px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE MASTER DATA ---
data = [
    {"ID": "E101", "Team": "Team 1", "Name": "Ananya T.", "Dept": "Data Analysis", "Task": "Predictive Modeling", "Profit": 75000, "Expense": 12000, "WorkDays": 22, "Leaves": 1, "Status": 90, "Rating": 5.0},
    {"ID": "E104", "Team": "Team 2", "Name": "Rushitha N.", "Dept": "Tech", "Task": "Security Patching", "Profit": 68000, "Expense": 20000, "WorkDays": 23, "Leaves": 0, "Status": 100, "Rating": 5.0},
    {"ID": "E112", "Team": "Team 2", "Name": "Tanvi H.", "Dept": "Tech", "Task": "DevOps Pipeline", "Profit": 58000, "Expense": 19000, "WorkDays": 23, "Leaves": 0, "Status": 85, "Rating": 4.8},
    {"ID": "E120", "Team": "Team 5", "Name": "Anish M.", "Dept": "Tech", "Task": "Mobile App Debug", "Profit": 54000, "Expense": 17500, "WorkDays": 22, "Leaves": 1, "Status": 90, "Rating": 4.5},
    {"ID": "E102", "Team": "Team 1", "Name": "Arjun S.", "Dept": "Sales", "Task": "Client Acquisition", "Profit": 42000, "Expense": 15000, "WorkDays": 21, "Leaves": 2, "Status": 75, "Rating": 4.2},
    {"ID": "E103", "Team": "Team 2", "Name": "Aasish K.", "Dept": "Web Arch", "Task": "Database Migration", "Profit": 28000, "Expense": 8000, "WorkDays": 19, "Leaves": 4, "Status": 40, "Rating": 3.5},
]
# Dummy entries to fill out the analytics
for i in range(7, 21):
    data.append({"ID": f"E1{i:02d}", "Team": f"Team {i%5+1}", "Name": f"Employee {i}", "Dept": "General", "Task": "Support", "Profit": 20000 + (i*1200), "Expense": 7000, "WorkDays": 20, "Leaves": 1, "Status": 80, "Rating": 4.0})

df = pd.DataFrame(data)

# --- 3. BRANDED HEADER ---
st.markdown('<p class="antrie-header">ANTRIE</p>', unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8;'>Advanced Network for Talent, Revenue, & Integrated Enterprise</p>", unsafe_allow_html=True)

# --- 4. NAVIGATION TABS ---
tab_ent, tab_hr = st.tabs(["📊 Enterprise Hub", "🌟 Talent Analytics"])

# --- TAB 1: ENTERPRISE HUB (Operational View) ---
with tab_ent:
    # High Level Metrics
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total Projects", "20")
    m2.metric("In Progress", "8", delta="Active")
    m3.metric("Completed", "7", delta="High ROI")
    m4.metric("At Hold", "5", delta="-1 this week", delta_color="inverse")
    m5.metric("Net Revenue", f"₹{(df['Profit'].sum() - df['Expense'].sum()):,}")
    
    st.divider()
    
    col_l, col_r = st.columns([1, 2.5])
    
    with col_l:
        st.subheader("👥 Work Assignments")
        search = st.text_input("🔍 Quick Search", placeholder="Name or Task...")
        for t in sorted(df['Team'].unique()):
            t_df = df[df['Team'] == t]
            if search:
                t_df = t_df[t_df['Name'].str.contains(search, case=False) | t_df['Task'].str.contains(search, case=False)]
            
            with st.expander(f"📁 {t} ({len(t_df)} Members)"):
                for _, row in t_df.iterrows():
                    st.markdown(f"""
                    <div style="background:#1e293b; padding:10px; border-radius:5px; margin-bottom:5px; border-left: 3px solid #00ffcc;">
                    <small><b>{row['Name']}</b> (ID: {row['ID']})</small><br>
                    <span style="color:#fbbf24; font-size:11px;">Task: {row['Task']}</span>
                    </div>
                    """, unsafe_allow_html=True)

    with col_r:
        # Pie & Donut Row
        c_pie, c_donut = st.columns(2)
        with c_pie:
            st.markdown("### 📊 Project Distribution")
            fig_p = px.pie(names=['Completed', 'Active', 'On Hold'], values=[7, 8, 5], 
                           color_discrete_sequence=['#00ffcc', '#3b82f6', '#ff4b4b'], hole=0.4)
            fig_p.update_layout(template="plotly_dark", height=300, showlegend=False)
            st.plotly_chart(fig_p, use_container_width=True)
            
        with c_donut:
            st.markdown("### 🎯 Global Completion %")
            fig_d = go.Figure(go.Pie(labels=['Done', 'Remaining'], values=[75, 25], hole=0.75, 
                                     marker_colors=['#00ffcc', '#0f172a']))
            fig_d.update_layout(template="plotly_dark", height=300, showlegend=False,
                                annotations=[dict(text='75%', x=0.5, y=0.5, font_size=24, showarrow=False)])
            st.plotly_chart(fig_d, use_container_width=True)

        st.markdown("### 📈 Expense vs. Profit Tracking")
        fig_f = go.Figure()
        fig_f.add_trace(go.Bar(x=df['Name'].head(12), y=df['Profit'], name='Profit (₹)', marker_color='#00ffcc'))
        fig_f.add_trace(go.Scatter(x=df['Name'].head(12), y=df['Expense'], name='Expense (₹)', line=dict(color='#ff4b4b', width=3)))
        fig_f.update_layout(template="plotly_dark", height=350, margin=dict(t=10, b=10))
        st.plotly_chart(fig_f, use_container_width=True)

# --- TAB 2: TALENT ANALYTICS (Deep Dive) ---
with tab_hr:
    st.markdown("### 🏆 Top Performance Spotlight")
    top_3 = df.sort_values(by="Profit", ascending=False).head(3)
    r1, r2, r3 = st.columns(3)
    
    ranks = [("🥇 Rank #1", "gold"), ("🥈 Rank #2", "silver"), ("🥉 Rank #3", "bronze")]
    cols = [r1, r2, r3]
    for i in range(3):
        emp = top_3.iloc[i]
        cols[i].markdown(f"""<div class="rank-card {ranks[i][1]}"><h4>{ranks[i][0]}</h4>
        <b>{emp['Name']}</b><br><small>Contribution: ₹{emp['Profit']:,}</small></div>""", unsafe_allow_html=True)

    st.divider()
    
    cl_p, cr_g = st.columns([1, 2])
    with cl_p:
        st.subheader("👤 Individual Report")
        sel = st.selectbox("Select Employee", df['Name'].unique())
        u = df[df['Name'] == sel].iloc[0]
        st.write(f"**Working Days:** {u['WorkDays']} | **Leaves:** {u['Leaves']}")
        st.metric("Bonus Awarded", f"₹{(u['Profit'] * 0.05):,.0f}")
        st.progress(int(u['Status']), text=f"Progress: {u['Status']}%")

    with cr_g:
        st.subheader("🎯 Bonus vs. Profit Efficiency")
        fig_s = px.scatter(df, x="Profit", y="Rating", size="Profit", color="Team", hover_name="Name")
        fig_s.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig_s, use_container_width=True)

# --- SIDEBAR FOOTER ---
st.sidebar.image("https://img.icons8.com/fluency/96/lightning-bolt.png")
st.sidebar.title("ANTRIE Admin")
st.sidebar.markdown("---")
st.sidebar.download_button("📥 Export CSV", df.to_csv(index=False), "ANTRIE_Report.csv", "text/csv")