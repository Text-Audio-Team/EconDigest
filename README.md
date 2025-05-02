# AI 기반 경제 유튜브 영상 요약 문서화 서비스  
### 팀원  
- 김형섭  
- 지서연  
- 이승재

---

## 1. 프로젝트 개요  
경제·재테크 관련 유튜브 영상과 팟캐스트를 대상으로, 음성→텍스트 변환(Whisper 기반)과 요약(BART/T5 기반)을 통해 핵심 내용을 빠르게 확인할 수 있는 웹 서비스입니다.  
- **메인 타깃**: 경제 정보가 낯선 시니어층  
- **서브 타깃**: 바쁜 직장인·학생  

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

## 5. 서비스 화면
> _아래 위치에 캡처 이미지를 `/assets` 폴더에 넣고 링크를 걸어 주세요._  
- **메인 화면**  
  ![메인화면 예시](/assets/screenshot_main.png)  
- **변환 원문 보기**  
  ![원문확장 예시](/assets/screenshot_raw.png)  
- **최종 요약 보기**  
  ![요약확장 예시](/assets/screenshot_summary.png)  

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