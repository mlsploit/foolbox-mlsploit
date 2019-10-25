import json


docs = {}
docs['tagline'] = 'Fool neural networks!'
docs['doctxt'] = 'Foolbox is a Python toolbox to create adversarial examples that fool neural networks.'
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

##################################################

docs['attacks']['CarliniWagnerL2Attack'] = {}
docs['attacks']['CarliniWagnerL2Attack']['doctxt'] = (
"""
The L2 version of the Carlini & Wagner attack.

This attack is described in [1]. This implementation is based on the reference implementation by Carlini [2]. For bounds ≠ (0, 1), it differs from [2] because we normalize the squared L2 loss with the bounds.

References
[1]	Nicholas Carlini, David Wagner: “Towards Evaluating the Robustness of Neural Networks”, https://arxiv.org/abs/1608.04644
[2]	(1, 2) https://github.com/carlini/nn_robust_attacks
""")
docs['attacks']['CarliniWagnerL2Attack']['parameters'] = {}
docs['attacks']['CarliniWagnerL2Attack']['parameters']['binary_search_steps'] = {
  'doctxt': (
"""
The number of steps for the binary search used to find the optimal tradeoff-constant between distance and confidence.
""")
}
docs['attacks']['CarliniWagnerL2Attack']['parameters']['max_iterations'] = {
  'doctxt': (
"""
The maximum number of iterations. Larger values are more accurate; setting it too small will require a large learning rate and will produce poor results.
""")
}

if __name__ == '__main__':
    print(json.dumps(docs))