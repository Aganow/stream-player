import requests
import vlc
import ctypes
import time

@vlc.CallbackDecorators.MediaOpenCb
def media_open_cb(opaque, data_pointer, size_pointer):
    print("OPEN", opaque, data_pointer, size_pointer)

    stream_provider = ctypes.cast(opaque, ctypes.POINTER(ctypes.py_object)).contents.value

    stream_provider.open()

    data_pointer.contents.value = opaque
    size_pointer.value = 1 ** 64 - 1

    return 0


@vlc.CallbackDecorators.MediaCloseCb
def media_close_cb(opaque):
    print("CLOSE", opaque)

    stream_provider = ctypes.cast(opaque, ctypes.POINTER(ctypes.py_object)).contents.value

    stream_provider.release_resources()

def my_callback(event, player):
    print(event.type)
    if (event.type == vlc.EventType.MediaPlayerStopped):
        print(event)
        print(player)
        attempts = 5
        connected=False
        interval = 5
        while (attempts > 0) and not connected:
            time.sleep(interval)
            print("attempting to restart")
            attempts = attempts-1
            player.play()
        
        print("done for now")

class StreamPlayer:
    def __init__(self, url):
        self.url = url


        # # helper object acting as media data provider
        # # it is just to highlight how the opaque pointer in the callback can be used
        # # and that the logic can be isolated from the callbacks
        # stream_provider = StreamProviderDir(args.media_folder, args.extension)

        # # these two lines to highlight how to pass a python object using ctypes
        # # it is verbose, but you can see the steps required
        # stream_provider_obj = ctypes.py_object(stream_provider)
        # stream_provider_ptr = ctypes.byref(stream_provider_obj)

        self.vlc_instance = vlc.Instance()
        # self.media = self.vlc_instance.media_new_callbacks(media_open_cb, None, None, media_close_cb, None)
        # self.player = self.media.player_new_from_media()

        # self.media = self.vlc_instance.media_new(url)

        self.player = self.vlc_instance.media_player_new()
        self.media = self.vlc_instance.media_new(url)
        self.player.set_media(self.media)
        events = self.player.event_manager()
        events.event_attach(vlc.EventType.MediaPlayerStopped, my_callback, self.player) 
        events.event_attach(vlc.EventType.MediaPlayerBuffering, my_callback, self.player) 
        events.event_attach(vlc.EventType.MediaPlayerPlaying, my_callback, self.player) 
        events.event_attach(vlc.EventType.MediaPlayerEncounteredError, my_callback, self.player) 

    def do_play(self):
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
    stream_url = "http://ais-sa3.cdnstream1.com/2606_128.aac"
    
    info = StreamInfo(stream_url)
    info.get_info()
    
    player = StreamPlayer(stream_url)
    player.do_play()


if __name__ == "__main__":
    main()
