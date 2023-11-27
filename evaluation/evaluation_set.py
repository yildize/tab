from dataclasses import dataclass


class EvaluationSet:
    """ This class contains the randomly hand-crafted evaluation questions and ideal answers from the corpus,
    this set will be used to evaluate the answer-correctness performance of different qa-systems so that
    we can compare them."""
    @dataclass
    class QAPair:
        q: str
        a: str

    def __init__(self):
        self.qas = []

        self.qas.append(EvaluationSet.QAPair(
            q="""How can I contact with Cemil Zalluhoğlu?""",
            a="""You can contact Asst. Prof. Dr. Cemil Zalluhoğlu via the following methods:

Email: cemil[at]cs.hacettepe.edu.tr (replace [at] with @)
Telephone: (0312) 297 7500 (Extension 127)
Office: Room 201
Web Site: http://web.cs.hacettepe.edu.tr/~cemil/"""
        ))

        self.qas.append(EvaluationSet.QAPair(
            q="""Give me the full list of names of Hacettepe Computer Engineering Department's Research Assistants.""",
            a="""The full list of names of Hacettepe Computer Engineering Department's Research Assistants is as follows:

Görkem AKYILDIZ
Ahmet ALKILINÇ
Burçak ASAL
Zeynep BALA
Alperen ÇAKIN
Hayriye ÇELİKBİLEK
Dr. Selma DİLEK
Bahar GEZİCİ
Dr. Tuğba GÜRGEN ERDOĞAN
Sibel Kapan
Ali Baran Taşdemir
Burcu YALÇINER
Ardan YILMAZ"""
        ))

        self.qas.append(EvaluationSet.QAPair(
            q="""What is the content of  CMP730	Pattern Classification Methods course?""",
            a="""The content of the CMP730 Pattern Classification Methods course is as follows:

The course covers general definitions and mathematical foundations of Bayes Decision Theory, Maximum Likelihood, Nearest Neighbor Classification, Linear Discrimination Functions, Multilayer Neural Networks, Unsupervised Learning and Clustering. It is a theoretical course with a focus on the underlying methods and principles used for pattern classification in the field of machine learning and data analysis."""
        ))


        self.qas.append(EvaluationSet.QAPair(
            q="""Do I have to pay a registration fee for Computer Engineering Graduate Education Programs?""",
            a="""During the normal education period (Master 4 semesters, Doctorate 8 semesters), no registration
fee is to be paid from citizens of the Republic of Turkey. Students who cannot complete their
education during normal education period pay the fees shown in the relevant document."""))


        self.qas.append(EvaluationSet.QAPair(
            q="""What is the suggested 2nd semester courses for Computer Engineering MSc. Program?""",
            a="""The suggested 2nd semester courses for the Master of Science (M.Sc.) program in Computer Engineering, are:

Elective CMP6XX
Elective CMP6XX
Elective CMP6XX
Elective CMP6XX
CMP601"""))

    @property
    def answers(self):
        return [qa.a for qa in self.qas]

    @property
    def questions(self):
        return [qa.q for qa in self.qas]

