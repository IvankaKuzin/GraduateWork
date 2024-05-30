from dash import Dash, Input, Output, html, dcc
import base64
from graphs_individual_services import *
from graphs_all_services import *

# Ініціалізація додатку
app = Dash(__name__)

# Загальний блок виводу
app.layout = html.Div(className='mainDiv', children=[
    dcc.Store(id='store'),
    html.H1('Характеристика сервісів'),
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Усі кіно-сервіси', value='tab-1', className='tab1', selected_className='custom-tab1--selected'),
        dcc.Tab(value='tab-2', className='tab2', selected_className='custom-tab2--selected'),
        dcc.Tab(value='tab-3', className='tab3', selected_className='custom-tab3--selected'),
        dcc.Tab(value='tab-4', className='tab4', selected_className='custom-tab4--selected')
    ]),

    html.Div(id='secondMenu', children=[
        html.Div(id='dropdownDiv', children=[
            html.H2('Оберіть тип контенту:'),
            dcc.Dropdown(['Загальний контент', 'Фільми', 'Серіали'],
                         'Загальний контент', id='type-dropdown'),
        ]),

        html.Div(id='sliderDiv', children=[
            html.Div(id='slider',children=[
                dcc.RangeSlider(
                    id='range-slider',
                    min=0,
                    max=10,
                    step=1,
                    value=[0, 10],
                    className='range-slider'
                )
            ]),
            html.H2(': Оберіть рейтинг контенту')
        ])
    ]),

    html.Div(id='tabs-content')
])

# Функція реалізації блоку виводу по першому сервісі
def create_statistics_layout_netflix(df, img):
    df_netflix = pd.read_csv('D:/GraduateWork/GradWork/data/netflix_titles.csv')

    pie_chart = creation_type_content_graph(df_netflix, 'red', '#800000')

    bar_chart_figure = creation_age_graph(df, 'red')

    hbar_chart = creation_genre_graph(df, 'red')

    content_map = creation_map(df, 'Reds')

    with open(img, 'rb') as img_file:
        image_string = base64.b64encode(img_file.read()).decode()

    # Отримайте топ-5 фільмів/серіалів за середнім рейтингом
    top_5_movies = df.nlargest(5, 'averageRating')[['title', 'type', 'averageRating', 'description']]

    return html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    html.Img(src='data:image/png;base64,' + image_string, style={'width': '800px', 'height': '300px'}),

                    dcc.Graph(id='pie-chart', figure={'data': [pie_chart], 'layout': {'width': 450, 'height': 450,
                                                                                      'paper_bgcolor': 'black',
                                                                                      'legend': {'font': {
                                                                                          'color': 'white'}}
                                                                                      }})
                ], style={'display': 'flex', 'justifyContent': 'space-around', 'align-items': 'center'}),

                html.Div(children=[
                    dcc.Graph(id='bar-chart', figure=bar_chart_figure),

                    html.Div(children=[
                        html.H2('Топ-5 фільмів/серіалів', style={'text-align': 'center'}),
                        html.Table([
                            *[html.Tr([
                                html.Tr([
                                    html.Td([
                                        html.Span(f"{movie['title']} ", style={'color': 'red'}),
                                        # Змініть колір за потребою
                                        f"({movie['averageRating']}) {movie['type']}"
                                    ],
                                        style={'text-align': 'left', 'font-size': '20px'}),
                                ]),
                                html.Tr([
                                    html.Td(movie['description'], style={'text-align': 'left', 'font-size': '18px',
                                                                         'border-bottom': '1px solid red'})
                                ])
                            ]) for _, movie in top_5_movies.iterrows()]
                        ])

                    ], style={'color': 'white'})
                ], style={'display': 'flex', 'justifyContent': 'space-around',
                          'align-items': 'center', 'marginTop': '-50px'}),

                html.Div(children=[
                    html.Div(children=[
                        dcc.Graph(id='hbar-chart', figure=hbar_chart)
                    ], style={'padding-right': 0, 'marginTop': '110px', 'width': '50%', "position": "absolute", "left": "20px",
                              'display': 'flex', 'align-items': 'center', 'justifyContent': 'start'}),

                    html.Div(children=[
                        html.Div(children=[
                            html.Div(children=[
                                dcc.RangeSlider(
                                    id='year-slider',
                                    min=int(df['release_year'].min()),
                                    max=int(df['release_year'].max()),
                                    value=[int(df['release_year'].min()), int(df['release_year'].max())],
                                    marks={str(year): str(year) for year in
                                           range(int(df['release_year'].min()), int(df['release_year'].max()) + 1, 10)},
                                    step=1
                                )
                            ], style={'width': '500px'}),
                            html.P('Період випуску контенту',
                                   style={'color': 'white', 'font-style': 'normal', 'font-size': '18px'})
                        ], style={'display': 'flex', 'align-items': 'center',
                                  'justify-content': 'end', "position": "absolute", "zIndex": 2, "right": "10px", 'top': '30px'}),

                        dcc.Graph(id='histogram', style={'display': 'flex','align-items': 'center', 'justifyContent': 'start', "position": "absolute", "zIndex": 1, "left": "990px"})
                    ], style={'width': 700, 'height': 500})

                ], style={'display': 'flex', 'justifyContent': 'start', 'align-items': 'center', "position": "relative"}),

                html.Div(children=[
                    dcc.Graph(id='fig', figure=content_map)
                ], style={'display': 'flex', 'align-items': 'center',
                          'justify-content': 'center', 'marginTop': '-30px'})
            ], style={'display': 'flex', 'flexDirection': 'column'})
        ], style={'backgroundColor': 'black'}, className='hidden')
    ])

