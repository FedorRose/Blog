from kivy.network.urlrequest import UrlRequest
from kivy.uix.screenmanager import Screen
from kivy.utils import get_color_from_hex, rgba
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.fitimage import FitImage
from kivymd.uix.label import MDLabel
from kivymd.uix.navigationdrawer import MDNavigationLayout, MDNavigationDrawer
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDToolbar

KV = '''
#:import SliverToolbar __main__.SliverToolbar
#:import get_color_from_hex kivy.utils.get_color_from_hex


<CardItem>
    size_hint_y: None
    height: "286dp"
    padding: "4dp"
    radius: 12
    elevation: 4
    on_press: self.single()

    MDRelativeLayout:
        height: "278dp"
        orientation: "vertical"
        adaptive_height: True
        spacing: "6dp"
        # padding: "12dp", 0, 0, 0
        # pos_hint: {"center_y": .5}

        FitImage:
            id: photo
            # source: "avatar.jpg"
            radius: root.radius
            # height: root.height
            width: root.height

        MDLabel:
            id: tt
            color: get_color_from_hex("ffffff")
            text: root.title
            font_style: "H6"
            bold: True
            adaptive_height: True
            halign: 'center'
            pos_hint: {"center_y": .3}


        MDLabel:
            id: cat
            text: root.cat
            color: get_color_from_hex("ffffff")
            adaptive_height: True
            halign: 'center'
            pos_hint: {"center_y": .4}
            
        MDLabel:
            id: st
            text: root.subtitle
            color: get_color_from_hex("ffffff")
            adaptive_height: True
            halign: 'center'
            pos_hint: {"center_y": .1}

MDScreen:

    MDSliverAppbar:
        background_color: get_color_from_hex("808080")       
        toolbar_cls: SliverToolbar()           

        MDSliverAppbarHeader:
            
            MDRelativeLayout:  
                FitImage:
                    source: "bg.jpg"                    
                             
        MDSliverAppbarContent:
            id: content
            orientation: "vertical"
            padding: "12dp"
            spacing: "12dp"
            adaptive_height: True
'''


class CardItem(MDCard, RoundedRectangularElevationBehavior):
    title = ' '
    cat = ' '
    subtitle = ' '
    pk = None
    photo = None

    def __init__(self, t, c, s, pk, ph):
        super(CardItem, self).__init__()
        self.ids.tt.text = t
        self.ids.st.text = s
        self.ids.cat.text = c
        self.ids.photo.source = ph
        self.title = t
        self.pk = pk
        self.cat = c
        self.subtitle = s
        self.photo = ph

    def single(self):
        print("single done!", self.pk, self.title)


class SliverToolbar(MDToolbar):
    cat = None

    def __init__(self, **kwargs):
        cats = None
        super().__init__(**kwargs)
        self.type_height = "medium"
        self.headline_text = "Magazine"
        UrlRequest('http://127.0.0.1:8000/api/v1/cats/',
                   on_success=self.fill_cats)

    def fill_cats(self, *args, **kwargs):
        self.cats = args[1]
        self.lay = MDBoxLayout()
        for cat in self.cats:
            slug = cat['slug']
            name = cat['name']
            self.lay.add_widget(MDLabel(text="[color=ffffff][size=15][ref="+slug+"]"+name+"[/ref]", markup=True,
                                        on_ref_press=self.pr))
        self.add_widget(self.lay)
        print(self.cats)

    def pr(self, *args, **kwargs):
        self.cat = args[1]
        UrlRequest('http://127.0.0.1:8000/api/v1/post/',
                    on_success=self.fill_board)

    def fill_board(self, cat, *args):
        collect = args[0]
        new_collect=[]
        print(collect)
        cat_id = None
        cat_name = None
        for i in self.cats:
            if self.cat == i['slug']:
                cat_id = i['id']
                cat_name = i['name']
        # print(cat_id)
        for i in collect:
            if i['cat'] == cat_id:
                new_collect.append(i)
        # print(new_collect)
        self.fill_new(collect=new_collect, cat=cat_id, cat_name=cat_name)

    def fill_new(self, collect, cat, cat_name):
        cats = [{'id': cat, 'name': cat_name}]
        print('fill_new1', collect, cats)

        Main.fill_content(Main(), 0, cats, kwargs=collect)
        # for i in collect:
        #     title = (i['title'])
        #     subtitle = (i['subtitle'])
        #     pk = (i['id'])
        #     ph = (i['photo'])
        #     self.root.ids.content.add_widget(CardItem(t=title, c=cat, s=subtitle, pk=pk, ph=ph))


class Main(MDApp):
    cats = None
    # rootC = None

    def __init__(self):
        super(Main, self).__init__()
        self.rootC = self.root
        print("rootC:::", self.rootC)

    def build(self):
        self.theme_cls.material_style = "M3"
        return Builder.load_string(KV)

    def posts(self):
        return UrlRequest('http://127.0.0.1:8000/api/v1/post/',
                          on_success=self.fill_board,
                          on_failure=self.fill_board)

    def fill_board(self, *args):
        self.collect = args[1]
        UrlRequest('http://127.0.0.1:8000/api/v1/cats/',
                   on_success=self.fill_content)

    def fill_content(self, *args, **kwargs):
        print("filcont", args, args[1], kwargs)
        self.cats = args[1]
        if kwargs:
            self.collect = kwargs['kwargs']
            print("kwargs: root1 =", self.rootC)
        for i in self.collect:
            title = (i['title'])
            cat = ''
            for j in range(len(self.cats)):
                if i['cat'] == self.cats[j]['id']:
                    cat = self.cats[j]['name']
            subtitle = (i['subtitle'])
            pk = (i['id'])
            ph = (i['photo'])
            self.root.ids.content.add_widget(CardItem(t=title, c=cat, s=subtitle, pk=pk, ph=ph))
            print("root2:", self.root)


    # def fill_new(self, collect, cat):
    #     self.root.ids.content.clear()
    #     for i in collect:
    #         title = (i['title'])
    #         subtitle = (i['subtitle'])
    #         pk = (i['id'])
    #         ph = (i['photo'])
    #         self.root.add_widget(MDScreen())
    #         self.root.ids.content.add_widget(CardItem(t=title, c=cat, s=subtitle, pk=pk, ph=ph))

    def on_start(self):
        self.posts()


if __name__ == "__main__":
    Main().run()
