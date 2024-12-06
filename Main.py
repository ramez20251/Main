from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from pytube import YouTube
from youtubesearchpython import VideosSearch

class YouTubeApp(BoxLayout):
    def __init__(self, **kwargs):
        super(YouTubeApp, self).__init__(**kwargs)

        self.orientation = 'vertical'

        self.query_input = TextInput(hint_text='أدخل كلمات البحث', size_hint=(1, 0.1))
        self.add_widget(self.query_input)

        self.search_button = Button(text='بحث عن الفيديو', size_hint=(1, 0.1))
        self.search_button.bind(on_press=self.search_video)
        self.add_widget(self.search_button)

        self.video_label = Label(text='', size_hint=(1, 0.1))
        self.add_widget(self.video_label)

        self.download_button = Button(text='تنزيل الفيديو', size_hint=(1, 0.1))
        self.download_button.bind(on_press=self.download_video)
        self.download_button.disabled = True
        self.add_widget(self.download_button)

        self.selected_video_url = None

    def search_video(self, instance):
        query = self.query_input.text
        videos_search = VideosSearch(query, limit=1)
        results = videos_search.next()
        
        if results and len(results['result']) > 0:
            self.selected_video_url = results['result'][0]['link']
            self.video_label.text = f"وجدت فيديو: {results['result'][0]['title']}"
            self.download_button.disabled = False
        else:
            self.video_label.text = "لم يتم العثور على فيديو."

    def download_video(self, instance):
        if self.selected_video_url:
            try:
                yt = YouTube(self.selected_video_url)
                stream = yt.streams.get_highest_resolution()
                stream.download()
                print(f"تم تنزيل الفيديو: {yt.title}")
            except Exception as e:
                print(f"حدث خطأ: {e}")

class MyApp(App):
    def build(self):
        return YouTubeApp()

if __name__ == '__main__':
    MyApp().run()
