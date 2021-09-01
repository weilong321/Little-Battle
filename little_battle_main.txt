import sys

#config
def check_resource_line(config_line, width, height):
  #Check if config line is all integers
  resource_name, coordinates = config_line.split(":", 1)
  for c in coordinates:
    if c != " " and not c.isdigit():
      raise ValueError("Invalid Configuration File: {} contains non integer characters!".format(resource_name))
  #Check if line has even number of elements
  coordinate_numbers = coordinates.strip().split(" ")
  coordinate_length = len(coordinate_numbers)
  if coordinate_length % 2 == 1:
    raise SyntaxError("Invalid Configuration File: {} has an odd number of elements!".format(resource_name))
  
  coordinate_list = []
  
  #Check if positions are in range of map
  for i in range(0, coordinate_length, 2):
    x = int(coordinate_numbers[i])
    y = int(coordinate_numbers[i + 1])
    if x < 0 or x >= width or y < 0 or y >= height:
      raise ArithmeticError("Invalid Configuration File: {} contains a position that is out of map.".format(resource_name))
    coord = (x, y)
    #Check if positions of home bases or positions next to home bases are occupied
    if (coord == (1, 1) or 
        coord == (width-2, height-2) or 
        coord == (0, 1) or
        coord == (1, 0) or 
        coord == (2, 1) or
        coord == (1, 2) or
        coord == (width-3, height-2) or 
        coord == (width-2, height-3) or 
        coord == (width-1, height-2) or 
        coord == (width-2, height-1)):
      raise ValueError("Invalid Configuration File: The positions of home bases or the positions next to the home bases are occupied!")

    coordinate_list.append(coord)


  return coordinate_list


# Please implement this function according to Section "Read Configuration File"
def load_config_file(filepath):

  width, height = 0, 0
  waters, woods, foods, golds = [], [], [], [] # list of position tuples
  
  #reading config file
  config_file = open(filepath, "r")
  frame_line = config_file.readline().rstrip()
  water_line = config_file.readline().rstrip()
  wood_line = config_file.readline().rstrip()
  food_line = config_file.readline().rstrip()
  gold_line = config_file.readline().rstrip()
  config_file.close()


  #Checking if config file starts with correct labels
  if (not frame_line.startswith("Frame: ") or 
      not water_line.startswith("Water: ") or 
      not wood_line.startswith("Wood: ") or 
      not food_line.startswith("Food: ") or 
      not gold_line.startswith("Gold: ")):
    raise SyntaxError("Invalid Configuration File: format error!")
  
  # WidthxHeight not in the right format
  frame_line = frame_line[7:]
  try:
    temp = frame_line.split("x", 1)
    if len(temp) != 2:
      raise ValueError
    width = int(temp[0])
    height = int(temp[1])
  except ValueError:
    raise SyntaxError("Invalid Configuration File: frame should be in format widthxheight!")
  
  # Width and height between 5 and 7
  if width < 5 or width > 7 or height < 5 or height > 7:
    raise ArithmeticError("Invalid Configuration File: width and height should range from 5 to 7!")

  #Checking if line contains non-integer characters, odd number of elements and positions out of the map
  waters = check_resource_line(water_line, width, height)
  woods = check_resource_line(wood_line, width, height)
  foods = check_resource_line(food_line, width, height)
  golds = check_resource_line(gold_line, width, height)

  #checking duplicate coordinates
  total_coords = waters + woods + foods + golds
  if len(total_coords) > len(set(total_coords)):
    raise SyntaxError("Invalid Configuration File: Duplicate position (x, y)!")

  return width, height, waters, woods, foods, golds

#grid
grid = []
EMPTY = "  "
player = 1
year = 617
#wood at index 0, food at index 1, gold at index 2
WOOD = 0
FOOD = 1
GOLD = 2
player_one_resources = [2, 2, 2]
player_two_resources = [2, 2, 2]
unit_names = {"S" : "Spearman", "A" : "Archer", "K" : "Knight", "T" : "Scout"}
player_one_units = {"S" : [], "A" : [], "K" : [], "T" : []}
player_two_units = {"S" : [], "A" : [], "K" : [], "T" : []}

