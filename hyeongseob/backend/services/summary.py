import torch
from fastapi import APIRouter
from backend.utils import load_model_and_tokenizer, post_process, get_generation_kwargs, get_detailed_prompt

summary_router = APIRouter(prefix="/tt", tags=["Text-to-Text"])

@summary_router.post("/summary")
def get_summary():
    torch.cuda.empty_cache()
    model, tokenizer = load_model_and_tokenizer()
    generation_kwargs = get_generation_kwargs()
    detailed_prompt = get_detailed_prompt()

    txt_file_path = "backend/output_folder/conversion_text.txt"
    with open(txt_file_path, "r", encoding="utf-8") as f:
        original_text = f.read()

    prompt = detailed_prompt.format(original_text=original_text)

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        output_tokens = model.generate(**inputs, **generation_kwargs)

    generated_text = tokenizer.decode(output_tokens[0], skip_special_tokens=True)
    
    if "Summary:" in generated_text:
        summary_only = generated_text.split("Summary:")[-1].strip()
    else:
        summary_only = generated_text.strip()

    if "Note:" in summary_only:
        summary_only = summary_only.split("Note:")[0].strip()

    summary_only = post_process(summary_only)

    with open("backend/output_folder/generated_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary_only)

    return {"summary": summary_only}