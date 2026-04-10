import numpy as np
import matplotlib.pyplot as plt


delay_ns = 5
attenuation = 0.30

t = np.linspace(0, 125, 2000)


def input_signal(t):
    y = 0.07 * np.sin(2 * np.pi * t / 40)
    y += 0.03 * np.sin(2 * np.pi * t / 80)
    y += 0.08
    return y


def delay_signal(signal, t, delay):
    return np.interp(t - delay, t, signal, left=0, right=0)


def attenuate_signal(signal, factor):
    return factor * signal

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
zero_crossings = [tz for tz in zero_crossings if 10 < tz < 115]

for tz in zero_crossings:
    plt.axvline(tz, color='gray', linestyle='--', linewidth=1.2, alpha=0.6)
    plt.plot(tz, 0, 'x', color='black')

plt.plot([], [], 'x', color='black', label='Zero crossings')


plt.xlim(5, 125)
plt.xticks(np.linspace(5, 120, 11), np.linspace(0, 100, 11))

plt.xlabel('Time [ns]')
plt.ylabel('Analog Voltage [V]')

plt.grid(True, alpha=0.3)

plt.legend(loc='lower right')
plt.tight_layout()
plt.show()