ATT_DIE = 0
DEF_DIE = 1
BOTH_DIE = 2
fighting = {
  "S" : {"S" : BOTH_DIE, "K" : DEF_DIE, "A" : ATT_DIE, "T" : DEF_DIE}, 
  "K" : {"S" : ATT_DIE, "K" : BOTH_DIE, "A" : DEF_DIE, "T" : DEF_DIE},
  "A" : {"S" : DEF_DIE, "K" : ATT_DIE, "A" : BOTH_DIE, "T" : DEF_DIE}, 
  "T" : {"S" : ATT_DIE, "K" : ATT_DIE, "A" : ATT_DIE, "T" : BOTH_DIE}
}




#set grid dimension and populate with empty strings
def initialise_map(width, height):
  global grid
  for i in range(height):
    grid.append([])
    for j in range(width):
      grid[i].append(EMPTY)
  grid[1][1] = "H1"
  grid[-2][-2] = "H2"

#populating coordinates with resources
def insert_resource(resource_list, resource_string):
  for coordinate in resource_list:
    x = coordinate[0]
    y = coordinate[1]
    grid[y][x] = resource_string

#populating resources in grid
def insert_resources(waters, woods, foods, golds):
  insert_resource(waters, "~~")
  insert_resource(woods, "WW")
  insert_resource(foods, "FF")
  insert_resource(golds, "GG")

#print prices for units
def print_prices():
  print('''Recruit Prices:
  Spearman (S) - 1W, 1F
  Archer (A) - 1W, 1G
  Knight (K) - 1F, 1G
  Scout (T) - 1W, 1F, 1G''')

#printing armies to move
def print_armies(moved):
  print("Armies to Move:")
  if player == 1:
    units = player_one_units
  else:
    units = player_two_units
  ls_spearman = [unit for unit in units["S"] if unit not in moved["S"]]
  ls_archer = [unit for unit in units["A"] if unit not in moved["A"]]
  ls_knight = [unit for unit in units["K"] if unit not in moved["K"]]
  ls_scout = [unit for unit in units["T"] if unit not in moved["T"]]
  if ls_spearman != []:
    print("  Spearman: " + str(ls_spearman).strip("[]"))
  if ls_archer != []:
    print("  Archer: " + str(ls_archer).strip("[]"))
  if ls_knight != []:
    print("  Knight: " + str(ls_knight).strip("[]"))
  if ls_scout != []:
    print("  Scout: " + str(ls_scout).strip("[]"))
  print()



#printing the map
def display_map():
  header = "  X"
  print("Please check the battlefield, commander.")
  width = len(grid[0])
  for i in range(width):
    header = header + "0" + str(i) + " "
  header = header.rstrip() + "X"
  print(header)
  num_dashes = width * 3 - 1
  print(" Y+" + num_dashes * "-" + "+")
  height = len(grid)
  for i in range(height):
    row_string = "0" + str(i) + "|"
    for j in range(width):
      row_string = row_string + grid[i][j] + "|"
    print(row_string)
  print(" Y+" + num_dashes * "-" + "+")

#checking recruiting position is valid
def check_recruitment_position():
  if player == 1:
    home = (1, 1)
  else:
    home = (len(grid[0]) - 2, len(grid) - 2)
  direction = (1, 0)
  for i in range(4):
    adjacent = (home[0] + direction[0], home[1] + direction[1])
    if grid[adjacent[1]][adjacent[0]] == EMPTY:
      return True

    direction = (-direction[1], direction[0])
  return False

#edge commands function
def edge_commands(command):
  if command == "DIS":
    display_map()
    return True
  elif command == "PRIS":
    print_prices()
    return True
  elif command == "QUIT":
    sys.exit()
  else:
    return False

