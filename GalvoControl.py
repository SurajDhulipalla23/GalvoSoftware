import nidaqmx
import numpy as np
from nidaqmx.constants import AcquisitionType

# Scan settings
num_points = 400
# 25 mm diameter lens (90%^) -> 22.5 mm
# 32 mm distance to lens
# +/- 20.58291441 degrees
volt_range = (-8.23, 8.23) # Voltage to degree converion (2.5 degrees/V)
scan_rate = 50
flyback_points = 20

# Calculate step sizes in voltage
voltage_step = (volt_range[1] - volt_range[0]) / (num_points - 1)

# Scanning Voltage patterns
x_voltages = np.linspace(volt_range[0], volt_range[1], num_points)
y_voltages = np.linspace(volt_range[0], volt_range[1], num_points)

try:
    with nidaqmx.Task() as task:
        # Analog output channels
        task.ao_channels.add_ao_voltage_chan("DaqDevice/ao0,DaqDevice/ao1",
                                             min_val=volt_range[0], max_val=volt_range[1])
        
        # task.timing.cfg_samp_clk_timing(rate=scan_rate, sample_mode=AcquisitionType.CONTINUOUS)
        
        # Nested loop for scanning pattern
        for y_idx, y in enumerate(y_voltages):
            for x in x_voltages:
                # Write voltage values to the galvanometers
                task.write([x, y], auto_start=True)
            
            # Flyback logic
            if y_idx < len(y_voltages) - 1:
                next_y = y_voltages[y_idx + 1]
                flyback_x_voltages = np.linspace(x_voltages[-1], x_voltages[0], flyback_points)
                flyback_y_voltages = np.linspace(y, next_y, flyback_points)
                for flyback_x, flyback_y in zip(flyback_x_voltages, flyback_y_voltages):
                    task.write([flyback_x, flyback_y], auto_start=True)
            
            # Code for synchronizing the galvo, making sure to include intermediate points during flyback

except nidaqmx.DaqError as e:
    print(e)
    
