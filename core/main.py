import Signal_Information
import node

s1 = Signal_Information.SignalInformation(0.5, ["A", "B", "C", "D"])

print(s1.path)
print(s1.signal_power)

s1.update_signal_power(0.2)

print(s1.signal_power)

s1.update_path()

print(s1.path)

s1.propagate()

