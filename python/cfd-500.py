import numpy as np
import matplotlib.pyplot as plt


delay_ns = 5
attenuation = 0.30

t = np.linspace(0, 525, 2000)


def sine_segment(t, t_start, t_end, y_start, y_end):
    y = np.zeros_like(t)
    
    mask = (t >= t_start) & (t <= t_end)
    x = (t[mask] - t_start) / (t_end - t_start)
    
    y[mask] = y_start + (y_end - y_start) * 0.5 * (1 - np.cos(np.pi * x))
    
    return y

def input_signal(t):
    y = np.zeros_like(t)

    y += sine_segment(t, 0, 40, 0, 0.25)    # rise to 0.25
    y += sine_segment(t, 40, 90, 0.25, 0)    # fall to 0

    y += sine_segment(t, 90, 130, 0, 0.45)    # rise to 0.45
    y += sine_segment(t, 130, 180, 0.45, 0)    # fall

    y += sine_segment(t, 180, 255, 0, 1.25)    #  large rise to 1.25
    y += sine_segment(t, 255, 295, 1.25, 0.4)  # fall to 0.4

    y += sine_segment(t, 295, 320, 0.4, 2.0)   # rise to 2.0
    y += sine_segment(t, 320, 360, 2.0, 0.0)  # fall

    y += sine_segment(t, 360, 410, 0.0, 1.0) # rise to 1.0
    y += sine_segment(t, 410, 450, 1.0, 0.05) # fall close to zero

    y += sine_segment(t, 450, 525, 0.05, 0.25) # final rise

    return y
    

def delay_signal(signal, t, delay):
    return np.interp(t - delay, t, signal, left=0, right=0)


def attenuate_signal(signal, factor):
    return factor * signal

def print_zero_crossings_with_amplitude(zero_crossings, t, y_in):
    print("Zero crossing times and input amplitudes:")
    
    if len(zero_crossings) == 0:
        print("No zero crossings found.")
        return
    
    for i, tz in enumerate(zero_crossings, 1):
        # interpolacja wartości sygnału wejściowego w czasie tz
        y_val = np.interp(tz, t, y_in)
        
        print(f"{i}. t = {tz:.2f} ns, Input amplitude = {y_val:.3f} V")

y_in = input_signal(t)
y_delayed = delay_signal(y_in, t, delay_ns)
y_attenuated = attenuation * y_in
y_diff = y_delayed - y_attenuated


zero_crossings = []

for i in range(len(y_diff) - 1):
    if y_diff[i] * y_diff[i + 1] < 0:
        t_zero = t[i] - y_diff[i] * (t[i + 1] - t[i]) / (y_diff[i + 1] - y_diff[i])
        zero_crossings.append(t_zero)

zero_crossings = np.array(zero_crossings)


plt.figure(figsize=(12, 6))

plt.plot(t, y_in, color='#d18f00', linewidth=2, label='Input signal')
plt.plot(t, y_delayed, color='#2ca7e0', linewidth=2, label=f'Delayed (Δ≈{delay_ns} ns)')
plt.plot(t, y_attenuated, color='#00916e', linewidth=2, label=f'Attenuated (f={attenuation:.2f})')
plt.plot(t, y_diff, color='#8b2bbd', linewidth=2, label='Difference (delayed - attenuated)')

plt.axhline(0, color='gray', linestyle='--', linewidth=1)
zero_crossings = [tz for tz in zero_crossings if 10 < tz < 525]

for tz in zero_crossings:
    plt.axvline(tz, color='gray', linestyle='--', linewidth=1.2, alpha=0.6)
    plt.plot(tz, 0, 'x', color='black')

plt.plot([], [], 'x', color='black', label='Zero crossings')


plt.xlim(5, 125)
plt.xticks(np.linspace(5, 525, 11), np.linspace(0, 500, 11))

plt.xlabel('Time [ns]')
plt.ylabel('Analog Voltage [V]')

plt.grid(True, alpha=0.3)

plt.legend(loc='upper right')
plt.tight_layout()
plt.show()

print_zero_crossings_with_amplitude(zero_crossings, t, y_in)
