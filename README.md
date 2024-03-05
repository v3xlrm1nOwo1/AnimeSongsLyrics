




# Anime Songs Lyrics Dataset ― アニメソングの歌詞データセット<img src="./assets/AnimeMusic.gif" width="80px" height="80" />

<!-- <p align="center">
	<img src="./assets/AnimeMusic.gif" width="80px" height="80" />
</p> -->

> Welcome to the Anime Songs Lyrics Dataset

<div align="center">
    <picture>
        <source 
        srcset="assets/AnimeMusic.jpg"
        media="(prefers-color-scheme: dark)"
        />
        <source
        srcset="assets/AnimeMusic.jpg"
        media="(prefers-color-scheme: light), (prefers-color-scheme: no-preference)"
        />
        <img src="assets/AnimeMusic.jpg" width="100%" height="450px" />
    </picture>
</div>


## Overview
This dataset compiles a diverse collection of lyrics from various anime songs, providing a rich resource for enthusiasts and researchers alike. The lyrics are structured in a list of dictionaries, allowing easy access for analysis, research, or personal enjoyment.

The dataset is also available in Parquet file format, named AnimeSongsLyrics.parquet, allowing efficient storage and retrieval of the dataset.

<p>You can find this dataset on my Huggingface account <a href="https://huggingface.co/datasets/v3xlrm1nOwo1/AnimeSongsLyrics">v3xlrm1nOwo1</a>.</p>


## Data Format

Each entry in the dataset is represented by a dictionary with the following fields:

- `Lyric`: The text of the song's lyrics.
- `LyricsBy`: The person or entity responsible for the lyrics.
- `CompositionBy`: The person or entity responsible for the composition.
- `ReleaseDate`: The date when the song was released.
- `Views`: The number of views or popularity metric.
- `SongTitle`: The title of the song.
- `SongURL`: The URL of the song.
- `Artist`: The artist or group performing the song.
- `Type`: The type or genre of the song.
- `StartSinging`: The starting point of the lyrics.
- `Anime`: The anime associated with the song.
- `AnimeListSongsURL`: URL linking to the anime's list of songs.
- `Arrangement`: Additional information about the arrangement or version.


## Usage

### Pickle File:

```python
import pickle
import random

# Load the dataset
with open('data/AnimeSongsLyrics.pkl', 'rb') as file:
    anime_songs_lyrics = pickle.load(file)

# Access a random song's lyrics
random_song_lyrics = random.choice(anime_songs_lyrics)

for key, value in random_song_lyrics.items():
    print(f'{key}:\n{value}\n')
```

```zsh
Lyric: 
もがきながら最高の夢を
形にするこの瞬間が好きさ
戦うような 手を繋ぐような
感覚が (交差して) 刺激的だね...

LyricsBy: 
畑亜貴

CompositionBy: 
高田暁

ReleaseDate: 
2012/11/07

Views: 
34846

SongTitle: 
Pride on Everyday

SongURL: 
https://www.uta-net.com/song/137527/

Artist: 
スフィア

Type: 
ED / エンディング

StartSinging: 
もがきながら最高の夢を形に

Anime: 
バクマン。3

AnimeListSongsURL: 
https://www.uta-net.com//user/search/anime_list_2.html?tno=8973

Arrangement: 
高田暁
```

### Parquet File:

```py
import pandas as pd

# Specify the Parquet file path
parquet_file_path = 'data/AnimeSongsLyrics.parquet'

# Read the Parquet file into a Pandas DataFrame
df = pd.read_parquet(parquet_file_path, engine='pyarrow')

# Display a random row from the DataFrame
random_row = df.sample()
print('Random Row:')
print(random_row)
```

```zsh
Random Row:
                                                   Lyric LyricsBy  ...                               AnimeListSongsURL Arrangement
16405  ふわりとなぞる風は\n包む指をすり抜けて\n刹那に満ちて欠ける\n月が妖しく光る彼方へ\n\...     中村振二郎  ...  https://www.uta-net.com//user/search/anime_lis...    悠木真一      

```


## Contributions
We welcome contributions and feedback to enhance the Anime Songs Lyrics Dataset further! Whether you're adding new songs, improving existing lyrics, or providing valuable feedback, your input is highly appreciated.


## Acknowledgments
A special thanks to all the talented artists and creators behind these anime songs, making this dataset a melodic treasure trove.


## License
<p>This dataset is provided under the [Apache License 2.0](LICENSE). Feel free to use, modify, and share it.</p>
<p>Immerse yourself in the Anime Songs Lyrics Dataset and let the enchanting melodies of anime unfold! 🎶🌟🚀</p>


> **_NOTE:_**  To contribute to the project, please contribute directly. I am happy to do so, and if you have any comments, advice, job opportunities, or want me to contribute to a project, please contact me I am happy to do so <a href='mailto:v3xlrm1nOwo1@gmail.com' target='blank'>v3xlrm1nOwo1@gmail.com</a>