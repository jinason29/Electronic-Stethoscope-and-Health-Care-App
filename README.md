# Electronic_stethoscope

프로젝트 소개


사용자의 호흡, 맥박, 체온에 대한 정보를 통해 병원에 자주 가기 어려운 심, 폐질환 환자들의 건강관리를 돕기 위한 심박수, 심장나이, 예상 질병, 체온의 정보를 제공하고 전용 Application으로 적절한 의료 행위를 취할 수 있도록 사용자별 건강정보를 제공합니다. 

================================================================================
수행 내용


Raspberry Pi로 vital sign(호흡수, 체온, 심장박동)측정 및 수집
측정한 심음 데이터를 Python으로 전송
제 1-4 심음에 따라 비정상 신호 판별 (S3, S4)
심음의 주기와 특성 분석
vital sign 데이터를 [심박수, 심장나이, 예상 질병, 체온]에 대한 정보로 변환하여 DB에 전송
DB에 저장된 개인 질병 데이터를 Application으로 보내 출력
