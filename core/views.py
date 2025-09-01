from django.shortcuts import render
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.io import to_html
from datetime import datetime
from .models import Company

def format_market_cap(market_cap):
    if market_cap is None:
        return "-"

    market_cap = int(market_cap)
    if market_cap >= 10**12:  # Trilyon ve üzeri
        return f'₺{market_cap / 10**12:.3f}T'
    elif market_cap >= 10**9:  # Milyar ve üzeri
        return f'₺{market_cap / 10**9:.3f}B'
    elif market_cap >= 10**6:  # Milyon ve üzeri
        return f'₺{market_cap / 10**6:.3f}M'
    else:
        return f'₺{market_cap}'
    
def format_free_cash_flow(free_cash_flow):
    if free_cash_flow is None:
        return None
   
    abs_value = abs(free_cash_flow)

    billion_value = abs_value / 10**9

    if free_cash_flow < 0:
        return "- {:.2f}B".format(billion_value)
    else:
        return "{:.2f}B".format(billion_value)
    
def format_total_debt(total_debt):
    if total_debt is None:
        return None

    # Veriyi mutlak değere çevir
    abs_value = abs(total_debt)

    # Milyar birimine çevir
    billion_value = abs_value / 10**9

    # Negatif mi pozitif mi olduğuna bakarak uygun biçimde formatla
    if total_debt < 0:
        return "- {:.2f}B".format(billion_value)
    else:
        return "{:.2f}B".format(billion_value)


def marketcap(request):

    symbols = ["ARCLK.IS", "ALARK.IS", "ASELS.IS", "ASTOR.IS", "BIMAS.IS", "BRSAN.IS", "EKGYO.IS", "ENKAI.IS", "EREGL.IS", "FROTO.IS","GUBRF.IS", "HEKTS.IS", "KCHOL.IS", "KONTR.IS", "KOZAL.IS", "KRDMD.IS", "ODAS.IS", "OYAKC.IS", "PETKM.IS", "PGSUS.IS", "SAHOL.IS", "SASA.IS", "SISE.IS", "TCELL.IS", "THYAO.IS", "TOASO.IS", "TUPRS.IS"]
    
    stock_data = {}

    for symbol in symbols:
        ticker = yf.Ticker(symbol)

        #current price
        current_price = ticker.history(period="1d")["Close"].iloc[-1]

        high_52w = ticker.info["fiftyTwoWeekHigh"]
        low_52w = ticker.info["fiftyTwoWeekLow"]

        market_cap = ticker.info["marketCap"]

        # PE Ratio
        pe_ratio = ticker.info.get("trailingPE")
        if pe_ratio is not None:
            pe_ratio = float(pe_ratio)
            pe_ratio = "{:.2f}".format(pe_ratio)

        enterprise_value = ticker.info.get("enterpriseValue")
        ebitda = ticker.info.get("ebitda")

        ev_ebitda = None
        if enterprise_value is not None and ebitda is not None and ebitda != 0:
            ev_ebitda = enterprise_value / ebitda

        free_cash_flow = ticker.info.get("freeCashflow")

        total_debt = ticker.info.get("totalDebt")

        stock_data[symbol] = {
            "current_price": current_price,
            "market_cap": market_cap,
            "high_52w": high_52w,
            "low_52w": low_52w,
            "pe_ratio": pe_ratio,
            "ev_ebitda": ev_ebitda,
            "free_cash_flow": free_cash_flow,
            "total_debt": total_debt
        }
        
        formatted_stock_data = {
        symbol: {
            "current_price": data["current_price"],
            "market_cap": format_market_cap(data["market_cap"]),
            "high_52w": data["high_52w"],
            "low_52w": data["low_52w"],
            "pe_ratio": data["pe_ratio"],
            "ev_ebitda": "{:.2f}".format(data["ev_ebitda"]) if data["ev_ebitda"] is not None else None, #format the data
            "free_cash_flow": format_free_cash_flow(data["free_cash_flow"]), #format the data
            "total_debt": format_total_debt(data["total_debt"]),
        }
        for symbol, data in stock_data.items()
    }
    return render(request, 'marketcap.html', {'stock_data': formatted_stock_data})

def retrieve_stock_data(ticker: str, start_date: str = "2020-01-01", end_date: str = datetime.now().strftime("%Y-%m-%d")):
    ticker_info = ticker.info
    
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    hist_df = ticker.history(start=start_date, end=end_date)
    hist_df = hist_df.reset_index()

    return hist_df, ticker_info

