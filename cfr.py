"""
Vanilla CFR 
"""
import pprint
from collections import defaultdict

def cfr(root, num_iter=1):
  sigma = defaultdict(lambda:1/len(root.actions))
  cum_sigma = defaultdict(lambda:0)
  cum_regret = defaultdict(lambda:0)
  avg_sigma = defaultdict(lambda:1/len(root.actions))

  def cfr_traversal(node, pi_0, pi_1):
    if node.terminal:
      return node.terminal_utility[0]
    I = node.infoset_repr
    if I == "root":
      return 1/len(node.actions) * sum([cfr_traversal(node.step(a), pi_0, pi_1) for a in node.actions])
    utility = 0
    child_utilities = {}
    cf_sigma = lambda player: sigma[(I, a)] if player == node.player else 1 
    for a in node.actions:
      child_utilities[a] = cfr_traversal(node.step(a), pi_0 * cf_sigma(0), pi_1 * cf_sigma(1))
      utility += sigma[(I, a)] * child_utilities[a]
    curr_pi, cf_pi = (pi_0, pi_1) if node.player == 0 else (pi_1, pi_0) 
    sign = -1 if node.player == 1 else 1
    for a in node.actions:
      cum_regret[(I, a)] += sign * cf_pi * (child_utilities[a] - utility)
      cum_sigma[(I, a)] += curr_pi * sigma[(I, a)]
    return utility

  def next_sigma(node):
    if node.terminal:
      return
    I = node.infoset_repr      
    if I != "root":
      total_regret = sum([cum_regret[(I, a)] for a in node.actions if cum_regret[(I,a)] > 0])
      for a in node.actions:
        if total_regret > 0:
          sigma[(I,a)] = max(0, cum_regret[(I, a)]) / total_regret
        else:
          sigma[(I,a)] = 1/len(node.actions)
    for a in node.actions:
      next_sigma(node.step(a))

  def update_avg_sigma(node):
    if node.terminal:
      return
    I = node.infoset_repr
    total_sigma = sum([cum_sigma[(I, a)] for a in node.actions])    
    for a in node.actions:
      if total_sigma:
        avg_sigma[(I, a)] = cum_sigma[(I,a)] / total_sigma
      update_avg_sigma(node.step(a))

  def game_utility(node, player=0):
    if node.terminal:
      return node.terminal_utility[player]
    utility = 0
    I = node.infoset_repr
    for a in node.actions:
      utility += avg_sigma[(I,a)] * game_utility(node.step(a), player)
    return utility

  for iter in range(num_iter):
    cfr_traversal(root, 1, 1)
    next_sigma(root)

  update_avg_sigma(root)
  print(game_utility(root,0))
  print(game_utility(root,1))
  pprint.pp(dict(avg_sigma))

    
    


    





