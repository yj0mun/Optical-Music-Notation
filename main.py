from kivy.config import Config

Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '400')
Config.set('graphics', 'resizable', False)

import tensorflow as tf
import cv2
import numpy as np
import os
from PIL import Image as PIL_Image
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.clock import Clock
from kivy.uix.popup import Popup
from plyer import filechooser

from generate_musicxml import Generate_Musicxml
from semantic_to_tempo import Semantic_To_Tempo
import music21
from datetime import datetime
import re
import pygame
from pygame import mixer

# from kivy.utils import platform
# if platform == "android":
#
#     from jnius import autoclass
#
#     Environment = autoclass('android.os.Environment')
#     path = Environment.getExternalStorageDirectory().getAbsolutePath()

tf.compat.v1.disable_eager_execution()


# creating temporary file name with datetime

class SETUP(Popup):
    pass


class SETUP2(Popup):
    pass


class OMR_UI(ScreenManager):
    # Getting the folder address of the program located
    running_program_path = os.path.abspath(os.path.dirname(__file__))
    # the semantic text file
    voc_file = running_program_path + f'\\vocabulary_semantic.txt'
    # the model meta file
    model = running_program_path + f'\\Semantic-Model\\semantic_model.meta'
    # prediction status
    prediction_state = False

    # global variable for music symbols list
    # Example of music_symbols_list/ or array
    # music_symbols = [['clef-G2', 'keySignature-FM', 'timeSignature-3/4',
    #                   'note-A3_eighth', 'barline', 'note-D4_quarter',
    #                   'note-F4_eighth', 'note-F4_quarter', 'note-F4_eighth',
    #                   'barline', 'note-F4_quarter.', 'tie', 'note-F4_quarter',
    #                   'gracenote-G4_eighth', 'barline', 'gracenote-A4_quarter', 'note-A4_eighth',
    #                   'note-A4_quarter', 'note-A4_eighth', 'barline', 'note-A4_half.',
    #                   'barline', 'note-C5_quarter.', 'note-C5_quarter', 'note-D5_thirty_second',
    #                   'note-D5_thirty_second', 'note-D5_thirty_second', 'rest-thirty_second',
    #                   'barline']]

    # music_symbols_array = music_symbols[0]
    music_symbols_array = []

    # global variable for check status of the image selected
    is_notation = True

    # global variable for midi. player
    mixer.init()
    midi = None
    position = None
    play = False
    stop = True
    pause = False

    # global variable for line indicator
    indicator = None
    x_init_pos = 0.05
    y_init_pos = 0.275
    x_init_size = 0.001
    y_init_size = 0.3
    ratio_new_old = 1
    x_end = 0.95
    pixel_per_sec = 0
    pixel_per_frame = 0

    # global variable for file temp variables
    music_symbols_file_temp = ""
    midi_file_temp = ""
    png_file_temp = ""
    musicxml_file_temp = ""
    xml_file_temp = ""

    # global variable popup
    setup_1 = None
    setup_2 = None
    bpm = 60
    folder_name = ""
    folder_path = ""

    # global variable for capturing the width and the height of the screen
    # width = 1000; height = 400; Config Values
    # width_previous = 1000
    # height_previous = 400
    # current_width = 0
    # current_width_pos = 0

    original_location = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.after:
            self.color = Color(0, 0, 0, 0)
            self.indicator = Rectangle(pos=(self.width * self.x_init_pos, self.height * self.y_init_pos), \
                                       size=(self.width * self.x_init_size, self.height * self.y_init_size))

        # Clock.schedule_interval(self.refresh, 1/20)

    def browse(self):
        self.ids.image_selected.source = ""
        self.ids.label_selected.text = ""
        self.music_symbols_array = ""
        filechooser.open_file(on_selection=self.selected)
        self.prediction_state = False

    def selected(self, selection):
        if selection:
            # showing the file on the Image Widget
            self.ids.image_selected.source = selection[0]

            # showing the path of file located
            self.ids.label_selected.text = "Source: " + self.ids.image_selected.source
            # print(self.ids.image_selected.source)

    def clearall(self):
        self.ids.image_selected.source = ""
        self.ids.label_selected.text = ""
        self.music_symbols_array = ""
        self.prediction_state = False

    def sparse_tensor_to_strs(self, sparse_tensor):
        indices = sparse_tensor[0][0]
        values = sparse_tensor[0][1]
        dense_shape = sparse_tensor[0][2]

        strs = [[] for i in range(dense_shape[0])]

        string = []
        ptr = 0
        b = 0

        for idx in range(len(indices)):
            if indices[idx][0] != b:
                strs[b] = string
                string = []
                b = indices[idx][0]

            string.append(values[ptr])

            ptr = ptr + 1

        strs[b] = string

        return strs

    def normalize(self, image):
        return (255. - image) / 255.

    def resize(self, image, height):
        width = int(float(height * image.shape[1]) / image.shape[0])
        sample_img = cv2.resize(image, (width, height))
        return sample_img

    def read_document(self, file):
        dict_file = open(file, 'r')
        dict_list = dict_file.read().splitlines()
        # print(dict_list)
        int2word = dict()
        for word in dict_list:
            word_idx = len(int2word)
            int2word[word_idx] = word
        # print(int2word)
        dict_file.close()

        return int2word

    def initialization_model(self, model):
        # tf.reset_default_graph()
        sess = tf.compat.v1.InteractiveSession()

        # Restore weights
        saver = tf.compat.v1.train.import_meta_graph(model)
        saver.restore(sess, model[:-5])

        graph = tf.compat.v1.get_default_graph()

        input = graph.get_tensor_by_name("model_input:0")
        seq_len = graph.get_tensor_by_name("seq_lengths:0")
        rnn_keep_prob = graph.get_tensor_by_name("keep_prob:0")
        height_tensor = graph.get_tensor_by_name("input_height:0")
        width_reduction_tensor = graph.get_tensor_by_name("width_reduction:0")
        logits = tf.compat.v1.get_collection("logits")[0]

        # Constants that are saved inside the model itself
        WIDTH_REDUCTION, HEIGHT = sess.run([width_reduction_tensor, height_tensor])

        decoded, _ = tf.nn.ctc_greedy_decoder(logits, seq_len)

        return sess, input, seq_len, rnn_keep_prob, WIDTH_REDUCTION, HEIGHT, decoded, _

    def preprocessing_image(self, img, height, width_reduction):
        img_input = img
        image = PIL_Image.open(img_input).convert('L')
        image = np.array(image)
        image = self.resize(image, height)
        image = self.normalize(image)
        image = np.asarray(image).reshape(1, image.shape[0], image.shape[1], 1)
        seq_lengths = [image.shape[2] / width_reduction]

        return image, seq_lengths

    def prediction_mn(self, session, decoded, image_input, image, sequence_length, sequence_length_get,
                      rnn_keep_problem):

        prediction_result = session.run(decoded,
                                        feed_dict={
                                            image_input: image,
                                            sequence_length: sequence_length_get,
                                            rnn_keep_problem: 1.0,
                                        })

        return prediction_result

    def convert_int_to_text(self, semantic_language, str_prediction):
        music_symbols_array = []
        for text in str_prediction[0]:
            music_symbols_array.append(semantic_language[text])

        return music_symbols_array

    def predict(self):

        input_notation_image = self.ids.image_selected.source

        if self.ids.image_selected.source == "":
            self.ids.label_selected.text = " Please insert a picture of a Music Notation from the browse..."

        elif self.prediction_state:
            self.ids.label_selected.text = "The Recognition Process is Done. Please press \"Clear\" or \"Browse...\"" \
                                           + "before starting a new process"
        else:

            if input_notation_image[len(input_notation_image) - 4:len(input_notation_image)] == ".png" or \
                    input_notation_image[len(input_notation_image) - 4:len(input_notation_image)] == ".jpg" or \
                    input_notation_image[len(input_notation_image) - 5:len(input_notation_image)] == ".jpeg":

                # read the semantic vocabulary file
                semantic_dict = self.read_document(self.voc_file)

                # initialization
                sess, image_input, seq_len, rnn_keep_prob, width_reduction, height, decoded, _ = self.initialization_model(
                    self.model)

                # preprocessing image
                image, seq_lengths = self.preprocessing_image(input_notation_image, height, width_reduction)

                # predicting the music notation
                prediction_result = self.prediction_mn(sess, decoded, image_input, image, seq_len, seq_lengths,
                                                       rnn_keep_prob)

                # convert the tensor value into the array number that match with vocabulary_semantic.txt
                str_predictions = self.sparse_tensor_to_strs(prediction_result)

                print(str_predictions[0])
                print(len(str_predictions[0]))

                # convert number into semantic text
                music_symbols = [self.convert_int_to_text(semantic_dict, str_predictions)]
                self.music_symbols_array = music_symbols[0]

                print(self.music_symbols_array)

                self.ids.label_selected.text = "Recognition Complete"

                self.is_notation = self.check_notation(self.music_symbols_array)

                self.prediction_state = True

                if self.is_notation:
                    pass

                else:
                    self.ids.label_selected.text = "This is not a music notation."

            else:
                self.ids.label_selected.text = "This is not a .png, .jpg or .jpeg file."

    # check whether is notation or not
    def check_notation(self, music_symbols_array):
        a = re.compile('clef')
        c = re.compile('timeSignature')
        d = re.compile('note')
        e = re.compile('barline')
        # b = re.compile('keySignature')

        is_a_notation = True

        # not more than 3 music symbols in the array
        if len(music_symbols_array) < 3:
            is_a_notation = False

        # not note , clef, timeSignature and barline is found
        if any(d.match(i) for i in music_symbols_array) and any(e.match(i) for i in music_symbols_array) \
                and any(c.match(i) for i in music_symbols_array) \
                and any(a.match(i) for i in music_symbols_array):
            pass
        else:
            is_a_notation = False

        return is_a_notation

    def browse_for_file(self):
        filechooser.open_file(on_selection=self.file_choose)

    def file_choose(self, selection):
        if selection:
            file_open = selection[0]

            # register file_open into midi global variable
            if file_open[len(file_open) - 4:len(file_open)] == ".txt":

                self.music_symbols_file_temp = file_open
                self.ids.label_showing.text = ""

            else:

                self.ids.label_showing.text = "The file type is not .txt file."

            # print(self.png_file_temp, self.musicxml_file_temp, self.midi_file_temp)

    def select_popup_window(self):
        if self.prediction_state:
            self.setup_1 = SETUP()
            self.setup_1.ids.folder_name.hint_text = "Type Folder Name"
            self.setup_1.ids.BPM.hint_text = str(self.bpm)
            self.setup_1.open()

        else:
            if self.music_symbols_file_temp == "":
                self.ids.label_showing.text = "Please insert a music symbols text file"
            else:
                self.setup_2 = SETUP2()
                self.setup_2.ids.folder_name_2.hint_text = "Type Folder Name"
                self.setup_2.ids.BPM_2.hint_text = str(self.bpm)
                self.setup_2.open()

    def get_files_ready(self):
        Gen_XML = Generate_Musicxml()
        # Create a folder for xml

        if self.setup_1.ids.BPM.text == "":
            bpm_selected = self.bpm

        else:
            bpm_selected = int(self.setup_1.ids.BPM.text)
            self.bpm = bpm_selected

        if self.setup_1.ids.folder_name.text == "":
            currentDateTime = datetime.now()
            currentDate = currentDateTime.strftime("%Y%m%d")
            currentTime = currentDateTime.strftime("%H%M%S")

            file_name = f"Music_" + currentDate + currentTime

            self.setup_1.ids.folder_name.text = file_name

        else:

            file_name = self.setup_1.ids.folder_name.text

        path_all_files = self.running_program_path + f'\\files\\' + file_name

        if not os.path.isdir(path_all_files):
            os.makedirs(path_all_files)

            self.music_symbols_file_temp = path_all_files + f"\\" + file_name + f".txt"

            with open(self.music_symbols_file_temp, "w") as txt_file:
                for line in self.music_symbols_array:
                    txt_file.write(" ".join(line) + "\n")

            self.xml_file_temp = path_all_files + f"\\" + file_name + f".xml"

            Gen_XML.GenerateXML(self.xml_file_temp, self.music_symbols_array, bpm_selected)
            print("test1")

            # name the png file name and midi file name
            self.png_file_temp = path_all_files + f"\\" + file_name + ".png"
            self.midi_file_temp = path_all_files + f"\\" + file_name + ".midi"

            # convert xml file
            c = music21.converter.parse(self.xml_file_temp)

            # get the converted files and save the files with the name given above
            c.write('musicxml.png', self.png_file_temp)
            c.write('midi', self.midi_file_temp)

            # save the converted files's name in the global variable (png and musicxml)
            self.png_file_temp = path_all_files + f"\\" + file_name + "-1.png"
            self.musicxml_file_temp = path_all_files + f"\\" + file_name + ".musicxml"

            # show the png file on the Image Widget
            self.ids.image_showing.source = self.png_file_temp

            # Notify the user
            self.ids.label_showing.text = "All files is ready"
            print("test1")

        else:
            self.setup_1.ids.showing_label_p1.text = f"\"" + file_name + "\"  is available in the directory." + \
                                                     " Please re-type a name."

    def read_music_text_file(self):
        music_symbols_file = open(self.music_symbols_file_temp, 'r')
        music_symbols_list = music_symbols_file.read().splitlines()

        # declare the global variable as array
        self.music_symbols_array = []

        for i in music_symbols_list:
            # remove the space which created by splitlines
            j = i.replace(" ", "")

            # insert the word into a global array variable
            self.music_symbols_array.append(j)

        # print(self.music_symbols_array)

    def re_setup_all_files(self):
        self.read_music_text_file()
        Gen_XML = Generate_Musicxml()
        # Create a folder for xml

        if self.setup_2.ids.BPM_2.text == "":
            bpm_selected = self.bpm

        else:
            bpm_selected = int(self.setup_2.ids.BPM_2.text)
            self.bpm = bpm_selected

        if self.setup_2.ids.folder_name_2.text == "":
            currentDateTime = datetime.now()
            currentDate = currentDateTime.strftime("%Y%m%d")
            currentTime = currentDateTime.strftime("%H%M%S")

            file_name = f"Music_" + currentDate + currentTime

            self.setup_2.ids.folder_name_2.text = file_name

        else:

            file_name = self.setup_2.ids.folder_name_2.text

        path_all_files = self.running_program_path + f'\\files\\' + file_name

        if not os.path.isdir(path_all_files):
            os.makedirs(path_all_files)
            self.music_symbols_file_temp = path_all_files + f"\\" + file_name + f".txt"

            with open(self.music_symbols_file_temp, "w") as txt_file:
                for line in self.music_symbols_array:
                    txt_file.write(" ".join(line) + "\n")

            self.xml_file_temp = path_all_files + f"\\" + file_name + f".xml"

            Gen_XML.GenerateXML(self.xml_file_temp, self.music_symbols_array, bpm_selected)
            print("test1")

            # name the png file name and midi file name
            self.png_file_temp = path_all_files + f"\\" + file_name + ".png"
            self.midi_file_temp = path_all_files + f"\\" + file_name + ".midi"

            # convert xml file
            c = music21.converter.parse(self.xml_file_temp)

            # get the converted files and save the files with the name given above
            c.write('musicxml.png', self.png_file_temp)
            c.write('midi', self.midi_file_temp)

            # save the converted files's name in the global variable (png and musicxml)
            self.png_file_temp = path_all_files + f"\\" + file_name + "-1.png"
            self.musicxml_file_temp = path_all_files + f"\\" + file_name + ".musicxml"

            # show the png file on the Image Widget
            self.ids.image_showing.source = self.png_file_temp

            # Notify the user
            self.ids.label_showing.text = "All files is ready"
        else:
            self.setup_2.ids.showing_label_p2.text = f"\"" + file_name + "\"  is available in the directory." + \
                                                     " Please re-type a name."

    def clear_all_files(self, instance):
        # Clear all files global variable
        self.musicxml_file_temp = ""
        self.midi_file_temp = ""
        self.png_file_temp = ""

        # Empty the Image Widget
        self.ids.image_showing.source = ""
        self.ids.label_showing.text = "All files are cleared"

        # Reset Music Player
        mixer.music.stop()
        self.pause = False
        self.play = False
        self.stop = True

        # Changing the play/pause button to PLAY
        self.ids.play_pause.text = "PLAY"

        # Hide the indicator
        self.color.rgba = [0, 0, 0, 0]

        # set the prediction status to False
        self.prediction_state = False

        # Stop the Clock
        Clock.unschedule(self.move_right)

    def play_music(self):
        midi_file = self.midi_file_temp
        print(midi_file)

        self.color.rgba = [0, 0, 0, 1]

        # play play stop pause False True False
        if not self.play and self.stop and not self.pause:
            # print(self.width, self.height)
            # self.current_width_pos = self.indicator.pos[0]
            # self.current_width = self.width
            new_pos = self.check_notation_lengths
            self.indicator.pos = (new_pos, self.height * self.y_init_pos)
            self.indicator.size = (self.width * self.x_init_size, self.height * self.y_init_size)
            Clock.schedule_interval(self.move_right, 1.0 / 60.0)
            Clock.schedule_interval(self.is_music_finished, 1.0 / 60.0)
            mixer.music.load(midi_file)
            mixer.music.play()
            self.play = True
            self.stop = False
            self.ids.play_pause.text = "PAUSE"

        # pause play stop pause True False False
        elif not self.stop and self.play:
            mixer.music.pause()
            self.pause = True
            self.play = False
            self.ids.play_pause.text = "PLAY"

        # unpause play stop pause False False True
        elif not self.stop and self.pause:
            mixer.music.unpause()
            self.play = True
            self.pause = False
            self.ids.play_pause.text = "PAUSE"

        else:
            pass

    def btn_play_music(self):
        midi_file = self.midi_file_temp
        print(midi_file)

        if midi_file == "":
            self.ids.label_showing.text = "No .midi file found."

        else:
            self.play_music()
            print(self.play, self.stop, self.pause)

    def btn_stop_music(self):
        midi_file = self.midi_file_temp

        if midi_file == "":
            self.ids.label_showing.text = "No .midi file is playing."

        else:
            mixer.music.stop()
            self.pause = False
            self.play = False
            self.stop = True
            self.ids.play_pause.text = "PLAY"
            self.color.rgba = [0, 0, 0, 0]
            Clock.unschedule(self.move_right)

    # change the play/pause btn back to play when music is finished
    def is_music_finished(self, instance):
        if self.play and not self.stop and not self.pause and not pygame.mixer.music.get_busy():
            self.pause = False
            self.play = False
            self.stop = True
            self.ids.play_pause.text = "PLAY"
            self.color.rgba = [0, 0, 0, 0]
            Clock.unschedule(self.move_right)

    @property
    def check_notation_lengths(self):
        STT = Semantic_To_Tempo()
        music_symbols_list = self.music_symbols_array
        clef = 0
        kS = 0
        tS = 0
        ratio_start = 0
        ratio_notation = 0
        ratio_note_rest = 0
        first_note = True

        last_symbols = music_symbols_list[len(music_symbols_list) - 1]

        if last_symbols == "barline":
            music_symbols_list.pop(len(music_symbols_list) - 1)

        for i in music_symbols_list:
            if i[0:5] == "clef-" and clef == 0:
                sign = i[5]
                line = int(i[6])
                ratio_start += STT.get_clef_tempo(i)
                clef = 1

            elif i[0:13] == "keySignature-" and kS == 0:
                ratio_start += STT.get_keySignature_tempo(i)
                kS = 1

            elif i[0:14] == "timeSignature-" and tS == 0:
                ratio_start += STT.get_timeSignature_tempo(i)
                tS = 1

            elif i[0:7] == "barline":
                ratio_notation += 0.008

            elif i[0:5] == "rest-":
                ratio_note_rest += STT.get_rest_tempo(i)

            else:
                if i[0:5] == "grace":
                    j = i.replace("grace", "")
                    i = j

                if i[0:5] == "note-":

                    if i[6].isdigit():
                        octave = int(i[6])
                    else:
                        octave = int(i[7])

                    if first_note:
                        first_note = False
                        # Treble Clef
                        if sign == "G":
                            if octave == 4 or octave == 5:
                                if octave == 5:
                                    pass
                                    if i[5] == "A" or i[5] == "B":
                                        first_note_ratio = 0.012
                                    else:
                                        first_note_ratio = 0.008
                                elif octave == 4:
                                    if i[5] == "C":
                                        first_note_ratio = 0.012
                                    else:
                                        first_note_ratio = 0.008
                                else:
                                    pass
                            else:
                                first_note_ratio = 0.012

                        # Bass Clef
                        elif sign == "F":
                            if octave == 3 or octave == 2:
                                if octave == 2:
                                    if i[5] == "E" or i[5] == "D" or i[5] == "C":
                                        first_note_ratio = 0.012
                                    else:
                                        first_note_ratio = 0.008
                                else:
                                    first_note_ratio = 0.008
                            else:
                                first_note_ratio = 0.012

                        # Alto Clef
                        elif sign == "C" and line > 3:
                            if octave == 3 or octave == 4:
                                if octave == 3:
                                    if i[5] == "D" or i[5] == "C":
                                        first_note_ratio = 0.012
                                    else:
                                        first_note_ratio = 0.008

                                elif octave == 4:
                                    if i[5] == "B":
                                        first_note_ratio = 0.012
                                    else:
                                        first_note_ratio = 0.008
                                else:
                                    pass
                            else:
                                first_note_ratio = 0.012

                        # Tenor Clef
                        elif sign == "C" and line < 4:
                            if octave == 3 or octave == 4:
                                if octave == 4:
                                    if i[5] == "G" or i[5] == "A" or i[5] == "B":
                                        first_note_ratio = 0.012
                                    else:
                                        first_note_ratio = 0.008
                                else:
                                    first_note_ratio = 0.008
                            else:
                                first_note_ratio = 0.012

                    ratio_note_rest += STT.get_note_tempo(i)

                else:
                    pass

        if kS == 1:
            ratio_start += 0.008

        if tS == 1:
            ratio_start += 0.008

        # Calculating the pixel of Image Widget
        starting_width_pixels = self.width * self.x_init_pos
        ending_width_pixels = self.width * self.x_end
        total_pixel = ending_width_pixels - starting_width_pixels

        # excluding pixels of clef, keySignature and timeSignature
        new_starting_pixels = ratio_start * self.width + starting_width_pixels + first_note_ratio

        # the rest pixel
        rest_pixel = total_pixel - new_starting_pixels

        # time lengths of midi
        time_lengths = (ratio_note_rest / 4) / self.bpm * 60
        # pixel per second
        self.pixel_per_sec = rest_pixel / time_lengths

        # pixel per frame if frame rate = 60
        self.pixel_per_frame = self.pixel_per_sec / 75

        return new_starting_pixels

    def move_right(self, instance):
        if self.play:
            # print("before: " + str(self.indicator.pos))
            x = self.indicator.pos[0]
            y = self.indicator.pos[1]

            if x <= self.width * 0.95:
                x += 1 * self.pixel_per_frame
                self.indicator.pos = (x, y)
                #print("after: " + str(self.indicator.pos))

            else:
                pass
        # x = self.indicator.pos[0]
        # y = self.indicator.pos[1]
        # self.color.rgba = (0, 0, 0, 1)
        # if x <= self.width * 0.95:
        #     x += 1 * self.ratio_new_old
        #
        #     self.indicator.pos = (x, y)
        #     print("after: " + str(self.indicator.pos))
        #     print(x - self.original_location)
        #
        # else:
        #     pass


class OpticalMusicNotation(App):
    Builder.load_file('OMR_layout.kv')

    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return OMR_UI()


OpticalMusicNotation().run()