def create_line_chart(hist_df: pd.DataFrame, symbol=None, dark_mode=False):
    # Define colors based on theme
    if dark_mode:
        line_color = '#8B5CF6'  # Purple for dark mode
        fill_color = 'rgba(139, 92, 246, 0.2)'
        plot_bg = 'rgba(17, 24, 39, 0.8)'
        paper_bg = 'rgba(31, 41, 55, 1)'
        grid_color = 'rgba(75, 85, 99, 0.4)'
        line_grid_color = 'rgba(75, 85, 99, 0.6)'
        text_color = '#F9FAFB'
        spike_color = 'rgba(139, 92, 246, 0.8)'
        hover_bg = 'rgba(139, 92, 246, 0.9)'
    else:
        line_color = '#667eea'
        fill_color = 'rgba(102, 126, 234, 0.15)'
        plot_bg = 'rgba(248, 250, 252, 0.6)'
        paper_bg = 'white'
        grid_color = 'rgba(156, 163, 175, 0.3)'
        line_grid_color = 'rgba(156, 163, 175, 0.5)'
        text_color = '#374151'
        spike_color = 'rgba(102, 126, 234, 0.6)'
        hover_bg = 'rgba(102, 126, 234, 0.9)'

    fig = go.Figure(data=[
        go.Scatter(
            x=hist_df['Date'],
            y=hist_df['Close'],
            mode='lines',
            fill='tozeroy',
            fillcolor=fill_color,
            line=dict(
                color=line_color,
                width=3,
                shape='spline',
                smoothing=0.3
            ),
            name='Close Price',
            hovertemplate='<b>%{x|%d %b %Y}</b><br>' +
                         '<b>Close Price:</b> ₺%{y:,.2f}<br>' +
                         f'<b>Symbol:</b> {symbol}<br>' +
                         '<extra></extra>' if symbol else '<extra></extra>',
            hoverlabel=dict(
                bgcolor=hover_bg,
                bordercolor="white" if not dark_mode else "#1F2937",
                font_color="white",
                font_size=12
            )
        )
    ])
    
    fig.update_layout(
        autosize=True,
        plot_bgcolor=plot_bg,
        paper_bgcolor=paper_bg,
        font=dict(
            family="Inter, -apple-system, BlinkMacSystemFont, sans-serif",
            size=12,
            color=text_color
        ),
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False,
        hovermode='x unified',
        transition_duration=300
    )
   
    fig.update_xaxes(
        showgrid=True,
        gridcolor=grid_color,
        gridwidth=1,
        linecolor=line_grid_color,
        linewidth=1,
        tickfont=dict(size=11, color=text_color),
        title_font=dict(size=12, color=text_color),
        nticks=8,
        showspikes=True,
        spikecolor=spike_color,
        spikethickness=1,
        spikedash="dot"
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor=grid_color,
        gridwidth=1,
        linecolor=line_grid_color,
        linewidth=1,
        tickfont=dict(size=11, color=text_color),
        title_font=dict(size=12, color=text_color),
        tickformat=",.0f",
        nticks=6,
        showspikes=True,
        spikecolor=spike_color,
        spikethickness=1,
        spikedash="dot"
    )

    return fig

def get_cash_flow_data(symbol):
    try:
        company_obj = Company.objects.get(symbol=symbol)
        cash_flow_data = company_obj.cash_flow
        return cash_flow_data
    
    except Company.DoesNotExist:
        return None
    
def get_income_statement_data(symbol):
    try:
        company_obj = Company.objects.get(symbol=symbol)
        income_statement_data = company_obj.income_statement
        return income_statement_data
    
    except Company.DoesNotExist:
        return None
    
def get_balance_sheet_data(symbol):
    try:
        company_obj = Company.objects.get(symbol=symbol)
        balance_sheet_data = company_obj.balance_sheet
        return balance_sheet_data
    
    except Company.DoesNotExist:
        return None
    
def get_profitability_data(symbol):
    try:
        company_obj = Company.objects.get(symbol=symbol)
        profitability_data = company_obj.profitability
        return profitability_data
    
    except Company.DoesNotExist:
        return None
    
def get_stock_name(symbol):
    company_obj = Company.objects.get(symbol=symbol)
    stock_name = company_obj.name
    return stock_name
    
