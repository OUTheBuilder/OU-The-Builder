import os
from functools import partial

from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Line

Window.clearcolor = (0.035, 0.045, 0.075, 1)
# Screen dimensions are controlled by Android; do not force a desktop window size.


def styled_button(text, callback=None, color=(0.12, 0.18, 0.28, 1), height=dp(42)):
    b = Button(text=text, size_hint_y=None, height=height,
               background_normal="", background_down="",
               background_color=color, color=(0.93, 0.96, 1, 1),
               font_size="14sp")
    if callback:
        b.bind(on_release=callback)
    return b


class Waveform(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(0.08, 0.85, 0.78, 1)
            self.line = Line(points=[], width=1.15)
        self.bind(pos=self.redraw, size=self.redraw)

    def redraw(self, *_):
        pts = []
        count = 100
        for i in range(count):
            x = self.x + self.width * i / (count - 1)
            # Decorative rhythm trace until decoded waveform analysis is added.
            import math
            y = self.center_y + math.sin(i * .47) * self.height * .22 * (0.35 + .65 * abs(math.sin(i*.13)))
            pts.extend([x, y])
        self.line.points = pts


class Deck(BoxLayout):
    def __init__(self, name, **kwargs):
        super().__init__(orientation="vertical", spacing=dp(7), padding=dp(10), **kwargs)
        self.name = name
        self.sound = None
        self.path = None
        self.cue_position = 0
        self.loop_start = None
        self.loop_end = None
        self.loop_event = None

        with self.canvas.before:
            Color(0.065, 0.085, 0.13, 1)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(14)])
        self.bind(pos=self._sync_bg, size=self._sync_bg)

        head = BoxLayout(size_hint_y=None, height=dp(34))
        head.add_widget(Label(text=name, bold=True, color=(0.18, .91, .82, 1), font_size="18sp"))
        self.track_label = Label(text="No track loaded", color=(.78,.84,.92,1), halign="right", font_size="12sp")
        head.add_widget(self.track_label)
        self.add_widget(head)

        self.wave = Waveform(size_hint_y=None, height=dp(72))
        self.add_widget(self.wave)

        self.position = Slider(min=0, max=100, value=0, size_hint_y=None, height=dp(28))
        self.position.bind(on_touch_up=self.seek_from_slider)
        self.add_widget(self.position)

        row = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(5))
        row.add_widget(styled_button("LOAD TRACK", self.choose_track, (.10,.34,.42,1)))
        row.add_widget(styled_button("▶ / ❚❚", self.toggle_play, (.08,.45,.37,1)))
        row.add_widget(styled_button("CUE", self.cue, (.28,.22,.48,1)))
        row.add_widget(styled_button("STOP", self.stop, (.43,.16,.22,1)))
        self.add_widget(row)

        self.volume = Slider(min=0, max=1, value=1)
        self.volume.bind(value=self.set_volume)
        volrow = BoxLayout(size_hint_y=None, height=dp(26))
        volrow.add_widget(Label(text="DECK VOLUME", size_hint_x=.38, font_size="10sp", color=(.6,.68,.8,1)))
        volrow.add_widget(self.volume)
        self.add_widget(volrow)

        pads = BoxLayout(size_hint_y=None, height=dp(38), spacing=dp(5))
        for i in range(1,5):
            pads.add_widget(styled_button("HOT CUE "+str(i), partial(self.hot_cue, i), (.16,.20,.32,1), dp(36)))
        self.add_widget(pads)
        loops = BoxLayout(size_hint_y=None, height=dp(36), spacing=dp(5))
        loops.add_widget(styled_button("SET LOOP IN", self.loop_in, (.17,.24,.34,1), dp(34)))
        loops.add_widget(styled_button("LOOP 4 BEATS", self.loop_four, (.17,.24,.34,1), dp(34)))
        loops.add_widget(styled_button("EXIT LOOP", self.loop_out, (.34,.19,.22,1), dp(34)))
        self.add_widget(loops)
        self.hot_cues = {}

        Clock.schedule_interval(self.refresh, .15)

    def _sync_bg(self, *_):
        self.bg.pos, self.bg.size = self.pos, self.size

    def choose_track(self, *_):
        start = "/storage/emulated/0/Music"
        if not os.path.isdir(start):
            start = "/storage/emulated/0"
        chooser = FileChooserListView(path=start, filters=["*.mp3","*.wav","*.ogg","*.m4a","*.flac"], dirselect=False)
        modal = ModalView(size_hint=(.94,.92), background_color=(.035,.045,.075,.98))
        layout = BoxLayout(orientation="vertical", padding=dp(8), spacing=dp(8))
        layout.add_widget(Label(text="Choose an audio track", size_hint_y=None, height=dp(35)))
        layout.add_widget(chooser)
        actions = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(8))
        actions.add_widget(styled_button("CANCEL", lambda *_: modal.dismiss()))
        def load_selected(*_):
            if chooser.selection:
                self.load_track(chooser.selection[0])
                modal.dismiss()
        actions.add_widget(styled_button("LOAD SELECTED", load_selected, (.08,.45,.37,1)))
        layout.add_widget(actions)
        modal.add_widget(layout)
        modal.open()

    def load_track(self, path):
        try:
            new_sound = SoundLoader.load(path)
            if not new_sound:
                self.track_label.text = "Unsupported audio format"
                return
            if self.sound:
                self.sound.stop()
            self.sound = new_sound
            self.path = path
            self.cue_position = 0
            self.hot_cues.clear()
            self.track_label.text = os.path.basename(path)[:28]
            self.sound.volume = self.volume.value
            self.position.max = max(float(self.sound.length or 1), 1)
            self.position.value = 0
        except Exception as exc:
            self.track_label.text = "Load error: " + str(exc)[:22]

    def toggle_play(self, *_):
        if not self.sound:
            self.choose_track()
            return
        if self.sound.state == "play":
            self.sound.stop()
        else:
            self.sound.play()
            self.sound.volume = self.volume.value

    def stop(self, *_):
        if self.sound:
            self.sound.stop()
            self.sound.seek(0)
            self.position.value = 0

    def cue(self, *_):
        if not self.sound:
            return
        if self.sound.state == "play":
            self.cue_position = self.sound.get_pos()
            self.sound.stop()
        else:
            self.sound.play()
            self.sound.seek(self.cue_position)

    def seek_from_slider(self, _slider, touch):
        if self.sound and self.position.collide_point(*touch.pos):
            self.sound.seek(self.position.value)

    def set_volume(self, _slider, value):
        if self.sound:
            self.sound.volume = value

    def hot_cue(self, number, *_):
        if not self.sound:
            return
        if number in self.hot_cues:
            self.sound.seek(self.hot_cues[number])
        else:
            self.hot_cues[number] = self.sound.get_pos() if self.sound.state == "play" else self.position.value

    def loop_in(self, *_):
        if self.sound:
            self.loop_start = self.sound.get_pos() if self.sound.state == "play" else self.position.value

    def loop_four(self, *_):
        if not self.sound:
            return
        start = self.sound.get_pos() if self.sound.state == "play" else self.position.value
        duration = max(float(self.sound.length or 0), 0)
        if duration <= 0:
            return
        # Approximate four-beat loop at 120 BPM = 2 seconds.
        self.loop_start, self.loop_end = start, min(start + 2.0, duration)
        self._start_loop()

    def _start_loop(self):
        if self.loop_event:
            self.loop_event.cancel()
        def check_loop(_dt):
            if self.sound and self.loop_end is not None and self.sound.state == "play":
                if self.sound.get_pos() >= self.loop_end:
                    self.sound.seek(self.loop_start)
        self.loop_event = Clock.schedule_interval(check_loop, .05)

    def loop_out(self, *_):
        self.loop_end = None
        if self.loop_event:
            self.loop_event.cancel()
            self.loop_event = None

    def refresh(self, _dt):
        if self.sound:
            length = float(self.sound.length or 0)
            if length > 0:
                self.position.max = length
                if self.sound.state == "play":
                    self.position.value = min(self.sound.get_pos(), length)


