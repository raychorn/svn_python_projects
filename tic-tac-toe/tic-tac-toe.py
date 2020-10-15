import os, sys

import random

import time

from utils import timeit
from utils import terminate

'''
(c). Copyright 2014-2018, Ray C Horn, All RIghts Reserved.
'''

import Queue
import threadpool
__utility_Q__ = threadpool.ThreadQueue(500)

num_games = 0
results = {'X':0, 'O':0}
results1 = {}

def show_board(board,without=False):

    print "The board%s look like this: \n" % (' layout' if (without) else ' during play')

    item = 1
    for i in xrange(3):
        if (without):
            print " ",
        for j in xrange(3):
            if (not without):
                print '(%s) ' % (item),
            if (board[i*3+j] == 1):
                print 'X',
            elif (board[i*3+j] == 0):
                print 'O',	
            elif (board[i*3+j] != -1):
                print board[i*3+j]-1,
            else:
                print ' ',
            item += 1
            if (not without):
                print " ",

            if (j != 2):
                print " | ",
        print

        if (i != 2):
            num = 17
            if (not without):
                num *= 2
            print "-"*num
        else: 
            print 

def print_instruction():
    print "Please use the following cell numbers to make your move"
    show_board([2,3,4,5,6,7,8,9,10],without=True)

def __input__(prompt):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    line = sys.stdin.readline()
    if line:
        return line[:-1]

def get_input(turn):

    valid = False
    while (not valid):
        try:
            user = input("Where would you like to place " + turn + " (1-9)? ")
            user = int(user)
            if (user >= 1) and (user <= 9):
                return user-1
            else:
                print "That is not a valid move! Please try again.\n"
                print_instruction()
        except Exception as e:
            print user + " is not a valid move! Please try again.\n"

win_cond = ((1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9),(1,5,9),(3,5,7))

def check_win(board):
    for each in win_cond:
        try:
            if (board[each[0]-1] == board[each[1]-1]) and (board[each[1]-1] == board[each[2]-1]):
                return board[each[0]-1]
        except:
            pass
    return -1

def quit_game(board,msg,automated=False):
    show_board(board)
    print msg
    if (not automated):
        quit()
    
def __make_a_move__(k,v,board,value=0,is_testing=False):
    # where can a move be made ?
    possibles = []
    m = v[0]
    k = eval(k)
    for i in xrange(0,len(m)):
        if (m[i] == -1):
            possibles.append(k[i])
    if (len(possibles) > 0):
        choice = int(random.choice(possibles))
        board[choice-1] = value
        if (not is_testing):
            print 'MOVE IS %s for %s' % (choice,'X' if (value) else 'O')
    else:
        #print 'NO MOVES !!!'
        choice = -1
        pass
    return choice
    
