#Assignment Details
"""
ENGG1001 Assignment 1
Semester 1, 2023
"""
#Author Details
__author__ = "Blaise Delforce"
__email__ = "b.delforce@uqconnect.edu.au"


#Setup and Constants
from math import sqrt

GRAVITY = 9.81
WATER_DENSITY       = 1000       # [kg/m^3]
RESERVOIR_FOOTPRINT = 200 * 200  # [m^2]
OUTLET_AREA         = 1          # [m^2]


#Task 1 - Determine quantity water pumped given parameters
def determine_water_pumped(gen_power, height_difference, pumping_time, efficiency):
    """
    Function to determine the amount of water pumped for a given pumped hydro scenario.

    Parameters:
        gen_power (float): generator power used to pump water [kW]
        height_difference (float): difference in the elevation levels of the upper and lower reservoirs [m]
        pumping_time (float): the number of daytime hours that water is pumped [hours]
        efficiency (float): the percentage efficiency of conversion from electrical to potential energy. [%]
    
    Returns:
        mass (float): total mass of water pumped upwards [kg]
    """
    
    mass = ((((float(gen_power))*1000)*((float(efficiency))/100))*(float(pumping_time)*60*60))/(GRAVITY*(float(height_difference)))
    return mass
    
#Task 2 - Determine the cost to pump up to the dam given input variables
def calc_cost_to_pump(gen_power, pumping_time, day_tariff):
    """
    Function to to determine the cost to pump water up to the dam
            
    Parameters:
        gen_power (float): generator power used to pump water [kW]
        pumping_time (float): the number of daytime hours that water is pumped [hours]
        day_tariff (float): day-time energy cost per kWh [$/kWh]
    Returns:
        daily_cost_to_pump(float): daily cost to pump water upwards [$]

    """
    daily_cost_to_pump = float(gen_power)*float(pumping_time)*float(day_tariff)
    return daily_cost_to_pump

#Task 3 - Determine the amount of water that flows out during each given time period (in a tuple)
def water_mass_drained(water_mass, time_increment):
    """
    Function to determine the amount of water drained from the reservoir over a specified time increment,
    given the amount of water currently in the reservoir and the time increment

    Parameters:
        water_mass (float): mass of water in the reservoir currently [kg]
        time_increment (float): discrete time increment used during the computer simulation [sec]
        
    Returns:
        water_out (float): The quantity of water drained during the discrete time interval [kg]
    
    """

    water_height = water_mass / WATER_DENSITY / RESERVOIR_FOOTPRINT
    energy_diff  = water_height * GRAVITY   # [J/kg]
    water_speed  = sqrt(energy_diff * 2)    # [m/s]
    water_flow   = WATER_DENSITY * water_speed * OUTLET_AREA  # [kg/s]
    water_out    = water_flow * time_increment # [kg]
    return water_out

def water_flow_out(water_pumped_daily, water_base_mass, time_interval):
    """
    Function to create a tuple to return to the user, that will (given a range of intervals),
    return the quantity of water returned in each interval across that entire range
    
    Parameters:
        water_pumped_daily (float): water transferred to upper reservoir during the day [kg]
        water_base_mass (float): the mass of water in the reservoir at the start of every day (i.e. before upward pumping commences) [kg]
        time_interval (float): discrete time increment used during the computer simulation [sec]

    Returns:
        tuple_water_outflow [tuple]: tuple of the outflows of water out in each time interval as water is released under gravity [kg]
    
    """
    water_mass = water_base_mass + water_pumped_daily 
    tuple_water_outflow = []
    
    #Loop that simulates water outflow from the damn, and adds each discrete value to a tuple, until the water level reaches the start-of-day mass
    while  water_mass > water_base_mass: 
        water_outflow = (water_mass_drained(water_mass, time_interval))  
        tuple_water_outflow.append(water_outflow)
        water_mass -= water_outflow
    return tuple(tuple_water_outflow)
        

#Task 4
    
