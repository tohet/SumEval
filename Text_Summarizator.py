from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.tokenizers import Tokenizer

from transformers import BartForConditionalGeneration, BartTokenizer, BartConfig
from transformers import T5Tokenizer, T5Config, T5ForConditionalGeneration

from Essentials import Package_Tag, Txt_package, Pipeline_Actor

class Text_Summarizator(Pipeline_Actor):
    def __init__(self):
        self.summarizer = LsaSummarizer()
        self.summarizer_name = 'LSA'

    def init_summarizer(self, summarizer_name: str):
        if summarizer_name == 'LSA':
            self.summarizer = LsaSummarizer()

        elif summarizer_name == 'T5':
            self.summarizer = T5ForConditionalGeneration.from_pretrained('t5-small')
            self.tokenizer = T5Tokenizer.from_pretrained('t5-small')

        elif summarizer_name == 'BART':
            self.summarizer = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
            self.tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
        else:
            raise Exception('Summarization method was not defined!')

        self.summarizer_name = summarizer_name

    def summarize(self, txt, summarizer, sent_n):

        if sent_n <= 0:
            raise ValueError('Number of sentences cannot be a negative value or zero')

        if self.summarizer_name == 'LSA':
            parser = PlaintextParser.from_string(txt, Tokenizer("english"))
            txt = summarizer(parser.document, sent_n)
            sum_txt = ''
            for sentence in txt:
                sum_txt += (' ' + sentence._text)
            return sum_txt

        elif self.summarizer_name == 'T5':
            text = "summarize:" + txt
            input_ids = self.tokenizer.encode(text, return_tensors='pt', max_length=512)
            summary_ids = self.summarizer.generate(input_ids)
            return self.tokenizer.decode(summary_ids[0])

        elif self.summarizer_name == 'BART':
            text = "summarize:" + txt
            inputs = self.tokenizer.batch_encode_plus([text], return_tensors='pt')
            summary_ids = summarizer.generate(inputs['input_ids'], early_stopping=True)
            bart_summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            return bart_summary

    def summarize_package(self, package):

        if package.tag == Package_Tag.FullText:
            sum_full_txt = ''
            sum_full_txt += self.summarize(package.txt[0], self.summarizer, 5)
            return [Txt_package([sum_full_txt], 0.0, package.tag)]

        elif package.tag == Package_Tag.Pages:
            return_packages = []

            # Суммаризация каждой страницы, после этого
            # саммари всех страниц складываются вместе
            sum_pgs_txt = ''
            for page in package.txt:
                sum_pgs_txt += self.summarize(page, self.summarizer, 1)

            return_packages.append(Txt_package([sum_pgs_txt], 0.0, package.tag))

            double_sum_pgs_txt = ''
            double_sum_pgs_txt += self.summarize(package.txt[0], self.summarizer, 5)

            return_packages.append(Txt_package([double_sum_pgs_txt], 0.0, package.tag))

            return return_packages

    def get_packages(self, packages: [Txt_package]):
        return_packages = []
        for package in packages:
            for entry in self.summarize_package(package):
                return_packages.append(entry)
        return return_packages
