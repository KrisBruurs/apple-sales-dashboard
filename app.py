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
        fig1 = px.line(df_fig1, 
                    x = 'month_calender', 
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
                'x': 0.25
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
                'x': 0.25
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
            'x': 0.25
        },
        height=600,
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

### --- Tab2 Col1 --- ###

    with col1:
        metric_pie_options = {
            "Revenue (USD)": "revenue_usd",
            "Units Sold": "units_sold"
        }

        metric_pie_label = st.selectbox(
            "Select Metric to Display",
            list(metric_pie_options.keys()),
            key='pie_metric'
        )

        metric_pie = metric_pie_options[metric_pie_label]

        # Pie chart for revenue/unit sold per region
        df_pie = df_net.groupby('region')[['revenue_usd', 'units_sold']].sum().reset_index()
        pie1 = px.pie(
            df_pie, 
            values=metric_pie, 
            names='region',
            color_discrete_sequence=px.colors.qualitative.Bold,
            hole=0.3,
            template='simple_white'
        )

        pie1.update_layout(
            font_family='rockwell',
            title = {
                'text': f'Percentage of {metric_pie_label} by Region <br> <sup style="font-size:12px;color:gray">Hover over slices to see specific values</sup>',
                'x': 0.25
            },
            legend_title_text='Region'
        )

        if metric_pie == 'revenue_usd':
            hover_template = '$%{value:,.2f} USD<extra></extra>'
        else:  
            hover_template = '%{value:,.0f} units<extra></extra>'

        pie1.update_traces(
            textposition='inside', 
            textinfo='label+percent',
            hoverinfo='value',
            hovertemplate=hover_template,
            marker=dict(line=dict(color='white', width=4))
        )

        st.plotly_chart(pie1, use_container_width=True, config={'displayModeBar': False})

### --- Tab2 Col2 --- ###

    with col2:
        metric_countries_options = {
            "Revenue (USD)": "revenue_usd",
            "Units Sold": "units_sold"
        }

        metric_countries_label = st.selectbox(
            "Select Metric to Display",
            list(metric_countries_options.keys()),
            key='countries_metric'
        )

        metric_countries = metric_countries_options[metric_countries_label]

        if metric_countries == 'revenue_usd':
            df_countries_tab = df_net.groupby('country')['revenue_usd'].mean().reset_index().sort_values(by='revenue_usd', ascending=False)
            formatted_values = df_countries_tab['revenue_usd'].map('${:,.2f}'.format)
            subtitle_text = 'Average Revenue per Sale'
        else:
            df_countries_tab = df_net.groupby('country')['units_sold'].sum().reset_index().sort_values(by='units_sold', ascending=False)
            formatted_values = df_countries_tab['units_sold'].map('{:,.0f}'.format)
            subtitle_text = 'Total Units Sold'

        countries_tab = go.Figure(data=[go.Table(
            columnorder = [0, 1, 2],
            columnwidth = [40, 150, 150],
            header=dict(values=['Rank','Country', metric_countries_label],
                        fill_color='steelblue',
                        font=dict(color='white', 
                                size=12,
                                family='rockwell'),),
            cells=dict(values=[list(range(1, len(df_countries_tab) + 1)), df_countries_tab['country'], formatted_values],
                        fill_color="#E5E6E6",
                        font = dict(color='black',
                                    size = 11,
                                    family='rockwell')),)      
            ]
        )
                          
        countries_tab.update_layout(
            title = {
                'text': f'Top Countries by {subtitle_text} (2022-2025) <br> <sup style="font-size:12px;color:gray">Scroll table to explore more countries</sup>',
                'font': {
                    'family': 'rockwell',
                    'size': 16
                },
                'x': 0.20
            }
        )

        st.plotly_chart(countries_tab, use_container_width=True, config={'displayModeBar': False})

        
## --- Tab3: product & Pricing Analytics --- ##
with tab3:
    st.header('Product & Pricing Analytics')
    st.write('This section analyzes product categories, pricing strategies, and discount distributions to identify key trends.')

### --- Tab3 Col Configuration --- ###
    col1, col2 = st.columns(2)

### --- Tab3 Col1 --- ###
    with col1:
        st.subheader('Revenue by Product Category')

        # Pie chart for revenue per category
        df_pie2 = df_net.groupby('category')['revenue_usd'].sum().reset_index()
        pie_product = px.pie(
            df_pie2, 
            values='revenue_usd', 
            names='category',
            color_discrete_sequence=px.colors.qualitative.Bold,
            hole=0.3,
            template='simple_white'
        )
              
        pie_product.update_layout(
            font_family='rockwell',
            title = {
                'text': 'Percentage of Revenue by Product Category <br> <sup style="font-size:12px;color:gray">Hover over slices to see specific USD values</sup>',
                'x': 0.25
            },
            legend_title_text='Product Category',
        )

        pie_product.update_traces(
            textposition='inside', 
            textinfo='label+percent',
            hoverinfo='value',
            hovertemplate='$%{value:,.2f} USD<extra></extra>',
            marker=dict(line=dict(color='white', width=4))
        )

        st.plotly_chart(pie_product, use_container_width=True, config={'displayModeBar': False})

