'''
functions to draw cahrts using plotly
'''
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utility.process_data import calculate_chart_portfolio_value, calculate_invested_value, calculate_compare_growth, claculate_portfolio_value
from utility.read_data import read_ohlcv, read_trading_data, read_current_position

CHART_THEME = 'seaborn'


def chart_portfolio_value():
    # calculate the portfolio dataframe for chart
    cahrt_df = calculate_chart_portfolio_value()
    invested_value_df = calculate_invested_value()

    # initialize the chart and then update in the following lines
    chart = go.Figure()

    chart.add_trace(
        go.Scatter(
            x=cahrt_df['date'],
            y=cahrt_df['portf_value'],
            mode='lines',
            name='Portfolio Value',
            hovertemplate='$ %{y:,.0f}'
        )

    )

    chart.update_layout(
        margin=dict(t=50, b=50, l=25, r=25),  # optimize spaces for chart
        xaxis_tickfont_size=12,
        yaxis=dict(title='Value(USD)', titlefont_size=14, tickfont_size=12,),
        title='Portfolio value (USD)',
    )

    chart.add_trace(
        go.Scatter(
            x=invested_value_df.date,
            y=invested_value_df['total_cashflow'],
            fill='tozeroy',
            fillcolor='rgba(255, 150, 20, 0.3)',
            line=dict(
                color='orangered',
                width=2,
                dash='dash'),
            mode='lines',
            name='Net Invested',
            hovertemplate='$ %{y:,.0f}'
        )
    )

    chart.update_layout(
        # this will help you optimize the chart space
        margin=dict(t=50, b=50, l=25, r=25),
        xaxis_tickfont_size=12,
        yaxis=dict(
            title='Value: $ USD',
            titlefont_size=14,
            tickfont_size=12,
        ),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01),
        showlegend=False,
        title_x=0.5,
    )

    # Range Selector Buttons
    chart.update_xaxes(
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list([
                dict(count=7, label="1w", step="day", stepmode="backward"),
                dict(count=14, label="2w", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=12, label="12m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(label='All', step="all"),
            ]),
        )
    )
    chart.update_layout(hovermode='x unified')
    chart.layout.template = CHART_THEME
    chart.layout.height = 500

    return chart


def chart_drawdown():
    # calculate the portfolio dataframe for chart
    cahrt_df = calculate_chart_portfolio_value()

    chart = go.Figure()
    chart.add_trace(
        go.Scatter(
            x=cahrt_df['date'],
            y=cahrt_df['drawdownpct'],
            fill='tozeroy',
            fillcolor='tomato',
            line=dict(
                color='firebrick',
                width=2),
            mode='lines',
            name='Drawdown %'))

    chart.update_layout(
        margin=dict(t=45, b=30, l=25, r=25),
        yaxis=dict(
            title='%',
            titlefont_size=14,
            tickfont_size=12,
        ),
        title='Drawdown',
        title_x=0.5,
    )

    chart.update_xaxes(
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list([
                dict(count=7, label="1w", step="day", stepmode="backward"),
                dict(count=14, label="2w", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=12, label="12m",
                     step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(label='All', step="all"),
            ]),
        )
    )

    chart.layout.template = CHART_THEME
    chart.layout.height = 250

    return chart


def chart_cashflow():
    # calculate the portfolio dataframe for chart
    cahrt_df = calculate_chart_portfolio_value()

    chart = go.Figure()  # generating a figure that will be updated in the following lines
    chart.add_trace(
        go.Bar(
            x=cahrt_df.date,
            y=cahrt_df.cashflow.replace(0, np.nan),
            name='Drawdown %',
            xperiod="M1",
        )
    )

    chart.update_layout(
        margin=dict(t=50, b=30, l=25, r=25),
        yaxis=dict(
            title='$ Value',
            titlefont_size=14,
            tickfont_size=12,
        ),
        title='Monthly Buy & Sell Orders',
        title_x=0.5,
        # paper_bgcolor="#272b30",
        # plot_bgcolor="#272b30"
    )

    chart.update_xaxes(
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list([
                dict(count=7, label="1w", step="day", stepmode="backward"),
                dict(count=14, label="2w", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=12, label="12m",
                     step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(label='All', step="all"),
            ]),
            # bgcolor="#272b30",
            # activecolor='tomato',
        )
    )

    chart.layout.template = CHART_THEME
    chart.layout.height = 250

    return chart


