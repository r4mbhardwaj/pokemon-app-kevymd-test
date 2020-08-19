from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.image import AsyncImage
from kivymd.uix.list import MDList, OneLineIconListItem, TwoLineListItem, IconLeftWidget, OneLineAvatarListItem, ImageLeftWidget
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



'''

toolbar_text = """

"""

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
        self.profile_now = ''
        return screen
    def listpokemons(self):
    	url = "https://pokeapi.co/api/v2/pokemon?limit=10"
    	r = requests.get(url)
    	for a in r.json()['results']:
    		no = a['url'].split("/")[-2]
    		btn = MDRectangleFlatButton(text=f"see {a['name']}", on_press=lambda x:self.profile_view_of(no))
    		image = AsyncImage(source=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{no}.png')
    		# icon_ = IconLeftWidget(icon="language-python")
    		listItem = OneLineAvatarListItem(text=a['name']) #, on_release=self.profile_view_of(a['name'])
    		listItem.add_widget(image)
    		listItem.add_widget(btn)
    		self.hlpr_str.get_screen('home').ids.ls.add_widget(listItem)
    def profile_view_of(self, no):
    	if self.profile_now != no:
    		self.profile_now == no
	    	url = f"https://pokeapi.co/api/v2/pokemon/{no}"
	    	print(url)
	    	r = requests.get(url)
	    	data = r.json()
	    	best_image = AsyncImage(source=data['sprites']['other']['official-artwork']['front_default'], size_hint_x=1.8, pos_hint={"center_x":0.5, "center_y":0.7})
	    	self.hlpr_str.get_screen('profile').ids.image.add_widget(best_image)
	    	name = data['species']['name']
	    	weight = data['weight']
	    	height = data['height']
	    	pokemon_type = ""
	    	for a in data['types']:
	    		pokemon_type += f"{a['type']['name']} "
	    		factors = {"name":name, "weight":weight, "height":height, 'type':pokemon_type}
	    	for f in factors:
	    		item = TwoLineListItem(text=f, secondary_text=str(factors[f]))
	    		self.hlpr_str.get_screen('profile').ids.data.add_widget(item)


	    	self.hlpr_str.get_screen('profile').ids.title_of_page.title = name
    	self.hlpr_str.get_screen('profile').manager.current = "profile"

PokemonApp().run()
