#!/usr/bin/env python
from psychopy import core, visual, event, monitors, sound
import random,math

# set up monitor resolution
mon = monitors.Monitor('lenovoTPE', width = 29.4, distance = 50)
mon.setSizePix([1366,768])
#create a window to draw in
myWin = visual.Window(size=(1366,768), fullscr=True, monitor = mon,
    units = 'height')
#add a mouse listener
mouse = event.Mouse()

#INITIALISE SOME STIMULI
global stimuli, startAngle, startPhase, mdir, opts, cMessage
stimuli = list()
labels = list()
soundsX = list()
soundsY = list()
startAngle = list()
startPhase = list()
mdir = list()
opts = dict()

keyArr = ['f','r','e','s','x','c']

for x in range(6):
    newGrating = visual.GratingStim(
        myWin,tex="sin",mask="gauss",texRes=256,
        units = 'height', opacity = 0,
        pos = (math.cos(x*math.pi/3) * 0.3, math.sin(x*math.pi/3) * 0.3),
        #pos = (random.uniform(-0.8,0.8), random.uniform(-0.5,0.5)),
        size=0.2, sf=[4,0], ori = 0, name='gabor'+str(x))
    labels.append(visual.TextStim(myWin, pos = (
        math.cos(x*math.pi/3) * 0.15, math.sin(x*math.pi/3) * 0.15),
        units = 'height', text = keyArr[x], height = 0.05))
    soundsX.append(None)
    soundsY.append(None)
    stimuli.append(newGrating)
    startPhase.append(random.random())
    startAngle.append(random.uniform(0,180))
    mdir.append(1)

message = visual.TextStim(myWin,pos=(0.0,-0.475),text='Hit Q to quit',
    height = 0.05, alignVert = 'bottom')
trialClock = core.Clock()

fixSpot = visual.GratingStim(myWin,tex=None, mask="gauss",
    size=(0.05,0.05),color='black', units = 'height')
fixSpot.setAutoDraw(True)


#reset mouse clicks
mouse.clickReset()

cs = 0
correctKey = keyArr[cs]
opts['skill'] = float(1)

def pos2log(value):
    if(abs(value) > 0.5):
        value = math.sign(value) * 0.5
    return((math.pow(10,value) - 1)/9)

def resetBlobs(showText=True):
    for x in range(6):
        startAngle[x] = random.uniform(0,360)
        startPhase[x] = random.random()
        mdir[x] = random.choice([-1,1])
        if(showText):
            labels[x].setAutoDraw(True)
        else:
            labels[x].setAutoDraw(False)
        soundsX[x] = sound.SoundPygame(
            value = pos2log(stimuli[x].pos[0])* 300 + 300)
        soundsX[x].setVolume(0.2)
        soundsY[x] = sound.SoundPygame(
            value = pos2log(stimuli[x].pos[1])* 300 + 300)
        soundsY[x].setVolume(0.2)
        stimuli[x].setAutoDraw(True)
        stimuli[x].opacity = 1
        stimuli[x].ori = startAngle[x]
    # stimulus that changes
    opts['cs'] = random.randint(0,5)
    opts['correctKey'] = keyArr[opts['cs']]

description = visual.TextStim(myWin, text =
'''In the following exercise your limit of detection for rotation will be discovered. Six
Gabor patches will appear around the dot at the centre of the screen. Five of
these will be phasing distractors, and one will be a rotating target (see below).
The aim of the exercise is to select the rotating target by pressing the correct
key. The keys that can be pressed are the six keys surrounding D (F,R,E,S,X, 
and C), and correspond to the patch in the same relative direction. A correct
response will reduce the rotation speed and produce a beep. An incorrect
response will increase the rotation speed. After 20 seconds with no response
the exercise will end.'''.replace("\n"," ") +
"\n\nPress any key to continue.",
height = 0.03, pos = (0,0.475), alignVert='top', wrapWidth = 0.8)

nextPhase = False
example1 = visual.GratingStim(
        myWin,tex="sin",mask="gauss",texRes=256,
        opacity = 1, pos = (-0.3, 0), size=0.2, sf=[4,0])
text1 = visual.TextStim(myWin,pos=(-0.3,-0.2),text='Phasing', height = 0.05,
    color = 'darkred')
example2 = visual.GratingStim(
        myWin,tex="sin",mask="gauss",texRes=256,
        opacity = 1, pos = (0.3, 0), size=0.2, sf=[4,0])
text2 = visual.TextStim(myWin,pos=(0.3,-0.2),text='Rotating', height = 0.05,
    color = 'lightblue')
while(not nextPhase):
    example1.setPhase(0.01,'+')
    example2.setOri(0.5,'+')
    description.draw()
    example1.draw()
    text1.draw()
    example2.draw()
    text2.draw()
    for keys in event.getKeys(timeStamped=True):
        if keys[0]in ['escape','q']:
            myWin.close()
            core.quit()
        else:
            nextPhase = True
    message.draw()
    myWin.flip()

nextPhase = False

cMessage = visual.TextStim(myWin, pos = (0.475,-0.475), text="%0.2f" % opts['skill'],
    height = 0.05, alignVert = 'bottom', alignHoriz = 'right')
cMessage.setAutoDraw(True)
resetBlobs()
trialClock.reset()

#repeat drawing for each frame
while(not nextPhase):
    t = float(trialClock.getTime()) / 20
    logt = (pow(10,t) - 1)/9
    #stimuli[0].setOpacity(logt)
    for x in range(6):
        if(x != opts['cs']):
            stimuli[x].setPhase(t*math.pi*opts['skill'] + startPhase[x])
    stimuli[opts['cs']].setOri(180*t*opts['skill']*mdir[cs] + startAngle[cs])
    message.draw()
    #handle key presses each frame
    for keys in event.getKeys(timeStamped=True):
        if keys[0]in ['escape','q']:
            myWin.close()
            core.quit()
        elif (keys[0] == opts['correctKey']):
            soundsX[opts['cs']].play()
            soundsY[opts['cs']].play()
            trialClock.reset()
            opts['skill'] *= 0.9
            resetBlobs(opts['skill'] > 0.5)
            cMessage.setText("%0.2f" % opts['skill'])
        elif(keys[0] in keyArr):
            trialClock.reset()
            opts['skill'] /= 0.9
            resetBlobs(opts['skill'] > 0.5)
            cMessage.setText("%0.2f" % opts['skill'])
        cMessage.draw()
    if(trialClock.getTime() >= 20):
        nextPhase = True
    myWin.flip()