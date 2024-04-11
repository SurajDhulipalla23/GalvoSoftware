import nidaqmx
from nidaqmx.constants import AcquisitionType
import numpy as np
import matplotlib.pyplot as plt

# Shared parameters
num_lines = 400
num_points_per_line = 400
flyback_points = 20
scan_rate = 1000  # Hz for scanning
image_acquisition_rate = 1000  # Hz for image acquisition
volt_range = (-8.23, 8.23)  # Voltage range

# Calculate the voltage step for scanning
voltage_step = (volt_range[1] - volt_range[0]) / (num_points_per_line - 1)

# Generate scanning voltage patterns
x_voltages = np.linspace(volt_range[0], volt_range[1], num_points_per_line)
y_voltages = np.linspace(volt_range[0], volt_range[1], num_lines)

# Initialize image data array
image_data = np.zeros((num_lines, num_points_per_line))

try:
    with nidaqmx.Task() as scan_task, nidaqmx.Task() as detect_task:
        # Setup scanning output channels
        scan_task.ao_channels.add_ao_voltage_chan("DaqDevice/ao0,DaqDevice/ao1",
                                                  min_val=volt_range[0], max_val=volt_range[1])
        
        # Setup detector input channel
        detect_task.ai_channels.add_ai_voltage_chan("DaqDevice/ai0")

        # Set the timing for both tasks to ensure synchronization
        scan_task.timing.cfg_samp_clk_timing(rate=scan_rate,
                                             sample_mode=AcquisitionType.CONTINUOUS)
        detect_task.timing.cfg_samp_clk_timing(rate=image_acquisition_rate,
                                               sample_mode=AcquisitionType.CONTINUOUS,
                                               samps_per_chan=num_points_per_line)

        # Synchronized scanning and detection
        for y_idx, y in enumerate(y_voltages):
            # Write voltages for one line
            scan_task.write([x_voltages, np.full_like(x_voltages, y)], auto_start=True)
            
            # Read one line of image data
            data = detect_task.read(number_of_samples_per_channel=num_points_per_line)
            image_data[y_idx, :] = data
            
            # Handle flyback between lines
            if y_idx < len(y_voltages) - 1:
                next_y = y_voltages[y_idx + 1]
                flyback_x_voltages = np.linspace(x_voltages[-1], x_voltages[0], flyback_points)
                flyback_y_voltages = np.linspace(y, next_y, flyback_points)
                for flyback_x, flyback_y in zip(flyback_x_voltages, flyback_y_voltages):
                    scan_task.write([flyback_x, flyback_y], auto_start=True)

except nidaqmx.DaqError as e:
    print(e)

# Display the synchronized image
plt.imshow(image_data, cmap='gray')
plt.colorbar()
plt.show()
