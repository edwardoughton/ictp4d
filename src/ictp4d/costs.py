"""
Cost module
Author: Edward Oughton
Date: April 2019

Based off the repo pysim5g:
https://github.com/edwardoughton/pysim5g

"""
import math
from itertools import tee
import collections, functools, operator

def find_single_network_cost(region, option, costs, global_parameters,
    country_parameters, core_lut):
    """
    Calculates the annual total cost using capex and opex.

    Parameters
    ----------
    region : dict
        The region being assessed and all associated parameters.
    # strategy : str
    #     Infrastructure sharing strategy.
    costs : dict
        Contains the costs of each necessary equipment item.
    global_parameters : dict
        Contains all global_parameters.
    country_parameters :
        ???
    backhaul_lut : dict
        Backhaul distance by region.

    Returns
    -------
    output : list of dicts
        Contains a list of costs, with affliated discounted capex and
        opex costs.

    """
    strategy = option['strategy']
    generation = strategy.split('_')[0]
    core = strategy.split('_')[1]
    backhaul = strategy.split('_')[2]

    new_sites = region['new_sites']
    upgraded_sites = region['upgraded_sites']
    all_sites = new_sites + upgraded_sites

    new_backhaul = region['backhaul_new']

    regional_cost = []
    regional_asset_cost = []

    for i in range(1, int(all_sites) + 1):

        if i <= upgraded_sites and generation == '3G':

            cost_structure = upgrade_to_3g(region,strategy, costs,
                global_parameters, core_lut, country_parameters)

            backhaul_quant = backhaul_quantity(i, new_backhaul)

            total_cost, cost_by_asset = calc_costs(region, strategy, cost_structure,
                backhaul_quant, global_parameters, country_parameters)

            regional_cost.append(total_cost)
            regional_asset_cost.append(cost_by_asset)

        if i <= upgraded_sites and generation == '4G':

            cost_structure = upgrade_to_4g(region,strategy, costs,
                global_parameters, core_lut, country_parameters, )

            backhaul_quant = backhaul_quantity(i, new_backhaul)

            total_cost, cost_by_asset = calc_costs(region, strategy, cost_structure,
                backhaul_quant, global_parameters, country_parameters)

            regional_cost.append(total_cost)
            regional_asset_cost.append(cost_by_asset)


        if i > upgraded_sites and generation == '3G':

            cost_structure = greenfield_3g(region, strategy, costs,
                global_parameters, core_lut, country_parameters)

            backhaul_quant = backhaul_quantity(i, new_backhaul)

            total_cost, cost_by_asset = calc_costs(region, strategy, cost_structure,
                backhaul_quant, global_parameters, country_parameters)

            regional_cost.append(total_cost)
            regional_asset_cost.append(cost_by_asset)


        if i > upgraded_sites and generation == '4G':

            cost_structure = greenfield_4g(region, strategy, costs,
                global_parameters, core_lut, country_parameters)

            backhaul_quant = backhaul_quantity(i, new_backhaul)

            total_cost, cost_by_asset = calc_costs(region, strategy, cost_structure,
                backhaul_quant, global_parameters, country_parameters)

            regional_cost.append(total_cost)
            regional_asset_cost.append(cost_by_asset)


    counter = collections.Counter()
    for d in regional_asset_cost:
        counter.update(d)
    test = dict(counter)

    network_cost = 0
    for k, v in test.items():
        region[k] = v
        network_cost += v

    region['network_cost'] = network_cost

    return region


def backhaul_quantity(i, new_backhaul):
    if i <= new_backhaul:
        return 1
    else:
        return 0


