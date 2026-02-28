import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Load Data --- #
df = pd.read_csv('data/apple_sales_data_transformed.csv')

# Subset non-returned data
df_net = df[df['return_status'] != 'Returned']


# --- Streamlit App --- #

## --- Page Configuration --- ##
st.set_page_config(
    page_title = 'Dashboard',
    layout = 'wide',
    page_icon='🍏',
)

st.title('Apple Sales Dashboard')
st.write('Welcome to the Apple Sales Dashboard! Explore key insights and trends in the sales data across different regions, products, and customer segments. Use the tabs below to navigate through various analyses and visualizations that will help you understand our performance and make informed decisions.')
st.write('<i>Note: All data is fictional and for portfolio purposes only.</i>',
         unsafe_allow_html=True)

## --- Tab Configuration --- ##
tab1, tab2, tab3, tab4 = st.tabs(['Executive Overview', 'Geographic Performance', 'Product & Prices Analytics', 'Customer Insights'])


## --- Tab1: Executive Overview --- ##
with tab1:
    st.header('Executive Overview')
    st.write('This section provides a high-level summary of sales performance')

### --- Tab1 Col Configuration --- ###
    col1, col2 = st.columns(2)

### --- Tab1 Col1 --- ###
    with col1:
        st.subheader('3-year Sales Trend')

        total_revenue = df_net['revenue_usd'].sum()
        total_units = df_net['units_sold'].sum()
        avg_discount = df_net['discount_pct'].mean()

        kpis = pd.DataFrame({
            "Metric": ["Total Revenue", "Units Sold", "Average Discount"],
            "Value": [
                f"${total_revenue/1e6:.1f}M",
                f"{total_units:,}",
                f"{avg_discount:.1f}%"
            ]
        })

        ind1 = go.Figure(go.Indicator(
            mode="number",
            value=total_revenue,
            number={'prefix': "$", 
                    'valueformat': ",.0f",
                    'font': {'color': 'steelblue'}},
            title={"text": "Total Revenue between 2022 and 2025",}
        ))
        ind1.update_layout(margin=dict(l=20, r=20, t=50, b=20), height=200)

        st.plotly_chart(ind1, use_container_width=True)

        ind2 = go.Figure(go.Indicator(
            mode="number",
            value=total_units,
            number={'valueformat': ".0f",
                    'font': {'color': 'steelblue'}},
            title={"text": "Total Units Sold between 2022 and 2025"}
        ))
        ind2.update_layout(margin=dict(l=20, r=20, t=50, b=20), height=200)

        st.plotly_chart(ind2, use_container_width=True)

        ind3 = go.Figure(go.Indicator(
            mode="number",
            value=avg_discount,
            number={'suffix': "%", 'valueformat': ".1f",
                    'font': {'color': 'steelblue'}},
            title={"text": "Average Discount Percentage between 2022 and 2025"}
        ))
        ind3.update_layout(margin=dict(l=20, r=20, t=50, b=20), height=200)

        st.plotly_chart(ind3, use_container_width=True)


