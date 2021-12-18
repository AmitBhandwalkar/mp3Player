from pygame import mixer
import pygame  

 

         
#   # Loading the song
  
#   # Start playing the song
       

    



# for test
if __name__ == "__main__":
    playList = []
    playList.append("Rome.mp3")
    playList.append("Speakerbox.mp3")

    pygame.mixer.init() 
    pygame.mixer.music.load(playList[0])
    pygame.mixer.music.play()
    

    x = 1
    while x != 3 :
         if pygame.mixer.music.get_busy():
           pass
         else :
           print("Song is finshed")
           x = 3

