import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import geopandas as gpd

# Load GeoJSON data
data = gpd.read_file(r'maptest3.geojson')
data2 = gpd.read_file(r'finland-with-regions_.geojson')

app = dash.Dash(__name__)

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'  # CSS reset
})

app.layout = html.Div(style={'height': '98vh', 'width': '100%', 'position': 'relative', 'margin': 0, 'padding': 0}, children=[
    
    # Map
    dcc.Graph(
        id='map-graph',
        style={'height': '100%', 'width': '100%'},
        config={'displayModeBar': False}
    ),
    
    # Visibility Check
    html.Div('Test UI', style={'position': 'absolute', 'top': '10px', 'left': '10px', 'z-index': 1000}),
    
    # UI layer
    html.Div(style={'position': 'absolute', 'top': '10px', 'left': '10px', 'z-index': 1000}, children=[
        dcc.Dropdown(
            id='data-dropdown',
            options=[
                {'label': 'Maptest3', 'value': 'maptest3'},
                {'label': 'Finland with Regions', 'value': 'finland-regions'},
            ],
            value='maptest3',  # default value
            style={'width': '250px'}
        ),
        html.Button('Submit', id='submit-button', style={'marginTop': '10px'})
    ])
])

@app.callback(
    Output('map-graph', 'figure'),
    [Input('data-dropdown', 'value')]
)
def update_graph(selected_value):
    if selected_value == 'maptest3':
        data_source = data
    else:  # 'finland-regions'
        data_source = data2

    fig = px.choropleth_mapbox(data_source, geojson=data_source.geometry, locations=data_source.index,
                               color=data_source.index,
                               mapbox_style="carto-positron",
                               center={"lat": 64.5, "lon": 26},
                               zoom=4,
                               hover_name=data_source.get('nimi', ''))  # Adjust as needed

    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        showlegend=False,
        mapbox=dict(
            bearing=0,
            pitch=0,
            zoom=1,
            center={"lat": 64.5, "lon": 26},
            layers=[]
        )
    )

    fig.update_mapboxes(
        bounds_east=56.17,
        bounds_west=-1,
        bounds_north=71,
        bounds_south=59
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
