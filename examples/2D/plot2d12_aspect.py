# Copyright (c) 2023 Jintao Li.
# Computational and Interpretation Group (CIG),
# University of Science and Technology of China (USTC).
# All rights reserved.
"""
aspect 参数的意义
======================

可以将 aspect 设置为 'equal' (default), 'auto' or float:
- 'equal' : 保持img的宽高比保持不变
- 'auto' : 宽高比与设置的figsize有关, 即改变长宽比
- float number f: 宽高比保持 f = h/w
"""

import cigvis
import numpy as np
import matplotlib.pyplot as plt

d = np.fromfile('../../data/rgt/sx.dat', np.float32).reshape(128, 128, 128)
sl = d[30, :, :]

fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# aspect='equal'
cigvis.plot2d(sl,
              aspect='equal',
              xlabel='xline',
              ylabel='time',
              title="Aspect='equal'",
              cbar='Amplitude',
              ax=axs[0, 0])

# aspect='auto'
cigvis.plot2d(sl,
              aspect='auto',
              xlabel='xline',
              ylabel='time',
              title="Aspect='auto'",
              cbar='Amplitude',
              ax=axs[0, 1])

# aspect=1.5  h/w=1.5
cigvis.plot2d(sl,
              aspect=1.5,
              xlabel='xline',
              ylabel='time',
              title="Aspect=1.5",
              cbar='Amplitude',
              ax=axs[1, 0])

# aspect=2/3, h/w=2/3
cigvis.plot2d(sl,
              aspect=2 / 3,
              xlabel='xline',
              ylabel='time',
              title="Aspect=2/3",
              cbar='Amplitude',
              ax=axs[1, 1])

plt.tight_layout()
plt.savefig('example.png', bbox_inches='tight', pad_inches=0.01, dpi=200)
plt.show()
