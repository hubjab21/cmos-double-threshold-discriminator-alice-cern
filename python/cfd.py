import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 20, 1000)

def input_signal(t, t0=5.0, A=1.0, tau=2.0):
    y = np.zeros_like(t)
    
    mask = t >= t0
    x = t[mask] - t0
    
    y[mask] = A * x * np.exp(-x / tau)
    
    return y

def find_zero_after(t, y_diff, t_min=5):
    mask = t > t_min
    
    t_cut = t[mask]
    y_cut = y_diff[mask]
    
    idx = np.where(np.diff(np.sign(y_cut)) != 0)[0]
    
    if len(idx) == 0:
        return None
    
    i = idx[0]
    
    x1, x2 = t_cut[i], t_cut[i+1]
    y1, y2 = y_cut[i], y_cut[i+1]
    
    return x1 - y1 * (x2 - x1) / (y2 - y1)

def delay_signal(signal, t, delay):
    return np.interp(t - delay, t, signal, left=0, right=0)
    
y = input_signal(t, t0=5, A=0.885, tau=1.9)

delay = 1.5
y_delayed = delay_signal(y, t, delay)

attenuation = 0.3
y_attenuated = attenuation * y

y_diff = y_delayed - y_attenuated

t_zero = find_zero_after(t, y_diff, t_min=5)

digital_width = 5.0

digital_signal = np.zeros_like(t)
digital_signal[(t >= t_zero) & (t <= t_zero + digital_width)] = 5

plt.figure(figsize=(12, 6))

ax1 = plt.gca()
ax1.axvline(t_zero, linestyle='--', color='red', linewidth=1.5)
ax1.plot(t, y, color='#fb7f0e', label='Input signal', linewidth=2)
ax1.plot(t, y_delayed, color='#439df7', label='Delayed (Δ=1.5 ns)', linewidth=2)
ax1.plot(t, y_attenuated, color='#00a676', label='Attenuated (f=0.30)', linewidth=2)
ax1.plot(t, y_diff, color='#6e12c4', label='Difference (delayed - attenuated)', linewidth=2)
plt.plot([], [], '--', color='red', label=f'Zero crossing ≈ {t_zero:.2f} ns')
plt.plot([], [], color='black', linewidth=2, label='Digital output (0/5 V)')

ax1.set_xlim(0, 20)
ax1.set_ylim(-0.19, 0.65)

ax1.set_xlabel("Time [ns]")
ax1.set_ylabel("Analog voltage [V]")

ax2 = ax1.twinx()
ax2.set_ylim(-1.525, 5.1)
ax2.set_ylabel("Digital voltage [V]")
ax2.plot(t, digital_signal, color='black', label='Digital output', linewidth=2)

ax1.legend()
ax1.grid()

plt.show()


