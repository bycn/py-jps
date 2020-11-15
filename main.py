import cfr
import kuhn
import jps
import simple_bidding
from collections import defaultdict
import pprint
import pickle
import pandas as pd

# root = kuhn.ChanceNode()

shared_dict = defaultdict(simple_bidding.InfoSet)
root = simple_bidding.ChanceNode(n=4, shared_dict=shared_dict)
print(len(shared_dict))
print(sum([len(a.h_lst) for a in shared_dict.values()]))

# with open('cfr1k.pkl', 'rb') as f:
#   base_sigma = pickle.load(f)  

base_sigma = cfr.cfr(root, 1000, chance=True, seed=0)

# base_sigma = defaultdict(lambda: 0)
# print(base_sigma)

def evaluate_policy(sigma):
  # Makes a pure policy, and evaluates it.
  rew = 0
  table = defaultdict(lambda: defaultdict(int))
  def traverse(node, s, i, j):
    nonlocal rew
    if node.terminal:
      table[i][j] = s + "({})".format(str(node.terminal_utility))
      rew += node.terminal_utility
      return
    I = node.infoset_repr
    if I == "root":
      for i, j in node.actions:
        traverse(node.step((i,j)),s,i,j)
      return
    card, a_h = I.split(":")
    a_h = eval(a_h)
    best_a, highest_prob = None, 0
    for a in node.actions:
      if sigma[(I, a)] > highest_prob:
        best_a = a
        highest_prob = sigma[(I,a)]
    traverse(node.step(best_a), s + str(best_a), i, j)
  traverse(root, "", -1, -1)
  return rew / (root.n * root.n), table 
rew_base, table_base = evaluate_policy(base_sigma)
print("Base reward")
print(pd.DataFrame(dict(table_base)).transpose())
print(rew_base)


sigma = jps.jps_main(root, shared_dict, base_sigma,1000)
rew, table = evaluate_policy(sigma)
print("after jps")
# print(pd.DataFrame(dict(table)).transpose())
print(rew)
# pprint.pp(sigma)

# pprint.pp(base_sigma)
# pprint.pp(sigma)

# kap = cfr.cfr(root, 1000, chance=True, seed=0)
# print(kap)
