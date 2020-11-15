"""
Minimal implementation of Kuhn Poker.
"""

class ChanceNode:
  def __init__(self):
    self.actions = {}
    self.possible_cards = [(1,2), (1,3), (2, 3), (2, 1), (3, 1), (3, 2)]
    for cards in self.possible_cards:
      self.actions[cards] = PlayerNode(0, cards, [])

  def step(self, action):
    return self.actions[action]

  @property
  def infoset_repr(self):
    return "root"

  @property
  def terminal(self):
    return False

class PlayerNode:
  def __init__(self, player, cards, h):
    self.player = player
    self.cards = cards
    self.h = h
    self.children = {} 
    for a in self.actions:
      self.children[a] = PlayerNode(1 - self.player, cards, h + [a]) 

  def step(self, action):
    return self.children[action]
    
  @property
  def actions(self):
    if len(self.h) < 2 or self.h == ['pass', 'bet']:
      return ['pass', 'bet']
    return []

  @property
  def terminal(self):
    return not self.actions
  
  @property 
  def terminal_utility(self):
    assert self.terminal
    p0_rew = 1 if self.cards[0] > self.cards[1] else -1
    if self.h == ['pass', 'pass']:
      return p0_rew
    if self.h[-2:] == ['bet', 'bet']:
      return 2 * p0_rew
    p0_rew = 1 if self.player == 0 else -1
    return p0_rew

  @property
  def infoset_repr(self):
    return "{}:{}".format(self.cards[self.player], self.h)

  

