clear ;
state = 4;%여기에서 신호파일을 선택하세요.
% 원본 데이터 읽어오기

switch state
    case 1
        [d, fs] = audioread('normal.m4a');
    case 2
        [d, fs] = audioread('s3.m4a');
    case 3
        [d, fs] = audioread('s4.m4a'); % 2
    case 4
        [d, fs] = audioread('s3 and s4.m4a'); % 4
end


% 원본 데이터 시간축에서 그래프 그리기
Ts = 1/fs ;
N = length(d) ;
t = [0:N-1]*Ts ;
n = 1:N ;

figure(1)
subplot(211)
plot( t, d ) ;
% subplot(312)
% plot( n, d ) ;
% grid on ;


% 원본 데이터에서 일부 구간만 잘라내기
tau = 2^16.55 ; % 2초
d1 = d(60000:60000+tau-1) ; %(:) 행렬의 일정부분만 선택
N1 = length(d1) ;
t = [0:N1-1]*Ts ;
n = 1:N1 ;

% 잘라낸 부분만 그래프 그리기
subplot(212)
plot(t, d1) ;

% 원본의 소리가 작아 3배 증폭시키기
y = 3*d1 ;

% 들어보기. 아래 문장의 주석을 풀고 실행하면 소리가 나옴
sound( 3*d1, fs )

% 원신호의 주파수 분석하기
Y = fftshift(fft(y)) ;
n = [0:N1-1]-N1/2 ;
f_hat = n/N1 ;
f0 = fs * f_hat ;

% 주파수 분석 결과를 그래프로 표시하기
figure(2)
subplot(111)
plot( f0, abs(Y) ) ;
grid on ;
xlim([0 500]) ;
xlabel('Original Signal Frequency [Hz]');
ylabel('Magnitude spectrum') ;

% n차 디지털 버터워스 BPF 설계하기
Wn=[20, 150];
BPF_order = 3; %3이상하면 값 출력 x
fn=fs/2;
ftype='bandpass';
[b,a]=butter(BPF_order, Wn/fn, ftype);

y2=filter(b, a, y);
Y2 = fftshift(fft(y2)) ;
% 필터 통과한 신호의 스펙트럼을 그래프에 표시
figure(3)
subplot(111)
plot( f0, abs(Y2) ) ;
grid on ;
xlim([0 500]) ;
xlabel('Filtered Signal Frequency [Hz]');
ylabel('Magnitude spectrum') ;

% 신호의 크기를 두배 증폭
y = 2*y ;
y2 = 2*y2 ; % Signal after filter

% 파일로 저장
audiowrite( 'Sound_before_filter.wav', y, fs ) ;
audiowrite( 'Sound_after_filter.wav', y2, fs ) ;

% % 필터 적용 전후의 신호를 시간영역에서 비교
% figure(3)
% plot( t, y, '-.', t, y2 ) ;
% grid on ;
% xlim([0 0.5]) ;
% xlabel('time [sec]') ;
% ylabel('Audio signal') ;
% legend('Before filtering', 'After filtering') ;

% 필터의 임펄스 응답 구하기, 위에서 구한 필터는 IIR 필터이므로 FIR 필터로 만들기 위해 임펄스 응답의 초반 N개를 잘라서
% 사용한다. 필터의 차수가 증가할수록 임펄스 응답도 길어짐
N = 50 ; % 임펄스 응답의 길이 조절, 임펄스 응답의 길이는 충분히 길어야 함
x = [1 zeros(1,N-1)] ;
h1 = filter( b, a, x ) ;

% % 위에서 구한 N개의 임펄스 응답 그래프로 표시
% figure(5)
% stem( 0:N-1, h1, 'filled' ) ;
% xlabel('n') ;
% ylabel('Impulse response h[n]') ;

% 임펄스 응답 파일로 저장
% 이 필터를 실제로 적용하기 위해서는 임의 입력 신호와 이 임펄스 응답과 컨볼루션을 구하면 된다.
fname = sprintf('IR_%d_th_order_fc_%d_Hz_length_%d.out', BPF_order, Wn, N ) ;
fp = fopen( fname, 'w' ) ;
for k=1:N
    fprintf(fp, '%f\n', h1(k) ) ;
end
fclose(fp) ;



figure(4);
subplot(2,1,1);
plot(t,y2);
subplot(2,1,2);
abs_y2 = abs(y2); 
plot(t, abs_y2);

%% Find Pulse Peaks
findpeaks(abs_y2, 'MinPeakHeight',max(abs_y2)/5);
[pks, locs]= findpeaks(abs_y2, 'MinPeakHeight',max(abs_y2)/5);
[pks2, locs2] = findpeaks(pks);
realPksLocs = locs(locs2);

