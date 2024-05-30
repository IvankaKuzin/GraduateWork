import plotly.graph_objs as go
import geopandas as gpd
import plotly.express as px

def creation_type_content_graph(data, color1, color2):
    type_counts = data['type'].value_counts()

    labels = type_counts.index
    values = type_counts.values

    pie_chart = go.Pie(labels=labels, values=values, hole=.3, marker_colors=[color1, color2])

    return pie_chart

def creation_age_graph(df, color):
    def get_age_category(rating):
        if rating in ['G', 'TV-Y', 'TV-Y7', 'TV-Y7-FV', 'ALL', '7+', 'ALL_AGES', 'U']:
            return 'Для всіх'
        elif rating == 'U/A 7+':
            return 'Від 7 років'
        elif rating == 'U/A 13+':
            return 'Від 13 років'
        elif rating == 'U/A 16+':
            return 'Від 16 років'
        elif rating in ['PG', 'TV-PG', '13+', 'PG-13']:
            return 'З батьками'
        elif rating in ['PG-13', 'TV-14', 'TV-G', '16+', 'AGES_16_', '16']:
            return 'Обмеження за віком'
        elif rating in ['R', 'TV-MA', 'NC-17', '18+', 'AGES_18_', 'A']:
            return '18+'
        else:
            return 'Не визначено'

    if color == 'blue':
        data = df['age_rating'].apply(get_age_category)
    else:
        data = df['rating'].apply(get_age_category)

    age_category_counts = data.value_counts()

    bar_chart = go.Bar(x=age_category_counts.index, y=age_category_counts.values, marker_color=color)

    bar_chart_figure = go.Figure(
        data=[bar_chart],
        layout={
            'autosize': False,
            'height': 500,
            'width': 700,
            'margin': {'l': 150},
            'plot_bgcolor': 'black',
            'paper_bgcolor': 'black',
            'font_color': 'white',
            'title': {'text': 'Вікові обмеження'}
        }
    )

    return bar_chart_figure

def creation_genre_graph(df, color):
    genre_dict = {
        'International TV Shows': 'International',
        'TV Dramas': 'Drama',
        'TV Sci-Fi & Fantasy': 'Science Fiction',
        'Dramas': 'Drama',
        'International Movies': 'International',
        'Horror Movies': 'Horror Movies',
        'Action & Adventure': 'Action & Adventure',
        'Independent Movies': 'Arthouse',
        'Sci-Fi & Fantasy': 'Science Fiction',
        'TV Mysteries': 'Mystery',
        'Thrillers': 'Thriller',
        'Crime TV Shows': 'Crime',
        'Docuseries': 'Documentaries',
        'Documentaries': 'Documentaries',
        'Sports Movies': 'Sports',
        'Comedies': 'Comedy',
        'Anime Series': 'Anime',
        'Reality TV': 'Reality',
        'TV Comedies': 'Comedy',
        'Romantic Movies': 'Romance',
        'Romantic TV Shows': 'Romance',
        'Science & Nature TV': 'Science',
        'Movies': 'Movies',
        'British TV Shows': 'International',
        'Korean TV Shows': 'International',
        'Music & Musicals': 'Music Videos and Concerts',
        'LGBTQ Movies': 'LGBTQ',
        'Faith & Spirituality': 'Faith and Spirituality',
        'Kids': 'Children & Family Movies',
        'TV Action & Adventure': 'Action & Adventure',
        'Spanish-Language TV Shows': 'International',
        'Children & Family Movies': 'Children & Family Movies',
        'TV Shows': 'TV Shows',
        'Classic Movies': 'Classic & Cult TV',
        'Cult Movies': 'Classic & Cult TV',
        'TV Horror': 'Horror Movies',
        'Stand-Up Comedy & Talk Shows': 'Talk Show and Variety',
        'Teen TV Shows': 'Teen',
        'Stand-Up Comedy': 'Comedy',
        'Anime Features': 'Anime',
        'TV Thrillers': 'Thriller',
        'Classic & Cult TV': 'Classic & Cult TV',
        'Suspense': 'Thriller',
        'Fantasys': 'Fantasy',
        'Special Interest': 'Documentaries',
        'Science Fiction': 'Science Fiction',
        'Talk Show and Variety': 'Talk Show and Variety',
        'Animes': 'Anime',
        'Arts': 'Arthouse',
        'Entertainment': 'Entertainment',
        'and Culture': 'Culture',
        'Animation': 'Animation',
        'Music Videos and Concerts': 'Music Videos and Concerts',
        'Fitness': 'Fitness',
        'Faith and Spirituality': 'Faith and Spirituality',
        'Military and War': 'Military and War',
        'Western': 'Western',
        'LGBTQ': 'LGBTQ',
        'Romances': 'Romance',
        'Unscripted': 'Reality',
        'Young Adult Audience': 'Teen',
        'Arthouses': 'Arthouse',
        'Historicals': 'Historical',
        'Superheros': 'Superhero',
        'Mysterys': 'Mystery',
        'Biopics': 'Biopic',
        'Standup Comedy': 'Comedy',
        'Crimes': 'Crime',
        'Animals & Nature': 'Animals & Nature',
        'Musical': 'Musical',
        'Sport': 'Sports',
        'Science': 'Science',
        'Food': 'Food',
        'Concert Film': 'Music Videos and Concerts',
        'Mythology': 'Mythology',
        'Travel': 'Travel',
        'Shorts': 'Shorts',
        'Fantasy': 'Fantasy',
        'Teen': 'Teen',
        'Docudrama': 'Docudrama',
        'Talk Show': 'Talk Show and Variety',
        'Reality': 'Reality',
        'Awards': 'Awards',
        'Lifestyle': 'Lifestyle',
        'Formula E': 'Sports',
        'Football': 'Sports',
        'Kabaddi': 'Sports'
    }

    if color == 'blue':
        df['genre'] = df['genre'].str.split(', ')
        df = df.explode('genre')
        genres = df['genre']
    else:
        df['listed_in'] = df['listed_in'].str.split(', ')
        df = df.explode('listed_in')
        genres = df['listed_in']

    genres = genres.replace(genre_dict).value_counts().head(10)


    data = [go.Bar(x=genres.values, y=genres.index, orientation='h', marker_color=color)]

    layout = {
        'autosize': False,
        'height': 440,
        'width': 950,
        'margin': {'l': 30, 't': 50},
        'plot_bgcolor': 'black',
        'paper_bgcolor': 'black',
        'font_color': 'white',
        'title': {'text': 'Огляд за жанрами'},
        'title_y': 1
    }

    hbar_chart = go.Figure(data=data, layout=layout)

    return hbar_chart

def creation_map(df,color):
    countries = df['country'].apply(
        lambda x: ', '.join(map(str, x)) if isinstance(x, list) else str(x)).value_counts()

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    world.set_index('name', inplace=True)
    world['movies_tv_shows'] = countries

    fig = px.choropleth(world,
                        geojson=world.geometry,
                        locations=world.index,
                        color='movies_tv_shows',
                        color_continuous_scale=color,
                        title='Огляд контенту за країнами')

    fig.update_layout(
        autosize=False,
        width=1000,
        height=650,
        margin=dict(l=0),
        paper_bgcolor='black',
        plot_bgcolor='black',
        font_color='white',
        title_y=0.85,
        coloraxis=dict(colorbar_len=0.9)
    )

    return fig
