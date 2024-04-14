from deep_translator import GoogleTranslator
from Essentials import Package_Tag, Txt_package, Pipeline_Actor

class Text_Translator(Pipeline_Actor):
    def get_packages(self, packages: [Txt_package]):
        return_packages = []
        for package in packages:
            transl_text = GoogleTranslator(source='auto', target='ru').translate(package.txt[0][:2500])
            return_packages.append(Txt_package(transl_text, 0.0, package.tag))
        return return_packages