### --- Tab1 Col2 --- ###
    with col2:
        st.subheader('Revenue by Year')

       # Line chart of revenue over time
        df_fig1 = df_net.groupby('month_calender')['revenue_usd'].sum().reset_index()
        fig1 = px.line(df_fig1, x = 'month_calender', 
                    y = 'revenue_usd', 
                    markers=True,
                    labels = {'month_calender': '', 'revenue_usd': 'Revenue (USD)'},
                    template='simple_white')

        fig1.update_yaxes(
            tickprefix='$', ticks='outside'
        )

        fig1.update_xaxes(
            hoverformat='%b %Y'
        )

        fig1.update_traces(
            mode='markers+lines', hovertemplate=None
        )

        fig1.update_layout(
            font_family='rockwell',
            hovermode='x unified',
            title = {
                'text': 'Apple Sales Revenue Over Time <br> <sup style="font-size:0.8em;color:gray;">Hover over data points to see specific USD values</sup>',
                'x': 0.5
            }
        )

        fig1.add_shape(
            type='line', line_color='salmon', line_width=3, opacity=1, line_dash='dot',
            x0=df_fig1['month_calender'].min(), x1=df_fig1['month_calender'].max(), 
            y0=df_fig1['revenue_usd'].mean(), y1=df_fig1['revenue_usd'].mean(),

        )

        fig1.add_annotation(
            x=df_fig1['month_calender'].max(), y=df_fig1['revenue_usd'].mean(),
            text='Average Revenue', showarrow=False, yshift=-10, font_color='salmon'
        )

        fig1.update_traces(mode='markers+lines', hovertemplate=None)

        st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})

        # Bar chart for units sold per year
        metric_options = {
            "Revenue (USD)": "revenue_usd",
            "Units Sold": "units_sold",
            "Average Discount (%)": "discount_pct"
        }

        metric_label = st.selectbox(
            "Select Metric to Display",
            list(metric_options.keys())
        )

        metric_bar = metric_options[metric_label]
        agg_func = 'mean' if metric_bar == 'discount_pct' else 'sum'

        df_fig3 = df_net.groupby('year')[metric_bar].agg(agg_func).reset_index()
        df_fig3['year'] = df_fig3['year'].astype(str)  

        fig3 = px.bar(
            df_fig3,
            x = 'year',
            y = metric_bar,
            labels = {'year':'Year', metric_bar: metric_label},
            template='simple_white',
            color_discrete_sequence=['steelblue'],
            text=df_fig3[metric_bar].map(lambda x: f'{x:.1f}' if metric_bar == 'discount_pct' else f'{x:.0f}')
        )

        fig3.update_layout(
            font_family = 'rockwell',
            title = {
                'text': f'Total {metric_label} by Year',
                'x': 0.5
            }
        )

        # Dynamic y-axis formatting based on selected metric
        if metric_bar == 'discount_pct':
            fig3.update_yaxes(
                ticks='outside',
                tickformat='d',
                dtick=1
            )
        else:
            fig3.update_yaxes(
                ticks='outside',
                tickformat='~s'
            )

        if metric_bar == 'units_sold':
            hover_template = '%{y:.0f} units<extra></extra>'
        elif metric_bar == 'revenue_usd':
            hover_template = '$%{y:,.0f}<extra></extra>'
        else:  
            hover_template = '%{y:.1f}%<extra></extra>'

        fig3.update_traces(
            hovertemplate=hover_template
        )

        st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})

## --- Tab2: Geographic Performance --- ##
with tab2:
    st.header('Geographic Performance')
    st.write('This section analyzes sales performance across different regions and countries, highlighting key geographic trends and insights.')

    df_map = df_net.groupby(['country', 'region'])['revenue_usd'].sum().reset_index()


    fig_map = go.Figure(data=go.Choropleth(
        locations=df_map['country'],
        z = df_map['revenue_usd'],
        locationmode='country names',
        text=df_map['country'],
        colorscale='Blues',
        marker_line_color='black',
        marker_line_width=0.5,
        colorbar_ticksuffix='$',
        colorbar_title='Revenue (USD)'
    ))

    fig_map.update_layout(
        title= {
            'text': 'Revenue by Country (2022-2025) <br> <sup style="font-size:12px;color:gray">Hover over countries to see specific USD values</sup>',
            'x': 0.5
        },
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular'
        ),
        annotations=[
            dict(
                x=0.5,
                y=-0.1,
                xref='paper',
                yref='paper',
                text='* Note: Dataset only contains data for 47 countries, so some regions may be underrepresented.',
                showarrow=False,
                font=dict(size=10, color='gray')
            )
        ],
        font_family='rockwell')

    fig_map.update_traces(
        hovertemplate='%{text}: $%{z:,.2f} USD<extra></extra>'
    )

    st.plotly_chart(fig_map, use_container_width=True, config={'displayModeBar': False})


### --- Tab2 Col Configuration --- ###
    col1, col2 = st.columns(2)

## --- Tab3: product & Pricing Analytics --- ##

### --- Tab3 Col Configuration --- ###

## --- Tab4: Customer Insights --- ##

### --- Tab4 Col Configuration --- ###



