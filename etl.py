import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    '''
    - Fetches data from json song file.
    
    - Loads relevant data into songs table.
    
    - Loads relevant data into artists table.
    '''
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id','title','artist_id','year','duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    '''
    - Fetches data from json log file.
    
    - Filters data based on NextSong action.
    
    - Tranforms and loads data into time table.
    
    - Loads relevant data into users table.
    
    - Inserts data into songplays table by fetching data from  songs table, artists table along with log data from json files.
    '''
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page']=='NextSong']

    # convert timestamp column to datetime
    time_df = df[['ts']]
    time_df['start_time'] = pd.to_datetime(time_df['ts'], unit='ms')
    time_df['hour'] = time_df['start_time'].dt.hour
    time_df['day'] = time_df['start_time'].dt.day
    time_df['week'] = time_df['start_time'].dt.week
    time_df['month'] = time_df['start_time'].dt.month
    time_df['year'] = time_df['start_time'].dt.year
    time_df['weekday'] = time_df['start_time'].dt.weekday
    
    # insert time data records
    time_df = time_df[['start_time','hour', 'day', 'week', 'month', 'year', 'weekday']]

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']].drop_duplicates().dropna()

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    df['start_time'] = pd.to_datetime(df['ts'], unit='ms')
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.start_time, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    '''
    - Iterates over all the files present in the filepath argument.
    
    - Executes ETL For each file object by calling process_song_file or process_log_file internally.
    
    - Commits the data ingested into the database.
    '''
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    - Establishes connection with the sparkify database and gets
    cursor to it.  
    
    - Performs ETL and ingests data into all the tables  
    
    - Finally, closes the connection. 
    """
    try:
        conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
        cur = conn.cursor()
        
        process_data(cur, conn, filepath='data/song_data', func=process_song_file)
        process_data(cur, conn, filepath='data/log_data', func=process_log_file)

        conn.close()
    except psycopg2.Error as e:
        print("Error: Could not make connection or could not get cursor")
        print(e)
        

    


if __name__ == "__main__":
    main()