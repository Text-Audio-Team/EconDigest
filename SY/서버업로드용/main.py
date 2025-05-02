#!/usr/bin/env python3
import os
from gpu_utils import initialize_gpu
from asr_model import load_asr_pipeline
from text_utils import remove_extra_repeated_words

def main():
    # GPU 초기화
    initialize_gpu()
    device = "cuda:0" if __import__("torch").cuda.is_available() else "cpu"
    torch_dtype = __import__("torch").float16 if __import__("torch").cuda.is_available() else __import__("torch").float32

    model_id = "openai/whisper-small"
    asr_pipe = load_asr_pipeline(model_id, device, torch_dtype)

    # 음성 인식 설정 (forced_decoder_ids를 생략하여 내부 language 옵션 사용)
    generate_kwargs = {
        "max_new_tokens": 445,
        "num_beams": 1,
        "condition_on_prev_tokens": False,
        "compression_ratio_threshold": 1.35,
        "temperature": (0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
        "logprob_threshold": -1.0,
        "no_speech_threshold": 0.6,
        "return_timestamps": True,
        # language 옵션은 내부적으로 처리하도록 합니다.
    }
    
    # 오디오 파일 경로
    audio_path = r"/home/wanted-1/potenup-workspace/Project/project3/team2/SY/서버업로드용/output_folder/영상 오디오 추출 자료_01.mp3"
    # language 옵션을 generate_kwargs에 포함하지 않고, 파이프라인 내부에서 설정하게 함.
    result = asr_pipe(audio_path, generate_kwargs={"language": "korean"}, return_timestamps=True)
    
    test_text = result.get("text", "")
    cleaned_text = remove_extra_repeated_words(test_text)
    print("처리된 텍스트:", cleaned_text)
    
    output_file = "processed_text.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(cleaned_text)
    print(f"최종 텍스트가 '{output_file}'에 저장되었습니다.")

if __name__ == '__main__':
    main()
