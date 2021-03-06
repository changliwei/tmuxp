# -*- coding: utf8 - *-
"""
    tmuxp.config
    ~~~~~~~~~~~~

    tmuxp helps you manage tmux workspaces.

    :copyright: Copyright 2013 Tony Narlock.
    :license: BSD, see LICENSE for details
"""


class ConfigExpand(object):
    '''Expand configuration into full form. Enables shorthand forms for
    tmuxinator config.

    This is necessary to keep the code in the :class:`Builder` clean and also
    allow for neat, short-hand configurations.

    As a simple example, internally, tmuxinator expects that config options
    like ``shell_command`` are a list (array)::

        'shell_command': ['htop']

    Tmuxinator configs allow for it to be simply a string::

        'shell_command': 'htop'

    Kaptan will load JSON/YAML/INI files into python dicts for you.

    For testability all expansion / shorthands are in methods here, each will
    check for any expandable config properties in the session, windows and
    their panes and apply the full form to self.config accordingly.

    self.expand will automatically expand all shortened config options. Adding
    ``.config`` will return the expanded config::

        ConfigExpand(config).expand().config

    They also return the context of self, so they are
    chainable.
    '''

    def __init__(self, config):
        '''
        :param config: the configuration for the session
        :type config: dict
        '''

        self.config = config

    def expand(self):
        return self.expand_shell_command().expand_shell_command_before()

    def expand_shell_command(self):
        '''
        iterate through session, windows, and panes for ``shell_command``, if
        it is a string, turn to list.
        '''
        config = self.config

        def _expand(c):
            '''any config section, session, window, pane that can
            contain the 'shell_command' value
            '''
            if ('shell_command' in c and
                    isinstance(c['shell_command'], basestring)):
                    c['shell_command'] = [c['shell_command']]

            return c

        config = _expand(config)
        for window in config['windows']:
            window = _expand(window)
            window['panes'] = [_expand(pane) for pane in window['panes']]

        self.config = config

        return self

    def expand_shell_command_before(self):
        '''
        iterate through session, windows, and panes for
        ``shell_command_before``, if it is a string, turn to list.
        '''
        config = self.config

        def _expand(c):
            '''any config section, session, window, pane that can
            contain the 'shell_command' value
            '''
            if ('shell_command_before' in c and
                    isinstance(c['shell_command_before'], basestring)):
                    c['shell_command_before'] = [c['shell_command_before']]

            return c

        config = _expand(config)
        for window in config['windows']:
            window = _expand(window)
            window['panes'] = [_expand(pane) for pane in window['panes']]

        self.config = config

        return self


class ConfigTrickleDown(object):
    '''Trickle down / inherit config values

    This will only work if config has been expand with ConfigExpand()

    tmuxp allows certain commands to be default at the session, window
    level. shell_command_before trickles down and prepends the
    ``shell_command`` for the pane.
    '''
    def __init__(self, config):
        '''
        :param config: the session configuration
        :type config: dict
        '''
        self.config = config

    def trickle(self):
        self.trickle_shell_command_before()
        return self

    def trickle_shell_command_before(self):
        '''
        prepends a pane's ``shell_command`` list with the window and sessions'
        ``shell_command_before``.
        '''
        config = self.config

        if 'shell_command_before' in config:
            self.assertIsInstance(config['shell_command_before'], list)
            session_shell_command_before = config['shell_command_before']
        else:
            session_shell_command_before = []

        for windowconfitem in config['windows']:
            window_shell_command_before = []
            if 'shell_command_before' in windowconfitem:
                window_shell_command_before = windowconfitem['shell_command_before']

            for paneconfitem in windowconfitem['panes']:
                pane_shell_command_before = []
                if 'shell_command_before' in paneconfitem:
                    pane_shell_command_before += paneconfitem['shell_command_before']

                if 'shell_command' not in paneconfitem:
                    paneconfitem['shell_command'] = list()

                paneconfitem['shell_command'] = session_shell_command_before + window_shell_command_before + pane_shell_command_before + paneconfitem['shell_command']

        self.config = config
