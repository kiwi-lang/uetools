# Copyright Epic Games, Inc. All Rights Reserved.

import time
import socket
import logging

import msgpack
import numpy as np


LOCALHOST = '127.0.0.1'
DEFAULT_PORT = 15151

REQUEST = 0
RESPONSE = 1
NOTIFY = 2


logger = logging.getLogger(__name__)


class RemoteException(Exception):
    pass


standard_function = [
    'list_functions', 
    'get_description', 
    'list_sensor_types', 
    'list_actuator_types', 
    'ping', 
    'get_name', 
    'is_finished', 
    'exit', 
    'batch_is_finished', 
    'add_agent', 
    'get_agent_config', 
    'act', 
    'none', 
    'get_observations', 
    'batch_get_observations', 
    'get_recent_agent', 
    'get_reward', 
    'batch_get_rewards', 
    'desc_action_space', 
    'desc_observation_space', 
    'reset', 
    'configure_agent', 
    'create_agent', 
    'is_agent_ready', 
    'is_ready', 
    'enable_manual_world_tick',
    'request_world_tick', 
    'enable_action_duration', 
    'wait_for_action_duration', 
    'close_session'
]


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
                    f"Connected after %5.2f s  and %d retries", time.time() - start, i
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
        logger.debug('Ensure connection')
        self.getlatency()
        logger.info("Latency (RTT) %5.2f ms", self.latency / 1e+6)
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
        # also reduce bandwith usage
        # mayve this dimension could be added to the `Librarian.AddRPCFunctionDescription`
        #
        noreturns = {
            'exit',
            'act',
            'batch_act',
            'reset',
            'disconnect',
            'configure_agent'
        }

        if function_name in noreturns:
            wrap = self.notify
        else:
            wrap = self.call

        self.__dict__[function_name] = lambda *args: wrap(function_name, *args)

    def add_functions(self):
        self.ensure_connection()

        function_list = self.call(Client.FUNCNAME_LIST_FUNCTIONS)
        print(function_list)

        for fname in function_list:
            self._add_function(fname)

        logger.debug("Functions bound: {}".format(function_list))

    @property
    def connected(self):
        try:
            self.ensure_connection()
            return True
        except ConnectionResetError:
            return False
