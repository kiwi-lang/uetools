import logging
import re
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
                logger.info("Connected after %5.2f s  and %d retries", time.time() - start, i)
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
        return self.latency / 1e6

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

    # Automatic Code generation
    # for auto completion
    # -------------------------
    def generate_methods(self):
        function_list = self.call(Client.FUNCNAME_LIST_FUNCTIONS)

        args_pat = re.compile(r"\((?P<ARGS>.*)\), (?P<DOC>.*)")

        type_renamp = {
            "uint": "int",
            "string": "str",
        }

        name_remap = {
            "AgentID": "agent_id",
            "Adds": "",
            "ElementName": "element_name",
            "TickCount": "tick_count",
            "bWaitForWorldTick": "wait_for_world_tick",
            "bEnableActionDuration": "enable_action_duration",
            "DurationSeconds": "duration_sec",
            "bEnable": "enable",
        }

        def extract_args(args):
            final = []
            forward = []
            args = args.replace("(", "").replace(")", "")

            for arg in args.split(", "):
                r = arg.split(" ")

                if len(r) == 2:
                    type, name = arg.split(" ")

                    type = type_renamp.get(type, type)
                    name = name_remap.get(name, name)

                    final.append(f"{name}: {type}")
                    forward.append(name)
                else:
                    final.append(r[0])
                    forward.append(r[0])

            return final, forward

        def generate_args(doc):
            result = args_pat.search(doc)

            if result:
                data = result.groupdict()
                doc = data["DOC"]
                args = data["ARGS"]

                args, forward = extract_args(args)
            else:
                args = []
                forward = []

            args = ["self"] + args
            forward = [f'"{fname}"'] + forward

            args = ", ".join(filter(lambda x: len(x) > 0, args))
            forward = ", ".join(filter(lambda x: len(x) > 0, forward))

            return args, forward, doc

        with open("fun.py", "w") as file:
            for fname in function_list:
                doc = self.get_description(fname)

                w = "call"
                if fname in noreturns:
                    w = "notify"

                args, forward, doc = generate_args(doc)

                file.write(f"    def {fname}({args}):\n")
                file.write(f'        """{doc}"""\n')
                file.write(f"        return self.{w}({forward})\n\n")

    # Generated
    # ---------
    #
    # If you call add_functions() those will get overridden
    #
    #

    def list_functions(self):
        """Lists all functions available through RPC"""
        return self.call("list_functions")

    def get_description(self, element_name: str):
        """Describes given element"""
        return self.call("get_description", element_name)

    def list_sensor_types(self):
        """Lists all sensor types available to agents.

        Notes
        -----

        Some of sensors might not make sense in a given environment
        like reading keyboard in an mouse-only game.

        """
        return self.call("list_sensor_types")

    def list_actuator_types(self):
        """Lists all actuator types available to agents.

        Notes
        -----

        Some of actuators might not make sense in a given environment
        like faking keyboard actions in an mouse-only game.

        """
        return self.call("list_actuator_types")

    def ping(self):
        """Checks if the RPC server is still alive and responding."""
        return self.call("ping")

    def get_name(self):
        """Fetches a human-readable identifier of the environment the external client is connected to."""
        return self.call("get_name")

    def is_finished(self, agent_id):
        """Checks if the game/simulation/episode is done for given agent_id."""
        return self.call("is_finished", agent_id)

    def exit(self):
        """Closes the UnrealEngine instance."""
        return self.notify("exit")

    def batch_is_finished(self):
        """Multi-agent version of is_finished"""
        return self.call("batch_is_finished")

    def add_agent(self):
        """Adds a default agent for current environment. Returns added agent's ID if successful, uint(-1) if failed."""
        return self.call("add_agent")

    def get_agent_config(self, agent_id: int):
        """Retrieves given agent's config in JSON formatted string"""
        return self.call("get_agent_config", agent_id)

    def act(self, agent_id: int, actions: list):
        """Distributes the given values array amongst all the actuators, based on actions_space."""
        return self.notify("act", agent_id, actions)

    def none(self, agent_id: int):
        """Lets the MLAdapter session know that given agent will not continue and is to be removed from the session."""
        return self.call("none", agent_id)

    def get_observations(self, agent_id: int):
        """fetches all the information gathered by given agent's sensors. Result matches observations_space"""
        return self.call("get_observations", agent_id)

    def batch_get_observations(self):
        """Multi-agent version of 'get_observations'"""
        return self.call("batch_get_observations")

    def get_recent_agent(self):
        """Fetches ID of the most recently created agent."""
        return self.call("get_recent_agent")

    def get_reward(self, agent_id: int):
        """Fetch current reward for given Agent."""
        return self.call("get_reward", agent_id)

    def batch_get_rewards(self):
        """Multi-agent version of 'get_rewards'."""
        return self.call("batch_get_rewards")

    def desc_action_space(self, agent_id: int):
        """Fetches actions space desction for given agent"""
        return self.call("desc_action_space", agent_id)

    def desc_observation_space(self, agent_id: int):
        """Fetches observations space desction for given agent"""
        return self.call("desc_observation_space", agent_id)

    def reset(self):
        """Lets the MLAdapter manager know that the environments should be reset.
        The details of how this call is handles heavily depends on the environment itself.
        """
        return self.notify("reset")

    def configure_agent(self, agent_id: int, json_config: str):
        """Configures given agent based on json_config. Will throw an exception if given agent doesn't exist."""
        return self.notify("configure_agent", agent_id, json_config)

    def create_agent(self):
        """Creates a new agent and returns its agent_id."""
        return self.call("create_agent")

    def is_agent_ready(self, agent_id: int):
        """Returns 'true' if given agent is ready to play, including having an avatar"""
        return self.call("is_agent_ready", agent_id)

    def is_ready(self):
        """return whether the session is ready to go, i.e. whether the simulation has loaded and started."""
        return self.call("is_ready")

    def enable_manual_world_tick(self, enable: bool):
        """Controls whether the world is running real time or it's being ticked manually
        with calls to 'step' or 'request_world_tick' functions.

        Default is 'real time'.

        """
        return self.call("enable_manual_world_tick", enable)

    def request_world_tick(self, tick_count: int, wait_for_world_tick: bool):
        """Requests a TickCount world ticks.
        This has meaning only if 'enable_manual_world_tick(true)' has been called prior to this function.
        If bWaitForWorldTick is true then the call will not return
        until the world has been ticked required number of times
        """
        return self.call("request_world_tick", tick_count, wait_for_world_tick)

    def enable_action_duration(self, agent_id: int, enable_action_duration: bool, duration_sec: float):
        """Enable/disable the action durations on the agent with the specified time duration in seconds."""
        return self.call("enable_action_duration", agent_id, enable_action_duration, duration_sec)

    def wait_for_action_duration(self, agent_id: int):
        """Wait for the action duration to elapse for the agent.
        Only works if 'enable_action_duration' has been called previously."""
        return self.call("wait_for_action_duration", agent_id)

    def close_session(self):
        """shuts down the current session (along with all the agents)."""
        return self.call("close_session")
