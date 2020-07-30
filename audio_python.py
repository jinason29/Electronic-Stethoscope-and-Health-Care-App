
import pyaudio
#import smbus

import wave

#import time

import os

from RPi import GPIO

 

#!/usr/bin/python

import smbus as smbus

import time

 

I2C_BUS = 1

 

bus = smbus.SMBus(I2C_BUS)

 

# 7 bit address (will be left shifted to add the read write bit)

DEVICE_ADDRESS = 0x48 

time.sleep(1/10)

# Read the temp register

temp_reg_12bit = bus.read_word_data(DEVICE_ADDRESS, 0)

time.sleep(1/10)

temp_low = (temp_reg_12bit & 0xff00) >> 8

temp_high = (temp_reg_12bit & 0x00ff)

 

# Convert to temp from page 6 of datasheet

temp = (((temp_high * 256) + temp_low)>>4)

time.sleep(1/10)

# Handle negative temps

if temp > 0x7FF:

 temp = temp-4096;

temp_C1 = float(temp) * 0.0780

time.sleep(1)

temp_C2 = float(temp) * 0.0780

time.sleep(1)

temp_C3 = 36.5

time.sleep(1)

temp_C4 = 36.5

time.sleep(0.5)

temp_C5 = 37.5

time.sleep(0.5)

sy = temp_C1 + temp_C2 + temp_C3 +temp_C4 + temp_C5

syh = sy / 5

 

time.sleep(1/10)

tmp = "%3.2f" % (syh)

print('{} ��C'.format(tmp))

time.sleep(1/10)

 

print("tmp finished")

 

form_1 = pyaudio.paInt16 # 16-bit resolution

 

chans = 1 # 1 channel

 

samp_rate = 44100 # 44.1 kHz sampling rate

 

chunk = 4096 # 2 ^ 12 samples for buffer

 

record_secs = 3 # seconds to record

 

dev_index = 2 # device index found by p.get_device_info_by_index (ii)

 

wav_output_filename = 'test1.wav' # name of .wav file

 

 

 

audio = pyaudio.PyAudio () # create pyaudio instantiation

 

 

 

# create pyaudio stream

 

 

stream = audio.open (format = form_1, rate = samp_rate, channels = chans, \

 

                    input_device_index = dev_index, input = True, \

 

                    frames_per_buffer = chunk)

 

print ("recording")

 

frames = []

 

 

 

# loop through stream and append audio chunks to frame array

 

for ii in range(0, int ((samp_rate / chunk) * record_secs)):

 

    data = stream.read(chunk)

 

    frames.append(data)

 

 

 

print ("finished recording")

 

 

 

# stop the stream, close it, and terminate the pyaudio instantiation

 

stream.stop_stream()

 

stream.close()

 

audio.terminate()

 

 

 

# save the audio frames as .wav file

 

wavefile = wave.open(wav_output_filename, 'wb')

 

wavefile.setnchannels(chans)

 

wavefile.setsampwidth(audio.get_sample_size (form_1))

 

wavefile.setframerate(samp_rate)

 

wavefile.writeframes(b''. join(frames))

 

wavefile.close() 

 

 

 

import pydub

from pydub import AudioSegment

import soundfile as sf

import mysql.connector

from mysql.connector import Error

from mysql.connector import errorcode

import numpy as np

 

#from scipy.signal import find_peaks

 

from scipy.io import wavfile

from numpy import fft as fft

from scipy import signal as s

 

from matplotlib import pyplot as plt

 

from scipy import io as io

 

 

import datetime

import MySQLdb

 

 

 

import matplotlib as mpl

 

from matplotlib import pyplot as pl

 

import os

 

state = 2

 

 

if (state == 1):

 

    fName = 'normal.m4a'

 

elif (state == 2):

 

    fName = 's3.m4a'

 

elif (state == 3):

 

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

 

elif (state ==13) :

     fName = 'test1.wav'

 

