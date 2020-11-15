"""
Implementation of Simple Bidding game. 

Additionally: for the JPS algorithm we need to have I which has all the same actions. Perhaps this should be represented as another class, that contains all of the PlayerNodes within it. Also have a map from infoset_repr to the actual infoset itself. 

"""
import math
import random

class ChanceNode:
  def __init__(self, n=4, shared_dict=None):
    self.n = n
    self.actions = {}
    self.possible_cards = [(i,j) for i in range(n) for j in range(n)]
    self.infoset_to_action = {}
    for cards in self.possible_cards:
      new_node = PlayerNode(0, cards, [], n, self, shared_dict)
      self.actions[cards] = new_node
      self.infoset_to_action[new_node.infoset_repr] = cards 
      shared_dict[new_node.infoset_repr].h_lst.add(new_node)
    shared_dict["root"] = InfoSet(set([self]))
      
  def step(self, action):
    return self.actions[action]

  def sample(self):
    return random.choice(list(self.actions.values()))

  @property
  def infoset_repr(self):
    return "root"

  @property
  def terminal(self):
    return False


class PlayerNode:
  def __init__(self, player, cards, h, n, parent, shared_dict):
    self.n = n
    self.player = player
    self.cards = cards
    self.h = h
    self.children = {} 
    self.parent = parent
    self.infoset_to_action = {}
    for a in self.actions:
      new_node = PlayerNode(1 - self.player, cards, h + [a], n, self, shared_dict)
      self.children[a] = new_node
      self.infoset_to_action[new_node.infoset_repr] = a
      if shared_dict is not None:
        shared_dict[new_node.infoset_repr].h_lst.add(new_node)
  def step(self, action):
    return self.children[action]
    
  @property
  def actions(self):
    if self.h and self.h[-1] == 0:
      return []
    last = self.h[-1] if self.h else 0
    return list(filter(lambda a : a > last, range(1, int(math.log2(self.n))+ 2)))  + ([0] if self.h else [])

  @property
  def terminal(self):
    return not self.actions

  @property 
  def terminal_utility(self):
    assert self.terminal
    cutoff = 2 ** (self.h[-2] - 1)
    return cutoff if sum(self.cards) >= cutoff else 0 

  @property
  def infoset_repr(self):
    return "{}:{}".format(self.cards[self.player], self.h)
  def __repr__(self):
    return "{}:{}".format(self.cards, self.h)
  def __hash__(self):
    return hash(repr(self))
  def __eq__(self, other):
    return repr(self) == repr(other)

class InfoSet:
  def __init__(self, h_lst=None):
    if not h_lst:
      h_lst = set()
    self.h_lst = h_lst

  def succ(self, a, shared_dict):
    out = {}
    for h in self.h_lst:
      I = h.step(a).infoset_repr
      out[I] = shared_dict[I]
    return list(out.values())

  @property
  def actions(self):
    return next(iter(self.h_lst)).actions
    
  def full_repr(self):
    return str([repr(h) for h in self.h_lst])
  def __repr__(self):
    assert self.h_lst
    return list(self.h_lst)[0].infoset_repr
