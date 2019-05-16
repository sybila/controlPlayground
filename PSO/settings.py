data = {
	'settings': {
		'testing': 'False',
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
		'0': {
			'devices': {
				'0': {
					'name': 'PBR',
					'ID': 'PBR01',
					'adress': '72700001',
					'initial_setup': {
						'0': {
							'command': 'set_thermoregulator_state',
							'arguments': {
								'0': '1'
							}
						},
						'1': {
							'command': 'set_pwm',
							'arguments': {
								'0': '50',
								'1': 'True'
							}
						},
						'2': {
							'command': 'set_temp',
							'arguments': {
								'0': '24'
							}
						},
						'3': {
							'command': 'turn_on_light',
							'arguments': {
								'0': '0',
								'1': 'True'
							}
						},
						'4': {
							'command': 'turn_on_light',
							'arguments': {
								'0': '1',
								'1': 'True'
							}
						},
						'5': {
							'command': 'set_pump_state',
							'arguments': {
								'0': '5',
								'1': 'False'
							}
						}
					}
				}
			},
			'parameter_values': '[265, 100]',
		},
		'1': {
			'devices': {
				'0': {
					'name': 'PBR',
					'ID': 'PBR02',
					'adress': '72700002',
					'initial_setup': {
						'0': {
							'command': 'set_thermoregulator_state',
							'arguments': {
								'0': '1'
							}
						},
						'1': {
							'command': 'set_pwm',
							'arguments': {
								'0': '50',
								'1': 'True'
							}
						},
						'2': {
							'command': 'set_temp',
							'arguments': {
								'0': '24'
							}
						},
						'3': {
							'command': 'turn_on_light',
							'arguments': {
								'0': '0',
								'1': 'True'
							}
						},
						'4': {
							'command': 'turn_on_light',
							'arguments': {
								'0': '1',
								'1': 'True'
							}
						},
						'5': {
							'command': 'set_pump_state',
							'arguments': {
								'0': '5',
								'1': 'False'
							}
						}
					}
				}
			},
			'parameter_values': '[130, 50]',
		},
	}
}