
'''

    Sokoban assignment


The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.

No partial marks will be awarded for functions that do not meet the specifications
of the interfaces.

You are NOT allowed to change the defined interfaces.
In other words, you must fully adhere to the specifications of the 
functions, their arguments and returned values.
Changing the interfacce of a function will likely result in a fail 
for the test of your code. This is not negotiable! 

You have to make sure that your code works with the files provided 
(search.py and sokoban.py) as your code will be tested 
with the original copies of these files. 

Last modified by 2021-08-17  by f.maire@qut.edu.au
- clarifiy some comments, rename some functions
  (and hopefully didn't introduce any bug!)

'''

# You have to make sure that your code works with 
# the files provided (search.py and sokoban.py) as your code will be tested 
# with these files
import search
import sokoban
import sys

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [ (10110364, 'Hayoung', 'Lee'), (10837353, 'Yena', 'Park'), (10892915, 'Xinyang Doris', 'Che') ]
    # raise NotImplementedError()


# - - - - - - - - - - - - - - - - Global Variable- - - - - - - - - - - - - - - - 

IMP = "Impossible"

# - - - - - - - - - - - - - - - - Auxiliary Functions- - - - - - - - - - - - - - - - 
"""
    To calculate manhattan_distance for heuristics
"""
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def manhattan_distance(coordi1, coordi2): 
    """
    manhattan distance |x2 - x1| + |y2 - y1|

    @param coordi_1: x, y value of start point
    @param coordi_2: x, y value of the destination

    @return
        the calculated manhattan distance between the two given tuples
    """
    return abs(coordi2[0] - coordi1[0]) + abs(coordi2[1] - coordi1[1])
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


"""
    To find taboo, this project use flood fill algorithm.
    We referenced a below code.
    http://inventwithpython.com/blogstatic/floodfill/recursivefloodfill.py
"""
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def getLocation(warehouseText, height, width):
    """
    To get warehouse's all cells location.
    Change warehouse file(text) to list to make it easy to use in code

    @param warehouseText: String type of warehouse map 
    @param height: The height of warehouse
    @param width: the width of warehouse

    @return
        List of all cells with nested list
        For example, warehouse's height is 2 and width is 3, it returns the below shpae of list
        [["","",""], ["","",""]]
    """
    warehouseText = warehouseText.split('\n')

    # make a empty cells list to find a shape of warehouse
    for idx, map in enumerate(warehouseText):
        if(len(map) < width):
            map = map+" "*(width-len(map))
        warehouseText[idx] = map
   
    characters = []
    # make a nested list
    for i in range(width):
        characters.append([''] * height)

    # make a final list with real chracters from warehoustText
    for x in range(width):
        for y in range(height):
            characters[x][y] = warehouseText[x][y]
    
    return characters

def inside(characters,height, width):
    """
    To find coordinates which are in inside of the walls

    @param characters: The list of warehouse cells
    @param height: The height of warehouse
    @param width: the width of warehouse

    @return
        The coordinates of inside cells
    """
    insideCoordinates=[]
    for y in range(height):
        for x in range(width):
            # after flood fill algorithm, the inside cells represented with 'X'
            # therefore, if the value is 'X' append coordinate in the insideCoordinates list
            if(characters[x][y]=='X'):
                insideCoordinates.append((y,x))
    return insideCoordinates
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def floodFill(characters, x, y, oldChar, newChar,height, width): # sourch URL
    
    """
        To find cells which are in inside of the walls using flood fill algorithm.
        This algorithm is recursive algorithm.
        When the oldChar and newChar are matched, oldChar turns to newChar

        @param characters: The list of warehouse cells
        @param x: x coordinate 
        @param y: y coordinate
        @param oldChar: original character 
        @param newChar: new character 
        @param height: The height of warehouse
        @param width: the width of warehouse
        
        @return
            The coordinates of inside cells
    """

    # If the oldChar is None insert character which is in (x,y).
    if oldChar == None:
        oldChar = characters[x][y]

    # If the current x, y character is not the oldChar,then do nothing.
    if characters[x][y] != oldChar:
        return

    # Change the character at characters[x][y] to newChar
    characters[x][y] = newChar
    
    # Recursive floodFill function if x or y is in boundary
    # check left side
    if x < width-1: 
        floodFill(characters, x-1, y, oldChar, newChar,height, width)
    
    #check upper side
    if y < height-1:
        floodFill(characters, x, y-1, oldChar, newChar,height, width)
    
    #check right side
    if x>0:
        floodFill(characters, x+1, y, oldChar, newChar,height, width)
    
    # check down side
    if y>0:
        floodFill(characters, x, y+1, oldChar, newChar,height, width)

    return(inside(characters,height, width))


