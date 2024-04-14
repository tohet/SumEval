from Text_Extractor import Text_Extractor
from Text_Summarizator import Text_Summarizator
from Text_Translator import Text_Translator
from Text_Evaluator import Text_Evaluator
class Pipeline():
    def __init__(self, data_path):
        self.extractor = Text_Extractor()
        self.summarizator = Text_Summarizator()
        self.translator = Text_Translator()
        self.evaluator = Text_Evaluator(data_path)

    def sum_eval(self, file_path: str, use_url: bool, start_page: int):
        extracted_packs = self.extractor.get_packages(file_path, use_url, start_page)
        extracted_packs = extracted_packs[1:len(extracted_packs)]

        summarized_packs = self.summarizator.get_packages(extracted_packs)

        translated_packs = self.translator.get_packages(summarized_packs)

        evaluated_packs = self.evaluator.get_packages(translated_packs)

        return evaluated_packs