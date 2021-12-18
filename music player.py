from logging import exception
from os import remove
from tkinter import *
from tkinter.filedialog import askopenfile, askopenfiles
from tkinter import ttk
import sqlite3
from song import Song
import eyed3, io
from PIL import Image,ImageTk
import pygame
import time
from tkinter import filedialog



                                #-define functions-#

   ## define global variable

#Current songs play list (song list box)
play_list = []
#Current play song
global playing_song 
playing_song = None
global playing_song_index 
global next_song_index
next_song_index = None


        # functions for database opertions Start #

# load Current Play List
def loadCurrentPlayList():
    #Create a database or connect to one
    conn = sqlite3.connect('play_list.db')



         # functions for database opertions End #



         # functions for top menubar start #

# function for add song to play List
def addSong():
    try:
        song_file = filedialog.askopenfilename(title="Choose A Song",filetypes =[('mp3 Files', '*.mp3')])
        x = song_file.rfind('/')+1
        song_name = song_file[x:len(song_file)]
        song = Song(song_file,song_name)
        play_list.append(song)
        songs_listBox.insert(END,song_name)
    except Exception as e:
      pass      
     # print(e)

# functions for add many songs to play List
def addManySongs():
    try:
        song_files = filedialog.askopenfilenames(title="Choose A Song",filetypes =[('mp3 Files', '*.mp3')])
        for song_file in song_files:
             x = song_file.rfind('/')+1
             song_name = song_file[x:len(song_file)]  
             song = Song(song_file,song_name)
             play_list.append(song)
             songs_listBox.insert(END,song_name)   
    except:
        pass  #no song selected


        # functions for top menubar End #


        # update functions Start #



#update song title heading
def updateSonginfo(song):
    if len(song.title) < 43:
      song_title.config(text=song.title)
    else:
        str1 = song.title[:43]
        str2 = song.title[43:len(song.title)]
        song_title.config(text=f'{str1} \n {str2}')
    song_info.config(text=f'Artist:{song.artist}   ||   Album:{song.album}')
    slider_lable2.config(text=song.time)
      # active bar in playlist
    songs_listBox.select_clear(0,END)
    songs_listBox.activate(playing_song_index)
    songs_listBox.itemconfig(playing_song_index, {'fg': 'blue'})
# update song Image
def updateImage(song_file):
    file = eyed3.load(song_file)
    try:
     #Load an image in the script
     img= (Image.open(io.BytesIO(file.tag.images[0].image_data)))
     #Resize the Image using resize method
     resized_image= img.resize((300,205), Image.ANTIALIAS)
     new_image= ImageTk.PhotoImage(resized_image)
     #Add image to the lable
     song_image.configure(image=new_image)
     song_image.image=new_image
    except:
      pass #not image in song file


# grab Song Length Time Info
def playTime():
           global pt_loop
           global next_song_index   
           current_time = pygame.mixer.music.get_pos() / 1000

           if int(my_slider.get()) == int(playing_song.length):
               #Song End
               if next_song_index != None:
                 playSong(next_song_index)
                 next_song_index = None
               else:  
                playNextSong() 
           elif playing_song.status == 'pause':
             # song is pause
             pass  
           else:
            if int(my_slider.get()) == int(current_time):
                     # slider hasn`t been moved
                # update slider To position     
                slider_postion = int(playing_song.length)
                my_slider.config(to=slider_postion,value=int(current_time))
            else:
                    # slider has been moved
                # update slider To position     
               slider_postion = int(playing_song.length)
               my_slider.config(to=slider_postion,value=int(my_slider.get()))  
                 # convert into time formate
               time_formt = time.strftime('%H:%M:%S',time.gmtime(int(my_slider.get())))
                 # update slider left label
               slider_lable1.config(text=str(time_formt))
               next_time = int(my_slider.get()) + 1
               my_slider.config(value=next_time)
         
           # call function after 1 second
           pt_loop  = my_slider.after(1000,playTime)

              
# update song postion on slider postion
def slider(x):
    global pt_loop
    try:
       xc = int(my_slider.get())
       playing_song.play(xc)    
    except:
        pass

# update volume Slider postion on slider
def volumeSlider(s):
  try:
       volume = int(volume_slider.get()) 
       v = volume/100
       pygame.mixer.music.set_volume(v)
       volume_lable2.config(text=volume)  
  except:
        pass 
     
        # update functions End #

