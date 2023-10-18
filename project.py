# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 08:51:01 2023

@author: raghavi

Layout of the web app:
    1. Homepage - App Title and Description (a. Intro to dataset: Explain what the dataset is 
    about and its significance. Highlight key features like the area for which this dataset is,
    time period covered and types of data recorded. 
    b. Data Summary: statistics of the dataset, such as the total number of records, 
    unique categories of stops, top offenses, and demographic distribution.
    c. Sample Data Exploration: Explore a small sample of the dataset interactively. Include 
    filters for attributes like date, time, race, gender allowing users to see how the filters
    affect the displayed data. Show a few sample rows from the dataset to give users an idea 
    of the data's structure.
    d. Educational Resources: 
    Stanford Open Policing Project (https://openpolicing.stanford.edu/))
    2. Demographic Analysis: a. Age Wise b. Race Wise c. Gender Wise
    Date Range Selector: Allow users to filter data within a specific date range.
    3. Other Analysis: Searches per 100 stops year wise, Drug Usage, Violation vs stop outcome
    Violation vs search type, violation vs drug usage, violation vs year, age vs drug, 
    gender vs drug, race vs drug.
    4. Predictions: Which profiles are more likely to commit crime.
"""

import streamlit as st
st.set_option('deprecation.showPyplotGlobalUse', False)
from streamlit_option_menu import option_menu
import datetime
import pandas as pd
import seaborn as sns
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

df = pd.read_csv("police_project.csv")
df['stop_date'] = pd.to_datetime(df['stop_date'], format='%Y-%m-%d')
df["stop_time"] = pd.to_datetime(df.stop_time, format="%H:%M").dt.hour
df.drop('county_name', axis=1, inplace=True)
df['search_type'].replace([np.nan], 'Search not Conducted', inplace=True)
df.dropna(inplace=True)
df["year"] = df.stop_date.dt.year
df = df.assign(bins = pd.cut(df["driver_age"], [0,5,18,64,100], 
                        labels=['0 to 5', '6 to 18', '19 to 64', '65 to 100']))
df.rename(columns={'bins':'driver_age_group'}, inplace=True)
a=[i.split(',')[0] for i in df.search_type]
df['search_type_agg']=a
race_pop={'driver_race':['White', 'Black', 'Asian', 'Hispanic', 'Other'],
    'race_population':[863105, 95783, 38945, 178936, 124202]}
df_race_pop = pd.DataFrame(race_pop)
df=df.merge(df_race_pop, on='driver_race', how='left')

age_pop={'driver_age_group':['6 to 18', '19 to 64', '65 to 100'],
    'age_population':[195777, 607331, 198935]}
df_age_pop = pd.DataFrame(age_pop)
df=df.merge(df_age_pop, on='driver_age_group', how='left')

gender_pop={'driver_gender':['M', 'F'],
    'gender_population':[516810, 535757]}

df_gender_pop = pd.DataFrame(gender_pop)
df=df.merge(df_gender_pop, on='driver_gender', how='left')

st.title("Police Stops Explorer") # App Title
with st.sidebar:
    selected = option_menu("Menu", ["Homepage","Exploratory Analysis","Demographic Analysis","Summary"],
                           icons=['house-fill', 'search', 'people-fill', 'newspaper'], menu_icon="cast",
                          default_index=0,
                          orientation="vertical")

if selected == "Homepage":
    # App Description
    selected_home = option_menu(None, ["About the dataset",
    "Summary Statistics", "Sample Data Explorer", "Educational Resources"],
    icons=['house', 'gear', 'globe', 'book'], menu_icon="cast", 
    default_index=0, orientation="horizontal")
    
    if selected_home == "About the dataset":
        st.subheader("Motivation behind the web app")
        st.markdown('<div style="text-align: justify;"> Every day, law enforcement in the U.S. conducts over 50,000 traffic stops. According to the Time Magazine, while many of these stops are conducted to ensure road safety, a significant portion is initiated for reasons unrelated to drivers behavior on the road. </div>', unsafe_allow_html=True)
        st.markdown('#####')
        st.subheader("Significance of the web app")
        st.markdown('<div style="text-align: justify;"> By visualizing and summarizing policing data, the app raises awareness about law enforcement activities, including patterns in stops, demographics, and potential biases. This awareness can lead to informed discussions and actions for positive change. </div>', unsafe_allow_html=True)
        st.markdown('#####')
        st.markdown('<div style="text-align: justify;"> Utilizing data-driven insights, the web app can aid in identifying potential patterns and trends related to criminal activities. By understanding these patterns, law enforcement agencies and communities can work together to implement proactive strategies and interventions aimed at preventing crimes. This approach focuses on community-wide safety initiatives promoting a safer environment for everyone </div>', unsafe_allow_html=True)
        st.markdown('######')
        st.subheader("Brief description of the dataset")
        st.markdown('<div style="text-align: justify;"> This web app displays information and insights about the traffic stops in the state of Rhode Island. The dataset encapsulates a decade worth of information, covering the period from January 2005 to December 2015. The data recorded in this project includes, </div>', unsafe_allow_html=True)
        st.markdown("- Date and Time: Information about the date and time when the police stop occurred.")
        st.markdown("- Driver Demographics: Information about the driver, such as race, gender, age, and ethnicity.")
        st.markdown("- Reason for Stop: The primary reason for the police stop, such as speeding, traffic violation, suspicious behavior, etc.")
        st.markdown("- Stop Outcome: The outcome of the stop, including whether a citation was issued, a warning given, or an arrest made.")
        st.markdown("- Search Details: If a vehicle or individual was searched, the reasons for the search and whether any contraband or illegal items were found.")
        
        st.markdown('''<style>[data-testid="stMarkdownContainer"] ul{list-style-position: inside;}</style>''', unsafe_allow_html=True)
    
    elif selected_home == "Summary Statistics":
        st.write("**Explore the Summary Statistics page, your gateway to key insights about the dataset. Here, you'll find a concise overview that provides some context about the data at your fingertips.**")
        
        st.subheader("What You'll Discover:")
        
        st.markdown("1. **Total Number of Records:** Get an understanding of the dataset's scale. Learn how many records are available, giving you an idea of the dataset's scope and depth.")
        st.markdown("- The dataset comprises 91,741 recorded stops. However, this analysis is based on 86,113 usable rows due to the presence of missing values in certain fields.")
        st.markdown("2. **Common Values for some columns like:**")
        st.markdown("- **Unique Categories of Stops:** The reason behind the stops include *Speeding*, *Moving Violation*, *Equipment*, *Registration*, and *Seat Belt*")
        st.markdown("- **Demographic Information:** *Race* includes values such as White, Black, Hispanic, Asian, and other. While, *gender* which includes values such as Male and Female. Also, *age* ranging from 15 to 99.")
        st.markdown("3. **Column Overview:** **Reason for Stops:**")
        st.markdown("- *Speeding - 56%*")
        st.markdown("- *Moving Violation - 18.7%*")
        st.markdown("- *Equipment - 12.7%*")
        st.markdown("- *Registration/Plates - 3.9%*")
        st.markdown("- *Seat belt - 3.4%*")
        st.markdown("- *Other - 4.9%*")
        st.markdown('''<style>[data-testid="stMarkdownContainer"] ul{list-style-position: inside;}</style>''', unsafe_allow_html=True)
        st.markdown("4. **Column Overview:** **Outcome of Stops:**")
        st.markdown("- *Citation - 89%*")
        st.markdown("- *Warning - 6%*")
        st.markdown("- *Arrest Driver - 2.9%*")
        st.markdown("- *Other - 3%*")
        st.markdown('''<style>[data-testid="stMarkdownContainer"] ul{list-style-position: inside;}</style>''', unsafe_allow_html=True)
        
    elif selected_home == "Sample Data Explorer":
        st.write("**Welcome to the Data Explorer section, where you have the power to navigate the dataset according to your preferences.**")
        st.write("**Export the selected data:** Need to analyze the data offline or share your findings? Export your customized results in CSV format, for further analysis or presentation!")
        selected_de = st.multiselect('Select columns to see the data present in it', df.columns,
                                     ['stop_date', 'driver_gender', 'driver_age', 'driver_race', 'violation'])

        choose_year = st.slider('Choose a year to see the data', min_value=2005, max_value=2015, value=2010)

        st.dataframe(df[selected_de][df.year==choose_year].head(10))        
        
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')

        csv = convert_df(df[selected_de][df.year==choose_year])
        customized_button = st.markdown("""
                                <style>
                                .stDownloadButton, div.stButton {text-align:right}
                                .stDownloadButton button, div.stButton > button:first-child {
                                background-color: #000000;
                                color:#FFFFFF;
                                padding-left: 20px;
                                padding-right: 20px;
                                }
    
                            .stDownloadButton button:hover, div.stButton > button:hover {
                            background-color: #ADD8E6;
                            color:#000000;
                            }
                        </style>""", unsafe_allow_html=True)
                        
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='open_policing_dataset_rhode_island.csv',
            mime='text/csv',
            )
    
    elif selected_home == "Educational Resources":
        st.write("For additional insights into this dataset, click the link below,")
        url1 = "https://openpolicing.stanford.edu/data/"
        st.write("[Stanford Open Policing Project](%s)" % url1)
        
        st.subheader("Articles and Research Papers")
        st.write("Comprehensive research papers discussing racial disparities in policing practices.")
        url2 = "https://5harad.com/papers/policing-the-police.pdf"
        st.write("[Combatting Police Discrimination in the age of Big Data](%s)" % url2)
        url3 = "https://5harad.com/papers/simple-rules.pdf"
        st.write("[Simple Rules to guide expert classifications](%s)" % url3)
        
        st.subheader("Community Safety Programs")
        st.write("Information about neighborhood watch programs and how communities can work together for safety.")
        url4 = "https://bja.ojp.gov/sites/g/files/xyckuh186/files/Publications/NSA_NW_Manual.pdf"
        st.write("[Neighborhood Watch Program](%s)" % url4)
        
        st.subheader("Educational Videos")
        st.write("An educational video explaining legal rights during police stops and interactions.")
        url5 = "https://www.youtube.com/watch?v=f26QJKREYB8&t=8s"
        st.write("[Know your rights!](%s)" % url5)
        
        st.subheader("References")
        st.write("Data used for this analysis is obtained from the below references:")
        st.write("https://openpolicing.stanford.edu/publications/")
        st.write("https://github.com/stanford-policylab/opp")
        st.write("https://www.kaggle.com/datasets/yassershrief/dataset-of-traffic-stops-in-rhode-island")
        
elif selected == "Exploratory Analysis":
    selected_exp = option_menu(None, ["Violation vs Other Attributes", "Drug Usage Trends", "Time Series Trends"], 
    default_index=0, orientation="horizontal")
    
    if selected_exp == "Violation vs Other Attributes":
        viol_so = df.groupby(['violation', 'stop_outcome'])['stop_date'].count().reset_index()
        st.subheader("Stop outcomes for each violation")
        fig = px.histogram(viol_so, x="violation", y="stop_date", color="stop_outcome", barnorm='percent')
        fig.update_layout(yaxis_title='Stop outcome percentage')
        st.plotly_chart(fig)
        
        st.subheader("Search Type for each violation")
        df_omit = df[df.search_type != "Search not Conducted"]
        viol_st = df_omit.groupby(['violation', 'search_type_agg'])['stop_date'].count().reset_index()
        fig2 = px.histogram(viol_st, x="violation", y="stop_date", color="search_type_agg", barnorm='percent')
        fig2.update_layout(yaxis_title='Search type percentage')
        st.plotly_chart(fig2)
        
        st.subheader("Violation vs Search Conducted")
        temp=df[df.search_conducted==True].groupby(['year','violation']).count()['search_conducted'].reset_index(1)
        temp.head()
        fig3 = px.pie(temp, values='search_conducted', names='violation')
        st.plotly_chart(fig3)
        
        st.subheader("Violation vs Arrests")
        temp=df[df.is_arrested==True].groupby(['year','violation']).count()['is_arrested'].reset_index(1)
        temp.head()
        fig4 = px.pie(temp, values='is_arrested', names='violation')
        st.plotly_chart(fig4)
        
    elif selected_exp == "Drug Usage Trends":
        st.subheader("Explore Daily Trends in Drug-Related Stops")
        st.write("Comprehensive view of how these stops vary over different hours. Dive into the data to gain a nuanced understanding of how the number of drug-related stops vary during various times of the day.")
        df.loc[df.sort_values(by="stop_time").drugs_related_stop, 'stop_time'].value_counts().sort_index().plot(figsize=(12, 6))
        plt.xlabel("Hour of the Day")
        plt.ylabel("Number of Drug Related Stops")
        st.pyplot()
        
        st.subheader("Examine Age-specific Trends in Drug-Related Stops")
        st.write("Below is the graph to understand the trends in drug-related stops categorized by age groups. Delve into the specifics to gain insights into how these stops differ among various age groups, providing valuable context for understanding law enforcement practices concerning drug-related incidents.")
        temp=df.loc[df.sort_values(by="driver_age_group").drugs_related_stop, 'driver_age_group'].value_counts().sort_index().reset_index()
        temp.columns=['driver_age_group','count']
        norm=pd.DataFrame(temp[['count','driver_age_group']].set_index('driver_age_group')['count']/df.groupby('driver_age_group').max()['age_population'],columns=['normalized_count'])
        temp=temp.merge(norm,on='driver_age_group',how='left')
        #st.dataframe(temp)
        fig=px.pie(temp, values='normalized_count', names='driver_age_group')
        st.plotly_chart(fig)
        st.write("**Note:** The figures depicted in this graph have been standardized according to the census data representing the different age groups in Rhode Island.")
        
        st.subheader("Duration of Stops in Drug-Related Incidents")
        st.write("Explore the stop duration patterns in incidents related to drugs. Investigate the duration disparities to gain a comprehensive understanding of the time spent during these specific interactions between law enforcement and individuals involved in drug-related incidents.")
        df.loc[df.sort_values(by="stop_time").drugs_related_stop, 'stop_time'].value_counts().sort_index().plot(figsize=(12, 6))
        plt.xlabel("Hour of the Day")
        plt.ylabel("Stop duration")
        st.pyplot()
        
        st.subheader("Analyze Drug-Related Stops Across Racial Groups")
        st.write("Dive into the visualization to understand how these stops vary between different races, offering valuable perspectives on the intersection of law enforcement practices and racial backgrounds in drug-related incidents.")
        temp=df.loc[df.sort_values(by="driver_race").drugs_related_stop, 'driver_race'].value_counts().sort_index().reset_index()
        temp.columns=['driver_race','count']
        norm=pd.DataFrame(temp[['count','driver_race']].set_index('driver_race')['count']/df.groupby('driver_race').max()['race_population'],columns=['normalized_count'])
        temp=temp.merge(norm,on='driver_race',how='left')
        #st.dataframe(temp)
        sns.barplot(data=temp,x='driver_race',y='normalized_count')
        plt.ylabel('Stop rates')
        st.pyplot()
        st.write("**Note:** The figures depicted in this graph have been standardized according to the census data representing the different racial groups in Rhode Island.")
        
    elif selected_exp=='Time Series Trends':
        st.markdown('<div style="text-align: justify;"> Delve into time series trends related to the selected violation type, stop outcome, and search category within your specified start and end dates. Gain valuable insights into how these factors have evolved over time, helping you understand the dynamic patterns for each selection.  </div>', unsafe_allow_html=True)
        st.markdown("#####")
        
        d1 = st.date_input("Specify your chosen start date:", datetime.date(2006, 7, 6))
        d2 = st.date_input("Specify your chosen end date:", datetime.date(2009, 7, 6))
        violation=st.selectbox('Select a type of violation:',df.violation.unique())
        temp=df[(df.violation==violation)]
        temp["stop_date"] = pd.to_datetime(temp["stop_date"]).dt.date
        temp=temp[(temp.stop_date>=d1) & (temp.stop_date<=d2)]
        temp=temp.groupby('stop_date').count()['violation']
        fig4=px.line(temp)
        fig4.update_layout(yaxis_title='Frequency')
        st.plotly_chart(fig4)
        
        stop_out=st.selectbox('Select a type of Stop Outcome:',df.stop_outcome.unique())
        temp=df[(df.stop_outcome==stop_out)]
        temp["stop_date"] = pd.to_datetime(temp["stop_date"]).dt.date
        temp=temp[(temp.stop_date>=d1) & (temp.stop_date<=d2)]
        temp=temp.groupby('stop_date').count()['stop_outcome']
        fig5=px.line(temp)
        fig5.update_layout(yaxis_title='Frequency')
        st.plotly_chart(fig5)
        
        search_out=st.selectbox('Select Search type:',df.search_type_agg.unique())
        temp=df[(df.search_type_agg==search_out)]
        temp["stop_date"] = pd.to_datetime(temp["stop_date"]).dt.date
        temp=temp[(temp.stop_date>=d1) & (temp.stop_date<=d2)]
        temp=temp.groupby('stop_date').count()['search_type_agg']
        fig6=px.line(temp)
        fig6.update_layout(yaxis_title='Frequency')
        st.plotly_chart(fig6)
        
    
elif selected == "Demographic Analysis":
    selected_dem = option_menu(None, ["Searches vs Stops", "Stop Duration across years", "Arrests vs Stops", "Speeding trends"], 
    default_index=0, orientation="horizontal")
    
    if selected_dem == "Searches vs Stops":
        st.subheader("Percentage of searches per stops")
        st.markdown('<div style="text-align: justify;"> Analyze the percentage of searches concerning the total number of stops. You have the flexibility to customize your analysis based on specific range of year and different demographic factors, such as age, gender, or race. </div>', unsafe_allow_html=True)
        st.markdown("#####")
        st.write("*Choose the range of years you are interested in analyzing. You can focus on a range of years to observe trends over time.*")
        min_max_year = st.slider('Select the Year Range:', 2005, 2015, (2007, 2012))
        st.markdown("####")
        st.write("*Select whether you want to analyze the data based on age, gender, or race. This choice will determine how the data is categorized and visualized.*")
        choose_hue = st.selectbox('Choose Demographic Factor:', ('driver_age_group', 'driver_race', 'driver_gender'))
        
        if choose_hue == 'driver_age_group':
            pop = 'age_population'
        elif choose_hue == 'driver_race':
            pop = 'race_population'
        else:
            pop = 'gender_population'
        
        temp = 100*df.groupby(by=['year',choose_hue])['search_conducted'].sum()/(df.groupby(by=['year',choose_hue]).max()[pop])
        temp = temp.reset_index().set_index('year')
        temp = temp[(temp.index>=min_max_year[0]) & (temp.index<=min_max_year[1])]
        
        fig = px.line(temp,color=choose_hue)
        fig.update_xaxes(showgrid=False, linecolor = "#BCCCDC")
        fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)')
        fig.update_yaxes(showgrid=True,gridcolor='#BCCCDC',gridwidth=0.3, linecolor = "#BCCCDC")
        if min_max_year[0]<2009:
            fig.add_vline(x=2009, line_dash="dash")
        st.write("**You can notice that the trends shift in the year 2009**")
        fig.update_layout(yaxis_title='Search rates')
        st.plotly_chart(fig)
        st.write("**Note:** The figures depicted in this graph have been standardized according to the census data representing the different racial, age and gender groups in Rhode Island.")
        
        st.subheader("Let's uncover the story behind the graph!")
        st.markdown("1. We observe a notable trend indicating that individuals within the age range of 65 to 100 years are consistently exempt from searches.")
        st.markdown("2. Individuals between the ages of 19 and 64 are searched more frequently compared to those in the age brackets of 6 to 18 or 65 to 100.")
        st.markdown("3. The graph reveals that black individuals are the most frequently searched, followed by Hispanics, and then Asians and whites.")
        st.markdown("The observed trend where individuals in the age groups 65 to 100 are never searched can be influenced by several factors such as,")
        st.markdown("- **Assumed Lower Risk:** Law enforcement officers might perceive elderly individuals as lower-risk in terms of criminal activity, leading to fewer searches in this age group.")
        st.markdown("- **Respect for Elderly:** There might be a cultural or societal norm that emphasizes respect for the elderly, resulting in fewer searches out of courtesy and regard for their age.")
        st.markdown("- **Health Considerations:** Older individuals may have health issues, and conducting searches could be physically challenging or potentially harmful, leading officers to avoid such procedures.")
        
        st.markdown('''<style>[data-testid="stMarkdownContainer"] ul{list-style-position: inside;}</style>''', unsafe_allow_html=True)
        
    elif selected_dem == "Arrests vs Stops":
        st.subheader("Percentage of arrests per stops")
        st.markdown('<div style="text-align: justify;"> Explore the percentage of arrests concerning the total number of police stops. </div>', unsafe_allow_html=True)
        st.markdown("#####")
        
        st.write("*Choose the range of years you are interested in analyzing. You can focus on a range of years to observe trends over time.*")
        min_max_year = st.slider('Select the Year Range:', 2005, 2015, (2005, 2008))
        st.markdown("####")
        st.write("*Select whether you want to analyze the data based on age, gender, or race. This choice will determine how the data is categorized and visualized.*")
        choose_hue = st.selectbox('Choose the demographic factor:', ('driver_age_group', 'driver_race', 'driver_gender'))
        
        if choose_hue == 'driver_age_group':
            pop = 'age_population'
        elif choose_hue == 'driver_race':
            pop = 'race_population'
        else:
            pop = 'gender_population'
        
        temp = 100*df.groupby(by=['year',choose_hue])['is_arrested'].sum()/(df.groupby(by=['year',choose_hue]).max()[pop])
        temp = temp.reset_index().set_index('year')
        temp = temp[(temp.index>=min_max_year[0]) & (temp.index<=min_max_year[1])]
        fig = px.line(temp,color=choose_hue)
        fig.update_xaxes(showgrid=False, linecolor = "#BCCCDC")
        fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)')
        fig.update_yaxes(showgrid=True,gridcolor='#BCCCDC',gridwidth=0.3, linecolor = "#BCCCDC")
        fig.update_layout(yaxis_title='Arrest rate')
        st.plotly_chart(fig)
        st.write("**Note:** The figures depicted in this graph have been standardized according to the census data representing the different racial, age and gender groups in Rhode Island.")
        
        st.subheader("Let's uncover the story behind the graph!")
        st.markdown("1. In 2006, the arrest rates for Black individuals notably decreased, although they continue to be higher than those for Hispanics, Whites, and Asians, with Hispanics having the second highest arrest rates among these groups.")
        st.markdown("2. The arrest rates for men significantly exceed those for women, standing at nearly three to four times the rate at which women are arrested.")
        st.markdown("3. Individuals between the ages of 19 and 64 exhibit higher arrest rates compared to any other age group, while those in the age group of 65 to 100 are rarely subject to arrest.")
        
        st.markdown("The reduction in arrest rates for Black individuals could be influenced by a range of factors like,")
        st.markdown("- **Policy Reforms:** Law enforcement agencies might have implemented policy changes, emphasizing community engagement, diversion programs, or rehabilitation over strict enforcement, leading to reduced arrests.")
        st.markdown("- **Community Outreach:** Increased efforts in community policing and engagement programs might have fostered trust and cooperation between law enforcement and minority communities, reducing confrontational interactions and subsequent arrests.")
        st.markdown("- **Legal Reforms:** Changes in laws or reforms related to non-violent offenses, drug offenses, or sentencing guidelines might have reduced the number of arrests across all racial groups.")
        
        st.markdown('''<style>[data-testid="stMarkdownContainer"] ul{list-style-position: inside;}</style>''', unsafe_allow_html=True)
        
        
    elif selected_dem == "Stop Duration across years":
        st.subheader("Trends in average stop duration across years")
        st.markdown('<div style="text-align: justify;"> Delve into the average stop duration concerning different periods. This interactive feature allows you to examine how the average duration of police stops has evolved over the chosen time frame. </div>', unsafe_allow_html=True)
        st.markdown("#####")
        
        st.write("*Choose the range of years you are interested in analyzing. You can focus on a range of years to observe trends over time.*")
        min_max_year = st.slider('Select the Year Range:', 2005, 2015, (2005, 2010))
        st.markdown("####")
        st.write("*Select whether you want to analyze the data based on age, gender, or race. This choice will determine how the data is categorized and visualized.*")
        choose_hue = st.selectbox('Choose the demographic factor:', ('driver_age_group', 'driver_race', 'driver_gender'))
        
        temp = df.groupby(by=['year',choose_hue])['stop_time'].mean()
        temp = temp.reset_index().set_index('year')
        temp = temp[(temp.index>=min_max_year[0]) & (temp.index<=min_max_year[1])]
        fig = px.line(temp,color=choose_hue)
        fig.update_xaxes(showgrid=False, linecolor = "#BCCCDC")
        fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)')
        fig.update_yaxes(showgrid=True,gridcolor='#BCCCDC',gridwidth=0.3, linecolor = "#BCCCDC")
        fig.update_layout(yaxis_title='Stop duration')
        st.plotly_chart(fig)
        
        st.subheader("Let's uncover the story behind the graph!")
        st.markdown("1. For individuals within the age group of 6 to 18, the duration of police stops is higher in comparison to other age groups.")
        st.markdown("2. For elderly individuals, specifically those aged between 65 and 100, the duration of police stops is higher than people belonging to the age groups 19 to 64.")
        st.markdown("3. The duration of police stops is longer for women in comparison to men.")
        
        st.markdown("The longer stop durations for individuals aged 6 to 18 could be influenced by several factors:")
        st.markdown("- **Parental Involvement:** Police officers might spend more time ensuring the safety and well-being of minors, which often involves interacting with parents or guardians, checking their identities, and confirming the child's relationship with them.")
        st.markdown("- **Document Verification:** Officers may need to verify identification documents and contact parents or legal guardians to confirm the minor's identity, which can prolong the stop duration.")
        st.markdown("- **Child Safety Protocols:** Law enforcement officers could be following specific protocols and procedures when dealing with minors, requiring additional time to confirm the child's safety, identity, and accompanying adult's authorization.")
        
        st.markdown("The fluctuations in stop duration for individuals aged 65 to 100 could be influenced by various factors such as,")
        st.markdown("- **Health Conditions:** Older individuals may have health issues or mobility challenges, leading to longer stop durations as they might need more time to provide information or exit the vehicle.")
        st.markdown("- **Communication Difficulties:** Seniors might experience hearing or communication difficulties, requiring officers to spend more time ensuring clear understanding, thereby increasing the stop duration.")
        st.markdown("- **Assistance Requirements:** Older individuals might need assistance in retrieving documents or complying with requests, contributing to extended stop durations.")
        
        st.markdown("The longer stop durations for women compared to men could be influenced by a variety of factors like,")
        st.markdown("- **Documentation Verification:** Officers might spend more time verifying identification documents or licenses for women, especially if there are name changes due to marriage or other reasons.")
        st.markdown("- **Safety Concerns:** Law enforcement officers could exercise extra precautions with women, particularly during late hours, to ensure their safety, which might involve more thorough checks and inquiries.")
        st.markdown("- **Search Procedures:** If a search is required, female officers might be called to conduct the search on women, which could take additional time.")
        
        st.markdown('''<style>[data-testid="stMarkdownContainer"] ul{list-style-position: inside;}</style>''', unsafe_allow_html=True)
        
    elif selected_dem == "Speeding trends":
        st.subheader("Understanding Speeding Patterns Across Demographics!")
        st.markdown('<div style="text-align: justify;"> Compare speeding incidents between different races or genders that you select. Explore the disparities in speeding patterns by comparing one race to another or analyzing gender categories comprehensively. </div>', unsafe_allow_html=True)
        st.markdown("#####")
        
        st.write("*Choose whether you want to analyze speeding patterns based on races or genders. This selection will determine the demographic factor that forms the basis of your analysis.*")
        choose_column = st.selectbox('Select Speeding Analysis Type', ('driver_race', 'driver_gender'))
        
        column1 = st.selectbox('Pick a parameter to define the x-axis variable for your analysis', df[choose_column].unique())
        column2 = st.selectbox('Pick a parameter to define the y-axis variable for your analysis', df[choose_column].unique())
        
        if choose_column == 'driver_age_group':
            pop = 'age_population'
        elif choose_column == 'driver_race':
            pop = 'race_population'
        else:
            pop = 'gender_population'
        
        d = {}
        for i in df[choose_column].unique():
            dataframe = df[(df[choose_column] == i)]
            dataframe['Speeding_violation'] = dataframe.violation=='Speeding'
            across_ethnicities = dataframe.groupby('driver_age')['Speeding_violation'].sum()/dataframe.groupby(['driver_age',choose_column])[pop].max()
            across_ethnicities=across_ethnicities.to_frame().reset_index()
            data = pd.DataFrame(columns=["age", choose_column]) 
            data.loc[:, 'age'] = np.arange(101) 
            data[choose_column] = i
            data1=data.merge(across_ethnicities, left_on='age', right_on='driver_age')
            d[i] = data1

        temp=d[column1].merge(d[column2],how='outer',on='age')
        fig=px.scatter(temp,x='0_x',y='0_y',size='age',width=400,height=400, 
                   labels={'0_x':column1, '0_y':column2})
        
        if temp['0_x'].max()>temp['0_y'].max():
            val=temp['0_x'].max()
        else:
            val=temp['0_y'].max()
            
        if temp['0_x'].min()<temp['0_y'].min():
            val2=temp['0_x'].min()
        else:
            val2=temp['0_y'].min()
            
        if temp['0_x'].std()>temp['0_y'].std():
            sd=temp['0_x'].std()
        else:
            sd=temp['0_y'].std()
        
        fig.update_yaxes(range=[val2-sd, val+sd])
        fig.update_xaxes(range=[val2-sd, val+sd])
        fig.update_layout(shapes = [{'type': 'line', 'yref': 'paper', 'xref': 'paper', 'y0': 0, 'y1': 1, 'x0': 0, 'x1': 1}])
        st.plotly_chart(fig)
        
elif selected == "Summary":
    st.subheader("Significance:")
    st.markdown('<div style="text-align: justify;"> Exploring Stanford Open Policing Dataset to understand law enforcement practices can be helpful to not only enhance interaction between the police and the public but can also potentially contribute to the safety and well-being of communities. This initiative aligns with the broader goal of creating proactive, data-driven solutions for crime prevention, making it a project of immense value and impact. </div>', unsafe_allow_html=True)
    st.markdown('#####')
    st.subheader("Focus Dataset:")
    st.markdown('<div style="text-align: justify;"> Stanford Open Policing Dataset (Rhode Island): Contains crucial data on stop time, violation, and outcomes. </div>', unsafe_allow_html=True)
    st.markdown('#####')
    st.subheader("Potential Impact:")
    st.markdown('<div style="text-align: justify;">  Improved Police-Community Relations and community well-being </div>', unsafe_allow_html=True)
    st.markdown('#####')
    st.subheader("Next Steps:")
    st.markdown('<div style="text-align: justify;">  Predict crime patterns based on the patterns observed in this historical data which will aid crime prevention. </div>', unsafe_allow_html=True)