def printWhareHouse(characters, taboo, col, row):
    
    """
        To find cells which are in inside of the walls using flood fill algorithm.
        This algorithm is recursive algorithm.
        When the oldChar and newChar are matched, oldChar turns to newChar

        @param characters: The list of warehouse cells
        @param x: x coordinate 
        @param y: y coordinate
        @param oldChar: original character 
        @param newChar: new character 
        @param height: The height of warehouse
        @param width: the width of warehouse
        
        @return
            The coordinates of inside cells
    """
    result=''
    for y in range(col):
        for x in range(row):
            if (y,x) in taboo:
                characters[x][y] = 'X'
    for x in range(row):
        for y in range(col):
            result+=characters[x][y]
        if(y != row-1):
            result+='\n'
    return result.rstrip('\n')
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def findInside(warehouse, walls):
    # to break for loops
    flag = False
    for col in range(warehouse.ncols):
            for row in range(warehouse.nrows):
                if ((col,row-1) in walls) and ((col-1,row) in walls) and ((col-1, row-1) in walls):
                    # check if the location is in the target or not
                    if ((col, row)) not in warehouse.targets:
                        # to get location of warehouse, replace all characters to space 
                        characters = getLocation(warehouse.__str__().replace(
                            ".", " ").replace('*', " ").replace("@", " ").replace("$", " "),warehouse.ncols, warehouse.nrows)
                        # get the inside cell's location list
                        inside = floodFill(characters, row, col, None, 'X',warehouse.ncols, warehouse.nrows)
                         # break the second for loop
                        flag = True
                        break
                
                # the second condition
                elif ((col, row-1) in walls) and ((col-1,row) in walls):
                    # check if the location is in the target or not
                    if ((col, row)) not in warehouse.targets:
                        characters = getLocation(warehouse.__str__().replace(
                            ".", " ").replace('*', " ").replace("@", " ").replace("$", " "),warehouse.ncols, warehouse.nrows)
                        inside = floodFill(characters, row, col, None, 'X',warehouse.ncols, warehouse.nrows)
                        flag = True
                        break
            # break the first for loop 
            if flag:
                break
    
    return inside
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def findTaboo(warehouse,walls, inside):
    taboo=[]
    for location in inside:
        col = location[0]
        row = location[1]

        if ((col, row)) in walls:
            continue
        else:
            if((col, row) not in warehouse.targets):
                # if x=0, y=0
                if(row == 0 and col == 0):
                    taboo.append((col, row))
                elif(col == 0 and row == warehouse.nrows):
                    taboo.append((col, row))
                elif(row == 0 and col == warehouse.ncols):
                    taboo.append((col, row))
                elif(row == warehouse.nrows and col == warehouse.ncols):
                    taboo.append((col, row))
                # last
                # row-1 : up, col-1: left, col+1: right, row+1: bottom
                else:
                    if(((col, row-1) in walls and (col-1, row) in walls) or ((col, row-1) in walls and (col+1, row) in walls) or ((col, row+1) in walls and (col+1, row) in walls) or ((col, row+1) in walls and (col-1, row) in walls)):
                        taboo.append((col, row))

    # second rule
    for location in inside:
        col = location[0]
        row = location[1]
        if((col, row) not in warehouse.targets):
            if(((col, row-1) in taboo) and ((col, row+1) in taboo)):
                taboo.append((col, row))
            if(((col+1, row) in taboo) and ((col-1, row) in taboo)):
                taboo.append((col, row))

    return taboo

