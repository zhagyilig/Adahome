import psutil

 

pc_mem =psutil.virtual_memory()

div_gb_factor =(1024.0 ** 3)
div_m_factor =(1024.0 ** 2)

print("totalmemor: %fGB" % float(pc_mem.total/div_gb_factor))
print("totalmemor: %fGB" % float(pc_mem.total/div_m_factor))