def upgrade_to_3g(region, strategy, costs, global_parameters,
    core_lut, country_parameters):
    """
    Reflects the baseline scenario of needing to build a single dedicated
    network.

    """
    backhaul = '{}_backhaul'.format(strategy.split('_')[2])
    sharing = strategy.split('_')[3]
    geotype = region['geotype'].split(' ')[0]

    # generation_core_backhaul_sharing_networks_spectrum_tax
    network_strategy = strategy.split('_')[4]
    networks = country_parameters['networks']['baseline' + '_' + geotype]

    if network_strategy == 'srn' and geotype == 'rural':
        sharing = 'cns'

    shared_assets = INFRA_SHARING_ASSETS[sharing]

    assets = {
        'single_sector_antenna': costs['single_sector_antenna'],
        'single_remote_radio_unit': costs['single_remote_radio_unit'],
        'io_fronthaul': costs['io_fronthaul'],
        'processing': costs['processing'],
        'io_s1_x2': costs['io_s1_x2'],
        'control_unit': costs['control_unit'],
        'cooling_fans': costs['cooling_fans'],
        'distributed_power_supply_converter': costs['distributed_power_supply_converter'],
        'bbu_cabinet': costs['bbu_cabinet'],
        'installation': costs['installation'],
        'site_rental': costs['site_rental_{}'.format(geotype)],
        'router': costs['router'],
        'backhaul': get_backhaul_costs(region, backhaul, costs, core_lut),
        'core_edge': core_costs(region, 'core_edge', costs, core_lut, strategy, country_parameters),
        'core_node': core_costs(region, 'core_node', costs, core_lut, strategy, country_parameters),
        'regional_edge': regional_net_costs(region, 'regional_edge', costs, core_lut, strategy, country_parameters),
        'regional_node': regional_net_costs(region, 'regional_node', costs, core_lut, strategy, country_parameters),
        'per_site_spectrum_acquisition_cost': costs['per_site_spectrum_acquisition_cost'],
        'per_site_administration_cost': costs['per_site_administration_cost'],
    }

    cost_structure = {}

    for key, value in assets.items():
        if not key in shared_assets:
            cost_structure[key] = value
        else:
            if network_strategy == 'srn' and geotype == 'rural':
                value = value * (1 / networks)
                cost_structure[key] = value
            else:
                value = value / networks
                cost_structure[key] = value

    return cost_structure


def upgrade_to_4g(region, strategy, costs, global_parameters,
    core_lut, country_parameters):
    """
    Reflects the baseline scenario of needing to build a single dedicated
    network.

    """
    backhaul = '{}_backhaul'.format(strategy.split('_')[2])
    sharing = strategy.split('_')[3]
    geotype = region['geotype'].split(' ')[0]

    # generation_core_backhaul_sharing_networks_spectrum_tax
    network_strategy = strategy.split('_')[4]
    networks = country_parameters['networks']['baseline' + '_' + geotype]

    if network_strategy == 'srn' and geotype == 'rural':
        sharing = 'cns'

    shared_assets = INFRA_SHARING_ASSETS[sharing]

    assets = {
        'single_sector_antenna': costs['single_sector_antenna'],
        'single_remote_radio_unit': costs['single_remote_radio_unit'],
        'io_fronthaul': costs['io_fronthaul'],
        'processing': costs['processing'],
        'io_s1_x2': costs['io_s1_x2'],
        'control_unit': costs['control_unit'],
        'cooling_fans': costs['cooling_fans'],
        'distributed_power_supply_converter': costs['distributed_power_supply_converter'],
        'bbu_cabinet': costs['bbu_cabinet'],
        'installation': costs['installation'],
        'site_rental': costs['site_rental_{}'.format(geotype)],
        'router': costs['router'],
        'backhaul': get_backhaul_costs(region, backhaul, costs, core_lut),
        'core_edge': core_costs(region, 'core_edge', costs, core_lut, strategy, country_parameters),
        'core_node': core_costs(region, 'core_node', costs, core_lut, strategy, country_parameters),
        'regional_edge': regional_net_costs(region, 'regional_edge', costs, core_lut, strategy, country_parameters),
        'regional_node': regional_net_costs(region, 'regional_node', costs, core_lut, strategy, country_parameters),
        'per_site_spectrum_acquisition_cost': costs['per_site_spectrum_acquisition_cost'],
        'per_site_administration_cost': costs['per_site_administration_cost'],
    }

    cost_structure = {}

    for key, value in assets.items():
        if not key in shared_assets:
            cost_structure[key] = value
        else:
            if network_strategy == 'srn' and geotype == 'rural':
                value = value * (1 / networks)
                cost_structure[key] = value
            else:
                value = value / networks
                cost_structure[key] = value

    return cost_structure