class DJStudio(App):
    def on_start(self):
        # Android 13+ uses READ_MEDIA_AUDIO; older versions use READ_EXTERNAL_STORAGE.
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_MEDIA_AUDIO, Permission.READ_EXTERNAL_STORAGE])
        except Exception:
            pass

    def build(self):
        root = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(8))
        header = BoxLayout(size_hint_y=None, height=dp(48))
        header.add_widget(Label(text="OU DJ STUDIO", bold=True, font_size="22sp",
                                color=(.18,.91,.82,1), halign="left"))
        header.add_widget(Label(text="PYTHON EDITION  •  TWO-DECK MIXER", font_size="11sp",
                                color=(.55,.66,.8,1), halign="right"))
        root.add_widget(header)

        decks = BoxLayout(spacing=dp(10))
        self.deck_a = Deck("DECK A")
        self.deck_b = Deck("DECK B")
        decks.add_widget(self.deck_a)
        decks.add_widget(self.deck_b)
        root.add_widget(decks)

        mixer = BoxLayout(size_hint_y=None, height=dp(92), padding=[dp(12),dp(4)], spacing=dp(10))
        mixer.add_widget(Label(text="A", size_hint_x=.06, color=(.18,.91,.82,1), bold=True))
        self.crossfader = Slider(min=0, max=1, value=.5)
        self.crossfader.bind(value=self.apply_crossfade)
        mixer.add_widget(self.crossfader)
        mixer.add_widget(Label(text="B", size_hint_x=.06, color=(.18,.91,.82,1), bold=True))
        master_col = BoxLayout(orientation="vertical", size_hint_x=.25)
        master_col.add_widget(Label(text="MASTER OUTPUT", font_size="10sp", color=(.65,.72,.82,1)))
        self.master = Slider(min=0,max=1,value=.9)
        self.master.bind(value=self.apply_master)
        master_col.add_widget(self.master)
        mixer.add_widget(master_col)
        root.add_widget(mixer)

        footer = Label(text="Load audio from your device • Use headphones for best results • Keep device volume moderate",
                       size_hint_y=None, height=dp(22), font_size="10sp", color=(.42,.52,.66,1))
        root.add_widget(footer)
        self.apply_crossfade(self.crossfader, .5)
        return root

    def apply_crossfade(self, _slider, value):
        # Equal-power approximation with per-deck gain.
        import math
        self.deck_a.volume.value = math.cos(value * math.pi / 2)
        self.deck_b.volume.value = math.sin(value * math.pi / 2)
        self.deck_a.set_volume(None, self.deck_a.volume.value)
        self.deck_b.set_volume(None, self.deck_b.volume.value)

    def apply_master(self, _slider, value):
        # Scale both decks while preserving their relative crossfade balance.
        self.deck_a.set_volume(None, self.deck_a.volume.value * value)
        self.deck_b.set_volume(None, self.deck_b.volume.value * value)


if __name__ == "__main__":
    DJStudio().run()