def computer_move(board,value=0,is_testing=False):
    possible_wins = {}
    opposing = 0 if (value == 1) else 1
    for each in win_cond:
        try:
            if (board[each[0]-1]) or (board[each[1]-1]) or (board[each[2]-1]):
                count_open = 0
                if (board[each[0]-1]==-1):
                    count_open += 1
                if (board[each[1]-1]==-1):
                    count_open += 1
                if (board[each[2]-1]==-1):
                    count_open += 1
                count_opposing = 0
                if (board[each[0]-1]==opposing):
                    count_opposing += 1
                if (board[each[1]-1]==opposing):
                    count_opposing += 1
                if (board[each[2]-1]==opposing):
                    count_opposing += 1
                possible_wins[str(each)] = (board[each[0]-1],board[each[1]-1],board[each[2]-1]),(each[0]==5)or(each[1]==5)or(each[2]==5),(board[each[0]-1]==-1)and(board[each[1]-1]==-1)and(board[each[2]-1]==-1),(board[each[0]-1]==-1)or(board[each[1]-1]==-1)or(board[each[2]-1]==-1),(board[each[0]-1]==1)or(board[each[1]-1]==1)or(board[each[2]-1]==1),count_open,count_opposing
        except:
            pass
    if (board[5-1]==-1):
        board[5-1] = value
        return
    for k,v in possible_wins.iteritems():
        if (v[5] == 1) and (v[6] == 2):
            choice = __make_a_move__(k,v,board,value=value,is_testing=is_testing)
            if (choice > -1):
                return
    for k,v in possible_wins.iteritems():
        if (all(v[1:-4])):
            choice = __make_a_move__(k,v,board,value=value,is_testing=is_testing)
            if (choice > -1):
                break
        if (v[1]):
            if (v[2]):
                choice = __make_a_move__(k,v,board,value=value,is_testing=is_testing)
                if (choice > -1):
                    break
            if (v[3]):
                choice = __make_a_move__(k,v,board,value=value,is_testing=is_testing)
                if (choice > -1):
                    break
            if (v[4]):
                choice = __make_a_move__(k,v,board,value=value,is_testing=is_testing)
                if (choice > -1):
                    break
        else:
            if (v[4]):
                choice = __make_a_move__(k,v,board,value=value,is_testing=is_testing)
                if (choice > -1):
                    break
            if (v[3]):
                choice = __make_a_move__(k,v,board,value=value,is_testing=is_testing)
                if (choice > -1):
                    break
            if (v[2]):
                choice = __make_a_move__(k,v,board,value=value,is_testing=is_testing)
                if (choice > -1):
                    break
        for k,v in possible_wins.iteritems():
            if (v[5]) and (v[6] == 2):
                choice = __make_a_move__(k,v,board,value=value,is_testing=is_testing)
                if (choice > -1):
                    return
        for k,v in possible_wins.iteritems():
            if (v[5]) and (v[6] == 0):
                choice = __make_a_move__(k,v,board,value=value,is_testing=is_testing)
                if (choice > -1):
                    return
        if (not is_testing):
            print

def main(automated=False,is_testing=False):

    # setup game
    # alternate turns
    # check if win or end
    # quit and show the board

    if (not is_testing):
        print_instruction()

    __automated__ = automated
    if (not automated):
        prompt = "Automated play ? (computer versus computer) (y/N) ??? "
        resp = raw_input(prompt)
        __automated__ = str(resp).lower() in ['yes','y']

    __is_X__ = __automated__
    if (not __automated__):
        prompt = "Play as 'X' ? (human goes first) (y/N) ??? "
        resp = raw_input(prompt)
        __is_X__ = str(resp).lower() in ['yes','y']

    board = []
    for i in xrange(9):
        board.append(-1)

    win = False
    move = 0
    while not win:

        if (not is_testing):
            show_board(board)
            print "Turn number " + str(move+1)
        if (move % 2 == 0):
            turn = 'X'
        else:
            turn = 'O'

        if (turn == 'X'):
            if (not __automated__ and __is_X__):
                user = get_input(turn)
                while (board[user] != -1):
                    print "Invalid move! Cell already taken. Please try again.\n"
                    user = get_input(turn)
                board[user] = 1 if (turn == 'X') else 0
            else:
                computer_move(board,value=1 if (__is_X__) else 0,is_testing=is_testing)
        else:
            if (not __automated__ and not __is_X__):
                user = get_input(turn)
                while (board[user] != -1):
                    print "Invalid move! Cell already taken. Please try again.\n"
                    user = get_input(turn)
                board[user] = 0 if (turn == 'X') else 1
            else:
                computer_move(board,value=0,is_testing=is_testing)

        move += 1
        if (move > 4):
            winner = check_win(board)
            if (winner != -1):
                out = "The winner is "
                winner_is = "X" if winner == 1 else "O"
                out += winner_is
                out += " :)"
                if (not automated):
                    out += 'Game Over.'
                if (not automated):
                    quit_game(board,out,automated=automated)
                else:
                    board.append(winner_is)
                win = True
            elif (move == 9):
                if (not automated):
                    quit_game(board,"No winner :(")
                else:
                    board.append('-')
                win = True
                    
    return board

def collate_results_from(board,is_testing=False):
    global num_games
    
    if (is_testing):
        b = ['X' if (i == 1) else 'O' for i in board]
        results[b[-1]] = results.get(b[-1], 0) + 1
        k = ''.join(b[0:-1])
        if (not results1.has_key(k)):
            results1[k] = 0
        results1[k] = results1.get(k, 0) + 1
        logger.info('%s %s %s' % (b[0:-1],b[-1],results))
        num_games += 1
    
