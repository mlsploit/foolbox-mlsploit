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

####################################################################################################

docs['attacks']['CarliniWagnerL2Attack'] = {}
docs['attacks']['CarliniWagnerL2Attack']['doctxt'] = (
"""
The L2 version of the Carlini & Wagner attack.

This attack is described in [1]. This implementation is based on the reference implementation by Carlini [2]. For bounds != (0, 1), it differs from [2] because we normalize the squared L2 loss with the bounds.

References
[1] Nicholas Carlini, David Wagner: "Towards Evaluating the Robustness of Neural Networks", https://arxiv.org/abs/1608.04644
[2] (1,2) https://github.com/carlini/nn_robust_attacks
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
docs['attacks']['CarliniWagnerL2Attack']['parameters']['confidence'] = {
  'doctxt': (
"""
Confidence of adversarial examples: a higher value produces adversarials that are further away, but more strongly classified as adversarial.
""")
}
docs['attacks']['CarliniWagnerL2Attack']['parameters']['learning_rate'] = {
  'doctxt': (
"""
The learning rate for the attack algorithm. Smaller values produce better results but take longer to converge.
""")
}
docs['attacks']['CarliniWagnerL2Attack']['parameters']['initial_const'] = {
  'doctxt': (
"""
The initial tradeoff-constant to use to tune the relative importance of distance and confidence. If binary_search_steps is large, the initial constant is not important.
""")
}
docs['attacks']['CarliniWagnerL2Attack']['parameters']['abort_early'] = {
  'doctxt': (
"""
If True, Adam will be aborted if the loss hasn't decreased for some time (a tenth of max_iterations).
""")
}

####################################################################################################

docs['attacks']['DeepFoolL2Attack'] = {}
docs['attacks']['DeepFoolL2Attack']['doctxt'] = (
"""
Simple and close to optimal gradient-based adversarial attack.
""")
docs['attacks']['DeepFoolL2Attack']['parameters'] = {}
docs['attacks']['DeepFoolL2Attack']['parameters']['steps'] = {
  'doctxt': (
"""
Maximum number of steps to perform.
""")
}
docs['attacks']['DeepFoolL2Attack']['parameters']['subsample'] = {
  'doctxt': (
"""
Limit on the number of the most likely classes that should be considered. A small value is usually sufficient and much faster.
""")
}
docs['attacks']['DeepFoolL2Attack']['parameters']['p'] = {
  'doctxt': (
"""
Lp-norm that should be minimzed, must be 2 or np.inf.
""")
}

####################################################################################################

docs['attacks']['DeepFoolLinfinityAttack'] = {}
docs['attacks']['DeepFoolLinfinityAttack']['doctxt'] = (
"""
Simple and close to optimal gradient-based adversarial attack.
""")
docs['attacks']['DeepFoolLinfinityAttack']['parameters'] = {}
docs['attacks']['DeepFoolLinfinityAttack']['parameters']['steps'] = {
  'doctxt': (
"""
Maximum number of steps to perform.
""")
}
docs['attacks']['DeepFoolLinfinityAttack']['parameters']['subsample'] = {
  'doctxt': (
"""
Limit on the number of the most likely classes that should be considered. A small value is usually sufficient and much faster.
""")
}
docs['attacks']['DeepFoolLinfinityAttack']['parameters']['p'] = {
  'doctxt': (
"""
Lp-norm that should be minimzed, must be 2 or np.inf.
""")
}

####################################################################################################

docs['attacks']['FGSM'] = {}
docs['attacks']['FGSM']['doctxt'] = (
"""
The Basic Iterative Method introduced in [1].
This attack is also known as Projected Gradient Descent (PGD) (without random start) or FGMS^k.
References
[1]	Alexey Kurakin, Ian Goodfellow, Samy Bengio, "Adversarial examples in the physical world", https://arxiv.org/abs/1607.02533
""")
docs['attacks']['FGSM']['parameters'] = {}
docs['attacks']['FGSM']['parameters']['binary_search'] = {
  'doctxt': (
"""
Whether to perform a binary search over epsilon and stepsize, keeping their ratio constant and using their values to start the search. If False, hyperparameters are not optimized. Can also be an integer, specifying the number of binary search steps (default 20).
""")
}
docs['attacks']['FGSM']['parameters']['epsilon'] = {
  'doctxt': (
"""
Limit on the perturbation size; if binary_search is True, this value is only for initialization and automatically adapted.
""")
}
docs['attacks']['FGSM']['parameters']['stepsize'] = {
  'doctxt': (
"""
Step size for gradient descent; if binary_search is True, this value is only for initialization and automatically adapted.
""")
}
docs['attacks']['FGSM']['parameters']['iterations'] = {
  'doctxt': (
"""
Number of iterations for each gradient descent run.
""")
}
docs['attacks']['FGSM']['parameters']['random_start'] = {
  'doctxt': (
"""
Start the attack from a random point rather than from the original input.
""")
}
docs['attacks']['FGSM']['parameters']['return_early'] = {
  'doctxt': (
"""
Whether an individual gradient descent run should stop as soon as an adversarial is found.
""")
}

####################################################################################################

docs['attacks']['IterativeGradientSignAttack'] = {}
docs['attacks']['IterativeGradientSignAttack']['doctxt'] = (
"""
Like GradientSignAttack but with several steps for each epsilon.
""")
docs['attacks']['IterativeGradientSignAttack']['parameters'] = {}
docs['attacks']['IterativeGradientSignAttack']['parameters']['epsilons'] = {
  'doctxt': (
"""
Either Iterable of step sizes in the direction of the sign of the gradient or number of step sizes between 0 and max_epsilon that should be tried.
""")
}
docs['attacks']['IterativeGradientSignAttack']['parameters']['max_epsilon'] = {
  'doctxt': (
"""
Largest step size if epsilons is not an iterable.
""")
}
docs['attacks']['IterativeGradientSignAttack']['parameters']['steps'] = {
  'doctxt': (
"""
Number of iterations to run.
""")
}

####################################################################################################

docs['attacks']['LBFGSAttack'] = {}
docs['attacks']['LBFGSAttack']['doctxt'] = (
"""
Perturbs the input with the gradient of the loss w.r.t. the input, gradually increasing the magnitude until the input is misclassified.
Does not do anything if the model does not have a gradient.
""")
docs['attacks']['LBFGSAttack']['parameters'] = {}
docs['attacks']['LBFGSAttack']['parameters']['epsilons'] = {
  'doctxt': (
"""
Either Iterable of step sizes in the direction of the sign of the gradient or number of step sizes between 0 and max_epsilon that should be tried.
""")
}
docs['attacks']['LBFGSAttack']['parameters']['max_epsilon'] = {
  'doctxt': (
"""
Largest step size if epsilons is not an iterable.
""")
}

####################################################################################################

docs['attacks']['ProjectedGradientDescent'] = {}
docs['attacks']['ProjectedGradientDescent']['doctxt'] = (
"""
The Projected Gradient Attack introduced in [1] with random start.

When used without a random start, this attack is also known as Basic Iterative Method (BIM) or FGSM^k.

References
[1]	Aleksander Madry, Aleksandar Makelov, Ludwig Schmidt, Dimitris Tsipras, Adrian Vladu,
"Towards Deep Learning Models Resistant to Adversarial Attacks", https://arxiv.org/abs/1706.06083
""")
docs['attacks']['ProjectedGradientDescent']['parameters'] = {}
docs['attacks']['ProjectedGradientDescent']['parameters']['binary_search'] = {
  'doctxt': (
"""
Whether to perform a binary search over epsilon and stepsize, keeping their ratio constant and using their values to start the search. If False, hyperparameters are not optimized. Can also be an integer, specifying the number of binary search steps (default 20).
""")
}
docs['attacks']['ProjectedGradientDescent']['parameters']['epsilon'] = {
  'doctxt': (
"""
Limit on the perturbation size; if binary_search is True, this value is only for initialization and automatically adapted.
""")
}
docs['attacks']['ProjectedGradientDescent']['parameters']['stepsize'] = {
  'doctxt': (
"""
Step size for gradient descent; if binary_search is True, this value is only for initialization and automatically adapted.
""")
}
docs['attacks']['ProjectedGradientDescent']['parameters']['iterations'] = {
  'doctxt': (
"""
Number of iterations for each gradient descent run.
""")
}
docs['attacks']['ProjectedGradientDescent']['parameters']['random_start'] = {
  'doctxt': (
"""
Start the attack from a random point rather than from the original input.
""")
}
docs['attacks']['ProjectedGradientDescent']['parameters']['return_early'] = {
  'doctxt': (
"""
Whether an individual gradient descent run should stop as soon as an adversarial is found.
""")
}

####################################################################################################

docs['attacks']['RandomProjectedGradientDescent'] = {}
docs['attacks']['RandomProjectedGradientDescent']['doctxt'] = (
"""
The Random Projected Gradient Descent introduced in [1] with random start.

References
[1]	Aleksander Madry, Aleksandar Makelov, Ludwig Schmidt, Dimitris Tsipras, Adrian Vladu,
"Towards Deep Learning Models Resistant to Adversarial Attacks", https://arxiv.org/abs/1706.06083
""")
docs['attacks']['RandomProjectedGradientDescent']['parameters'] = {}
docs['attacks']['RandomProjectedGradientDescent']['parameters']['binary_search'] = {
  'doctxt': (
"""
Whether to perform a binary search over epsilon and stepsize, keeping their ratio constant and using their values to start the search. If False, hyperparameters are not optimized. Can also be an integer, specifying the number of binary search steps (default 20).
""")
}
docs['attacks']['RandomProjectedGradientDescent']['parameters']['epsilon'] = {
  'doctxt': (
"""
Limit on the perturbation size; if binary_search is True, this value is only for initialization and automatically adapted.
""")
}
docs['attacks']['RandomProjectedGradientDescent']['parameters']['stepsize'] = {
  'doctxt': (
"""
Step size for gradient descent; if binary_search is True, this value is only for initialization and automatically adapted.
""")
}
docs['attacks']['RandomProjectedGradientDescent']['parameters']['iterations'] = {
  'doctxt': (
"""
Number of iterations for each gradient descent run.
""")
}
docs['attacks']['RandomProjectedGradientDescent']['parameters']['random_start'] = {
  'doctxt': (
"""
Start the attack from a random point rather than from the original input.
""")
}
docs['attacks']['RandomProjectedGradientDescent']['parameters']['return_early'] = {
  'doctxt': (
"""
Whether an individual gradient descent run should stop as soon as an adversarial is found.
""")
}

####################################################################################################

docs['attacks']['SaltAndPepperNoiseAttack'] = {}
docs['attacks']['SaltAndPepperNoiseAttack']['doctxt'] = (
"""
Increases the amount of salt and pepper noise until the input is misclassified.
""")
docs['attacks']['SaltAndPepperNoiseAttack']['parameters'] = {}
docs['attacks']['SaltAndPepperNoiseAttack']['parameters']['epsilons'] = {
  'doctxt': (
"""
Number of steps to try between probability 0 and 1.
""")
}
docs['attacks']['SaltAndPepperNoiseAttack']['parameters']['repetitions'] = {
  'doctxt': (
"""
Specifies how often the attack will be repeated.
""")
}

####################################################################################################

docs['attacks']['SinglePixelAttack'] = {}
docs['attacks']['SinglePixelAttack']['doctxt'] = (
"""
Perturbs just a single pixel and sets it to the min or max.
""")
docs['attacks']['SinglePixelAttack']['parameters'] = {}
docs['attacks']['SinglePixelAttack']['parameters']['max_pixels'] = {
  'doctxt': (
"""
Maximum number of pixels to try.
""")
}

####################################################################################################

if __name__ == '__main__':
    print(json.dumps(docs))
