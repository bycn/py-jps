import pprint
from collections import defaultdict
import pandas as pd
import random
import pickle
import copy


def jps_main(root, shared_dict, base_sigma, num_iter=1, seed=0):
  random.seed(seed)
  def jps(last_sigma, running_sigma, I_cand, active_set, pi_sigma_prime):
    pi_sigma_p = dict(pi_sigma_prime)
    def get_new_reachability(h):
      build_up = 1
      curr_h = h
      while curr_h.infoset_repr != "root":
        child_h = curr_h
        curr_h = curr_h.parent
        curr_I = curr_h.infoset_repr
        curr_to_child_action = curr_h.infoset_to_action[child_h.infoset_repr]
        if curr_I in active_set:
          build_up *= pi_sigma_prime[repr(curr_h)] * int(active_set[curr_I] == curr_to_child_action)
          break
        build_up *= last_sigma[curr_I, curr_to_child_action] 
      return build_up
    def compute_J(I, one_hot_action, pi_sigma_prime, value_sigma):
      out = 0
      for h in I.h_lst:
        out += pi_sigma_prime[repr(h)]  * (value_sigma[repr(h.step(one_hot_action))] - value_sigma[repr(h)])
      return out
    for I in I_cand:
      for h in I.h_lst: 
        pi_sigma_prime[repr(h)] = get_new_reachability(h)
    best_r = 0   
    for I in I_cand:
      for a_i in I.actions:
        curr_active_set = dict(active_set)
        curr_active_set[repr(I)] = a_i
        r = jps(last_sigma, running_sigma, I.succ(a_i, shared_dict), curr_active_set, pi_sigma_prime) + compute_J(I, a_i, pi_sigma_prime, value_sigma)
        if r > best_r:
          best_r = r
          for a in I.actions:
            running_sigma[(repr(I),a)] = int(a == a_i)
    return best_r

  next_sigma = dict(base_sigma)
  for it in range(num_iter):
    pi_sigma = defaultdict(int)
    value_sigma = defaultdict(int)
    def init(pi_sigma, value_sigma,h, running_pi):
      I = h.infoset_repr
      if I == "root":
        value_sigma[repr(h)] = 1/len(h.actions) * sum([init(pi_sigma, value_sigma, h.step(a), 1/len(h.actions)) for a in h.actions])
        return value_sigma[repr(h)]
      pi_sigma[repr(h)] = running_pi
      if h.terminal:
        value_sigma[repr(h)] = h.terminal_utility
        return value_sigma[repr(h)]
      v = 0
      for a in h.actions:
        v += next_sigma[(I,a)] * init(pi_sigma, value_sigma, h.step(a), running_pi * next_sigma[(I, a)])
      value_sigma[repr(h)] = v
      return v
    init(pi_sigma, value_sigma, root, 1)
    I_one = shared_dict[root.sample().infoset_repr]
    jps(dict(next_sigma), next_sigma, [I_one], {}, {})
  return next_sigma





        
      
      