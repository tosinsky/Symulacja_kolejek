import random
import functools
import simpy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from SimComponentsC import PacketGenerator, PacketSink, SwitchPort

lambda_= 0.4
mu_ = 1
mean_pkt_size = 100
def same_size():
    return 100

adist = functools.partial(random.expovariate, lambda_)
sdist = functools.partial(same_size)

samp_dist = functools.partial(random.expovariate, 1.0)

port_rate = mu_*8*mean_pkt_size

env = simpy.Environment()

ps = PacketSink(env, rec_waits=True)
pg = PacketGenerator(env, "ID", adist, sdist, flow_id=1)
pg2 = PacketGenerator(env, "ID", adist, sdist, flow_id=2)
pg3 = PacketGenerator(env, "ID", adist, sdist, flow_id=3)

switch_port = SwitchPort(env, port_rate, qlimit=None)

pg.out = switch_port
pg2.out = switch_port
pg3.out = switch_port

switch_port.out = ps

env.run(until=2000)


print("Średni czas oczekiwania pakietu = {:.3f}".format(sum(ps.waits)/len(ps.waits)))
print("Średni czas oczekiwania pakietu kolejki 1 = {:.3f}".format(sum(ps.waits_flow1)/len(ps.waits_flow1)))
print("Średni czas oczekiwania pakietu kolejki 2 = {:.3f}".format(sum(ps.waits_flow2)/len(ps.waits_flow2)))
print("Średni czas oczekiwania pakietu kolejki 3 = {:.3f}".format(sum(ps.waits_flow3)/len(ps.waits_flow3)))

plt.hist([ps.waits_flow1], weights=np.ones(len(ps.waits_flow1)) / len(ps.waits_flow1), color="Red", edgecolor = "black", bins=15)
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.title("Rozkład czasu oczekiwania pakietów kolejki 1")
plt.xlabel("Czas oczekiwania pakietu [tiki]")
plt.ylabel("Procent wszystkich pakietów kolejki")

plt.figure()
plt.hist([ps.waits_flow2], weights=np.ones(len(ps.waits_flow2)) / len(ps.waits_flow2), color="Blue", edgecolor = "black", bins=15)
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.title("Rozkład czasu oczekiwania pakietów kolejki 2")
plt.xlabel("Czas oczekiwania pakietu [tiki]")
plt.ylabel("Procent wszystkich pakietów kolejki")

plt.figure()
plt.hist([ps.waits_flow3], weights=np.ones(len(ps.waits_flow3)) / len(ps.waits_flow3), color="Green", edgecolor = "black", bins=15)
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.title("Rozkład czasu oczekiwania pakietów kolejki 3")
plt.xlabel("Czas oczekiwania pakietu [tiki]")
plt.ylabel("Procent wszystkich pakietów kolejki")

plt.figure()
plt.hist([ps.waits], weights=np.ones(len(ps.waits)) / len(ps.waits), color="Yellow", edgecolor = "black", bins=15)
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.title("Rozkład czasu oczekiwania pakietów wszystkich kolejek")
plt.xlabel("Czas oczekiwania pakietu [tiki]")
plt.ylabel("Procent wszystkich pakietów")
plt.show()
