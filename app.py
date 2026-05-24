import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud

# Page Configuration
st.set_page_config(page_title="WhatsApp Insight", layout="wide", page_icon="📊")

# Custom CSS for Premium Look
st.markdown("""
<style>
    /* Glassmorphism effect for metrics */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        text-align: center;
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #00d4ff;
    }
    .metric-label {
        font-size: 14px;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        color: #00d4ff;
    }
    
    /* Title Styling */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(#00d4ff, #0055ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.2rem;
        color: #555;
        margin-bottom: 2rem;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #111;
        border-right: 1px solid #333;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown('<p style="font-size: 24px; font-weight: bold; color: #00d4ff;">WA Insight 📊</p>', unsafe_allow_html=True)

uploaded_file = st.sidebar.file_uploader("Upload WhatsApp Chat Export (.txt)")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    if df.empty:
        st.error("Could not parse this file. Please ensure it's a valid WhatsApp export.")
        st.stop()

    # User Selection
    user_list = [user for user in df['user'].unique().tolist() if user != 'group_notification']
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Analyze For:", user_list)

    # Main Area
    st.markdown(f'<h1 class="main-title">Analysis Report</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-title">Exploring insights for: <b>{selected_user}</b></p>', unsafe_allow_html=True)

    # Stats Area (Metric Cards)
    num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Total Messages</div><div class="metric-value">{num_messages}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Total Words</div><div class="metric-value">{words}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Media Shared</div><div class="metric-value">{num_media_messages}</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Links Shared</div><div class="metric-value">{num_links}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["🕒 Timelines", "📊 Activity Map", "🔍 User Insights", "🔤 Content Analysis"])

    with tab1:
        st.subheader("Message Volume Over Time")
        
        # Monthly Timeline (Plotly)
        timeline = helper.monthly_timeline(selected_user, df)
        fig = px.line(timeline, x='time', y='message', title="Monthly Timeline", 
                     labels={'message': 'Messages', 'time': 'Month-Year'},
                     template="plotly_dark", color_discrete_sequence=['#00d4ff'])
        fig.update_layout(hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

        # Daily Timeline (Plotly)
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig2 = px.line(daily_timeline, x='only_date', y='message', title="Daily Timeline",
                      labels={'message': 'Messages', 'only_date': 'Date'},
                      template="plotly_dark", color_discrete_sequence=['#ffffff'])
        fig2.update_layout(hovermode="x unified")
        st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Busy Days")
            busy_day = helper.week_activity_map(selected_user, df)
            fig = px.bar(x=busy_day.index, y=busy_day.values, 
                        labels={'x': 'Day of Week', 'y': 'Message Count'},
                        template="plotly_dark", color_discrete_sequence=['#00d4ff'])
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Busy Months")
            busy_month = helper.month_activity_map(selected_user, df)
            fig = px.bar(x=busy_month.index, y=busy_month.values,
                        labels={'x': 'Month', 'y': 'Message Count'},
                        template="plotly_dark", color_discrete_sequence=['#ff4b4b'])
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Weekly Activity Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        if not user_heatmap.empty:
            fig = px.imshow(user_heatmap, labels=dict(x="Hour of Day", y="Day of Week", color="Messages"),
                           template="plotly_dark", color_continuous_scale="Viridis")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Not enough data for heatmap.")

    with tab3:
        if selected_user == 'Overall':
            st.subheader("Most Active Users")
            x, new_df = helper.most_busy_users(df)
            
            col1, col2 = st.columns([2, 1])
            with col1:
                fig = px.pie(names=x.index, values=x.values, hole=0.4,
                            template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                st.dataframe(new_df, use_container_width=True)
        else:
            st.info("User insights are available in 'Overall' mode to compare with others.")

    with tab4:
        st.subheader("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        if df_wc:
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(df_wc)
            ax.axis("off")
            plt.tight_layout(pad=0)
            st.pyplot(fig)
        else:
            st.info("Not enough words for a wordcloud.")

        st.subheader("Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        if not most_common_df.empty:
            fig = px.bar(most_common_df, x=1, y=0, orientation='h',
                        labels={ '1': 'Frequency', '0': 'Word'},
                        template="plotly_dark", color_discrete_sequence=['#00d4ff'])
            fig.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Emoji Sentiment")
        emoji_df = helper.emoji_helper(selected_user, df)
        if not emoji_df.empty:
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(emoji_df.rename(columns={0: 'Emoji', 1: 'Count'}), use_container_width=True)
            with col2:
                fig = px.pie(emoji_df.head(10), names=0, values=1,
                            template="plotly_dark", title="Top 10 Emojis")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No emojis found.")

else:
    # Landing Page
    st.markdown('<h1 class="main-title">WhatsApp Insight</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Transform your chat history into visual intelligence.</p>', unsafe_allow_html=True)
    
    st.info("👈 Upload your WhatsApp export (the .txt file) from the sidebar to get started.")
    
    st.markdown("""
    ### How to export your chat:
    1. Open WhatsApp on your phone.
    2. Open the individual or group chat.
    3. Tap on the options (three dots) > **More** > **Export chat**.
    4. Choose **Without Media** for faster analysis.
    5. Save the `.txt` file and upload it here!
    """)
