import simpy

class Packet(object):
    def __init__(self, time, size, id, src="a", dst="z", flow_id=0):
        self.time = time
        self.size = size
        self.id = id
        self.src = src
        self.dst = dst
        self.flow_id = flow_id

    def __lt__(self, other):
            return self.flow_id < other.flow_id

    def __repr__(self):
        return "id: {}, src: {}, time: {}, size: {}, flow_id: {}".\
            format(self.id, self.src, self.time, self.size, self.flow_id)


class PacketGenerator(object):
    def __init__(self, env, id,  adist, sdist, finish=float("inf"), flow_id=0):
        self.id = id
        self.env = env
        self.adist = adist
        self.sdist = sdist
        self.finish = finish
        self.out = None
        self.action = env.process(self.run())
        self.flow_id = flow_id

    def run(self):
        while self.env.now < self.finish:
            yield self.env.timeout(self.adist())
            p = Packet(self.env.now, self.sdist(), src=self.id, flow_id=self.flow_id)
            self.out.put(p)


class PacketSink(object):
    def __init__(self, env, rec_waits=True, selector=None):
        self.store = simpy.Store(env)
        self.env = env
        self.rec_waits = rec_waits
        self.waits = []
        self.selector = selector
        self.waits_flow1 = []
        self.waits_flow2 = []
        self.waits_flow3 = []

    def put(self, pkt):
        if not self.selector or self.selector(pkt):
            if self.rec_waits:
                self.waits.append(self.env.now - pkt.time)
            if pkt.flow_id == 1:
                self.waits_flow1.append(self.env.now - pkt.time)
            if pkt.flow_id == 2:
                self.waits_flow2.append(self.env.now - pkt.time)
            if pkt.flow_id == 3:
                self.waits_flow3.append(self.env.now - pkt.time)

class SwitchPort(object):
    def __init__(self, env, rate, qlimit=None):
        self.store1 = simpy.Store(env)
        self.store2 = simpy.Store(env)
        self.store3 = simpy.Store(env)
        self.rate = rate
        self.env = env
        self.out = None
        self.qlimit = qlimit
        self.byte_size = 0
        self.action = env.process(self.run())
        self.queue = []

    def run(self):
        while True:
            for _ in iter(int, 1):
                start_time = self.env.now
                current_time = self.env.now
                elapsed_time = current_time - start_time

                while elapsed_time < 3:
                    current_time = self.env.now
                    elapsed_time = current_time - start_time
                    msg = (yield self.store1.get())
                    yield self.env.timeout(msg.size * 8.0 / self.rate)
                    self.out.put(msg)
                start_time = self.env.now
                current_time = self.env.now
                elapsed_time = current_time - start_time
                while elapsed_time < 3:
                    current_time = self.env.now
                    elapsed_time = current_time - start_time
                    msg = (yield self.store2.get())
                    yield self.env.timeout(msg.size * 8.0 / self.rate)
                    self.out.put(msg)
                start_time = self.env.now
                current_time = self.env.now
                elapsed_time = current_time - start_time
                while elapsed_time < 3:
                    current_time = self.env.now
                    elapsed_time = current_time - start_time
                    msg = (yield self.store3.get())
                    yield self.env.timeout(msg.size * 8.0 / self.rate)
                    self.out.put(msg)

    def put(self, pkt):
        if pkt.flow_id == 1:
            return self.store1.put(pkt)
        if pkt.flow_id == 2:
            return self.store2.put(pkt)
        if pkt.flow_id == 3:
            return self.store3.put(pkt)

