from pydub import AudioSegment
import soundfile as sf
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import numpy as np
from scipy.io import wavfile
from numpy import fft as fft
from scipy import signal as s
from matplotlib import pyplot as plt
from scipy import io as  io

import scipy as sp
from matplotlib import pyplot as pl

state = 8

if (state==1):
    fName = 'normal.m4a'
elif (state==2):
    fName = 's3.m4a'
elif (state==3):
    fName = 's4.m4a'
elif (state == 4):
    fName = 's3 and s4.m4a'
elif (state == 5):
    fName = 'micTest.wav'
elif (state == 6):
    fName = 'noise.m4a'
elif (state == 7):
    fName = 'sja.wav'
elif (state == 8):
    fName = 'sja1.wav'
elif (state == 9):
    fName = 'sja2.wav'
elif (state == 10):
    fName = 'test.wav'
elif (state == 11):
    fName = 'test.wav'
elif (state == 12):
    fName = 'ttest.wav'

audio = AudioSegment.from_file(fName)



d_modified = []

if (fName[-3:]=='m4a'):
    # print("m4a")
    audio.export(fName, format="wav")
    [d, fs] = sf.read(fName)
    for i in d:
        d_modified.append(i[0])
    for i in d:
        d_modified.append(i[1])

if (fName[-3:]=='wav'):
    # print("wav")
    # [fs,d] = wavfile.read(fName)
    [d, fs] = sf.read(fName)
    d_modified =d


Ts = 1/fs
N = len(d)
t = np.asarray(list(range(0,N)))
t = t*Ts
n = np.asarray(list(range(1,N+1)))
tau = 2**16.55

if (len(d)<60000 + int(tau)):
    d1 = np.asarray(d)
else:
    d1 = np.asarray(d_modified[60000:60000 + int(tau)])

N1 = len(d1)
t = np.asarray(list(range(0,N1)))
t = t*Ts
y = d1*3


Y = fft.fft(y)
Y = fft.fftshift(Y)
n = np.asarray(list(range(0, N1)))
n = n-N1/2
f_hat = n/N1
f0 = f_hat*fs
Wn = np.asarray([20,150])
BPF_order = 3
fn = fs/2
ftype = 'bandpass'
[b,a] = s.butter(BPF_order,Wn/fn,ftype)


y2 = s.lfilter(b,a,y)
Y2 = fft.fft(y2)
Y2 = fft.fftshift(Y2)


y = y*2
y2 = y2*2

io.wavfile.write('Sound_before_filter.wav',fs,y)
io.wavfile.write('Sound_after_filter.wav',fs,y2)

N = 50
x = np.zeros(N-1)
x = np.insert(x,0,1,axis=0)
h1 = s.lfilter(b,a,x)


ffName = "IR_%d_th_order_fc_%d_Hz_length_%d.out" %(BPF_order, Wn[0], Wn[1])
f = open(ffName,"a")
for i in range(N):
    ff = "%f\n" % h1[i]
    f.write(ff)
f.close()


abs_y2 = abs(y2)
[locs,pks] = s.find_peaks(abs_y2,height=np.max(abs_y2)/5)


pks = (pks.get('peak_heights'))
plt.scatter(locs,pks,c = 'r')
plt.plot(abs_y2)
plt.show()

[locs2,pks2] = s.find_peaks(pks);
pks2 = (pks2.get('peak_heights'))

realPksLocs = []

for i in locs2:
    realPksLocs.append(locs[i])

rmv = []

for i in range(1,len(realPksLocs)):
    if (realPksLocs[i] - realPksLocs[i-1] < 2500):
        rmv.append(i)

for index in sorted(rmv, reverse=True):
    del realPksLocs[index]

realPks = []

for i in realPksLocs:
    realPks.append(abs_y2[i])

s1AndS2 = []
for i in realPks:
    if (i>np.max(realPks)*0.6):
        s1AndS2.append(i)
s1AndS2Locs = []

for i in range(len(realPks)):
    if(realPks[i]>np.max(realPks)*0.6):
        s1AndS2Locs.append(realPksLocs[i])

if (len(s1AndS2Locs)<2):
    Period = 1;
elif (len(s1AndS2Locs)<3):
    Period = (s1AndS2Locs[1]-s1AndS2Locs[0])*Ts
else:
    if (s1AndS2[0]>s1AndS2[1]):
        i =0
    else:
        i = 1
    Period = (t[s1AndS2Locs[i+2]]) - t[s1AndS2Locs[i]]

beatPerMinute = 60/Period

if (len(s1AndS2Locs)<3):
    print("normal")
    s3Result = "X";
    s4Result = "X";
    disease = "Normal"
else:
    for j in range(realPksLocs[0]):
        if (s1AndS2Locs[i]==realPksLocs[j]):
            startInd =j
        if (s1AndS2Locs[i+2]==realPksLocs[j]):
            endInd = j
            break
    if (endInd-startInd == 3):
        if abs(realPksLocs[endInd-1] - realPksLocs[endInd]) < abs(realPksLocs[endInd-2] - realPksLocs[endInd-1]):
            print("s4")
            s3Result = "X";
            s4Result = "O";
            disease = "s4";
        else:
            print("s3")
            resultCase = 2;
            s3Result = "O";
            s4Result = "X";
            disease = "s3";
    else:
        print("s3 and s4")
        s3Result = "O";
        s4Result = "O";
        disease = "s3 and s4";

print(s3Result)
print(s4Result)
print( beatPerMinute)
print(disease)


# try:
#     #specify the database details here
#     connection = mysql.connector.connect(host='localhost',
#                                          database='electronics',
#                                          user='pynative',
#                                          password='pynative@#29')
#
#     #have to write a custom querry to insert data
#     mySql_insert_query = """INSERT INTO Laptop (Id, Name, Price, Purchase_date)
#                            VALUES
#                            (1, 'Lenovo ThinkPad P71', 6459, '2019-08-14') """
#     cursor = connection.cursor()
#     result = cursor.execute(mySql_insert_query)
#     connection.commit()
#     cursor.close()
# except mysql.connector.Error as error:
#     print("Failed to insert ".format(error))
# finally:
#     if (connection.is_connected()):
#         connection.close()
#         print("MySQL connection is closed")










