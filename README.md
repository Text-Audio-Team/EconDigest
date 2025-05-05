# Economic Digest
## AI 기반 경제 유튜브 영상 요약 문서화 서비스  
**역할 구성**  
- 팀장 : 김형섭(hyeongseob)  
- 팀원 : 지서연(SY)
- 팀원 : 이승재(SJ)

---

## 1. 프로젝트 개요  
**“경제 유튜브, 핵심만 보자!”**
해당 서비스는 금융·재테크 정보를 찾기 위해 방대한 영상을 일일이 시청할 필요 없이,
클릭 한 번으로 요약 보고서를 받아볼 수 있는 AI 웹 애플리케이션입니다. 


### 과제 해결
- “중요한 구간을 놓쳤다”  
- “전문 용어가 어려워 이해가 안 된다”  
- “긴 영상 다 보기가 부담스러워요” 


### 솔루션 요약 
- **오디오 추출**: 유튜브·팟캐스트에서 고음질 음성만 분리
- **Whisper 기반 ASR**: 정확한 한글·영어 자막 생성
- **Gemini 기반 요약**: 핵심 문장·통계·인사이트를 번호 목록으로 깔끔하게 정리 


### 대상 고객
- AI·금융 비전문가인 시니어층
- 쉽고 직관적인 인터페이스로 경제 뉴스를 빠르게 습득 


### 서브 타깃
- 바쁜 직장인·학생
- 짧은 시간에 중요한 내용만 빠르게 파악  


**이제 번거로운 영상 감상 없이, 꼭 알아야 할 경제 인사이트만 빠르게 확인 할 수 있습니다**


- <a href = "https://www.canva.com/design/DAGgAvj-nkA/yyMAhf4EtcO8BrEba_aiuA/view?utm_content=DAGgAvj-nkA&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=hb6bc8602bc"> 프로젝트 발표 자료 </a>
---

## 2. 주요 기능  
1. **영상 URL 입력**  
   - 유튜브 링크를 텍스트 박스에 붙여넣기  
2. **오디오 추출 및 변환**  
   - `yt_dlp` + FFmpeg 로 음성 추출 → Transformers 기반 Whisper ASR 파이프라인으로 텍스트 변환  
3. **핵심 요약 생성**  
   - GenAI 기반 Gemini Model을 사용하여 변환 텍스트를 요약 텍스트로 재가공 
   - 영어 번역 → 요약 → 한글 번역 후 깔끔한 번호형 문장 출력  
4. **PDF/Markdown 다운로드**  
   - 완성된 요약을 PDF 형식으로 저장
5. **실시간 피드백 & 스타일링**  
   - Streamlit UI에서 버튼 클릭 한 번으로 전체 파이프라인 실행  
   - 배경컬러·버튼·입력창 CSS 커스터마이징

---

## 3. 기술 스택  
- **음성 처리**:  
  - yt_dlp · FFmpeg · OpenAI Whisper  
- **요약 모델**:  
  - Hugging Face Gemini-7b, Gemini-2b 계열 + QLoRA Fine-Tuning 진행
- **백엔드**:  
  - FastAPI (음성 추출·텍스트 변환·요약 REST API)  
  - Python 3.11 · PyTorch 2.5.1 · Transformers 4.48.0 · PEFT (LoRA)  
- **프론트엔드**:  
  - Streamlit (단일 버튼 UI · 커스텀 CSS)  
- **기타**:  
  - Git/GitHub

---

## 4. 사용자 시나리오  
1. **로그인 없이** 메인 페이지 접근  
2. 영상 URL 입력(복사 후 붙여넣기) → “영상 요약하기” 버튼 클릭  
3. 오디오 추출 → 텍스트 변환 → 요약 생성 순차 처리
4. 중간 단계(변환 원문, 완전 요약)를 확장(expander) 패널에서 확인  
5. “다운로드” 버튼으로 요약문 PDF 저장  

---

## 5. 서비스 화면 스크린샷
### 서비스 시작화면
![서비스 화면 #1](/assets/image_frontend_screenshot0.png)

### 유튜브 링크 입력 후 영상 요약 버튼 클릭화면
![서비스 화면 #2](/assets/image_frontend_screenshot1_1.png)

### 오디오 추출 및 텍스트 변환 화면
![서비스 화면 #3](/assets/image_frontend_screenshot2.png)

### 요약 텍스트 변환 화면
<p align="center">
  <img src="/assets/image_frontend_screenshot3.png" alt="영상 내용 요약 전문">
</p>

### 요약 텍스트 PDF 다운로드
- 요약 기능의 미흡부분 개선 후 고도화 예정
---

## 6. 설치 및 실행 방법

### 로컬 개발 환경  
1. 저장소 클론  
```
bash
git clone https://github.com/Text-Audio-Team/EconDigest.git
cd EconDigest
```


2. 가상환경 생성 및 패키지 설치
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. 백엔드 실행
```
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

4. 프론트엔드 실행
```
cd frontend
streamlit run streamlit.py
```

### 문의  
- 이메일: rukais2294@gmail.com
- KakaoTalk ID : KeemHS91
