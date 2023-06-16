# Copyright Epic Games, Inc. All Rights Reserved.

import logging
import socket
import time

import msgpack
import numpy as np

LOCALHOST = "127.0.0.1"
DEFAULT_PORT = 15151

REQUEST = 0
RESPONSE = 1
NOTIFY = 2


logger = logging.getLogger(__name__)


class RemoteException(Exception):
    pass


standard_function = [
    "list_functions",
    "get_description",
    "list_sensor_types",
    "list_actuator_types",
    "ping",
    "get_name",
    "is_finished",
    "exit",
    "batch_is_finished",
    "add_agent",
    "get_agent_config",
    "act",
    "none",
    "get_observations",
    "batch_get_observations",
    "get_recent_agent",
    "get_reward",
    "batch_get_rewards",
    "desc_action_space",
    "desc_observation_space",
    "reset",
    "configure_agent",
    "create_agent",
    "is_agent_ready",
    "is_ready",
    "enable_manual_world_tick",
    "request_world_tick",
    "enable_action_duration",
    "wait_for_action_duration",
    "close_session",
]

sensor_types = {
    "MLAdapterSensor_AIPerception": 1,
    "MLAdapterSensor_Attribute": 2,
    "MLAdapterSensor_Camera": 3,
    "MLAdapterSensor_EnhancedInput": 4,
    "MLAdapterSensor_Input": 5,
    "MLAdapterSensor_Movement": 6,
}

actuator_types = {
    "MLAdapterActuator_Camera": 1,
    "MLAdapterActuator_EnhancedInput": 2,
    "MLAdapterActuator_InputKey": 3,
}

noreturns = {
    "exit",
    "act",
    "batch_act",
    "reset",
    "disconnect",
    "configure_agent",
}


class Client:
    """Simple client that does not rely on the outdated msgpackrpc lib

    Notes
    -----
    It also looks to be more reliable.
    It has a lot less moving parts.

    """

    FUNCNAME_LIST_FUNCTIONS = "list_functions"
    FUNCNAME_PING = "ping"

    def __init__(
        self,
        server_address=LOCALHOST,
        server_port=DEFAULT_PORT,
        timeout=20,
        reconnect_limit=1024,
        **kwargs,
    ):
        self.host = server_address
        self.port = server_port
        self.packer = msgpack.Packer()
        self.unpacker = msgpack.Unpacker()
        self.buffer = np.empty(8192, dtype="<u1")
        self.uid = 0
        self.timeout = timeout
        self.retries = reconnect_limit
        self.latency = 0
        self.sock = None

    def close(self):
        if self.sock is not None:
            self.sock.close()
            self.sock = None

    def connect(self, retries=None, timeout=None, sleep_step=1):
        if timeout is None:
            timeout = self.timeout

        if retries is None:
            retries = self.retries

        start = time.time()

        for i in range(retries):
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                self.sock.settimeout(self.timeout)
                self.sock.connect((self.host, self.port))
                logger.info(
                    "Connected after %5.2f s  and %d retries", time.time() - start, i
                )
                return
            except ConnectionRefusedError:
                pass

            time.sleep(sleep_step)

            if timeout and time.time() - start > timeout:
                raise TimeoutError()
        else:
            raise ConnectionRefusedError()

    def getlatency(self):
        self.call(Client.FUNCNAME_PING)
        return self.latency

    def ensure_connection(self):
        logger.debug("Ensure connection")
        self.getlatency()
        logger.info("Latency (RTT) %5.2f ms", self.latency / 1e6)
        return

    def notify(self, method, *args):
        return self._retry(self._notify, method, args)

    def call(self, method, *args):
        """Call a RPC, re-connect once if the connection drops"""
        return self._retry(self._call, method, *args)

    def multicall(self, methods):
        return self._retry(self._multicall, methods)

    def _multicall(self, methods):
        messages = dict()
        results = []

        for i, (method, args) in enumerate(methods):
            mid = self.send_message(method, args)
            messages[mid] = i
            results.append(None)

        while len(messages) > 0:
            kind, mid, error, result = self.receive_message()

            uid = messages.pop(mid, None)

            assert uid is not None
            assert kind == RESPONSE

            results[uid] = error, result

        return results

    def _call(self, method, *args):
        start = time.perf_counter_ns()

        msgid1 = self.send_message(method, args)
        kind, msgid2, error, result = self.receive_message()

        assert kind == RESPONSE
        assert msgid1 == msgid2

        self.latency = time.perf_counter_ns() - start
        if error is None:
            return result

        raise RemoteException(error)

    def _retry(self, fun, *args, retry=2):
        """
        Parameters
        ----------

        fun: callable
            Function that will be retried in case of an exception

        *args:
            arguments forwarded to fun

        retry: int
            number of time to retry reconnecting to the server

        Raises
        ------
        TimeoutError
            raise when socket operation times out, not retried

        ConnectionResetError
            raised when server close the connection unexpectedly, retried until
            max retry count

        """
        for i in range(retry):
            try:
                return fun(*args)

            except socket.timeout as e:
                raise TimeoutError() from e

            except ConnectionResetError:
                if i == 0:
                    self.connect()
                else:
                    raise

    def send_message(self, method, args):
        uid = self.uid
        payload = msgpack.packb([REQUEST, uid, method, args])
        self.sock.sendall(payload)
        self.uid += 1
        return uid

    def _notify(self, method, args):
        payload = msgpack.packb([NOTIFY, method, args])
        self.sock.sendall(payload)

    def receive_message(self):
        while True:
            # Finish reading buffered messages first
            for msg in self.unpacker:
                return msg

            size = self.sock.recv_into(self.buffer)
            self.unpacker.feed(memoryview(self.buffer[:size]))

    def _add_function(self, function_name):
        # Function that do not have a return type are sent using notify
        # this avoid an explicit sync on the python side
        # also reduce bandwidth usage
        # maybe this dimension could be added to the `Librarian.AddRPCFunctionDescription`
        #

        if function_name in noreturns:
            wrap = self.notify
        else:
            wrap = self.call

        self.__dict__[function_name] = lambda *args: wrap(function_name, *args)

    def generate_methods(self):
        function_list = self.call(Client.FUNCNAME_LIST_FUNCTIONS)

        with open("fun.py", "w") as file:
            for fname in function_list:
                doc = self.get_description(fname)

                w = "call"
                if fname in noreturns:
                    w = "notify"

                file.write(f"    def {fname}(self, *args):\n")
                file.write(f'        """{doc}"""\n')
                file.write(f'        return self.{w}("{fname}", *args)\n\n')

    def add_functions(self):
        self.ensure_connection()

        function_list = self.call(Client.FUNCNAME_LIST_FUNCTIONS)

        for fname in function_list:
            self._add_function(fname)

        logger.debug(f"Functions bound: {function_list}")

    @property
    def connected(self):
        try:
            self.ensure_connection()
            return True
        except ConnectionResetError:
            return False

    # Generated
    # ---------
    #
    # If you call add_functions() those will get overridden
    #
    #

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
