clear ;
state = 4;%���⿡�� ��ȣ������ �����ϼ���.
% ���� ������ �о����

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


% ���� ������ �ð��࿡�� �׷��� �׸���
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


% ���� �����Ϳ��� �Ϻ� ������ �߶󳻱�
tau = 2^16.55 ; % 2��
d1 = d(60000:60000+tau-1) ; %(:) ����� �����κи� ����
N1 = length(d1) ;
t = [0:N1-1]*Ts ;
n = 1:N1 ;

% �߶� �κи� �׷��� �׸���
subplot(212)
plot(t, d1) ;

% ������ �Ҹ��� �۾� 3�� ������Ű��
y = 3*d1 ;

% ����. �Ʒ� ������ �ּ��� Ǯ�� �����ϸ� �Ҹ��� ����
sound( 3*d1, fs )

% ����ȣ�� ���ļ� �м��ϱ�
Y = fftshift(fft(y)) ;
n = [0:N1-1]-N1/2 ;
f_hat = n/N1 ;
f0 = fs * f_hat ;

% ���ļ� �м� ����� �׷����� ǥ���ϱ�
figure(2)
subplot(111)
plot( f0, abs(Y) ) ;
grid on ;
xlim([0 500]) ;
xlabel('Original Signal Frequency [Hz]');
ylabel('Magnitude spectrum') ;

% n�� ������ ���Ϳ��� BPF �����ϱ�
Wn=[20, 150];
BPF_order = 3; %3�̻��ϸ� �� ��� x
fn=fs/2;
ftype='bandpass';
[b,a]=butter(BPF_order, Wn/fn, ftype);

y2=filter(b, a, y);
Y2 = fftshift(fft(y2)) ;
% ���� ����� ��ȣ�� ����Ʈ���� �׷����� ǥ��
figure(3)
subplot(111)
plot( f0, abs(Y2) ) ;
grid on ;
xlim([0 500]) ;
xlabel('Filtered Signal Frequency [Hz]');
ylabel('Magnitude spectrum') ;

% ��ȣ�� ũ�⸦ �ι� ����
y = 2*y ;
y2 = 2*y2 ; % Signal after filter

% ���Ϸ� ����
audiowrite( 'Sound_before_filter.wav', y, fs ) ;
audiowrite( 'Sound_after_filter.wav', y2, fs ) ;

% % ���� ���� ������ ��ȣ�� �ð��������� ��
% figure(3)
% plot( t, y, '-.', t, y2 ) ;
% grid on ;
% xlim([0 0.5]) ;
% xlabel('time [sec]') ;
% ylabel('Audio signal') ;
% legend('Before filtering', 'After filtering') ;

% ������ ���޽� ���� ���ϱ�, ������ ���� ���ʹ� IIR �����̹Ƿ� FIR ���ͷ� ����� ���� ���޽� ������ �ʹ� N���� �߶�
% ����Ѵ�. ������ ������ �����Ҽ��� ���޽� ���䵵 �����
N = 50 ; % ���޽� ������ ���� ����, ���޽� ������ ���̴� ����� ���� ��
x = [1 zeros(1,N-1)] ;
h1 = filter( b, a, x ) ;

% % ������ ���� N���� ���޽� ���� �׷����� ǥ��
% figure(5)
% stem( 0:N-1, h1, 'filled' ) ;
% xlabel('n') ;
% ylabel('Impulse response h[n]') ;

% ���޽� ���� ���Ϸ� ����
% �� ���͸� ������ �����ϱ� ���ؼ��� ���� �Է� ��ȣ�� �� ���޽� ����� ��������� ���ϸ� �ȴ�.
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


%�ֱ�(s1~s1����)�� ã�Ƽ� 1�п� �� ���� �ֱⰡ �ݺ��Ǵ��� üũ�Ͽ� �ɹڼ��� ���ؾ� �Ѵ�. (�� �ֱ� x 60)
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
beatPerMinute = 60 / Period % �д� Beat

% S3�� S4�� üũ�մϴ�.
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
           % S3 or S4�� S1���� �Ÿ��� �� ���� ��쿡
            disp("s4")
            s3Result = "S3: X";
            s4Result = "S4: O";
            disease = "Acute Myocardial Infarction, Hypertension or Aortic Stenos is expected.";
            c = newline;
            % �ɱٰ��
            advice = "For the patients who are suffering from myocardial infarction or acute myocardial infarction , it would be nessesary avoiding foods with high levels of cholesterol. Furthermore forming habits with balanced diet are recommended.";
            % ������
            advice = advice + newline + "For hypertension patients, having low salt and potassium contained food are recommended. Moreover, starting a simple exercise after dinner and reducing drinking and smoking are very crucial to them.";
            % �뵿�� ������
            advice = advice + newline + "Moreover they need to avoid from severe psychological Stress.";
        else
            disp("s3")
            resultCase = 2;
            s3Result = "S3: O";
            s4Result = "S4: X";
            disease = "Cardiac Insufficiency, Angina Pector or Myocardial Infarction is expected.";
            % �ɺ�����
            advice ="For patients who suffer from cardiac insufficiency, exercising aerobic yet avoiding from muscular exercises are suggested.";
            % ������
            advice = advice + newline + "For the patients who suffer from angina pectoris,stretching lightly, taking care about body temperature in cold weather, eating foods consisted with low-salt, and controlling weights are crucial. Furthermore, quitting smoking would be helpful either.";
        end

    elseif endInd - startInd == 4
        disp("s3 and s4")
        s3Result = "S3: O";
        s4Result = "S4: O";
        disease = "Coronary Disease or Cardiac Insufficiency is expected.";
        % �ɱٰ��
        advice = "For the patients who are suffering from myocardial infarction or acute myocardial infarction , it would be nessesary avoiding foods with high levels of cholesterol. Furthermore forming habits with balanced diet are recommended.";
        % �ɺ���
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
