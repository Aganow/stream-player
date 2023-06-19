import requests
import vlc


class StreamPlayer:
    def __init__(self, url):
        self.url = url
        self.vlc_instance = vlc.Instance()
        self.player = self.vlc_instance.media_player_new()
        self.media = self.vlc_instance.media_new(url)
        self.player.set_media(self.media)

    def play(self):
        try:
            self.player.play()
            input("Press Enter to stop playback...")
            self.player.stop()
        except Exception as e:
            print(f"An error occurred while playing the stream: {e}")
        finally:
            self.player.release()


class StreamInfo:
    def __init__(self, url):
        self.url = url

    def get_info(self):
        try:
            response = requests.head(self.url)
            if response.status_code == 200:
                print("Stream information:")
                for key, value in response.headers.items():
                    print(f"{key}: {value}")
            else:
                print("Failed to connect to the stream.")
        except requests.RequestException as e:
            print(f"An error occurred while retrieving stream information: {e}")


def main():
    stream_url = "STREAM URL"
    
    info = StreamInfo(stream_url)
    info.get_info()
    
    player = StreamPlayer(stream_url)
    player.play()

if __name__ == "__main__":
    main()
