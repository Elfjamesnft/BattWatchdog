import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from logger.abuse_detector import generate_abuse_report

# Configure the page
st.set_page_config(
    page_title="BattWatchdog Dashboard",
    page_icon="🔋",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {background-color: #f9f9f9;}
    .stAlert {padding: 20px !important;}
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

def load_data():
    """Load battery log data"""
    try:
        df = pd.read_csv('data/battery_log.csv')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        st.error(f"Failed to load data: {str(e)}")
        return pd.DataFrame()

def display_metrics(df):
    """Show key metrics at the top"""
    if df.empty:
        return
        
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Latest SOC", f"{df['soc'].iloc[-1]}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Min SOC", f"{df['soc'].min()}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Voltage Range", f"{df['voltage'].min():.2f}V - {df['voltage'].max():.2f}V")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Data Points", len(df))
        st.markdown('</div>', unsafe_allow_html=True)

def plot_timeseries(df):
    """Create interactive time series plots"""
    if df.empty:
        return
        
    tab1, tab2 = st.tabs(["State of Charge", "Voltage"])
    
    with tab1:
        fig = px.line(
            df, x='timestamp', y='soc',
            title='State of Charge Over Time',
            labels={'soc': 'State of Charge (%)'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        fig = px.line(
            df, x='timestamp', y='voltage',
            title='Voltage Over Time',
            labels={'voltage': 'Voltage (V)'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

def show_abuse_report():
    """Display battery abuse findings"""
    st.subheader("🔍 Abuse Detection Report")
    with st.spinner("Analyzing battery logs..."):
        report = generate_abuse_report()
    
    if "No battery abuse detected" in report:
        st.success(report)
    else:
        st.warning(report)
        
    with st.expander("Raw Data Preview"):
        df = load_data()
        st.dataframe(df.sort_values('timestamp', ascending=False))

def main():
    """Main dashboard layout"""
    st.title("🔋 BattWatchdog Dashboard")
    st.markdown("Monitor your battery's health in real-time")
    
    df = load_data()
    display_metrics(df)
    
    if not df.empty:
        plot_timeseries(df)
        show_abuse_report()
    else:
        st.warning("No battery data found. Please run the simulator first.")

if __name__ == "__main__":
    main()
