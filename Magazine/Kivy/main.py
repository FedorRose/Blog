import json
from kivy.network.urlrequest import UrlRequest
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex, rgba
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRoundFlatIconButton, MDRoundFlatButton, MDFillRoundFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.fitimage import FitImage
from kivymd.uix.label import MDLabel
from kivymd.uix.navigationdrawer import MDNavigationLayout, MDNavigationDrawer
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.sliverappbar import MDSliverAppbar, MDSliverAppbarHeader, MDSliverAppbarContent
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar import MDToolbar
from kivy.uix.button import Button
from kivy.uix.slider import Slider

KV = '''
#:import SliverToolbar __main__.SliverToolbar
#:import get_color_from_hex kivy.utils.get_color_from_hex

<CardItem>
    size_hint_y: None
    height: "286dp"
    padding: "4dp"
    radius: 12
    elevation: 4
    # on_press: self.single()

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

'''


class Main(MDApp):
    content_list = []
    text_comm_name, text_comm_last, text_comm_mess = '', '', ''

    def __init__(self):
        super(Main, self).__init__()
        self.root = MDScreen()
        self.sl = MDSliverAppbar(background_color=get_color_from_hex("808080"))
        self.head = MDSliverAppbarHeader()
        self.tool = SliverToolbar()
        self.sl.toolbar_cls = self.tool
        self.rel = MDRelativeLayout()
        self.content = MDSliverAppbarContent(orientation="vertical", padding="12dp", spacing="12dp",
                                             adaptive_height=True)

    def posts(self, *args):
        return UrlRequest('http://magazinefkolo.pythonanywhere.com/api/v1/post/',
                          on_success=self.fill_board,
                          on_failure=self.fill_board)

    def fill_board(self, *args):
        self.collect = args[1]
        UrlRequest('http://magazinefkolo.pythonanywhere.com/api/v1/cats/',
                   on_success=self.fill_content)

    def fill_content(self, *args, **kwargs):
        self.content.clear_widgets()
        self.cats = args[1]
        self.fill_cats()
        for i in self.collect:
            title = (i['title'])
            cat = ''
            for j in range(len(self.cats)):
                if i['cat'] == self.cats[j]['id']:
                    cat = self.cats[j]['name']
            subtitle = (i['subtitle'])
            pk = (i['id'])
            ph = (i['photo'])
            card = CardItem(t=title, c=cat, s=subtitle, pk=pk, ph=ph)
            self.content_list.append(card)
            self.content.add_widget(card)
        self.kk()

    def kk(self):
        for el in self.content_list:
            el.bind(on_press=self.single)

    def fill_cats(self, *args, **kwargs):
        self.tool.clear_widgets()
        self.tool.height = "90dp"
        self.tool.add_widget(MDLabel(text="[ref=home][color=ffffff][size=20]Magazine[/ref]", markup=True,
                                     on_ref_press=self.posts))
        lay = MDBoxLayout()
        for cat in self.cats:
            slug = cat['slug']
            name = cat['name']
            lay.add_widget(MDLabel(text="[color=ffffff][size=15][ref="+slug+"]"+name+"[/ref]", markup=True,
                                   on_ref_press=self.pr))
        self.tool.add_widget(lay)

    def pr(self, *args, **kwargs):
        self.cat = args[1]
        UrlRequest('http://magazinefkolo.pythonanywhere.com/api/v1/post/',
                   on_success=self.fill_board_2)

    def fill_board_2(self, cat, *args):
        collect, new_collect = args[0], []
        cat_id, cat_name = None, None
        for i in self.cats:
            if self.cat == i['slug']:
                cat_id = i['id']
                cat_name = i['name']
        # print(cat_id)
        for i in collect:
            if i['cat'] == cat_id:
                new_collect.append(i)
        self.fill_new(collect=new_collect, cat=cat_id, cat_name=cat_name)

    def fill_new(self, collect, cat, cat_name):
        self.content.clear_widgets()
        for i in collect:
            title = (i['title'])
            subtitle = (i['subtitle'])
            pk = (i['id'])
            ph = (i['photo'])
            card = CardItem(t=title, c=cat_name, s=subtitle, pk=pk, ph=ph)
            card.bind(on_press=self.single)
            self.content.add_widget(card)

    def single(self, *args):
        # print("args:", args)
        if len(args) > 1:
            self.pks = args[1]['post']
        else:
            self.pks = args[0].pk
        UrlRequest('http://magazinefkolo.pythonanywhere.com/api/v1/post/{}/'.format(self.pks),
                   on_success=self.comm)

    def comm(self, *args):
        self.post = args[1]
        UrlRequest('http://magazinefkolo.pythonanywhere.com/api/v1/comment/post/{}/'.format(self.pks),
                   on_success=self.fill_single,
                   on_failure=self.fill_single)

    def fill_single(self, *args):
        self.content.clear_widgets()
        post = self.post

        fi = FitImage(source=post['photo'], radius=12)
        rel = MDRelativeLayout(height="278dp", size_hint_y=None, orientation="vertical", adaptive_height=True)
        rel3 = MDRelativeLayout(height="478dp", size_hint_y=None, orientation="vertical", adaptive_height=True)
        rel2 = MDBoxLayout(height="100dp", adaptive_height=True, size_hint_y=None, orientation="vertical")
        rel.add_widget(fi)
        title = MDLabel(text="[size=25][ref=t]"+post['title']+"[/ref]"+"\n", markup=True, halign='center')
        subtitle = MDLabel(text="[size=18][ref=st]" + post['subtitle'] + "[/ref]"+"\n", markup=True, halign='center')
        text = MDLabel(text="[size=15][ref=tx]" + post['content'] + "[/ref]", markup=True)
        rel2.add_widget(title)
        rel2.add_widget(subtitle)
        rel3.add_widget(text)
        self.content.add_widget(rel)
        self.content.add_widget(rel2)
        self.content.add_widget(rel3)
        self.content.add_widget(MDLabel(text='[size=25][ref=t]Comments[/ref]'+"\n", markup=True))

        if 'detail' not in args[1]:
            comm = args[1]
            for com in range(len(comm)):
                box = MDRelativeLayout(orientation="vertical", size_hint_y=None)
                name = MDLabel(text="[size=18][ref=t]"+comm[com]['name']+"[/ref]" + "\n", markup=True)
                date = MDLabel(text="[size=15][color=808080][ref=t]" + comm[com]['created'][:10] + "\n",
                               halign='right',
                               markup=True)
                text = MDLabel(text="\n"*2+"[size=15][ref=t]"+comm[com]['text']+"[/ref]", markup=True)
                box.add_widget(name)
                box.add_widget(date)
                box.add_widget(text)
                self.content.add_widget(box)
        self.content.add_widget(MDLabel(text='[size=20][ref=t]Say something[/ref]'+"\n", markup=True))

        text_comm = MDTextField(hint_text="First Name", size_hint_x=.7, pos_hint={"center_x": .4, "center_y": 1})
        text_comm2 = MDTextField(hint_text="Last Name", size_hint_x=.7, pos_hint={"center_x": .4, "center_y": 1})
        text_comm3 = MDTextField(hint_text="Your message", size_hint_x=.7, pos_hint={"center_x": .4, "center_y": 1},
                                 multiline=True)

        text_comm.bind(text=self.on_name)
        text_comm2.bind(text=self.on_last)
        text_comm3.bind(text=self.on_mess)

        text_comm.mode, text_comm2.mode, text_comm3.mode = "round", "round", "round"
        self.idfp = post['id']
        self.content.add_widget(text_comm)
        self.content.add_widget(text_comm2)
        self.content.add_widget(text_comm3)
        self.content.add_widget(MDFillRoundFlatButton(text="POST COMMENT",
                                                      on_press=self.post_comm,
                                                      md_bg_color=(128/255, 128/255, 128/255, 1)))

    def on_name(self, ins, value):
        self.text_comm_name = value

    def on_last(self, ins, value):
        self.text_comm_last = value

    def on_mess(self, ins, value):
        self.text_comm_mess = value

    def post_comm(self, *args):
        if self.text_comm_name != '' and self.text_comm_last != '' and self.text_comm_mess != '':
            params = json.dumps({'name': self.text_comm_name, 'last_name': self.text_comm_last,
                             'text': self.text_comm_mess, 'post': self.idfp})
            UrlRequest('http://magazinefkolo.pythonanywhere.com/api/v1/comment/', req_body=params,
                       req_headers={'Content-Type': 'application/json'},
                       on_success=self.single)
            self.text_comm_name, self.text_comm_last, self.text_comm_mess = '', '', ''

    def on_start(self):
        self.posts()

    def build(self):
        self.root.clear_widgets()
        self.rel.add_widget(FitImage(source="bg.jpg"))
        self.head.add_widget(self.rel)
        self.sl.add_widget(self.head)
        self.sl.add_widget(self.content)
        self.root.add_widget(self.sl)
        Builder.load_string(KV)


class SliverToolbar(MDToolbar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type_height = "medium"


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
        UrlRequest('http://magazinefkolo.pythonanywhere.com/api/v1/post/{}/'.format(self.pk),
                   on_success=Main.fill_single)


if __name__ == "__main__":
    Main().run()
