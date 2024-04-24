"""
Author: Alyssa DeMarco
Date: 04/26/2024
File: main.py
Purpose: launches the IEP dashboard
"""
# imports
from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import scrape
import sankey_diagram as sd

# use scrape.py to import and clean all csvs
# India
df_India = scrape.createImport('India')
# Lebanon
df_Lebanon = scrape.createImport('Lebanon')
# Montenegro
df_Montenegro = scrape.createImport('Montenegro')
# South Africa
df_SouthAfrica = scrape.createImport('SouthAfrica')
# Tajikistan
df_Tajikistan = scrape.createImport('Tajikistan')
# United States
df_UnitedStates = scrape.createImport('UnitedStates')

# initialize app
app = Dash(__name__)
app.config.suppress_callback_exceptions=True

# call a configurization
app.layout = html.Div([
    html.Div([
        # title
        html.H1('Analyzing Ramsar Convention Additional Information'),
        # image
        html.Img(id="ramsar_locs", 
             height=300, 
             src="https://bpb-us-w2.wpmucdn.com/u.osu.edu/dist/d/12517/files/2015/04/MAP-WETLANDS.png-1l4ekto.jpg", 
             ),
], style={'textAlign': 'center'}),
    
    # dropdown selection
    html.P('Select Countries:'),
    dcc.Dropdown(options=[
        {'label': 'India', 'value':"df_India"},
        {'label': 'Lebanon', 'value':"df_Lebanon"},
        {'label': 'Montenegro', 'value':"df_Montenegro"},
        {'label': 'South Africa', 'value':"df_SouthAfrica"},
        {'label': 'Tajikistan', 'value':"df_Tajikistan"},
        {'label': 'United States', 'value':"df_UnitedStates"},
    ], value=["df_SouthAfrica", "df_Montenegro"], id='countries', multi=True, clearable=False),
    
    # sentiment scatter
    html.H3("Sentiment Score Scatter Plot"),
    html.P("This graph represents the sentiment analysis for each additional information section per question.  Each question is plotted on the x-axis while the sentiment score is plotted on the y-axis.  The size of the point is the score the reporter gave (range of 2 to 7 in increasing positivity)"),
    dcc.Graph(id="sentimentScatter"),
    
    # sankey words
    html.H3("Sankey Diagram of Common Words by Country Report"),
    html.P("This Sankey diagram visualizes the most common words written across the whole report for each country.  Filler words were removed beforehand.  Each country is on the left, their most common words on the right, and the bar thinkness is number of uses"),
    dcc.Graph(id="sankeyCommon"),
    
    # bar quantity per score
    html.H3("Average Word Count Per Score Available"),
    html.P("The bar graph represents the average word count for each score possible across the selected countries.  The x-axis is each possible score, and the y-axis is that country's average word count"),
    dcc.Graph(id="barQuantity")
])

# sentiment scatter
@app.callback(
    Output("sentimentScatter", "figure"),
    Input("countries", "value")
)
def updateSent(countries_list):
    # create a dataframe of selected countries dataframes
    countries_list2 = [globals()[x] for x in countries_list]
    df = pd.concat(countries_list2, ignore_index=True)
    # create a score value that can be plotted as point size
    df['score'] = df['score'] + 2
    # generate the figure
    fig = px.scatter(df, x="q_num", y="Sentiment", color="country", size="score")
    return fig

# sankey words
@app.callback(
    Output("sankeyCommon", "figure"),
    Input("countries", "value")
)
def updateSankey(countries_list):
    # create a list of selected countries dataframes
    countries_list2 = [globals()[x] for x in countries_list]

    # generate the figure
    fig = sd.make_nlp_sankey(countries_list2, countries_list)
    return fig

# bar quantity per score
@app.callback(
    Output("barQuantity", "figure"),
    Input("countries", "value")
)
def updateBar(countries_list):
    # create a dataframe of selected countries dataframes
    countries_list2 = [globals()[x] for x in countries_list]
    df = pd.concat(countries_list2, ignore_index=True)

    # group the dataframe by country and then score
    avg_word_count = df.groupby(["country","score"])["cleanText"].apply(lambda x: x.str.split().apply(len).mean()).reset_index()
    avg_word_count.rename(columns={"cleanText": "avg_word_count"}, inplace=True)
    # convert x-axis to string
    avg_word_count['score']=avg_word_count['score'].apply(str)
    
    # generate the figure
    fig = px.bar(avg_word_count, x="score", y="avg_word_count", color = "country", barmode='group', title="Average Word Count by q_num")
    fig.update_xaxes(categoryorder='category ascending')
    return fig


# Run the server
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False, port=8000)