def greenfield_3g(region, strategy, costs, global_parameters,
    core_lut, country_parameters):
    """
    Build a greenfield 3G asset.

    """
    backhaul = '{}_backhaul'.format(strategy.split('_')[2])
    sharing = strategy.split('_')[3]
    geotype = region['geotype'].split(' ')[0]

    # generation_core_backhaul_sharing_networks_spectrum_tax
    network_strategy = strategy.split('_')[4]
    networks = country_parameters['networks']['baseline' + '_' + geotype]

    if network_strategy == 'srn' and geotype == 'rural':
        sharing = 'cns'

    shared_assets = INFRA_SHARING_ASSETS[sharing]

    assets = {
        'single_sector_antenna': costs['single_sector_antenna'],
        'single_remote_radio_unit': costs['single_remote_radio_unit'],
        'io_fronthaul': costs['io_fronthaul'],
        'processing': costs['processing'],
        'io_s1_x2': costs['io_s1_x2'],
        'control_unit': costs['control_unit'],
        'cooling_fans': costs['cooling_fans'],
        'distributed_power_supply_converter': costs['distributed_power_supply_converter'],
        'power_generator_battery_system': costs['power_generator_battery_system'],
        'bbu_cabinet': costs['bbu_cabinet'],
        'tower': costs['tower'],
        'civil_materials': costs['civil_materials'],
        'transportation': costs['transportation'],
        'installation': costs['installation'],
        'site_rental': costs['site_rental_{}'.format(geotype)],
        'router': costs['router'],
        'backhaul': get_backhaul_costs(region, backhaul, costs, core_lut),
        'core_edge': core_costs(region, 'core_edge', costs, core_lut, strategy, country_parameters),
        'core_node': core_costs(region, 'core_node', costs, core_lut, strategy, country_parameters),
        'regional_edge': regional_net_costs(region, 'regional_edge', costs, core_lut, strategy, country_parameters),
        'regional_node': regional_net_costs(region, 'regional_node', costs, core_lut, strategy, country_parameters),
        'per_site_spectrum_acquisition_cost': costs['per_site_spectrum_acquisition_cost'],
        'per_site_administration_cost': costs['per_site_administration_cost'],
    }

    cost_structure = {}

    for key, value in assets.items():
        if not key in shared_assets:
            cost_structure[key] = value
        else:
            if network_strategy == 'srn' and geotype == 'rural':
                value = value * (1 / networks)
                cost_structure[key] = value
            else:
                value = value / networks
                cost_structure[key] = value

    return cost_structure