def chart_compare_growth():
    '''
    chart for comparing portfolio growth and compare it with growth of S&P500
    '''
    compare_growth_df = calculate_compare_growth()
    chart = go.Figure()

    chart.add_trace(go.Bar(
        x=compare_growth_df.timeperiod,
        y=compare_growth_df.net_value.round(2),
        name='Portfolio'
    ))
    chart.add_trace(go.Bar(
        x=compare_growth_df.timeperiod,
        y=compare_growth_df.sp500_mktvalue.round(2),
        name='S&P 500',
    ))
    chart.update_layout(barmode='group')
    chart.layout.height = 300
    chart.update_layout(margin=dict(t=50, b=50, l=25, r=25))
    chart.update_layout(
        xaxis_tickfont_size=12,
        yaxis=dict(
            title='% change',
            titlefont_size=13,
            tickfont_size=12,
        ))

    chart.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=0.99))
    chart.layout.template = CHART_THEME

    return chart


def chart_ohlcv(ticker_name):
    # read ohlcv data and store it in a dataframe
    ohlcv_df = read_ohlcv(ticker_name=ticker_name)

    # read trading data
    trading_df = read_trading_data()

    # read current position data
    position_df = read_current_position()

    # Create subplots and mention plot grid size
    chart = make_subplots(rows=2, cols=1, shared_xaxes=True,
                          vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'),
                          row_width=[0.2, 0.7])
    chart.layout.template = CHART_THEME

    # Plot OHLC on 1st row
    chart.add_trace(go.Candlestick(x=ohlcv_df["date"], open=ohlcv_df["open"], high=ohlcv_df["high"],
                                   low=ohlcv_df['low'], close=ohlcv_df['close'], name="OHLC", showlegend=False),
                    row=1, col=1
                    )

    tx_df = trading_df[trading_df.ticker == ticker_name]

    chart.add_trace(go.Scatter(
        x=tx_df[tx_df.type == 'Buy'].date,
        y=tx_df[tx_df.type == 'Buy'].price,
        mode='markers',
        name='Buy Orders',
        marker=dict(
            color='rgba(63, 255, 56, 0.6)',
            size=12,
            line=dict(
                color='black',
                width=1
            )), showlegend=False))

    chart.add_trace(go.Scatter(
        x=tx_df[tx_df.type == 'Sell'].date,
        y=tx_df[tx_df.type == 'Sell'].price,
        mode='markers',
        name='Sell Orders',
        marker=dict(
            color='rgba(255, 13, 17, 0.6)',
            size=12,
            line=dict(
                color='black',
                width=1
            )), showlegend=False))

    avg_price_df = position_df.set_index('ticker')
    avg_price = avg_price_df.loc[ticker_name].avg_price
    res = round((avg_price_df.loc[ticker_name].price/avg_price-1)*100, 2)

    chart.update_layout(
        yaxis_title='Price $',
        shapes=[dict(
            x0=0, x1=1, y0=avg_price, y1=avg_price, xref='paper', yref='y',
            line_width=1)],
        annotations=[dict(
            x=0.05, y=avg_price*0.90, xref='paper', yref='y',
            showarrow=False, xanchor='left',
            opacity=0.30, text='Average Price: $ {}<br>Result: {} %'.format(avg_price, res), font={'size': 12})]
    )

    # Bar trace for volumes on 2nd row without legend
    chart.add_trace(go.Bar(
        x=ohlcv_df['date'], y=ohlcv_df['volume'], showlegend=False), row=2, col=1)

    # Do not show OHLC's rangeslider plot
    chart.update(layout_xaxis_rangeslider_visible=False)
    chart.update_layout(margin=dict(t=50, b=50, l=25, r=25))

    return chart


