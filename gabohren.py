#!/usr/bin/env python
from psychopy import core, visual, event, monitors, sound
import random,math,numpy

# set up monitor resolution
mon = monitors.Monitor('lenovoTPE', width = 29.4, distance = 50)
mon.setSizePix([1366,768])
#create a window to draw in
myWin = visual.Window(fullscr=True, monitor = mon, units = 'height')
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

keyArr = ['6','9','8','7','4','1','2','3']

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

opts['cs'] = 0
correctKey = keyArr[opts['cs']]
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
        stimuli[x].opacity = 1
        stimuli[x].ori = startAngle[x]
    # stimulus that changes
    opts['cs'] = random.randint(0,5)
    opts['correctKey'] = keyArr[opts['cs']]

def inStim(pointer, target):
    pos1 = pointer.getPos()
    pos2 = target.pos
    return(event.xydist(pos1,pos2) < 0.05)

def task1():
    description = visual.TextStim(myWin, text =
    '''In the following exercise your limit of detection for rotation
    will be discovered. Six Gabor patches will appear around the dot
    at the centre of the screen. Five of these will be phasing
    distractors, and one will be a rotating target (see below).  The
    aim of the exercise is to select the rotating target by pressing
    the correct key. The keys that can be pressed are the six keys
    surrounding D (F,R,E,S,X, and C), and correspond to the patch in
    the same relative direction. A correct response will reduce the
    rotation speed and produce a beep. An incorrect response will
    increase the rotation speed. After 20 seconds with no response the
    exercise will end.'''.replace("\n    "," ") +
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

    cMessage = visual.TextStim(myWin, pos = (0.475,-0.475),
                               text="%0.2f" % opts['skill'],
                               height = 0.05, alignVert = 'bottom',
                               alignHoriz = 'right')
    resetBlobs()
    trialClock.reset()

    #repeat drawing for each frame
    while(not nextPhase):
        t = float(trialClock.getTime()) / 20
        logt = (pow(10,t) - 1)/9
        #stimuli[0].setOpacity(logt)
        stimuli[opts['cs']].setOri(180*t*opts['skill']*mdir[opts['cs']] +
                                   startAngle[opts['cs']])
        for x in range(6):
            if(x != opts['cs']):
                stimuli[x].setPhase(t*math.pi*opts['skill']*mdir[x] +
                                    startPhase[x])
            stimuli[x].draw()
        message.draw()
        # handle mouse clicks
        buttons, times = mouse.getPressed(getTime = True)
        inside = False
        correct = False
        if(buttons[0] and (times[0] > 0.1)):
            for x in range(6):
                if(inStim(mouse,stimuli[x])):
                    inside = True
                    correct = (x == opts['cs'])
            mouse.clickReset()
        #handle key presses each frame
        keys = event.getKeys(timeStamped=True)
        for k in keys:
            if(k[0] in ['escape','q']):
                myWin.close()
                core.quit()
            if(k[0] in keyArr):
                inside = True
                correct = (k[0] == opts['correctKey'])
        if(inside):
            if(correct):
                soundsX[opts['cs']].play()
                soundsY[opts['cs']].play()
                opts['skill'] *= 0.9
            else:
                opts['skill'] /= 0.9
            trialClock.reset()
            resetBlobs(opts['skill'] > 0.5)
        if(trialClock.getTime() >= 20):
            nextPhase = True
        cMessage.setText("%0.2f" % opts['skill'])
        cMessage.draw()
        myWin.flip()

def resetBlobs2(blobArray, featureDict, rangeDict):
    n = len(blobArray)
    poss = random.sample(range(n),n)
    for x in range(n):
        blob = blobArray[x]
        p = poss[x]
        if(x == 0):
            featureDict['correctKey'] = featureDict['keyArr'][p]
            opts['soundX'] = sound.SoundPygame(
                value = pos2log(blob.pos[0])* 300 + 300)
            opts['soundX'].setVolume(0.2)
            opts['soundY'] = sound.SoundPygame(
                value = pos2log(blob.pos[1])* 300 + 300)
            opts['soundY'].setVolume(0.2)
        blob.pos = (math.cos(p*math.pi/(n/2)) * 0.3,
            math.sin(p*math.pi/(n/2)) * 0.3)
        for m in rangeDict:
            if(m == 'ori'):
                blob.ori = random.uniform(rangeDict[m][0],rangeDict[m][1])
            else:
                if(rangeDict[m][2] == 'binary'):
                    featureDict[m][x] = random.choice(rangeDict[m][0:2])

def task2():
    numPatches = 8
    features = dict()
    for opt in ['mdir','label','keyArr']:
        features[opt] = [None] * numPatches

    features['keyArr'] = ['6','9','8','7','4','1','2','3']
    features['correctKey'] = None

    for x in range(numPatches):
        features['label'][x] = visual.TextStim(myWin, pos = (
            math.cos(x*math.pi/(numPatches/2)) * 0.15,
            math.sin(x*math.pi/(numPatches/2)) * 0.15),
            units = 'height', text = ((features['keyArr'])[x]), height = 0.05)

    description = visual.TextStim(myWin, text =
    '''In the following exercise your limit of detection for contrast
    will be discovered. Six patches will appear around the dot at the
    centre of the screen. Five of these will be non-Gabor distractors
    with a triangular carrier wave, and one will be a Gabor target
    with a sine carrier wave (see below).  The aim of the exercise is
    to select the gabor target by pressing the correct key. The keys
    that can be pressed are the six keys surrounding D (F,R,E,S,X, and
    C), and correspond to the patch in the same relative direction. A
    correct response will reduce the contrast and produce a beep. An
    incorrect response will increase the contrast. After 20 seconds
    with no response the exercise will end.'''.replace("\n    "," ") +
    "\n\nPress any key to continue.",
    height = 0.03, pos = (0,0.475), alignVert='top', wrapWidth = 0.8)

    nextPhase = False
    example1 = visual.GratingStim(
            myWin,tex="tri",mask="gauss",texRes=256, ori = 30,
            opacity = 1, pos = (-0.3, 0), size=0.2, sf=[4,0])
    text1 = visual.TextStim(myWin,pos=(-0.3,-0.2),text='Distractor', height = 0.05,
        color = 'darkred')
    example2 = visual.GratingStim(
            myWin,tex="sin",mask="gauss",texRes=256, ori = 30,
            opacity = 1, pos = (0.3, 0), size=0.2, sf=[4,0])
    text2 = visual.TextStim(myWin,pos=(0.3,-0.2),text='Gabor', height = 0.05,
        color = 'lightblue')

    while(not nextPhase):
        example1.setOri(0.5,'+')
        example1.setPhase(0.01,'+')
        example2.setOri(0.5,'+')
        example2.setPhase(0.01,'+')
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

    opts['score'] = 0
    cMessage = visual.TextStim(myWin, pos = (0.475,-0.475),
        text="%0.3f" % opts['skill'],
        height = 0.05, alignVert = 'bottom', alignHoriz = 'right')
    sMessage = visual.TextStim(myWin, pos = (-0.475,-0.475),
        text="%d" % opts['score'],
        height = 0.05, alignVert = 'bottom', alignHoriz = 'left')
    patches = [None] * numPatches
    ranges = {'ori': (0,180,'linear'), 'mdir': (-1,1,'binary')}
    patches[0] = visual.GratingStim(
            myWin,tex="sin",mask="gauss",texRes=256, ori = 30,
            opacity = 1, pos = (0.3, 0), size=0.15, sf=[4,0])
    for x in range(1,numPatches):
        patches[x] = visual.GratingStim(
            myWin,tex="tri",mask="gauss",texRes=256, ori = 30,
            opacity = 1, pos = (0.3, 0), size=0.15, sf=[4,0])
    resetBlobs2(patches, features, ranges)

    nextPhase = False
    trialClock.reset()
    opts['skill'] = 1
    cMessage.setText("%0.2f" % opts['skill'])
    while(not nextPhase):
        t = float(trialClock.getTime()) / 5
        logt = (pow(10,t) - 1)/9
        op = (t * opts['skill']) if (t < 1) else opts['skill']
        for x in range(numPatches):
            patches[x].setOpacity(op)
            patches[x].setOri(0.5*features['mdir'][x],'+')
            patches[x].setPhase(0.01,'+')
            patches[x].draw()
            if (opts['skill'] > 0.5):
                features['label'][x].draw()
        cMessage.draw()
        sMessage.draw()
        for keys in event.getKeys(timeStamped=True):
            keys = (keys[0].replace("num_",""),keys[1])
            if keys[0]in ['escape','q']:
                myWin.close()
                core.quit()
            elif (keys[0] == features['correctKey']):
                opts['skill'] *= 0.9
                opts['score'] += 1
                trialClock.reset()
                resetBlobs2(patches, features, ranges)
                sMessage.setText("%d" % opts['score'])
                cMessage.setText("%0.3f" % opts['skill'])
                opts['soundX'].play()
                opts['soundY'].play()
            elif(keys[0] in features['keyArr']):
                opts['skill'] /= 0.9
                opts['score'] -= 2
                trialClock.reset()
                resetBlobs2(patches, features, ranges)
                sMessage.setText("%d" % opts['score'])
                cMessage.setText("%0.3f" % opts['skill'])
        if(trialClock.getTime() >= 20):
            nextPhase = True
        myWin.flip()

#task1()
task2()