def greenfield_4g(region, strategy, costs, global_parameters,
    core_lut, country_parameters):
    """
    Build a greenfield 4G asset.

    """
    backhaul = '{}_backhaul'.format(strategy.split('_')[2])
    sharing = strategy.split('_')[3]
    geotype = region['geotype'].split(' ')[0]

    # generation_core_backhaul_sharing_networks_spectrum_tax
    network_strategy = strategy.split('_')[4]
    networks = country_parameters['networks']['baseline' + '_' + geotype]

    if network_strategy == 'srn' and geotype == 'rural':
        sharing = 'cns'

    shared_assets = INFRA_SHARING_ASSETS[sharing]

    assets = {
        'single_sector_antenna': costs['single_sector_antenna'],
        'single_remote_radio_unit': costs['single_remote_radio_unit'],
        'io_fronthaul': costs['io_fronthaul'],
        'processing': costs['processing'],
        'io_s1_x2': costs['io_s1_x2'],
        'control_unit': costs['control_unit'],
        'cooling_fans': costs['cooling_fans'],
        'distributed_power_supply_converter': costs['distributed_power_supply_converter'],
        'power_generator_battery_system': costs['power_generator_battery_system'],
        'bbu_cabinet': costs['bbu_cabinet'],
        'tower': costs['tower'],
        'civil_materials': costs['civil_materials'],
        'transportation': costs['transportation'],
        'installation': costs['installation'],
        'site_rental': costs['site_rental_{}'.format(geotype)],
        'router': costs['router'],
        'backhaul': get_backhaul_costs(region, backhaul, costs, core_lut),
        'core_edge': core_costs(region, 'core_edge', costs, core_lut, strategy, country_parameters),
        'core_node': core_costs(region, 'core_node', costs, core_lut, strategy, country_parameters),
        'regional_edge': regional_net_costs(region, 'regional_edge', costs, core_lut, strategy, country_parameters),
        'regional_node': regional_net_costs(region, 'regional_node', costs, core_lut, strategy, country_parameters),
        'per_site_spectrum_acquisition_cost': costs['per_site_spectrum_acquisition_cost'],
        'per_site_administration_cost': costs['per_site_administration_cost'],
    }

    cost_structure = {}

    for key, value in assets.items():
        if not key in shared_assets:
            cost_structure[key] = value
        else:
            if network_strategy == 'srn' and geotype == 'rural':
                value = value * (1 / networks)
                cost_structure[key] = value
            else:
                value = value / networks
                cost_structure[key] = value

    return cost_structure


def get_fronthaul_costs(region, costs):
    """
    Calculate fronthaul costs.
    """
    average_cell_spacing_km = math.sqrt(1/region['site_density'])
    average_cell_spacing_m = average_cell_spacing_km * 1000 #convert km to m

    tech = 'fiber_{}_m'.format(region['geotype'].split(' ')[0])
    cost_per_meter = costs[tech]
    cost = cost_per_meter * average_cell_spacing_m

    return cost


def get_backhaul_costs(region, backhaul, costs, core_lut):
    """
    Calculate backhaul costs.
    # backhaul_fiber backhaul_copper backhaul_microwave	backhaul_satellite
    """
    backhaul_tech = backhaul.split('_')[0]
    geotype = region['geotype'].split(' ')[0]

    nodes = 0
    for asset_type in ['core_node', 'regional_node']:
        for age in ['new', 'existing']:
            combined_key = '{}_{}'.format(region['GID_id'], age)
            nodes += core_lut[asset_type][combined_key]

    node_density_km2 = nodes / region['area_km2']
    if node_density_km2 > 0:
        ave_distance_to_a_node_m = (math.sqrt(1/node_density_km2) / 2) * 1000
    else:
        ave_distance_to_a_node_m = math.sqrt(region['area_km2']) * 1000

    if backhaul_tech == 'microwave':
        if ave_distance_to_a_node_m < 15000:
            tech = '{}_{}'.format(backhaul_tech, 'small')
            cost = costs[tech]
        elif 15000 < ave_distance_to_a_node_m < 30000:
            tech = '{}_{}'.format(backhaul_tech, 'medium')
            cost = costs[tech]
        else:
            tech = '{}_{}'.format(backhaul_tech, 'large')
            cost = costs[tech] * (ave_distance_to_a_node_m / 30000)


    elif backhaul_tech == 'fiber':
        tech = '{}_{}_m'.format(backhaul_tech, geotype)
        cost_per_meter = costs[tech]
        cost = cost_per_meter * ave_distance_to_a_node_m

    else:
        print('Did not recognise the backhaul technology {}'.format(backhaul_tech))
        cost = 0

    return cost


