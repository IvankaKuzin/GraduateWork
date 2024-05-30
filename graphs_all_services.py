import plotly.graph_objs as go
import pycountry
import pandas as pd
import plotly.express as px
from collections import defaultdict

def creation_count_content_servises(df_netflix, df_amazon, df_disney):
    netflix_size = len(df_netflix)
    amazon_size = len(df_amazon)
    disney_size = len(df_disney)

    sizes = [netflix_size, amazon_size, disney_size]

    labels = ['Netflix', 'Amazon', 'Disney+']

    colors = ['#CD5C5C', 'orange', '#87CEFA']

    pie_charts = go.Figure(data=[go.Pie(labels=labels, values=sizes, marker_colors=colors)])

    pie_charts.update_xaxes(showgrid=False, zeroline=False, showticklabels=False)
    pie_charts.update_yaxes(showgrid=False, zeroline=False, showticklabels=False)

    pie_charts.update_layout(
        title_text='Порівняння обсягів контенту на сервісах',
        title_font_color='white',
        paper_bgcolor='black',
        plot_bgcolor='black',
        legend=dict(
            font=dict(
                color='white'
            ),
            x=0.75,
            y=0.9
        )
    )

    return pie_charts

def creation_type_content_servises(df_netflix, df_amazon, df_disney):
    type_counts1 = df_netflix['type'].value_counts()
    type_counts2 = df_amazon['type'].value_counts()
    type_counts3 = df_disney['type'].value_counts()

    type_counts1 = type_counts1.rename({'Movie': 'Movie'}, errors='ignore')
    type_counts3 = type_counts3.rename({'movie': 'Movie'}, errors='ignore')

    type_counts1 = type_counts1.rename({'TV Show': 'TV Show'}, errors='ignore')
    type_counts3 = type_counts3.rename({'tv': 'TV Show'}, errors='ignore')

    labels = type_counts1.index.union(type_counts2.index).union(type_counts3.index)

    counts1 = [type_counts1[label] if label in type_counts1 else 0 for label in labels]
    counts2 = [type_counts2[label] if label in type_counts2 else 0 for label in labels]
    counts3 = [type_counts3[label] if label in type_counts3 else 0 for label in labels]

    histograms = go.Figure(data=[
        go.Bar(name='Netflix', x=labels, y=counts1, marker_color='#CD5C5C'),
        go.Bar(name='Amazon', x=labels, y=counts2, marker_color='orange'),
        go.Bar(name='Disney+', x=labels, y=counts3, marker_color='#87CEFA')
    ])

    histograms.update_layout(
        barmode='group',
        title='Категорії вмісту',
        yaxis=dict(
            title='Counts',
            title_font=dict(color='white'),
            tickfont=dict(color='white'),
        ),
        xaxis=dict(
            title='Type',
            title_font=dict(color='white'),
            tickfont=dict(color='white'),
        ),
        title_font_color='white',
        paper_bgcolor='black',
        plot_bgcolor='black',
        legend=dict(
            font=dict(
                color='white'
            )
        )
    )

    return histograms

def creation_age_category_content_servises(df_netflix, df_amazon, df_disney):
    def get_age_category(rating):
        if rating in ['G', 'TV-Y', 'TV-Y7', 'TV-Y7-FV', 'ALL', 'ALL_AGES', '7+', 'U', 'U/A 7+']:
            return 'Для всіх'
        elif rating in ['PG', 'TV-PG', 'TV-G', '13+', '16', '16+', 'AGES_16_', 'U/A 13+', 'U/A 16+', 'PG-13', 'TV-14']:
            return 'З батьками'
        elif rating in ['R', 'TV-MA', 'NC-17', '18+', 'AGES_18_', 'A']:
            return '18+'
        else:
            return 'Без рейтингу'

    rating_netflix = df_netflix['rating'].apply(get_age_category)
    rating_amazon = df_amazon['rating'].apply(get_age_category)
    rating_disney = df_disney['age_rating'].apply(get_age_category)

    ratings1 = rating_netflix.value_counts()
    ratings2 = rating_amazon.value_counts()
    ratings3 = rating_disney.value_counts()

    labels = set(ratings1.index).union(set(ratings2.index), set(ratings3.index))

    counts1 = [ratings1.get(label, 0) for label in labels]
    counts2 = [ratings2.get(label, 0) for label in labels]
    counts3 = [ratings3.get(label, 0) for label in labels]

    total1 = sum(counts1)
    total2 = sum(counts2)
    total3 = sum(counts3)

    percentages1 = [f'{(count / total1) * 100:.2f}%' for count in counts1]
    percentages2 = [f'{(count / total2) * 100:.2f}%' for count in counts2]
    percentages3 = [f'{(count / total3) * 100:.2f}%' for count in counts3]

    rating_platforms = go.Figure(data=[
        go.Bar(name='Netflix', x=list(labels), y=counts1, text=percentages1, textposition='outside',
               textfont=dict(color='white'), marker_color='#CD5C5C'),
        go.Bar(name='Amazon', x=list(labels), y=counts2, text=percentages2, textposition='outside',
               textfont=dict(color='white'), marker_color='orange'),
        go.Bar(name='Disney+', x=list(labels), y=counts3, text=percentages3, textposition='outside',
               textfont=dict(color='white'), marker_color='#87CEFA')
    ])

    rating_platforms.update_xaxes(tickfont=dict(color='white'))
    rating_platforms.update_yaxes(tickfont=dict(color='white'), showgrid=False,
                                  range=[0, max(counts1 + counts2 + counts3) * 1.2])


    rating_platforms.update_layout(
        barmode='group',
        title='Вікові обмеження',
        title_font_color='white',
        paper_bgcolor='black',
        plot_bgcolor='black',
        legend=dict(
            font=dict(
                color='white'
            )
        )
    )

    return rating_platforms

