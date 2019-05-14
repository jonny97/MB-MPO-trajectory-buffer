from rllab.envs.base import Env
from rllab.core.serializable import Serializable

class ProxyEnv(Env, Serializable):
    def __init__(self, wrapped_env):
        Serializable.quick_init(self, locals())
        self._wrapped_env = wrapped_env

    @property
    def wrapped_env(self):
        return self._wrapped_env

    def reset(self, *args, **kwargs):
        #print("proxy resets!",args,kwargs)
        #print("proxy resets func: ",self._wrapped_env.reset)
        return self._wrapped_env.reset(*args, **kwargs)

    @property
    def action_space(self):
        return self._wrapped_env.action_space

    @property
    def observation_space(self):
        return self._wrapped_env.observation_space

    def step(self, action):
        return self._wrapped_env.step(action)

    def render(self, *args, **kwargs):
        return self._wrapped_env.render(*args, **kwargs)

    def log_diagnostics(self, paths, prefix=''):
        self._wrapped_env.log_diagnostics(paths, prefix=prefix)

    @property
    def horizon(self):
        return self._wrapped_env.horizon

    def terminate(self):
        self._wrapped_env.terminate()

    def get_param_values(self):
        return self._wrapped_env.get_param_values()

    def set_param_values(self,params):
        self._wrapped_env.set_param_values(params)
