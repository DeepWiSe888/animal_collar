import numpy as np
import struct
from scipy import signal,ndimage
try:
    from conf import *
except:
    from libs.conf import *

def parse_radar_pack(pack):
    cursor = 0
    cursor = cursor + len(flag)
    
    # sec
    sec_pack_tmp = pack[cursor:cursor + 4]
    sec = list(struct.unpack('L',sec_pack_tmp))[0]
    cursor = cursor + 4

    # usec
    usec_pack_tmp = pack[cursor:cursor + 4]
    usec = list(struct.unpack('L',usec_pack_tmp))[0]
    usec = usec / 1000000
    cursor = cursor + 4

    # rx
    rx_pack_tmp = pack[cursor:cursor + 4]
    rx = list(struct.unpack('i',rx_pack_tmp))[0]
    cursor = cursor + 4

    # tx
    tx_pack_tmp = pack[cursor:cursor + 4]
    tx = list(struct.unpack('i',tx_pack_tmp))[0]
    cursor = cursor + 4

    # frame no
    fno_pack_tmp = pack[cursor:cursor + 4]
    fno = list(struct.unpack('i',fno_pack_tmp))[0]
    cursor = cursor + 4

    # DATA
    adc_data_pack_tmp = pack[cursor:]
    adc_data = list(struct.unpack('{}f'.format(len(adc_data_pack_tmp)//4),adc_data_pack_tmp))

    pack_dict = {'fno':fno,'tx':tx,'rx':rx,'t':sec + usec,'data':adc_data}
    return pack_dict

def parse_imu_pack(pack):
    cursor = 0
    cursor = cursor + len(flag)
    
    # sec
    sec_pack_tmp = pack[cursor:cursor + 4]
    sec = list(struct.unpack('L',sec_pack_tmp))[0]
    cursor = cursor + 4

    # usec
    usec_pack_tmp = pack[cursor:cursor + 4]
    usec = list(struct.unpack('L',usec_pack_tmp))[0]
    usec = usec / 1000000
    cursor = cursor + 4

    # pressure
    pressure_pack_tmp = pack[cursor:cursor + 8]
    pressure = list(struct.unpack('d',pressure_pack_tmp))[0]
    cursor = cursor + 8

    # temp
    temp_pack_tmp = pack[cursor:cursor + 8]
    temp = list(struct.unpack('d',temp_pack_tmp))[0]
    cursor = cursor + 8

    # hum
    hum_pack_tmp = pack[cursor:cursor + 8]
    hum = list(struct.unpack('d',hum_pack_tmp))[0]
    cursor = cursor + 8

    # lux
    lux_pack_tmp = pack[cursor:cursor + 4]
    lux = list(struct.unpack('I',lux_pack_tmp))[0]
    cursor = cursor + 4
    
    # uvs
    uvs_pack_tmp = pack[cursor:cursor + 4]
    uvs = list(struct.unpack('I',uvs_pack_tmp))[0]
    cursor = cursor + 4
    
    # gas
    gas_pack_tmp = pack[cursor:cursor + 4]
    gas = list(struct.unpack('I',gas_pack_tmp))[0]
    cursor = cursor + 4
    
    # angles
    fyaw_pack_tmp = pack[cursor:cursor + 4]
    yaw = list(struct.unpack('f',fyaw_pack_tmp))[0]
    cursor = cursor + 4
    
    fpitch_pack_tmp = pack[cursor:cursor + 4]
    pitch = list(struct.unpack('f',fpitch_pack_tmp))[0]
    cursor = cursor + 4
    
    froll_pack_tmp = pack[cursor:cursor + 4]
    roll = list(struct.unpack('f',froll_pack_tmp))[0]
    cursor = cursor + 4
    
    # acceleration 
    acceleration_x_pack_tmp = pack[cursor:cursor + 2]
    acceleration_x = list(struct.unpack('h',acceleration_x_pack_tmp))[0]
    cursor = cursor + 2
    
    acceleration_y_pack_tmp = pack[cursor:cursor + 2]
    acceleration_y = list(struct.unpack('h',acceleration_y_pack_tmp))[0]
    cursor = cursor + 2
    
    acceleration_z_pack_tmp = pack[cursor:cursor + 2]
    acceleration_z = list(struct.unpack('h',acceleration_z_pack_tmp))[0]
    cursor = cursor + 2
    
    # gyroscope 
    gyroscope_x_pack_tmp = pack[cursor:cursor + 2]
    gyroscope_x = list(struct.unpack('h',gyroscope_x_pack_tmp))[0]
    cursor = cursor + 2
    
    gyroscope_y_pack_tmp = pack[cursor:cursor + 2]
    gyroscope_y = list(struct.unpack('h',gyroscope_y_pack_tmp))[0]
    cursor = cursor + 2
    
    gyroscope_z_pack_tmp = pack[cursor:cursor + 2]
    gyroscope_z = list(struct.unpack('h',gyroscope_z_pack_tmp))[0]
    cursor = cursor + 2
    
    # magnetic 
    magnetic_x_pack_tmp = pack[cursor:cursor + 2]
    magnetic_x = list(struct.unpack('h',magnetic_x_pack_tmp))[0]
    cursor = cursor + 2
    
    magnetic_y_pack_tmp = pack[cursor:cursor + 2]
    magnetic_y = list(struct.unpack('h',magnetic_y_pack_tmp))[0]
    cursor = cursor + 2
    
    magnetic_z_pack_tmp = pack[cursor:cursor + 2]
    magnetic_z = list(struct.unpack('h',magnetic_z_pack_tmp))[0]
    cursor = cursor + 2
    
    pack_dict = {'time':sec+usec,'pressure':round(pressure,2),'temperature':round(temp,2),'humidity':round(hum,2),
                 'illuminance':lux,'uvs':uvs,'gas':gas,
                 'angles':{'Yaw':round(yaw,2),'Pitch':round(pitch,2),'Roll':round(roll,2)},
                 'acceleration':{'x':acceleration_x,'y':acceleration_y,'z':acceleration_z},
                 'gyroscope':{'x':gyroscope_x,'y':gyroscope_y,'z':gyroscope_z},
                 'magnetic':{'x':magnetic_x,'y':magnetic_y,'z':magnetic_z}}
    print(pack_dict)
    return pack_dict


def range_fft(data,range_fft_n):
    data =  data * np.hanning(len(data))
    data_fft = np.fft.fft(data,range_fft_n)
    return data_fft
    