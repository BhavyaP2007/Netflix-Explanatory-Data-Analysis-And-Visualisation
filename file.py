import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#I will draw useful insights from the data based on changes in trends over the years

#Cleaning Data
df1 = pd.read_csv("C:/Users/bpmch/OneDrive/Desktop/python/pandas/projects/netflix eda/netflix_titles.csv")
df = df1.drop(columns=["description"])
df["cast"]=df["cast"].str.split(", ")
df_cast_analysis = df.explode(column="cast").reset_index()
df["listed_in"]=df["listed_in"].str.split(", ")
df_genre_analysis = df.explode(column="listed_in").reset_index()
pd.set_option('display.max_columns', None)

#How has the number of movies listed on Netflix changed over the years?
release_years = df["release_year"].value_counts().reset_index().sort_values("release_year")
release_years = release_years.loc[release_years["count"]>10].sort_values("release_year")
plt.figure(figsize=(15,7))
plt.subplot(2,2,1)
plt.plot(release_years["release_year"],release_years["count"])
plt.xticks(list(range(1980,2030,10)))
plt.xlabel("Year")
plt.ylabel("No. Of Movies and Shows")
plt.title("No. of movies and shows released in last 40 years")
plt.grid()
#Comparision of TV Shows and Movies

bins = [0, 1990, 2000, 2010, 2020,2030]
labels = ['<1990', '1991-2000', '2001-2010', '2011-2020',"2020+"]
categories_by_year = df.loc[:,["release_year","type"]]
categories_by_year["time_group"] = pd.cut(categories_by_year["release_year"],labels=labels,bins=bins)
movies = categories_by_year.loc[categories_by_year["type"]=="Movie"]["time_group"].value_counts().reset_index()
tv_shows = categories_by_year.loc[categories_by_year["type"]=="TV Show"]["time_group"].value_counts().reset_index()
movies.rename(index={4:0,3:1,1:2,0:3,2:4},inplace=True)
movies.sort_index(inplace=True)
tv_shows.rename(index={4:0,3:1,2:2,0:3,1:4},inplace=True)
tv_shows.sort_index(inplace=True)
plt.subplot(2,2,2)
bar_plot1 = plt.bar(np.arange(0,5)-0.15,movies["count"],width=0.3,label="Movies")
bar_plot2 = plt.bar(np.arange(0,5)+0.15,tv_shows["count"],width=0.3,label="TV Shows")
plt.legend()
plt.title("Comparision of Movies and TV Shows")
plt.xticks(np.arange(0,5),labels)
plt.xlabel("Year Groups")
plt.ylabel("Count")
plt.grid()

#Genre Distribution Data Cleaning
genre = df_genre_analysis.loc[:,["listed_in"]].value_counts().reset_index().sort_values("count",ascending=False)
genre.loc[1,"count"] = genre.loc[1,"count"]+genre.loc[6,"count"]
genre.loc[2,"count"] = genre.loc[2,"count"]+genre.loc[10,"count"]
genre.loc[5,"count"] = genre.loc[5,"count"]+genre.loc[25,"count"]
genre.loc[9,"count"] = genre.loc[9,"count"]+genre.loc[16,"count"]
genre.loc[11,"count"] = genre.loc[11,"count"]+genre.loc[37,"count"]
genre.loc[21,"count"] = genre.loc[11,"count"]+genre.loc[31,"count"]
genre.loc[56,"count"] = genre.loc[18,"count"]+genre.loc[39,"count"]
genre.drop(index=[0,3,6,10,16,25,37,31,18,41],inplace=True)
genre = genre[genre['listed_in'] != 'Independent Movies']
genre.dropna(inplace=True)
plt.subplot(2,2,3)
genre = genre.reset_index()
genre = genre.loc[genre["count"]>=300]
plt.title("Top Genres")
plt.pie(genre["count"],labels=genre["listed_in"],labeldistance=1.4,explode=[0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1],autopct="%1.1f %%",pctdistance=1.18)

#Variation of genre with time
genre_with_time = df_genre_analysis.loc[:,["release_year","listed_in"]]
genre_with_time = genre_with_time.loc[(genre_with_time["listed_in"] != "International Movies") & (genre_with_time["listed_in"] != "International TV Shows") & (genre_with_time["listed_in"] != "Classic Movies")]
genre_with_time = genre_with_time.groupby(["release_year","listed_in"])["listed_in"].value_counts().reset_index(name="count")
genre_with_time = genre_with_time.loc[genre_with_time.groupby('release_year')['count'].idxmax()].reset_index().loc[:,["release_year","listed_in"]]
genre_with_time.to_csv(path_or_buf="C:/Users/bpmch/OneDrive/Desktop/python/pandas/projects/netflix eda/genre_with_time.csv")

#Caste Analysis
#Most frequent actors
cast_count = df_cast_analysis["cast"].dropna().value_counts().reset_index()
cast_count = cast_count.iloc[0:15]
plt.subplot(2,2,4)
plt.subplots_adjust(wspace=0.2,hspace=0.5)
plt.barh(cast_count["cast"],cast_count["count"])
plt.title("Most frequent Actors")
plt.grid()
plt.show()

#Movies preferred by famous actors
df_genre_analysis.dropna(subset="duration",inplace=True)
genre_movies_length =  df_genre_analysis.loc[~(df_genre_analysis["duration"].str.contains("Season"))].loc[:,["listed_in","duration"]]
genre_movies_length["duration"] = genre_movies_length["duration"].astype(str).apply(lambda  x: x[:-4]).astype(int)
genre_movies_length = genre_movies_length.groupby("listed_in")["duration"].mean().reset_index()
genre_movies_length["duration"] = genre_movies_length["duration"].apply(lambda x: round(x,1))
genre_movies_length.drop(index=[13,10,11,3],inplace=True)
plt.style.use("dark_background")
plt.subplot(2,1,1)
plt.barh(genre_movies_length["listed_in"],genre_movies_length["duration"])
for i,v in enumerate(genre_movies_length["duration"]):
    plt.text(v,i,str(v))
plt.title("Average Length of top 15 Genres")
plt.xlabel("Length in minutes")

#duration_over_time
df_drop = df.dropna(subset="duration")
duration_with_time = df_drop.loc[~(df_drop["duration"].str.contains("Season"))].loc[:,["release_year","duration"]]
duration_with_time["duration"] = duration_with_time["duration"].astype(str).apply(lambda  x: x[:-4]).astype(int)
duration_with_time = duration_with_time.groupby("release_year")["duration"].mean().reset_index(name="average_length")
plt.subplot(2,1,2)
plt.subplots_adjust(wspace=0.2,hspace=0.5)
plt.plot(duration_with_time["release_year"],duration_with_time["average_length"])
plt.ylabel("Duration in mintues")
plt.xlabel("Year")
plt.title("Average Duration over the years")
plt.show()