import pdfplumber, re

re_in_brackets = re.compile(r'\(.*?\)')
re_al_num = re.compile(r'[^a-zA-Z]\s')
re_connected_words = re.compile(r'- +\n|-\n')
re_wo_linebreaks = re.compile(r'\n')
re_anti_camel_case = re.compile(r'(?<!^)(?=[A-Z])')
re_multi_whitespace = re.compile(r" +")
re_short_words = re.compile(r'\W*\b\w{1,3}\b')




def parse_publication_pdf(pdf_file) -> str:
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += " " + page.extract_text()
    # remove everything in brackets
    text = re_in_brackets.sub("", text)
    # replace umlaute
    text = re.sub(r"ä", "ae", text)
    text = re.sub(r"ö", "oe", text)
    text = re.sub(r"ü", "ue", text)
    text = re.sub(r"ß", "ss", text)
    # remove non alphanumeric characters
    text = re_al_num.sub("", text)
    # unify words spepareted by hyphens and newlines
    text = re_connected_words("", text)
    # remove linebreaks
    text = re_wo_linebreaks(" ", text)
    # remove unicaode characters
    text = text.encode('ascii', errors='ignore').decode()
    # remove remaining brackets
    text = re_in_brackets.sub("", text)
    # separate words that are wrongly sticked together
    text = re_anti_camel_case(" ", text)
    # remove words < 3 characters
    text = re_short_words.sub("", text)
    # collapse multi whitespaces to single whitespaces
    text = re_multi_whitespace(" ", text)
    return text


class keyword_extractor():
    full_text: str

    def __init__(self, full_text:str) -> None:
        self.full_text = full_text

    def extract_keywords()->list:
        pass

class tfidf_keyword_extractot(keyword_extractor):

    def extract_keywords() -> list:
        pass