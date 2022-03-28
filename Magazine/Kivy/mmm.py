from kivy.network.urlrequest import UrlRequest
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
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
from kivymd.uix.sliverappbar import MDSliverAppbar, MDSliverAppbarHeader, MDSliverAppbarContent
from kivymd.uix.toolbar import MDToolbar
from kivy.uix.button import Button
from kivy.uix.slider import Slider



class Main(MDApp):
    content_list = []

    def __init__(self):
        super(Main, self).__init__()
        self.root = MDScreen()
        self.sl = MDSliverAppbar(background_color=get_color_from_hex("808080"))
        self.head = MDSliverAppbarHeader()
        self.tool = SliverToolbar()
        # self.tool.add_widget(MDLabel(text="Magazine"))
        self.sl.toolbar_cls = self.tool
        self.rel = MDRelativeLayout()
        self.content = MDSliverAppbarContent(orientation="vertical", padding="12dp", spacing="12dp",
                                             adaptive_height=True)
        self.fill()

    def fill(self):
        for i in range(5):
            card = CardItem(t='title', c='cat_name', s='subtitle', pk=i)
            card.on_press = UrlRequest('http://127.0.0.1:8000/api/v1/cats/',
                                         on_success=self.single)
            self.content.add_widget(card)

    def single(self, *args):
        print(1)
        self.content.clear_widgets()

    def build(self):
        self.root.clear_widgets()
        self.rel.add_widget(FitImage(source="bg.jpg"))
        self.head.add_widget(self.rel)
        self.sl.add_widget(self.head)
        self.sl.add_widget(self.content)
        self.root.add_widget(self.sl)


class CardItem(MDCard, RoundedRectangularElevationBehavior):
    def __init__(self, t, c, s, pk):
        super(CardItem, self).__init__()
        self.size_hint_y = None
        self.height = "286dp"
        self.padding = "4dp"
        self.radius = 12
        self.elevation = 4
        rel2 = MDRelativeLayout(height="278dp",
                                # orientation="vertical",
                                adaptive_height=True,
                                # spacing="6dp"
                                )
        fi = FitImage(source="avatar.jpg", radius=self.radius)
        ml = MDLabel(text="[ref=t][color=ffffff]"+"title"+"[/ref]", markup=True,
                     font_style="H6", bold=True, adaptive_height=True, halign='center', valign='center',
                     pos_hint={"center_y": .3})
        rel2.add_widget(fi)
        rel2.add_widget(ml)
        self.add_widget(rel2)


class SliverToolbar(MDToolbar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type_height = "medium"


if __name__ == "__main__":
    Main().run()