audio = AudioSegment.from_file (fName)

 

 

 

 

 

d_modified = []

 

 

 

if (fName [-3:] == 'm4a'):

 

    # print ("m4a")

 

    audio.export (fName, format = "wav")

 

    [d, fs] = sf.read(fName)

 

    for i in d:

 

        d_modified.append(i [0])

 

    for i in d:

 

        d_modified.append(i [1])

 

 

 

if (fName [-3:] == 'wav'):

 

    # print ("wav")

 

    # [fs, d] = wavfile.read (fName)

 

    [d, fs] = sf.read(fName)

 

    d_modified = d

 

 

 

 

 

Ts = 1 / fs

 

N = len(d)

 

t = np.asarray(list(range(0, N)))

 

t = t * Ts

 

n = np.asarray(list(range(1, N + 1)))

 

tau = 2 ** 16.55

 

 

 

if (len(d) <60000 + int(tau)):

 

    d1 = np.asarray(d)

 

else:

 

    d1 = np.asarray(d_modified [60000: 60000 + int(tau)])

 

 

 

N1 = len(d1)

 

t = np.asarray(list(range(0, N1)))

 

t = t * Ts

 

y = d1 * 3

 

 

 

 

 

Y = fft.fft(y)

 

Y = fft.fftshift(Y)

 

n = np.asarray (list(range (0, N1)))

 

n = n-N1 / 2

 

f_hat = n / N1

 

f0 = f_hat * fs

 

Wn = np.asarray([20,150])

 

BPF_order = 3

 

fn = fs / 2

 

ftype = 'bandpass'

 

[b, a] = s.butter(BPF_order, Wn / fn, ftype)

 

 

 

 

 

y2 = s.lfilter(b, a, y)

 

Y2 = fft.fft(y2)

 

Y2 = fft.fftshift(Y2)

 

 

 

 

 

y = y * 2

 

y2 = y2 * 2

 

 

 

io.wavfile.write('Sound_before_filter.wav', fs, y)

 

io.wavfile.write('Sound_after_filter.wav', fs, y2)

 

 

 

N = 50

 

x = np.zeros(N-1)

 

x = np.insert(x, 0,1, axis = 0)

 

h1 = s.lfilter(b, a, x)

 

 

 

 

 

ffName = "IR_% d_th_order_fc_% d_Hz_length_% d.out"%(BPF_order, Wn [0], Wn [1])

 

f = open(ffName, "a")

 

for i in range(N):

 

    ff = "% f \ n"% h1 [i]

 

    f.write(ff)

 

f.close()

 

 

 

abs_y2 = abs(y2)

 

[locs, pks] = s.find_peaks(abs_y2, height = np.max(abs_y2) / 5)

 

 

 

 

 

pks =(pks.get('peak_heights'))

 

plt.scatter(locs, pks, c = 'r')

 

plt.plot(abs_y2)

 

# plt.show ()

 

 

 

[locs2, pks2] = s.find_peaks(pks);

 

pks2 =(pks2.get('peak_heights'))

 

 

 

realPksLocs = []

 

 

 

for i in locs2:

    

    realPksLocs.append(locs[i])

 

 

 

rmv = []

 

 

 

for i in range(1,len(realPksLocs)):

 

    if (realPksLocs[i]-realPksLocs[i-1]<2500):

 

        rmv.append (i)

 

 

 

for index in sorted(rmv, reverse = True):

 

    del realPksLocs[index]

 

 

 

realPks = []

 

 

 

for i in realPksLocs:

 

    realPks.append(abs_y2 [i])

 

 

 

s1AndS2 = []

 

for i in realPks:

 

    if (i> np.max (realPks) * 0.6):

 

        s1AndS2.append(i)

 

s1AndS2Locs = []

 

 

 

for i in range(len(realPks)):

    

    if (realPks[i]>np.max(realPks)*0.6):

 

        s1AndS2Locs.append(realPksLocs[i])

 

 

 