@threadpool.threadify(__utility_Q__)
def __main__(automated=False,is_testing=False):
    '''
    Threaded version of the main() function.
    '''
    b = main(automated=automated,is_testing=is_testing)
    collate_results_from(b,is_testing=is_testing)

if (__name__ == "__main__"):
    assert tuple([sys.version_info.major,sys.version_info.minor,sys.version_info.micro]) == (2, 7, 14), 'Wrong Python Version.'

    from optparse import OptionParser
    
    parser = OptionParser()
    
    parser.add_option("-a", "--auto",
                      action="store_true", dest="auto", default=False,
                      help="Automated with no user input.")
    
    parser.add_option("-m", "--multi",
                      action="store_true", dest="multi", default=False,
                      help="Multi-threaded using worker threads.")

    parser.add_option("-t", "--test",
                      action="store_true", dest="test", default=False,
                      help="Test mode, free running, runs for a long time, stress test.")

    parser.add_option("-s", "--seed",
                      action="store_true", dest="seed", default=False,
                      help="Seed or reseed the random functions.")

    parser.add_option("-r", "--relax",
                      action="store_true", dest="relax", default=False,
                      help="Relaxed testing.")

    parser.add_option("-n", type="int", dest="iterations", default=0)

    options, arguments = parser.parse_args()
    
    logger_info_callback = {}

    import logging
    from datetime import datetime
    
    from logging.config import dictConfig
    
    abspath = os.path.abspath('.')
    fname = os.path.splitext(os.path.basename(__file__))[0]
    now = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    
    s_options = ''
    s_options += '_Auto' if (options.auto) else ''
    s_options += '_Multi' if (options.multi) else ''
    s_options += '_Test' if (options.test) else ''
    s_options += '_Seed' if (options.seed) else ''
    s_options += '_Relax' if (options.relax) else ''
    s_options += '_Iterations(%s)' % (options.iterations) if (options.iterations > 0) else ''
    
    logging_config = dict(
        version=1,
        formatters={
            'f': {'format':
                  '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
            },
        handlers={
            'h': {'class': 'logging.FileHandler',
                  'formatter': 'f',
                  'level': logging.DEBUG,
                  'filename': os.path.sep.join([abspath, fname+s_options+'_'+now+'.log']), 
                  },
            'c': {'class': 'logging.StreamHandler',
                  'formatter': 'f',
                  'level': logging.DEBUG,
                  'stream': sys.stdout,
                  }
            },
        root={
            'handlers': ['h', 'c'],
            'level': logging.DEBUG,
            },
    )

    dictConfig(logging_config)
    logger = logging.getLogger()

    logger_info_callback['callback'] = logger.info

    if (options.seed):
        random.seed(time.time())
        
    if (options.test):
        @timeit(log_time=None, callback=logger_info_callback)
        def handle_options():
            for iter in xrange(0,options.iterations):
                if (options.multi):
                    __main__(automated=options.auto,is_testing=options.test)
                else:
                    bb = main(automated=options.auto,is_testing=options.test)
                    collate_results_from(bb,is_testing=options.test)
            
            if (options.multi):
                logger.info('Waiting for threads to finish working.')
                __utility_Q__.join()
                
        handle_options()

    else:
        main(automated=options.auto)
        
    cross_total = 0
    logger.info('%s' % ('='*30))
    for k,v in results1.iteritems():
        logger.info('%s --> %s' % (k,v))
        cross_total += v
    logger.info('%s' % ('='*30))
    results_total = sum([v for v in results.values()])
    try:
        assert num_games == options.iterations, 'Not enough iterations.'
    except Exception, details:
        logger.exception(details)
    try:
        assert len(results.keys()) == 2, 'Wrong winner results.'
    except Exception, details:
        logger.exception(details)
    try:
        if (not options.relax):
            assert results_total == cross_total, 'Analytics total does not match results total.'
    except Exception, details:
        logger.exception(details)
    try:
        if (not options.relax):
            assert results_total == cross_total, 'Analytics total does not match results total.'
    except Exception, details:
        logger.exception(details)

    logger.info('DONE!!!')
    terminate()
