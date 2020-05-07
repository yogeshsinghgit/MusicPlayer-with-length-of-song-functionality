from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedStyle
from tkinter import filedialog,messagebox
import pygame
import os
from mutagen.mp3 import MP3
class MusicPlayer():
    def __init__(self, master):
        self.song_len = 100
        self.master = master
        self.i=1
        self.unmute = True
        self.stop = True
        self.unpause = True
        self.vol = 1.0
		# A debug variable 
        self.debug = False
        self.song_name = 'pata nahi.mp3'
        # default song path only for testing purpose ...
        self.path = filedialog.askdirectory(initialdir='/', title="Select a folder to play songs from")
        if self.debug:
            self.default_path = filedialog.askdirectory(initialdir='/', title="Select a default folder") 
        else:
            self.default_path = "/"
        self.tracks = []
        # initializing pygame constructor ....
        pygame.init()
        # Initiating Pygame Mixer
        pygame.mixer.init()
        self.widgets()

    def widgets(self):
        self.notebk = ttk.Notebook(self.master)
        self.notebk.pack()
        self.frame1 = Frame(self.notebk, width=400, height=200, relief=SUNKEN, bg='sky blue')
        self.frame2 = Frame(self.notebk, width=400, height=200, relief=SUNKEN, bg='sky blue')
        self.notebk.add(self.frame1, text='Music')
        self.notebk.add(self.frame2, text='List')

        # adding widgets in frame 1 ..or music frame ..

        self.song_info_frame = LabelFrame(self.frame1, text="Song Info .", relief=SUNKEN)
        self.song_info_frame.place(x=5, y=5, width=390, height=80)
        # initialised the image before creating buttons ..
        self.play = PhotoImage(file='play.png')
        self.pause = PhotoImage(file='pause.png')
        self.exit = PhotoImage(file='power-button.png')
        self.next = PhotoImage(file='advance.png')
        self.pre = PhotoImage(file='previous.png')
        self.open = PhotoImage(file='folder.png')
        self.mute = PhotoImage(file='mute.png')
        self.speaker = PhotoImage(file='speaker.png')
        self.stop_song = PhotoImage(file='square.png')

        previous_button = Button(self.frame1, image=self.pre, command=self.previous_song)
        previous_button.image = self.pre
        previous_button.place(x=40, y=100)

        self.play_button = Button(self.frame1, image=self.play, command=self.play_song)
        self.play_button.image = self.play
        self.play_button.place(x=100, y=100)

        next_button = Button(self.frame1, image=self.next, command= self.next_song)
        next_button.image = self.next
        next_button.place(x=160, y=100)

        pause_button = Button(self.frame1, image=self.pause, command=self.pause_song)
        pause_button.image = self.pause
        pause_button.place(x=220, y=100)

        self.mute_button = Button(self.frame1, image=self.mute, command=self.mute_song)
        self.mute_button.image = self.mute
        self.mute_button.place(x=280, y=100)

        self.volume_slider = Scale(self.frame1, length=100, orient=VERTICAL, from_=100, to=0, bg='sky blue',command=self.volumne_song)
        self.volume_slider.set(40)
        self.volume_slider.place(x=340, y=100)

        self.song_title = Label(self.song_info_frame, text=" Song name:")
        self.song_title.grid(row=0, column=0)

        self.total_length = Label(self.song_info_frame, text="Length:", )
        self.total_length.grid(row=0, column=1, padx=150)

        self.playing_time = Label(self.song_info_frame, text="00:00:00", font=('arial', 20, 'bold'))
        self.playing_time.grid(row=1, column=0, ipadx=10)

        self.list_frame = Frame(self.frame2, relief=SUNKEN)
        self.list_frame.place(x=130, y=5)

        # Inserting scrollbar
        scrol_y = Scrollbar(self.list_frame, orient=VERTICAL)
        # Inserting Playlist listbox

        self.song_list = Listbox(self.list_frame, width=30, height=10, bd=3, font=('arial', 11), yscrollcommand=scrol_y.set)

        # Applying Scrollbar to listbox
        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_y.config(command=self.song_list.yview)
        self.song_list.pack(fill=BOTH)
        self.open_song_list()

        self.open_button = Button(self.frame2, image=self.open, command=self.open_folder)
        self.open_button.image = self.open
        self.open_button.place(x=15, y=30)

        self.play_button_list = Button(self.frame2, image=self.play, command=self.play_from_list)
        self.play_button_list.image = self.play
        self.play_button_list.place(x=15, y=80)

        self.exit_button = Button(self.frame2, image=self.exit, command=root.destroy)
        self.exit_button.image = self.exit
        self.exit_button.place(x=15, y=130)

    def play_song(self):
        if(self.stop):
            self.stop = False
            self.play_button.configure(image=self.stop_song)
            pygame.mixer.music.load(self.tracks[self.i])
            self.current_position_of_song()
            self.song_title['text']=" Song name: "+str(self.tracks[self.i])
            self.song_length(self.tracks[self.i])
            pygame.mixer.music.play()
            self.i += 1
            pygame.mixer.music.queue(self.tracks[self.i])
        else:
            self.stop = True
            self.play_button.configure(image=self.play)
            pygame.mixer.music.stop()

    def current_position_of_song(self):
        current_pos = pygame.mixer.music.get_pos() # returns song in milliseconds ..
        current_pos = int(current_pos * 0.001)
        h,m,s = self.convert(current_pos)
        self.playing_time['text'] = str(h)+":"+str(m)+":"+str(s)
        self.master.after(1000,self.current_position_of_song)

    def pause_song(self):
        if(self.unpause):
            pygame.mixer.music.pause()
            self.unpause = False
        else:
            pygame.mixer.music.unpause()
            self.unpause = True

    def next_song(self):
        self.i+=1
        try:
            self.stop = True
            self.play_song()
        except:
            self.i=0
            self.stop = True
            pygame.mixer.music.play()

    def previous_song(self):
        self.i-=1
        try:
            self.stop = True
            self.play_song()
        except:
            self.stop = True
            self.i =0
            self.play_song()

    def open_folder(self):
        self.path = filedialog.askdirectory()
        #print(self.path)
        self.open_song_list()

    def open_song_list(self):
        if self.path =="":
            self.path = self.default_path
        os.chdir(self.path)
        for song in os.listdir(self.path):
            if song.endswith('.mp3'):
                self.song_list.insert(END, song)
                self.tracks.append(song)

    def mute_song(self):
        if(self.unmute):
            self.vol = pygame.mixer.music.get_volume()
            pygame.mixer.music.set_volume(0)
            #self.mute_button.image = self.speaker
            self.mute_button.configure(image=self.speaker)
            self.unmute= False
        else:
            pygame.mixer.music.set_volume(self.vol)
            self.mute_button.configure(image=self.mute)
            self.unmute = True

    def volumne_song(self,val):
        pygame.mixer.music.set_volume(int(self.volume_slider.get()) / 100)

    def song_length(self,file):
        # function to convert the seconds into readable format
        # Create an MP3 object
        # Specify the directory address to the mp3 file as a parameter
        audio = MP3(file)
        # Contains all the metadata about the mp3 file
        audio_info = audio.info
        length_in_secs = int(audio_info.length)
        hours, mins, seconds = self.convert(length_in_secs)
        # chnaging total length text ...
        self.total_length['text'] = "Length:"+str(hours)+":" +str(mins)+":"+str(seconds)

    def convert(self,seconds):
        hours = seconds // 3600
        seconds %= 3600
        mins = seconds // 60
        seconds %= 60
        return hours, mins, seconds

    def play_from_list(self):
        # returns a tuple.
        selected_track = self.song_list.curselection()
        self.i = selected_track[0]
        self.play_song()

if __name__ == '__main__':
    root = Tk()
    style = ThemedStyle(root)
    style.set_theme("scidblue")  #Radiance . #Arc
    MusicPlayer(root)
    root.geometry('405x230+300+250')
    root.configure(background='blue')
    #icon = PhotoImage(file='D:\\OFER\\Python\\MusicPlayer-with-length-of-song-functionality\\icon.png')
    #root.iconphoto(False,icon)
    root.resizable(0,0)
    root.title('Music Player')
    root.mainloop()