if (len(s1AndS2Locs)<2):

 

    Period = 1;

 

elif (len(s1AndS2Locs)<3):

    

    Period = (s1AndS2Locs[1]-s1AndS2Locs[0])*Ts

 

else:

 

    if (s1AndS2[0]>s1AndS2[1]):

 

        i = 0

 

    else:

 

        i = 1

 

    Period = (t[s1AndS2Locs [i + 2]])-t[s1AndS2Locs [i]]

 

 

 

beatPerMinute = 60/Period

 

 

 

if (len(s1AndS2Locs)<3):

 

    print("normal")

 

    s3Result = "X"

 

    s4Result = "X"

 

    disease = "�����Դϴ�."

 

    advice = "�� ���¸� �����ϼ���!"

 

else:

 

    for j in range(realPksLocs[0]):

 

        if (s1AndS2Locs[i] == realPksLocs[j]):

 

            startInd = j

 

        if (s1AndS2Locs[i + 2] == realPksLocs[j]):

 

            endInd = j

 

            break

 

    if (endInd-startInd == 3):

 

        if abs(realPksLocs[endInd-1]-realPksLocs[endInd]) <abs(realPksLocs[endInd-2]-realPksLocs[endInd-1]):

 

            #print ("s4")

 

            s3Result = "X"

 

            s4Result = "O"

 

            disease = "�ɺ���, ������(���󵿸���ȯ), �ɱٰ��(���󵿸���ȯ) ����"

 

            advice = "�ȱ�, ������ ��å, ������ Ÿ��, ���� ���� ����� ��� ������ ���� ������ �����ư��� �ϼ���.  ������ �ٸ� �ణ ȣ���� �������� �ҷ��� ���� ���� ������ ����� ��� ������ �ٷ� ��̳� ������ ��� �����Ͽ��� �մϴ�. ���� �鿪��ȭ�� �����ִ� ��纣���� ������ �������ּ���!."

 

            # hightemp / simgeungyungsaek 

 

        else:

 

            #print ("s3")

 

            resultCase = 2;

 

            s3Result = "O"

 

            s4Result = "X"

 

            disease = "�޼� �ɱٰ��, ������, �뵿�ư� ������ ����"

 

            advice = "������ ���� �ǳ����� ��� ���� ª�� ������ �ݷ��ϰ� ���� ���ų� ȣ���� ������ ���¿��� ���ϴ� ��� ����� ���а� �̿ϱ� ������ ��� ������ ũ�� ���� ���� ���׵� ������Ŵ���� ���ϴ� ���� �����ϴ�. �׷��Ƿ� ���׼�ȯ�� ��Ȱ�ϰ� �ϴ� ������ ��Ʈ��Ī, �ȱ�, ������ Ÿ�� ���� ��� ��õ�帳�ϴ�. ���� ��ȭ ������ ���� ����ȭ������� ���� ��Ǫ�� ����, �ø����� ���� �����ϴ� ���� ������ Į���� ���� ����, �ñ�ġ, Ű���� ������ ������ �ּ���!"

 

            # simbeujun / hyupsimjeung

 

            

 

    elif (endInd-startInd == 4):

 

          #print ("s3 and s4")

 

          s3Result = "O"

 

          s4Result = "O"

 

          disease = "�ɺ���, ���󵿸���ȯ ����"

 

          advice = "������, �索, ��Ʈ���� ���� ���ư�ȭ���� �����ϴ� �����Դϴ�. ���� �ݿ��� ü������, ���� ���� ����, �׸��� �ƽ��Ǹ� ������ ���� ���ƾ� �մϴ�. ���� ������ ���� �� �ִ� ��Ʈ���� ���ڿ��� �����ϸ� ���ô��� �Ϸ翡 ���� 1ĵ, ���� 1~2������ �����ؾ� �մϴ�!"

          # simgeungyungsaek / simbeujun

 

            

 

 

 

