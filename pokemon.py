from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.image import AsyncImage
from kivymd.uix.list import MDList, ILeftBody, OneLineIconListItem, TwoLineListItem, IconLeftWidget, OneLineAvatarListItem, ImageLeftWidget
from kivymd.uix.button import MDRectangleFlatButton
import requests
import re


helper_text = '''
ScreenManager:
	Home:
	Profile:

<Home>:
	name: "home"
	BoxLayout:
		orientation:"vertical"
		MDToolbar:
		    title: "PokeDexTer"
		MDRectangleFlatButton:
		    text: "see charmandar"
		    pos_hint: {"center_x":.5, "center_y":.4}
		    on_release:
		    	app.profile_view_of("4")
		ScrollView:
			MDList:
				id: ls
<Profile>:
	name: "profile"
	BoxLayout:
		orientation:"vertical"
		MDToolbar:
			id: title_of_page
		    title: ""
		MDRectangleFlatButton:
		    text: "Back to home"
		    on_release:
		    	root.manager.current = "home"
		Image:
			id: image

		ScrollView:
			MDList:
				id: data
				TwoLineListItem:
					id: pokName
					text: "Name"
					secondary_text: ""

				TwoLineListItem:
					id: pokWeight
					text: "Weight"
					secondary_text: ""

				TwoLineListItem:
					id: pokHeight
					text: "Height"
					secondary_text: ""

				TwoLineListItem:
					id: pokType
					text: "Type"
					secondary_text: ""
'''

class AsyncImageLeftWidget(ILeftBody, AsyncImage):
    pass

class Home(Screen):
	pass

class Profile(Screen):
	pass
	
sm = ScreenManager()
sm.add_widget(Home(name="home"))
sm.add_widget(Profile(name="profile"))


class PokemonApp(MDApp):
	def build(self):
		screen = Screen()
		self.theme_cls.theme_style = "Light"
		self.hlpr_str = Builder.load_string(helper_text)
		screen.add_widget(self.hlpr_str)
		self.listpokemons()
		return screen
	def listpokemons(self):
		url = "https://pokeapi.co/api/v2/pokemon?limit=100"
		r = requests.get(url)
		for a in r.json()['results']:
			pokemon_no = a['url'].split("/")[-2]
			# https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/100.png
			image = AsyncImageLeftWidget(source=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon_no}.png')
			# image = AsyncImageLeftWidget(source=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_no}.png')
			listItem = OneLineAvatarListItem(text=a['name'], on_release=lambda x:self.profile_view_of(a['name'])) #, on_release=self.profile_view_of(a['name'])
			listItem.add_widget(image)
			self.hlpr_str.get_screen('home').ids.ls.add_widget(listItem)
	def profile_view_of(self, name):
		url = f"https://pokeapi.co/api/v2/pokemon/{name}"
		r = requests.get(url)
		data = r.json()
		print(data['sprites']['other']['official-artwork']['front_default'])
		best_image = AsyncImageLeftWidget(source=data['sprites']['other']['official-artwork']['front_default'], size_hint_x=1.8, pos_hint={"center_x":0.5, "center_y":0.7})
		self.hlpr_str.get_screen('profile').ids.image.add_widget(best_image)
		
		name = data['species']['name']
		weight = data['weight']
		height = data['height']
		pokemon_type = ""
		for a in data['types']:
			pokemon_type += f"{a['type']['name']} "
		

		self.hlpr_str.get_screen('profile').ids.pokName.secondary_text = name
		self.hlpr_str.get_screen('profile').ids.pokWeight.secondary_text = str(weight)
		self.hlpr_str.get_screen('profile').ids.pokHeight.secondary_text = str(height)
		self.hlpr_str.get_screen('profile').ids.pokType.secondary_text = pokemon_type


		self.hlpr_str.get_screen('profile').ids.title_of_page.title = name
		self.hlpr_str.get_screen('profile').manager.current = "profile"


PokemonApp().run()
