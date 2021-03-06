"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
                
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        #self._cells[row][col] = ZOMBIE
        self._zombie_list.append([row, col])
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)   
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for zombie_loc in self._zombie_list:
            yield tuple(zombie_loc)

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append([row, col])
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for human_loc in self._human_list:
            yield tuple(human_loc)
      
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        visited = poc_grid.Grid(self.get_grid_height(), self.get_grid_width())
        
        dist_value = self._grid_height*self._grid_width        
        distance_field = [[dist_value for dummy_col in range(self._grid_width)]
                          for dummy_row in range(self._grid_height)]        
        boundary = poc_queue.Queue()
        entity_list = []
        if entity_type == ZOMBIE:
            entity_list = self._zombie_list
        elif entity_type == HUMAN:
            entity_list = self._human_list
            
        for entity in entity_list:
            boundary.enqueue(entity)
            visited.set_full(entity[0], entity[1])
            distance_field[entity[0]][entity[1]] = 0            
        while len(boundary) > 0:
            cell = boundary.dequeue()           
            neighbors = self.four_neighbors(cell[0], cell[1])
            for neighbor in neighbors:
                if visited.is_empty(neighbor[0], neighbor[1]):  
                    if self.is_empty(neighbor[0], neighbor[1]):
                        dist_value = min(distance_field[neighbor[0]][neighbor[1]], 
                                      distance_field[cell[0]][cell[1]]+1)                
                        distance_field[neighbor[0]][neighbor[1]] = dist_value                       
                        visited.set_full(neighbor[0], neighbor[1])
                        if neighbor not in boundary:
                            boundary.enqueue(neighbor)
        return distance_field
                
                
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        for index in range(self.num_humans()):
            human = self._human_list[index]
            neighbors = self.eight_neighbors(human[0], human[1])
            dist_tmp = zombie_distance[human[0]][human[1]]
            loc_tmp = (human[0], human[1])
            for nghbr in neighbors:
                if zombie_distance[nghbr[0]][nghbr[1]] > dist_tmp:
                    dist_tmp = zombie_distance[nghbr[0]][nghbr[1]]
                    loc_tmp = (nghbr[0], nghbr[1])
            zombie_distance[loc_tmp[0]][loc_tmp[1]] = -self._grid_height*self._grid_width 
            self._human_list[index] = loc_tmp
        return self._human_list
    
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for index in range(self.num_zombies()):
            zombie = self._zombie_list[index]
            neighbors = self.four_neighbors(zombie[0], zombie[1])
            dist_tmp = human_distance[zombie[0]][zombie[1]]
            loc_tmp = (zombie[0], zombie[1])
            for nghbr in neighbors:
                if human_distance[nghbr[0]][nghbr[1]] < dist_tmp:
                    dist_tmp = human_distance[nghbr[0]][nghbr[1]]
                    loc_tmp = (nghbr[0], nghbr[1])
            human_distance[loc_tmp[0]][loc_tmp[1]] = self._grid_height*self._grid_width 
            self._zombie_list[index] = loc_tmp
        return self._zombie_list

# Start up gui for simulation - You will need to write some code above
# before this will work without errors
# poc_zombie_gui.run_gui(Zombie(30, 40))
