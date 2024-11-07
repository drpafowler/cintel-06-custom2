
import requests
import json
import seaborn as sns
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import os
from datetime import datetime
from shiny import reactive
from shiny.express import input, render, ui
from shinywidgets import render_widget  

@reactive.calc
def url():
    return f"https://v6.exchangerate-api.com/v6/e4422bdb5030904fad352315/latest/USD"

@render.code
async def info():
    response = requests.get(url())
    if response.status_code == 200:
        exrate = json.loads(response.text)['conversion_rates']
        filename = "exchange_rate.txt"
        with open(filename, "w") as file:
            file.write(json.dumps(exrate))
        return exrate
    else:
        return None

# Load Historical Data
current_dir = os.path.dirname(os.path.abspath(__file__))
historical_data_path = os.path.join(current_dir, "historical_rates_fixed.csv")
historical_df = pd.read_csv(historical_data_path)
historical_df['Date'] = pd.to_datetime(historical_df['Date'])

@reactive.calc
def exchange_rate_df():
    filename = "exchange_rate.txt"
    with open(filename, "r") as file:
        exrate = json.load(file)
    df = pd.DataFrame(list(exrate.items()), columns=['Currency', 'Rate'])
    return df

@reactive.calc
def historical_rates_df():
    filename = "historical_rates_fixed.csv"
    df = pd.read_csv(filename)
    return df

@reactive.calc()
def filtered_historical_df():
    # Get the selected time interval from the input
    selected_interval = input.daterange()
    # Filter the historical_df based on the selected interval
    start_date, end_date = selected_interval
    filtered_df = historical_df[(historical_df['Date'] >= start_date) & (historical_df['Date'] <= end_date)]
    return filtered_df

ui.page_opts(
    title="App with navbar",
    fillable=True,    
)

