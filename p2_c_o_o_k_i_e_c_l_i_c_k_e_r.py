"""
Cookie Clicker Simulator
"""

import simpleplot
import math
import random
# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):       
        self._totalcookies = 0.0
        self._currentcookies = 0.0
        self._currenttime = 0.0
        self._cps = 1.0
        self._itembought = None
        self._itemcost = 0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """       
        # prtstr = str(self._history)
        prtstr = (self._currenttime, self._cps, self._currentcookies, self._totalcookies)
        return str(prtstr)
     
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)        
        Should return a float
        """
        return self._currentcookies
    
    def get_cps(self):
        """
        Get current CPS
        Should return a float
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time
        Should return a float
        """
        return self._currenttime
    
    def get_history(self):
        """
        Return history list
        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)
        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history   

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)
        Should return a float with no fractional part
        """
        if self._currentcookies >= cookies:
            return 0.0
        else:
            return math.ceil((cookies-self._currentcookies) / self._cps)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state
        Should do nothing if time <= 0
        """
        if time > 0:
            self._currenttime += time
            self._currentcookies += self._cps*time
            self._totalcookies += self._cps*time
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state
        Should do nothing if you cannot afford the item
        """
        if self._currentcookies >= cost:
            self._cps += additional_cps
            self._currentcookies -= cost
            self._history.append((self._currenttime, item_name, 
                                  cost, self._totalcookies))

    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """
    # Replace with your code
    
    obj_clickerstate = ClickerState()
    obj_buildinfoclone = build_info.clone()
    stop = False

    while (obj_clickerstate.get_time() <= duration) and (stop == False):   
    
        item_name = strategy(obj_clickerstate.get_cookies(), obj_clickerstate.get_cps(), 
                             duration - obj_clickerstate.get_time(), obj_buildinfoclone)
        if item_name == None:
            stop = True
            obj_clickerstate.wait(duration - obj_clickerstate.get_time())        
        else:
            cost = obj_buildinfoclone.get_cost(item_name)
            waiting_time = obj_clickerstate.time_until(cost)
            additional_cps = obj_buildinfoclone.get_cps(item_name)             
            if obj_clickerstate.get_time() + waiting_time > duration:
                obj_clickerstate.wait(duration - obj_clickerstate.get_time())
                stop = True
            else:
                obj_clickerstate.wait(waiting_time)                  
                obj_clickerstate.buy_item(item_name, cost, additional_cps)
                obj_buildinfoclone.update_item(item_name)
        
    return obj_clickerstate


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!
    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None
    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """  
    this strategy should always select the cheapest item. 
    """
    cookies += cps*time_left
    all_itemname = build_info.build_items()
    min_itemname = all_itemname[0]
    min_itemcost = build_info.get_cost(min_itemname)   
    for item_name in build_info.build_items(): 
        if cookies >= build_info.get_cost(item_name):
            if build_info.get_cost(item_name) < min_itemcost:
                min_itemcost = build_info.get_cost(item_name)
                min_itemname = item_name
    if cookies < min_itemcost:
        return None
    else:
        return min_itemname

def strategy_expensive(cookies, cps, time_left, build_info):
    """  
    this strategy should always select the most expensive item 
    you can afford in the time left.
    """
    cookies += cps*time_left
    all_itemname = build_info.build_items()
    max_itemname = all_itemname[0]
    max_itemcost = build_info.get_cost(max_itemname)   
    for item_name in build_info.build_items(): 
        if cookies >= build_info.get_cost(item_name):
            if build_info.get_cost(item_name) > max_itemcost:
                max_itemcost = build_info.get_cost(item_name)
                max_itemname = item_name
    if cookies < max_itemcost:
        return None
    else:
        return max_itemname

def strategy_best(cookies, cps, time_left, build_info):
    """
    this is the best strategy that you can come up with.
    """
    choices = []
    cookies += cps*time_left 
    for item_name in build_info.build_items(): 
        if cookies >= build_info.get_cost(item_name):
            choices.append(item_name)
    if len(choices) > 0:
        item_choose_num = random.randrange(len(choices))       
        return choices[item_choose_num]
    else:
        return None

def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)
    
run()
 
