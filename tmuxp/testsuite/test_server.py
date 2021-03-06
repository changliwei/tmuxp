import unittest
from random import randint
from .. import t, Session, Window, Pane
from ..util import tmux
from .helpers import TmuxTestCase, TEST_SESSION_PREFIX


class ServerTestCase(TmuxTestCase):
    def test_has_session(self):
        self.assertTrue(t.has_session(self.TEST_SESSION_NAME))
        self.assertFalse(t.has_session('asdf2314324321'))

    def test_has_clients(self):
        pass

    def test_has_sessions(self):
        pass

    def test_socket(self):
        ''' tmux allows the following configuration options for the server

        ``-L`` socket_name  file name of socket. which will be stored in
               env TMUX_TMPDIR or /tmp if unset.)

        ``-S`` socket_path  (alternative path for server socket)

        '''
        pass

    def test_config(self):
        ''' test whether passing a ``file`` into Server will alter the tmux
            options for server, session and windows '''
        pass

if __name__ == '__main__':
    unittest.main()