# - - - - - - - - - - - - - - - - - - Auxiliary Functions End- - - - - - - - - - - - - - - - - - - - -
def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A "taboo cell" is by definition
    a cell inside a warehouse such that whenever a box get pushed on such 
    a cell then the puzzle becomes unsolvable. 
    
    Cells outside the warehouse are not taboo. It is a fail to tag one as taboo.
    
    When determining the taboo cells, you must ignore all the existing boxes, 
    only consider the walls and the target  cells.  
    Use only the following rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of 
             these cells is a target.
    
    @param warehouse: 
        a Warehouse object with a worker inside the warehouse

    @return
       A string representing the warehouse with only the wall cells marked with 
       a '#' and the taboo cells marked with a 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''
    # find the inside cells
    walls = warehouse.walls
    inside = findInside(warehouse,walls)
     # find taboo cells
    
    taboo = findTaboo(warehouse,walls,inside)

    # to write the taboo cell map
    characters = getLocation(warehouse.__str__().replace(
        ".", " ").replace('*', " ").replace("@", " ").replace("$", " "),warehouse.ncols, warehouse.nrows)

   
    return printWhareHouse(characters, taboo, warehouse.ncols, warehouse.nrows)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    '''
    def __init__(self, warehouse):
        """
        initialisation function

        @param warehouse: warehouse object
        
        """
        # initial state
        self.initial = (warehouse.worker, frozenset(zip(warehouse.boxes, warehouse.weights)))

        # to save legal actions 
        self.legal=[]

        # to using cells
        self.inside = findInside(warehouse,warehouse.walls)
        self.taboo_cells = set(findTaboo(warehouse,warehouse.walls,self.inside))
        self.walls = set(warehouse.walls)
        self.goal = set(warehouse.targets)

        # to check the legal actions
        self.warehouse = warehouse

    def actions(self, state):
        """
        Return the actions that can be executed in the given state.

        The rules of legal actions:
            1. Worker cannot go to wall
            2. If the worker moves a box, the worker cannot move a box to another box or wall
            3. Worker cannot go to a taboo cell

        @ return
            legal actions list
        """

        #list of leagal actions
        L = []   
        col = state[0][0]
        row = state[0][1]

        walls = self.walls
        boxes = set(state[1])
        warehouse = self.warehouse

        # find inside cell and taboo to check the conditions
        inside = findInside(warehouse,walls)
        taboo = findTaboo(warehouse,walls,inside)

        for location in inside:
            if ((col,row)==location):
                # LEFT
                if ((col-1,row) not in walls):
                    if ((col-1,row) not in boxes):
                        L.append("Left")
                    # moving a box
                    elif ((col-1,row) in boxes):
                        # check if a worker moves a box to another box or the wall
                        if (col-2,row) not in boxes and (col-2,row) not in walls:
                            # check if a worker moves a box to the taboo cell
                            if (col-2,row) not in taboo:
                                L.append("Left")
                # RIGHT
                if ((col+1,row) not in walls):
                    if ((col+1,row) not in boxes):
                        L.append("Right")
                    # moving a box
                    elif ((col+1,row) in boxes):
                        # check if a worker moves a box to another box or the wall
                        if (((col+2,row) not in boxes) and ((col+2,row) not in walls)):
                            # check if a worker moves a box to the taboo cell
                            if ((col+2,row) not in taboo):
                                L.append("Right")
                # UP
                if ((col,row-1) not in walls):
                    if ((col,row-1) not in boxes):
                        L.append("Up")
                    # moving a box
                    elif ((col,row-1) in boxes):
                        # check if a worker moves a box to another box or the wall
                        if ((col,row-2) not in boxes and (col,row-2) not in walls):
                            # check if a worker moves a box to the taboo cell
                            if ((col,row-2) not in taboo):
                                L.append("Up")
                # DOWN
                if ((col,row+1) not in walls):
                    if ((col,row+1) not in boxes):
                        L.append("Down")
                    # moving a box
                    elif ((col,row+1) in boxes):
                        # check if a worker moves a box to another box or the wall
                        if (((col,row+2) not in boxes) and ((col,row+2) not in walls)):
                            # check if a worker moves a box to the taboo cell
                            if ((col,row+2) not in taboo):
                                L.append("Down")
                               
        self.legal = set(L)
       
        return self.legal


       
    def path_cost(self, c, state1, worker_movement_cost, state2): 
        """
        Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path.
    

        @param c: the current cost
        @param state1: current state 
        @param worker_movement_cost: cost for each action of worker movement from state1 to state2
        @param state2: next state

        @return
            the cost of performing the action to get from state1 to state2
        """
        worker_movement_cost = 1

        # save the two states' boxes information as a set
        old_boxes, new_boxes = state1[1], state2[1]
       
        old_boxes, new_boxes = set(old_boxes), set(new_boxes)

        # if the two are different, find the box which is moved
        if new_boxes != old_boxes:
            for box, weight in new_boxes:
                # add the weight of box
                if (box, weight) not in old_boxes:
                    return c + worker_movement_cost + weight

        # returns the current cost + 1
        return c + worker_movement_cost

    def goal_test(self, state):
        """
        tests if the state is in the goal position

        @param state: current state of the puzzle

        @return
            True if the goal is met
            False otherwise
        """
        boxesState=[]
        for boxes in state[1]:
            boxesState.append(boxes[0])
        return set(boxesState) == set(self.goal)

    def result(self, state, action):
        """
        act upon the given action using the given state

        @param state: current state of the puzzle
        @param action: the action to act upon

        @return
            the new state
        """
        # copy the state 
        (worker, boxes) = state
        boxes = list(boxes)

        # convert action into coordinate uinsg tuple
       
        if(action == "Up"):
            worker = (worker[0] , worker[1] -1)
        elif(action == "Left"):
            worker = (worker[0]-1 , worker[1])
        elif(action == "Down"):
            worker = (worker[0] , worker[1]+1)
        elif(action == "Right"):
            worker = (worker[0]+1 , worker[1])
       
        # update the box if one of the box is pushed
        for i, (box, cost) in enumerate(boxes):
            if worker == box:
                if(action == "Up"):
                    boxes[i] = ((box[0] , box[1] -1), cost)
                elif(action == "Left"):
                    boxes[i] = ((box[0]-1 , box[1]), cost)
                elif(action == "Down"):
                    boxes[i] = ((box[0] , box[1]+1), cost)
                elif(action == "Right"):
                    boxes[i] = ((box[0]+1 , box[1]), cost)
              

        return worker, frozenset(boxes)

    def h(self, n): 
        """
        heuristic using that defines the closest box to the worker
        and also the closest box to target combination,

        @param n: current node

        @return
            The sum of minimum value of the distances between worker and box and minimun value of the distances between boxes and targets
        """
        # save the state
        (worker, boxes) = n.state
        boxes = list(boxes)

        # initialise the list of distances
        worker_to_box_cost, box_to_target_cost = set(), set()

        # iterate all boexes and calculate manhattan distance between worker and box
        for (box, _) in boxes:
            worker_to_box_distance = manhattan_distance(worker, box)
            worker_to_box_cost.add(worker_to_box_distance)

        # iterate all goals to find the distance between each box and targets
        for goal in self.goal:
            total_weighted_distance = 0
            for box in boxes:
                weight = box[1]
                weight = 1 if weight == 0 else weight
                
                #calculate weight
                weighted_distance = manhattan_distance(goal, box[0]) * weight 
                # weighted distance for boxes as worker movement always 1 cost
                total_weighted_distance += weighted_distance
            box_to_target_cost.add(total_weighted_distance)
 

        return min(worker_to_box_cost) + min(box_to_target_cost)


def check_elem_action_seq(warehouse, action_seq):
    '''

    Determine if the sequence of actions listed in 'action_seq' is legal or not.

    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.

    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']

    @return
        The string 'Impossible', if one of the action was not valid.
           For example, if the agent tries to push two boxes at the same time,
                        or push a box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''

    # to use the warehouse information and result function in the SoKobanPuzzle class
    sp = SokobanPuzzle(warehouse)
     # copy the original information
    new_warehouse = warehouse.copy(warehouse.worker, warehouse.boxes)
    col = new_warehouse.worker[0]
    row = new_warehouse.worker[1]
    boxes = new_warehouse.boxes
    
    
    for action in action_seq:
        # to check the legal actions
        sp.actions(sp.initial)

        # if the action is legal
        if(action in sp.legal):
            # find a coordinate which can go
            result = sp.result(sp.initial, action)
            # check it is not moved
            if(result[0] == (col,row)):
                warehouse.worker = (col,row)
                warehouse.boxes = boxes
                sp.initial = (warehouse.worker, frozenset(zip(warehouse.boxes, warehouse.weights)))
                return IMP
            # update the warhouse's state using action
            else:
                warehouse.worker = result[0]
                box_list=[]
                for box in result[1]:
                    box_list.append(box[0])
                warehouse.boxes = box_list
                sp.initial = (warehouse.worker, frozenset(zip(warehouse.boxes, warehouse.weights)))
        # if the action is illegal return Impossible
        else:
            return IMP
    return warehouse.__str__()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban(warehouse):
    '''
    This function analyses the given warehouse.
    It returns the two items. The first item is an action sequence solution. 
    The second item is the total cost of this action sequence.
    
    @param 
     warehouse: a valid Warehouse object

    @return
    
        If puzzle cannot be solved 
            return 'Impossible', None
        
        If a solution was found, 
            return S, C 
            where S is a list of actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
            C is the total cost of the action sequence C

    '''
    # excute A* algorithm
    path = search.astar_graph_search(SokobanPuzzle(warehouse))

    # if path is not None return path and path cost
    if path is not None:
        return path.solution(), path.path_cost

    # if path is None, return "Impossible"
    return IMP

