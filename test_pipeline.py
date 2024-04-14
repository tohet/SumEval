import unittest
from Text_Extractor import Text_Extractor
from Text_Summarizator import Text_Summarizator
from Pipeline import Pipeline

class test_Extractor(unittest.TestCase):
    def test_Etract_URL(self):
        extractor = Text_Extractor()
        self.assertRaises(Exception, extractor.get_pdf, 'dfgfdgbfdgsdfdvdfvbfgb', True)
        self.assertRaises(Exception, extractor.get_pdf, 'grbbbdsfvstdgffgrfdvfd', False)
        self.assertRaises(Exception, extractor.get_pdf,'https://www.youtube.com/watch?v=dQw4w9WgXcQ', True)
        self.assertRaises(Exception, extractor.get_pdf,'https://www.imf.org/-/media/Files/Publications/WP/2023/English/wpiea2023242-print-pdf.ashx', False)

    def test_page_input(self):
        extractor = Text_Extractor()
        self.assertRaises(AssertionError, extractor.get_packages, 'https://www.imf.org/-/media/Files/Publications/WP/2023/English/wpiea2023242-print-pdf.ashx', True, 99999)
        self.assertRaises(AssertionError, extractor.get_packages,'https://www.imf.org/-/media/Files/Publications/WP/2023/English/wpiea2023242-print-pdf.ashx', True, -99999)
        self.assertRaises(TypeError, extractor.get_packages,'https://www.imf.org/-/media/Files/Publications/WP/2023/English/wpiea2023242-print-pdf.ashx', True, 'frog')

class test_Summarizator(unittest.TestCase):
    def test_init_summarizer(self):
        summarizator = Text_Summarizator()
        self.assertRaises(Exception, summarizator.init_summarizer, 'TGVDTGVD')

    def test_summarize(self):
        summarizator = Text_Summarizator()
        self.assertRaises(ValueError, summarizator.summarize, 'she sells seashells', summarizator.summarizer, -999)

class test_Evaluator(unittest.TestCase):
    def test_eval_positives(self):
        pipeline = Pipeline('topic_offers.csv')
        sum_positive1 = pipeline.sum_eval('https://www.imf.org/-/media/Files/Publications/WP/2023/English/wpiea2023220-print-pdf.ashx', True, 3)
        self.assertGreater(sum_positive1[0].interest_score, 0.48)
        sum_positive2 = pipeline.sum_eval('https://www.ecb.europa.eu/pub/pdf/fsr/ecb.fsr202311~bfe9d7c565.en.pdf', True, 6)
        self.assertGreater(sum_positive2[0].interest_score, 0.48)

    def test_eval_negatives(self):
        pipeline = Pipeline('topic_offers.csv')
        sum_negative1 = pipeline.sum_eval('https://www.imf.org/-/media/Files/Publications/WP/2023/English/wpiea2023137-print-pdf.ashx', True, 5)
        self.assertLess(sum_negative1[0].interest_score, 0.5)
        sum_negative2 = pipeline.sum_eval('https://www.bis.org/publ/work1105.pdf', True, 4)
        self.assertLess(sum_negative2[0].interest_score, 0.5)



if __name__ == '__main__':
    unittest.main()