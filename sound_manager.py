import pygame

   # all audio used throughout is managed here
class SoundManager:
    def __init__(self):
       
        
        pygame.mixer.init()
        self.sounds = {}
        self.background_music = None
        self.background_playing = False
        
       
        self.laodingSound()
    
    def laodingSound(self):
       
        sound_files = {
            "coin": "sounds/coin.mp3",
            "fire": "sounds/gunshot.mp3",    
        }
        
           # looping through the sound files to load each sound file
        for sound_name, sound_path in sound_files.items():
            self.sounds[sound_name] = pygame.mixer.Sound(sound_path)
            
        
        
        
        self.background_music = pygame.mixer.Sound("sounds/background.mp3")
           
        
        self.background_music.set_volume(0.5)  
      
    
    def soundplaying(self, sound_name):
           # checks if the requested sound actually exists in self.sounds.
        if sound_name in self.sounds and self.sounds[sound_name]:
            pygame.mixer.Sound.play(self.sounds[sound_name])
    
    def bgmusic(self):
        
       
        self.background_music.play(-1) 
        self.background_playing = True
    
    
    
   
    