def regional_net_costs(region, asset_type, costs, core_lut, strategy, country_parameters):
    """
    Return regional asset costs for only the 'new' assets that have been planned.
    """
    core = strategy.split('_')[1]
    geotype = region['geotype'].split(' ')[0]

    networks = country_parameters['networks']['baseline' + '_' + geotype]

    if asset_type in core_lut.keys():

        combined_key = '{}_{}'.format(region['GID_id'], 'new')

        if combined_key in core_lut[asset_type]:

            if asset_type == 'regional_edge':

                distance_m = core_lut[asset_type][combined_key]
                cost_m = costs['regional_edge']
                cost = int(distance_m * cost_m)

                sites = ((region['upgraded_sites'] + region['new_sites']) / networks)

                if sites == 0:
                    return 0
                elif sites <= 1:
                    return cost * sites
                else:
                    return cost / sites

            elif asset_type == 'regional_node':

                regional_nodes = core_lut[asset_type][combined_key]

                cost_each = costs['regional_node_{}'.format(core)]

                regional_node_cost = int(regional_nodes * cost_each)

                sites = ((region['upgraded_sites'] + region['new_sites']) / networks)

                if sites == 0:
                    return 0
                elif sites <= 1:
                    return regional_node_cost
                else:
                    return regional_node_cost / sites


                return (regional_node_cost / sites)

            else:
                return 'Did not recognise core asset type'
        else:
            return 0

    return 'Asset name not in lut'


def core_costs(region, asset_type, costs, core_lut, strategy, country_parameters):
    """
    Return core asset costs for only the 'new' assets that have been planned.
    """
    core = strategy.split('_')[1]
    geotype = region['geotype'].split(' ')[0]
    networks = country_parameters['networks']['baseline' + '_' + geotype]

    if asset_type == 'core_edge':

        if asset_type in core_lut.keys():

            total_cost = []

            #only grab the new edges that need to be built
            combined_key = '{}_{}'.format(region['GID_id'], 'new')

            if combined_key in core_lut[asset_type].keys():
                distance_m = core_lut[asset_type][combined_key]

                cost = int(distance_m * costs['core_edge'])
                total_cost.append(cost)

                sites = ((region['upgraded_sites'] + region['new_sites']) / networks)

                if sites == 0:
                    return 0
                elif sites < 1:
                    return sum(total_cost)
                else:
                    return sum(total_cost) / sites
        else:
            return 0

    elif asset_type == 'core_node':

        if asset_type in core_lut.keys():

            total_cost = []

            #only grab the new nodes that need to be built
            combined_key = '{}_{}'.format(region['GID_id'], 'new')

            nodes = core_lut[asset_type][combined_key]

            cost = int(nodes * costs['core_node_{}'.format(core)])
            total_cost.append(cost)

            sites = ((region['upgraded_sites'] + region['new_sites']) / networks)

            if sites == 0:
                return 0
            elif sites < 1:
                return sum(total_cost)
            else:
                return sum(total_cost) / sites

        else:
            return 0

    else:
        print('Did not recognise core asset type {}'.format(asset_type))

    return 0


def discount_capex_and_opex(capex, global_parameters, country_parameters):
    """
    Discount costs based on return period.
    Parameters
    ----------
    cost : float
        Financial cost.
    global_parameters : dict
        All global model parameters.
    Returns
    -------
    discounted_cost : float
        The discounted cost over the desired time period.
    """
    return_period = global_parameters['return_period']
    discount_rate = global_parameters['discount_rate'] / 100
    wacc = country_parameters['financials']['wacc']

    costs_over_time_period = []

    costs_over_time_period.append(capex)

    opex = round(capex * (global_parameters['opex_percentage_of_capex'] / 100))

    for i in range(0, return_period):
        costs_over_time_period.append(
            opex / (1 + discount_rate)**i
        )

    discounted_cost = round(sum(costs_over_time_period))

    #add wacc
    discounted_cost = discounted_cost * (1 + (wacc/100))

    return discounted_cost


