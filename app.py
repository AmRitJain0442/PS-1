<<<<<<< HEAD
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def load_data(query, params=None):
    conn = sqlite3.connect('station_data_v2.db')
    if params:
        df = pd.read_sql_query(query, conn, params=params)
    else:
        df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def main():
    st.set_page_config(
        page_title="Station Data Analytics",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stMetric {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            transition: all 0.3s ease;
        }
        .stMetric:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .stDataFrame {
            border-radius: 0.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .css-1d391kg {
            padding: 1rem;
        }
        .stSelectbox, .stRadio {
            background-color: #1e1e1e;
            border-radius: 0.5rem;
            padding: 0.5rem;
        }
        .stButton>button {
            width: 100%;
            border-radius: 0.5rem;
            padding: 0.5rem;
            background-color: #4CAF50;
            color: white;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #45a049;
            transform: translateY(-1px);
        }
        .info-box {
            background-color: #1e1e1e;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
        }
        .stExpander {
            background-color: #1e1e1e !important;
            border: 1px solid #333333;
            border-radius: 0.5rem;
        }
        div[data-testid="stExpander"] {
            background-color: #1e1e1e !important;
            border: 1px solid #333333;
            border-radius: 0.5rem;
            padding: 0.5rem;
            color: white;
        }
        div[data-testid="stExpanderContent"] {
            background-color: #1e1e1e !important;
            color: white;
        }
        div.streamlit-expanderContent {
            background-color: #1e1e1e !important;
            color: white;
        }
        .element-container {
            background-color: #1e1e1e;
        }
        div[data-testid="stMarkdownContainer"] > div.stAlert {
            background-color: #1e1e1e;
            color: white;
        }
        .stSidebar {
            background-color: #1e1e1e;
            border-right: 1px solid #333333;
        }
        .stSidebar .stRadio > div {
            background-color: #1e1e1e;
            padding: 1rem;
            border-radius: 0.5rem;
            border: 1px solid #333333;
            color: white;
        }
        .stSidebar .stRadio > div:hover {
            background-color: #2e2e2e;
        }
        .stTextInput > div > div {
            background-color: #1e1e1e;
            border: 1px solid #333333;
            border-radius: 0.5rem;
            color: white;
        }
        .stTextInput > div > div:hover {
            border-color: #4CAF50;
        }
        .stMultiSelect > div > div {
            background-color: #1e1e1e;
            border: 1px solid #333333;
            border-radius: 0.5rem;
            color: white;
        }
        .stMultiSelect > div > div:hover {
            border-color: #4CAF50;
        }
        .dataframe {
            background-color: #1e1e1e !important;
            color: white !important;
        }
        .dataframe th {
            background-color: #2e2e2e !important;
            color: white !important;
        }
        .dataframe td {
            background-color: #1e1e1e !important;
            color: white !important;
        }
        div[data-testid="stTable"] {
            background-color: #1e1e1e !important;
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("📊 Station Data Analytics Dashboard")
    
    # Sidebar with search and filters
    with st.sidebar:
        st.header("🔍 Navigation & Filters")
        
        # Search functionality
        search_query = st.text_input("Search Stations", placeholder="Enter station name...")
        
        # Date range filter
        st.subheader("📅 Date Range")
        date_range = st.date_input(
            "Select Date Range",
            value=(datetime.now().date(), datetime.now().date()),
            max_value=datetime.now().date()
        )
        
        # Mode filter
        st.subheader("🎯 Project Mode")
        mode_filter = st.multiselect(
            "Filter by Mode",
            options=["Online", "Onsite", "Hybrid", "Others", "Not Specified"],
            default=["Online", "Onsite", "Hybrid", "Others", "Not Specified"]
        )
        
        # Business Domain filter
        st.subheader("🏢 Business Domain")
        domain_filter = st.multiselect(
            "Filter by Domain",
            options=load_data("SELECT DISTINCT business_domain FROM problem_banks")['business_domain'].tolist(),
            default=[]
        )
        
        # Navigation
        st.subheader("📑 Navigation")
        page = st.radio(
            "Select View",
            ["Overview", "Station Details", "Project Analysis", "Skills Analysis"],
            label_visibility="collapsed"
        )
    
    if page == "Overview":
        st.header("📈 Overview")
        
        # Key Metrics with tooltips
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_stations = load_data("SELECT COUNT(*) FROM stations").iloc[0,0]
            st.metric("Total Stations", total_stations, help="Total number of registered stations")
        
        with col2:
            total_projects = load_data("SELECT COUNT(*) FROM projects").iloc[0,0]
            st.metric("Total Projects", total_projects, help="Total number of projects across all stations")
        
        with col3:
            total_spocs = load_data("SELECT COUNT(*) FROM station_spocs").iloc[0,0]
            st.metric("Total SPOCs", total_spocs, help="Total number of Single Point of Contacts")
        
        with col4:
            unique_skills = load_data("SELECT COUNT(DISTINCT skill_id) FROM project_skills").iloc[0,0]
            st.metric("Unique Skills", unique_skills, help="Number of unique skills required across all projects")
        
        # Projects by Business Domain with interactive chart
        st.subheader("📊 Projects by Business Domain")
        domain_data = load_data("""
            SELECT business_domain, COUNT(*) as count 
            FROM problem_banks 
            GROUP BY business_domain 
            ORDER BY count DESC
        """)
        
        fig = px.bar(domain_data, x='business_domain', y='count',
                    title="Project Distribution by Business Domain",
                    color='business_domain',
                    labels={'business_domain': 'Business Domain', 'count': 'Number of Projects'},
                    hover_data={'count': True})
        fig.update_traces(hovertemplate="<b>%{x}</b><br>Projects: %{y}<extra></extra>")
        st.plotly_chart(fig, use_container_width=True)
        
        # Project Mode Distribution with interactive charts
        st.subheader("🎯 Project Mode Distribution")
        mode_data = load_data("""
            SELECT mode, COUNT(*) as count 
            FROM projects 
            GROUP BY mode
        """)
        mode_data['mode'] = mode_data['mode'].fillna('Not Specified')
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.pie(mode_data, values='count', names='mode',
                        title="Project Mode Distribution",
                        hole=0.4)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(mode_data, x='mode', y='count',
                        title="Project Mode Count",
                        color='mode',
                        labels={'mode': 'Mode', 'count': 'Number of Projects'})
            fig.update_traces(hovertemplate="<b>%{x}</b><br>Projects: %{y}<extra></extra>")
            st.plotly_chart(fig, use_container_width=True)
    
    elif page == "Station Details":
        st.header("🏢 Station Details")
        
        # Station Selection with search
        stations = load_data("SELECT DISTINCT name FROM stations ORDER BY name")
        if search_query:
            stations = stations[stations['name'].str.contains(search_query, case=False)]
        
        selected_station = st.selectbox("Select a Station", stations['name'].tolist())
        
        if selected_station:
            # Station Metrics with tooltips
            station_details = load_data("""
                SELECT s.*, 
                       COUNT(DISTINCT p.project_id) as project_count,
                       COUNT(DISTINCT sp.spoc_id) as spoc_count
                FROM stations s
                LEFT JOIN projects p ON s.station_id = p.station_id
                LEFT JOIN station_spocs sp ON s.station_id = sp.station_id
                WHERE s.name = ?
                GROUP BY s.station_id
            """, (selected_station,))
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Station ID", station_details['station_id'].iloc[0], help="Unique identifier for the station")
            with col2:
                st.metric("Total Projects", station_details['project_count'].iloc[0], help="Number of projects at this station")
            with col3:
                st.metric("Total SPOCs", station_details['spoc_count'].iloc[0], help="Number of Single Point of Contacts")
            
            # Station Information with expandable sections
            with st.expander("📋 Station Information", expanded=True):
                info_cols = ['name', 'website', 'address']
                station_info = station_details[info_cols].T
                station_info.columns = ['Details']
                st.dataframe(station_info, use_container_width=True)
            
            # Contact Information Section
            with st.expander("📞 Contact Information", expanded=True):
                # Station Contact Info
                st.subheader("Station Contact")
                contact_info = load_data("""
                    SELECT 
                        name as contact_name,
                        contact_number,
                        address
                    FROM stations 
                    WHERE station_id = ?
                """, (station_details['station_id'].iloc[0],))
                
                if not contact_info.empty:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Contact Person**")
                        st.write(contact_info['contact_name'].iloc[0] if not pd.isna(contact_info['contact_name'].iloc[0]) else "Not specified")
                    with col2:
                        st.markdown("**Contact Number**")
                        st.write(contact_info['contact_number'].iloc[0] if not pd.isna(contact_info['contact_number'].iloc[0]) else "Not specified")
                    st.markdown("**Address**")
                    st.write(contact_info['address'].iloc[0] if not pd.isna(contact_info['address'].iloc[0]) else "Not specified")
                else:
                    st.info("No station contact information available.")

                # SPOC Contact Info
                st.subheader("SPOCs Contact Information")
                spoc_info = load_data("""
                    SELECT 
                        name,
                        email,
                        designation,
                        contact_number
                    FROM station_spocs 
                    WHERE station_id = ?
                """, (station_details['station_id'].iloc[0],))
                
                if not spoc_info.empty:
                    for idx, spoc in spoc_info.iterrows():
                        with st.expander(f"SPOC: {spoc['name'] if not pd.isna(spoc['name']) else 'Unknown'}", expanded=False):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("**Name**")
                                st.write(spoc['name'] if not pd.isna(spoc['name']) else "Not specified")
                                st.markdown("**Email**")
                                st.write(spoc['email'] if not pd.isna(spoc['email']) else "Not specified")
                            with col2:
                                st.markdown("**Contact Number**")
                                st.write(spoc['contact_number'] if not pd.isna(spoc['contact_number']) else "Not specified")
                                st.markdown("**Designation**")
                                st.write(spoc['designation'] if not pd.isna(spoc['designation']) else "Not specified")
                else:
                    st.info("No SPOCs found for this station.")
            
            # Station Projects with filtering
            with st.expander("📚 Projects", expanded=True):
                station_id = station_details['station_id'].iloc[0]
                
                # Debug information
                st.write("Debug Info:")
                st.write(f"Station ID: {station_id}")
                
                # First check if projects exist
                project_count = load_data("""
                    SELECT COUNT(*) as count
                    FROM projects
                    WHERE station_id = ?
                """, (station_id,)).iloc[0]['count']
                
                st.write(f"Total projects in database: {project_count}")
                
                station_projects = load_data("""
                    SELECT 
                        p.project_id,
                        p.title,
                        p.description,
                        p.mode,
                        p.mentor_name,
                        pb.business_domain
                    FROM projects p
                    LEFT JOIN problem_banks pb ON p.problem_bank_id = pb.problem_bank_id
                    WHERE p.station_id = ?
                """, (station_id,))
                
                st.write(f"Projects retrieved: {len(station_projects)}")
                
                if not station_projects.empty:
                    st.write("Project Data:")
                    st.write(station_projects)
                    st.dataframe(station_projects, use_container_width=True)
                else:
                    st.info("No projects found for this station.")
            
            # Station SPOCs with expandable sections
            with st.expander("👥 SPOCs", expanded=True):
                # Debug information
                st.write("Debug Info:")
                
                # First check if SPOCs exist
                spoc_count = load_data("""
                    SELECT COUNT(*) as count
                    FROM station_spocs
                    WHERE station_id = ?
                """, (station_id,)).iloc[0]['count']
                
                st.write(f"Total SPOCs in database: {spoc_count}")
                
                station_spocs = load_data("""
                    SELECT 
                        spoc_id,
                        name,
                        email,
                        designation
                    FROM station_spocs
                    WHERE station_id = ?
                """, (station_id,))
                
                st.write(f"SPOCs retrieved: {len(station_spocs)}")
                
                if not station_spocs.empty:
                    st.write("SPOC Data:")
                    st.write(station_spocs)
                    st.dataframe(station_spocs, use_container_width=True)
                else:
                    st.info("No SPOCs found for this station.")
    
    elif page == "Project Analysis":
        st.header("📋 Project Analysis")
        
        # Project Mode Analysis with interactive charts
        st.subheader("🎯 Project Mode Analysis")
        df = load_data("""
            SELECT 
                p.*,
                pb.business_domain,
                s.name as station_name
            FROM projects p
            JOIN problem_banks pb ON p.problem_bank_id = pb.problem_bank_id
            JOIN stations s ON p.station_id = s.station_id
        """)
        
        # Replace NULL values with 'Not Specified'
        df['mode'] = df['mode'].fillna('Not Specified')
        
        # Add sorting options
        st.sidebar.subheader("Sort Options")
        sort_by = st.sidebar.radio(
            "Sort Stations By:",
            ["Name", "Most Online Projects", "Most Onsite Projects", "Most Hybrid Projects"],
            key="sort_option"
        )
        
        # Prepare station-wise mode counts
        station_mode_counts = pd.pivot_table(
            df,
            values='project_id',
            index='station_name',
            columns='mode',
            aggfunc='count',
            fill_value=0
        ).reset_index()
        
        # Sort based on selection
        if sort_by == "Name":
            station_mode_counts = station_mode_counts.sort_values('station_name')
        elif sort_by == "Most Online Projects":
            station_mode_counts = station_mode_counts.sort_values('Online', ascending=False)
        elif sort_by == "Most Onsite Projects":
            station_mode_counts = station_mode_counts.sort_values('Onsite', ascending=False)
        elif sort_by == "Most Hybrid Projects":
            station_mode_counts = station_mode_counts.sort_values('Hybrid', ascending=False)
        
        # Display the sorted summary
        st.subheader("📊 Station Project Modes (Sorted)")
        st.dataframe(station_mode_counts, use_container_width=True)
        
        # Create sorted bar chart
        station_modes = df.groupby(['station_name', 'mode']).size().reset_index(name='count')
        station_order = station_mode_counts['station_name'].tolist()
        
        fig = px.bar(station_modes, 
                    x='station_name', 
                    y='count',
                    color='mode',
                    title=f"Project Modes by Station (Sorted by {sort_by})",
                    labels={
                        'station_name': 'Station Name',
                        'count': 'Number of Projects',
                        'mode': 'Project Mode'
                    },
                    category_orders={"station_name": station_order})
        
        fig.update_layout(
            xaxis_tickangle=-45,
            height=600,
            showlegend=True,
            xaxis_title="Station Name",
            yaxis_title="Number of Projects"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Mode distribution pie chart
        st.subheader("🔄 Overall Mode Distribution")
        mode_counts = df['mode'].value_counts()
        fig_pie = px.pie(
            values=mode_counts.values, 
            names=mode_counts.index,
            title="Overall Project Mode Distribution",
            hole=0.4
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Filter projects with advanced options
        st.subheader("🔍 Filter and Search Projects")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            all_modes = ['All'] + sorted(df['mode'].unique().tolist())
            selected_mode = st.selectbox("Select Project Mode", all_modes, key="mode_filter")
        
        with col2:
            all_domains = ['All'] + sorted(df['business_domain'].unique().tolist())
            selected_domain = st.selectbox("Select Business Domain", all_domains, key="domain_filter")
            
        with col3:
            all_stations = ['All'] + station_order  # Use sorted station list
            selected_station = st.selectbox("Select Station", all_stations, key="station_filter")
        
        filtered_df = df.copy()
        if selected_mode != "All":
            filtered_df = filtered_df[filtered_df['mode'] == selected_mode]
        if selected_domain != "All":
            filtered_df = filtered_df[filtered_df['business_domain'] == selected_domain]
        if selected_station != "All":
            filtered_df = filtered_df[filtered_df['station_name'] == selected_station]
        
        # Add search functionality to the dataframe
        search_text = st.text_input("Search in Projects", placeholder="Search by title, description...", key="project_search")
        if search_text:
            filtered_df = filtered_df[
                filtered_df['title'].str.contains(search_text, case=False, na=False) |
                filtered_df['description'].str.contains(search_text, case=False, na=False)
            ]
        
        # Display the filtered projects with station names
        if not filtered_df.empty:
            display_cols = ['station_name', 'title', 'mode', 'business_domain', 'mentor_name']
            st.dataframe(
                filtered_df[display_cols].sort_values(['mode', 'station_name']), 
                use_container_width=True
            )
            
            # Show statistics for filtered results
            st.subheader("📈 Filtered Results Statistics")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Projects", len(filtered_df))
            with col2:
                mode_stats = filtered_df['mode'].value_counts()
                st.write("Mode Distribution:")
                st.write(mode_stats)
            with col3:
                station_stats = filtered_df['station_name'].value_counts()
                st.write("Top Stations:")
                st.write(station_stats.head())
        else:
            st.info("No projects found matching the selected criteria.")
    
    elif page == "Skills Analysis":
        st.header("🎯 Skills Analysis")
        
        # Top Skills with interactive chart
        st.subheader("📊 Most Required Skills")
        skills_data = load_data("""
            SELECT skill_id, COUNT(*) as count
            FROM project_skills
            GROUP BY skill_id
            ORDER BY count DESC
            LIMIT 10
        """)
        
        fig = px.bar(skills_data, x='skill_id', y='count',
                    title="Top 10 Required Skills",
                    labels={'skill_id': 'Skill ID', 'count': 'Number of Projects'})
        fig.update_traces(hovertemplate="<b>Skill ID: %{x}</b><br>Projects: %{y}<extra></extra>")
        st.plotly_chart(fig, use_container_width=True)
        
        # Skills by Project Mode with interactive chart
        st.subheader("🎯 Skills Distribution by Project Mode")
        skills_mode = load_data("""
            SELECT p.mode, COUNT(DISTINCT ps.skill_id) as skill_count
            FROM projects p
            JOIN project_skills ps ON p.project_id = ps.project_id
            GROUP BY p.mode
        """)
        skills_mode['mode'] = skills_mode['mode'].fillna('Not Specified')
        
        fig = px.bar(skills_mode, x='mode', y='skill_count',
                    title="Number of Unique Skills by Project Mode",
                    labels={'mode': 'Project Mode', 'skill_count': 'Number of Unique Skills'})
        fig.update_traces(hovertemplate="<b>%{x}</b><br>Unique Skills: %{y}<extra></extra>")
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
=======
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def load_data(query, params=None):
    conn = sqlite3.connect('station_data_v2.db')
    if params:
        df = pd.read_sql_query(query, conn, params=params)
    else:
        df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def main():
    st.set_page_config(
        page_title="Station Data Analytics",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stMetric {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            transition: all 0.3s ease;
        }
        .stMetric:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .stDataFrame {
            border-radius: 0.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .css-1d391kg {
            padding: 1rem;
        }
        .stSelectbox, .stRadio {
            background-color: #1e1e1e;
            border-radius: 0.5rem;
            padding: 0.5rem;
        }
        .stButton>button {
            width: 100%;
            border-radius: 0.5rem;
            padding: 0.5rem;
            background-color: #4CAF50;
            color: white;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #45a049;
            transform: translateY(-1px);
        }
        .info-box {
            background-color: #1e1e1e;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
        }
        .stExpander {
            background-color: #1e1e1e !important;
            border: 1px solid #333333;
            border-radius: 0.5rem;
        }
        div[data-testid="stExpander"] {
            background-color: #1e1e1e !important;
            border: 1px solid #333333;
            border-radius: 0.5rem;
            padding: 0.5rem;
            color: white;
        }
        div[data-testid="stExpanderContent"] {
            background-color: #1e1e1e !important;
            color: white;
        }
        div.streamlit-expanderContent {
            background-color: #1e1e1e !important;
            color: white;
        }
        .element-container {
            background-color: #1e1e1e;
        }
        div[data-testid="stMarkdownContainer"] > div.stAlert {
            background-color: #1e1e1e;
            color: white;
        }
        .stSidebar {
            background-color: #1e1e1e;
            border-right: 1px solid #333333;
        }
        .stSidebar .stRadio > div {
            background-color: #1e1e1e;
            padding: 1rem;
            border-radius: 0.5rem;
            border: 1px solid #333333;
            color: white;
        }
        .stSidebar .stRadio > div:hover {
            background-color: #2e2e2e;
        }
        .stTextInput > div > div {
            background-color: #1e1e1e;
            border: 1px solid #333333;
            border-radius: 0.5rem;
            color: white;
        }
        .stTextInput > div > div:hover {
            border-color: #4CAF50;
        }
        .stMultiSelect > div > div {
            background-color: #1e1e1e;
            border: 1px solid #333333;
            border-radius: 0.5rem;
            color: white;
        }
        .stMultiSelect > div > div:hover {
            border-color: #4CAF50;
        }
        .dataframe {
            background-color: #1e1e1e !important;
            color: white !important;
        }
        .dataframe th {
            background-color: #2e2e2e !important;
            color: white !important;
        }
        .dataframe td {
            background-color: #1e1e1e !important;
            color: white !important;
        }
        div[data-testid="stTable"] {
            background-color: #1e1e1e !important;
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("📊 Station Data Analytics Dashboard")
    
    # Sidebar with search and filters
    with st.sidebar:
        st.header("🔍 Navigation & Filters")
        
        # Search functionality
        search_query = st.text_input("Search Stations", placeholder="Enter station name...")
        
        # Date range filter
        st.subheader("📅 Date Range")
        date_range = st.date_input(
            "Select Date Range",
            value=(datetime.now().date(), datetime.now().date()),
            max_value=datetime.now().date()
        )
        
        # Mode filter
        st.subheader("🎯 Project Mode")
        mode_filter = st.multiselect(
            "Filter by Mode",
            options=["Online", "Onsite", "Hybrid", "Others", "Not Specified"],
            default=["Online", "Onsite", "Hybrid", "Others", "Not Specified"]
        )
        
        # Business Domain filter
        st.subheader("🏢 Business Domain")
        domain_filter = st.multiselect(
            "Filter by Domain",
            options=load_data("SELECT DISTINCT business_domain FROM problem_banks")['business_domain'].tolist(),
            default=[]
        )
        
        # Navigation
        st.subheader("📑 Navigation")
        page = st.radio(
            "Select View",
            ["Overview", "Station Details", "Project Analysis", "Skills Analysis"],
            label_visibility="collapsed"
        )
    
    if page == "Overview":
        st.header("📈 Overview")
        
        # Key Metrics with tooltips
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_stations = load_data("SELECT COUNT(*) FROM stations").iloc[0,0]
            st.metric("Total Stations", total_stations, help="Total number of registered stations")
        
        with col2:
            total_projects = load_data("SELECT COUNT(*) FROM projects").iloc[0,0]
            st.metric("Total Projects", total_projects, help="Total number of projects across all stations")
        
        with col3:
            total_spocs = load_data("SELECT COUNT(*) FROM station_spocs").iloc[0,0]
            st.metric("Total SPOCs", total_spocs, help="Total number of Single Point of Contacts")
        
        with col4:
            unique_skills = load_data("SELECT COUNT(DISTINCT skill_id) FROM project_skills").iloc[0,0]
            st.metric("Unique Skills", unique_skills, help="Number of unique skills required across all projects")
        
        # Projects by Business Domain with interactive chart
        st.subheader("📊 Projects by Business Domain")
        domain_data = load_data("""
            SELECT business_domain, COUNT(*) as count 
            FROM problem_banks 
            GROUP BY business_domain 
            ORDER BY count DESC
        """)
        
        fig = px.bar(domain_data, x='business_domain', y='count',
                    title="Project Distribution by Business Domain",
                    color='business_domain',
                    labels={'business_domain': 'Business Domain', 'count': 'Number of Projects'},
                    hover_data={'count': True})
        fig.update_traces(hovertemplate="<b>%{x}</b><br>Projects: %{y}<extra></extra>")
        st.plotly_chart(fig, use_container_width=True)
        
        # Project Mode Distribution with interactive charts
        st.subheader("🎯 Project Mode Distribution")
        mode_data = load_data("""
            SELECT mode, COUNT(*) as count 
            FROM projects 
            GROUP BY mode
        """)
        mode_data['mode'] = mode_data['mode'].fillna('Not Specified')
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.pie(mode_data, values='count', names='mode',
                        title="Project Mode Distribution",
                        hole=0.4)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(mode_data, x='mode', y='count',
                        title="Project Mode Count",
                        color='mode',
                        labels={'mode': 'Mode', 'count': 'Number of Projects'})
            fig.update_traces(hovertemplate="<b>%{x}</b><br>Projects: %{y}<extra></extra>")
            st.plotly_chart(fig, use_container_width=True)
    
    elif page == "Station Details":
        st.header("🏢 Station Details")
        
        # Station Selection with search
        stations = load_data("SELECT DISTINCT name FROM stations ORDER BY name")
        if search_query:
            stations = stations[stations['name'].str.contains(search_query, case=False)]
        
        selected_station = st.selectbox("Select a Station", stations['name'].tolist())
        
        if selected_station:
            # Station Metrics with tooltips
            station_details = load_data("""
                SELECT s.*, 
                       COUNT(DISTINCT p.project_id) as project_count,
                       COUNT(DISTINCT sp.spoc_id) as spoc_count
                FROM stations s
                LEFT JOIN projects p ON s.station_id = p.station_id
                LEFT JOIN station_spocs sp ON s.station_id = sp.station_id
                WHERE s.name = ?
                GROUP BY s.station_id
            """, (selected_station,))
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Station ID", station_details['station_id'].iloc[0], help="Unique identifier for the station")
            with col2:
                st.metric("Total Projects", station_details['project_count'].iloc[0], help="Number of projects at this station")
            with col3:
                st.metric("Total SPOCs", station_details['spoc_count'].iloc[0], help="Number of Single Point of Contacts")
            
            # Station Information with expandable sections
            with st.expander("📋 Station Information", expanded=True):
                info_cols = ['name', 'website', 'address']
                station_info = station_details[info_cols].T
                station_info.columns = ['Details']
                st.dataframe(station_info, use_container_width=True)
            
            # Contact Information Section
            with st.expander("📞 Contact Information", expanded=True):
                # Station Contact Info
                st.subheader("Station Contact")
                contact_info = load_data("""
                    SELECT 
                        name as contact_name,
                        contact_number,
                        address
                    FROM stations 
                    WHERE station_id = ?
                """, (station_details['station_id'].iloc[0],))
                
                if not contact_info.empty:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Contact Person**")
                        st.write(contact_info['contact_name'].iloc[0] if not pd.isna(contact_info['contact_name'].iloc[0]) else "Not specified")
                    with col2:
                        st.markdown("**Contact Number**")
                        st.write(contact_info['contact_number'].iloc[0] if not pd.isna(contact_info['contact_number'].iloc[0]) else "Not specified")
                    st.markdown("**Address**")
                    st.write(contact_info['address'].iloc[0] if not pd.isna(contact_info['address'].iloc[0]) else "Not specified")
                else:
                    st.info("No station contact information available.")

                # SPOC Contact Info
                st.subheader("SPOCs Contact Information")
                spoc_info = load_data("""
                    SELECT 
                        name,
                        email,
                        designation,
                        contact_number
                    FROM station_spocs 
                    WHERE station_id = ?
                """, (station_details['station_id'].iloc[0],))
                
                if not spoc_info.empty:
                    for idx, spoc in spoc_info.iterrows():
                        with st.expander(f"SPOC: {spoc['name'] if not pd.isna(spoc['name']) else 'Unknown'}", expanded=False):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("**Name**")
                                st.write(spoc['name'] if not pd.isna(spoc['name']) else "Not specified")
                                st.markdown("**Email**")
                                st.write(spoc['email'] if not pd.isna(spoc['email']) else "Not specified")
                            with col2:
                                st.markdown("**Contact Number**")
                                st.write(spoc['contact_number'] if not pd.isna(spoc['contact_number']) else "Not specified")
                                st.markdown("**Designation**")
                                st.write(spoc['designation'] if not pd.isna(spoc['designation']) else "Not specified")
                else:
                    st.info("No SPOCs found for this station.")
            
            # Station Projects with filtering
            with st.expander("📚 Projects", expanded=True):
                station_id = station_details['station_id'].iloc[0]
                
                # Debug information
                st.write("Debug Info:")
                st.write(f"Station ID: {station_id}")
                
                # First check if projects exist
                project_count = load_data("""
                    SELECT COUNT(*) as count
                    FROM projects
                    WHERE station_id = ?
                """, (station_id,)).iloc[0]['count']
                
                st.write(f"Total projects in database: {project_count}")
                
                station_projects = load_data("""
                    SELECT 
                        p.project_id,
                        p.title,
                        p.description,
                        p.mode,
                        p.mentor_name,
                        pb.business_domain
                    FROM projects p
                    LEFT JOIN problem_banks pb ON p.problem_bank_id = pb.problem_bank_id
                    WHERE p.station_id = ?
                """, (station_id,))
                
                st.write(f"Projects retrieved: {len(station_projects)}")
                
                if not station_projects.empty:
                    st.write("Project Data:")
                    st.write(station_projects)
                    st.dataframe(station_projects, use_container_width=True)
                else:
                    st.info("No projects found for this station.")
            
            # Station SPOCs with expandable sections
            with st.expander("👥 SPOCs", expanded=True):
                # Debug information
                st.write("Debug Info:")
                
                # First check if SPOCs exist
                spoc_count = load_data("""
                    SELECT COUNT(*) as count
                    FROM station_spocs
                    WHERE station_id = ?
                """, (station_id,)).iloc[0]['count']
                
                st.write(f"Total SPOCs in database: {spoc_count}")
                
                station_spocs = load_data("""
                    SELECT 
                        spoc_id,
                        name,
                        email,
                        designation
                    FROM station_spocs
                    WHERE station_id = ?
                """, (station_id,))
                
                st.write(f"SPOCs retrieved: {len(station_spocs)}")
                
                if not station_spocs.empty:
                    st.write("SPOC Data:")
                    st.write(station_spocs)
                    st.dataframe(station_spocs, use_container_width=True)
                else:
                    st.info("No SPOCs found for this station.")
    
    elif page == "Project Analysis":
        st.header("📋 Project Analysis")
        
        # Project Mode Analysis with interactive charts
        st.subheader("🎯 Project Mode Analysis")
        df = load_data("""
            SELECT p.*, pb.business_domain
            FROM projects p
            JOIN problem_banks pb ON p.problem_bank_id = pb.problem_bank_id
        """)
        
        # Replace NULL values with 'Not Specified'
        df['mode'] = df['mode'].fillna('Not Specified')
        
        # Mode distribution with interactive chart
        mode_counts = df['mode'].value_counts()
        fig = px.pie(values=mode_counts.values, names=mode_counts.index,
                    title="Project Mode Distribution",
                    hole=0.4)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        
        # Mode by Business Domain with interactive chart
        mode_domain = df.groupby(['business_domain', 'mode']).size().reset_index(name='count')
        fig = px.bar(mode_domain, x='business_domain', y='count', color='mode',
                    title="Project Mode Distribution by Business Domain",
                    barmode='group',
                    labels={'business_domain': 'Business Domain', 'count': 'Number of Projects', 'mode': 'Mode'})
        fig.update_traces(hovertemplate="<b>%{x}</b><br>Projects: %{y}<br>Mode: %{fullData.name}<extra></extra>")
        st.plotly_chart(fig, use_container_width=True)
        
        # Filter projects with advanced options
        st.subheader("🔍 Filter Projects")
        col1, col2 = st.columns(2)
        
        with col1:
            all_modes = ['All'] + sorted(df['mode'].unique().tolist())
            selected_mode = st.selectbox("Select Project Mode", all_modes)
        
        with col2:
            all_domains = ['All'] + sorted(df['business_domain'].unique().tolist())
            selected_domain = st.selectbox("Select Business Domain", all_domains)
        
        filtered_df = df.copy()
        if selected_mode != "All":
            filtered_df = filtered_df[filtered_df['mode'] == selected_mode]
        if selected_domain != "All":
            filtered_df = filtered_df[filtered_df['business_domain'] == selected_domain]
        
        # Add search functionality to the dataframe
        search_text = st.text_input("Search in Projects", placeholder="Search by title, description...")
        if search_text:
            filtered_df = filtered_df[
                filtered_df['title'].str.contains(search_text, case=False, na=False) |
                filtered_df['description'].str.contains(search_text, case=False, na=False)
            ]
        
        st.dataframe(filtered_df, use_container_width=True)
    
    elif page == "Skills Analysis":
        st.header("🎯 Skills Analysis")
        
        # Top Skills with interactive chart
        st.subheader("📊 Most Required Skills")
        skills_data = load_data("""
            SELECT skill_id, COUNT(*) as count
            FROM project_skills
            GROUP BY skill_id
            ORDER BY count DESC
            LIMIT 10
        """)
        
        fig = px.bar(skills_data, x='skill_id', y='count',
                    title="Top 10 Required Skills",
                    labels={'skill_id': 'Skill ID', 'count': 'Number of Projects'})
        fig.update_traces(hovertemplate="<b>Skill ID: %{x}</b><br>Projects: %{y}<extra></extra>")
        st.plotly_chart(fig, use_container_width=True)
        
        # Skills by Project Mode with interactive chart
        st.subheader("🎯 Skills Distribution by Project Mode")
        skills_mode = load_data("""
            SELECT p.mode, COUNT(DISTINCT ps.skill_id) as skill_count
            FROM projects p
            JOIN project_skills ps ON p.project_id = ps.project_id
            GROUP BY p.mode
        """)
        skills_mode['mode'] = skills_mode['mode'].fillna('Not Specified')
        
        fig = px.bar(skills_mode, x='mode', y='skill_count',
                    title="Number of Unique Skills by Project Mode",
                    labels={'mode': 'Project Mode', 'skill_count': 'Number of Unique Skills'})
        fig.update_traces(hovertemplate="<b>%{x}</b><br>Unique Skills: %{y}<extra></extra>")
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
>>>>>>> bf2110df8bb1623be4b7b45140e00ae579b78634
    main() 