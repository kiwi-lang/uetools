from __future__ import annotations

from collections import namedtuple
from contextlib import contextmanager

import gym
import gym.spaces

from uetools.commands.editor.ml import UnrealEngineProcess, unrealgame

from .client import Client


def _convert_action_space(space):
    return space


def _convert_observation(space):
    return space


class AgentConfig:
    def __init__(self, config: dict = None) -> None:
        if config is None:
            config = dict()

        config.setdefault("sensors", dict())
        config.setdefault("actuators", dict())
        config.setdefault("avatarClassName", "PlayerController")
        config.setdefault("agentClassName", "")
        config.setdefault("bAutoRequestNewAvatarUponClearingPrev", True)
        config.setdefault("bAvatarClassExact", False)

        self.config = config

    def new_actuator(self, name, **params):
        self.actuators[name] = dict(params=params)
        return self

    def new_sensor(self, name, **params):
        self.sensors[name] = dict(params=params)
        return self

    def __getattr__(self, item):
        if item in self.config:
            return self.config[item]

        return super().__getattr__(self, item)


Step = namedtuple("Step", ["observation", "reward", "done", "info"])


class UnrealEnv(gym.Env):
    metadata = {"render.modes": []}
    reward_range = (-float("inf"), float("inf"))
    spec = None

    def __init__(self) -> None:
        self.instance_ctx = None
        self.instance: UnrealEngineProcess = None
        self.client: Client = None
        self.name: str = None

        self.realtime: bool = False
        self.step_function = lambda: None
        self.frames_step: int = 20
        self.action_duration: int = None
        self.steps: int = 0

        self.agent_id = None
        self.agent_config: None | AgentConfig = None

        self.action_space: gym.Space = None
        self.observation_space: gym.Space = None

    def __enter__(self):
        return self.start()

    def __exit__(self, *args):
        self.close()
        return super().__exit__(*args)

    def start(self):
        self.instance_ctx = unrealgame()
        self.instance = self.instance_ctx.__enter__()

        self.client = Client()
        self.client.add_functions()
        self.name = self.client.get_name()

        # if reacquire:
        #    self.agent_id = self.client.get_recent_agent()
        #    self.client.configure_agent(self.agent_id, self.agent_config)

        # Create the agent
        # ----------------

        if self.agent_config:
            self.agent_id = self.client.create_agent(self.agent_config)
        else:
            self.agent_id = self.client.add_agent()

        # Retrieve the action and observation space for our agent
        self.action_space = _convert_action_space(
            self.client.desc_action_space(self.agent_id)
        )
        self.observation_space = _convert_observation(
            self.client.desc_observation_space(self.agent_id)
        )

        # Configure Tick
        # --------------
        assert (not self.realtime) ^ (
            self.action_duration is not None
        ), "Only one of the option is possible"

        if not self.realtime:

            def world_tick():
                self.client.request_world_tick(self.frames_step, True)

            self.step_function = world_tick

        elif self.action_duration is not None:

            def wait_action():
                self.client.wait_for_action_duration(self.agent_id)

            self.step_function = wait_action
            self.client.enable_action_duration(
                self.agent_id, True, self.action_duration
            )

        self.client.enable_manual_world_tick(not self.realtime)
        return self

    # Gym Interface
    # -------------
    def close(self):
        # Make the client close the instance
        self.client.exit()
        self.instance_ctx.__exit__(None, None, None)

    def reset(self):
        self.client.reset()

        while not self.client.is_ready():
            self.client.act()
            self.skip()

        self.steps = 0
        return self.client.get_observation()

    def step(self, action) -> Step:
        # send action
        if True:
            self.client.act(self.agent_id, action)

        # Reply with result
        obs = self.client.get_observations(self.agent_id)
        reward = self.client.get_reward(self.agent_id)
        is_done = self.client.is_finished(self.agent_id)

        self.steps += 1
        return Step(obs, reward, is_done, dict())

    def render(self, mode="human"):
        # Allow the human to pass some input to the UE through the agent
        pass

    def seed(self, seed=None):
        pass


@contextmanager
def unrealenv():
    with UnrealEnv() as env:
        yield env()
