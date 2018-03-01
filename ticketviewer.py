# -*- coding: utf-8 -*-
"""Script for initiating this application.

This script calls create_app() with config name and
runs the application.
"""
from app import create_app
from config import Config
from flask_script import Manager, Command

app = create_app(Config)
manager = Manager(app)

class CommandTest(Command):
    """Command for testing this application."""
    def run(self):
        """
        Run test for this application.
        """
        import unittest
        tests = unittest.TestLoader().discover('tests')
        unittest.TextTestRunner(verbosity=2).run(tests)

class CommandRun(Command):
    """Command for running this application."""
    def run(self):
        """
        Run this application.
        """
        app.run(host="0.0.0.0")

class CommandDebug(Command):
    """Command for debugging this application."""
    def run(self):
        """
        Run this application with debug mode.
        """
        app.run(host="0.0.0.0", debug=True)

manager.add_command('test', CommandTest)
manager.add_command('run', CommandRun)
manager.add_command('debug', CommandDebug)
manager.run()
