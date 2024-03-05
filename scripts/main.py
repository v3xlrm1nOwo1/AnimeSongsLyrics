import pickle
import langid
import requests
import argparse
import pandas as pd
import pyarrow as pa
import concurrent.futures
import pyarrow.parquet as pq
from bs4 import BeautifulSoup



class AnimeSongsLyrics:
    def __init__(self):
        self.url = 'https://www.uta-net.com/user/search/anime_list.html?index='
        self.tags = {'TM': '主題歌', 'S': '挿入歌', 'OP': 'オープニング', 'ED': 'エンディング', 'IS': 'イメージソング', 'O': 'その他'}


    # =============================== SAVE DATA =============================== #
    def save(self, data, output_file):
        output_file = f'data/{output_file}.pkl'

        print(f'Saving {len(data)} rows!')

        with open(output_file, 'wb') as f:
            pickle.dump(data, f)

        print(f'Data successfully written to {output_file}\n')


    # =============================== CONVERT TO PARQUET =============================== #  
    def convert_to_parquet(self, output_file, data: list):
        '''
            - convert a list of dictionaries to a Parquet file.
        '''

        print(f'Saving {len(data)} rows!')

        # Convert list of dictionaries to pandas DataFrame
        df = pd.DataFrame(data)

        # Convert pandas DataFrame to PyArrow Table
        table = pa.Table.from_pandas(df)

        # Specify the Parquet file path
        parquet_file_path = f'data/{output_file}.parquet'

        # Write the PyArrow Table to a Parquet file
        pq.write_table(table, parquet_file_path)

        print(f'Data successfully written to {parquet_file_path}')


    # =============================== PAGE CONTENT =============================== #    
    def get_page_content(self, page_url):
        req = requests.get(url=page_url)
        return BeautifulSoup(req.text, 'lxml')


    # =============================== GET ALL ANIME SONGS LISTS URLS =============================== #
    def get_anime_songs_lists_urls(self):
        '''
            - Main goal: Retrieve all anime list URLs.
            - Returns list: A list of dictionaries containing anime name and corresponding list URL.
        '''
    
        # data storage
        anime_songs_lists_urls = []
        unique_anime_songs_lists_urls = []

        def fetch_page(page_index):
            # page url
            page_url = f'{self.url}{str(page_index)}'

            # page content
            bs = self.get_page_content(page_url=page_url)

            # process tables
            for table_class in ['title_table', 'title_table2']:
                table = bs.find(name='table', attrs={'class': table_class})
                if table:
                    # all URLs from the table
                    table_urls = table.find_all(name='a', )

                    # save data in a dictionary and add it to the list
                    for a_tag in table_urls:
                        anime_name = a_tag.text.strip()
                        anime_url = f'https://www.uta-net.com/{a_tag["href"]}'.strip()
                        if anime_url not in unique_anime_songs_lists_urls:
                            unique_anime_songs_lists_urls.append(anime_url)

                            anime_songs_lists_urls.append({
                                'Anime': anime_name, 
                                'Anime List Songs URL': anime_url
                                })

        # Fetching pages concurrently using ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Create a list of futures for each page index using the fetch_page function
            futures = [executor.submit(fetch_page, page_index) for page_index in range(48)]
            # Wait for all the futures to complete before proceeding
            concurrent.futures.wait(futures)

        self.save(data=anime_songs_lists_urls, output_file='anime_songs_lists_urls.pkl')
        return anime_songs_lists_urls


# =============================== GET ALL ANIME SONGS URLS =============================== #
    def get_anime_songs_urls(self, anime_songs_lists_urls: list):
        '''
            - Main goal get all anime song url.
            - Save all data Song Title, Song URL, Artist, Type and Start Singing in list of dict.
        '''

        # data storage
        anime_songs_urls = []

        def fetch_songs(anime_songs_list_url):
            list_url = anime_songs_list_url['Anime List Songs URL']
            
            bs = self.get_page_content(page_url=list_url)
            
            # main table
            main_table = bs.find(name='table', attrs={'width': "645", 'border': "0", 'align': "center", 'cellpadding': "3", 'cellspacing': "1", 'bgcolor': "#CCCCCC",})

            if main_table is None:
                return None

            tr_tags = main_table.find_all(name='tr')

            if tr_tags is None:
                return None

            # songs information
            for tr_tag in tr_tags:
                td_tags = tr_tag.find_all(name='td')

                if td_tags is None:
                    continue

                try:
                    song_title = td_tags[0].text.strip()
                    song_url = f'https://www.uta-net.com{td_tags[0].find(name="a")["href"].strip()}'
                    artist = td_tags[1].text.strip()
                    song_type = td_tags[2].text.strip()
                    start_singing = td_tags[3].text.strip()

                    # find japanese tag song 
                    for key in self.tags.keys():
                        if song_type == key:
                            song_type_jp = self.tags[key]
                            song_type = f'{song_type} / {song_type_jp}'
                except:
                    continue

                # save data in dictionary
                result = {
                    'Song Title': song_title,
                    'Song URL': song_url,
                    'Artist': artist,
                    'Type': song_type,
                    'Start Singing': start_singing,
                    **anime_songs_list_url,
                }
                
                # save dictionary in list
                anime_songs_urls.append(result)

        # Fetching anime songs lists concurrently using ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Create a list of futures for each anime songs list URL using the fetch_songs function
            futures = [executor.submit(fetch_songs, anime_songs_list_url) for anime_songs_list_url in anime_songs_lists_urls]
            # Wait for all the futures to complete before proceeding
            concurrent.futures.wait(futures)

        self.save(data=anime_songs_urls, output_file='anime_songs_urls.pkl')
        return anime_songs_urls


