from pytest import fixture


@fixture(scope='function')
def setup_region():
    return [{
    'GID_0': 'MWI',
    'GID_id': 'MWI.1.1.1_1',
    'mean_luminosity_km2': 26.736407691655717,
    'population': 10000,
    'area_km2': 2,
    'population_km2': 5000,
    'decile': 100,
    'geotype': 'urban',
    'demand_mbps_km2': 5000,
    'integration': 'baseline'
    }]


@fixture(scope='function')
def setup_region_rural():
    return [{
    'GID_0': 'MWI',
    'GID_id': 'MWI.1.1.1_1',
    'mean_luminosity_km2': 26.736407691655717,
    'population': 10000,
    'area_km2': 2,
    'population_km2': 5000,
    'decile': 100,
    'geotype': 'rural'
    }]


@fixture(scope='function')
def setup_option():
    return { #generation_core_backhaul_sharing_networks_spectrum_tax_integration
        'scenario': 'S1_50_50_50',
        'strategy': '4G_epc_microwave_baseline_baseline_baseline_baseline_baseline_baseline'
    }


@fixture(scope='function')
def setup_option_high():
    return {
        'scenario': 'S1_50_50_50',
        'strategy': '4G_epc_microwave_baseline_baseline_high_high_high'
    }


@fixture(scope='function')
def setup_global_parameters():
    return {
        'overbooking_factor': 100,
        'return_period': 2,
        'discount_rate': 5,
        'opex_percentage_of_capex': 10,
        'sectorization': 3,
        'confidence': [1, 10, 50],
        'cots_processing_split_urban': 2,
        'cots_processing_split_suburban': 4,
        'cots_processing_split_rural': 16,
        'io_n2_n3_split': 7,
        'low_latency_switch_split': 7,
        'rack_split': 7,
        'cloud_power_supply_converter_split': 7,
        'software_split': 7,
        'cloud_backhaul_split': 7,
        'regional_integration_factor': 10
    }


@fixture(scope='function')
def setup_country_parameters():
    return {
        'luminosity': {
            'high': 5,
            'medium': 1,
        },
        'arpu': {
            'high': 15,
            'medium': 5,
            'low': 2,
        },
        'networks': {
            'baseline_urban': 2,
            'baseline_suburban': 2,
            'baseline_rural': 2,
            # 'srn_urban': 2,
            # 'srn_suburban': 2,
            # 'srn_rural': 1,
        },
        'frequencies': {
            '4G': [
                {
                    'frequency': 800,
                    'bandwidth': '2x10',
                },
                {
                    'frequency': 1800,
                    'bandwidth': '2x10',
                },
            ],
            '5G': [
                {
                    'frequency': 700,
                    'bandwidth': '2x10',
                },
                {
                    'frequency': 3500,
                    'bandwidth': '1x50',
                },
            ]
        },
        'financials': {
            'wacc': 15,
            'profit_margin': 20,
            'spectrum_coverage_baseline_usd_mhz_pop': 1,
            'spectrum_capacity_baseline_usd_mhz_pop': 1,
            'spectrum_cost_low': 50,
            'spectrum_cost_high': 50,
            'tax_low': 10,
            'tax_baseline': 25,
            'tax_high': 40,
            'acquisition_per_subscriber': 10,
            },
        }


@fixture(scope='function')
def setup_timesteps():
    return [
        2020,
        # 2021,
        # 2022,
        # 2023,
        # 2024,
        # 2025,
        # 2026,
        # 2027,
        # 2028,
        # 2029,
        # 2030
    ]


@fixture(scope='function')
def setup_penetration_lut():
    return {
        2020: 50,
        # 2021: 75,
    }


@fixture(scope='function')
def setup_costs():
    return {
        #all costs in $USD
        'single_sector_antenna': 1500,
        'single_remote_radio_unit': 4000,
        'io_fronthaul': 1500,
        'processing': 1500,
        'io_s1_x2': 1500,
        'control_unit': 1500,
        'cooling_fans': 250,
        'distributed_power_supply_converter': 250,
        'power_generator_battery_system': 5000,
        'bbu_cabinet': 500,
        'fiber_fronthaul_urban_m': 10,
        'fiber_fronthaul_suburban_m': 5,
        'fiber_fronthaul_rural_m': 2,
        'cots_processing': 500,
        'io_n2_n3': 1500,
        'low_latency_switch': 500,
        'rack': 500,
        'cloud_power_supply_converter': 1000,
        'software': 50,
        'tower': 10000,
        'civil_materials': 5000,
        'transportation': 5000,
        'installation': 5000,
        'site_rental_urban': 9600,
        'site_rental_suburban': 4000,
        'site_rental_rural': 2000,
        'router': 2000,
        'microwave_small': 10000,
        'microwave_medium': 20000,
        'microwave_large': 40000,
        'fiber_urban_m': 10,
        'fiber_suburban_m': 5,
        'fiber_rural_m': 2,
        'core_node_epc': 100000,
        'core_node_nsa': 150000,
        'core_node_sa': 200000,
        'core_edge': 20,
        'regional_node_epc': 100000,
        'regional_node_nsa': 150000,
        'regional_node_sa': 200000,
        'regional_edge': 10,
        'regional_node_lower_epc': 10000,
        'regional_node_lower_nsa': 10000,
        'regional_node_lower_sa': 10000,
        'per_site_spectrum_acquisition_cost': 1000,
        'per_site_administration_cost': 100,
    }


@fixture(scope='function')
def setup_lookup():
    return {
        ('urban', 'macro', '800', '4G', '50'): [
            (0.01, 1),
            (0.02, 2),
            (0.05, 5),
            (0.15, 15),
            (2, 100)
        ],
        ('urban', 'macro', '1800', '4G', '50'): [
            (0.01, 5),
            (0.02, 10),
            (0.05, 20),
            (0.15, 40),
            (2, 1000)
        ],
    }


@fixture(scope='function')
def setup_ci():
    return 50

@fixture(scope='function')
def setup_core_lut():
    return {
        'core_edge': {
            'MWI.1.1.1_1_new': 1000,
            'MWI.1.1.1_1_existing': 1000
        },
        'core_node': {
            'MWI.1.1.1_1_new': 2,
            'MWI.1.1.1_1_existing': 2
        },
        'regional_edge': {
            'MWI.1.1.1_1_new': 1000,
            'MWI.1.1.1_1_existing': 1000
        },
        'regional_node': {
            'MWI.1.1.1_1_new': 2,
            'MWI.1.1.1_1_existing': 2
        },
    }

@fixture(scope='function')
def setup_empty_core_lut():
    return {
        'core_edge': {
            'MWI.1.1.1_1_new': 0,
            'MWI.1.1.1_1_existing': 0
        },
        'core_node': {
            'MWI.1.1.1_1_new': 0,
            'MWI.1.1.1_1_existing': 0
        },
        'regional_edge': {
            'MWI.1.1.1_1_new': 0,
            'MWI.1.1.1_1_existing': 0
        },
        'regional_node': {
            'MWI.1.1.1_1_new': 0,
            'MWI.1.1.1_1_existing': 0
        },
    }
