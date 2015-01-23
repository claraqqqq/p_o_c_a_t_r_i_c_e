"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
import math
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """   
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.
    hand: full yahtzee hand
    Returns an integer score 
    """
    record = dict()
    for dice in hand:
        if dice not in record.keys():
            record[dice] = dice
        else:
            record[dice] += dice
    max_score = 0        
    for dice in record.keys():
        if record[dice] > max_score:
            max_score = record[dice]
    return max_score


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.
    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled
    Returns a floating point expected value
    """
    outcomes = [dice for dice in range(1, num_die_sides+1)]
    possible_set_tmp = gen_all_sequences(outcomes, num_free_dice)
    possible_set = set()
    
    for comb_dice in possible_set_tmp:
        comb_dice_list = list(comb_dice)
        for dice in held_dice:
            comb_dice_list.append(dice)        
        possible_set.add(tuple(comb_dice_list))
    
    sum_score = 0
    for hand in possible_set:
        sum_score += score(hand)    
    exp_value = 1.0 * sum_score / len(possible_set)    
    return exp_value


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.
    hand: full yahtzee hand
    Returns a set of tuples, where each tuple is dice to hold
    """
    #hand_len = len(hand)
    #hand_list = list(hand)
    mask = list(gen_all_sequences([0, 1], len(hand)))
    all_holds = set([()])
    for comb_dice in mask:
        tmp = list()
        for index in range(len(comb_dice)):         
            if comb_dice[index] == 1:
                tmp.append(hand[index])
        all_holds.add(tuple(tmp))
    all_holds.add(tuple())
    return all_holds


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.
    hand: full yahtzee hand
    num_die_sides: number of sides on each die
    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    all_holds = gen_all_holds(hand)
    exp_value_max = 0    
    for held_dice in all_holds:
        num_free_dice = len(hand) - len(held_dice)
        exp_value = expected_value(held_dice, num_die_sides, num_free_dice)
        if exp_value > exp_value_max:
            exp_value_max = exp_value
            held_dice_max = held_dice
    return (exp_value_max, held_dice_max)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1,) #(1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    



