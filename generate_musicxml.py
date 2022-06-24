import xml.etree.ElementTree as xml
from semantic_to_musicxml import Semantic_To_Musicxml

STM = Semantic_To_Musicxml()


class Generate_Musicxml:

    @staticmethod
    def GenerateXML(fileName, music_symbols_list, bpm):
        barline_count = 1

        beatsPerMinute = bpm

        duration = {
            "long..": 28.0,
            "long.": 24.0,
            "long": 16.0,
            "breve..": 14.0,
            "breve.": 12.0,
            "breve": 8.0,
            "whole..": 7.0,
            "whole.": 6.0,
            "whole": 4.0,
            "half..": 3.5,
            "half.": 3.0,
            "half": 2.0,
            "quarter..": 1.75,
            "quarter.": 1.5,
            "quarter": 1.0,
            "eighth..": 0.875,
            "eighth.": 0.75,
            "eighth": 0.5,
            "sixteenth..": 0.4375,
            "sixteenth.": 0.375,
            "16th": 0.25,
            "thirty_second..": 0.21875,
            "thirty_second.": 0.1875,
            "32th": 0.125,
            "sixty_fourth..": 0.109375,
            "sixty_fourth.": 0.09375,
            "64th": 0.0625,
        }

        # initialization of xml
        root = xml.Element("score-partwise", version="4.0")
        c_starting = xml.Element("part-list")
        root.append(c_starting)

        c_setting_score_part = xml.SubElement(c_starting, "score-part", id="P1")

        type1 = xml.SubElement(c_setting_score_part, "part-name")
        type1.text = "Music"  # choosing the instrument sound

        c_music_score_part = xml.Element("part", id="P1")
        root.append(c_music_score_part)
        globals()[f"c_measure_{barline_count}"] = xml.SubElement(c_music_score_part, "measure",
                                                                 number=str(barline_count))

        c_attribute = xml.SubElement(globals()[f"c_measure_{barline_count}"], "attributes")
        type_divisions = xml.SubElement(c_attribute, "divisions")
        type_divisions.text = "1"

        last_symbols = music_symbols_list[len(music_symbols_list) - 1]

        if last_symbols == "barline":
            music_symbols_list.pop(len(music_symbols_list) - 1)

            # print(music_symbols_list)

        for i in music_symbols_list:
            # print(i)
            if i[0:7] == "barline":
                barline_count += 1
                globals()[f"c_measure_{barline_count}"] = xml.SubElement(c_music_score_part, "measure",
                                                                         number=str(barline_count))

            elif i[0:5] == "clef-" or i[0:13] == "keySignature-" or i[0:14] == "timeSignature-":

                if i[0:5] == "clef-":
                    sign, line = STM.get_clef(i)
                    # print(sign, line)

                    type_clef = xml.SubElement(c_attribute, "clef")
                    type_sign = xml.SubElement(type_clef, "sign")
                    type_sign.text = sign

                    type_line = xml.SubElement(type_clef, "sign")
                    type_line.text = line

                elif i[0:13] == "keySignature-":
                    fifths = STM.get_keySignature(i)
                    # print(fifths)

                    type_kS = xml.SubElement(c_attribute, "key")
                    type_fifths = xml.SubElement(type_kS, "fifths")
                    type_fifths.text = fifths

                    type_mode = xml.SubElement(type_kS, "mode")
                    type_mode.text = "major"

                elif i[0:14] == "timeSignature-":
                    beats, beat_type = STM.get_timeSignature(i)
                    # print(beats, beat_type)

                    type_tS = xml.SubElement(c_attribute, "time")
                    type_beats = xml.SubElement(type_tS, "beats")
                    type_beats.text = beats

                    type_beat_type = xml.SubElement(type_tS, "beat-type")
                    type_beat_type.text = beat_type

                else:
                    pass

            else:
                if i[0:5] == "grace":
                    j = i.replace("grace", "")
                    i = j

                if i[0:5] == "note-":
                    step, alter_value, octave, note_types, dot, note_types1 = STM.get_note(i)
                    # print(step, alter_value, octave, note_types, dot, note_types1)

                    c_note = xml.SubElement(globals()[f"c_measure_{barline_count}"], "note")
                    c_pitch = xml.SubElement(c_note, "pitch")
                    type_step = xml.SubElement(c_pitch, "step")
                    type_step.text = step
                    type_alter = xml.SubElement(c_pitch, "alter")
                    type_alter.text = str(alter_value)
                    type_octave = xml.SubElement(c_pitch, "octave")
                    type_octave.text = octave

                    type_duration = xml.SubElement(c_note, "duration")

                    if dot < 0:
                        noteDurationSeconds = (60.0 / beatsPerMinute) * duration[note_types1]*2
                    else:
                        noteDurationSeconds = (60.0 / beatsPerMinute) * duration[note_types]*2

                    type_duration.text = str(noteDurationSeconds)

                    type_note = xml.SubElement(c_note, "type")
                    type_note.text = note_types

                    if dot == 1:
                        xml.SubElement(c_note, "dot")
                    if dot == 2:
                        xml.SubElement(c_note, "dot")
                        xml.SubElement(c_note, "dot")
                    # print("nothing")

                elif i[0:5] == "rest-":
                    rest_types, dot, rest_types1 = STM.get_rest(i)
                    # print(rest_type, dot, rest_type1)

                    c_rest = xml.SubElement(globals()[f"c_measure_{barline_count}"], "note")
                    xml.SubElement(c_rest, "rest")

                    type_duration = xml.SubElement(c_rest, "duration")
                    if dot < 0:
                        restDurationSeconds = (60.0 / beatsPerMinute) * duration[rest_types1]*2
                    else:
                        restDurationSeconds = (60.0 / beatsPerMinute) * duration[rest_types]*2
                    type_duration.text = str(restDurationSeconds)

                    type_note = xml.SubElement(c_rest, "type")
                    type_note.text = rest_types

                    if dot == 1:
                        xml.SubElement(c_note, "dot")
                    if dot == 2:
                        xml.SubElement(c_note, "dot")
                        xml.SubElement(c_note, "dot")

                    # print("nothing")

                else:
                    pass

        tree = xml.ElementTree(root)
        with open(fileName, "wb") as files:
            files.write(
                '<?xml version="1.0" encoding="UTF-8" standalone="no"?><!DOCTYPE score-partwise PUBLIC' \
                '\n"-//Recordare//DTD MusicXML 4.0 Partwise//EN"' \
                '\n"http://www.musicxml.org/dtds/partwise.dtd">'.encode('utf8'))
            tree.write(files, 'utf-8')

