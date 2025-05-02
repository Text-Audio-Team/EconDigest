import re
from collections import defaultdict

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
