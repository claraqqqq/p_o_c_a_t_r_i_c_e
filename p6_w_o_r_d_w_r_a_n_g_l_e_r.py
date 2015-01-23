"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"
codeskulptor.set_timeout(40) 

# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.
    Returns a new sorted list with the same elements in list1, but
    with no duplicates.
    This function can be iterative.
    """
    result = []
    for element in list1:
        if element not in result:
            result.append(element)
    return result 
    
#list1 = ['a','b','c','a','c','b','s','s','r','f']
#print remove_duplicates(list1)

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.
    Returns a new sorted list containing only elements that are in
    both list1 and list2.
    This function can be iterative.
    """
    result = []
    #list1_tmp = remove_duplicates(list1)
    #list2_tmp = remove_duplicates(list2)
    #for element in list1_tmp:
    #    if element in list2_tmp:
    #        result.append(element)
    index1 = 0
    index2 = 0 
    while index1 < len(list1) and index2 < len(list2):
        if list1[index1] < list2[index2]:
            index1 += 1
        elif list1[index1] > list2[index2]:
            index2 += 1
        else:
            result.append(list1[index1])
            index1 += 1
            index2 += 1
    return result

#list1 = ['a','b','c','a','c','b','s','s','r','d']
#list2 = ['a','b','c','a','c','b','s','s','r','d']
#print intersect(list1, list2)

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.
    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.
    This function can be iterative.
    """  
    result = []
    if len(list1) == 0:
        return list2
    if len(list2) == 0:
        return list1
    
    label = True
    list1_tmp = []
    list2_tmp = []
    for element in list1:
        list1_tmp.append(element)
    for element in list2:
        list2_tmp.append(element)
        
    while label:
        if list1_tmp[0] <= list2_tmp[0]:
            result.append(list1_tmp[0])
            list1_tmp.remove(list1_tmp[0])
        else:
            result.append(list2_tmp[0])
            list2_tmp.remove(list2_tmp[0])
        if (len(list1_tmp) == 0) or (len(list2_tmp) == 0):
            label = False
            
    if len(list1_tmp) == 0:
        result += list2_tmp
    if len(list2_tmp) == 0:
        result += list1_tmp
    return result

#list1 = ['a','b','c','a']
#list2 = ['a','b','c']
#print merge(list1, list2)
#print merge([1, 2, 3], [4, 5, 6]) 
#print merge([], [])
#print merge([2], [6])
#print
#print merge([], [])
#print
#print merge([2], [])

def merge_sort(list1):
    """
    Sort the elements of list1.
    Return a new sorted list with the same elements as list1.
    This function should be recursive.
    """
    if len(list1) == 0:
        return []
    if len(list1) == 1:
        return list1
    if len(list1) == 2:
        return merge([list1[0]], [list1[1]])
    while len(list1) > 2:
        list_a = list(list1[:len(list1)/2])
        list_b = list(list1[len(list1)/2:])
        return merge(merge_sort(list_a), merge_sort(list_b))
        #return merge(merge_sort(list1[:len(list1)/2]), merge_sort(list1[len(list1)/2:]))
        #return merge(merge_sort([list1[:len(list1)/2]]), merge_sort([list1[len(list1)/2:]]))
#ll = [2, 6] 
#print len(ll)
#print ll[0]
#print ll[1]
#print list(0)
#print list(ll[0])
#list1 = ['b','f','a','b','a']
#print merge_sort(list1)
#print merge_sort([2, 6, 8, 10])
#print merge_sort([6, 2, 6, 8, 10])

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.
    Returns a list of all strings that can be formed from the letters
    in word.
    This function should be recursive.
    """
    result = []
    if len(word) == 0:
        result.append('')
        return result
    first = word[0]
    #print 'first:', first
    rest = word[1:]
    #print 'rest:', rest
    if len(word) >= 1:
        rest_strings = gen_all_strings(rest)
        #print 'rest_strings:', rest_strings 
        for element in rest_strings:
            for index in range(len(element)+1):
                result.append(element[:index] + first + element[index:])
    result += rest_strings
    return result

#print ['a'] + ['b']
#print gen_all_strings("")
#print gen_all_strings('a')
#print gen_all_strings('ab')
#print gen_all_strings('aa')
#print gen_all_strings('aab')

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.
    Returns a list of strings.
    """
    url = codeskulptor.file2url(WORDFILE)
    netfile = urllib2.urlopen(url)
    data = netfile.readlines()
    #return_list = [word[:-1] for word in data]
    return_list = [word.strip() for word in data]
    return return_list


def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)


# Uncomment when you are ready to try the game
run()

    
    
