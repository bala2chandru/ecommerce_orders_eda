import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="E-Commerce Orders Analytics 2023–2026",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  .top-bar {
    background: linear-gradient(135deg, #0F2027, #203A43, #2C5364);
    border-radius: 8px;
    padding: 24px 32px;
    margin-bottom: 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .top-bar-title { color: #fff; font-size: 1.8rem; font-weight: 700; margin: 0; }
  .top-bar-sub { color: #94B4C1; font-size: 0.85rem; margin-top: 4px; }
  .top-bar-badge {
    background: #F7B731; color: #1a1a1a;
    font-size: 0.75rem; font-weight: 600;
    padding: 6px 14px; border-radius: 20px;
  }

  .kpi-card {
    background: #fff;
    border-radius: 10px;
    padding: 18px 22px;
    border: 1px solid #E8ECF0;
    border-left: 4px solid #2C5364;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  }
  .kpi-card.green { border-left-color: #26de81; }
  .kpi-card.red   { border-left-color: #fc5c65; }
  .kpi-card.amber { border-left-color: #F7B731; }
  .kpi-card.teal  { border-left-color: #2bcbba; }
  .kpi-label { font-size: 0.7rem; font-weight: 600; text-transform: uppercase;
               letter-spacing: 0.08em; color: #8492A6; margin-bottom: 6px; }
  .kpi-value { font-size: 1.75rem; font-weight: 700; color: #2D3748; line-height: 1; }
  .kpi-sub   { font-size: 0.75rem; color: #8492A6; margin-top: 4px; }

  .section-header {
    font-size: 0.7rem; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: #2C5364;
    border-left: 3px solid #F7B731; padding-left: 10px;
    margin-bottom: 16px; margin-top: 8px;
  }
  .stTabs [data-baseweb="tab"] { font-size: 0.8rem; font-weight: 600; }
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 1rem; }
</style>
""", unsafe_allow_html=True)

# ── LOAD DATA ────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('ecommerce_orders_dataset.csv')
    ##df = pd.read_csv(r"D:\ecommerce_orders_eda\ecommerce_orders_dataset.csv")
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    df['YearMonth']  = df['Order_Date'].dt.to_period('M').astype(str)
    df['Age_Group']  = pd.cut(df['Customer_Age'],
                               bins=[17,30,40,50,60,70],
                               labels=['18-30','31-40','41-50','51-60','61-70'])
    return df

df = load_data()

# ── SIDEBAR FILTERS ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Filters")
    st.markdown("---")

    countries   = ["All"] + sorted(df['Country'].unique())
    sel_country = st.selectbox("Country", countries)

    categories  = ["All"] + sorted(df['Product_Category'].unique())
    sel_cat     = st.selectbox("Product Category", categories)

    years       = ["All"] + sorted(df['Year'].unique().tolist())
    sel_year    = st.selectbox("Year", years)

    statuses    = ["All"] + sorted(df['Order_Status'].unique())
    sel_status  = st.selectbox("Order Status", statuses)

    memberships = ["All"] + sorted(df['Membership_Status'].unique())
    sel_member  = st.selectbox("Membership Status", memberships)

    genders     = ["All", "Male", "Female"]
    sel_gender  = st.selectbox("Gender", genders)

    hvo_filter  = st.radio("High Value Orders", ["All", "Yes Only", "No Only"])

    amt_range   = st.slider("Order Amount ($)", 0, int(df['Order_Amount'].max()),
                             (0, int(df['Order_Amount'].max())), step=10)
    st.markdown("---")
    st.markdown("**Built with ❤️ using Streamlit**")

# ── APPLY FILTERS ────────────────────────────────────────────────────
fdf = df.copy()
if sel_country != "All": fdf = fdf[fdf['Country']          == sel_country]
if sel_cat     != "All": fdf = fdf[fdf['Product_Category'] == sel_cat]
if sel_year    != "All": fdf = fdf[fdf['Year']             == int(sel_year)]
if sel_status  != "All": fdf = fdf[fdf['Order_Status']     == sel_status]
if sel_member  != "All": fdf = fdf[fdf['Membership_Status']== sel_member]
if sel_gender  != "All": fdf = fdf[fdf['Customer_Gender']  == sel_gender]
if hvo_filter == "Yes Only": fdf = fdf[fdf['High_Value_Order'] == 'Yes']
if hvo_filter == "No Only":  fdf = fdf[fdf['High_Value_Order'] == 'No']
fdf = fdf[(fdf['Order_Amount'] >= amt_range[0]) & (fdf['Order_Amount'] <= amt_range[1])]

# ── TOP BAR ──────────────────────────────────────────────────────────
st.markdown(f"""
<div class="top-bar">
  <div>
    <div class="top-bar-title">🛒 E-Commerce Orders Analytics</div>
    <div class="top-bar-sub">2023 – 2026 &nbsp;·&nbsp; {len(fdf):,} of {len(df):,} orders &nbsp;·&nbsp; 10 Countries &nbsp;·&nbsp; 8 Categories</div>
  </div>
  <div class="top-bar-badge">Portfolio Dashboard</div>
</div>
""", unsafe_allow_html=True)

# ── KPI CARDS ────────────────────────────────────────────────────────
total_rev   = fdf['Order_Amount'].sum()
total_prof  = fdf['Profit_Amount'].sum()
avg_order   = fdf['Order_Amount'].mean() if len(fdf) > 0 else 0
return_rate = (fdf['Returned'] == 'Yes').mean() * 100 if len(fdf) > 0 else 0
avg_rating  = fdf['Review_Rating'].mean() if len(fdf) > 0 else 0
hvo_pct     = (fdf['High_Value_Order'] == 'Yes').mean() * 100 if len(fdf) > 0 else 0

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.markdown(f'<div class="kpi-card"><div class="kpi-label">Total Revenue</div><div class="kpi-value">${total_rev/1e6:.2f}M</div><div class="kpi-sub">{len(fdf):,} orders</div></div>', unsafe_allow_html=True)
k2.markdown(f'<div class="kpi-card green"><div class="kpi-label">Total Profit</div><div class="kpi-value">${total_prof/1e6:.2f}M</div><div class="kpi-sub">avg margin {fdf["Profit_Margin_Percent"].mean():.1f}%</div></div>', unsafe_allow_html=True)
k3.markdown(f'<div class="kpi-card teal"><div class="kpi-label">Avg Order Value</div><div class="kpi-value">${avg_order:.0f}</div><div class="kpi-sub">median ${fdf["Order_Amount"].median():.0f}</div></div>', unsafe_allow_html=True)
k4.markdown(f'<div class="kpi-card red"><div class="kpi-label">Return Rate</div><div class="kpi-value">{return_rate:.1f}%</div><div class="kpi-sub">{int((fdf["Returned"]=="Yes").sum()):,} returned</div></div>', unsafe_allow_html=True)
k5.markdown(f'<div class="kpi-card amber"><div class="kpi-label">Avg Rating</div><div class="kpi-value">{avg_rating:.2f}★</div><div class="kpi-sub">out of 5.0</div></div>', unsafe_allow_html=True)
k6.markdown(f'<div class="kpi-card"><div class="kpi-label">High-Value Orders</div><div class="kpi-value">{hvo_pct:.1f}%</div><div class="kpi-sub">{int((fdf["High_Value_Order"]=="Yes").sum()):,} orders</div></div>', unsafe_allow_html=True)

st.markdown("---")

# ── TABS ─────────────────────────────────────────────────────────────
t1,t2,t3,t4,t5,t6,t7,t8 = st.tabs([
    "📊 Revenue", "👤 Customers", "🛍️ Products",
    "💳 Payment & Traffic", "🚚 Shipping", "💰 Profit",
    "🔥 Correlations", "🤖 ML Insights"
])

# ─── TAB 1: REVENUE ──────────────────────────────────────────────────
with t1:
    st.markdown('<div class="section-header">Revenue & Order Trends</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        monthly = fdf.groupby('YearMonth')['Order_Amount'].sum().reset_index()
        fig = px.area(monthly, x='YearMonth', y='Order_Amount',
                      color_discrete_sequence=['#2C5364'],
                      title='Monthly Revenue Trend',
                      labels={'YearMonth':'Month','Order_Amount':'Revenue ($)'})
        fig.update_layout(height=380, plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        rev_cat = fdf.groupby('Product_Category')['Order_Amount'].sum().sort_values(ascending=False).reset_index()
        fig2 = px.bar(rev_cat, x='Product_Category', y='Order_Amount',
                      color='Order_Amount', color_continuous_scale='Blues',
                      title='Total Revenue by Category',
                      labels={'Order_Amount':'Revenue ($)','Product_Category':''},
                      text='Order_Amount')
        fig2.update_traces(texttemplate='$%{text:,.0f}', textposition='outside', textfont_size=9)
        fig2.update_layout(coloraxis_showscale=False, height=380,
                           plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        rev_country = fdf.groupby('Country')['Order_Amount'].sum().sort_values(ascending=False).reset_index()
        fig3 = px.bar(rev_country, x='Order_Amount', y='Country', orientation='h',
                      color='Order_Amount', color_continuous_scale='Teal',
                      title='Revenue by Country',
                      labels={'Order_Amount':'Revenue ($)'})
        fig3.update_layout(coloraxis_showscale=False, height=400,
                           plot_bgcolor='white', paper_bgcolor='white',
                           yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        season_rev = fdf.groupby('Season')['Order_Amount'].agg(['sum','mean']).reset_index()
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(x=season_rev['Season'], y=season_rev['sum'],
                              name='Total Revenue ($)', marker_color='#2C5364', opacity=0.85))
        fig4.add_trace(go.Scatter(x=season_rev['Season'], y=season_rev['mean'],
                                  name='Avg Order ($)', yaxis='y2', mode='lines+markers',
                                  line=dict(color='#F7B731', width=2.5), marker=dict(size=8)))
        fig4.update_layout(
            title='Revenue by Season', height=400,
            yaxis=dict(title='Total Revenue ($)'),
            yaxis2=dict(title='Avg Order ($)', overlaying='y', side='right', showgrid=False),
            legend=dict(orientation='h', y=1.15),
            plot_bgcolor='white', paper_bgcolor='white'
        )
        st.plotly_chart(fig4, use_container_width=True)

    # Year-wise revenue
    yr_rev = fdf.groupby('Year')['Order_Amount'].sum().reset_index()
    fig5 = px.bar(yr_rev, x='Year', y='Order_Amount',
                  color='Order_Amount', color_continuous_scale='Blues',
                  title='Annual Revenue Comparison',
                  text='Order_Amount',
                  labels={'Order_Amount':'Revenue ($)'})
    fig5.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    fig5.update_layout(coloraxis_showscale=False, height=360,
                       plot_bgcolor='white', paper_bgcolor='white')
    st.plotly_chart(fig5, use_container_width=True)

# ─── TAB 2: CUSTOMERS ────────────────────────────────────────────────
with t2:
    st.markdown('<div class="section-header">Customer Demographics & Behaviour</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        fig = px.histogram(fdf, x='Customer_Age', nbins=40,
                           color_discrete_sequence=['#2C5364'],
                           title='Age Distribution',
                           labels={'Customer_Age':'Age'})
        fig.add_vline(x=fdf['Customer_Age'].mean(), line_dash='dash',
                      line_color='#F7B731',
                      annotation_text=f"Avg {fdf['Customer_Age'].mean():.0f}")
        fig.update_layout(height=360, plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        gen = fdf['Customer_Gender'].value_counts().reset_index()
        gen.columns = ['Gender','Count']
        fig2 = px.pie(gen, values='Count', names='Gender',
                      color='Gender',
                      color_discrete_map={'Male':'#2C5364','Female':'#fc5c65'},
                      title='Gender Split', hole=0.5)
        fig2.update_traces(textinfo='label+percent')
        fig2.update_layout(height=360, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    with c3:
        mem_order = ['Standard','Silver','Gold','Platinum']
        mem = fdf['Membership_Status'].value_counts().reindex(mem_order).reset_index()
        mem.columns = ['Membership','Count']
        fig3 = px.bar(mem, x='Membership', y='Count',
                      color='Membership',
                      color_discrete_map={'Standard':'#8492A6','Silver':'#94A6B0',
                                          'Gold':'#F7B731','Platinum':'#2bcbba'},
                      title='Membership Distribution', text='Count')
        fig3.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig3.update_layout(height=360, showlegend=False,
                           plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig3, use_container_width=True)

    c4, c5 = st.columns(2)
    with c4:
        clv_mem = fdf.groupby('Membership_Status')['Customer_Lifetime_Value'].mean().reindex(mem_order).reset_index()
        fig4 = px.bar(clv_mem, x='Membership_Status', y='Customer_Lifetime_Value',
                      color='Membership_Status',
                      color_discrete_map={'Standard':'#8492A6','Silver':'#94A6B0',
                                          'Gold':'#F7B731','Platinum':'#2bcbba'},
                      title='Avg Customer Lifetime Value by Membership ($)',
                      text='Customer_Lifetime_Value')
        fig4.update_traces(texttemplate='$%{text:.0f}', textposition='outside')
        fig4.update_layout(height=380, showlegend=False,
                           plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig4, use_container_width=True)

    with c5:
        seg_avg = fdf.groupby('Customer_Segment')['Order_Amount'].mean().sort_values(ascending=False).reset_index()
        fig5 = px.bar(seg_avg, x='Customer_Segment', y='Order_Amount',
                      color='Order_Amount', color_continuous_scale='Blues',
                      title='Avg Order Amount by Customer Segment ($)',
                      text='Order_Amount')
        fig5.update_traces(texttemplate='$%{text:.0f}', textposition='outside')
        fig5.update_layout(coloraxis_showscale=False, height=380,
                           plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig5, use_container_width=True)

# ─── TAB 3: PRODUCTS ─────────────────────────────────────────────────
with t3:
    st.markdown('<div class="section-header">Product & Category Analysis</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        avg_cat = fdf.groupby('Product_Category')['Order_Amount'].mean().sort_values(ascending=False).reset_index()
        fig = px.bar(avg_cat, x='Product_Category', y='Order_Amount',
                     color='Order_Amount', color_continuous_scale='Blues',
                     title='Avg Order Amount by Category ($)', text='Order_Amount')
        fig.update_traces(texttemplate='$%{text:.0f}', textposition='outside')
        fig.update_layout(coloraxis_showscale=False, height=400,
                          plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        ret_cat = fdf.groupby('Product_Category')['Returned'].apply(
            lambda x: (x=='Yes').mean()*100).sort_values(ascending=False).reset_index()
        ret_cat.columns = ['Category','Return Rate']
        overall_ret = (fdf['Returned']=='Yes').mean()*100
        fig2 = px.bar(ret_cat, x='Return Rate', y='Category', orientation='h',
                      color='Return Rate', color_continuous_scale='RdYlGn_r',
                      title='Return Rate by Category (%)', text='Return Rate')
        fig2.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig2.add_vline(x=overall_ret, line_dash='dash', line_color='gray',
                       annotation_text=f'Avg {overall_ret:.1f}%')
        fig2.update_layout(coloraxis_showscale=False, height=400,
                           plot_bgcolor='white', paper_bgcolor='white',
                           yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        rat_cat = fdf.groupby('Product_Category')['Review_Rating'].mean().sort_values(ascending=False).reset_index()
        fig3 = px.bar(rat_cat, x='Review_Rating', y='Product_Category',
                      orientation='h', color='Review_Rating',
                      color_continuous_scale='RdYlGn',
                      title='Avg Review Rating by Category',
                      text='Review_Rating')
        fig3.update_traces(texttemplate='%{text:.2f}★', textposition='outside')
        fig3.update_layout(coloraxis_showscale=False, height=400,
                           plot_bgcolor='white', paper_bgcolor='white',
                           yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        prof_cat = fdf.groupby('Product_Category')['Profit_Margin_Percent'].mean().sort_values(ascending=False).reset_index()
        fig4 = px.bar(prof_cat, x='Product_Category', y='Profit_Margin_Percent',
                      color='Profit_Margin_Percent', color_continuous_scale='Greens',
                      title='Avg Profit Margin % by Category', text='Profit_Margin_Percent')
        fig4.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig4.update_layout(coloraxis_showscale=False, height=400,
                           plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig4, use_container_width=True)

# ─── TAB 4: PAYMENT & TRAFFIC ────────────────────────────────────────
with t4:
    st.markdown('<div class="section-header">Payment Methods & Traffic Sources</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        pay = fdf['Payment_Method'].value_counts().reset_index()
        pay.columns = ['Method','Count']
        fig = px.pie(pay, values='Count', names='Method',
                     title='Payment Method Distribution', hole=0.45)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        traffic = fdf.groupby('Traffic_Source')['Order_Amount'].mean().sort_values(ascending=False).reset_index()
        fig2 = px.bar(traffic, x='Traffic_Source', y='Order_Amount',
                      color='Order_Amount', color_continuous_scale='Purples',
                      title='Avg Order Amount by Traffic Source ($)',
                      text='Order_Amount')
        fig2.update_traces(texttemplate='$%{text:.0f}', textposition='outside')
        fig2.update_layout(coloraxis_showscale=False, height=400,
                           plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        dev = fdf.groupby('Device_Type')['Order_Amount'].mean().sort_values(ascending=False).reset_index()
        fig3 = px.bar(dev, x='Device_Type', y='Order_Amount',
                      color='Device_Type',
                      color_discrete_sequence=['#2C5364','#F7B731','#26de81'],
                      title='Avg Order Amount by Device Type ($)', text='Order_Amount')
        fig3.update_traces(texttemplate='$%{text:.0f}', textposition='outside')
        fig3.update_layout(showlegend=False, height=380,
                           plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        coupon = fdf.groupby('Coupon_Used')['Order_Amount'].mean().reset_index()
        coupon['Label'] = coupon['Coupon_Used'].map({'Yes':'Coupon Used','No':'No Coupon'})
        fig4 = px.bar(coupon, x='Label', y='Order_Amount',
                      color='Label',
                      color_discrete_map={'Coupon Used':'#F7B731','No Coupon':'#2C5364'},
                      title='Avg Order Amount: Coupon Used vs Not ($)', text='Order_Amount')
        fig4.update_traces(texttemplate='$%{text:.0f}', textposition='outside')
        fig4.update_layout(showlegend=False, height=380,
                           plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig4, use_container_width=True)

# ─── TAB 5: SHIPPING ─────────────────────────────────────────────────
with t5:
    st.markdown('<div class="section-header">Shipping & Delivery Performance</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        status_df = fdf['Order_Status'].value_counts().reset_index()
        status_df.columns = ['Status','Count']
        color_map = {'Delivered':'#26de81','Shipped':'#2C5364','Returned':'#fc5c65',
                     'Processing':'#F7B731','Cancelled':'#8492A6'}
        fig = px.bar(status_df, x='Status', y='Count', color='Status',
                     color_discrete_map=color_map, title='Order Status Distribution',
                     text='Count')
        fig.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig.update_layout(showlegend=False, height=380,
                          plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        ship = fdf.groupby('Shipping_Method')['Delivery_Days'].mean().sort_values().reset_index()
        fig2 = px.bar(ship, x='Delivery_Days', y='Shipping_Method', orientation='h',
                      color='Delivery_Days', color_continuous_scale='RdYlGn_r',
                      title='Avg Delivery Days by Shipping Method', text='Delivery_Days')
        fig2.update_traces(texttemplate='%{text:.1f}d', textposition='outside')
        fig2.update_layout(coloraxis_showscale=False, height=380,
                           plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig2, use_container_width=True)

    # Delivery days distribution
    fig3 = px.histogram(fdf, x='Delivery_Days', nbins=20,
                        color_discrete_sequence=['#2C5364'],
                        title='Delivery Days Distribution',
                        labels={'Delivery_Days':'Delivery Days'})
    fig3.add_vline(x=fdf['Delivery_Days'].mean(), line_dash='dash',
                   line_color='#F7B731',
                   annotation_text=f"Avg {fdf['Delivery_Days'].mean():.1f} days")
    fig3.update_layout(height=360, plot_bgcolor='white', paper_bgcolor='white')
    st.plotly_chart(fig3, use_container_width=True)

# ─── TAB 6: PROFIT ───────────────────────────────────────────────────
with t6:
    st.markdown('<div class="section-header">Profit & Discount Analysis</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(fdf, x='Profit_Margin_Percent', nbins=40,
                           color_discrete_sequence=['#26de81'],
                           title='Profit Margin % Distribution',
                           labels={'Profit_Margin_Percent':'Profit Margin (%)'})
        fig.add_vline(x=fdf['Profit_Margin_Percent'].mean(), line_dash='dash',
                      line_color='red',
                      annotation_text=f"Avg {fdf['Profit_Margin_Percent'].mean():.1f}%")
        fig.update_layout(height=380, plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        prof_cat = fdf.groupby('Product_Category')['Profit_Amount'].sum().sort_values(ascending=False).reset_index()
        fig2 = px.bar(prof_cat, x='Product_Category', y='Profit_Amount',
                      color='Profit_Amount', color_continuous_scale='Greens',
                      title='Total Profit by Category ($)', text='Profit_Amount')
        fig2.update_traces(texttemplate='$%{text:,.0f}', textposition='outside', textfont_size=9)
        fig2.update_layout(coloraxis_showscale=False, height=380,
                           plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig2, use_container_width=True)

    # Discount vs profit scatter
    sample = fdf.sample(min(3000, len(fdf)), random_state=42)
    fig3 = px.scatter(sample, x='Discount_Percent', y='Profit_Amount',
                      color='Product_Category', opacity=0.5, size_max=8,
                      trendline='ols',
                      title='Discount % vs Profit Amount',
                      labels={'Discount_Percent':'Discount (%)','Profit_Amount':'Profit ($)'})
    fig3.update_layout(height=420, plot_bgcolor='white', paper_bgcolor='white')
    st.plotly_chart(fig3, use_container_width=True)

# ─── TAB 7: CORRELATIONS ─────────────────────────────────────────────
with t7:
    st.markdown('<div class="section-header">Feature Correlations</div>', unsafe_allow_html=True)

    num_cols = ['Customer_Age','Unit_Price','Quantity','Discount_Percent',
                'Shipping_Cost','Tax_Amount','Order_Amount','Delivery_Days',
                'Review_Rating','Customer_Lifetime_Value',
                'Profit_Margin_Percent','Profit_Amount']
    corr = fdf[num_cols].corr()
    fig = px.imshow(corr, text_auto='.2f', color_continuous_scale='RdBu_r',
                    zmin=-1, zmax=1, title='Correlation Heatmap — Numerical Features')
    fig.update_layout(height=560)
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        x_col = st.selectbox("X Axis", num_cols, index=1)
    with c2:
        y_col = st.selectbox("Y Axis", num_cols, index=6)

    scatter_sample = fdf.sample(min(3000, len(fdf)), random_state=42)
    fig2 = px.scatter(scatter_sample, x=x_col, y=y_col,
                      color='Product_Category', opacity=0.5,
                      hover_data=['Country','Customer_Segment'],
                      title=f'{x_col} vs {y_col}')
    fig2.update_layout(height=450, plot_bgcolor='white', paper_bgcolor='white')
    st.plotly_chart(fig2, use_container_width=True)

# ─── TAB 8: ML INSIGHTS ──────────────────────────────────────────────
with t8:
    st.markdown('<div class="section-header">Machine Learning — Model Results</div>', unsafe_allow_html=True)
    st.info("💡 Full ML models with feature importance are in the Jupyter Notebook. Below are key business insights derived from model outputs.")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🎯 High-Value Order Classifier (Random Forest)")
        st.markdown("""
| Metric | Score |
|--------|-------|
| Accuracy | ~88-92% |
| Precision (HVO) | ~85% |
| Recall (HVO) | ~80% |
| F1 Score | ~82% |

**Top Predictive Features:**
- Unit Price & Quantity
- Customer Lifetime Value
- Product Category
- Membership Status
- Discount Percent
        """)

    with c2:
        st.markdown("#### 📈 Order Amount Regressor (Random Forest)")
        st.markdown("""
| Metric | Score |
|--------|-------|
| MAE | ~$20-35 |
| R² Score | ~0.85-0.92 |
| RMSE | ~$40-60 |

**Top Predictive Features:**
- Unit Price
- Quantity
- Tax Amount
- Shipping Cost
- Product Category
        """)

    # High value order breakdown
    st.markdown("#### High-Value Order Breakdown by Category")
    hvo_cat = fdf.groupby('Product_Category')['High_Value_Order'].apply(
        lambda x: (x=='Yes').mean()*100).sort_values(ascending=False).reset_index()
    hvo_cat.columns = ['Category','HVO Rate']
    fig3 = px.bar(hvo_cat, x='Category', y='HVO Rate',
                  color='HVO Rate', color_continuous_scale='Blues',
                  title='High-Value Order Rate by Category (%)',
                  text='HVO Rate')
    fig3.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig3.update_layout(coloraxis_showscale=False, height=380,
                       plot_bgcolor='white', paper_bgcolor='white')
    st.plotly_chart(fig3, use_container_width=True)

# ── RAW DATA ─────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("📋 View Filtered Data (500 rows)"):
    show_cols = ['Order_ID','Order_Date','Country','Product_Category','Customer_Segment',
                 'Order_Amount','Payment_Method','Order_Status','Returned',
                 'Review_Rating','High_Value_Order']
    st.dataframe(fdf[show_cols].head(500), use_container_width=True)
    csv = fdf[show_cols].head(5000).to_csv(index=False)
    st.download_button("⬇️ Download CSV (5K rows)", data=csv,
                       file_name="ecommerce_filtered.csv", mime="text/csv")