def chart_portfolio_kpi():
    portfolio_value_df = claculate_portfolio_value()
    kpi_portfolio7d_abs = portfolio_value_df.tail(
        7).ptf_value_diff.sum().round(2)

    kpi_portfolio15d_abs = portfolio_value_df.tail(
        15).ptf_value_diff.sum().round(2)
    kpi_portfolio30d_abs = portfolio_value_df.tail(
        30).ptf_value_diff.sum().round(2)
    kpi_portfolio200d_abs = portfolio_value_df.tail(
        200).ptf_value_diff.sum().round(2)
    kpi_portfolio7d_pct = round(
        kpi_portfolio7d_abs/portfolio_value_df.tail(7).portf_value.iloc[0]*100, 2)
    kpi_portfolio15d_pct = round(
        kpi_portfolio15d_abs/portfolio_value_df.tail(15).portf_value.iloc[0]*100, 2)
    kpi_portfolio30d_pct = round(
        kpi_portfolio30d_abs/portfolio_value_df.tail(30).portf_value.iloc[0]*100, 2)
    kpi_portfolio200d_pct = round(
        kpi_portfolio200d_abs/portfolio_value_df.tail(200).portf_value.iloc[0]*100, 2)

    kpi_sp500_7d_abs = portfolio_value_df.tail(7).sp500_diff.sum().round(2)
    kpi_sp500_15d_abs = portfolio_value_df.tail(15).sp500_diff.sum().round(2)
    kpi_sp500_30d_abs = portfolio_value_df.tail(30).sp500_diff.sum().round(2)
    kpi_sp500_200d_abs = portfolio_value_df.tail(200).sp500_diff.sum().round(2)
    kpi_sp500_7d_pct = round(
        kpi_sp500_7d_abs/portfolio_value_df.tail(7).sp500_mktvalue.iloc[0]*100, 2)
    kpi_sp500_15d_pct = round(
        kpi_sp500_15d_abs/portfolio_value_df.tail(15).sp500_mktvalue.iloc[0]*100, 2)
    kpi_sp500_30d_pct = round(
        kpi_sp500_30d_abs/portfolio_value_df.tail(30).sp500_mktvalue.iloc[0]*100, 2)
    kpi_sp500_200d_pct = round(
        kpi_sp500_200d_abs/portfolio_value_df.tail(200).sp500_mktvalue.iloc[0]*100, 2)

    chart = go.Figure()

    chart.layout.template = CHART_THEME
    chart.add_trace(go.Indicator(
        mode="number+delta",
        value=kpi_portfolio7d_pct,
        number={'suffix': " %"},
        title={"text": "<br><span style='font-size:0.7em;color:gray'>7 Days</span>"},
        delta={'position': "bottom",
               'reference': kpi_sp500_7d_pct, 'relative': False},
        domain={'row': 0, 'column': 0}))

    chart.add_trace(go.Indicator(
        mode="number+delta",
        value=kpi_portfolio15d_pct,
        number={'suffix': " %"},
        title={"text": "<span style='font-size:0.7em;color:gray'>15 Days</span>"},
        delta={'position': "bottom",
               'reference': kpi_sp500_15d_pct, 'relative': False},
        domain={'row': 1, 'column': 0}))

    chart.add_trace(go.Indicator(
        mode="number+delta",
        value=kpi_portfolio30d_pct,
        number={'suffix': " %"},
        title={"text": "<span style='font-size:0.7em;color:gray'>30 Days</span>"},
        delta={'position': "bottom",
               'reference': kpi_sp500_30d_pct, 'relative': False},
        domain={'row': 2, 'column': 0}))

    chart.add_trace(go.Indicator(
        mode="number+delta",
        value=kpi_portfolio200d_pct,
        number={'suffix': " %"},
        title={"text": "<span style='font-size:0.7em;color:gray'>200 Days</span>"},
        delta={'position': "bottom",
               'reference': kpi_sp500_200d_pct, 'relative': False},
        domain={'row': 3, 'column': 1}))

    chart.update_layout(
        grid={'rows': 4, 'columns': 1, 'pattern': "independent"},
        margin=dict(l=50, r=50, t=30, b=30)
    )

    return chart


