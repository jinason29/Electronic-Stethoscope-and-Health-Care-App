
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

print('{} °C'.format(tmp))

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

 

    disease = "정상입니다."

 

    advice = "현 상태를 유지하세요!"

 

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

 

            disease = "심부전, 협심증(관상동맥질환), 심근경색(관상동맥질환) 예상"

 

            advice = "걷기, 가벼운 산책, 자전거 타기, 수영 등의 유산소 운동을 고강도와 보통 강도로 번갈아가며 하세요.  가슴이 뛰며 약간 호흡이 가빠지고 소량의 땀이 나는 적당한 유산소 운동은 좋지만 근력 운동이나 과격한 운동은 지양하여야 합니다. 또한 면역강화를 시켜주는 블루베리를 꾸준히 섭취해주세요!."

 

            # hightemp / simgeungyungsaek 

 

        else:

 

            #print ("s3")

 

            resultCase = 2;

 

            s3Result = "O"

 

            s4Result = "X"

 

            disease = "급성 심근경색, 고혈압, 대동맥관 협착증 예상"

 

            advice = "역도나 씨름 실내골프 등과 같이 짧은 순간에 격렬하게 힘을 쓰거나 호흡을 정지한 상태에서 행하는 운동은 수축기 혈압과 이완기 혈압의 상승 반응이 크고 말초 혈관 저항도 증가시킴으로 피하는 것이 좋습니다. 그러므로 혈액순환을 원활하게 하는 가벼운 스트레칭, 걷기, 자전거 타기 등의 운동을 추천드립니다. 또한 포화 지방이 적고 불포화지방산이 많은 등푸른 생선, 올리브유 등을 섭취하는 것이 좋으며 칼륨이 많은 부추, 시금치, 키위를 꾸준히 섭취해 주세요!"

 

            # simbeujun / hyupsimjeung

 

            

 

    elif (endInd-startInd == 4):

 

          #print ("s3 and s4")

 

          s3Result = "O"

 

          s4Result = "O"

 

          disease = "심부전, 관상동맥질환 예상"

 

          advice = "고혈압, 당뇨, 스트레스 등이 동맥경화증을 재촉하는 요인입니다. 따라서 금연과 체중조절, 정상 혈압 유지, 그리고 아스피린 복용을 잊지 말아야 합니다. 또한 혈압을 높일 수 있는 나트륨과 알코올을 지양하며 마시더라도 하루에 맥주 1캔, 소주 1~2잔으로 제한해야 합니다!"

          # simgeungyungsaek / simbeujun

 

            

 

 

 

if (beatPerMinute <= 60):

 

        heartage = "당신의 심장 나이는 20대 입니다."

 

elif (beatPerMinute <= 65):

 

        heartage = "당신의 심장 나이는 30대 입니다."

 

elif(beatPerMinute <= 70):

 

        heartage = "당신의 심장 나이는 40대 입니다."

 

elif(beatPerMinute <= 75):

 

        heartage = "당신의 심장 나이는 50대 입니다."

 

elif(beatPerMinute <= 80):

 

        heartage = "당신의 심장 나이는 60대 입니다."

 

else:  

 

        heartage = "당신의 심장 나이는 70대 입니다."

 

 

 

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

 

print('{} °C'.format(tmp))

 

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

print('{} °C'.format(tmp))

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

 

    disease = "정상입니다."

 

    advice = "현 상태를 유지하세요!"

 

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

 

            disease = "심부전, 협심증(관상동맥질환), 심근경색(관상동맥질환) 예상"

 

            advice = "걷기, 가벼운 산책, 자전거 타기, 수영 등의 유산소 운동을 고강도와 보통 강도로 번갈아가며 하세요.  가슴이 뛰며 약간 호흡이 가빠지고 소량의 땀이 나는 적당한 유산소 운동은 좋지만 근력 운동이나 과격한 운동은 지양하여야 합니다. 또한 면역강화를 시켜주는 블루베리를 꾸준히 섭취해주세요!."

 

            # hightemp / simgeungyungsaek 

 

        else:

 

            #print ("s3")

 

            resultCase = 2;

 

            s3Result = "O"

 

            s4Result = "X"

 

            disease = "급성 심근경색, 고혈압, 대동맥관 협착증 예상"

 

            advice = "역도나 씨름 실내골프 등과 같이 짧은 순간에 격렬하게 힘을 쓰거나 호흡을 정지한 상태에서 행하는 운동은 수축기 혈압과 이완기 혈압의 상승 반응이 크고 말초 혈관 저항도 증가시킴으로 피하는 것이 좋습니다. 그러므로 혈액순환을 원활하게 하는 가벼운 스트레칭, 걷기, 자전거 타기 등의 운동을 추천드립니다. 또한 포화 지방이 적고 불포화지방산이 많은 등푸른 생선, 올리브유 등을 섭취하는 것이 좋으며 칼륨이 많은 부추, 시금치, 키위를 꾸준히 섭취해 주세요!"

 

            # simbeujun / hyupsimjeung

 

            

 

    elif (endInd-startInd == 4):

 

          #print ("s3 and s4")

 

          s3Result = "O"

 

          s4Result = "O"

 

          disease = "심부전, 관상동맥질환 예상"

 

          advice = "고혈압, 당뇨, 스트레스 등이 동맥경화증을 재촉하는 요인입니다. 따라서 금연과 체중조절, 정상 혈압 유지, 그리고 아스피린 복용을 잊지 말아야 합니다. 또한 혈압을 높일 수 있는 나트륨과 알코올을 지양하며 마시더라도 하루에 맥주 1캔, 소주 1~2잔으로 제한해야 합니다!"

          # simgeungyungsaek / simbeujun

 

            

 

 

 

if (beatPerMinute <= 60):

 

        heartage = "당신의 심장 나이는 20대 입니다."

 

elif (beatPerMinute <= 65):

 

        heartage = "당신의 심장 나이는 30대 입니다."

 

elif(beatPerMinute <= 70):

 

        heartage = "당신의 심장 나이는 40대 입니다."

 

elif(beatPerMinute <= 75):

 

        heartage = "당신의 심장 나이는 50대 입니다."

 

elif(beatPerMinute <= 80):

 

        heartage = "당신의 심장 나이는 60대 입니다."

 

else:  

 

        heartage = "당신의 심장 나이는 70대 입니다."

 

 

 

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

 

print('{} °C'.format(tmp))

 

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