# function for play song and update time ,song info
def playSong(index):
    global playing_song
    global playing_song_index
    global pt_loop
    # check song is plying or not
    if playing_song != None:
       # Stop playtTime Loop
       my_slider.after_cancel(pt_loop) 
    playing_song_index = index
    playing_song = play_list[index]
    playing_song.play()
     #update song title and image
    updateSonginfo(playing_song)
    updateImage(playing_song.filepath)
     # update slider To position
    my_slider.config(to=playing_song.length,value=0)
     # call play function for update silder check song end
    playTime()
    # # update slider To position
    #  slider_postion = int(playing_song.length)
    #  my_slider.config(to=slider_postion,value=0)




       # list box functions Start #

# function for play song In playlist on    'double click'
def playSongDoubleClick(event):
     global playing_song_index
     try:
      # get tuple form curselection
      song_name = songs_listBox.curselection()
      index = song_name[0]
        # change old song background color
      songs_listBox.itemconfig(playing_song_index, {'fg': 'black'})
      playSong(index)
     except Exception as e:
       #print("exc->",e)
       # if no song playing
       # get tuple form curselection
       song_name = songs_listBox.curselection()
       index = song_name[0]
        # change old song background color
       playSong(index)

# Right click on song in list Menu functions
def menuPopRightClick(event):
           songs_listBox.selection_clear(0,END)
           song_left_select = songs_listBox.nearest(event.y)
           if song_left_select != -1:
                songs_listBox.selection_set(song_left_select)
                songs_listBox.activate(song_left_select)
                song_right_menu.tk_popup(event.x_root, event.y_root)
                song_right_menu.grab_release()  

# function for remove song form list box
def removeSongListbox():
       try:
        global playing_song_index
        song_name = songs_listBox.curselection()
        index = song_name[0]  
        del play_list[index] 
        songs_listBox.delete(index)
        if index < playing_song_index:
          playing_song_index -=1
        print(playing_song_index)
       except Exception as e:
        pass
    
#function for play song in listbox
def playSongListbox():
            global playing_song_index
            song_name = songs_listBox.curselection()
            index = song_name[0]
            try:
             # change old song background color
             songs_listBox.itemconfig(playing_song_index, {'fg': 'black'})
             playSong(index)
            except Exception as e:
              playSong(index)  

#function for add song in nextSong
def playNextSongListbox():
      global next_song_index
      global playing_song
      try: 
          song_name = songs_listBox.curselection()  
          if playing_song == None:
            playSong(song_name[0])
          else:  
            next_song_index  = song_name[0]
      except:
            pass 


      # list box functions End #


      # Button functions start #
 
 # Function for pause Song
def pauseSong():
    try:
      playing_song.pause()
    except:
        # song not playing
        pass

#function for Play song on 'click on play button'
def playSongPlayButton():
   try:
     #playing_song exit
    if playing_song.status == 'pause':
      # song is pause
      playing_song.unpause()
    else:
      pass   
   except:
     if len(play_list) > 0:
       # play first song in play list
       playSong(0)

#Functions for rewind song
def rewindSong():
    global playing_song_index
    global playing_song
    try:
      playSong(playing_song_index)
    except:
        pass
      #  print("no plyin song")


      # Button functions End #


#Function for play next Song on button click
def playNextSong():
    global playing_song_index
    global playing_song
    try:
     index = playing_song_index
     psl = len(play_list)-1
     if index < psl:
         index += 1 
           # change old song background color
         songs_listBox.itemconfig(playing_song_index, {'fg': 'black'})
         playSong(index)
    except:
        pass
     #   print("no playing song")

#Function for play back Song
def playBackSong():
    global playing_song_index
    global playing_song
    try:
     index = playing_song_index
     if index > 0:
         index -= 1
           # change old song background color
         songs_listBox.itemconfig(playing_song_index, {'fg': 'black'})
         playSong(index)
    except:
        pass
     #   print("no playing song")






                                ##-create Gui-##






    # load Current playing List in Datbase#
loadCurrentPlayList()



#creating window
window = Tk()
window.geometry('850x750')
#set Title and title icon
window.title("Music Player")
window.iconbitmap('icons/music_title_icon.ico')




               ## Top Menu Bar start

# Creating Top Menubar
top_menubar = Menu(window)

#add Song Submenu 
add_song_menu = Menu(top_menubar,tearoff=0)
top_menubar.add_cascade(label="Add Song",menu=add_song_menu)
add_song_menu.add_command(label="add One Song play list",command=addSong)
add_song_menu.add_command(label="add Many Songa play list",command=addManySongs)