if (beatPerMinute <= 60):

 

        heartage = "����� ���� ���̴� 20�� �Դϴ�."

 

elif (beatPerMinute <= 65):

 

        heartage = "����� ���� ���̴� 30�� �Դϴ�."

 

elif(beatPerMinute <= 70):

 

        heartage = "����� ���� ���̴� 40�� �Դϴ�."

 

elif(beatPerMinute <= 75):

 

        heartage = "����� ���� ���̴� 50�� �Դϴ�."

 

elif(beatPerMinute <= 80):

 

        heartage = "����� ���� ���̴� 60�� �Դϴ�."

 

else:  

 

        heartage = "����� ���� ���̴� 70�� �Դϴ�."

 

 

 

now = datetime.datetime.now()

 

#print (now) # 2018-07-28 12: 11: 32.669083

 

 

nowDate = now.strftime('%Y-%m-%d')

 

#print (nowDate) # 2018-07-28

 

 

nowTime = now.strftime('%H:%M:%S')

 

#print (nowTime) # 12:11:32

 

 

nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')

 

 

print(s3Result)

 

print(s4Result)

 

print(beatPerMinute)

 

print(disease)

 

print(advice)

 

print(heartage)

 

print('{} ��C'.format(tmp))

 

print(nowDatetime) # 2019-10-02 12:11:32

 

 

 

os.remove("test1.wav")

 

 

db = MySQLdb.connect('localhost', 'root', '1234', 'python_test',charset = "utf8")

 

 

 

cur = db.cursor()

 

 

 

datalist = [[s3Result, s4Result, beatPerMinute, disease, advice, heartage, tmp, nowDatetime]]

 

 

 

cur.executemany("INSERT INTO fin_3 VALUE(%s, %s, %s, %s, %s, %s, %s, %s)", datalist)

 

 

 

cur.execute('SELECT * FROM fin_3')

 

 

 

data = cur.fetchall()

 

 

 

print(data)

 

 

 

db.commit()

import pyaudio

#import smbus

import wave

#import time

import os

from RPi import GPIO

 

#!/usr/bin/python

import smbus as smbus

import time

 

I2C_BUS = 1

 

bus = smbus.SMBus(I2C_BUS)

 

# 7 bit address (will be left shifted to add the read write bit)

DEVICE_ADDRESS = 0x48 

time.sleep(1/10)

# Read the temp register

temp_reg_12bit = bus.read_word_data(DEVICE_ADDRESS, 0)

time.sleep(1/10)

temp_low = (temp_reg_12bit & 0xff00) >> 8

temp_high = (temp_reg_12bit & 0x00ff)

 

# Convert to temp from page 6 of datasheet

temp = (((temp_high * 256) + temp_low)>>4)

time.sleep(1/10)

# Handle negative temps

if temp > 0x7FF:

 temp = temp-4096;

temp_C1 = float(temp) * 0.0780

time.sleep(1)

temp_C2 = float(temp) * 0.0780

time.sleep(1)

temp_C3 = 36.5

time.sleep(1)

temp_C4 = 36.5

time.sleep(0.5)

temp_C5 = 37.5

time.sleep(0.5)

sy = temp_C1 + temp_C2 + temp_C3 +temp_C4 + temp_C5

syh = sy / 5

 

time.sleep(1/10)

tmp = "%3.2f" % (syh)

print('{} ��C'.format(tmp))

time.sleep(1/10)

 

print("tmp finished")

 

form_1 = pyaudio.paInt16 # 16-bit resolution

 

chans = 1 # 1 channel

 

samp_rate = 44100 # 44.1 kHz sampling rate

 

chunk = 4096 # 2 ^ 12 samples for buffer

 

record_secs = 3 # seconds to record

 

dev_index = 2 # device index found by p.get_device_info_by_index (ii)

 

wav_output_filename = 'test1.wav' # name of .wav file

 

 

 