def creation_release_content_servises(df_netflix, df_amazon, df_disney):
    release_year_counts_netflix = df_netflix['release_year'].value_counts().sort_index()
    release_year_counts_prime = df_amazon['release_year'].value_counts().sort_index()
    release_year_counts_disney = df_disney['release_year'].value_counts().sort_index()

    release_year_fig = go.Figure()

    release_year_fig.add_trace(go.Scatter(
        x=release_year_counts_netflix.index,
        y=release_year_counts_netflix.values,
        fill='tozeroy',
        mode='lines',
        name='Netflix',
        line=dict(color='#CD5C5C', width=0.5),
        fillcolor='rgba(205, 92, 92, 0.9)',
    ))

    release_year_fig.add_trace(go.Scatter(
        x=release_year_counts_prime.index,
        y=release_year_counts_prime.values,
        fill='tozeroy',
        mode='lines',
        name='Amazon Prime',
        line=dict(color='orange', width=0.5),
        fillcolor='rgba(255, 165, 0, 0.9)',
    ))

    release_year_fig.add_trace(go.Scatter(
        x=release_year_counts_disney.index,
        y=release_year_counts_disney.values,
        fill='tozeroy',
        mode='lines',
        name='Disney+',
        line=dict(color='#87CEFA', width=0.5),
        fillcolor='rgba(135, 206, 250, 0.9)',
    ))

    release_year_fig.update_xaxes(tickfont=dict(color='white'))
    release_year_fig.update_yaxes(tickfont=dict(color='white'))

    release_year_fig.update_layout(
        title='Динаміка випуску контенту',
        xaxis_title='Рік випуску',
        yaxis_title='Кількість',
        title_font_color='white',
        paper_bgcolor='black',
        plot_bgcolor='black',
        legend=dict(font=dict(color='white')),
        xaxis=dict(color='white'),
        yaxis=dict(color='white'),
    )

    return release_year_fig
def compare_countries_by_dataset(df_netflix, df_amazon, df_disney):
    for df in [df_netflix, df_amazon, df_disney]:
        if 'country' not in df.columns:
            raise ValueError(f"Датасет {df.name} не містить колонки 'country'")

    df_netflix['country'] = df_netflix['country'].fillna('Unknown')
    df_amazon['country'] = df_amazon['country'].fillna('Unknown')
    df_disney['country'] = df_disney['country'].fillna('Unknown')

    df_netflix['country'] = df_netflix['country'].str.split(', ')
    df_netflix = df_netflix.explode('country')

    df_amazon['country'] = df_amazon['country'].str.split(', ')
    df_amazon = df_amazon.explode('country')

    df_disney['country'] = df_disney['country'].str.split(', ')
    df_disney = df_disney.explode('country')

    unique_countries = df_netflix['country'].unique()

    results = {}

    for country in unique_countries:
        netflix_count = df_netflix[df_netflix['country'] == country].shape[0]
        amazon_count = df_amazon[df_amazon['country'] == country].shape[0]
        disney_count = df_disney[df_disney['country'] == country].shape[0]

        results[country] = {
            'Netflix': netflix_count,
            'Amazon': amazon_count,
            'Disney': disney_count
        }

    return results
def get_max_platform_count(country_records):
    result = {}

    for country, platform_counts in country_records.items():
        max_platform = max(platform_counts, key=platform_counts.get)
        max_count = platform_counts[max_platform]
        result[country] = {max_platform: max_count}

    return result
def convert_to_alpha_3(country_name):
    try:
        return pycountry.countries.get(name=country_name).alpha_3
    except AttributeError:
        return None
def create_platform_choropleth(disck):
    data = [(country, list(platform.keys())[0], list(platform.values())[0])
            for country, platform in disck.items()]
    df = pd.DataFrame(data, columns=['country', 'platform', 'count'])
    df['country'] = df['country'].apply(convert_to_alpha_3)

    colors = {'Netflix': '#CD5C5C', 'Amazon': 'orange', 'Disney': '#87CEFA'}

    fig = px.choropleth(df,
                        locations="country",
                        color="platform",
                        hover_name="country",
                        hover_data=["platform", "count"],
                        color_discrete_map=colors,
                        projection="natural earth")

    fig.update_layout(title='Сервіс з найбільшою кількістю контенту',
                      geo=dict(showframe=False,
                               projection={'type': 'natural earth'}),
                      width=1000,
                      height=650,
                      margin=dict(l=0),
                      paper_bgcolor='black',
                      geo_bgcolor='white',
                      font=dict(color='white'))

    return fig

