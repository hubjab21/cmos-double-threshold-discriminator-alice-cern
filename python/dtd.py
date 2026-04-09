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
plt.plot([], [], '--', color='#2ca02c', label='Δt1 = 0.100')
plt.plot([], [], '--', color='#439df7', label='Δt2 = 0.133')
plt.plot([], [], '--', color='#fb7f0e', label='Δt3 = 0.200')

plt.xlim(0, 2)
plt.ylim(0, 2.1)

plt.axhline(0.9, linestyle='--', color='red', linewidth=1.2)
threshold = 0.9

t_cross1 = t[np.where(y1 >= threshold)[0][0]]
t_cross2 = t[np.where(y2 >= threshold)[0][0]]
t_cross3 = t[np.where(y3 >= threshold)[0][0]]

plt.axhline(0.5, linestyle='--', color='#6e12c4', linewidth=1.2)

threshold2 = 0.5

t1_cross1 = t[np.where(y1 >= threshold2)[0][0]]
t1_cross2 = t[np.where(y2 >= threshold2)[0][0]]
t1_cross3 = t[np.where(y3 >= threshold2)[0][0]]


plt.vlines(t_cross1, ymin=0, ymax=0.9, colors='#2ca02c', linestyles='--', linewidth=1)
plt.vlines(t_cross2, ymin=0, ymax=0.9, colors='#439df7', linestyles='--', linewidth=1)
plt.vlines(t_cross3, ymin=0, ymax=0.9, colors='#fb7f0e', linestyles='--', linewidth=1)

plt.vlines(t1_cross1, ymin=0, ymax=0.5, colors='#2ca02c', linestyles='--', linewidth=1.5)
plt.vlines(t1_cross2, ymin=0, ymax=0.5, colors='#439df7', linestyles='--', linewidth=1.5)
plt.vlines(t1_cross3, ymin=0, ymax=0.5, colors='#fb7f0e', linestyles='--', linewidth=1.5)

plt.axvline(0.8, linestyle='--', color='black', linewidth=1)
plt.hlines(2.0, xmin=0, xmax=0.8, colors='#2ca02c', linestyles='--', linewidth=1)
plt.hlines(1.5, xmin=0, xmax=0.8, colors='#439df7', linestyles='--', linewidth=1)
plt.hlines(1.0, xmin=0, xmax=0.8, colors='#fb7f0e', linestyles='--', linewidth=1)

# add double arrow (Δt) between x=0.525 and x=0.75 at y=0.25
plt.annotate(
    '',
    xy=(0.555, 0.03),      # end point
    xytext=(0.420, 0.03), # start point
    arrowprops=dict(
        arrowstyle='<->',  # double-headed arrow
        color='red',
        linewidth=1.5
    )
)

plt.annotate(
    '',
    xy=(0.535, 0.15),      # end point
    xytext=(0.420, 0.15), # start point
    arrowprops=dict(
        arrowstyle='<->',  # double-headed arrow
        color='#2ca02c',
        linewidth=1.5
    )
)

plt.annotate(
    '',
    xy=(0.610, 0.25),      # end point
    xytext=(0.465, 0.25), # start point
    arrowprops=dict(
        arrowstyle='<->',  # double-headed arrow
        color='#439df7',
        linewidth=1.5
    )
)

plt.annotate(
    '',
    xy=(0.760, 0.35),      # end point
    xytext=(0.545, 0.35), # start point
    arrowprops=dict(
        arrowstyle='<->',  # double-headed arrow
        color='#fb7f0e',
        linewidth=1.5
    )
)

plt.text(0.495, 0.06, 'Jitter', color='red', ha='center', fontweight='bold')
plt.text(0.485, 0.17, 'Δt1', color='#2ca02c', ha='center', fontweight='bold')
plt.text(0.537, 0.28, 'Δt2', color='#439df7', ha='center', fontweight='bold')
plt.text(0.660, 0.38, 'Δt3', color='#fb7f0e', ha='center', fontweight='bold')

plt.xlabel("Time [ns]")
plt.ylabel("Analog voltage [V]")
plt.legend()
plt.grid()

plt.show()