### --- Tab3 Col2 --- ###
    with col2:
        st.subheader('Top Products by Revenue')

        # Table for revenue by product name
        df_prod_rev = df_net.groupby('product_name')[['revenue_usd', 'units_sold']].sum().reset_index().sort_values(by='revenue_usd', ascending=False)

        top10_products = go.Figure(data=[go.Table(
            columnorder = [0, 1, 2],
            columnwidth = [40, 250, 150],
            header=dict(values=['Rank','Product Name', 'Revenue (USD)'],
                        fill_color='steelblue',
                        font=dict(color='white', 
                                  size=12,
                                  family='rockwell'),),
            cells=dict(values=[list(range(1, len(df_prod_rev) + 1)), df_prod_rev['product_name'], df_prod_rev['revenue_usd'].map('${:,.2f}'.format)],
                        fill_color="#E5E6E6",
                        font = dict(color='black',
                                    size = 11,
                                    family='rockwell')),)      
            ]
        )

        top10_products.update_layout(
            title = {
                'text': 'Revenue by Product Name (2022-2025) <br> <sup style="font-size:12px;color:gray">Scroll table to explore more products</sup>',
                'font': {
                    'family': 'rockwell',
                    'size': 16
                }
            },
            title_x=0.25
        )

        st.plotly_chart(top10_products, use_container_width=True, config={'displayModeBar': False})

    # Discount Analysis and Pareto Analysis side by side
    col3, col4 = st.columns(2)

    with col3:
        st.subheader('Discount Analysis')

        df_disc_count = (
            df_net
            .groupby(["category", "discount_pct"])
            .size()
            .reset_index(name="n_discounts")
        )

        # Calculate total sales per category
        total_sales_per_category = df_net.groupby('category').size().reset_index(name='total_sales')

        # Merge to get the denominator for each category
        df_disc_count = df_disc_count.merge(total_sales_per_category, on='category')

        # Calculate percentage of total sales per category
        df_disc_count['pct_of_category_sales'] = (df_disc_count['n_discounts'] / df_disc_count['total_sales']) * 100

        df_disc_count['discount_pct'] = df_disc_count['discount_pct'].astype(str)

        category_order = (
            df_disc_count.groupby('category')['pct_of_category_sales']
            .sum()
            .sort_values(ascending=False)
            .index
        )

        fig_disc_count = px.bar(
            df_disc_count,
            x='category',
            y='pct_of_category_sales',
            color='discount_pct',
            custom_data=['discount_pct'],
            color_discrete_sequence=px.colors.sequential.Blues,
            labels={
                'category':'Product Category',
                'pct_of_category_sales':'Percentage of Category Sales (%)',
                'discount_pct':'Discount Percentage'
            },
            template='simple_white',
            category_orders={'category': category_order}
        )

        fig_disc_count.update_layout(
            font_family='rockwell',
            title={
                'text': 'Percentage of Category Sales by Discount Percentage (2022-2025)'
                        '<br><sup style="font-size:12px;color:gray">Hover over bars to see specific discount percentages</sup>',
                'x': 0.25
            },
            legend_traceorder='reversed'
        )

        fig_disc_count.update_traces(
            hovertemplate="%{customdata[0]}%<br>%{y:.2f}% of category sales<extra></extra>",
            marker_line_color='steelblue',
        )

        st.plotly_chart(fig_disc_count, use_container_width=True, config={'displayModeBar': False})

    with col4:
        st.subheader('Pareto Analysis - Accessories')

        # Pareto chart for revenue by product name
        df_pareto = df_net[df_net['category'] == 'Accessories'].groupby('product_name')['revenue_usd'].sum().reset_index().sort_values(by='revenue_usd', ascending=False)

        fig_pareto = go.Figure()

        fig_pareto.add_trace(go.Bar(
            x = df_pareto['product_name'],
            y = df_pareto['revenue_usd'],
            name='Revenue',
            marker_color='steelblue',
        ))

        fig_pareto.add_trace(go.Scatter(
            x = df_pareto['product_name'],
            y = (df_pareto['revenue_usd'].cumsum() / df_pareto['revenue_usd'].sum() * 100).round(1),
            name='Cumulative Percentage',
            mode='lines+markers',
            marker_color='salmon',
            yaxis='y2'
        ))

        fig_pareto.update_layout(
            title = {
                'text': 'Pareto Chart of Revenue by Product Name for Accessories (2022-2025) <br> <sup style="font-size:12px;color:gray">Hover over bars and points to see specific values</sup>',
                'x': 0.25
            },
            yaxis=dict(
                title='Revenue (USD)',
                showgrid=False
            ),
            yaxis2=dict(
                title='Cumulative Percentage (%)',
                overlaying='y',
                side='right',
                showgrid=False,
                ticksuffix='%',
                range=[0, 115]

            ),
            xaxis=dict(
                tickangle=-45
            ),
            legend=dict(
                x = .25,
                y = 1,
                orientation='h'
            ),
            template='simple_white',
            font_family='rockwell'
        )

        fig_pareto.add_hline(
            y=80, 
            line_dash='dot', 
            line_color='gray',
            line_width=2,
            yref='y2',
            annotation_text='80% Threshold',
            annotation_position='top right',
            annotation_font_color='gray'
        )

        st.plotly_chart(fig_pareto, use_container_width=True, config={'displayModeBar': False})