#process of recruiting an army unit
def positive_recruitment(unit, resources, units):
  while True:
    print()
    print("You want to recruit a {}. Enter two integers as format ‘x y’ to place your army.".format(unit_names[unit]))
    army_coordinate = input()
    #checking edge commands first
    if edge_commands(army_coordinate) == True:
      continue
    #checking if coordinates are 2 integers
    temp = army_coordinate.split(" ", 1)
    if len(temp) != 2:
      print("Sorry, invalid input. Try again.")
      continue
    try:
      x = int(temp[0])
      y = int(temp[1])
    except ValueError:
      print("Sorry, invalid input. Try again.")
      continue
    #home base variable 
    if player == 1:
      home = (1, 1)
    else:
      home = (len(grid[0]) - 2, len(grid) - 2)
    #checking to see if positions are valid then subtracting resources based on army unit
    if abs(x - home[0]) + abs(y - home[1]) == 1 and grid[y][x] == EMPTY:
      if unit == "S":
        resources[0] -= 1
        resources[1] -= 1
      elif unit == "A":
        resources[0] -= 1
        resources[2] -= 1
      elif unit == "K":
        resources[1] -= 1
        resources[2] -= 1
      elif unit == "T":
        resources[0] -= 1
        resources[1] -= 1
        resources[2] -= 1
      units[unit].append((x, y))
      grid[y][x] = unit + str(player)
      print()
      print("You has recruited a {}.".format(unit_names[unit]))
      print()
      break
    else:
      print("You must place your newly recruited unit in an unoccupied position next to your home base. Try again.")
      continue

#function to recruit army
def recruit(resources, units):
  while True:
    print("[Your Asset: Wood - {} Food - {} Gold - {}]".format(resources[0], 
                                                               resources[1], 
                                                               resources[2]))
    #checking to see if there are available resources to recruit army unit
    while True:
      if (resources[0] == 0 and resources[1] == 0) or \
        (resources[1] == 0 and resources[2] == 0) or \
        (resources[0] == 0 and resources[2] == 0):
        print("No resources to recruit any armies.")
        return
      #checking to see if there is empty spot next to home base
      if check_recruitment_position() == False:
        print("No place to recruit new armies")
        return
      print()
      print("Which type of army to recruit, (enter) ‘S’, ‘A’, ‘K’, or ‘T’? Enter ‘NO’ to end this stage.")
      command = input()
      #checking edge commands then recruiting army unit
      if edge_commands(command) == True:
        continue
      elif command == "NO":
        return
      elif command in ["S", "A", "K", "T"]:
        if command == "S" and (resources[0] == 0 or resources[1] == 0):
          print("Insufficient resources. Try again.")
          continue
        elif command == "A" and (resources[0] == 0 or resources[2] == 0):
          print("Insufficient resources. Try again.")
          continue
        elif command == "K" and (resources[1] == 0 or resources[2] == 0):
          print("Insufficient resources. Try again.")
          continue
        elif command == "T" and (resources[0] == 0 or resources[1] == 0 or resources[2] == 0):
          print("Insufficient resources. Try again.")
          continue
        positive_recruitment(command, resources, units)
        break
      else:
        print("Sorry, invalid input. Try again.")
        continue

#function to check if a player has units to move
def has_units_to_move(moved):
  for i in range(len(grid)):
    for j in range (len(grid[i])):
      unit = grid[i][j][0]
      if grid[i][j][1] == str(player) and grid[i][j][0] != "H" and not (j, i) in moved[unit]:
        return True
  return False

