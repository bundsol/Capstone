# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_sites = spacex_df['Launch Site'].unique()
drop_options = [{'label': 'All Sites', 'value': 'ALL'} ] 
for site in launch_sites:
    drop_options.append({'label': site, 'value': site})
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout

app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                 dcc.Dropdown(id='site-dropdown', 
                                      options=drop_options,
                                      value='ALL' ,
                                      placeholder='Select a Launch Site here',
                                      searchable=True
                                 ) ,
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', 
                                        min=0, max=10000, step=1000, 
                                        marks={0:'0', 2500: '2,500', 5000: '5,000', 7500: '7,500', 10000:'10,000'} ,
                                        value=[min_payload,max_payload]
                                    ) ,
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):    
    filtered_df = spacex_df

    if entered_site != 'ALL':
        filtered_df = filtered_df[filtered_df["Launch Site"]==entered_site]     
        filtered_df = filtered_df.groupby('class').count() 
        filtered_df.reset_index(inplace=True)
        options = {'values': 'Launch Site', 'names': 'class', 'title': 'Total Success Launches for site %s' % entered_site}
    else:
        options = {'values': 'class', 'names': 'Launch Site', 'title': 'Total Success Launches By Site'}

    fig = px.pie(filtered_df, **options )
    return fig
        # return the outcomes piechart for a selected site


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))
def get_scatter_chart(entered_site, payload_range): 
    filtered_df = spacex_df
    site = 'all Sites'
    range_min = payload_range[0]    
    range_max = payload_range[1]
    if entered_site != 'ALL':
        filtered_df = filtered_df[filtered_df["Launch Site"]==entered_site]     
        site = 'launch site %s' % entered_site
       
    filtered_df = filtered_df[filtered_df['Payload Mass (kg)'] >= range_min]   
    filtered_df = filtered_df[filtered_df['Payload Mass (kg)'] <= range_max]   

    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
    
    fig.update_layout(title='Correlation between Payload and Success for %s' % site)
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
