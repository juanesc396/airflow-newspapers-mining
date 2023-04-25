import pandas as pd
from datetime import datetime
import pymongo
from sqlalchemy import create_engine
import os
import spacy

print(f'Spacy prefer GPU: {spacy.prefer_gpu()}')

IP_LOCAL = os.environ.get('IPPC')
RDSIP = os.environ.get('RDSIP')
RDSPW = os.environ.get('RDSPW')


mongodb_conn = pymongo.MongoClient(f"mongodb://{IP_LOCAL}:27017/")
mydb = mongodb_conn['Newspapers']

mysql_rds = create_engine(f'mysql+pymysql://admin:{RDSPW}@{RDSIP}/newspaper_analytics')

def extract_data(date) -> pd.core.frame.DataFrame:
    to_df = []
    for col in mydb.list_collection_names():
        for d in mydb[col].find(date):
            if d['title'] != None and d['language'] == 'Spanish':
                to_df.append(d)

    dataframe = pd.DataFrame(to_df)
    return dataframe

def cleaner(row):
    """
    Function that returns clean headlines
    """
    return row['title'].strip('\n').strip().replace(u'\xa0', u' ')

def set_country_key(row):
    """
    Function that returns the country key (3 letters)
    """
    c_key = pd.read_excel('/home/juan/airflow/projects/nlp_task/country_keys.xlsx')
    key = c_key.loc[c_key['country'] == row.country]['3key'].values[0]
    return key

def clean_data(dataframe) -> pd.core.frame.DataFrame:
    """
    Function that cleans the data
    """
    dataframe['title'] = dataframe.apply(cleaner, axis = 1)
    dataframe = dataframe[dataframe['title'].astype(bool)].copy() # NaN cleaner
    dataframe.drop_duplicates(subset='title', inplace=True)
    dataframe['country_key'] = dataframe.apply(set_country_key, axis = 1)
    dataframe.drop(columns=['_id', 'epigraph'], inplace=True)
    dataframe.reset_index(drop=True, inplace=True)
    return dataframe

def classification(cleaned_dataframe) -> pd.core.frame.DataFrame:
    """
    Function built to classify the data
    """
    # Loading the models to use
    posneg_textcat = spacy.load('/home/juan/airflow/projects/nlp_task/pn_model/model-best')
    genre_textcat = spacy.load('/home/juan/airflow/projects/nlp_task/genre_textcat_model/model-best')

    # Create a list with the Positive/Negative classification of each headline.
    posneg_classf = []
    for i in cleaned_dataframe.itertuples():
        doc = posneg_textcat(i.title)
        cats = doc.cats
        if cats['POSITIVE'] > .5:
            posneg_classf.append(1)
        else:
            posneg_classf.append(0)

    # Create a list with the Genre classification of each headline.
    genre_classf = []
    for i in cleaned_dataframe.itertuples():
        doc = genre_textcat(i.title)
        cats = doc.cats
        temp = {}
        for key, value in cats.items():
            if value > 0.1:
                temp[key.lower()] = 1
            else:
                temp[key.lower()] = 0
        if sum(temp.values()) == 0:
            temp['other'] = 1
        else:
            temp['other'] = 0
        genre_classf.append(temp)

    posneg_df = pd.DataFrame(posneg_classf, columns=['positive'])
    genre_df = pd.DataFrame(genre_classf)
    df = pd.concat([cleaned_dataframe, posneg_df, genre_df], axis=1, ignore_index=True)
    columns_names = cleaned_dataframe.columns.to_list()
    columns_names.append('positive')
    columns_names.extend(genre_df.columns.to_list())
    columns_names[3] = 'lang' #SQL doesn't allows "language" as a field name 
    df.columns = columns_names

    return df

if __name__ == '__main__':
    today = datetime.today().strftime('%Y-%m-%d')
    date = {"scrape_date": f"{today}"}
    
    news_dataset = extract_data(date)
    cleaned_news = clean_data(news_dataset)
    classificated_news = classification(cleaned_news)

    classificated_news.to_sql(name='news',
                              con=mysql_rds,
                              if_exists='append',
                              index=False
                              )
