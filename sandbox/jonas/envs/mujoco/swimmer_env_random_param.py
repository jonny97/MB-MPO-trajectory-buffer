from rllab.envs.base import Step
from rllab.misc.overrides import overrides
import numpy as np
from rllab.core.serializable import Serializable
from rllab.misc import logger
from rllab.misc import autoargs
from rllab.misc.overrides import overrides
from rllab_maml.envs.base import Step

from rllab.core.serializable import Serializable
from sandbox.jonas.envs.mujoco.base_env_rand_param import BaseEnvRandParams
from rllab.envs.mujoco.swimmer_env import SwimmerEnv
from sandbox.jonas.envs.helpers import get_all_function_arguments



class SwimmerEnvRandParams(BaseEnvRandParams, SwimmerEnv, Serializable):

    FILE = 'swimmer.xml'

    def __init__(self, *args, log_scale_limit=2.0, fix_params=False, rand_params=BaseEnvRandParams.RAND_PARAMS, random_seed=None, max_path_length=None, **kwargs):
        """
        Half-Cheetah environment with randomized mujoco parameters
        :param log_scale_limit: lower / upper limit for uniform sampling in logspace of base 2
        :param random_seed: random seed for sampling the mujoco model params
        :param fix_params: boolean indicating whether the mujoco parameters shall be fixed
        :param rand_params: mujoco model parameters to sample
        """

        args_all, kwargs_all = get_all_function_arguments(self.__init__, locals())
        BaseEnvRandParams.__init__(*args_all, **kwargs_all)
        SwimmerEnv.__init__(self, *args, **kwargs)
        Serializable.__init__(*args_all, **kwargs_all)

    @overrides
    def step(self, action):
        self.forward_dynamics(action)
        next_obs = self.get_current_obs()
        lb, ub = self.action_bounds
        scaling = (ub - lb) * 0.5
        ctrl_cost = 0.5 * self.ctrl_cost_coeff * np.sum(
            np.square(action / scaling))
        forward_reward = self.get_body_comvel("torso")[0]
        reward = forward_reward - ctrl_cost
        done = False
        return Step(next_obs, reward, done)

    def reward(self, obs, action, obs_next):
        lb, ub = self.action_bounds
        scaling = (ub - lb) * 0.5
        if obs.ndim == 2 and action.ndim == 2:
            vel = (obs_next[:, -3] - obs[:, -3]) / 0.05
            ctrl_cost = 0.5 * self.ctrl_cost_coeff * np.sum(np.square(action / scaling), axis=1)
            return vel - ctrl_cost
        else:
            ctrl_cost = 0.5 * self.ctrl_cost_coeff * np.sum(
                np.square(action / scaling))
            vel = (obs_next[-3] - obs[-3]) / 0.05
            return vel - ctrl_cost


    @overrides
    def log_diagnostics(self, paths, prefix=''):
        if len(paths) > 0:
            progs = [
                path["observations"][-1][-3] - path["observations"][0][-3]
                for path in paths
            ]
            logger.record_tabular(prefix +'AverageForwardProgress', np.mean(progs))
            logger.record_tabular(prefix + 'MaxForwardProgress', np.max(progs))
            logger.record_tabular(prefix + 'MinForwardProgress', np.min(progs))
            logger.record_tabular(prefix + 'StdForwardProgress', np.std(progs))
        else:
            logger.record_tabular(prefix + 'AverageForwardProgress', np.nan)
            logger.record_tabular(prefix + 'MaxForwardProgress', np.nan)
            logger.record_tabular(prefix + 'MinForwardProgress', np.nan)
            logger.record_tabular(prefix + 'StdForwardProgress', np.nan)