#moving army units function
def move():
  moved = {"S" : [], "A" : [], "K" : [], "T" : []}
  #checking if there are any units to move
  while True:
    print()
    if has_units_to_move(moved) == False:
      print("No Army to Move: next turn.")
      print()
      break
    print_armies(moved)
    print("Enter four integers as a format ‘x0 y0 x1 y1’ to represent move unit from (x0, y0) to (x1, y1) or ‘NO’ to end this turn.")
    army_movement = input()
    #checking edge commands
    if edge_commands(army_movement) == True:
      continue
    elif army_movement == "NO":
      print()
      break
    ls_army_movement = army_movement.split(" ", 3)
    #checking if input is correct
    if len(ls_army_movement) != 4:
      print("Invalid move. Try again.")
      continue
    try:
      x0 = int(ls_army_movement[0])
      y0 = int(ls_army_movement[1])
      x1 = int(ls_army_movement[2])
      y1 = int(ls_army_movement[3])
    except ValueError:
      print("Invalid move. Try again.")
      continue
    width = len(grid[0])
    height = len(grid)
    #if any coordinates are outside the map
    if x0 >= width or x1 >= width or y0 >= height or y1 >= height or x0 < 0 or x1 < 0 or y0 < 0 or y1 < 0:
      print("Invalid move. Try again.")
      continue
    #if the starting coordinates and the ending coordinates stay the same
    if x0 == x1 and y0 == y1:
      print("Invalid move. Try again.")
      continue
    #if the unit does not belong to the player
    if grid[y1][x1][1] == str(player):
      print("Invalid move. Try again.")
      continue
    #if the unit is a home base or not
    if grid[y0][x0][1] != str(player) or grid[y0][x0][0] == "H":
      print("Invalid move. Try again.")
      continue
    unit = grid[y0][x0][0]
    #if the unit ahs already moved
    if (x0, y0) in moved[unit]:
      print("Invalid move. Try again.")
      continue
    #if the unit is not a scout then it can only move one space
    if unit != "T":
      if not ((abs(x0 - x1) == 1 and y0 == y1) or (abs(y0 - y1) == 1 and x0 == x1)):
        print("Invalid move. Try again.")
        continue
    #if the unit is scout then it can move two spaces
    else:
      if not ((abs(x0 - x1) <= 2 and y0 == y1) or (abs(y0 - y1) <= 2 and x0 == x1)):
        print("Invalid move. Try again.")
        continue
    #if the input is correct then move the unit
    if valid_moves(x0, y0, x1, y1, unit) == True:
      moved[unit].append((x1, y1))

#function to show the deletion of a unit
def delete_unit(x, y):
  if grid[y][x][1] == "1":
    player_units = player_one_units
  else:
    player_units = player_two_units
  player_units[grid[y][x][0]].remove((x, y))
  grid[y][x] = EMPTY

#fucntion to show movement of units from one place to another
def move_unit(x0, y0, x1, y1):
  unit = grid[y0][x0][0]
  grid[y1][x1] = grid[y0][x0]
  grid[y0][x0] = EMPTY
  if player == 1:
    player_units = player_one_units
  else:
    player_units = player_two_units
  replace_coordinate = player_units[unit].index((x0, y0))
  player_units[unit][replace_coordinate] = (x1, y1)

#victory function
def victory(unit):
  print("The army {} captured the enemy’s capital.".format(unit_names[unit]))
  print()
  print("What’s your name, commander?")
  name = input()
  print()
  print("***Congratulation! Emperor {} unified the country in {}.***".format(name, year))
  sys.exit()

#function for the movement of one space
def move_one(x0, y0, x1, y1, unit):
  #dies if in water
  if grid[y1][x1] == "~~":
    print("We lost the army {} due to your command!".format(unit_names[unit]))
    delete_unit(x0, y0)
    return False
  #if the unit is yours or an enemies
  if grid[y1][x1][1] == str(3 - player) and grid[y1][x1][0] != "H":
    enemy_unit = grid[y1][x1][0]
    outcome = fighting[unit][enemy_unit]
    #your unit has died
    if outcome == ATT_DIE:
      print("We lost the army {} due to your command!".format(unit_names[unit]))
      delete_unit(x0, y0)
      return False
    #defender unit has died
    elif outcome == DEF_DIE:
      print("Great! We defeated the enemy {}!".format(unit_names[enemy_unit]))
      delete_unit(x1, y1)
      move_unit(x0, y0, x1, y1)
      return True
    #both die
    elif outcome == BOTH_DIE:
      print("We destroyed the enemy {} with massive loss!".format(unit_names[enemy_unit]))
      delete_unit(x0, y0)
      delete_unit(x1, y1)
      return False
  #collecting resources
  if grid[y1][x1] in ["WW", "FF", "GG"]:
    if player == 1:
      player_resources = player_one_resources
    else:
      player_resources = player_two_resources
    if grid[y1][x1] == "WW":
      print("Good. We collected 2 Wood.")
      player_resources[WOOD] += 2
    elif grid[y1][x1] == "FF":
      print("Good. We collected 2 Food.")
      player_resources[FOOD] += 2
    elif grid[y1][x1] == "GG":
      print("Good. We collected 2 Gold.")
      player_resources[GOLD] += 2
    move_unit(x0, y0, x1, y1)
    return True
  #win condition of capturing home base
  if grid[y1][x1][0] == "H" and grid[y1][x1][1] == str(3 - player):
    victory(unit)
  move_unit(x0, y0, x1, y1)
  return True