# Функція реалізації блоку виводу по другому сервісі
def create_statistics_layout_amazon(df, img):
    df_amazon = pd.read_csv('D:/GraduateWork/GradWork/data/amazon_prime_titles.csv')
    pie_chart = creation_type_content_graph(df_amazon, 'yellow', 'orange')

    bar_chart_figure = creation_age_graph(df, 'orange')

    hbar_chart = creation_genre_graph(df, 'orange')

    content_map = creation_map(df, 'Oranges')

    with open(img, 'rb') as img_file:
        image_string = base64.b64encode(img_file.read()).decode()

    # Отримайте топ-5 фільмів/серіалів за середнім рейтингом
    top_5_movies = df.nlargest(5, 'averageRating')[['title', 'type', 'averageRating', 'description']]

    return html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    html.Img(src='data:image/png;base64,' + image_string, style={'width': '900px', 'height': '250px'}),

                    dcc.Graph(id='pie-chart', figure={'data': [pie_chart], 'layout': {'width': 450, 'height': 450,
                                                                                      'paper_bgcolor': 'black',
                                                                                      'legend': {'font': {
                                                                                          'color': 'white'}}
                                                                                      }})
                ], style={'display': 'flex', 'justifyContent': 'space-around', 'align-items': 'center'}),

                html.Div(children=[
                    dcc.Graph(id='bar-chart', figure=bar_chart_figure),

                    html.Div(children=[
                        html.H2('Топ-5 фільмів/серіалів', style={'text-align': 'center'}),
                        html.Table([
                            *[html.Tr([
                                html.Tr([
                                    html.Td([
                                        html.Span(f"{movie['title']} ", style={'color': 'orange'}),
                                        # Змініть колір за потребою
                                        f"({movie['averageRating']}) {movie['type']}"
                                    ],
                                        style={'text-align': 'left', 'font-size': '20px'}),
                                ]),
                                html.Tr([
                                    html.Td(movie['description'], style={'text-align': 'left', 'font-size': '18px',
                                                                         'border-bottom': '1px solid orange'})
                                ])
                            ]) for _, movie in top_5_movies.iterrows()]
                        ])

                    ], style={'color': 'white'})
                ], style={'display': 'flex', 'justifyContent': 'space-around',
                          'align-items': 'center', 'marginTop': '-50px'}),

                html.Div(children=[
                    html.Div(children=[
                        dcc.Graph(id='hbar-chart', figure=hbar_chart)
                    ], style={'padding-right': 0, 'marginTop': '110px', 'width': '50%', "position": "absolute",
                              "left": "20px",
                              'display': 'flex', 'align-items': 'center', 'justifyContent': 'start'}),

                    html.Div(children=[
                        html.Div(children=[
                            html.Div(children=[
                                dcc.RangeSlider(
                                    id='year-slider',
                                    min=int(df['release_year'].min()),
                                    max=int(df['release_year'].max()),
                                    value=[int(df['release_year'].min()), int(df['release_year'].max())],
                                    marks={str(year): str(year) for year in
                                           range(int(df['release_year'].min()), int(df['release_year'].max()) + 1, 10)},
                                    step=1
                                )
                            ], style={'width': '500px'}),
                            html.P('Період випуску контенту',
                                   style={'color': 'white', 'font-style': 'normal', 'font-size': '18px'})
                        ], style={'display': 'flex', 'align-items': 'center',
                                  'justify-content': 'end', "position": "absolute", "zIndex": 2, "right": "10px",
                                  'top': '30px'}),

                        dcc.Graph(id='histogram',
                                  style={'display': 'flex', 'align-items': 'center', 'justifyContent': 'start',
                                         "position": "absolute", "zIndex": 1, "left": "990px"})
                    ], style={'width': 700, 'height': 500})

                ], style={'display': 'flex', 'justifyContent': 'start', 'align-items': 'center',
                          "position": "relative"}),

                html.Div(children=[
                    dcc.Graph(id='fig', figure=content_map)
                ], style={'display': 'flex', 'align-items': 'center',
                          'justify-content': 'center', 'marginTop': '-30px'})
            ], style={'display': 'flex', 'flexDirection': 'column'})
        ], style={'backgroundColor': 'black'}, className='hidden')
    ])

