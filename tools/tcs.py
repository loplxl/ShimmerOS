import ctypes

class TIMECAPS(ctypes.Structure):
    _fields_ = [("wPeriodMin", ctypes.c_uint),
                ("wPeriodMax", ctypes.c_uint)]

tc = TIMECAPS()
ctypes.windll.winmm.timeGetDevCaps(ctypes.byref(tc), ctypes.sizeof(tc))
print(f"Minimum timer resolution: {tc.wPeriodMin} ms")
print(f"Maximum timer resolution: {tc.wPeriodMax} ms")
