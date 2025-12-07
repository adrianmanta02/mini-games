import pygame
import os
from os.path import join

class DamageableEntity:
	# class-level cache for loaded sounds to avoid reloading
	sound_cache = {}
	
	def __init__(self, damage_sound_file: str, cooldown_frames: int = 30):
		self.damage_sound = self._load_damage_sound(damage_sound_file)
		self.damage_cooldown = 0
		self.cooldown_frames = cooldown_frames
	
	def _load_damage_sound(self, soundname: str) -> pygame.mixer.Sound:
		# loads damage sound from assets/sound directory with caching
		
		# check if sound is already in cache
		if soundname in DamageableEntity.sound_cache:
			return DamageableEntity.sound_cache[soundname]
		
		# Load sound and add to cache
		BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
		path_to_damage_sound = join(BASE_DIRECTORY, "..", "..", "..", "assets", "Sound", soundname)
		sound = pygame.mixer.Sound(path_to_damage_sound)
		sound.set_volume(0.5)  
		DamageableEntity.sound_cache[soundname] = sound
		return sound
	
	def update_damage_cooldown(self):
		if self.damage_cooldown > 0:
			self.damage_cooldown -= 1
	
	def apply_damage(self, player) -> bool:
		if self.damage_cooldown == 0:
			self.damage_sound.play()
			player.hit()
			self.damage_cooldown = self.cooldown_frames
			return True
		return False
	
	def handle_player_damage(self, player, collision_check):
		if collision_check and self.damage_cooldown == 0:
			self.apply_damage(player)
