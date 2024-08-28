import easyocr

def extract_text_from_image(image_path):
    reader = easyocr.Reader(['ch_tra', 'en'])
    result = reader.readtext(image_path)
    
    text_results = []
    for (bbox, text, prob) in result:
        text_results.append({
            'text': text,
            'prob': prob
        })
    
    return text_results