def chart_sp500_kpi():
    portfolio_value_df = claculate_portfolio_value()
    kpi_portfolio7d_abs = portfolio_value_df.tail(
        7).ptf_value_diff.sum().round(2)

    kpi_portfolio15d_abs = portfolio_value_df.tail(
        15).ptf_value_diff.sum().round(2)
    kpi_portfolio30d_abs = portfolio_value_df.tail(
        30).ptf_value_diff.sum().round(2)
    kpi_portfolio200d_abs = portfolio_value_df.tail(
        200).ptf_value_diff.sum().round(2)
    kpi_portfolio7d_pct = round(
        kpi_portfolio7d_abs/portfolio_value_df.tail(7).portf_value.iloc[0]*100, 2)
    kpi_portfolio15d_pct = round(
        kpi_portfolio15d_abs/portfolio_value_df.tail(15).portf_value.iloc[0]*100, 2)
    kpi_portfolio30d_pct = round(
        kpi_portfolio30d_abs/portfolio_value_df.tail(30).portf_value.iloc[0]*100, 2)
    kpi_portfolio200d_pct = round(
        kpi_portfolio200d_abs/portfolio_value_df.tail(200).portf_value.iloc[0]*100, 2)

    kpi_sp500_7d_abs = portfolio_value_df.tail(7).sp500_diff.sum().round(2)
    kpi_sp500_15d_abs = portfolio_value_df.tail(15).sp500_diff.sum().round(2)
    kpi_sp500_30d_abs = portfolio_value_df.tail(30).sp500_diff.sum().round(2)
    kpi_sp500_200d_abs = portfolio_value_df.tail(200).sp500_diff.sum().round(2)
    kpi_sp500_7d_pct = round(
        kpi_sp500_7d_abs/portfolio_value_df.tail(7).sp500_mktvalue.iloc[0]*100, 2)
    kpi_sp500_15d_pct = round(
        kpi_sp500_15d_abs/portfolio_value_df.tail(15).sp500_mktvalue.iloc[0]*100, 2)
    kpi_sp500_30d_pct = round(
        kpi_sp500_30d_abs/portfolio_value_df.tail(30).sp500_mktvalue.iloc[0]*100, 2)
    kpi_sp500_200d_pct = round(
        kpi_sp500_200d_abs/portfolio_value_df.tail(200).sp500_mktvalue.iloc[0]*100, 2)

    chart = go.Figure()

    chart.layout.template = CHART_THEME
    chart.add_trace(go.Indicator(
        mode="number+delta",
        value=kpi_sp500_7d_pct,
        number={'suffix': " %"},
        title={"text": "<br><span style='font-size:0.7em;color:gray'>7 Days</span>"},
        domain={'row': 0, 'column': 0}))

    chart.add_trace(go.Indicator(
        mode="number+delta",
        value=kpi_sp500_15d_pct,
        number={'suffix': " %"},
        title={"text": "<span style='font-size:0.7em;color:gray'>15 Days</span>"},
        domain={'row': 1, 'column': 0}))

    chart.add_trace(go.Indicator(
        mode="number+delta",
        value=kpi_sp500_30d_pct,
        number={'suffix': " %"},
        title={"text": "<span style='font-size:0.7em;color:gray'>30 Days</span>"},
        domain={'row': 2, 'column': 0}))

    chart.add_trace(go.Indicator(
        mode="number+delta",
        value=kpi_sp500_200d_pct,
        number={'suffix': " %"},
        title={"text": "<span style='font-size:0.7em;color:gray'>200 Days</span>"},
        domain={'row': 3, 'column': 1}))

    chart.update_layout(
        grid={'rows': 4, 'columns': 1, 'pattern': "independent"},
        margin=dict(l=50, r=50, t=30, b=30)
    )

    return chart


def build_hierarchical_dataframe(df, levels, value_column, color_columns=None, total_name='total'):
    """
    Build a hierarchy of levels for Sunburst or Treemap charts.

    Levels are given starting from the bottom to the top of the hierarchy,
    ie the last level corresponds to the root.
    """
    df_all_trees = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
    for i, level in enumerate(levels):
        df_tree = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
        dfg = df.groupby(levels[i:]).sum()
        dfg = dfg.reset_index()
        df_tree['id'] = dfg[level].copy()
        if i < len(levels) - 1:
            df_tree['parent'] = dfg[levels[i+1]].copy()
        else:
            df_tree['parent'] = total_name
        df_tree['value'] = dfg[value_column]
        df_tree['color'] = round(
            (dfg[color_columns[0]] / dfg[color_columns[1]]-1)*100, 2)
        df_all_trees = df_all_trees.append(df_tree, ignore_index=True)
    total = pd.Series(dict(id=total_name, parent='',
                           value=df[value_column].sum(),
                           color=100*round(df[color_columns[0]].sum() / df[color_columns[1]].sum()-1, 2)))
    df_all_trees = df_all_trees.append(total, ignore_index=True)
    return df_all_trees