# - - - - - - - - - -Evidence of testing with assert statements or equivalents - - - - - - - - - - - - - -

# - - - - - - - - - - (base) hayoung@HayoungLees-Air sokoban_assignment_code % python sanity_check.py
#  - - - - - - - - - - Using submitted solver
#  - - - - - - - - - - <<  Testing test_taboo_cells >>
#  - - - - - - - - - - ####  
# - - - - - - - - - -  #X #  
#  - - - - - - - - - - #  ###
#  - - - - - - - - - - #   X#
#  - - - - - - - - - - #   X#
#  - - - - - - - - - - #XX###
#  - - - - - - - - - - ####  
#  - - - - - - - - - - test_taboo_cells  passed!  :-)

# - - - - - - - - - -  <<  check_elem_action_seq, test 1>>
#  - - - - - - - - - - Test 1 passed!  :-)

#  - - - - - - - - - - <<  check_elem_action_seq, test 2>>
#  - - - - - - - - - - Test 2 passed!  :-)

# - - - - - - - - - -  <<  test_solve_weighted_sokoban >>
#   - - - - - - - - - - Answer as expected!  :-)

#  - - - - - - - - - - Your cost = 431, expected cost = 431
# - - - - - - - - - -Evidence of testing with assert statements or equivalents - - - - - - - - - - - - - -