## --- Tab4: Customer Insights --- ##
with tab4:
    st.header('Customer Insights')
    st.write('This section explores customer demographics, satisfaction levels, and return patterns to understand customer behavior.')

### --- Tab4 Col Configuration --- ###
    col1, col2 = st.columns(2)

### --- Tab4 Col1 --- ###
    with col1:
        st.subheader('Revenue by Customer Age Group')

        # Customizable pie chart for revenue or units sold by age group
        df_cust_pie = df_net.groupby('customer_age_group')[['revenue_usd', 'units_sold']].sum().reset_index()

        fig_pie_cust = px.pie(
            df_cust_pie,
            values = 'revenue_usd',
            names = 'customer_age_group',
            color_discrete_sequence=px.colors.qualitative.Bold,
            hole=0.3,
            template='simple_white',
            category_orders={'customer_age_group': ['18-24', '25-34', '35-44', '45-54', '55+']}
        )

        fig_pie_cust.update_layout(
            font_family='rockwell',
            title={
                'text': 'Revenue by Customer Age Group (2022-2025) <br> <sup style="font-size:12px;color:gray">Hover over slices to see specific USD values</sup>',
                'x': 0.25
            },
            legend_traceorder='reversed',
        )

        fig_pie_cust.update_traces(
            textposition='inside',
            textinfo='label+percent',
            hoverinfo='value',
            hovertemplate='$%{value:,.2f} USD<extra></extra>',
            marker=dict(line=dict(color='white', width=4))
        )

        st.plotly_chart(fig_pie_cust, use_container_width=True, config={'displayModeBar': False})

### --- Tab4 Col2 --- ###
    with col2:
        st.subheader('Return Rate by Customer Segment')

        # Table for return rate by customer segment
        df_return = (
            df
            .assign(is_returned=lambda x: x["return_status"] == "Returned")
            .groupby("customer_segment")["is_returned"]
            .mean()
            .reset_index(name="return_rate")
        )

        df_return['return_rate'] = round(df_return['return_rate'] * 100)

        fig_return = go.Figure(data=[go.Table(
            header = dict(values = ['Customer Segment', 'Return Rate (%)'],
                          fill_color='steelblue',
                          font=dict(color='white', size=12, family='rockwell')),
            cells = dict(values = [df_return['customer_segment'], df_return['return_rate']],
                        fill_color="#E5E6E6",
                        font = dict(color='black', size = 11, family='rockwell'))
        )])

        fig_return.update_layout(
            font_family='rockwell',
            title={
                "text": "Return Rate by Customer Segment (2022-2025)",
                "x": 0.25
            }
        )

        st.plotly_chart(fig_return, use_container_width=True, config={'displayModeBar': False})

    st.subheader('Customer Rating Distribution')

    # Chart for rating distribution
    fig_hist = px.histogram(
        df_net,
        x = 'customer_rating',
        range_x = [1, 5.1],
        marginal='violin',
        opacity=0.5,
        labels={'customer_rating':'Customer Rating'},
        template='simple_white',
        color_discrete_sequence=['steelblue']
    )

    fig_hist.update_layout(
        font_family='rockwell',
        title={
            'text': 'Distribution of Customer Ratings (2022-2025) <br> <sup style="font-size:12px;color:gray">Hover over bars to see specific unit values</sup>',
            'x': 0.25
        },
        xaxis_title='Customer Rating',
        yaxis_title='Number of ratings',
    )

    fig_hist.update_traces(
        hovertemplate='<b>Customer Rating:</b> %{x}<br><b>Number of Ratings:</b> %{y}<extra></extra>'
    )

    st.plotly_chart(fig_hist, use_container_width=True, config={'displayModeBar': False})



