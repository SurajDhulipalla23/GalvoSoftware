import nidaqmx
import numpy as np
from nidaqmx.constants import AcquisitionType
import matplotlib.pyplot as plt

# Parameters
scan_rate = 100000  # Hz
num_samples_per_line = 400
num_lines = 400  # Resolution
flyback = 20
total_samples = num_samples_per_line + flyback

# Initialize the data array
image_data = np.zeros((num_lines, num_samples_per_line))

# Setup NI-DAQmx task
with nidaqmx.Task() as task:
    # Analog input channel
    task.ai_channels.add_ai_voltage_chan("DaqDevice/ai0")

    # Timing for acquisition
    task.timing.cfg_samp_clk_timing(rate=scan_rate,
                                    sample_mode=AcquisitionType.CONTINUOUS,
                                    samps_per_chan=num_samples_per_line)

    # Read and process the data
    for i in range(num_lines):
        # One line of data
        data = task.read(number_of_samples_per_channel=num_samples_per_line)
        image_data[i, :] = data[:, -flyback]

        # Code for movement between lines (add a delay so that I don't detect)
        # Maybe add a couple of points of buffer

# Display image
plt.imshow(image_data, cmap='gray')
plt.colorbar()
plt.show()