# =============================== GET ALL ANIME SONGS INFORMATION =============================== #
    def get_anime_songs_info(self, anime_songs_urls: list):
        '''
            - Main goal get all anime song lyrics.
            - Get all song lyrics data and all data from previous functions and save them in list of dictionary.
        '''

        # data storage
        anime_songs_info = []

        def fetch_song_info(anime_song_info):
            url = anime_song_info['Song URL']
            bs = self.get_page_content(page_url=url)

            main_div = bs.find(name='div', attrs={'class': 'col-12 song-infoboard'})
            
            if main_div is None:
                return None

            song_info = (main_div.find(name='p', attrs={'class', 'ms-2 ms-md-3 detail mb-0'})).get_text().strip()
            song_info = [i.strip() for i in song_info.split('  ') if i.strip() != '']

            song_info_ = {}
            for item in song_info:
                if item.find('：') != -1:
                    try:
                        key, value = item.split('：')
                    except:
                        item = item.split('：')
                        key = item[0]
                        value = item[1].split('・')
                        value = '・'.join(value[: -1])
                        value = f'{value} / {item[-1]}'

                    value = value.strip()

                    if key.strip() == '作詞':
                        key = 'lyrics_by'
                    elif key.strip() == '作曲':
                        key = 'composition_by'
                    elif key.strip() == '編曲':
                        key = 'arrange'
                    elif key.strip() == '発売日':
                        key = 'release_date'
                    elif key.strip() == 'この曲の表示回数':
                        key = 'views'
                        value = value[: -1]
                        value = value.replace(',', '')

                    song_info_[key.strip()] = value

            lyric_div = bs.find(name='div', attrs={'id': 'kashi_area'})

            if lyric_div is None:
                return None

            lyric = ''

            for tag in lyric_div.contents:
                if tag.name == 'br':
                    lyric += '\n'
                else:
                    lyric += tag.text.replace('\u3000', ' ')

            lyric_lines = lyric.split('\n')

            for i in range(len(lyric_lines)):
                line = lyric_lines[i]
                if line is None:
                    continue

                if i != len(lyric_lines) - 1 and line.startswith('(') and line.endswith(')') and langid.classify(lyric_lines[i + 1])[0] != 'ja':
                    lyric_lines[i] = line[1: -1]
                    lyric_lines[i + 1] = None

            lyric = '\n'.join([line for line in lyric_lines if isinstance(line, str)])
            result = {
                'Lyric': lyric,
                **song_info_,
                **anime_song_info,
            }

            anime_songs_info.append(result)
        
        # Fetching anime song information concurrently using ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Create a list of futures for each anime song info using the fetch_song_info function
            futures = [executor.submit(fetch_song_info, anime_song_info) for anime_song_info in anime_songs_urls]
            # Wait for all the futures to complete before proceeding
            concurrent.futures.wait(futures)

        return anime_songs_info


    def main(self, output_file):
        lists_urls = self.get_anime_songs_lists_urls()
        songs_urls = self.get_anime_songs_urls(anime_songs_lists_urls=lists_urls)
        anime_songs_info = self.get_anime_songs_info(anime_songs_urls=songs_urls)

        self.save(data=anime_songs_info, output_file=output_file)
        self.convert_to_parquet(data=anime_songs_info, output_file=output_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output-file', type=str, default='AnimeSongsLyrics', help='output file name')
    args = parser.parse_args()
    print(args)

    anime_song_lyrics = AnimeSongsLyrics()
    anime_song_lyrics.main(output_file=args.output_file)
    print('Done!!')


