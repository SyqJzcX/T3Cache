from .force_scheduler import force_scheduler
import json
import os

CACHE_POLICY = json.loads(os.getenv('CACHE_POLICY', '[]'))


def cal_type(cache_dic, current):
    '''
    Determine calculation type for this step
    '''
    # first_step = (current['step'] < cache_dic['first_enhance'])
    step_index = current['step']  # 0 -> 49
    cache_policy = CACHE_POLICY[step_index]
    threshold = 19
    cache_dic['Delta-DiT'] = False  # 关闭 Delta-DiT
    cache_dic['Erta-DiT'] = True  # 开启 Erta-DiT
    cache_dic['Delta-DiT-pre'] = True  # 开启 Delta-DiT-pre
    # current['type'] = 'full'
    # current['activated_steps'].append(current['step'])

    # if first_step:
    #     current['type'] = 'full'
    #     if current['step'] not in current['activated_steps']:
    #         current['activated_steps'].append(current['step'])
    # 完整计算
    if cache_policy == 1:
        current['type'] = 'full'
        if current['step'] not in current['activated_steps']:
            current['activated_steps'].append(current['step'])
    # 中等票数的前期
    elif cache_policy == 2:
        # 残差跳过19个双流块与前19个单流块
        if current['stream'] == 'double_stream' or current['layer'] < threshold:
            current['type'] = 'Delta-Cache-pre'
        # 后19层单流块用 ToCa
        else:
            current['type'] = 'ToCa'
    # 残差跳过
    elif cache_policy == 0:
        current['type'] = 'Erta-Cache'
