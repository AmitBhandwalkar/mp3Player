import eyed3
from pygame import mixer
from mutagen.mp3 import MP3
import time

# song class
class Song:
  # volume
  volume = 0.5
   # Starting the mixer
  mixer.init()

  def __init__(self,song_file,title):
      self.filepath = song_file
      self.title = title
      #convert into mutagen.mp3 for time
      audio = MP3(song_file)
      self.length = audio.info.length
      self.time = time.strftime('%H:%M:%S',time.gmtime(self.length))
      if self.title == None:
        self.title = "song-1"
        self.status = None 
      try:
         # convert into eyed3 audio file
         audiofile = eyed3.load(song_file)
         self.artist = audiofile.tag.artist
         self.album = audiofile.tag.album
      except: 
        self.artist = "-"
        self.album = "-"

       #play Song
  def play(self,start=0): 
  # Loading the song
   mixer.music.load(self.filepath)
  # Start playing the song
   mixer.music.play(loops=0, start=start)   
   self.status = 'play'

    #increase Volume of song
  @staticmethod
  def increaseVolume():
    Song.volume += 0.2
    mixer.music.set_volume(Song.volume)
  
   #decrease Volume of song
  @staticmethod
  def decreaseVolume():
    Song.volume -= 0.2
    mixer.music.set_volume(Song.volume)
  
   # Stop Song
  def stop(self):
     self.status = 'stop'
     mixer.music.stop()

  # Pausing the music
  def pause(self):
        self.status = 'pause'
        mixer.music.pause()

   # UnPausing the music
  def unpause(self):
        self.status = 'unpause'
        mixer.music.unpause()
    # restart song
  def rewind(self):
    self.status = 'rewind'  
    mixer.music.stop()
    mixer.music.play()
   # change status
  def  changeStatus(self,status):
      self.status = status





 # for test
if __name__ == "__main__":
   audio_file = eyed3.load("02 All We Know (feat. Phoebe Ryan).mp3")
   album_name = audio_file.tag.album
   artist_name = audio_file.tag.artist
   for image in audio_file.tag.images:
     print(image)