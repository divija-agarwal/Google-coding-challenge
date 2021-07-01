"""A video player class."""

from .video_library import VideoLibrary
import random
from enum import Enum
from .video_playlist import Playlist

class VideoPlayer:
    """A class used to represent a Video Player."""
    status = "inactive"
    paused = "no"
    def __init__(self):
        self._video_library = VideoLibrary()
        self.status = "inactive"
        self._paused = "no"
        self._list_playlist = []
        

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""

        print("Here's a list of all available videos:")
        list_of_video_objects = self._video_library.get_all_videos()
        list_of_video_ids = []
        for video_object in list_of_video_objects:
            list_of_video_ids.append(video_object._video_id)
        list_of_video_ids.sort()
        for video_id in list_of_video_ids:
            video = self._video_library.get_video(video_id)
            tags = str(video._tags)
            tags = tags[1:len(tags) - 1]
            tags = tags.replace("'", "")
            tags = tags.replace(",", "")

            print(video._title + " (" + video._video_id + ") [" + tags + "]")

           
           
    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        video = self._video_library.get_video(video_id)
        if (self.status == "active" and video != None):
            self.stop_video()
        if video == None:
            print("Cannot play video: Video does not exist")
        else:
            print("Playing video: " + video._title) 
            self.status = "active" 
            self._title = video._title
            self._video_id = video._video_id
            self.paused = "no"

    def stop_video(self):
        """Stops the current video."""
        if(self.status == "active"):
            print("Stopping video: " + self._title)
            self.status = "inactive"
        else:
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""
        if(self.status == "active"):
            print("Stopping video: " + self._title)
            self.status = "inactive"
        list_of_video_objects = self._video_library.get_all_videos()
        list_of_video_ids = []
        for video_object in list_of_video_objects:
            list_of_video_ids.append(video_object._video_id)
        random_id = random.choice(list_of_video_ids)
        video = self._video_library.get_video(random_id)
        print("Playing video: " + video._title) 
        self.status = "active" 
        self._title = video._title

    def pause_video(self):
        """Pauses the current video."""
        if(self.status == "active" and self.paused == "no"):
            print("Pausing video: " + self._title)
            self.paused = "yes"
        elif(self.status == "active" and self.paused == "yes"):
            print("Video already paused: " + self._title)
        else:
            print("Cannot pause video: No video is currently playing")

    def continue_video(self):
        """Resumes playing the current video."""
        if self.paused == "yes":
            print("Continuing video: " + self._title)
            self.paused = "no"
        elif self.status == "inactive":
            print("Cannot continue video: No video is currently playing")  
        else:
            print("Cannot continue video: Video is not paused") 


    def show_playing(self):
        """Displays video currently playing."""
        if self.status == "inactive":
            print("No video is currently playing")
        elif self.status == "active" and self.paused == "yes":
            video_id = self._video_id
            video = self._video_library.get_video(video_id)
            tags = str(video._tags)
            tags = tags[1:len(tags) - 1]
            tags = tags.replace("'", "")
            tags = tags.replace(",", "")
            print("Currently playing: " + video._title + " (" + video._video_id + ") [" + tags + "] - PAUSED")
        else:
            video_id = self._video_id
            video = self._video_library.get_video(video_id)
            tags = str(video._tags)
            tags = tags[1:len(tags) - 1]
            tags = tags.replace("'", "")
            tags = tags.replace(",", "")
            print("Currently playing: " + video._title + " (" + video._video_id + ") [" + tags + "]") 

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if len(self._list_playlist) == 0:
            self._list_playlist.append(Playlist(playlist_name))
            print(f"Successfully created new playlist: {playlist_name}")
        else:
            for playlist in self._list_playlist:
                if playlist_name.lower() == playlist.name.lower():
                    print("Cannot create playlist: A playlist with the same name already exists")
                else:
                    self._list_playlist.append(Playlist(playlist_name))
                    print(f"Successfully created new playlist: {playlist_name}")
                    break

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        temp = 0
        video = self._video_library.get_video(video_id)
        for playlist in self._list_playlist:
            if playlist_name.lower() == playlist.name.lower():
                temp = 1
                if video == None:
                    print("Cannot add video to " + playlist_name + ": Video does not exist added")
                elif playlist.find_video(video) == True:
                    print("Cannot add video to " + playlist_name + ": Video already added")
                else:
                    playlist.add_video(video)
                    print("Added video to " + playlist_name + ": " + video._title)
        if temp == 0:
            print("Cannot add video to " + playlist_name + ": Playlist does not exist")

    def show_all_playlists(self):
        """Display all playlists."""

        if len(self._list_playlist) == 0:
            print("No playlists exist yet")
        else:
            print("Showing all playlists:")
            self._list_playlist = sorted(self._list_playlist, key=lambda x: x.name)
            for playlist in self._list_playlist:
                print(playlist.name)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        temp = 0
        for playlist in self._list_playlist:
            if playlist_name.lower() == playlist.name.lower():
                temp = 1
                print(f"Showing playlist: {playlist_name}")
                if len(playlist.content) == 0:
                    print("No videos here yet")
                    
                else:
                    for video in playlist.content:
                        tags = str(video._tags)
                        tags = tags[1:len(tags) - 1]
                        tags = tags.replace("'", "")
                        tags = tags.replace(",", "")
                        print(video._title + " (" + video._video_id + ") [" + tags + "]")
            break

        if temp == 0:
            self._list_playlist.append(Playlist(playlist_name=playlist_name))
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")

                    

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        temp = 0
        video = self._video_library.get_video(video_id)
        for playlist in self._list_playlist:
            if playlist.name.lower() == playlist_name.lower():
                temp = 1
                if video == None:
                    print(f"Cannot remove video from {playlist_name}: Video does not exist")
                elif playlist.find_video(video) == False:
                    print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
                else:
                    playlist.remove_video(video)
                    print(f"Removed video from {playlist_name}: {video.title}")
        if(temp == 0):
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        temp = 0
        for playlist in self._list_playlist:
            if playlist.name.lower() == playlist_name.lower():
                temp = 1
                playlist.clear()
                print(f"Successfully removed all videos from {playlist_name}")
                break
        if(temp == 0):
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")


    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        temp = 0
        for playlist in self._list_playlist:
            if playlist.name.lower() == playlist_name.lower():
                temp = 1
                self._list_playlist.remove(playlist)
                print(f"Deleted playlist: {playlist_name}")
                break
        if(temp == 0):
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        print("search_videos needs implementation")

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        print("search_videos_tag needs implementation")

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        print("flag_video needs implementation")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        print("allow_video needs implementation")