def discount_opex(opex, global_parameters, country_parameters):
    """
    Discount opex based on return period.
    """
    return_period = global_parameters['return_period']
    discount_rate = global_parameters['discount_rate'] / 100
    wacc = country_parameters['financials']['wacc']

    costs_over_time_period = []

    for i in range(0, return_period):
        costs_over_time_period.append(
            opex / (1 + discount_rate)**i
        )

    discounted_cost = round(sum(costs_over_time_period))

    #add wacc
    discounted_cost = discounted_cost * (1 + (wacc/100))

    return discounted_cost


def calc_costs(region, strategy, cost_structure, backhaul_quantity,
    global_parameters, country_parameters):
    """

    """
    # generation = strategy.split('_')[0]
    core = strategy.split('_')[1]
    backhaul = strategy.split('_')[2]
    regional_integration = region['integration']

    all_sites = region['upgraded_sites'] + region['new_sites']

    total_cost = 0
    cost_by_asset = []

    for asset_name1, cost in cost_structure.items():
        for asset_name2, type_of_cost in COST_TYPE.items():
            if asset_name1 == asset_name2:

                if asset_name1 == 'backhaul' and backhaul_quantity == 0:
                    continue

                if asset_name1 == 'regional_node' and backhaul == 'microwave':
                    continue

                if asset_name1 == 'regional_edge' and backhaul == 'microwave':
                    continue

                if type_of_cost == 'capex_and_opex':

                    cost = discount_capex_and_opex(cost, global_parameters, country_parameters)

                    if regional_integration == 'integration':
                        cost = (cost * (1 -
                            (global_parameters['regional_integration_factor'] /  100)))

                    if asset_name1 == 'single_sector_antenna':
                        cost = cost * global_parameters['sectorization']

                    if asset_name1 in [
                        'core_edge',
                        'core_node',
                        'regional_edge',
                        'regional_node',
                        ]:
                        cost = cost / all_sites

                elif type_of_cost == 'capex':

                    cost = cost

                    if regional_integration == 'integration' and asset_name1 == 'per_site_spectrum_acquisition_cost':
                        cost = cost / 2
                    elif regional_integration == 'integration':
                        cost = (cost * (1 -
                            (global_parameters['regional_integration_factor'] /  100)))

                elif type_of_cost == 'opex':

                    cost = discount_opex(cost, global_parameters, country_parameters)

                    if regional_integration == 'integration' and asset_name1 == 'per_site_administration_cost':
                        cost = cost / 2
                    elif regional_integration == 'integration':
                        cost = (cost * (1 -
                            (global_parameters['regional_integration_factor'] /  100)))

                else:
                    return 'Did not recognize cost type'

                total_cost += cost

                cost_by_asset.append({
                    'asset': asset_name1,
                    'cost': cost,
                })

    cost_by_asset = {item['asset']: item['cost'] for item in cost_by_asset}

    ran = [
        'single_sector_antenna',
        'single_remote_radio_unit',
        'io_fronthaul',
        'processing',
        'io_s1_x2',
        'control_unit',
        'cooling_fans',
        'distributed_power_supply_converter',
        'bbu_cabinet',
        'cots_processing',
        'io_n2_n3',
        'low_latency_switch',
        'rack',
        'cloud_power_supply_converter',
        'software'
    ]

    backhaul_fronthaul = [
        'fronthaul',
        'backhaul',
    ]

    civils = [
        'tower',
        'civil_materials',
        'transportation',
        'installation',
        'site_rental',
        'power_generator_battery_system',
    ]

    core = [
        'cloud_backhaul',
        'regional_node',
        'regional_edge',
        'core_node',
        'core_edge',
    ]

    admin_and_ops = [
        'per_site_spectrum_acquisition_cost',
        'per_site_administration_cost',
    ]

    ran_cost = 0
    backhaul_fronthaul_cost = 0
    civils_cost = 0
    core_cost = 0
    admin_and_ops_cost = 0

    for key, value in cost_by_asset.items():
        if key in ran:
            ran_cost += value
        if key in backhaul_fronthaul:
            backhaul_fronthaul_cost += value
        if key in civils:
            civils_cost += value
        if key in core:
            core_cost += value
        if key in admin_and_ops:
            admin_and_ops_cost += value

    cost_by_asset = {
        'ran': ran_cost,
        'backhaul_fronthaul': backhaul_fronthaul_cost,
        'civils': civils_cost,
        'core_network': core_cost,
        'admin_and_ops': admin_and_ops_cost,
    }

    return total_cost, cost_by_asset


