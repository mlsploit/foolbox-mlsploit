import json


docs = {}
docs['doctxt'] = 'Foolbox module doctx here...'
docs['attacks'] = {}


##################################################

docs['attacks']['BasicIterativeMethod'] = {}
docs['attacks']['BasicIterativeMethod']['doctxt'] = (
"""
The Basic Iterative Method introduced in [1].

This attack is also known as Projected Gradient Descent (PGD) (without random start) or FGMS^k.

References
[1] Alexey Kurakin, Ian Goodfellow, Samy Bengio, "Adversarial examples in the physical world", https://arxiv.org/abs/1607.02533
""")
docs['attacks']['BasicIterativeMethod']['parameters'] = {}
docs['attacks']['BasicIterativeMethod']['parameters']['binary_search'] = {
  'doctxt': (
"""
Whether to perform a binary search over epsilon and stepsize, keeping their ratio constant and using their values to start the search. If False, hyperparameters are not optimized.
""")
}
docs['attacks']['BasicIterativeMethod']['parameters']['epsilon'] = {
  'doctxt': (
"""
Limit on the perturbation size; if binary_search is True, this value is only for initialization and automatically adapted.
""")
}
docs['attacks']['BasicIterativeMethod']['parameters']['stepsize'] = {
  'doctxt': (
"""
Step size for gradient descent; if binary_search is True, this value is only for initialization and automatically adapted.
""")
}
docs['attacks']['BasicIterativeMethod']['parameters']['iterations'] = {
  'doctxt': (
"""
Number of iterations for each gradient descent run.
""")
}
docs['attacks']['BasicIterativeMethod']['parameters']['random_start'] = {
  'doctxt': (
"""
Start the attack from a random point rather than from the original input.
""")
}
docs['attacks']['BasicIterativeMethod']['parameters']['return_early'] = {
  'doctxt': (
"""
Whether an individual gradient descent run should stop as soon as an adversarial is found.
""")
}


if __name__ == '__main__':
    print(json.dumps(docs))