import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 2, 1000)

def triangle(t, t_start, t_peak, t_end, height):
    y = np.zeros_like(t)

    rising = (t >= t_start) & (t <= t_peak)
    y[rising] = height * (t[rising] - t_start) / (t_peak - t_start)

    falling = (t > t_peak) & (t <= t_end)
    y[falling] = height * (t_end - t[falling]) / (t_end - t_peak)

    return y

y1 = triangle(t, 0.3, 0.8, 1.7, 2.0)
y2 = triangle(t, 0.3, 0.8, 1.7, 1.5)
y3 = triangle(t, 0.3, 0.8, 1.7, 1.0)

mask = (t < 0.3) | (t > 1.7)
y1[mask] = np.nan
y2[mask] = np.nan
y3[mask] = np.nan

plt.figure(figsize=(12, 6))
plt.plot(t, y1, color='#2ca02c', label='Signal 1 (~2.0 V)', linewidth=2)
plt.plot(t, y2, color='#439df7', label='Signal 2 (~1.5 V)', linewidth=2)
plt.plot(t, y3, color='#fb7f0e', label='Signal 3 (~1.0 V)', linewidth=2)
plt.plot([], [], ' ', label='Δt = 0.225 ns')
plt.xlim(0, 2)
plt.xlim(0, 2)
plt.ylim(0, 2.1)

plt.axhline(0.9, linestyle='--', color='red', linewidth=1.2)
threshold = 0.9

t_cross1 = t[np.where(y1 >= threshold)[0][0]]
t_cross2 = t[np.where(y2 >= threshold)[0][0]]
t_cross3 = t[np.where(y3 >= threshold)[0][0]]

plt.vlines(t_cross1, ymin=0, ymax=0.9, colors='#2ca02c', linestyles='--', linewidth=1)
plt.vlines(t_cross2, ymin=0, ymax=0.9, colors='#439df7', linestyles='--', linewidth=1)
plt.vlines(t_cross3, ymin=0, ymax=0.9, colors='#fb7f0e', linestyles='--', linewidth=1)
plt.axvline(0.8, linestyle='--', color='black', linewidth=1)
plt.hlines(2.0, xmin=0, xmax=0.8, colors='#2ca02c', linestyles='--', linewidth=1)
plt.hlines(1.5, xmin=0, xmax=0.8, colors='#439df7', linestyles='--', linewidth=1)
plt.hlines(1.0, xmin=0, xmax=0.8, colors='#fb7f0e', linestyles='--', linewidth=1)

# add double arrow (Δt) between x=0.525 and x=0.75 at y=0.25
plt.annotate(
    '',
    xy=(0.760, 0.25),      # end point
    xytext=(0.520, 0.25), # start point
    arrowprops=dict(
        arrowstyle='<->',  # double-headed arrow
        color='red',
        linewidth=1.5
    )
)
plt.text(0.65, 0.28, 'Jitter', color='red', ha='center')
plt.xlabel("Time [ns]")
plt.ylabel("Analog voltage [V]")
plt.legend()
plt.grid()

plt.show()