def chart_sunburst():
    portfolio_value_df = claculate_portfolio_value()
    current_positions_df = read_current_position()

    # levels used for the hierarchical chart
    levels = ['ticker', 'industry', 'sector']
    color_columns = ['current_value', 'cml_cost']
    value_column = 'current_value'
    current_ptfvalue = "${:,.2f}".format(
        portfolio_value_df.portf_value.iloc[-1])
    df_all_trees = build_hierarchical_dataframe(
        current_positions_df, levels, value_column, color_columns, total_name='Portfolio')

    average_score = current_positions_df['current_value'].sum(
    ) / current_positions_df['cml_cost'].sum()-1

    chart = make_subplots(
        1, 2, specs=[[{"type": "domain"}, {"type": "domain"}]],)
    chart.layout.template = CHART_THEME
    chart.add_trace(go.Sunburst(
        labels=df_all_trees['id'],
        parents=df_all_trees['parent'],
        values=df_all_trees['value'],
        branchvalues='total',
        marker=dict(
            colors=df_all_trees['color'],
            colorscale='brbg',
            cmid=average_score),
        hovertemplate='<b>%{label} </b> <br> Size: $ %{value}<br> Variation: %{color:.2f}%',
        name=''
    ), 1, 1)

    chart.add_trace(go.Sunburst(
        labels=df_all_trees['id'],
        parents=df_all_trees['parent'],
        values=df_all_trees['value'],
        branchvalues='total',
        marker=dict(
            colors=df_all_trees['color'],
            colorscale='brbg',
            cmid=average_score),
        hovertemplate='<b>%{label} </b> <br> Size: $ %{value}<br> Variation: %{color:.2f}%',
        maxdepth=2,
        name=''
    ), 1, 2)

    chart.update_layout(margin=dict(t=10, b=10, r=10, l=10),
                        paper_bgcolor="#272b30")
    return chart


def chart_sunburst_all():
    portfolio_value_df = claculate_portfolio_value()
    current_positions_df = read_current_position()

    # levels used for the hierarchical chart
    levels = ['ticker', 'industry', 'sector']
    color_columns = ['current_value', 'cml_cost']
    value_column = 'current_value'
    current_ptfvalue = "${:,.2f}".format(
        portfolio_value_df.portf_value.iloc[-1])
    df_all_trees = build_hierarchical_dataframe(
        current_positions_df, levels, value_column, color_columns, total_name='Portfolio')

    average_score = current_positions_df['current_value'].sum(
    ) / current_positions_df['cml_cost'].sum()-1

    chart = go.Figure()
    chart.layout.template = CHART_THEME
    chart.add_trace(go.Sunburst(
        labels=df_all_trees['id'],
        parents=df_all_trees['parent'],
        values=df_all_trees['value'],
        branchvalues='total',
        marker=dict(
            colors=df_all_trees['color'],
            colorscale='brbg',
            cmid=average_score),
        hovertemplate='<b>%{label} </b> <br> Size: $ %{value}<br> Variation: %{color:.2f}%',
        name=''
    ))

    chart.update_layout(margin=dict(t=10, b=10, r=10, l=10))

    return chart, current_ptfvalue


def chart_sunburst_small():
    portfolio_value_df = claculate_portfolio_value()
    current_positions_df = read_current_position()

    # levels used for the hierarchical chart
    levels = ['ticker', 'industry', 'sector']
    color_columns = ['current_value', 'cml_cost']
    value_column = 'current_value'
    current_ptfvalue = "${:,.2f}".format(
        portfolio_value_df.portf_value.iloc[-1])
    df_all_trees = build_hierarchical_dataframe(
        current_positions_df, levels, value_column, color_columns, total_name='Portfolio')

    average_score = current_positions_df['current_value'].sum(
    ) / current_positions_df['cml_cost'].sum()-1

    chart = go.Figure()
    chart.layout.template = CHART_THEME
    chart.add_trace(go.Sunburst(
        labels=df_all_trees['id'],
        parents=df_all_trees['parent'],
        values=df_all_trees['value'],
        branchvalues='total',
        marker=dict(
            colors=df_all_trees['color'],
            colorscale='mrybm',
            cmid=average_score),
        hovertemplate='<b>%{label} </b> <br> Size: $ %{value}<br> Variation: %{color:.2f}%',
        maxdepth=2,
        name=''
    ))

    chart.update_layout(margin=dict(t=10, b=10, r=10, l=10))

    return chart
