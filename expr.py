from psychopy import visual, core, logging, event, colors
from psychopy.colors import Color
import numpy as np
import random
from psycholib import CombinedStim, tuple_mul

path = '/home/silver/Documents/Projects/ARL/'

anchor_center = [(0,0)]
ext_center = 0.16
anchor_rect = [(+ext_center,0),
               (0,+ext_center),
               (-ext_center,0),
               (0,-ext_center)]

ext_rect = (0.05, 0.05)
ext_vertical = (0.0, 0.04)
ext_horizontal = (0.04, 0.0)
ext_para = (0.03, 0.03)

anchor_blue = []
for direct in range(4):
    anchor_blue.append([])
    for shift in range(-1,2):
        anchor_blue[direct].append( (anchor_rect[direct][0],anchor_rect[direct][1]+ext_para[1]*shift) )
anchor_yellow = []
for direct in range(4):
    anchor_yellow.append([])
    for shift in range(-1,2):
        anchor_yellow[direct].append( (anchor_rect[direct][0]+ext_para[0]*shift,anchor_rect[direct][1]) )

def build_rect(win, anchor, ext):
    temp = ()
    for direct in range(4):
        temp += ( visual.Rect(win, pos=anchor[direct], size=tuple_mul(2, *ext), lineWidth=0.01, lineColor='white'), )
    return CombinedStim(*temp)

def build_line(win, anchor, ext, color):
    temp = ()
    for para in range(3):
        temp += ( visual.Line(win,
                              start=(anchor[para][0]-ext[0], anchor[para][1]-ext[1]),
                              end=(anchor[para][0]+ext[0], anchor[para][1]+ext[1]),
                              lineWidth=0.05,
                              lineColor=color), )
    return CombinedStim(*temp)

def test(win):
    for i in range(100):
        rect = build_rect(win, anchor_rect, ext_rect)
        line = build_line(win, anchor_yellow[0], ext_vertical, color='yellow')
        rect.draw()
        line.draw()
        '''
        pp = visual.Line(win,
                              start=(anchor_blue[0][0][0]-ext_horizontal[0], anchor_blue[0][0][1]-ext_horizontal[0]),
                              end=(anchor_blue[0][0][0]+ext_horizontal[0], anchor_blue[0][0][1]+ext_horizontal[1]),
                              lineWidth=0.05,
                              lineColor='blue')
        pp.draw()
        '''
        win.flip()
        core.wait(5)

def proc(win, num_trials=80, reversal=40, init_ans='blue', ac_ratio=0.8):
    def rating(choice, answer):
        if choice == 'b' and answer == 'blue':
            return True
        if choice == 'y' and answer == 'yellow':
            return True
        return False
    def reverse(ans):
        if ans == 'blue':
            return 'yellow'
        return 'blue'
    num_ac = 0

    rect = build_rect(win, anchor_rect, ext_rect)
    img_ac = visual.ImageStim(win, image=path+'ac.png', size=(0.1,0.13))
    img_wa = visual.ImageStim(win, image=path+'wa.png', size=(0.1,0.13))
    event.globalKeys.add(key='q', modifiers=['ctrl'], func=core.quit)

    line_blue = []
    line_yellow = []
    for idx in range(4):
        line_blue.append( build_line(win, anchor_blue[idx], ext_horizontal, color='blue') )
        line_yellow.append( build_line(win, anchor_yellow[idx], ext_vertical, color='yellow') )

    rate = True
    correct_ans = init_ans
    last_choice = None
    W_S = 0
    L_S = 0
    PerErr = 0
    pe_cnt = 0
    for trial in range(1, num_trials+1):
        '''
        Draw images
        '''
        rect.draw()
        if rate == True:
            img_ac.draw()
        else:
            img_wa.draw()
        rand_blue = random.randint(0,3)
        rand_yellow = (rand_blue + random.randint(1,3)) % 4
        line_blue[rand_blue].draw()
        line_yellow[rand_yellow].draw()

        win.flip()

        choice = event.waitKeys(keyList=['b', 'y'])[0]
        rate = rating(choice, correct_ans)
        if random.uniform(0.0, 1.0) > ac_ratio:
            rate = rate ^ True
        # Win-Stay and Lose-Shift
        if last_choice == choice and rate == True:
            W_S += 1
        if last_choice != choice and rate == False:
            L_S += 1
        last_choice = choice
        if rate == True:
            num_ac += 1
        # Perservative Error
        if trial > reversal and rate == False:
            pe_cnt += 1
        elif pe_cnt > 0:
            PerErr += (pe_cnt-1)
            pe_cnt = 0
        if trial == reversal:
            correct_ans = reverse(correct_ans)
    ac = num_ac / num_trials
    W_S = W_S / num_trials
    L_S = L_S / num_trials
    PerErr = PerErr / num_trials
    print( 'Accuracy: %4f, Win-Stay: %4f, Lose-Shift: %4f, Perservative Error: %4f' % (ac, W_S, L_S, PerErr) )
    return

if __name__ == '__main__':
    '''
    test
    '''
    win = visual.Window(color='black')
    proc(win)

