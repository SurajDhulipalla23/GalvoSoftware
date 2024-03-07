import numpy as np
import nidaqmx
from nidaqmx.constants import AcquisitionType

num_points_x = 400
num_points_y = 400
scan_rate = 1000  # Adjustable scan rate

# Sawtooth waveform for x-axis scanning
x_waveform = np.tile(np.linspace(-10, 10, num_points_x), num_points_y)  # ±10V range

# Step waveform for y-axis scanning
y_waveform = np.repeat(np.linspace(-10, 10, num_points_y), num_points_x)  # ±10V range

with nidaqmx.Task() as task:

    task.ao_channels.add_ao_voltage_chan("Dev1/ao0")  # X-channel
    task.ao_channels.add_ao_voltage_chan("Dev1/ao1")  # Y-channel

    # Configure timing
    task.timing.cfg_samp_clk_timing(rate=scan_rate, sample_mode=AcquisitionType.CONTINUOUS)

    # Waveforms to buffer
    task.write([x_waveform, y_waveform], auto_start=True)

    # Keep the task running until complete
    task.wait_until_done(timeout=10.0)

    # Stop + clear the task
    task.stop()
