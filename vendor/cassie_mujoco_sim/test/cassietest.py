#!/usr/bin/env python3

# Copyright (c) 2018 Dynamic Robotics Laboratory
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from cassiemujoco import *
import time

# Initialize cassie simulation
sim = CassieSim()
vis = CassieVis()

# Set control parameters
u = pd_in_t()
u.leftLeg.motorPd.torque[3] = 0 # Feedforward torque
u.leftLeg.motorPd.pTarget[3] = -1
u.leftLeg.motorPd.pGain[3] = 1000 # proportional gain
u.leftLeg.motorPd.dTarget[3] = -2
u.leftLeg.motorPd.dGain[3] = 1000 # differential gain
u.rightLeg.motorPd = u.leftLeg.motorPd
for i in range(5):
    print(i, u.leftLeg.motorPd.pTarget[i])
u.rightLeg.motorPd.pTarget[3] = -0.5
u.leftLeg.motorPd.pGain[3] = 100
u.rightLeg.motorPd.pTarget[0] = 1.5

# Hold pelvis in place
#sim.hold()

# Record time
t = time.monotonic()

# Run until window is closed

for j in range(1000):
    #for i in range(5):
    #    print(i, u.rightLeg.motorPd.pTarget[i])

    s = sim.get_state()

    u.rightLeg.motorPd.pTarget[3] = -1

    for _ in range(33):
        y = sim.step_pd(u)

    if not vis.draw(sim):
        break

    while time.monotonic() - t < 1/60:
        time.sleep(0.001)
    t = time.monotonic()
