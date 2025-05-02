import torch
import os
import re
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel, prepare_model_for_kbit_training, LoraConfig, get_peft_model

# GPU 0 으로 강제 설정
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# 모델 불러오기 
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

model = PeftModel.from_pretrained(base_model, "/home/wanted-1/potenup-workspace/Project/project3/team2/SY/Gemma/path/to/save/lora_adapters_ver1_law")
model.eval()  

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# 하이퍼파라미터 조정
generation_kwargs = {
    "max_length": 4096,           # 최대 생성 토큰 수 (요약 길이 제한)
    "min_length": 512,            # 최소 생성 토큰 수
    "do_sample": True,           # 샘플링 방식 사용
    "temperature": 0.5,          # 낮은 값은 결정론적, 높은 값은 다양성 증가
    "top_k": 50,                 # 상위 k개 단어 내에서 샘플링
    "top_p": 0.95,               # 누적 확률 p 내 단어에서 샘플
}

# 텍스트 파일 경로 수정
txt_file_path = "/home/wanted-1/potenup-workspace/Project/project3/team2/SY/Gemma/processed_text.txt"  # 파일 경로를 수정하세요.
with open(txt_file_path, "r", encoding="utf-8") as f:
    original_text = f.read()

# 프롬프트 
detailed_prompt = """
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

# 프롬프트 구성
prompt = detailed_prompt.format(original_text=original_text)

#  요약 생성
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
with torch.no_grad():
    output_tokens = model.generate(**inputs, **generation_kwargs)

# 후처리 
def post_process(text):
    # 앞뒤 공백 제거
    text = text.strip()
    # 불필요한 공백, 줄바꿈, 중복 문장 부호 제거 (예시: 느낌표, 공백 등)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'!{2,}', '!', text)
    return text

generated_text = tokenizer.decode(output_tokens[0], skip_special_tokens=True)
# 4. "Summary:" 이후의 텍스트만 추출하여 순수 요약문만 저장
if "Summary:" in generated_text:
    summary_only = generated_text.split("Summary:")[-1].strip()
else:
    summary_only = generated_text.strip()

# "Note:"가 있다면, 그 뒤의 모든 텍스트를 제거
if "Note:" in summary_only:
    summary_only = summary_only.split("Note:")[0].strip()


# .txt 파일로 저장 
with open("generated_summary.txt", "w", encoding="utf-8") as f:
    f.write(summary_only)

print("Summary Only:", summary_only)

with open("generated_summary.txt", "w", encoding="utf-8") as f:
    f.write(summary_only)
print("File 'generated_summary.txt' has been created.")