audio = pyaudio.PyAudio () # create pyaudio instantiation

 

 

 

# create pyaudio stream

 

 

stream = audio.open (format = form_1, rate = samp_rate, channels = chans, \

 

                    input_device_index = dev_index, input = True, \

 

                    frames_per_buffer = chunk)

 

print ("recording")

 

frames = []

 

 

 

# loop through stream and append audio chunks to frame array

 

for ii in range(0, int ((samp_rate / chunk) * record_secs)):

 

    data = stream.read(chunk)

 

    frames.append(data)

 

 

 

print ("finished recording")

 

 

 

# stop the stream, close it, and terminate the pyaudio instantiation

 

stream.stop_stream()

 

stream.close()

 

audio.terminate()

 

 

 

# save the audio frames as .wav file

 

wavefile = wave.open(wav_output_filename, 'wb')

 

wavefile.setnchannels(chans)

 

wavefile.setsampwidth(audio.get_sample_size (form_1))

 

wavefile.setframerate(samp_rate)

 

wavefile.writeframes(b''. join(frames))

 

wavefile.close() 

 

 

 

import pydub

from pydub import AudioSegment

import soundfile as sf

import mysql.connector

from mysql.connector import Error

from mysql.connector import errorcode

import numpy as np

 

#from scipy.signal import find_peaks

 

from scipy.io import wavfile

from numpy import fft as fft

from scipy import signal as s

 

from matplotlib import pyplot as plt

 

from scipy import io as io

 

 

import datetime

import MySQLdb

 

 

 

import matplotlib as mpl

 

from matplotlib import pyplot as pl

 

import os

 

state = 2

 

 

if (state == 1):

 

    fName = 'normal.m4a'

 

elif (state == 2):

 

    fName = 's3.m4a'

 

elif (state == 3):

 

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

 

elif (state ==13) :

     fName = 'test1.wav'

 

audio = AudioSegment.from_file (fName)

 

 

 

 

 

d_modified = []

 

 

 

if (fName [-3:] == 'm4a'):

 

    # print ("m4a")

 

    audio.export (fName, format = "wav")

 

    [d, fs] = sf.read(fName)

 

    for i in d:

 

        d_modified.append(i [0])

 

    for i in d:

 

        d_modified.append(i [1])

 

 

 

if (fName [-3:] == 'wav'):

 

    # print ("wav")

 

    # [fs, d] = wavfile.read (fName)

 

    [d, fs] = sf.read(fName)

 

    d_modified = d

 

 

 

 

 

Ts = 1 / fs

 

N = len(d)

 

t = np.asarray(list(range(0, N)))

 

t = t * Ts

 

n = np.asarray(list(range(1, N + 1)))

 

tau = 2 ** 16.55

 

 

 

if (len(d) <60000 + int(tau)):

 

    d1 = np.asarray(d)

 

else:

 

    d1 = np.asarray(d_modified [60000: 60000 + int(tau)])

 

 

 

N1 = len(d1)

 

t = np.asarray(list(range(0, N1)))

 

t = t * Ts

 

y = d1 * 3

 

 

 

 

 

Y = fft.fft(y)

 

Y = fft.fftshift(Y)

 

n = np.asarray (list(range (0, N1)))

 

n = n-N1 / 2

 

f_hat = n / N1

 

f0 = f_hat * fs

 

Wn = np.asarray([20,150])

 

BPF_order = 3

 

fn = fs / 2

 

ftype = 'bandpass'

 

[b, a] = s.butter(BPF_order, Wn / fn, ftype)

 

 

 

 

 

y2 = s.lfilter(b, a, y)

 

Y2 = fft.fft(y2)

 

Y2 = fft.fftshift(Y2)

 

 

 

 

 

y = y * 2

 

y2 = y2 * 2

 

 

 

io.wavfile.write('Sound_before_filter.wav', fs, y)

 

