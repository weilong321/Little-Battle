from little_battle import load_config_file
folder_path = "./invalid_files/"

def test_file_not_found():
  try: 
    load_config_file(folder_path + "kfbheiof.txt")
    assert False
  except FileNotFoundError as err:
    assert True
  except Exception:
    assert False

def test_format_error():
  try: 
    load_config_file(folder_path + "format_error_file.txt")
    assert False
  except SyntaxError as err:
    assert str(err) == "Invalid Configuration File: format error!"
  except Exception:
    assert False

def test_frame_format_error():
  try: 
    load_config_file(folder_path + "frame_format_error_file.txt")
    assert False
  except SyntaxError as err:
    assert str(err) == "Invalid Configuration File: frame should be in format widthxheight!"
  except Exception:
    assert False

def test_frame_out_of_range():
  try: 
    load_config_file(folder_path + "format_out_of_range_file.txt")
    assert False
  except ArithmeticError as err:
    assert str(err) == "Invalid Configuration File: width and height should range from 5 to 7!"
  except Exception:
    assert False

def test_non_integer():
  try: 
    load_config_file(folder_path + "non_integer_file.txt")
    assert False
  except ValueError as err:
    assert str(err) == "Invalid Configuration File: Wood contains non integer characters!"
  except Exception:
    assert False

def test_out_of_map():
  try: 
    load_config_file(folder_path + "out_of_map_file.txt")
    assert False
  except ArithmeticError as err:
    assert str(err) == "Invalid Configuration File: Food contains a position that is out of map."
  except Exception:
    assert False

def test_occupy_home_or_next_to_home():
  try: 
    load_config_file(folder_path + "occupy_home_file.txt")
    assert False
  except ValueError as err:
    assert str(err) == "Invalid Configuration File: The positions of home bases or the positions next to the home bases are occupied!"
  except Exception:
    assert False
  try: 
    load_config_file(folder_path + "occupy_next_to_home_file.txt")
    assert False
  except ValueError as err:
    assert str(err) == "Invalid Configuration File: The positions of home bases or the positions next to the home bases are occupied!"
  except Exception:
    assert False

def test_duplicate_position():
  try: 
    load_config_file(folder_path + "dupli_pos_in_single_line.txt")
    assert False
  except SyntaxError as err:
    assert str(err) == "Invalid Configuration File: Duplicate position (x, y)!"
  except Exception:
    assert False
  try: 
    load_config_file(folder_path + "dupli_pos_in_multiple_lines.txt")
    assert False
  except SyntaxError as err:
    assert str(err) == "Invalid Configuration File: Duplicate position (x, y)!"
  except Exception:
    assert False

def test_odd_length():
  try: 
    load_config_file(folder_path + "odd_length_file.txt")
    assert False
  except SyntaxError as err:
    assert str(err) == "Invalid Configuration File: Gold has an odd number of elements!"
  except Exception:
    assert False

def test_valid_file():
  try: 
    width, height, waters, woods, foods, golds = load_config_file("config.txt")
    assert width == 5
    assert height == 5
    assert waters == [(0, 0), (4, 2), (1, 3)]
    assert woods == [(0, 2), (2, 4)]
    assert foods == [(0, 4), (3, 1)]
    assert golds == [(4, 1), (2, 2)]
  except Exception:
    assert False

if __name__ == "__main__":
  test_file_not_found()
  test_format_error()
  test_frame_format_error()
  test_frame_out_of_range()
  test_non_integer()
  test_out_of_map()
  test_occupy_home_or_next_to_home()
  test_duplicate_position()
  test_odd_length()
  test_valid_file()