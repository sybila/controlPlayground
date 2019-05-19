data = {
'settings': {
	'testing': True,
	'max_values': 100,
	'timeout': 60,
	'conf_tol': 0.06,
	'lin_tol': 0.04,
	'OD_MIN': 0.43,
	'OD_MAX': 0.47,
	'optimum_type': -1,
	'working_dir': '.log/RUNNING',
	'parameter_space': {
		'light-red' : [50, 1500],
		'light-blue': [50, 1500]
	}
},
'nodes': [
	{
		'devices': [
			{
				'name': 'PBR',
				'ID': 'PBR01',
				'adress': 72700001,
				'initial_setup': [
					{
						'command': 'set_thermoregulator_state',
						'arguments': [1]
					},
					{
						'command': 'set_pwm',
						'arguments': [50, True]
					},
					{
						'command': 'set_temp',
						'arguments': [24]
					},
					{
						'command': 'turn_on_light',
						'arguments': [0, True]
					},
					{
						'command': 'turn_on_light',
						'arguments': [1, True]
					},
					{
						'command': 'set_pump_state',
						'arguments': [5, False]
					}
				]
			}
		],
		'parameter_values': [265, 100],
	},
	{
		'devices': [
			{
				'name': 'PBR',
				'ID': 'PBR02',
				'adress': '72700002',
				'initial_setup': [
					{
						'command': 'set_thermoregulator_state',
						'arguments': [1]
					},
					{
						'command': 'set_pwm',
						'arguments': [50, True]
					},
					{
						'command': 'set_temp',
						'arguments': [24]
					},
					{
						'command': 'turn_on_light',
						'arguments': [0, True]
					},
					{
						'command': 'turn_on_light',
						'arguments': [1, True]
					},
					{
						'command': 'set_pump_state',
						'arguments': [5, False]
					}
				]
			}
		],
		'parameter_values': [130, 50],
	},
]
}