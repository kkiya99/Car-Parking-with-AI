# PPO-PyTorch
Minimal PyTorch implementation of Proximal Policy Optimization with clipped objective for OpenAI gym environments.

## Usage

- To test a preTrained network : run `test.py` or `test_continuous.py`
- To train a new network : run `PPO.py` or `PPO_continuous.py`
- All the hyperparameters are in the `PPO.py` or `PPO_continuous.py` file


## Dependencies
Trained and tested on:
```
Python 3.6
PyTorch 1.0
NumPy 1.15.3
```

## Results

PPO Discrete LunarLander-v2 (1200 episodes)           |  PPO Continuous BipedalWalker-v2 (4000 episodes)
:-------------------------:|:-------------------------:
![](https://github.com/nikhilbarhate99/PPO-PyTorch/blob/master/gif/PPO_LunarLander-v2.gif) |  ![](https://github.com/nikhilbarhate99/PPO-PyTorch/blob/master/gif/PPO_BipedalWalker-v2.gif)


## References

- PPO [paper](https://arxiv.org/abs/1707.06347)
- [OpenAI Spinning up](https://spinningup.openai.com/en/latest/)