INFRA_SHARING_ASSETS = {
    'baseline': [],
    'pss': [
        'tower',
        'civil_materials',
        'transportation',
        'installation',
        'site_rental',
        'power_generator_battery_system',
    ],
    'psb': [
        'tower',
        'civil_materials',
        'transportation',
        'installation',
        'site_rental',
        'power_generator_battery_system',
        'backhaul',
        'cloud_backhaul',
    ],
    'moran': [
        'single_sector_antenna',
        'single_remote_radio_unit',
        'io_fronthaul',
        'processing',
        'io_s1_x2',
        'control_unit',
        'cooling_fans',
        'distributed_power_supply_converter',
        'bbu_cabinet',
        'fronthaul',
        'cots_processing',
        'io_n2_n3',
        'low_latency_switch',
        'rack',
        'cloud_power_supply_converter',
        'software',
        'tower',
        'civil_materials',
        'transportation',
        'installation',
        'site_rental',
        'power_generator_battery_system',
        'backhaul',
        'cloud_backhaul',
    ],
    'cns': [
        'single_sector_antenna',
        'single_remote_radio_unit',
        'io_fronthaul',
        'processing',
        'io_s1_x2',
        'control_unit',
        'cooling_fans',
        'distributed_power_supply_converter',
        'bbu_cabinet',
        'fronthaul',
        'cots_processing',
        'io_n2_n3',
        'low_latency_switch',
        'rack',
        'cloud_power_supply_converter',
        'tower',
        'civil_materials',
        'transportation',
        'installation',
        'site_rental',
        'power_generator_battery_system',
        'backhaul',
        'cloud_backhaul',
        'local_node',
        'regional_edge',
        'regional_node',
        'core_edge',
        'core_node',
    ],
}

COST_TYPE = {
    'single_sector_antenna': 'capex_and_opex',
    'single_remote_radio_unit': 'capex_and_opex',
    'single_baseband_unit': 'capex_and_opex',
    'io_fronthaul': 'capex_and_opex',
    'processing': 'capex_and_opex',
    'io_s1_x2': 'capex_and_opex',
    'control_unit': 'capex_and_opex',
    'cooling_fans': 'capex_and_opex',
    'distributed_power_supply_converter': 'capex_and_opex',
    'bbu_cabinet': 'capex',
    'fronthaul': 'capex_and_opex',
    'cots_processing': 'capex_and_opex',
    'io_n2_n3': 'capex_and_opex',
    'low_latency_switch': 'capex_and_opex',
    'rack': 'capex',
    'cloud_power_supply_converter': 'capex_and_opex',
    'software': 'opex',
    'tower': 'capex',
    'civil_materials': 'capex',
    'transportation': 'capex',
    'installation': 'capex',
    'site_rental': 'opex',
    'power_generator_battery_system': 'capex_and_opex',
    'backhaul': 'capex_and_opex',
    'cloud_backhaul': 'capex_and_opex',
    'regional_node': 'capex_and_opex',
    'regional_edge': 'capex_and_opex',
    'core_node': 'capex_and_opex',
    'core_edge': 'capex_and_opex',
    'per_site_spectrum_acquisition_cost': 'capex',
    'per_site_administration_cost': 'opex',
}
