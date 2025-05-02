import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

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
        torch_dtype=torch.float32,
        device=device,
    )
    return asr_pipe
