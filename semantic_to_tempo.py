# work with generate_musicxml.py to convert the semantic text to tempo


class Semantic_To_Tempo:
    barline_count = 0
    symbol = ""

    @staticmethod
    def get_note_tempo(note):
        number_of_char = len(note)
        tempo_ratio_note = 0

        if note[0:5] == "grace":
            j = note.replace("grace", "")
        else:
            j = note

        # check _fermata is present, remove it when found it
        if note[number_of_char - 8:number_of_char] == "_fermata":
            i = j.replace("_fermata", "")
        else:
            i = j

        # getting octave eg: 1, 2, 3, 4, 5, 6, 7
        if i[6].isdigit():
            type_start = 8
        else:
            type_start = 9

        # getting tempo eg: quadruple_whole, whole, half, quarter, eighth, \
        # sixteenth, thirty_second, sixty_fourth
        if i[type_start:number_of_char] == 'quadruple_whole':
            tempo_ratio_note = 64
        elif i[type_start:number_of_char] == 'double_whole':
            tempo_ratio_note = 32
        elif i[type_start:number_of_char] == 'whole':
            tempo_ratio_note = 16
        elif i[type_start:number_of_char] == 'half':
            tempo_ratio_note = 8
        elif i[type_start:number_of_char] == 'quarter':
            tempo_ratio_note = 4
        elif i[type_start:number_of_char] == 'eighth':
            tempo_ratio_note = 2
        elif i[type_start:number_of_char] == 'sixteenth':
            tempo_ratio_note = 1
        elif i[type_start:number_of_char] == 'thirty_second':
            tempo_ratio_note = 0.5
        elif i[type_start:number_of_char] == 'sixty_fourth':
            tempo_ratio_note = 0.25
        else:
            pass

        # if it is dotted note
        if i[number_of_char - 1] == '.' and i[number_of_char - 2] == '.':
            dot = 2

            if i[type_start:number_of_char - dot] == 'quadruple_whole':
                tempo_ratio_note = 64
            elif i[type_start:number_of_char - dot] == 'double_whole':
                tempo_ratio_note = 32
            elif i[type_start:number_of_char - dot] == 'whole':
                tempo_ratio_note = 16
            elif i[type_start:number_of_char - dot] == 'half':
                tempo_ratio_note = 8
            elif i[type_start:number_of_char - dot] == 'quarter':
                tempo_ratio_note = 4
            elif i[type_start:number_of_char - dot] == 'eighth':
                tempo_ratio_note = 2
            elif i[type_start:number_of_char - dot] == 'sixteenth':
                tempo_ratio_note = 1
            elif i[type_start:number_of_char - dot] == 'thirty_second':
                tempo_ratio_note = 0.5
            elif i[type_start:number_of_char - dot] == 'sixty_fourth':
                tempo_ratio_note = 0.25
            else:
                pass

        elif i[number_of_char - 1] == '.' and not i[number_of_char - 2] == '.':

            dot = 1

            if i[type_start:number_of_char - dot] == 'quadruple_whole':
                tempo_ratio_note = 64
            elif i[type_start:number_of_char - dot] == 'double_whole':
                tempo_ratio_note = 32
            elif i[type_start:number_of_char - dot] == 'whole':
                tempo_ratio_note = 16
            elif i[type_start:number_of_char - dot] == 'half':
                tempo_ratio_note = 8
            elif i[type_start:number_of_char - dot] == 'quarter':
                tempo_ratio_note = 4
            elif i[type_start:number_of_char - dot] == 'eighth':
                tempo_ratio_note = 2
            elif i[type_start:number_of_char - dot] == 'sixteenth':
                tempo_ratio_note = 1
            elif i[type_start:number_of_char - dot] == 'thirty_second':
                tempo_ratio_note = 0.5
            elif i[type_start:number_of_char - dot] == 'sixty_fourth':
                tempo_ratio_note = 0.25
            else:
                pass
        else:
            pass

        return tempo_ratio_note

    @staticmethod
    def get_clef_tempo(clef):
        i = clef
        sign = i[5]

        if sign == "G":
            tempo = 0.027

        if sign == "F" or sign == "C":
            tempo = 0.029

        return tempo

    @staticmethod
    def get_rest_tempo(rest):
        number_of_char = len(rest)
        tempo_ratio_rest = 0
        type_start = 5

        # check _fermata is present, remove it when found it
        if rest[number_of_char-8:number_of_char] == "_fermata":
            i = rest.replace("_fermata", "")
        else:
            i = rest

        # getting tempo eg: quadruple_whole, whole, half, quarter, eighth, sixteenth, thirty_second, sixty_fourth
        if i[type_start:number_of_char] == 'quadruple_whole':
            tempo_ratio_rest = 64
        elif i[type_start:number_of_char] == 'double_whole':
            tempo_ratio_rest = 32
        elif i[type_start:number_of_char] == 'whole':
            tempo_ratio_rest = 16
        elif i[type_start:number_of_char] == 'half':
            tempo_ratio_rest = 8
        elif i[type_start:number_of_char] == 'quarter':
            tempo_ratio_rest = 4
        elif i[type_start:number_of_char] == 'eighth':
            tempo_ratio_rest = 2
        elif i[type_start:number_of_char] == 'sixteenth':
            tempo_ratio_rest = 1
        elif i[type_start:number_of_char] == 'thirty_second':
            tempo_ratio_rest = 0.5
        elif i[type_start:number_of_char] == 'sixty_fourth':
            tempo_ratio_rest = 0.25
        else:
            pass

        # if it is dotted note
        if i[number_of_char - 1] == '.' and i[number_of_char - 2] == '.':
            dot = 2

            if i[type_start:number_of_char - dot] == 'quadruple_whole':
                tempo_ratio_rest = 64
            elif i[type_start:number_of_char - dot] == 'double_whole':
                tempo_ratio_rest = 32
            elif i[type_start:number_of_char - dot] == 'whole':
                tempo_ratio_rest = 16
            elif i[type_start:number_of_char - dot] == 'half':
                tempo_ratio_rest = 8
            elif i[type_start:number_of_char - dot] == 'quarter':
                tempo_ratio_rest = 4
            elif i[type_start:number_of_char - dot] == 'eighth':
                tempo_ratio_rest = 2
            elif i[type_start:number_of_char - dot] == 'sixteenth':
                tempo_ratio_rest = 1
            elif i[type_start:number_of_char - dot] == 'thirty_second':
                tempo_ratio_rest = 0.5
            elif i[type_start:number_of_char - dot] == 'sixty_fourth':
                tempo_ratio_rest = 0.25
            else:
                pass

        elif i[number_of_char - 1] == '.' and not i[number_of_char - 2] == '.':
            dot = 1

            if i[type_start:number_of_char - dot] == 'quadruple_whole':
                tempo_ratio_rest = 64
            elif i[type_start:number_of_char - dot] == 'double_whole':
                tempo_ratio_rest = 32
            elif i[type_start:number_of_char - dot] == 'whole':
                tempo_ratio_rest = 16
            elif i[type_start:number_of_char - dot] == 'half':
                tempo_ratio_rest = 8
            elif i[type_start:number_of_char - dot] == 'quarter':
                tempo_ratio_rest = 4
            elif i[type_start:number_of_char - dot] == 'eighth':
                tempo_ratio_rest = 2
            elif i[type_start:number_of_char - dot] == 'sixteenth':
                tempo_ratio_rest = 1
            elif i[type_start:number_of_char - dot] == 'thirty_second':
                tempo_ratio_rest = 0.5
            elif i[type_start:number_of_char - dot] == 'sixty_fourth':
                tempo_ratio_rest = 0.25
            else:
                pass
        else:
            pass

        return tempo_ratio_rest

    @staticmethod
    def get_keySignature_tempo(kS):
        i = kS
        if i[13:15] == "Ab":
            tempo_KS = 0.033
        elif i[13:15] == "Bb":
            tempo_KS = 0.016
        elif i[13:15] == "Db":
            tempo_KS = 0.041
        elif i[13:15] == "Eb":
            tempo_KS = 0.025
        elif i[13:15] == "Gb":
            tempo_KS = 0.050
        elif i[13:15] == "Cb":
            tempo_KS = 0.058
        elif i[13:15] == "C#":
            tempo_KS = 0.060
        elif i[13:15] == "F#":
            tempo_KS = 0.051
        elif i[13:14] == "A":
            tempo_KS = 0.027
        elif i[13:14] == "B":
            tempo_KS = 0.043
        elif i[13:14] == "C":
            tempo_KS = 0
        elif i[13:14] == "D":
            tempo_KS = 0.018
        elif i[13:14] == "E":
            tempo_KS = 0.035
        elif i[13:14] == "F":
            tempo_KS = 0.008
        elif i[13:14] == "G":
            tempo_KS = 0.01
        else:
            pass

        return tempo_KS

    @staticmethod
    def get_timeSignature_tempo(tS):
        i = tS
        if i[14:16].isdigit() and i[17:19].isdigit():
            tempo_TS = 0.022
        elif i[14:16].isdigit() and i[17].isdigit():
            tempo_TS = 0.022
        elif i[14].isdigit() and i[16:18].isdigit():
            tempo_TS = 0.022
        elif i[14].isdigit() and i[16].isdigit():
            tempo_TS = 0.014
        elif i[14] == "C":
            tempo_TS = 0.014
        elif i[14:16] == "C/":
            tempo_TS = 0.014
        else:
            pass

        return tempo_TS
