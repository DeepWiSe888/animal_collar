import os
import time
import numpy as np

import threading
from pyqtgraph.Qt import QtGui, QtWidgets
import pyqtgraph.opengl as gl
import pyqtgraph as pg

from libs.conf import *
from libs.utils import *
from libs.reader import *
from libs.plot import PlotData


def read_data(path,dev_type):
    files = []
    if os.path.isdir(path):
        fs = os.listdir(path)
        for f in fs:
            if f.endswith('.txt'):
                files.append(path + f)
    else:
        if path.endswith('.txt'):
            files.append(path)

    framelist = []
    for file in files:
        reader = RawDataReader(file,dev_type)
        while True:
            frame = reader.get_next_frame()
            if frame is None:
                break
            if dev_type == RADAR:
                adc_tmp = frame["data"]
                adc = np.zeros((num_tx * num_rx ,num_chirps_per_frame,num_samples_per_chirp),dtype=np.complex_)
                try:
                    for i in range(num_tx * num_rx):
                        adc[i,:,:] = np.reshape(adc_tmp[num_chirps_per_frame * num_samples_per_chirp * i:num_chirps_per_frame * num_samples_per_chirp * (i + 1)],(num_chirps_per_frame,num_samples_per_chirp))
                except:
                    pass
                (n_rx,_,_) = adc.shape
                rx_iq = np.zeros((n_rx,num_range_bins),dtype=np.complex_)
                for rx in range(n_rx):
                    tmp_adc = np.mean(adc[rx,:,:],0)
                    iq = range_fft(tmp_adc,num_range_nfft)
                    iq = iq[:num_range_bins]
                    rx_iq[rx,:] = iq
                framelist.append(rx_iq)
            else:
                framelist.append(frame)
    return framelist

def main():
    plot_data = PlotData()
    
    path = "./datas/data_1666766328.txt"
    range_data = read_data(path,RADAR)
    range_data = np.array(range_data)
    (frame_cnt,rx_cnt,bin_cnt) = range_data.shape
    
    path = "./datas/sensor_data_1666770167.txt"
    environment_data = read_data(path,IMU)
    
    try:
        #plot data
        for i in range(0,frame_cnt - FRAMES,STEP):
            x = range_data[i:i+FRAMES,:,OFFSET:MAX_BIN]
            x = np.mean(x,1)
            
            #remove the background
            iq_data = x - np.mean(x,0)
            iq_abs = np.abs(iq_data)
            iq_bin_sum = np.sum(iq_abs,0)

            #determine the target bin
            iq_bin = np.mean(np.abs(iq_data),0)
            bin_offset = 0
            bin_idx = np.where(np.max(iq_bin[bin_offset:]) <= iq_bin[bin_offset:])[0][0]
            bin_idx += bin_offset
            print(bin_idx)
            org_wave = iq_data[:,bin_idx]

            #fft
            fft_data = np.fft.fft(iq_data,n = NFFT,axis=0)
            fft_shift_data = np.fft.fftshift(fft_data,axes=0)
            fft_abs = np.abs(fft_shift_data)

            curve_list = [iq_bin_sum,[org_wave.real,org_wave.imag],iq_abs[:,bin_idx],
                                  np.abs(x).T,iq_abs.T,fft_abs.T]
                    
            plot_data.update(curve_list)
            
            #update plot immediate
            QtWidgets.QApplication.processEvents()

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
