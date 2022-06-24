# call dictionary which built in read_document() at main.py

# work with generate_musicxml.py to convert the semantic text to MusicXML and generate it into xml file

class Semantic_To_Musicxml:

    @staticmethod
    def get_note(note):
        number_of_char = len(note)
        alter_value = 0
        note_types = ""
        note_types1 = ""
        dot = 0

        # check grace is present, remove it when found it
        if note[0:5] == "grace":
            j = note.replace("grace", "")
        else:
            j = note

        # check _fermata is present, remove it when found it
        if note[number_of_char - 8:number_of_char] == "_fermata":
            i = j.replace("_fermata", "")
        else:
            i = j

        # getting step eg: A, B, C, D, E, F, G
        step = (i[5])

        # getting octave eg: 1, 2, 3, 4, 5, 6, 7
        if i[6].isdigit():
            octave = (i[6])
            alter_status = False
            type_start = 8
        else:
            octave = (i[7])
            alter_status = True
            type_start = 9

        # getting alter_value eg: 1,-1
        if alter_status:
            if i[6] == "#":
                alter_value = 1
            elif i[6] == "b":
                alter_value = -1
            else:
                pass

        # getting type eg: quadruple_whole, whole, half, quarter, eighth, \
        # sixteenth, thirty_second, sixty_fourth
        if i[type_start:number_of_char] == 'quadruple_whole':
            note_types = 'long'
        elif i[type_start:number_of_char] == 'double_whole':
            note_types = 'breve'
        elif i[type_start:number_of_char] == 'whole':
            note_types = (i[type_start:number_of_char])
        elif i[type_start:number_of_char] == 'half':
            note_types = (i[type_start:number_of_char])
        elif i[type_start:number_of_char] == 'quarter':
            note_types = (i[type_start:number_of_char])
        elif i[type_start:number_of_char] == 'eighth':
            note_types = (i[type_start:number_of_char])
        elif i[type_start:number_of_char] == 'sixteenth':
            note_types = "16th"
        elif i[type_start:number_of_char] == 'thirty_second':
            note_types = "32th"
        elif i[type_start:number_of_char] == 'sixty_fourth':
            note_types = "64th"
        else:
            pass

        if i[number_of_char - 1] == '.' and i[number_of_char - 2] == '.':
            dot = 2
            # for MusicXML
            note_types = i[type_start:number_of_char-dot]
            # for MusicXML tempo
            note_types1 = (i[type_start:number_of_char])
            if i[type_start:number_of_char - dot] == 'quadruple_whole':
                note_types = 'long'
            elif i[type_start:number_of_char - dot] == 'double_whole':
                note_types = 'breve'
            elif i[type_start:number_of_char - dot] == 'whole':
                note_types = 'whole'
            elif i[type_start:number_of_char - dot] == 'half':
                note_types = 'half'
            elif i[type_start:number_of_char - dot] == 'quarter':
                note_types = 'quarter'
            elif i[type_start:number_of_char - dot] == 'eighth':
                note_types = 'eighth'
            elif i[type_start:number_of_char - dot] == 'sixteenth':
                note_types = '16th'
            elif i[type_start:number_of_char - dot] == 'thirty_second':
                note_types = '32th'
            elif i[type_start:number_of_char - dot] == 'sixty_fourth':
                note_types = '64th'
            else:
                pass

        elif i[number_of_char - 1] == '.' and not i[number_of_char - 2] == '.':
            dot = 1
            # for MusicXML
            note_types = i[type_start:number_of_char - dot]
            # for MusicXML tempo
            note_types1 = (i[type_start:number_of_char])
            if i[type_start:number_of_char - dot] == 'quadruple_whole':
                note_types = 'long'
            elif i[type_start:number_of_char - dot] == 'double_whole':
                note_types = 'breve'
            elif i[type_start:number_of_char - dot] == 'whole':
                note_types = 'whole'
            elif i[type_start:number_of_char - dot] == 'half':
                note_types = 'half'
            elif i[type_start:number_of_char - dot] == 'quarter':
                note_types = 'quarter'
            elif i[type_start:number_of_char - dot] == 'eighth':
                note_types = 'eighth'
            elif i[type_start:number_of_char - dot] == 'sixteenth':
                note_types = '16th'
            elif i[type_start:number_of_char - dot] == 'thirty_second':
                note_types = '32th'
            elif i[type_start:number_of_char - dot] == 'sixty_fourth':
                note_types = '64th'
            else:
                pass

        else:
            pass

        return step, alter_value, octave, note_types, dot, note_types1

    @staticmethod
    def get_clef(clef):
        i = clef
        sign = i[5]
        line = i[6]

        return sign, line

    @staticmethod
    def get_rest(rest):
        number_of_char = len(rest)
        type_start = 5
        dot = 0
        rest_types = ""
        rest_types1 = ""

        # check _fermata is present, remove it when found it
        if rest[number_of_char-8:number_of_char] == "_fermata":
            i = rest.replace("_fermata", "")
        else:
            i = rest

        # getting type eg: quadruple_whole, whole, half, quarter, eighth, sixteenth, thirty_second, sixty_fourth
        if i[type_start:number_of_char] == 'quadruple_whole':
            rest_types = 'long'
        elif i[type_start:number_of_char] == 'double_whole':
            rest_types = 'breve'
        elif i[type_start:number_of_char] == 'whole':
            rest_types = (i[type_start:number_of_char])
        elif i[type_start:number_of_char] == 'half':
            rest_types = (i[type_start:number_of_char])
        elif i[type_start:number_of_char] == 'quarter':
            rest_types = (i[type_start:number_of_char])
        elif i[type_start:number_of_char] == 'eighth':
            rest_types = (i[type_start:number_of_char])
        elif i[type_start:number_of_char] == 'sixteenth':
            rest_types = "16th"
        elif i[type_start:number_of_char] == 'thirty_second':
            rest_types = "32th"
        elif i[type_start:number_of_char] == 'sixty_fourth':
            rest_types = "64th"
        else:
            pass

        if i[number_of_char - 1] == '.' and i[number_of_char - 2] == '.':
            dot = 2
            # for MusicXML
            rest_types = (i[type_start:number_of_char-dot])
            # for MusicXML tempo
            rest_types1 = (i[type_start:number_of_char])

            if i[type_start:number_of_char - dot] == 'quadruple_whole':
                rest_types = 'long'
            elif i[type_start:number_of_char - dot] == 'double_whole':
                rest_types = 'breve'
            elif i[type_start:number_of_char - dot] == 'whole':
                rest_types = 'whole'
            elif i[type_start:number_of_char - dot] == 'half':
                rest_types = 'half'
            elif i[type_start:number_of_char - dot] == 'quarter':
                rest_types = 'quarter'
            elif i[type_start:number_of_char - dot] == 'eighth':
                rest_types = 'eighth'
            elif i[type_start:number_of_char - dot] == 'sixteenth':
                rest_types = '16th'
            elif i[type_start:number_of_char - dot] == 'thirty_second':
                rest_types = '32th'
            elif i[type_start:number_of_char - dot] == 'sixty_fourth':
                rest_types = '64th'
            else:
                pass

        elif i[number_of_char - 1] == '.' and not i[number_of_char - 2] == '.':
            dot = 1
            # for MusicXML
            rest_types = (i[type_start:number_of_char - dot])
            # for MusicXML tempo
            rest_types1 = (i[type_start:number_of_char - dot])

            if i[type_start:number_of_char - dot] == 'quadruple_whole':
                rest_types = 'long'
            elif i[type_start:number_of_char - dot] == 'double_whole':
                rest_types = 'breve'
            elif i[type_start:number_of_char - dot] == 'whole':
                rest_types = 'whole'
            elif i[type_start:number_of_char - dot] == 'half':
                rest_types = 'half'
            elif i[type_start:number_of_char - dot] == 'quarter':
                rest_types = 'quarter'
            elif i[type_start:number_of_char - dot] == 'eighth':
                rest_types = 'eighth'
            elif i[type_start:number_of_char - dot] == 'sixteenth':
                rest_types = '16th'
            elif i[type_start:number_of_char - dot] == 'thirty_second':
                rest_types = '32th'
            elif i[type_start:number_of_char - dot] == 'sixty_fourth':
                rest_types = '64th'
            else:
                pass

        else:
            pass

        return rest_types, dot, rest_types1

    @staticmethod
    def get_keySignature(kS):
        i = kS
        if i[13:15] == "Ab":
            fifths = '-4'
        elif i[13:15] == "Bb":
            fifths = '-2'
        elif i[13:15] == "Db":
            fifths = '-5'
        elif i[13:15] == "Eb":
            fifths = '-3'
        elif i[13:15] == "Gb":
            fifths = '-6'
        elif i[13:15] == "Cb":
            fifths = '-7'
        elif i[13:15] == "C#":
            fifths = '7'
        elif i[13:15] == "F#":
            fifths = '6'
        elif i[13:14] == "A":
            fifths = '3'
        elif i[13:14] == "B":
            fifths = '5'
        elif i[13:14] == "C":
            fifths = '0'
        elif i[13:14] == "D":
            fifths = '2'
        elif i[13:14] == "E":
            fifths = '4'
        elif i[13:14] == "F":
            fifths = '-1'
        elif i[13:14] == "G":
            fifths = '1'
        else:
            pass

        return fifths

    @staticmethod
    def get_timeSignature(tS):
        i = tS
        if i[14:16].isdigit() and i[17:19].isdigit():
            beats = i[14:16]
            beat_types = i[17:19]
        elif i[14:16].isdigit() and i[17].isdigit():
            beats = i[14:16]
            beat_types = i[17]
        elif i[14].isdigit() and i[16:18].isdigit():
            beats = i[14]
            beat_types = i[16:18]
        elif i[14].isdigit() and i[16].isdigit():
            beats = i[14]
            beat_types = i[16]
        elif i[14] == "C":
            beats = "4"
            beat_types = "4"
        elif i[14:16] == "C/":
            beats = "2"
            beat_types = "2"
        else:
            pass

        return beats, beat_types
