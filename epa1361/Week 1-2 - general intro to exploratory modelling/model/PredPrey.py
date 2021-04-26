"""
Python model "PredPrey.py"
Translated using PySD version 0.10.0
"""
from __future__ import division
import numpy as np
from pysd import utils
import xarray as xr

from pysd.py_backend.functions import cache
from pysd.py_backend import functions

_subscript_dict = {}

_namespace = {
    'TIME': 'time',
    'Time': 'time',
    'predator growth': 'predator_growth',
    'predators': 'predators',
    'prey': 'prey',
    'prey growth': 'prey_growth',
    'predator loss': 'predator_loss',
    'predator efficiency': 'predator_efficiency',
    'prey loss': 'prey_loss',
    'initial predators': 'initial_predators',
    'initial prey': 'initial_prey',
    'predator loss rate': 'predator_loss_rate',
    'prey birth rate': 'prey_birth_rate',
    'predation rate': 'predation_rate',
    'FINAL TIME': 'final_time',
    'INITIAL TIME': 'initial_time',
    'SAVEPER': 'saveper',
    'TIME STEP': 'time_step'
}

__pysd_version__ = "0.10.0"

__data = {'scope': None, 'time': lambda: 0}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


def time():
    return __data['time']()


@cache('step')
def predator_growth():
    """
    Real Name: b'predator growth'
    Original Eqn: b'predator efficiency*predators*prey'
    Units: b''
    Limits: (None, None)
    Type: component

    b''
    """
    return predator_efficiency() * predators() * prey()


@cache('step')
def predators():
    """
    Real Name: b'predators'
    Original Eqn: b'INTEG ( predator growth-predator loss, initial predators)'
    Units: b''
    Limits: (0.0, None)
    Type: component

    b''
    """
    return _integ_predators()


@cache('step')
def prey():
    """
    Real Name: b'prey'
    Original Eqn: b'INTEG ( prey growth-prey loss, initial prey)'
    Units: b''
    Limits: (0.0, None)
    Type: component

    b''
    """
    return _integ_prey()


@cache('step')
def prey_growth():
    """
    Real Name: b'prey growth'
    Original Eqn: b'prey birth rate*prey'
    Units: b''
    Limits: (None, None)
    Type: component

    b''
    """
    return prey_birth_rate() * prey()


@cache('step')
def predator_loss():
    """
    Real Name: b'predator loss'
    Original Eqn: b'predator loss rate*predators'
    Units: b''
    Limits: (None, None)
    Type: component

    b''
    """
    return predator_loss_rate() * predators()


@cache('run')
def predator_efficiency():
    """
    Real Name: b'predator efficiency'
    Original Eqn: b'0.002'
    Units: b''
    Limits: (None, None)
    Type: constant

    b''
    """
    return 0.002


@cache('step')
def prey_loss():
    """
    Real Name: b'prey loss'
    Original Eqn: b'predation rate*predators*prey'
    Units: b''
    Limits: (None, None)
    Type: component

    b''
    """
    return predation_rate() * predators() * prey()


@cache('run')
def initial_predators():
    """
    Real Name: b'initial predators'
    Original Eqn: b'20'
    Units: b''
    Limits: (None, None)
    Type: constant

    b''
    """
    return 20


@cache('run')
def initial_prey():
    """
    Real Name: b'initial prey'
    Original Eqn: b'50'
    Units: b''
    Limits: (None, None)
    Type: constant

    b''
    """
    return 50


@cache('run')
def predator_loss_rate():
    """
    Real Name: b'predator loss rate'
    Original Eqn: b'0.06'
    Units: b''
    Limits: (None, None)
    Type: constant

    b''
    """
    return 0.06


@cache('run')
def prey_birth_rate():
    """
    Real Name: b'prey birth rate'
    Original Eqn: b'0.025'
    Units: b''
    Limits: (None, None)
    Type: constant

    b''
    """
    return 0.025


@cache('run')
def predation_rate():
    """
    Real Name: b'predation rate'
    Original Eqn: b'0.0015'
    Units: b''
    Limits: (None, None)
    Type: constant

    b''
    """
    return 0.0015


@cache('run')
def final_time():
    """
    Real Name: b'FINAL TIME'
    Original Eqn: b'365'
    Units: b'Day'
    Limits: (None, None)
    Type: constant

    b'The final time for the simulation.'
    """
    return 365


@cache('run')
def initial_time():
    """
    Real Name: b'INITIAL TIME'
    Original Eqn: b'0'
    Units: b'Day'
    Limits: (None, None)
    Type: constant

    b'The initial time for the simulation.'
    """
    return 0


@cache('step')
def saveper():
    """
    Real Name: b'SAVEPER'
    Original Eqn: b'TIME STEP'
    Units: b'Day'
    Limits: (0.0, None)
    Type: component

    b'The frequency with which output is stored.'
    """
    return time_step()


@cache('run')
def time_step():
    """
    Real Name: b'TIME STEP'
    Original Eqn: b'0.25'
    Units: b'Day'
    Limits: (0.0, None)
    Type: constant

    b'The time step for the simulation.'
    """
    return 0.25


_integ_predators = functions.Integ(lambda: predator_growth() - predator_loss(),
                                   lambda: initial_predators())

_integ_prey = functions.Integ(lambda: prey_growth() - prey_loss(), lambda: initial_prey())
