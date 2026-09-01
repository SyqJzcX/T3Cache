import json
import os

CACHE_POLICY = json.loads(os.getenv('CACHE_POLICY', '[]'))


def cal_type(cache_dic, current):
    '''
    Determine calculation type for this step
    '''
    step_index = current['step']
    cache_policy = CACHE_POLICY[step_index]
    lower_threshold = 2
    upper_threshold = 12
    cache_dic['Erta-DiT'] = True
    cache_dic['Delta-DiT-pre'] = True

    if cache_policy == 1:
        current['type'] = 'full'
        if current['step'] not in current['activated_steps']:
            current['activated_steps'].append(current['step'])
    elif cache_policy == 0:
        current['type'] = 'Erta-Cache'
    elif cache_policy == 2:
        if current['stream'] == 'double_stream' and current['layer'] >= lower_threshold and current['layer'] < upper_threshold:
            current['type'] = 'Delta-Cache-pre'
        else:
            current['type'] = 'ToCa'
    else:
        current['type'] = 'Erta-Cache'