#function for movement of two spaces; checks the same as above function
def move_two(x0, y0, x2, y2, unit):
  x1 = (x0 + x2) // 2
  y1 = (y0 + y2) // 2
  for coord in [(x1, y1), (x2, y2)]:
    x, y = coord  
    if grid[y][x] == "~~":
      print("We lost the army {} due to your command!".format(unit_names[unit]))
      delete_unit(x0, y0)
      return False
    #checking is the move is valid
    if grid[y][x][1] == str(3 - player) and grid[y][x][0] != "H":
      enemy_unit = grid[y][x][0]
      outcome = fighting[unit][enemy_unit]
      if outcome == ATT_DIE:
        print("We lost the army {} due to your command!".format(unit_names[unit]))
        delete_unit(x0, y0)
        return False
      elif outcome == BOTH_DIE:
        print("We destroyed the enemy {} with massive loss!".format(unit_names[enemy_unit]))
        delete_unit(x0, y0)
        delete_unit(x, y)
        return False
    if grid[y][x] in ["WW", "FF", "GG"]:
      if player == 1:
        player_resources = player_one_resources
      else:
        player_resources = player_two_resources
      if grid[y][x] == "WW":
        print("Good. We collected 2 Wood.")
        player_resources[WOOD] += 2
      elif grid[y][x] == "FF":
        print("Good. We collected 2 Food.")
        player_resources[FOOD] += 2
      elif grid[y][x] == "GG":
        print("Good. We collected 2 Gold.")
        player_resources[GOLD] += 2
      grid[y][x] = EMPTY
    if grid[y][x][0] == "H" and grid[y][x][1] == str(3 - player):
      victory(unit)
  move_unit(x0, y0, x2, y2)
  return True
  
#printing movement of units
def valid_moves(x0, y0, x1, y1, unit):
  print()
  print("You have moved {} from ({}, {}) to ({}, {}).".format(unit_names[unit], x0, y0, x1, y1))
  if ((abs(x0 - x1) == 1 and y0 == y1) or (abs(y0 - y1) == 1 and x0 == x1)):
    return move_one(x0, y0, x1, y1, unit)
  else:
    return move_two(x0, y0, x1, y1, unit)

#function for counting turns and years
def each_turn():
  player_resources = 0
  player_units = {}
  if player == 1:
    player_resources = player_one_resources
    player_units = player_one_units
  else:
    player_resources = player_two_resources
    player_units = player_two_units
  print("-Year {}-".format(year))
  print()
  print("+++Player {}'s Stage: Recruit Armies+++".format(player))
  print()
  recruit(player_resources, player_units)
  print()
  print("===Player {}'s Stage: Move Armies===".format(player))
  move()

#main 
if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("Usage: python3 little_battle.py <filepath>")
    sys.exit()
  width, height, waters, woods, foods, golds = load_config_file(sys.argv[1])
  print("Configuration file {} was loaded.".format(sys.argv[1]))

  print("Game Started: Little Battle! (enter QUIT to quit the game)")
  print()

  initialise_map(width, height)
  insert_resources(waters, woods, foods, golds)

  display_map()
  print("(enter DIS to display the map)")
  print()

  print_prices()
  print("(enter PRIS to display the price list)")
  print()

  #turn counter
  while True:
    player = 1
    each_turn()
    player = 2
    each_turn()
    year += 1  