# Функція реалізації блоку виводу по третьому сервісі
def create_statistics_layout_disney(df, img):
    df_disney = pd.read_csv('D:/GraduateWork/GradWork/data/hotstar.csv')
    pie_chart = creation_type_content_graph(df_disney, 'blue', 'navy')

    bar_chart_figure = creation_age_graph(df, 'blue')

    hbar_chart = creation_genre_graph(df, 'blue')

    content_map = creation_map(df, 'Blues')

    with open(img, 'rb') as img_file:
        image_string = base64.b64encode(img_file.read()).decode()

    # Отримайте топ-5 фільмів/серіалів за середнім рейтингом
    top_5_movies = df.nlargest(5, 'averageRating')[['title', 'type', 'averageRating', 'description']]

    return html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    html.Img(src='data:image/png;base64,' + image_string, style={'width': '700px', 'height': '400px'}),

                    dcc.Graph(id='pie-chart', figure={'data': [pie_chart], 'layout': {'width': 450, 'height': 450,
                                                                                      'paper_bgcolor': 'black',
                                                                                      'legend': {'font': {
                                                                                          'color': 'white'}}
                                                                                      }})
                ], style={'display': 'flex', 'justifyContent': 'space-around', 'align-items': 'center'}),

                html.Div(children=[
                    dcc.Graph(id='bar-chart', figure=bar_chart_figure),

                    html.Div(children=[
                        html.H2('Топ-5 фільмів/серіалів', style={'text-align': 'center'}),
                        html.Table([
                            *[html.Tr([
                                html.Tr([
                                    html.Td([
                                        html.Span(f"{movie['title']} ", style={'color': 'blue'}),
                                        # Змініть колір за потребою
                                        f"({movie['averageRating']}) {movie['type']}"
                                    ],
                                        style={'text-align': 'left', 'font-size': '20px'}),
                                ]),
                                html.Tr([
                                    html.Td(movie['description'], style={'text-align': 'left', 'font-size': '18px',
                                                                         'border-bottom': '1px solid blue'})
                                ])
                            ]) for _, movie in top_5_movies.iterrows()]
                        ])

                    ], style={'color': 'white'})
                ], style={'display': 'flex', 'justifyContent': 'space-around',
                          'align-items': 'center', 'marginTop': '-30px'}),

                html.Div(children=[
                    html.Div(children=[
                        dcc.Graph(id='hbar-chart', figure=hbar_chart)
                    ], style={'padding-right': 0, 'marginTop': '110px', 'width': '50%', "position": "absolute",
                              "left": "20px",
                              'display': 'flex', 'align-items': 'center', 'justifyContent': 'start'}),

                    html.Div(children=[
                        html.Div(children=[
                            html.Div(children=[
                                dcc.RangeSlider(
                                    id='year-slider',
                                    min=int(df['release_year'].min()),
                                    max=int(df['release_year'].max()),
                                    value=[int(df['release_year'].min()), int(df['release_year'].max())],
                                    marks={str(year): str(year) for year in
                                           range(int(df['release_year'].min()), int(df['release_year'].max()) + 1, 10)},
                                    step=1
                                )
                            ], style={'width': '500px'}),
                            html.P('Період випуску контенту',
                                   style={'color': 'white', 'font-style': 'normal', 'font-size': '18px'})
                        ], style={'display': 'flex', 'align-items': 'center',
                                  'justify-content': 'end', "position": "absolute", "zIndex": 2, "right": "10px",
                                  'top': '30px'}),

                        dcc.Graph(id='histogram',
                                  style={'display': 'flex', 'align-items': 'center', 'justifyContent': 'start',
                                         "position": "absolute", "zIndex": 1, "left": "990px"})
                    ], style={'width': 700, 'height': 500})

                ], style={'display': 'flex', 'justifyContent': 'start', 'align-items': 'center',
                          "position": "relative"}),

                html.Div(children=[
                    dcc.Graph(id='fig', figure=content_map)
                ], style={'display': 'flex', 'align-items': 'center',
                          'justify-content': 'center', 'marginTop': '-30px'})
            ], style={'display': 'flex', 'flexDirection': 'column'})
        ], style={'backgroundColor': 'black'}, className='hidden')
    ])

