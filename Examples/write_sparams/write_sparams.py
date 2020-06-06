"""
SiEPIC Photonics Package

Author:     Mustafa Hammood
            Mustafa@siepic.com
            
            https://github.com/SiEPIC-Kits/SiEPIC_Photonics_Package

Module:     s-parameters writer

Write data to Lumerical INTERCONNECT S-parameters .dat format

TO DO: add orthogonal identifier handlers, currently works only for orth. ID 1
"""
#%%
import numpy as np

class S_param_file():
    def __init__(self):
        self.name = 'sparams'
        self.wavl = [1500e-9, 1600e-9, 20e-9] # start, stop, resolution
        self.n_ports = 2
        self.data = 0
        self.encoding = 'utf-8'

    def make_file(self):
        f = open(self.name+'.dat',"wb")
        return f

    def npoints(self):
        self.nPts = int((self.wavl[1]-self.wavl[0])/self.wavl[2] +1)
        return self.nPts

    def get_index(self, idx):
        return str(int(idx/self.n_ports)+1)+str(idx%self.n_ports+1)

    def visualize(self):
        import matplotlib.pyplot as plt
        wavelength = np.linspace(self.wavl[0], self.wavl[1], self.npoints())
        for idx, S in enumerate(self.data):
            txt = 'S'+self.get_index(idx)
            plt.plot(wavelength*1e9, 10*np.log10(S[0]), label = txt)
        plt.xlabel('Wavelength [nm]')
        plt.ylabel('Re(Transmission) [dB]')
        plt.tight_layout()
        plt.legend()
        return 0

    def write_header(self, file):
        for i in range(self.n_ports):
            text = bytes('["port %d",""]\n' % (i+1), encoding = self.encoding)
            file.write(text)
        return 0

    def write_S_header(self, file, S):
        port1 = S[0]; port2 = S[1]; OID1 = S[2]; OID2 = S[3]
        text = bytes('("port %d","mode 1",%d,"port %d",%d,"transmission")\n' % (port1, OID1, port2, OID2), encoding = 'utf-8')
        file.write(text)
        text = bytes('(%d, 3)\n' % self.nPts, encoding = self.encoding)
        file.write(text)
        return 0

    def write_S_data(self, file, data):
        c = 299792458 #m/s
        wavelength = np.linspace(self.wavl[0], self.wavl[1], self.nPts)
        freq = c/wavelength; freq = np.flip(freq)
        for idx, i in enumerate(freq):
            text = bytes('%d %f %f\n' % (i, data[0][idx], data[1][idx]), encoding = self.encoding)
            file.write(text)
        return 0

    def write_S(self):
        self.npoints()
        f = self.make_file()
        self.write_header(f)
        idx = 0
        for i in range(self.n_ports):
            for k in range(self.n_ports):
                S = [i+1,k+1,1,1] # out_port, in_port2, out_OID1, in_OID2
                self.write_S_header(f, S)
                self.write_S_data(f, self.data[idx])
                idx+=1
        f.close()
        return 0
#%%
sparams = S_param_file()
sparams.n_ports = 2
sparams.wavl = [1500e-9, 1600e-9, 0.1e-9]

# generate dummy s-parameters data
# data format [S11, S12, ...., S21, S22, ....]
linspace = np.linspace(0,10*np.pi,sparams.npoints())
S11 = [0.3*np.sin(linspace)+0.3, 0*linspace] # [real, imag]
S12 = [0.5*np.cos(linspace)+0.5, 0*linspace]
S22= np.array(S11)/2; S21 = np.array(S12)/2
sparams.data = [S11, S12, S21, S22]

sparams.write_S()
sparams.visualize()

# %%
