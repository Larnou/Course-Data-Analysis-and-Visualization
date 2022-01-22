from googleapiclient.discovery import build
import codecs
import isodate

api_key = 'AIzaSyCGR-p_nZalvIo1dooOrA1q98hjRmfmhi4'
utopia_show = "UC8M5YVWQan_3Elm-URehz9w"
youtube = build('youtube', 'v3', developerKey=api_key)

playlists = []
videos = []


def get_videos(playlist_id, playlist_name, token):
    videos_list = []
    while True:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            pageToken=token,
            maxResults=50
        )
        response = request.execute()
        for i in range(len(response['items'])):
            videos_list += [[playlist_name, response['items'][i]['snippet']['resourceId']['videoId'],
                             response['items'][i]['snippet']['title']]]
        try:
            token = response['nextPageToken']
        except:
            break

    return videos_list


def video_info():
    for i in range(len(videos)):
        request = youtube.videos().list(
            part="statistics, snippet, contentDetails",
            id=videos[i][1]
        )
        response = request.execute()

        # Обрабатываем ошибки, возникающие при обработке приватных видео, видео с закрытыми лайками и прочего такого
        #  В привытных или удалённых видео, нельзя получить данные видео

        # videos[i] += response.get('items')[0].get('snippet').get('publishedAt')
        # videos[i] += response.get('items')[0].get('statistics').get('viewCount')
        # videos[i] += response.get('items')[0].get('statistics').get('likeCount')
        # videos[i] += response.get('items')[0].get('statistics').get('commentCount')
        # videos[i] += [int(isodate.parse_duration(response.get('items')[0].get('contentDetails').get('duration')).total_seconds())]

        try:
            videos[i] += [response['items'][0]['snippet']['publishedAt']]
            videos[i] += [response['items'][0]['statistics']['viewCount']]
            videos[i] += [response['items'][0]['statistics']['likeCount']]
            # videos[i] += [response['items'][0]['statistics']['dislikeCount']]
            videos[i] += [response['items'][0]['statistics']['commentCount']]
            videos[i] += [int(isodate.parse_duration(response['items'][0]['contentDetails']['duration']).total_seconds())]
        except:
            print('oops')


def write_csv():
    with codecs.open('datas.csv', "w", "utf-8") as dataFile:
        dataFile.write(
            "playlist_name;video_id;video_name;publication_date;views;likes;comments;duration" + "\n")
        for i in range(len(videos)):
            if videos[i][2] != "Private video" and videos[i][2] != "Deleted video":
                for j in range(7):
                    dataFile.write(str(videos[i][j]) + ";")
                dataFile.write(str(videos[i][7]) + "\n")


# ===================================== КОД НАЧИНАЮТСЯ С ЭТОГО МЕСТА ==================================

# Получаем id и названия каждого плейлиста на канале Utopia Show
request = youtube.playlists().list(
    part="snippet",
    channelId=utopia_show,
    maxResults=50
)
response = request.execute()

for i in range(len(response['items'])):
    playlists += [[response['items'][i]['id'], response['items'][i]['snippet']['title']]]

# Получаем список всех видео в каждом плейлисте, если в плелисте больше 50 видео, повторяем запрос с токеном
# nextPageToken
for i in range(len(playlists)):
    v_request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlists[i][0],
        maxResults=50
    )
    v_response = v_request.execute()

    for j in range(len(v_response['items'])):
        videos += [[playlists[i][1], v_response['items'][j]['snippet']['resourceId']['videoId'],
                    v_response['items'][j]['snippet']['title']]]
    try:
        videos += get_videos(playlists[i][0], playlists[i][1], v_response['nextPageToken'])
    except:
        pass

video_info()
write_csv()