#display Top Menu Bar
window.config(menu = top_menubar)
  
                ## Top Menu Bar End
  
     ## Left side Frame start
  
font = ('Verdana',15)
font1 = ('Verdana',12)
  
# right click on song in list Menu
song_right_menu = Menu(window,tearoff=0)
song_right_menu.add_command(label="remove",command=removeSongListbox)
song_right_menu.add_command(label="play",command=playSongListbox)
song_right_menu.add_command(label="Next play",command=playNextSongListbox)
# right_menu.add_command(label="add playlist")


# create left frame
left_frame = Frame(window,relief=SUNKEN)
left_frame.pack(side=LEFT,fill="y")
# list box label(title)
songs_listBox_label = Label(left_frame,text="play List")
songs_listBox_label.pack(side=TOP, anchor=NW,padx=90)
# create list box for play list songs
songs_listBox = Listbox(left_frame,height=40,width=45)
#blind functiond for play Song Double on Click
songs_listBox.bind('<Double-1>',playSongDoubleClick)
songs_listBox.bind('<Button-3>',menuPopRightClick)
songs_listBox.pack()



    ## Left side Frame End


    ## right side frame Start

right_frame = Frame(window,relief=SUNKEN)
right_frame.pack(side=TOP,fill=X,pady=50)

pic = PhotoImage(file='icons/icon.png')
song_image = Label(right_frame,image=pic)
song_image.pack(side=TOP) 

song_title = Label(right_frame,text="",font=font,justify="center")
song_title.pack(pady=5,padx=20)

song_info =Label(right_frame,text="Artist:      Album:",font=font1)
song_info.pack(pady=20)

# buttonframe pack with right frame
buttonFrame = Frame(right_frame)
buttonFrame.pack(side=TOP,pady=20)

#Play / unpause Button
playImage = PhotoImage(file='icons/playicon.png')
playBtn = Button(buttonFrame,font=font,text='stop',width=50,relief='ridge',activebackground='red' ,image=playImage,command=playSongPlayButton)
playBtn.grid(row=0,column=0,padx=5)

#pause Button
stopImage = PhotoImage(file='icons/stopIcon.png')
stopBtn = Button(buttonFrame,font=font,text='stop',width=50,relief='ridge',activebackground='red' ,image=stopImage,command=pauseSong)
stopBtn.grid(row=0,column=1,padx=5)

#rewind Button
rewindImage = PhotoImage(file='icons/rewindicon.png')
rewindBtn = Button(buttonFrame,font=font,text='stop',width=50,height=65,relief='ridge',activebackground='red' ,image=rewindImage,command=rewindSong)
rewindBtn.grid(row=0,column=2,padx=5)

#next Song Button
nextImage = PhotoImage(file='icons/next.png')
nextBtn = Button(buttonFrame,font=font,text='stop',width=50,height=65,relief='ridge',activebackground='red' ,image=nextImage,command=playNextSong)
nextBtn.grid(row=0,column=3,padx=5)

#back Song Button
backImage = PhotoImage(file='icons/back.png')
backBtn = Button(buttonFrame,font=font,text='stop',width=50,height=65,relief='ridge',activebackground='red' ,image=backImage,command=playBackSong)
backBtn.grid(row=0,column=4,padx=5)


#create silder frame
silder_frame = Frame(right_frame)
silder_frame.pack(side=TOP,pady=10)

#create staring time label
slider_lable1 = Label(silder_frame,text='0')
slider_lable1.grid(row=0,column=0,padx=5)

#Create Music Position slider
my_slider = ttk.Scale(silder_frame,from_=0,to=100,orient=HORIZONTAL,value=0,length=360,command=slider)
my_slider.grid(row=0,column=4,padx=5)

#create time  start for end
slider_lable2 = Label(silder_frame,text='00:00:00')
slider_lable2.grid(row=0,column=6,padx=5)


#create volume frame
volume_frame = Frame(right_frame)
volume_frame.pack(side=RIGHT,pady=0)
#create volumelabel
volume_lable1 = Label(volume_frame,text='Volume')
volume_lable1.grid(row=0,column=0,padx=5)
#Create volume Position slider
volume_slider = ttk.Scale(volume_frame,from_=0,to=100,orient=HORIZONTAL,value=50,length=100,command=volumeSlider)
volume_slider.grid(row=0,column=4,padx=5)
#create time  start for end
volume_lable2 = Label(volume_frame,text='50')
volume_lable2.grid(row=0,column=6,padx=5)





  ## right side frame End








       
       

       # main loop #
window.mainloop()