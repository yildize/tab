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
            q="""How to contact to Cemil ZALLUHOĞLU?""",
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
            q="""What is the content of CMP730 Pattern Classification Methods course?""",
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

        self.qas.append(EvaluationSet.QAPair(
            q="""Give me a list of course names (only the names) from Hacettepe Computer Engineering Graduate Curriculum, that would help me learn Machine Learning.""",
            a="""Here is a list of course names from the Hacettepe University Computer Engineering Graduate Curriculum that would be particularly relevant for learning Machine Learning:

CMP712 - Machine Learning
CMP784 - Deep Learning
CMP711 - Natural Language Processing
CMP713 - Data Mining
CMP714 - Text Mining
CMP670 - Statistical Natural Language Processing
CMP671 - Probabilistic Learning
CMP719 - Computational Vision
CMP722 - Advanced Computer Vision
CMP730 - Pattern Classification Methods
CMP735 - Speech Recognition
CMP795 - Advanced Natural Language Processing"""
        ))

        self.qas.append(EvaluationSet.QAPair(
            q="""Who is the head of the Hacettepe Computer Engineering Department?""",
            a="""The head of the Hacettepe University Computer Engineering Department is Prof. Dr. İlyas ÇİÇEKLİ."""
        ))

        self.qas.append(EvaluationSet.QAPair(
            q="""Please shortly inform me about the Ph.D. Qualifying Exam for Hacettepe Computer Engineering Department.""",
            a="""The Ph.D. Qualifying Exam in the Hacettepe University Computer Engineering Department consists of both a written and an oral part. Here are the key details:

Eligibility: Ph.D. students must have completed their required coursework with a minimum GPA of 2.75 to be eligible to take the exam. Those who meet the conditions must enroll in the CMP702 Qualifying Exam course in the same semester.

Exam Structure:

Written Part: Covers 10 subject areas, with questions at the undergraduate level. Students must attempt one question from each subject area, with each question graded out of 30 points. The written exam is conducted in two sessions over two different days, totaling 300 minutes.
Oral Part: May include questions from the subject areas covered in the written part, areas related to the candidate's Ph.D. thesis, and directly about the candidate's Ph.D. thesis.
Scheduling: The Ph.D. Qualifying exam is offered each semester during the final exam week. Examination committees are organized in April and November.

Subject Areas for the Written Part:

Session 1 (Theory): Includes Data Structures and Algorithms, Automata and Formal Languages, Algorithm Analysis, Programming Languages.
Session 2 (System): Covers Data Management and Database Systems, Operating Systems, Logic Design and Computer Architectures, Computer Networks, Software Engineering.
Students are expected to be successful in both the written and oral parts of the exam."""
        ))

        self.qas.append(EvaluationSet.QAPair(
            q="""When and how should I determine my MSc. thesis teacher?""",
            a="""For determining your MSc thesis supervisor in the Computer Engineering Graduate Program at Hacettepe University, the process is outlined as follows:

Initial Supervisor Assignment: When you register for the program, the Head of the Department is automatically appointed as your temporary supervisor.
Selection of Permanent Thesis Supervisor: You are required to select your permanent thesis supervisor by the end of the first semester.
Thesis Proposal Submission: The thesis proposal must be submitted to the Institute of Science by the end of the second semester at the latest. Before taking CMP600 (Special Studies) courses, the thesis proposal should be submitted by the specified date in the academic calendar.
Enrollment in Thesis Course: After your thesis proposal is approved, you must enroll in the non-credit thesis course (CMP600) every semester, starting from the third semester."""
        ))
    @property
    def answers(self):
        return [qa.a for qa in self.qas]

    @property
    def questions(self):
        return [qa.q for qa in self.qas]

