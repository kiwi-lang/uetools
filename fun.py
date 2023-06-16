def list_functions(self, *args):
    """(), Lists all functions available through RPC"""
    return self.call("list_functions", *args)


def get_description(self, *args):
    """(string ElementName), Describes given element"""
    return self.call("get_description", *args)


def list_sensor_types(self, *args):
    """(), Lists all sensor types available to agents. Note that some of sensors might not make sense in a given environment (like reading keyboard in an mouse-only game)."""
    return self.call("list_sensor_types", *args)


def list_actuator_types(self, *args):
    """(), Lists all actuator types available to agents. Note that some of actuators might not make sense in a given environment (like faking keyboard actions in an mouse-only game)."""
    return self.call("list_actuator_types", *args)


def ping(self, *args):
    """(), Checks if the RPC server is still alive and responding."""
    return self.call("ping", *args)


def get_name(self, *args):
    """(), Fetches a human-readable identifier of the environment the external client is connected to."""
    return self.call("get_name", *args)


def is_finished(self, *args):
    """(agent_id), Checks if the game/simulation/episode is done for given agent_id."""
    return self.call("is_finished", *args)


def exit(self, *args):
    """(), Closes the UnrealEngine instance."""
    return self.notify("exit", *args)


def batch_is_finished(self, *args):
    """(), Multi-agent version of is_finished"""
    return self.call("batch_is_finished", *args)


def add_agent(self, *args):
    """Adds a default agent for current environment. Returns added agent's ID if successful, uint(-1) if failed."""
    return self.call("add_agent", *args)


def get_agent_config(self, *args):
    """(uint AgentID), Retrieves given agent's config in JSON formatted string"""
    return self.call("get_agent_config", *args)


def act(self, *args):
    """(uint agent_id, list actions), Distributes the given values array amongst all the actuators, based on actions_space."""
    return self.notify("act", *args)


def none(self, *args):
    """(uint agent_id), Lets the MLAdapter session know that given agent will not continue and is to be removed from the session."""
    return self.call("none", *args)


def get_observations(self, *args):
    """(uint agent_id), fetches all the information gathered by given agent's sensors. Result matches observations_space"""
    return self.call("get_observations", *args)


def batch_get_observations(self, *args):
    """Multi-agent version of 'get_observations'"""
    return self.call("batch_get_observations", *args)


def get_recent_agent(self, *args):
    """(), Fetches ID of the most recently created agent."""
    return self.call("get_recent_agent", *args)


def get_reward(self, *args):
    """(uint agent_id), Fetch current reward for given Agent."""
    return self.call("get_reward", *args)


def batch_get_rewards(self, *args):
    """(), Multi-agent version of 'get_rewards'."""
    return self.call("batch_get_rewards", *args)


def desc_action_space(self, *args):
    """(uint agent_id), Fetches actions space desction for given agent"""
    return self.call("desc_action_space", *args)


def desc_observation_space(self, *args):
    """(uint agent_id), Fetches observations space desction for given agent"""
    return self.call("desc_observation_space", *args)


def reset(self, *args):
    """(), Lets the MLAdapter manager know that the environments should be reset. The details of how this call is handles heavily depends on the environment itself."""
    return self.notify("reset", *args)


def configure_agent(self, *args):
    """(uint agent_id, string json_config), Configures given agent based on json_config. Will throw an exception if given agent doesn't exist."""
    return self.notify("configure_agent", *args)


def create_agent(self, *args):
    """(), Creates a new agent and returns its agent_id."""
    return self.call("create_agent", *args)


def is_agent_ready(self, *args):
    """(uint agent_id), Returns 'true' if given agent is ready to play, including having an avatar"""
    return self.call("is_agent_ready", *args)


def is_ready(self, *args):
    """(), return whether the session is ready to go, i.e. whether the simulation has loaded and started."""
    return self.call("is_ready", *args)


def enable_manual_world_tick(self, *args):
    """(bool bEnable), Controls whether the world is running real time or it's being ticked manually with calls to 'step' or 'request_world_tick' functions. Default is 'real time'."""
    return self.call("enable_manual_world_tick", *args)


def request_world_tick(self, *args):
    """(int TickCount, bool bWaitForWorldTick), Requests a TickCount world ticks. This has meaning only if 'enable_manual_world_tick(true)' has been called prior to this function. If bWaitForWorldTick is true then the call will not return until the world has been ticked required number of times"""
    return self.call("request_world_tick", *args)


def enable_action_duration(self, *args):
    """(uint AgentID, bool bEnableActionDuration, float DurationSeconds), Enable/disable the action durations on the agent with the specified time duration in seconds."""
    return self.call("enable_action_duration", *args)


def wait_for_action_duration(self, *args):
    """(uint AgentID), Wait for the action duration to elapse for the agent. Only works if 'enable_action_duration' has been called previously."""
    return self.call("wait_for_action_duration", *args)


def close_session(self, *args):
    """(), shuts down the current session (along with all the agents)."""
    return self.call("close_session", *args)