def creation_map_servises(df_netflix, df_amazon, df_disney):
    country_records = compare_countries_by_dataset(df_netflix, df_amazon, df_disney)

    filtered_records = get_max_platform_count(country_records)

    choropleth_map = create_platform_choropleth(filtered_records)

    return choropleth_map

def creation_genre_servises(df_netflix, df_amazon, df_disney):
    # Розділення жанрів і розширення їх на окремі рядки
    df_netflix['listed_in'] = df_netflix['listed_in'].str.split(', ')
    df_netflix = df_netflix.explode('listed_in')

    df_amazon['listed_in'] = df_amazon['listed_in'].str.split(', ')
    df_amazon = df_amazon.explode('listed_in')

    df_disney['genre'] = df_disney['genre'].str.split(', ')
    df_disney = df_disney.explode('genre')

    genre_dict = {
        'International TV Shows': 'International',
        'TV Dramas': 'Drama',
        'TV Sci-Fi & Fantasy': 'Science Fiction',
        'Drama': 'Drama',
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
        'Comedy': 'Comedy',
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
        'Fantasy': 'Fantasy',
        'Special Interest': 'Documentaries',
        'Science Fiction': 'Science Fiction',
        'Sports': 'Sports',
        'Talk Show and Variety': 'Talk Show and Variety',
        'Anime': 'Anime',
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
        'Romance': 'Romance',
        'Unscripted': 'Reality',
        'Young Adult Audience': 'Teen',
        'Arthouse': 'Arthouse',
        'Historical': 'Historical',
        'Superhero': 'Superhero',
        'Mystery': 'Mystery',
        'Biopic': 'Biopic',
        'Standup Comedy': 'Comedy',
        'Crime': 'Crime',
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

    # Заміна жанрів у датасетах
    df_netflix['listed_in'] = df_netflix['listed_in'].replace(genre_dict)
    df_amazon['listed_in'] = df_amazon['listed_in'].replace(genre_dict)
    df_disney['genre'] = df_disney['genre'].replace(genre_dict)

    # Підрахунок жанрів для кожного датасету
    netflix_genres = df_netflix['listed_in'].value_counts()
    amazon_genres = df_amazon['listed_in'].value_counts()
    disney_genres = df_disney['genre'].value_counts()

    # Знаходження спільних жанрів
    common_genres = netflix_genres.index.intersection(amazon_genres.index).intersection(disney_genres.index)

    # Вибір 10 найпопулярніших спільних жанрів
    top_10_common_genres = common_genres[:10]

    # Створення графіка
    hist_genres = go.Figure()

    hist_genres.add_trace(go.Bar(
        x=top_10_common_genres,
        y=[netflix_genres[genre] for genre in top_10_common_genres],
        name='Netflix',
        marker_color='#CD5C5C'
    ))
    hist_genres.add_trace(go.Bar(
        x=top_10_common_genres,
        y=[amazon_genres[genre] for genre in top_10_common_genres],
        name='Amazon',
        marker_color='orange'
    ))
    hist_genres.add_trace(go.Bar(
        x=top_10_common_genres,
        y=[disney_genres[genre] for genre in top_10_common_genres],
        name='Disney',
        marker_color='#87CEFA'
    ))

    hist_genres.update_layout(
        title='Огляд найпопулярніших жанрів',
        width=900,
        height=600,
        xaxis_title="Жанри",
        yaxis_title="Кількість",
        barmode='group',
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white')
    )

    return hist_genres

def creation_rating_servises(df_netflix, df_amazon, df_disney):
    ratings1 = df_netflix['averageRating']
    ratings2 = df_amazon['averageRating']
    ratings3 = df_disney['averageRating']

    data_ratings = defaultdict(lambda: [0, 0, 0])

    # Заповніть словник даними про рейтинги
    for rating in ratings1:
        data_ratings[rating][0] += 1
    for rating in ratings2:
        data_ratings[rating][1] += 1
    for rating in ratings3:
        data_ratings[rating][2] += 1

    traces = []
    platforms = ['Netflix', 'Amazon', 'Disney']
    colors = ['#CD5C5C', 'orange', '#87CEFA']

    for i in range(len(platforms)):
        traces.append(go.Bar(
            x=list(data_ratings.keys()),
            y=[data[i] for data in data_ratings.values()],
            name=platforms[i],
            marker_color=colors[i]
        ))

    # Конфігурація макета
    layout = go.Layout(
        barmode='stack',
        title='Рейтинг контенту',
        width=900,
        height=550,
        xaxis=dict(title='Рейтинг', color='white'),
        yaxis=dict(title='Кількість', color='white'),
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white')
    )

    # Створіть фігуру та додайте сліди
    hist_ratings = go.Figure(data=traces, layout=layout)

    return hist_ratings