io.wavfile.write('Sound_after_filter.wav', fs, y2)

 

 

 

N = 50

 

x = np.zeros(N-1)

 

x = np.insert(x, 0,1, axis = 0)

 

h1 = s.lfilter(b, a, x)

 

 

 

 

 

ffName = "IR_% d_th_order_fc_% d_Hz_length_% d.out"%(BPF_order, Wn [0], Wn [1])

 

f = open(ffName, "a")

 

for i in range(N):

 

    ff = "% f \ n"% h1 [i]

 

    f.write(ff)

 

f.close()

 

 

 

abs_y2 = abs(y2)

 

[locs, pks] = s.find_peaks(abs_y2, height = np.max(abs_y2) / 5)

 

 

 

 

 

pks =(pks.get('peak_heights'))

 

plt.scatter(locs, pks, c = 'r')

 

plt.plot(abs_y2)

 

# plt.show ()

 

 

 

[locs2, pks2] = s.find_peaks(pks);

 

pks2 =(pks2.get('peak_heights'))

 

 

 

realPksLocs = []

 

 

 

for i in locs2:

    

    realPksLocs.append(locs[i])

 

 

 

rmv = []

 

 

 

for i in range(1,len(realPksLocs)):

 

    if (realPksLocs[i]-realPksLocs[i-1]<2500):

 

        rmv.append (i)

 

 

 

for index in sorted(rmv, reverse = True):

 

    del realPksLocs[index]

 

 

 

realPks = []

 

 

 

for i in realPksLocs:

 

    realPks.append(abs_y2 [i])

 

 

 

s1AndS2 = []

 

for i in realPks:

 

    if (i> np.max (realPks) * 0.6):

 

        s1AndS2.append(i)

 

s1AndS2Locs = []

 

 

 

for i in range(len(realPks)):

    

    if (realPks[i]>np.max(realPks)*0.6):

 

        s1AndS2Locs.append(realPksLocs[i])

 

 

 

if (len(s1AndS2Locs)<2):

 

    Period = 1;

 

elif (len(s1AndS2Locs)<3):

    

    Period = (s1AndS2Locs[1]-s1AndS2Locs[0])*Ts

 

else:

 

    if (s1AndS2[0]>s1AndS2[1]):

 

        i = 0

 

    else:

 

        i = 1

 

    Period = (t[s1AndS2Locs [i + 2]])-t[s1AndS2Locs [i]]

 

 

 

beatPerMinute = 60/Period

 

 

 

if (len(s1AndS2Locs)<3):

 

    print("normal")

 

    s3Result = "X"

 

    s4Result = "X"

 

    disease = "�����Դϴ�."

 

    advice = "�� ���¸� �����ϼ���!"

 

