import os
import re
import gc
import yt_dlp
from datetime import datetime
from fastapi import HTTPException
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel, prepare_model_for_kbit_training, LoraConfig, get_peft_model
from collections import defaultdict

OUTPUT_FOLDER = "backend/output_folder"

# 1. 오디오 추출 함수
def download_audio(video_url: str):
    """유튜브 비디오에서 오디오 추출하여 output_folder에 저장"""

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)       # output_folder 생성

    # 타임스탬프 추가 (파일명 중복 방지)
    # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    audio_filename = "extracted_audio"
    audio_path = os.path.join(OUTPUT_FOLDER, audio_filename)

    # 유튜브 오디오 다운로드 옵션 설정
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": audio_path,                      # 저장될 경로 지정
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])               # 유튜브에서 오디오 다운로드
    except Exception as e:
        # print(e)
        raise HTTPException(status_code=500, detail=f"오디오 추출 실패: {str(e)}")

    return audio_path                               # 다운로드된 파일 경로 반환


# 2. 텍스트 변환 pipeline 구조 작성
def load_asr_pipeline(model_id: str, torch_dtype,  device: str):
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id,
        torch_dtype=torch_dtype,
        low_cpu_mem_usage=True,
        use_safetensors=True
    )
    model.to(device)
    processor = AutoProcessor.from_pretrained(model_id)
    
    asr_pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        torch_dtype=torch_dtype, #torch.float16,
        device=device,
    )
    return asr_pipe

# 3. 문장 완성도 구조화 함수
def remove_extra_repeated_words(text: str) -> str:
    """
    동일한 한글 단어가 3번 이상 반복될 경우 2개만 남기고 나머지 삭제
    (숫자 및 특수문자는 유지)
    """
    word_count = defaultdict(int)
    word_positions = {}
    
    for match in re.finditer(r"[가-힣]+", text):
        word = match.group()
        word_count[word] += 1
        word_positions.setdefault(word, []).append(match.start())
    
    result = list(text)
    for word, positions in word_positions.items():
        if word_count[word] > 2:
            for i in range(2, len(positions)):
                start_idx = positions[i]
                for j in range(len(word)):
                    result[start_idx + j] = ""
    return "".join(result)

# 4. GPU 초기화 함수
def initialize_gpu():
    """
    GPU 캐시, IPC, 가비지 컬렉션 실행 후 GPU 동기화 및 초기화
    """
    torch.cuda.empty_cache()
    torch.cuda.ipc_collect()
    gc.collect()
    torch.cuda.synchronize()
    # os.system("nvidia-smi --gpu-reset")  # 필요시 주석 해제 (관리자 권한 필요)


# 5. Summary Text 함수
def load_model_and_tokenizer():
    BASE_MODEL = "google/gemma-2b-it"
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16
    )
    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        quantization_config=bnb_config,
        device_map={"": torch.cuda.current_device()}
    )
    base_model = prepare_model_for_kbit_training(base_model)
    torch.cuda.empty_cache()    
    model = PeftModel.from_pretrained(base_model, "backend/models/lora_adapters_ver1_law")
    model.eval()

    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    return model, tokenizer

def post_process(text):
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'!{2,}', '!', text)
    return text

def get_generation_kwargs():
    return {
        "max_length": 4096,
        "min_length": 512,
        "do_sample": False,
        "temperature": 0.5,
        "top_k": 50,
        "top_p": 0.95,
    }

def get_detailed_prompt():
    return """
    After reading the original text below, please perform the following steps in order:

    1. Translate the original text into English.
    2. Summarize the translated text by extracting only the most important core points. Present each key point as a numbered item (for example, "1.", "2.", "3.", etc.). Write each point concisely and clearly.
    3. Finally, translate the numbered summary into Korean.

    Important:
    - The final output must be only the summary in Korean.
    - Use simple and direct language.
    - Do not include any extra commentary, notes, or repeated information.
    - Each numbered point must be on a separate line and end with a period.
    - Do not include any bullet symbols (such as "*" or "-").
    - Do not write '**Note:**'
    - Do not include any notes, disclaimers, or additional comments. Only output the summary.
    - Do not write any 'Note:'
    - Avoid duplication of word

    Original Text:
    {original_text}

    Summary:
    """