def determine_power_formed(water_flow_out, time_interval, efficiency, height_difference):
    """
    Takes the parameters plus the water_flow tuple from the water_out_flow,
    and creates another tuple with the power generated in each time period, plus the average nightly power.

    Parameters:
        tuple_water_outflow (tuple): tuple of water outflows returned from the tuple_water_outflow
        time_interval (float): discrete time increment used during the computer simulation [sec]
        efficiency (float): the quantity of energy converted into useful output [5]
        height_difference (float): the difference in height between the two reservoirs [m]

    Returns:
        elec_power_tuple (tuple): Tuple whose elements correspond to power generated at each time period [J]
        average_nightly_power: The average power across all increments of the night [J]
        
        
    """

    elec_power_tuple = []
    p = 0
    sumof = 0
    power_increment = 0
    
    #Loop that calculates the power generated in each discrete time increment and places it in a tuple
    while len(elec_power_tuple) < len(water_flow_out): 
        power_increment = ((water_flow_out[p])*(GRAVITY)*(height_difference)*((efficiency/100)))/(time_interval*1000) 
        elec_power_tuple.append(power_increment) 
        p += 1 
    counter = list(elec_power_tuple)
    
    #loop that adds up the total amount of power generated from the list
    for i in counter:
        sumof += i
    average_nightly_power = float(sumof/len(elec_power_tuple))
    return elec_power_tuple, average_nightly_power
    
#Task 5 - determine the revenue generated over a night of running
def revenue_generated(elec_power_tuple, time_increment, night_tariff):
    """
    Function to determine the daily revenue obtained by the generation
    of night-time electricity
    
    Parameters:
        elec_power_tuple (tuple): tuple of the electrical power generated in each time_interval [kWh]
        time_increment (float): length of each time increment [sec]
        night_tariff (float): amount of $ paid per kWh of power generated during the night [kWh]
    
    Returns:
        daily_revenue (float): Daily revenue from night-time electricity generation [$]
    """
    total_power = 0
    elec_power_list = list(elec_power_tuple)
    
    #loop that adds up the total amount of power generated 
    for i in elec_power_list: 
        total_power += i
    daily_revenue = ((total_power)*(time_increment/3600)*(night_tariff)) 
    return daily_revenue

#Task 6 - determine daily profit
def determine_profit(height_difference, pumping_time, gen_power, \
day_tariff, night_tariff, efficiency, water_base_mass, time_increment):
    """
    Function to determine profit by pumping upwards and then releasing at night.
    Parameters:
        height_difference (float): the height difference between the upper and lower reservoirs [m]
        pumping_time (float): the number of daytime hours that water is pumped [hours]
        gen_power (float): generator power used to pump water [kW]
        day_tariff (float): day-time energy cost per kWh [$/kWh]
        night_tariff (float): night-time energy cost per kWh [$/kWh]
        efficiency (float): efficiency of conversion ofbetween electrical and potential energy and vice versa [%]
        water_base_mass (float): the mass of water in the reservoir at the start of every day (i.e. before upward pumping commences) [kg]
        time_increment (float): discrete time increment used during the computer simulation [sec]

    Returns:
        daily_profit (float): the daily profit created from the night-time running of the generator [$]
        
    """
    daily_cost_to_pump = calc_cost_to_pump(gen_power, pumping_time, day_tariff)
    water_pumped_daily = determine_water_pumped(gen_power, height_difference, pumping_time, efficiency)
    water_flow_out_answer = water_flow_out(water_pumped_daily, water_base_mass, time_increment)
    elec_power_tuple, average_nightly_power = determine_power_formed(water_flow_out_answer, time_increment, efficiency, height_difference)
    daily_revenue = revenue_generated(elec_power_tuple, time_increment, night_tariff)
    daily_profit = (daily_revenue) - (daily_cost_to_pump)
    return daily_profit

    