with ui.sidebar(bg="#f8f8f8", width=400):  
    "Sidebar" 
    ui.input_selectize(
        "input_currency", 
        "Input Currency",
        {'AED': 'UAE Dirham', 'AFN': 'Afghan Afghani', 'ALL': 'Albanian Lek', 'AMD': 'Armenian Dram', 'ANG': 'Netherlands Antillian Guilder', 'AOA': 'Angolan Kwanza', 'ARS': 'Argentine Peso', 'AUD': 'Australian Dollar', 'AWG': 'Aruban Florin', 'AZN': 'Azerbaijani Manat', 'BAM': 'Bosnia and Herzegovina Mark', 'BBD': 'Barbados Dollar', 'BDT': 'Bangladeshi Taka', 'BGN': 'Bulgarian Lev', 'BHD': 'Bahraini Dinar', 'BIF': 'Burundian Franc', 'BMD': 'Bermudian Dollar', 'BND': 'Brunei Dollar', 'BOB': 'Bolivian Boliviano', 'BRL': 'Brazilian Real', 'BSD': 'Bahamian Dollar', 'BTN': 'Bhutanese Ngultrum', 'BWP': 'Botswana Pula', 'BYN': 'Belarusian Ruble', 'BZD': 'Belize Dollar', 'CAD': 'Canadian Dollar', 'CDF': 'Congolese Franc', 'CHF': 'Swiss Franc', 'CLP': 'Chilean Peso', 'CNY': 'Chinese Renminbi', 'COP': 'Colombian Peso', 'CRC': 'Costa Rican Colon', 'CUP': 'Cuban Peso', 'CVE': 'Cape Verdean Escudo', 'CZK': 'Czech Koruna', 'DJF': 'Djiboutian Franc', 'DKK': 'Danish Krone', 'DOP': 'Dominican Peso', 'DZD': 'Algerian Dinar', 'EGP': 'Egyptian Pound', 'ERN': 'Eritrean Nakfa', 'ETB': 'Ethiopian Birr', 'EUR': 'Euro', 'FJD': 'Fiji Dollar', 'FKP': 'Falkland Islands Pound', 'FOK': 'Faroese Króna', 'GBP': 'Pound Sterling', 'GEL': 'Georgian Lari', 'GGP': 'Guernsey Pound', 'GHS': 'Ghanaian Cedi', 'GIP': 'Gibraltar Pound', 'GMD': 'Gambian Dalasi', 'GNF': 'Guinean Franc', 'GTQ': 'Guatemalan Quetzal', 'GYD': 'Guyanese Dollar', 'HKD': 'Hong Kong Dollar', 'HNL': 'Honduran Lempira', 'HRK': 'Croatian Kuna', 'HTG': 'Haitian Gourde', 'HUF': 'Hungarian Forint', 'IDR': 'Indonesian Rupiah', 'ILS': 'Israeli New Shekel', 'IMP': 'Manx Pound', 'INR': 'Indian Rupee', 'IQD': 'Iraqi Dinar', 'IRR': 'Iranian Rial', 'ISK': 'Icelandic Króna', 'JEP': 'Jersey Pound', 'JMD': 'Jamaican Dollar', 'JOD': 'Jordanian Dinar', 'JPY': 'Japanese Yen', 'KES': 'Kenyan Shilling', 'KGS': 'Kyrgyzstani Som', 'KHR': 'Cambodian Riel', 'KID': 'Kiribati Dollar', 'KMF': 'Comorian Franc', 'KRW': 'South Korean Won', 'KWD': 'Kuwaiti Dinar', 'KYD': 'Cayman Islands Dollar', 'KZT': 'Kazakhstani Tenge', 'LAK': 'Lao Kip', 'LBP': 'Lebanese Pound', 'LKR': 'Sri Lanka Rupee', 'LRD': 'Liberian Dollar', 'LSL': 'Lesotho Loti', 'LYD': 'Libyan Dinar', 'MAD': 'Moroccan Dirham', 'MDL': 'Moldovan Leu', 'MGA': 'Malagasy Ariary', 'MKD': 'Macedonian Denar', 'MMK': 'Burmese Kyat', 'MNT': 'Mongolian Tögrög', 'MOP': 'Macanese Pataca', 'MRU': 'Mauritanian Ouguiya', 'MUR': 'Mauritian Rupee', 'MVR': 'Maldivian Rufiyaa', 'MWK': 'Malawian Kwacha', 'MXN': 'Mexican Peso', 'MYR': 'Malaysian Ringgit', 'MZN': 'Mozambican Metical', 'NAD': 'Namibian Dollar', 'NGN': 'Nigerian Naira', 'NIO': 'Nicaraguan Córdoba', 'NOK': 'Norwegian Krone', 'NPR': 'Nepalese Rupee', 'NZD': 'New Zealand Dollar', 'OMR': 'Omani Rial', 'PAB': 'Panamanian Balboa', 'PEN': 'Peruvian Sol', 'PGK': 'Papua New Guinean Kina', 'PHP': 'Philippine Peso', 'PKR': 'Pakistani Rupee', 'PLN': 'Polish Złoty', 'PYG': 'Paraguayan Guaraní', 'QAR': 'Qatari Riyal', 'RON': 'Romanian Leu', 'RSD': 'Serbian Dinar', 'RUB': 'Russian Ruble', 'RWF': 'Rwandan Franc', 'SAR': 'Saudi Riyal', 'SBD': 'Solomon Islands Dollar', 'SCR': 'Seychellois Rupee', 'SDG': 'Sudanese Pound', 'SEK': 'Swedish Krona', 'SGD': 'Singapore Dollar', 'SHP': 'Saint Helena Pound', 'SLE': 'Sierra Leonean Leone', 'SOS': 'Somali Shilling', 'SRD': 'Surinamese Dollar', 'SSP': 'South Sudanese Pound', 'STN': 'São Tomé and Príncipe Dobra', 'SYP': 'Syrian Pound', 'SZL': 'Eswatini Lilangeni', 'THB': 'Thai Baht', 'TJS': 'Tajikistani Somoni', 'TMT': 'Turkmenistan Manat', 'TND': 'Tunisian Dinar', 'TOP': 'Tongan Paʻanga', 'TRY': 'Turkish Lira', 'TTD': 'Trinidad and Tobago Dollar', 'TVD': 'Tuvaluan Dollar', 'TWD': 'New Taiwan Dollar', 'TZS': 'Tanzanian Shilling', 'UAH': 'Ukrainian Hryvnia', 'UGX': 'Ugandan Shilling', 'USD': 'United States Dollar', 'UYU': 'Uruguayan Peso', 'UZS': "Uzbekistani So'm", 'VES': 'Venezuelan Bolívar Soberano', 'VND': 'Vietnamese Đồng', 'VUV': 'Vanuatu Vatu', 'WST': 'Samoan Tālā', 'XAF': 'Central African CFA Franc', 'XCD': 'East Caribbean Dollar', 'XDR': 'Special Drawing Rights', 'XOF': 'West African CFA franc', 'XPF': 'CFP Franc', 'YER': 'Yemeni Rial', 'ZAR': 'South African Rand', 'ZMW': 'Zambian Kwacha', 'ZWL': 'Zimbabwean Dollar'}
    )
    ui.input_selectize(
        "output_currency", 
        "Output Currency",
        {'AED': 'UAE Dirham', 'AFN': 'Afghan Afghani', 'ALL': 'Albanian Lek', 'AMD': 'Armenian Dram', 'ANG': 'Netherlands Antillian Guilder', 'AOA': 'Angolan Kwanza', 'ARS': 'Argentine Peso', 'AUD': 'Australian Dollar', 'AWG': 'Aruban Florin', 'AZN': 'Azerbaijani Manat', 'BAM': 'Bosnia and Herzegovina Mark', 'BBD': 'Barbados Dollar', 'BDT': 'Bangladeshi Taka', 'BGN': 'Bulgarian Lev', 'BHD': 'Bahraini Dinar', 'BIF': 'Burundian Franc', 'BMD': 'Bermudian Dollar', 'BND': 'Brunei Dollar', 'BOB': 'Bolivian Boliviano', 'BRL': 'Brazilian Real', 'BSD': 'Bahamian Dollar', 'BTN': 'Bhutanese Ngultrum', 'BWP': 'Botswana Pula', 'BYN': 'Belarusian Ruble', 'BZD': 'Belize Dollar', 'CAD': 'Canadian Dollar', 'CDF': 'Congolese Franc', 'CHF': 'Swiss Franc', 'CLP': 'Chilean Peso', 'CNY': 'Chinese Renminbi', 'COP': 'Colombian Peso', 'CRC': 'Costa Rican Colon', 'CUP': 'Cuban Peso', 'CVE': 'Cape Verdean Escudo', 'CZK': 'Czech Koruna', 'DJF': 'Djiboutian Franc', 'DKK': 'Danish Krone', 'DOP': 'Dominican Peso', 'DZD': 'Algerian Dinar', 'EGP': 'Egyptian Pound', 'ERN': 'Eritrean Nakfa', 'ETB': 'Ethiopian Birr', 'EUR': 'Euro', 'FJD': 'Fiji Dollar', 'FKP': 'Falkland Islands Pound', 'FOK': 'Faroese Króna', 'GBP': 'Pound Sterling', 'GEL': 'Georgian Lari', 'GGP': 'Guernsey Pound', 'GHS': 'Ghanaian Cedi', 'GIP': 'Gibraltar Pound', 'GMD': 'Gambian Dalasi', 'GNF': 'Guinean Franc', 'GTQ': 'Guatemalan Quetzal', 'GYD': 'Guyanese Dollar', 'HKD': 'Hong Kong Dollar', 'HNL': 'Honduran Lempira', 'HRK': 'Croatian Kuna', 'HTG': 'Haitian Gourde', 'HUF': 'Hungarian Forint', 'IDR': 'Indonesian Rupiah', 'ILS': 'Israeli New Shekel', 'IMP': 'Manx Pound', 'INR': 'Indian Rupee', 'IQD': 'Iraqi Dinar', 'IRR': 'Iranian Rial', 'ISK': 'Icelandic Króna', 'JEP': 'Jersey Pound', 'JMD': 'Jamaican Dollar', 'JOD': 'Jordanian Dinar', 'JPY': 'Japanese Yen', 'KES': 'Kenyan Shilling', 'KGS': 'Kyrgyzstani Som', 'KHR': 'Cambodian Riel', 'KID': 'Kiribati Dollar', 'KMF': 'Comorian Franc', 'KRW': 'South Korean Won', 'KWD': 'Kuwaiti Dinar', 'KYD': 'Cayman Islands Dollar', 'KZT': 'Kazakhstani Tenge', 'LAK': 'Lao Kip', 'LBP': 'Lebanese Pound', 'LKR': 'Sri Lanka Rupee', 'LRD': 'Liberian Dollar', 'LSL': 'Lesotho Loti', 'LYD': 'Libyan Dinar', 'MAD': 'Moroccan Dirham', 'MDL': 'Moldovan Leu', 'MGA': 'Malagasy Ariary', 'MKD': 'Macedonian Denar', 'MMK': 'Burmese Kyat', 'MNT': 'Mongolian Tögrög', 'MOP': 'Macanese Pataca', 'MRU': 'Mauritanian Ouguiya', 'MUR': 'Mauritian Rupee', 'MVR': 'Maldivian Rufiyaa', 'MWK': 'Malawian Kwacha', 'MXN': 'Mexican Peso', 'MYR': 'Malaysian Ringgit', 'MZN': 'Mozambican Metical', 'NAD': 'Namibian Dollar', 'NGN': 'Nigerian Naira', 'NIO': 'Nicaraguan Córdoba', 'NOK': 'Norwegian Krone', 'NPR': 'Nepalese Rupee', 'NZD': 'New Zealand Dollar', 'OMR': 'Omani Rial', 'PAB': 'Panamanian Balboa', 'PEN': 'Peruvian Sol', 'PGK': 'Papua New Guinean Kina', 'PHP': 'Philippine Peso', 'PKR': 'Pakistani Rupee', 'PLN': 'Polish Złoty', 'PYG': 'Paraguayan Guaraní', 'QAR': 'Qatari Riyal', 'RON': 'Romanian Leu', 'RSD': 'Serbian Dinar', 'RUB': 'Russian Ruble', 'RWF': 'Rwandan Franc', 'SAR': 'Saudi Riyal', 'SBD': 'Solomon Islands Dollar', 'SCR': 'Seychellois Rupee', 'SDG': 'Sudanese Pound', 'SEK': 'Swedish Krona', 'SGD': 'Singapore Dollar', 'SHP': 'Saint Helena Pound', 'SLE': 'Sierra Leonean Leone', 'SOS': 'Somali Shilling', 'SRD': 'Surinamese Dollar', 'SSP': 'South Sudanese Pound', 'STN': 'São Tomé and Príncipe Dobra', 'SYP': 'Syrian Pound', 'SZL': 'Eswatini Lilangeni', 'THB': 'Thai Baht', 'TJS': 'Tajikistani Somoni', 'TMT': 'Turkmenistan Manat', 'TND': 'Tunisian Dinar', 'TOP': 'Tongan Paʻanga', 'TRY': 'Turkish Lira', 'TTD': 'Trinidad and Tobago Dollar', 'TVD': 'Tuvaluan Dollar', 'TWD': 'New Taiwan Dollar', 'TZS': 'Tanzanian Shilling', 'UAH': 'Ukrainian Hryvnia', 'UGX': 'Ugandan Shilling', 'USD': 'United States Dollar', 'UYU': 'Uruguayan Peso', 'UZS': "Uzbekistani So'm", 'VES': 'Venezuelan Bolívar Soberano', 'VND': 'Vietnamese Đồng', 'VUV': 'Vanuatu Vatu', 'WST': 'Samoan Tālā', 'XAF': 'Central African CFA Franc', 'XCD': 'East Caribbean Dollar', 'XDR': 'Special Drawing Rights', 'XOF': 'West African CFA franc', 'XPF': 'CFP Franc', 'YER': 'Yemeni Rial', 'ZAR': 'South African Rand', 'ZMW': 'Zambian Kwacha', 'ZWL': 'Zimbabwean Dollar'}
    )
    ui.input_date_range("daterange", "Date range", start="2004-01-01")  

with ui.layout_columns():
    with ui.value_box():
        "Conversion Rate"
        @render.text
        def conversion_text():
            df = exchange_rate_df()
            input_currency = input.input_currency()
            output_currency = input.output_currency()
            usd_rate_input = df[df['Currency'] == input_currency]['Rate'].values[0]
            usd_rate_output = df[df['Currency'] == output_currency]['Rate'].values[0]
            conversion_rate = usd_rate_output / usd_rate_input
            return f"1 {input_currency} is equal to {conversion_rate:.4f} {output_currency}"

        

    with ui.card(bg="light", width=6):
        @ render.data_frame
        async def table():
            return exchange_rate_df()
with ui.card():
    ui.card_header("Historical Data")   

