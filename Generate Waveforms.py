import nidaqmx
import math
import time




def generate_stair_function(num_steps, min, max):
    function = []
    step_size = (max - min) / num_steps
    for step in range(num_steps):
        function.append(min + step_size * step)
    return function

def generate_sine_function(frequency, amplitude, num_samples, sample_rate):
    function = []
    for x in range(num_samples):
        function.append(amplitude * math.sin(2 * math.pi * x * (frequency / sample_rate)))
    return function

#define constants
sample_rate = 10000

sine_freq = 100
sine_amplitude = 1.0
sine_num_samples = 10000

stair_step_number = 100
stair_min = 0.0
stair_max = 2.0
step_duration = .05

#calculate functions
stair_step_function = generate_stair_function(stair_step_number, stair_min, stair_max)
sine_function = generate_sine_function(sine_freq, sine_amplitude, sine_num_samples, sample_rate)

with nidaqmx.Task() as task:
    task.ao_channels.add_ao_voltage_chan('PXI1Slot18/ao0')

    #software timed
    print('Generate stair step function ')
    task.write(0.0, auto_start=True)
    for step in stair_step_function:
        task.write(step)
        time.sleep(step_duration)
    task.stop()

    #switch to hardware timing
    task.timing.cfg_samp_clk_timing(sample_rate, samps_per_chan=sine_num_samples)

    print('Generate sine wave ')
    print(task.write(sine_function, auto_start=True))
    task.wait_until_done(timeout=10.0)
    task.write(0.0)
    task.stop()