#Task 7 - create a profit table under different conditions
def print_table(attributes):
    """
    Function to print out a table of daily profits under different scenarios.

    Parameters:
        Attributes [tuple]: A tuple of typles containing the inputs required for each different scenario
        
    Returns:
        Table: Contains the scenario number and daily profit

    """
    
    print('###################################################')
    print('#    Scenario number     #    Daily profit ($)    #')
    print('###################################################')
    
    #Unpacks each scenario from the input values, and calculates the profit from each set of variables, before printing the scenario number and profit in a table
    for i, scenario in enumerate(attributes, start=1):
        height_difference, pumping_time, gen_power, day_tariff, night_tariff, efficiency, water_base_mass, time_interval = scenario 
        profit = determine_profit(height_difference, pumping_time, gen_power, day_tariff, night_tariff, efficiency, water_base_mass, time_interval)
        print(f"#           {i}            #{f'{profit:.2f}' : ^24}#")
    print('###################################################')

              

#Task 8 - create a profit table under different conditions with the average power as well
def print_table_extended(attributes):
    """
    Function to print out a table of daily profits and average power produced under different scenarios.

    Parameters:
        Attributes [tuple]: A tuple of typles containing the inputs required for each different scenario
        
    Returns:
        Table: Contains the scenario number, daily profit and the average power produced

    """

    print('############################################################################')
    print('#    Scenario number     #    Daily profit ($)    #     Ave power (kW)     #')
    print('############################################################################')
    
    #Unpacks each scenario from the input values, before calculating the profit generated per set of variables, before printing the scenario number, profit and average power in each row
    for i, scenario in enumerate(attributes, start=1): 
        height_difference, pumping_time, gen_power, day_tariff, night_tariff, efficiency, water_base_mass, time_interval = scenario #unpack the scenario attributes
        profit = determine_profit(height_difference, pumping_time, gen_power, day_tariff, night_tariff, efficiency, water_base_mass, time_interval)
        daily_cost_to_pump = calc_cost_to_pump(gen_power, pumping_time, day_tariff)
        water_pumped_daily = determine_water_pumped(gen_power, height_difference, pumping_time, efficiency) 
        water_flow_out_answer = water_flow_out(water_pumped_daily, water_base_mass, time_interval)
        elec_power_tuple, average_nightly_power = determine_power_formed(water_flow_out_answer, time_interval, efficiency, height_difference) 
        print(f"#           {i}            #{f'{profit:.2f}' : ^24}#{f'{average_nightly_power:.2f}' : ^24}#")
    print('############################################################################')
                                
#Task 9 - Create a User Interaction Function
MAIN_PROMPT = """Please enter a command: """

HELP = """
    The available commands are:
    
    'h' - provide help message
    'r' - read input parameters for various scenarios from a file
    'p c' - print a table with the cost savings for the various pumped
          electricity scenarios
    'p c e' - print a table with the cost savings and the available average
          night power for the various pumped electricity scenarios
    'q' - quit
"""


INVALID = "Please enter a valid command."

SEPARATOR = "#"

def load_data(directory, file_name):
    """ 
    Reads a data file, converts the information into floating point
    numbers, then returns the numbers in tuples.

    Parameters:
        directory (string): name of file where text file is placed
        file_name (string): name of file for input data
    """
    output = ()
    with open(directory + '/' + file_name, 'r') as file:
        for line in file.readlines():
            output += (tuple([float(x) for x in line.strip().split(', ')]),)

    return output

def main():
    """
    Allows User interaction - REFER to HELP for inputs. Allows users the option to input data from a text file, print two types of tables, get help, or quit.

    Parameters:
        None
    Returns:
       Dependent on request
    """

    while True:
        #Main Command 
        user_input = input(MAIN_PROMPT)
            
        #Help Request
        if user_input == 'h':
            print(HELP)
            
        #Load File Request
        elif user_input == 'r':
            directory = input('Please specify the directory: ')
            file_name = input('Please specify the filename: ')
            raw_data = load_data(directory, file_name)
            
        #Profit Print Table Request
        elif user_input == 'p c':
            print_table(raw_data)
            
        #Profit + Average Print Extended Table Request
        elif user_input == 'p c e':
            print_table_extended(raw_data)
            
        #Quit Request
        elif user_input == 'q':
            final_answer = input('Are you sure (y/n): ')
            if final_answer == 'y':
                break
            
        #Invalid Input Check
        else:
            print(INVALID)
