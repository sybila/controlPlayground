data = {
'data': {
    'settings': {
        'testing': 'True',
        'max_values': '100',
        'timeout': '60',
        'conf_tol': '0.06',
        'lin_tol': '0.04',
        'OD_MIN': '0.43',
        'OD_MAX': '0.47',
        'optimum_type': '-1',
        'working_dir': '.log/RUNNING',
        'parameter_space': {
            'light-red' : '[50, 1500]',
            'light-blue': '[50, 1500]'
        }
    },
    'nodes': {
        'n0': {
            'devices': {
                'd0': {
                    'name': 'PBR',
                    'ID': 'PBR01',
                    'adress': '72700001',
                    'initial_setup': {
                        'i0': {
                            'command': 'set_thermoregulator_state',
                            'arguments': {
                                'a0': '1'
                            }
                        },
                        'i1': {
                            'command': 'set_pwm',
                            'arguments': {
                                'a0': '50',
                                'a1': 'True'
                            }
                        },
                        'i2': {
                            'command': 'set_temp',
                            'arguments': {
                                'a0': '24'
                            }
                        },
                        'i3': {
                            'command': 'turn_on_light',
                            'arguments': {
                                'a0': '0',
                                'a1': 'True'
                            }
                        },
                        'i4': {
                            'command': 'turn_on_light',
                            'arguments': {
                                'a0': '1',
                                'a1': 'True'
                            }
                        },
                        'i5': {
                            'command': 'set_pump_state',
                            'arguments': {
                                'a0': '5',
                                'a1': 'False'
                            }
                        }
                    }
                }
            },
            'parameter_values': '[265, 100]',
        },
        'n1': {
            'devices': {
                'd0': {
                    'name': 'PBR',
                    'ID': 'PBR02',
                    'adress': '72700002',
                    'initial_setup': {
                        'i0': {
                            'command': 'set_thermoregulator_state',
                            'arguments': {
                                'a0': '1'
                            }
                        },
                        'i1': {
                            'command': 'set_pwm',
                            'arguments': {
                                'a0': '50',
                                'a1': 'True'
                            }
                        },
                        'i2': {
                            'command': 'set_temp',
                            'arguments': {
                                'a0': '24'
                            }
                        },
                        'i3': {
                            'command': 'turn_on_light',
                            'arguments': {
                                'a0': '0',
                                'a1': 'True'
                            }
                        },
                        'i4': {
                            'command': 'turn_on_light',
                            'arguments': {
                                'a0': '1',
                                'a1': 'True'
                            }
                        },
                        'i5': {
                            'command': 'set_pump_state',
                            'arguments': {
                                'a0': '5',
                                'a1': 'False'
                            }
                        }
                    }
                }
            },
            'parameter_values': '[130, 50]',
        },
    }
}
}