from graphics import *
from multiprocessing import Process
import time
import winsound
import math


width = 800
height = 800
radius = 200
chord_set = []
beats_set = []
BPM = 0


def chord_sequence_visualizer_input():
    ask_for_notes()
    win = GraphWin("Program", width, height)
    draw_clock(win, 12)
    note_names(win)
    draw_chord_sequence(win, chord_set)

 
def chord_sequence_visualizer_file():
    if __name__ == '__main__':
        notes_from_file()
        win = GraphWin("Program", width, height)
        draw_clock(win,12)
        note_names(win)
        SoundProcess = Process(target = background_music)
        SoundProcess.start()
        draw_chord_sequence_file(win, chord_set, beats_set, BPM)

def rhythm_visualizer(beatlist, bpm):
    if __name__ == '__main__':
        win = GraphWin("Program", width, height)
        draw_clock(win, len(beatlist))
        points_x = points_around_circle_x(radius, width/2, len(beatlist))
        points_y = points_around_circle_y(radius, height/2, len(beatlist))
        pulselist = []
        for a in range(0, len(beatlist)):
            if beatlist[a] == 1:
                fill_circ = Circle(Point(points_x[a],points_y[a]), 5)
                fill_circ.setFill("black")
                fill_circ.draw(win)
                pulselist.append(a)
        for a in range(0, len(pulselist) - 1):
            line = Line(Point(points_x[pulselist[a]],points_y[pulselist[a]]),Point(points_x[pulselist[a+1]],points_y[pulselist[a+1]]))
            line.draw(win)
        line = Line(Point(points_x[pulselist[-1]],points_y[pulselist[-1]]),Point(points_x[pulselist[0]],points_y[pulselist[0]]))
        line.draw(win)
        pulse = 0
        while 1 == 1:   
            circle = Circle(Point(points_x[pulse], points_y[pulse]), 15)
            circle.draw(win)
            if beatlist[pulse] == 1:
                SoundProcess = Process(target = pulse_noise)
                SoundProcess.start()
            time.sleep(60/bpm)
            circle.undraw()
            if pulse == len(beatlist) - 1:
                pulse = 0
            else:
                pulse = pulse + 1


def Bjorklunds_Algorithm(n,k):
    beatlist = []
    for x in range(0,k):
        beatlist.append([1])
    if n-k <= k:
        for x in range(0,n-k):
            beatlist[x].append(0)
    else:
        z = n-k
        while z > 0:
            for x in range(0,k):
                if z > 0:
                    beatlist[x].append(0)
                    z = z - 1
    while beatlist[-1] == beatlist[-2] and beatlist[0] != beatlist[-1]:
        rlist = []
        remainder = beatlist[-1]
        while remainder in beatlist:
            rlist.append(remainder)
            beatlist.remove(remainder)      
        if len(rlist) <= len(beatlist):
            for x in range(0,len(rlist)):
                beatlist[x] = beatlist[x] + remainder
        else:
            z = len(rlist)
            while z > 0:
                for x in range(0,len(beatlist)):
                    if z > 0:
                        beatlist[x] = beatlist[x] + remainder
                        z = z - 1
        if len(beatlist) == 1:
            break
    euclidean_rhythm = []
    for x in beatlist:
        euclidean_rhythm = euclidean_rhythm + x
    return euclidean_rhythm


def ask_for_notes():
    prog_num = int(input('How many pitch class sets in progression? '))
    for x in range(0, prog_num):
        user_input = input('Enter the set of notes: ')
        note_set = list(map(str,user_input.split(',')))
        chord_set.append(note_set)


def notes_from_file():
    file = open("song.txt","r")
    lines = file.readlines()
    for line in lines:
        if line == lines[0]:
            global BPM
            BPM = float(line)
        else:
            words = line.split()
            chord_set.append(words[0])
            beats_set.append(float(words[1]))
            

def draw_clock(win, n):
    clock = Circle(Point(width/2, height/2), radius)
    clock.draw(win)
    clock.setFill("white")
    points_x = points_around_circle_x(radius, width/2, n)
    points_y = points_around_circle_y(radius, height/2, n)
    for a in range(0, n):
        circle = Circle(Point(points_x[a], points_y[a]), 5)
        circle.setFill("white")
        circle.draw(win)


def points_around_circle_x(r, x, n):
    points = []
    for a in range(0,n):
        points.append( x + r * math.cos(math.radians(a*360/n-90)) )
    return points


def points_around_circle_y(r, y, n):
    points = []
    for a in range(0,n):
        points.append( y + r * math.sin(math.radians(a*360/n-90)) )
    return points
    

def note_names(win):
    labels_x = points_around_circle_x(radius+40, width/2, 12)
    labels_y = points_around_circle_y(radius+40, height/2, 12)
    note_names = ['A', 'A#/Bb', 'B', 'C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab']
    for x in range(0, 12):
        note_name = Text(Point(labels_x[x], labels_y[x]), note_names[x])
        note_name.draw(win)


def draw_chord(win, notes):
    notes_list = notes
    target_notes = notes_list.copy()
    fill_circle_dict = {}
    line_dict = {}
    note_coordinates_dict = {}
    note_names = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']
    points_x = points_around_circle_x(radius, width/2, 12)
    points_y = points_around_circle_y(radius, height/2, 12)
    for x in range(0, 12):
        note_coordinates_dict[note_names[x]] = Point(points_x[x], points_y[x])
    for a in notes_list:
        target_notes.remove(a)
        fill_circle_dict[a] = Circle(note_coordinates_dict[a], 5)
        fill_circle_dict[a].setFill("black")
        fill_circle_dict[a].draw(win)
        for b in target_notes:
            line_dict[a,b] = Line(note_coordinates_dict[a], note_coordinates_dict[b])
            line_dict[a,b].draw(win)
    key = win.getKey()
    while key != 'space':
        key = win.getKey()  
    for key in line_dict:
        line_dict[key].undraw()
    for key in fill_circle_dict:
        fill_circle_dict[key].undraw()
        

def draw_chord_sequence(win, note_sets):
    while 1==1:
        for x in note_sets:
            draw_chord(win, x)


def draw_chord_file(win, notes, beat, bpm):
    notes_list = notes.split(",")
    target_notes = notes_list.copy()
    fill_circle_dict = {}
    line_dict = {}
    note_coordinates_dict = {}
    note_names = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']
    points_x = points_around_circle_x(radius, width/2, 12)
    points_y = points_around_circle_y(radius, height/2, 12)
    for x in range(0, 12):
        note_coordinates_dict[note_names[x]] = Point(points_x[x], points_y[x])
    for a in notes_list:
        target_notes.remove(a)
        fill_circle_dict[a] = Circle(note_coordinates_dict[a], 5)
        fill_circle_dict[a].setFill("black")
        fill_circle_dict[a].draw(win)
        for b in target_notes:
            line_dict[a,b] = Line(note_coordinates_dict[a], note_coordinates_dict[b])
            line_dict[a,b].draw(win)
    pausetime = beat*60/bpm
    time.sleep(pausetime)
    for key in line_dict:
        line_dict[key].undraw()
    for key in fill_circle_dict:
        fill_circle_dict[key].undraw()


def draw_chord_sequence_file(win, note_sets, beat_sets, bpm):
        for x in range(0, len(note_sets)):
            draw_chord_file(win, note_sets[x], beat_sets[x], bpm)

            
def background_music():
    winsound.PlaySound('song.wav', winsound.SND_FILENAME) 
        

def pulse_noise():
    winsound.PlaySound('pulse.wav', winsound.SND_FILENAME)
    
    



    


