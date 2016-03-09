# Tic Tac Toe
# jacobcui123@gmail.com

import copy
import random
import os

class Board(object):
  def __init__(self, clean=False):
    self.reset_blocks()
    self.reset_blocks(ai=True)
    self.clean = clean

  def reset_blocks(self, ai=False):
    if not ai:
      self.blocks = [' '] * 10
    else:
      self.ai_blocks = copy.copy(self.blocks)    

  def is_full(self):
    """Checks whether the block on the board has been taken.

    Return: True if taken, otherwise False
    """
    for i in range(1, 10):
      if self.is_block_free(i):
        return False
    return True

  def is_block_free(self, move, ai=False):
    if ai:
      self.reset_blocks(ai=True)
      return self.ai_blocks[move] == ' '
    return self.blocks[move] == ' '
    
  def draw(self):
    if self.clean:
      os.system('clear')
    for i in (7, 4, 1):
      print(' {} | {} | {} |'.format(self.blocks[i].strip() or i,
                                     self.blocks[i + 1].strip() or i + 1,
                                     self.blocks[i + 2].strip() or i + 2))
      print('-' * 12)    
    
class TicTacToe(object):
  def __init__(self, board):
    self.board = board
    self.x = 'x'
    self.o = 'o'
    self.assign_chess()

  def play_again(self):
    # This function returns True if the player wants to play again, otherwise it returns False.
    return raw_input('Do you want to play again? [Y/N])').strip().lower().startswith('y')

  def is_winning(self, le, ai=False):
    # Given a board and a player's letter, this function returns True
    # if that player has won.  We use bo instead of board and le
    # instead of letter so we don't have to type as much.
    if ai:
      use_blocks = self.board.ai_blocks
    else:
      use_blocks = self.board.blocks
    return ((use_blocks[7] == le and use_blocks[8] == le and use_blocks[9] == le) or # across the top
            (use_blocks[4] == le and use_blocks[5] == le and use_blocks[6] == le) or # across the middle
            (use_blocks[1] == le and use_blocks[2] == le and use_blocks[3] == le) or # across the bottom
            (use_blocks[7] == le and use_blocks[4] == le and use_blocks[1] == le) or # down the left side
            (use_blocks[8] == le and use_blocks[5] == le and use_blocks[2] == le) or # down the middle
            (use_blocks[9] == le and use_blocks[6] == le and use_blocks[3] == le) or # down the right side
            (use_blocks[7] == le and use_blocks[5] == le and use_blocks[3] == le) or # diagonal
            (use_blocks[9] == le and use_blocks[5] == le and use_blocks[1] == le)) # diagonal

  def move_to(self, letter, move, ai=False):
    if ai:
      self.board.reset_blocks(ai=True)
      self.board.ai_blocks[move] = letter
    else:
      self.board.blocks[move] = letter

  def get_player_move(self):
    # Let the player type in their move.
    move = ''
    while True:
      move = raw_input('What is your next ({}) move? (1-9)'.format(self.chess['human'])).strip()
      try:
        if int(move) in range(10)[1:] or self.board.is_block_free(int(move)):
          break
      except ValueError:
        continue
    return int(move)

  def get_computer_move(self):
    # Given a board and the computer's letter, determine where to move
    # and return that move.
    if self.chess['computer'] == self.x:
      self.chess['human'] = self.o
    else:
      self.chess['human'] = self.x

    # Checks if computer can win in the next move.
    for i in range(1, 10):
      if self.board.is_block_free(i, ai=True):
        self.move_to(self.chess['computer'], i, ai=True)
        if self.is_winning(self.chess['computer'], ai=True):
          return i

    # Checks if human could win on their next move, and block them.
    for i in range(1, 10):
      if self.board.is_block_free(i, ai=True):
        self.move_to(self.chess['human'], i, ai=True)
        if self.is_winning(self.chess['human'], ai=True):
          return i

    # Try to take the center, if not taken.
    if self.board.is_block_free(5):
      return 5

    # Try to take one of the corners, if not taken.
    move = self.random_move([1, 3, 7, 9])
    if move != None:
      return move

    # Move on one of the sides.
    return self.random_move([2, 4, 6, 8])

  def first_player(self):
    # Randomly choose the player who goes first.
    if random.randint(0, 1) == 0:
      return 'computer'
    else:
      return 'human'

  def main_loop(self):
    self.board.draw()

    while True:
      # Reset the board
      player = self.first_player()
      print('The {} ({}) will go first.'.format(player, self.chess[player]))
      game_is_on = True
    
      while game_is_on:
        if player == 'human':
          # Human's turn.
          self.board.draw()
          move = self.get_player_move()
          self.move_to(self.chess['human'], move)
    
          if self.is_winning(self.chess['human']):
            self.board.draw()
            print("Can't believe it, you won!")
            game_is_on = False
          else:
            if self.board.is_full():
              self.board.draw()
              print('The game ends as a draw!')
              break
            else:
              player = 'computer'
        else:
          # Computer's turn.
          move = self.get_computer_move()
          self.move_to(self.chess['computer'], move)
    
          if self.is_winning(self.chess['computer']):
            self.board.draw()
            print('You lose :(')
            game_is_on = False
          else:
            if self.board.is_full():
              self.board.draw()
              print('The game ends as a draw!')
              break
            else:
              player = 'human'
    
      if not self.play_again():
        print('Bye, Chicken!')
        break
      else:
        self.board.reset_blocks()
        self.board.draw()
        
  def assign_chess(self):
    """Nominates letter to be used as chess for players.

    Returns: A dictionary.
    """
    # Lets the player type which letter they want to be.  Returns a
    # list with the player's letter as the first item, and the
    # computer's letter as the second.
    letter = ''
    while not (letter == self.x or letter == self.o):
        letter = raw_input('Do you want to use x or o?').strip()
        print letter.strip().lower()
    # the first element in the list is the player's letter, the second
    # is the computer's letter.
    if letter == self.x:
      self.chess = {'human': self.x, 'computer': self.o}
    else:
      self.chess = {'human': self.o, 'computer': self.x}

  def random_move(self, movesList):
    # Returns a valid move from the passed list on the passed board.
    # Returns None if there is no valid move.
    possible_moves = []
    for i in movesList:
      if self.board.is_block_free(i):
        possible_moves.append(i)

    if len(possible_moves) != 0:
        return random.choice(possible_moves)
    else:
        return None
  
if __name__ == '__main__':
  # Use Board(clean=True) to refresh screen.
  board = Board()
  game = TicTacToe(board)
  game.main_loop()

