import streamlit as st
st.set_page_config(layout="wide", page_icon="🥇")
import pandas as pd
from pandas import DataFrame
import inflect
import plotly.express as px
from utils.country_medal_counts import total_medal_counts, medal_rank, best_event, medals_over_time
from utils.data import load_data, filter_data
p = inflect.engine()

def main():
    st.title("🥇 History of the Olympics", anchor=False)

    tab1, tab2, tab3 = st.tabs(
        ["🏅 Medals", "🧾 Events", "‍🏃‍♂️ Athletes"]
    )

    with tab1:
        st.subheader('Overall Medal Counts')
        df = load_data('data/athlete_events.csv')

        col1, col2 = st.columns([2, 8])

        with col1:
            # Filter options
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            selected_season = st.selectbox('Season:', ['All', 'Summer', 'Winter'])
            if selected_season in ['Summer', 'Winter']:
                available_years = df[df['Season'] == selected_season]['Year'].unique()
            else:
                available_years = df['Year'].unique()
            selected_year = st.selectbox('Year:', ['All'] + sorted(available_years.tolist(), reverse=True))
            selected_medal = st.selectbox('Medal Type:', ['All', 'Gold', 'Silver', 'Bronze'])
            num_countries = st.slider('Number of Countries:', min_value=1, max_value=40, value=10)

        with col2:
            # Filter the DataFrame based on selected options
            filtered_df = filter_data(df,
                                    selected_year if selected_year != 'All' else None,
                                    selected_season if selected_season != 'All' else None,
                                    selected_medal if selected_medal != 'All' else None)

            # Group by Team and Medal and count occurrences
            grouped_df = filtered_df.groupby(['Team', 'Medal']).size().reset_index(name='Count')

            # Calculate total number of medals for each team
            total_medals = grouped_df.groupby('Team')['Count'].sum().reset_index()

            # Sort teams by total number of medals in descending order and take top N teams
            top_teams = total_medals.sort_values(by='Count', ascending=False).head(num_countries)['Team']

            # Filter grouped DataFrame to include only top N teams
            grouped_df = grouped_df[grouped_df['Team'].isin(top_teams)]

            # Create a new column to represent the desired order of Medal types
            grouped_df['Medal_Order'] = grouped_df['Medal'].map({'Gold': 1, 'Silver': 2, 'Bronze': 3})

            # Sort the DataFrame based on the Medal_Order column
            grouped_df_sorted = grouped_df.sort_values(by=['Team', 'Medal_Order'])

            # Map medal types to colors
            medal_colors = {'Gold': 'gold', 'Silver': 'silver', 'Bronze': 'peru'}

            # Create stacked bar chart using Plotly
            fig = px.bar(grouped_df_sorted, x='Team', y='Count', color='Medal',
                        title='Total Medals by Country',
                        labels={'Count': 'Total Medals', 'Team': 'Team'},
                        barmode='stack',
                        category_orders={'Team': top_teams},
                        color_discrete_map=medal_colors)

            # Add annotations for total medal count on top of each bar
            for team in top_teams:
                total_medal_count = total_medals[total_medals['Team'] == team]['Count'].values[0]
                fig.add_annotation(x=team, y=total_medal_count, text=str(total_medal_count),
                                font=dict(size=12, color='black', weight='bold'), showarrow=False,
                                yshift=10)

            # Update layout
            fig.update_layout(title={'x': 0.3},
                          xaxis_title='Team', yaxis_title='Total Medals',
                          xaxis=dict(tickfont=dict(color='black'), showgrid=False, title=dict(font=dict(color='black'))),
                          yaxis=dict(tickfont=dict(color='black'), showgrid=False, title=dict(font=dict(color='black'))),
                          font=dict(color='black'))

            # Display the bar chart
            st.plotly_chart(fig, use_container_width=True)

        st.subheader('Country Medal Counts')

        col3, line_graph = st.columns([4, 6])

        with col3:
            available_countries = df['Team'].unique()
            selected_team = st.selectbox('Country:', sorted(available_countries.tolist()), index=1095)
            start_year, end_year = st.slider('Time Period:', min_value=min(df['Year']), max_value=max(df['Year']), value=(1896, 2016))
            total_medals = total_medal_counts(selected_team, start_year, end_year)
            medal_rank_num = medal_rank(selected_team, start_year, end_year)
            best_event_str = best_event(selected_team, start_year, end_year)
            col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
            col1.metric("Total Medals", total_medals)
            col2.metric("Medal Rank", p.ordinal(int(medal_rank_num)))
            sport1, sport2, sport3 = [(index,row) for index, row in best_event_str.iterrows()]
            for col, sport, medal in zip( (col3, col4, col5), (sport1, sport2, sport3), ('🥇', '🥈', '🥉')):
                col.metric(f"{medal} {sport[1]['Sport']}", sport[1]['Total Medals'])

        with line_graph:
            pass

    
    with tab2:
     st.subheader("Event Success by Country")
     st.info("Which countries dominate which events", icon="ℹ️")

    with tab3:
     st.subheader("Most Dominant Athletes")
     st.info("Individual athlete success over the years", icon="ℹ️")

if __name__ == '__main__':
    main()