# Функція реалізації блоку виводу по порівняльній характеристиці сервісів
def create_comparison_layout(df_netflix, df_amazon, df_disney):
    pie_charts = creation_count_content_servises(df_netflix, df_amazon, df_disney)

    histograms = creation_type_content_servises(df_netflix, df_amazon, df_disney)

    rating_platforms = creation_age_category_content_servises(df_netflix, df_amazon, df_disney)

    release_year_fig = creation_release_content_servises(df_netflix, df_amazon, df_disney)

    choropleth_map = creation_map_servises(df_netflix, df_amazon, df_disney)

    hist_genres = creation_genre_servises(df_netflix, df_amazon, df_disney)

    hist_ratings = creation_rating_servises(df_netflix, df_amazon, df_disney)

    return html.Div(children=[
        html.Div(children=[
            html.Div(dcc.Graph(figure=pie_charts), style={'backgroundColor': 'black', 'width': '50%'}),
            html.Div(dcc.Graph(figure=histograms), style={'backgroundColor': 'black', 'width': '50%'})
        ], style={'display': 'flex', 'justifyContent': 'space-around'}),

        html.Div(children=[
            html.Div(dcc.Graph(figure=rating_platforms), style={'width': '50%'}),
            html.Div(dcc.Graph(figure=release_year_fig), style={'width': '50%'})
        ], style={'display': 'flex', 'justifyContent': 'space-around'}),

        html.Div(children=[
            html.Div(dcc.Graph(figure=hist_ratings)),
            html.Div(dcc.Graph(figure=hist_genres))
        ], style={'display': 'flex', 'justifyContent': 'space-around'}),

        html.Div(children=[
            html.Div(dcc.Graph(figure=choropleth_map))
        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'})
    ], style={'backgroundColor': 'black'})

# Сallback для коректної роботи меню
@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'),
              Input('type-dropdown', 'value'),
              Input('range-slider', 'value'))
def render_content(tab, value, slider_value):
    min_value, max_value = slider_value

    df_netflix = pd.read_csv('D:/GraduateWork/GradWork/data/netflix_filtered.csv')
    df_amazon = pd.read_csv('D:/GraduateWork/GradWork/data/amazon_filtered.csv')
    df_disney = pd.read_csv('D:/GraduateWork/GradWork/data/disney_filtered.csv')

    # Фільтруйте датасети відповідно до заданого діапазону
    df_netflix_filtered = df_netflix[
        (df_netflix['averageRating'] >= min_value) & (df_netflix['averageRating'] <= max_value)]
    df_amazon_filtered = df_amazon[(df_amazon['averageRating'] >= min_value) & (df_amazon['averageRating'] <= max_value)]
    df_disney_filtered = df_disney[(df_disney['averageRating'] >= min_value) & (df_disney['averageRating'] <= max_value)]

    if tab == 'tab-1':
        if value == 'Загальний контент':
            return create_comparison_layout(df_netflix_filtered, df_amazon_filtered, df_disney_filtered)

        elif value == 'Фільми':
            netflix_film = df_netflix_filtered[df_netflix_filtered['type'] == 'Movie']
            amazon_film = df_amazon_filtered[df_amazon_filtered['type'] == 'Movie']
            disney_film = df_disney_filtered[df_disney_filtered['type'] == 'movie']
            return create_comparison_layout(netflix_film, amazon_film, disney_film)

        elif value == 'Серіали':
            netflix_show = df_netflix_filtered[df_netflix_filtered['type'] == 'TV Show']
            amazon_show = df_amazon_filtered[df_amazon_filtered['type'] == 'TV Show']
            disney_show = df_disney_filtered[df_disney_filtered['type'] == 'tv']
            return create_comparison_layout(netflix_show, amazon_show, disney_show)
    elif tab == 'tab-2':
        if value == 'Загальний контент':
            images = 'D:/GraduateWork/GradWork/assets/wordcloud_all_red.png'
            return create_statistics_layout_netflix(df_netflix_filtered, images)

        elif value == 'Фільми':
            netflix_film = df_netflix_filtered[df_netflix_filtered['type'] == 'Movie']
            images = 'D:/GraduateWork/GradWork/assets/wordcloud_film_red.png'
            return create_statistics_layout_netflix(netflix_film, images)

        elif value == 'Серіали':
            netflix_show = df_netflix_filtered[df_netflix_filtered['type'] == 'TV Show']
            images = 'D:/GraduateWork/GradWork/assets/wordcloud_serial_red.png'
            return create_statistics_layout_netflix(netflix_show, images)
    elif tab == 'tab-3':
        if value == 'Загальний контент':
            images = 'D:/GraduateWork/GradWork/assets/wordcloud_all_orange.png'
            return create_statistics_layout_amazon(df_amazon_filtered, images)

        elif value == 'Фільми':
            amazon_film = df_amazon_filtered[df_amazon_filtered['type'] == 'Movie']
            images = 'D:/GraduateWork/GradWork/assets/wordcloud_film_orange.png'
            return create_statistics_layout_amazon(amazon_film, images)

        elif value == 'Серіали':
            amazon_show = df_amazon_filtered[df_amazon_filtered['type'] == 'TV Show']
            images = 'D:/GraduateWork/GradWork/assets/wordcloud_serial_orange.png'
            return create_statistics_layout_amazon(amazon_show, images)
    elif tab == 'tab-4':
        if value == 'Загальний контент':
            images = 'D:/GraduateWork/GradWork/assets/wordcloud_all_blue.png'
            return create_statistics_layout_disney(df_disney_filtered, images)

        elif value == 'Фільми':
            disney_film = df_disney_filtered[df_disney_filtered['type'] == 'movie']
            images = 'D:/GraduateWork/GradWork/assets/wordcloud_film_blue.png'
            return create_statistics_layout_disney(disney_film, images)

        elif value == 'Серіали':
            disney_show = df_disney_filtered[df_disney_filtered['type'] == 'tv']
            images = 'D:/GraduateWork/GradWork/assets/wordcloud_serial_blue.png'
            return create_statistics_layout_disney(disney_show, images)

# Сallback для оновлення даних та вигляду гістограми
@app.callback(
    Output('histogram', 'figure'),
    Input('year-slider', 'value'),
    Input('tabs', 'value'))
def update_histogram(year_range, tab):
    if tab == 'tab-2':
        df = pd.read_csv('D:/GraduateWork/GradWork/data/netflix_titles.csv')
        marker_color = 'red'
    elif tab == 'tab-3':
        df = pd.read_csv('D:/GraduateWork/GradWork/data/amazon_prime_titles.csv')
        marker_color = 'orange'
    elif tab == 'tab-4':
        df = pd.read_csv('D:/GraduateWork/GradWork/data/hotstar.csv')
        marker_color = 'blue'

    mask = ((df['release_year']) >= year_range[0]) & (df['release_year'] <= year_range[1])
    filtered_df = df.loc[mask, 'release_year']
    fig = go.Figure(data=[go.Histogram(x=filtered_df, nbinsx=20, marker_color=marker_color)])
    fig.update_layout(title_text='Динаміка випуску', plot_bgcolor='black',
                      paper_bgcolor='black', font_color='white', width=900, height=520, title_y=0.83)
    return fig


# Запуску веб-сервера
if __name__ == '__main__':
    app.run_server(debug=False)
