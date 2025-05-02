import torch
import gc
import os

def initialize_gpu():
    """
    GPU 캐시, IPC, 가비지 컬렉션 실행 후 GPU 동기화 및 초기화
    """
    torch.cuda.empty_cache()
    torch.cuda.ipc_collect()
    gc.collect()
    torch.cuda.synchronize()
    # os.system("nvidia-smi --gpu-reset")  # 필요시 주석 해제 (관리자 권한 필요)
