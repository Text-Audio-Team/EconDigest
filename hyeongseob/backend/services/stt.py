import torch
from fastapi import APIRouter
from backend.utils import initialize_gpu, load_asr_pipeline, remove_extra_repeated_words

stt_router = APIRouter(prefix="/stt", tags=["Audio-to-Text"])

@stt_router.post("/conversion")
def audio_conversion_to_text():
    # gpu reset
    initialize_gpu()

    # default
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 

    # model select
    model_id = "openai/whisper-large"
    asr_pipe = load_asr_pipeline(model_id, torch_dtype, device)
    generate_kwargs = {
        "max_new_tokens": 445,
        "num_beams": 1,
        "condition_on_prev_tokens": False,
        "compression_ratio_threshold": 1.35,
        "temperature": (0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
        "logprob_threshold": -1.0,
        "no_speech_threshold": 0.6,
        "return_timestamps": True,
    }
    
    # 오디오 파일 경로
    audio_path = "backend/output_folder/extracted_audio.mp3"
    # language 옵션을 generate_kwargs에 포함하지 않고, 파이프라인 내부에서 설정하게 함(핵심)
    result = asr_pipe(audio_path, generate_kwargs={"language": "korean"}, return_timestamps=True)
    
    test_text = result.get("text", "")
    cleaned_text = remove_extra_repeated_words(test_text)
    print("처리된 텍스트:", cleaned_text)
    
    output_file = "backend/output_folder/conversion_text.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(cleaned_text)
    print(f"텍스트가 '{output_file}'에 저장되었습니다.")

    return {"conversion_text" : cleaned_text}
