import numpy as np
import yaml


# Original location_sequence function definition to compare any changes with
def location_sequence(start, end, steps):
        lats = np.linspace(start[0], end[0], steps)
        longs = np.linspace(start[1], end[1], steps)
        return np.vstack([lats, longs]).transpose()


def make_fixture(start, end, steps):
    params_dict = {'start': start, 'end': end, 'steps': steps, 'result': None}
    params_dict['result'] = location_sequence(params_dict['start'], params_dict['end'], params_dict['steps']).tolist()
    return params_dict

with open('location_sequence_fixtures.yaml', 'w') as file_to_write:
    file_to_write.write('# Increasing latitude longitude\n')
    file_to_write.write(yaml.dump([make_fixture((0, 0), (1, 1), 10)]))
    file_to_write.write('\n# Decreasing latitude longitude\n')
    file_to_write.write(yaml.dump([make_fixture((1, 1), (0, 0), 10)]))
    file_to_write.write('\n# No change in position\n')
    file_to_write.write(yaml.dump([make_fixture((0, 0), (0, 0), 10)]))