def generate_net_debt_change_chart(symbol, dark_mode=False):
    # Sembole göre finansal verileri çek
    ticker = yf.Ticker(symbol)
    
    try:
        # Bilanço tablosunu al
        balance_sheet_annual = ticker.balance_sheet
        # DataFrame oluştur
        df_balance_sheet = pd.DataFrame(balance_sheet_annual)
        
        # Gerekli verileri seç
        required_values = ['Total Debt', 'Cash And Cash Equivalents', 'Other Short Term Investments']
        
        # Anahtarların veri setinde olup olmadığını kontrol et
        if 'Other Short Term Investments' not in df_balance_sheet.index:
            required_values.remove('Other Short Term Investments')
        
        # Seçilen verileri bir önceki yılın verileriyle birleştir
        selected_data = df_balance_sheet.loc[required_values].T
        
        # Tarih aralığını oluştur
        dates = pd.date_range('2020-12-31', '2023-12-31', freq='Y')
        
        # Seçilen verileri belirtilen tarih aralığına göre filtrele
        selected_data = selected_data[selected_data.index.isin(dates)]
        
        # Farkları içeren bir DataFrame oluştur
        percentage_change_df = pd.DataFrame(columns=['2021', '2022', '2023'])
        
        if '2020-12-31' in selected_data.index and '2021-12-31' in selected_data.index:
            percentage_change_2021_2020 = (selected_data.loc['2021-12-31'] / selected_data.loc['2020-12-31'] - 1) * 100
            percentage_change_df['2021'] = percentage_change_2021_2020
        
        if '2021-12-31' in selected_data.index and '2022-12-31' in selected_data.index:
            percentage_change_2022_2021 = (selected_data.loc['2022-12-31'] / selected_data.loc['2021-12-31'] - 1) * 100
            percentage_change_df['2022'] = percentage_change_2022_2021
        
        if '2022-12-31' in selected_data.index and '2023-12-31' in selected_data.index:
            percentage_change_2023_2022 = (selected_data.loc['2023-12-31'] / selected_data.loc['2022-12-31'] - 1) * 100
            percentage_change_df['2023'] = percentage_change_2023_2022
            
        # Finansal kalemleri ayrı sütunlar olarak ayır
        separated_df = pd.DataFrame()
            
        for index in percentage_change_df.index:
            separated_df[index] = percentage_change_df.loc[index]
            

        
        fig = go.Figure()
        
        # Define colors based on theme
        if dark_mode:
            colors = [
                "rgba(139, 92, 246, 0.8)",   # Purple
                "rgba(251, 191, 36, 0.8)",   # Amber
                "rgba(34, 197, 94, 0.8)"     # Green
            ]
            hover_colors = [
                "rgba(139, 92, 246, 1.0)",
                "rgba(251, 191, 36, 1.0)", 
                "rgba(34, 197, 94, 1.0)"
            ]
            plot_bg = 'rgba(17, 24, 39, 0.6)'
            paper_bg = 'rgba(31, 41, 55, 1)'
            text_color = '#F9FAFB'
            grid_color = 'rgba(75, 85, 99, 0.3)'
            line_color = 'rgba(75, 85, 99, 0.6)'
            legend_bg = 'rgba(55, 65, 81, 0.9)'
            legend_border = 'rgba(75, 85, 99, 0.5)'
        else:
            colors = [
                "rgba(102, 126, 234, 0.8)",   # Primary blue
                "rgba(245, 184, 73, 0.8)",    # Warm orange  
                "rgba(34, 197, 94, 0.8)"      # Fresh green
            ]
            hover_colors = [
                "rgba(102, 126, 234, 1.0)",
                "rgba(245, 184, 73, 1.0)", 
                "rgba(34, 197, 94, 1.0)"
            ]
            plot_bg = 'rgba(248, 250, 252, 0.4)'
            paper_bg = 'white'
            text_color = '#374151'
            grid_color = 'rgba(156, 163, 175, 0.2)'
            line_color = 'rgba(156, 163, 175, 0.5)'
            legend_bg = 'rgba(255, 255, 255, 0.8)'
            legend_border = 'rgba(156, 163, 175, 0.3)'
            
        for i, column in enumerate(separated_df.columns):
            fig.add_trace(go.Bar(
                x=[f"202{i+1}" for i in range(len(separated_df))], 
                y=separated_df[column], 
                name=column,
                marker=dict(
                    color=colors[i],
                    line=dict(color=hover_colors[i], width=2),
                    cornerradius=8
                ),
                text=[f"{val:.1f}%" for val in separated_df[column]],
                textposition='auto',
                textfont=dict(
                    size=12,
                    color="white",
                    family="Inter, sans-serif"
                ),
                hovertemplate='<b>%{fullData.name}</b><br>' +
                             '<b>Year:</b> %{x}<br>' +
                             '<b>Change:</b> %{y:.1f}%<br>' +
                             '<extra></extra>',
                hoverlabel=dict(
                    bgcolor=hover_colors[i],
                    bordercolor="white",
                    font_color="white"
                ),
                showlegend=True
            ))
            
        fig.update_layout(
            title='',
            autosize=True,
            plot_bgcolor=plot_bg,
            paper_bgcolor=paper_bg,
            barmode='group',
            bargap=0.15,
            bargroupgap=0.1,
            font=dict(
                family="Inter, -apple-system, BlinkMacSystemFont, sans-serif",
                size=12,
                color=text_color
            ),
            margin=dict(l=20, r=20, t=20, b=40),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.15,
                xanchor="center",
                x=0.5,
                bgcolor=legend_bg,
                bordercolor=legend_border,
                borderwidth=1,
                font=dict(size=11, color=text_color)
            ),
            hovermode='x unified',
            transition_duration=300
        )
            
        fig.for_each_trace(lambda trace: trace.update(name=trace.name.replace('Total Debt', 'Financial Debt')))
            
        fig.update_xaxes(
            showline=True, 
            linewidth=1, 
            linecolor=line_color,
            showgrid=True,
            gridcolor=grid_color,
            tickfont=dict(size=11, color=text_color),
            title_font=dict(size=12, color=text_color)
        )
        
        fig.update_yaxes(
            showline=True, 
            linewidth=1, 
            linecolor=line_color,
            showgrid=True,
            gridcolor=grid_color,
            tickfont=dict(size=11, color=text_color),
            title_font=dict(size=12, color=text_color),
            ticksuffix="%",
            zeroline=True,
            zerolinecolor=line_color,
            zerolinewidth=2
        )
        
    except KeyError:
        print("Veri setinde beklenmeyen bir anahtar bulundu.")
        return None

    return fig