%% Remove ripples from peaks ( within 0.05 sec )
rmv = [];
for i = 2:length(realPksLocs)
    if realPksLocs(i) - realPksLocs(i-1) < 2500
        rmv = [rmv, i];
    end
end
realPksLocs(rmv) = [];
length(realPksLocs);

%% Find S1 Peak


%주기(s1~s1까지)를 찾아서 1분에 몇 번의 주기가 반복되는지 체크하여 심박수도 구해야 한다. (총 주기 x 60)
realPks = abs_y2(realPksLocs); %% S1~S4 Peaks
s1AndS2 = realPks(realPks > max(realPks) * 0.6); %% Find S1 and S2 Signals Only
s1AndS2Locs = realPksLocs(realPks > max(realPks) * 0.6);    

if length(s1AndS2Locs)  < 3
    Period = (s1AndS2Locs(2)-s1AndS2Locs(1))*Ts;
else
    if s1AndS2(1) > s1AndS2(2)
       i = 1;
    else
       i = 2;
    end
    % i : S1 Signal start
    Period = (t(s1AndS2Locs(i+2))-t(s1AndS2Locs(i)));
end
beatPerMinute = 60 / Period % 분당 Beat

% S3와 S4를 체크합니다.
if length(s1AndS2Locs)  < 3
    disp("Normal")
    s3Result = "S3: X";
    s4Result = "S4: X";
    disease = "normal";
    advice = "Stay healthy";
else
    for j = 1:realPksLocs
        if s1AndS2Locs(i) == realPksLocs(j)
            startInd = j;
        end
        if s1AndS2Locs(i+2) == realPksLocs(j)
            endInd = j;
            break
        end
    end
    if endInd - startInd == 3
        if abs(realPksLocs(endInd-1) - realPksLocs(endInd)) < abs(realPksLocs(endInd-2) - realPksLocs(endInd-1))
           % S3 or S4가 S1과의 거리가 더 작은 경우에
            disp("s4")
            s3Result = "S3: X";
            s4Result = "S4: O";
            disease = "Acute Myocardial Infarction, Hypertension or Aortic Stenos is expected.";
            c = newline;
            % 심근경색
            advice = "For the patients who are suffering from myocardial infarction or acute myocardial infarction , it would be nessesary avoiding foods with high levels of cholesterol. Furthermore forming habits with balanced diet are recommended.";
            % 고혈압
            advice = advice + newline + "For hypertension patients, having low salt and potassium contained food are recommended. Moreover, starting a simple exercise after dinner and reducing drinking and smoking are very crucial to them.";
            % 대동관 협착증
            advice = advice + newline + "Moreover they need to avoid from severe psychological Stress.";
        else
            disp("s3")
            resultCase = 2;
            s3Result = "S3: O";
            s4Result = "S4: X";
            disease = "Cardiac Insufficiency, Angina Pector or Myocardial Infarction is expected.";
            % 심부전증
            advice ="For patients who suffer from cardiac insufficiency, exercising aerobic yet avoiding from muscular exercises are suggested.";
            % 협심증
            advice = advice + newline + "For the patients who suffer from angina pectoris,stretching lightly, taking care about body temperature in cold weather, eating foods consisted with low-salt, and controlling weights are crucial. Furthermore, quitting smoking would be helpful either.";
        end

    elseif endInd - startInd == 4
        disp("s3 and s4")
        s3Result = "S3: O";
        s4Result = "S4: O";
        disease = "Coronary Disease or Cardiac Insufficiency is expected.";
        % 심근경색
        advice = "For the patients who are suffering from myocardial infarction or acute myocardial infarction , it would be nessesary avoiding foods with high levels of cholesterol. Furthermore forming habits with balanced diet are recommended.";
        % 심부전
        advice = advice + newline + "For patients who suffer from cardiac insufficiency, exercising aerobic yet avoiding from muscular exercises are suggested.";
    end
end
    
if  beatPerMinute < 60 
    heartage = "Your heart age is around 20s."
elseif  beatPerMinute <= 65
    heartage = "Your heart age is around 30s."
elseif  beatPerMinute <= 70
    heartage = "Your heart age is around 40s." 
elseif  beatPerMinute <= 75
    heartage = "Your heart age is around 50s."
elseif  beatPerMinute <= 80
    heartage = "Your heart age is around 60s."
else  
    heartage = "Your heart age is around 70s."
end
    
datasource = 'test';
conn = database(datasource,'','');
tablename = 'user_record';
txt = datestr(now, 'yyyy-mm-dd HH:MM:SS')
records = sqlread(conn,tablename);

data = table(s3Result,s4Result,beatPerMinute,disease,txt,heartage,advice, ...
    'VariableNames',{ 'S3' ...
    'S4' 'BPM' 'disease' 'time' 'Heartage' 'Advice'});
sqlwrite(conn,tablename,data);
