'''
This module contains functions to do sampling with and without 
replacement and random shuffling.  The algorithms are from
Knuth, vol. 2, section 3.4.2.

Copyright (C) 2002 GDS Software

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 2 of
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the Free
Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
MA  02111-1307  USA

See http://www.gnu.org/licenses/licenses.html for more details.
'''

import whrandom
__version__ = "$Id: sample.py,v 1.4 2002/08/21 12:41:49 donp Exp $"

# Note:  it's important to make the generator global.  If you put it into
# one of the functions and call that function rapidly, the generator will
# be initialized using the clock.  If the calls are fast enough, you'll 
# see distinctly nonrandom behavior.

rand_num_generatorG = whrandom.whrandom()

def sample_wor(population_size, sample_size):
    '''Sample without replacement from a set of integers from 1 to 
    population_size.  It returns a tuple of sample_size integers 
    that were selected.  The sampling distribution is 
    hypergeometric.
    '''
    assert type(population_size) == type(0) and            type(sample_size) == type(0)     and            population_size > 0              and            sample_size > 0                  and            sample_size <= population_size
    global rand_num_generatorG
    m = 0  # number of records selected so far
    t = 1  # Candidate integer to select if frac is right
    list = []
    while m < sample_size:    
        unif_rand = rand_num_generatorG.random()
        frac = 1.0 * (sample_size - m) / (population_size - (t-1))
        if unif_rand < frac:
            list.append(t)
            m = m + 1
        t = t + 1
    return tuple(list)

def sample_wr(population_size, sample_size):
    '''Sample with replacement from a set of integers from 1 to 
    population_size.  It returns a tuple of sample_size integers 
    that were selected.  The sampling distribution is binomial.
    '''
    assert type(population_size) == type(0) and            type(sample_size) == type(0)     and            population_size > 0              and            sample_size > 0
    global rand_num_generatorG
    list = []
    for ix in xrange(sample_size):
        list.append(rand_num_generatorG.randint(1, population_size))
    return tuple(list)

def shuffle(sample_size):
    '''Moses and Oakford algorithm.  See Knuth, vol 2, section 3.4.2.
    Returns a tuple of a random permutation of the integers from 1 to 
    sample_size.
    '''
    assert type(sample_size) == type(0) and sample_size > 0
    global rand_num_generatorG
    list = range(1, sample_size + 1)
    for ix in xrange(sample_size - 1, 0, -1):
        rand_int = rand_num_generatorG.randint(0, ix)
        if rand_int == ix:
            continue
        tmp = list[ix]
        list[ix] = list[rand_int]
        list[rand_int] = tmp
    return tuple(list)

def shuffle_set(set):
    '''Returns a tuple of the sequence set that has been randomly
    shuffled.  Works with lists and tuples.
    '''
    shuffled_set = []
    if type(set) != type([]) and type(set) != type(()):
        raise "Bad data", "must be list or tuple"
    numlist = shuffle(len(set))
    for jx in numlist:
        ix = jx - 1
        shuffled_set.append(set[ix])
    return tuple(shuffled_set)

def deal(deck_size, num_hands, num_per_hand):
    '''Returns a dictionary of dealt hands from the integers 1 to
    deck_size.  Each dictionary element (indexed by 1, 2, ...,
    num_hands) is a list of num_per_hand integers.  The element
    indexed by 0 is the remaining integers that were not selected
    for one of the hands.
    '''
    assert deck_size                             and            deck_size >= num_hands * num_per_hand and            num_hands > 0                         and            type(num_hands) == type(0)            and            num_per_hand > 0                      and            type(num_per_hand) == type(0)
    dict = {}
    # Generate the integers that will be in the hands
    sample = shuffle_set(range(1, deck_size + 1))
    for ix in range(num_hands):     # Partition into the dictionary
        start = ix * num_per_hand
        stop  = start + num_per_hand
        dict[ix+1] = sample[start : stop]
    dict[0] = sample[stop:]
    return dict

def deal_deck(num_hands, num_per_hand):
    '''Returns a dictionary of a dealt card hand.  The deal() function
    is used, but the routine also maps the integers to a string that
    contains the card identifications.  For example, 1 -> 2S, 2 -> 3S,
    ..., 13 -> AS, 14 -> 2C, etc.
    '''
    cards = deal(52, num_hands, num_per_hand)
    # Now go through and put identifier on the cards (and change them
    # from type integer to type string).
    suit_name = "SCHD"             # Spades, clubs, hearts, diamonds
    card_name = "A234567890JQK"    # Note 10 will need special handling...
    for hand in cards.keys():
        new_hand = []
        for card_num in cards[hand]:
            # We subtract 1 from card_num because cards are numbered 1 to 52
            suit_index, card_index = divmod(card_num-1, 13)
            #print "suit_index =", suit_index, " card_index =", card_index, " card_num =", card_num
            suit = suit_name[suit_index]
            card = ("1" * (card_index == 9)) + card_name[card_index]
            new_hand.append(card + suit)
        cards[hand] = new_hand
    return cards