def profile(request, symbol):
    stocks = {
        "ARCLK.IS": "ARCLK", "ALARK.IS": "ALARK", "ASELS.IS": "ASELS", "ASTOR.IS": "ASTOR", "BIMAS.IS": "BIMAS", "BRSAN.IS": "BRSAN","EKGYO.IS": "EKGYO",
        "ENKAI.IS": "ENKAI","EREGL.IS": "EREGL", "FROTO.IS": "FROTO","GUBRF.IS": "GUBRF","HEKTS.IS": "HEKTS","KCHOL.IS": "KCHOL","KONTR.IS": "KONTR", 
        "KOZAL.IS": "KOZAL","KRDMD.IS": "KRDMD","ODAS.IS": "ODAS","OYAKC.IS": "OYAKC","PETKM.IS": "PETKM",
        "PGSUS.IS": "PGSUS","SAHOL.IS": "SAHOL","SASA.IS": "SASA","SISE.IS": "SISE", 
        "TCELL.IS": "TCELL","THYAO.IS": "THYAO","TOASO.IS": "TOASO","TUPRS.IS": "TUPRS",
    }

    stock_data = {}

    label = stocks.get(symbol)

    if label:
        ticker = yf.Ticker(symbol)

        pe_ratio = ticker.info.get("trailingPE", "N/A")
        price_to_book = ticker.info.get("priceToBook", "N/A")

        enterprise_value = ticker.info.get("enterpriseValue", "N/A")
        ebitda = ticker.info.get("ebitda", "N/A")
        enterpriseToEbitda = ticker.info.get("enterpriseToEbitda", "N/A")

        ev_fcff = None
        free_cash_flow = ticker.info.get("freeCashflow", "N/A")
        if enterprise_value != "N/A" and free_cash_flow != "N/A":
            ev_fcff = round(enterprise_value / free_cash_flow, 2)
        else:
            ev_fcff = "N/A"
            
        roa = ticker.info.get("returnOnAssets", "N/A")
        roe = ticker.info.get("returnOnEquity", "N/A")
        current_ratio = ticker.info.get("currentRatio", "N/A")
        quick_ratio = ticker.info.get("quickRatio", "N/A")

        total_debt = ticker.info.get("totalDebt", "N/A")
        total_debt_to_fcf = None
    
        # total_debt and free_cash_flow convert to float
        try:
            total_debt = float(total_debt)
            free_cash_flow = float(free_cash_flow)
        except (TypeError, ValueError):
        #excepting errors
            total_debt = None
            free_cash_flow = None

        # total_debt_to_fcf calculation
        if total_debt is not None and free_cash_flow is not None:
            total_debt_to_fcf = round(total_debt / free_cash_flow, 2)
        else:
            total_debt_to_fcf = "N/A" 

        marketcap = ticker.info.get("marketCap", "N/A")
        total_cash = ticker.info.get("totalCash", "N/A")
        cash_to_marketcap = None
        if total_cash and marketcap:
            cash_to_marketcap = round(total_cash / marketcap, 2)
        
        #details about company
        company_info = ticker.info
        address = company_info.get("address2")
        city = company_info.get("city")
        country = company_info.get("country")
        sector = company_info.get("sector")
        industry = company_info.get("industry")
        phone = company_info.get("phone")
        website = company_info.get("website")
        long_name = company_info.get("longName")

        long_description = company_info.get("longBusinessSummary")

        company_officers = ticker.info.get("companyOfficers", [])
        ceo = "N/A"
        cfo = "N/A"

        # For now, default to light mode charts
        # The charts will adapt based on your existing dark mode CSS
        dark_mode = False
        
        # Get stock data for chart
        hist_df_tl, info = retrieve_stock_data(ticker)
        linechart_fig = create_line_chart(hist_df_tl, symbol, dark_mode)
        
        # Get basic price data for change calculation  
        hist_df_basic = yf.download(symbol, start="2020-01-01", end=datetime.now().strftime("%Y-%m-%d"))

        chart_div = to_html(
            linechart_fig, 
            full_html=False, 
            include_plotlyjs="cdn",
            config={
                'responsive': True,
                'displayModeBar': False,
                'scrollZoom': True,
                'doubleClick': 'reset+autosize',
                'showTips': False,
                'editable': False,
                'staticPlot': False
            }
        )
        p1, p2 = hist_df_basic["Close"].values[-1], hist_df_basic["Close"].values[-2]
        change, prcnt_change = (p2-p1), (p2-p1) / p1
        columnchart_fig = generate_net_debt_change_chart(symbol, dark_mode)
        chart_netdebt_div = to_html(
            columnchart_fig, 
            full_html=False, 
            include_plotlyjs="cdn",
            config={
                'responsive': True,
                'displayModeBar': False,
                'scrollZoom': False,
                'doubleClick': 'reset+autosize'
            }
        )

        cash_flow= get_cash_flow_data(symbol)
        income_data = get_income_statement_data(symbol)
        balance_data = get_balance_sheet_data(symbol)
        profitability_data = get_profitability_data(symbol)
        stock_name = get_stock_name(symbol)


        for officer in company_officers:
            title = officer.get("title", "").lower()  # Unvanı küçük harfe dönüştür
            if "ceo" in title or "chief executive" in title or "gm" in title or "general manager" in title:
                ceo = officer.get("name", "N/A")
            elif "cfo" in title or "chief financial" in title or "head of financial" in title or "director of finance" in title or "financial director":
                cfo = officer.get("name", "N/A")

        stock_data = {
            "pe_ratio": round(float(pe_ratio), 2) if pe_ratio != "N/A" else pe_ratio,
            "price_to_book": round(price_to_book, 2) if price_to_book != "N/A" else price_to_book,
            "ev_ebitda": round(enterpriseToEbitda, 2) if enterpriseToEbitda != "N/A" else enterpriseToEbitda,
            "ebitda": round(ebitda, 2) if ebitda != "N/A" else ebitda,
            "ev_fcff": ev_fcff,
            "roa": round(roa * 100, 2) if isinstance(roa, float) else roa,
            "roe": round(roe * 100, 2) if isinstance(roe, float) else roe,
            "current_ratio": round(current_ratio, 2) if current_ratio != "N/A" else current_ratio,
            "quick_ratio": round(quick_ratio, 2) if quick_ratio != "N/A" else quick_ratio,
            "total_debt_to_fcf": total_debt_to_fcf,
            "cash_market_cap": cash_to_marketcap,

            
            "address": address,
            "city": city,
            "country": country,
            "phone": phone,
            "website": website,
            "long_name": long_name,
            "long_description": long_description,
            "sector": sector,
            "industry": industry,
            "ceo": ceo,
            "cfo": cfo,
            "chart_div": chart_div,
            "chart_netdebt_div": chart_netdebt_div,
            "cash_flow": cash_flow,
            "income_data": income_data,
            "balance_data": balance_data,
            "profitability_data": profitability_data,
            "stock_name": stock_name,
        }

        # Verileri şablona gönderin
        return render(request, 'profile_improved.html', {'symbol': symbol, 'stock_data': stock_data})
    else:
        # Geçersiz sembol durumunda hata sayfasına yönlendirme
        return render(request, 'error.html', {'error_message': 'Geçersiz sembol: {}'.format(symbol)})

def tables (request): 
    return render(request, 'tables.html')

def tables2 (request): 
    return render(request, 'tables2.html')

def datatables_improved(request):
    return render(request, 'datatables_improved.html')

def apexcolumncharts (request): 
    return render(request, 'apexcolumncharts.html') 

def apexlinecharts (request):     
    return render(request, 'apexlinecharts.html')