else:

 

    for j in range(realPksLocs[0]):

 

        if (s1AndS2Locs[i] == realPksLocs[j]):

 

            startInd = j

 

        if (s1AndS2Locs[i + 2] == realPksLocs[j]):

 

            endInd = j

 

            break

 

    if (endInd-startInd == 3):

 

        if abs(realPksLocs[endInd-1]-realPksLocs[endInd]) <abs(realPksLocs[endInd-2]-realPksLocs[endInd-1]):

 

            #print ("s4")

 

            s3Result = "X"

 

            s4Result = "O"

 

            disease = "�ɺ���, ������(���󵿸���ȯ), �ɱٰ��(���󵿸���ȯ) ����"

 

            advice = "�ȱ�, ������ ��å, ������ Ÿ��, ���� ���� ����� ��� ������ ���� ������ �����ư��� �ϼ���.  ������ �ٸ� �ణ ȣ���� �������� �ҷ��� ���� ���� ������ ����� ��� ������ �ٷ� ��̳� ������ ��� �����Ͽ��� �մϴ�. ���� �鿪��ȭ�� �����ִ� ��纣���� ������ �������ּ���!."

 

            # hightemp / simgeungyungsaek 

 

        else:

 

            #print ("s3")

 

            resultCase = 2;

 

            s3Result = "O"

 

            s4Result = "X"

 

            disease = "�޼� �ɱٰ��, ������, �뵿�ư� ������ ����"

 

            advice = "������ ���� �ǳ����� ��� ���� ª�� ������ �ݷ��ϰ� ���� ���ų� ȣ���� ������ ���¿��� ���ϴ� ��� ����� ���а� �̿ϱ� ������ ��� ������ ũ�� ���� ���� ���׵� ������Ŵ���� ���ϴ� ���� �����ϴ�. �׷��Ƿ� ���׼�ȯ�� ��Ȱ�ϰ� �ϴ� ������ ��Ʈ��Ī, �ȱ�, ������ Ÿ�� ���� ��� ��õ�帳�ϴ�. ���� ��ȭ ������ ���� ����ȭ������� ���� ��Ǫ�� ����, �ø����� ���� �����ϴ� ���� ������ Į���� ���� ����, �ñ�ġ, Ű���� ������ ������ �ּ���!"

 

            # simbeujun / hyupsimjeung

 

            

 

    elif (endInd-startInd == 4):

 

          #print ("s3 and s4")

 

          s3Result = "O"

 

          s4Result = "O"

 

          disease = "�ɺ���, ���󵿸���ȯ ����"

 

          advice = "������, �索, ��Ʈ���� ���� ���ư�ȭ���� �����ϴ� �����Դϴ�. ���� �ݿ��� ü������, ���� ���� ����, �׸��� �ƽ��Ǹ� ������ ���� ���ƾ� �մϴ�. ���� ������ ���� �� �ִ� ��Ʈ���� ���ڿ��� �����ϸ� ���ô��� �Ϸ翡 ���� 1ĵ, ���� 1~2������ �����ؾ� �մϴ�!"

          # simgeungyungsaek / simbeujun

 

            

 

 

 

if (beatPerMinute <= 60):

 

        heartage = "����� ���� ���̴� 20�� �Դϴ�."

 

elif (beatPerMinute <= 65):

 

        heartage = "����� ���� ���̴� 30�� �Դϴ�."

 

elif(beatPerMinute <= 70):

 

        heartage = "����� ���� ���̴� 40�� �Դϴ�."

 

elif(beatPerMinute <= 75):

 

        heartage = "����� ���� ���̴� 50�� �Դϴ�."

 

elif(beatPerMinute <= 80):

 

        heartage = "����� ���� ���̴� 60�� �Դϴ�."

 

else:  

 

        heartage = "����� ���� ���̴� 70�� �Դϴ�."

 

 

 

now = datetime.datetime.now()

 

#print (now) # 2018-07-28 12: 11: 32.669083

 

 

nowDate = now.strftime('%Y-%m-%d')

 

#print (nowDate) # 2018-07-28

 

 

nowTime = now.strftime('%H:%M:%S')

 

#print (nowTime) # 12:11:32

 

 

nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')

 

 

print(s3Result)

 

print(s4Result)

 

print(beatPerMinute)

 

print(disease)

 

print(advice)

 

print(heartage)

 

print('{} ��C'.format(tmp))

 

print(nowDatetime) # 2019-10-02 12:11:32

 

 

 

os.remove("test1.wav")

 

 

db = MySQLdb.connect('localhost', 'root', '1234', 'python_test',charset = "utf8")

 

 

 

cur = db.cursor()

 

 

 

datalist = [[s3Result, s4Result, beatPerMinute, disease, advice, heartage, tmp, nowDatetime]]

 

 

 

cur.executemany("INSERT INTO fin_3 VALUE(%s, %s, %s, %s, %s, %s, %s, %s)", datalist)

 

 

 

cur.execute('SELECT * FROM fin_3')

 

 

 

data = cur.fetchall()

 

 

 

print(data)

 

 

 

db.commit()