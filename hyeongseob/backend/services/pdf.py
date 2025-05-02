from fpdf import FPDF

def generate_pdf(text: str, output_file: str = "summary.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15) # 자동 페이지 분할
    pdf.add_page() # 페이지 추가 
    pdf.set_font("Arial", size=12) # 폰트 
    pdf.multi_cell(0, 10, text) # 긴 텍스트 자동 줄바꿈
    pdf.output(output_file) # 파일 저장
    return output_file
