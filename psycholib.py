from psychopy import visual, core, logging, event, colors
from psychopy.colors import Color
import numpy as np

def tuple_mul(times, *args):
    ret = ()
    for item in args:
        ret += (item*times, )
    return ret

class CombinedStim():
    '''
    combinedStim: combined multiple stimulus which show together
    '''
    def __init__(self, *args, **kwargs):
        self.__list = args
        # print(self.__list)
    def append(self, stim):
        self.__list += (stim,)
    def draw(self):
        for item in self.__list:
            if hasattr(item, 'draw'):
                item.draw()
            else:
                print('WARNING: draw() attribute does not exist.')
        return

if __name__ == '__main__':
    win = visual.Window(color='black')
    text = visual.TextStim(win, text='Please print good!')
    text1 = visual.TextStim(win, text='Please print bad!')
    stim1 = CombinedStim(*(text,text1))
    while True:
        stim1.draw()
        # text.draw()
        win.flip()
