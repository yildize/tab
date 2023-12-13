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
            q="""What is the contact information of Ebru AKÇAPINAR SEZER?""",
            a="""The email address of Prof. Dr. Ebru Akçapınar Sezer is ebru[at]hacettepe.edu.tr. In a standard email format, this would be ebru@hacettepe.edu.tr."""
        ))

        self.qas.append(EvaluationSet.QAPair(
            q="""What are the research areas of  Mehmet Önder EFE?""",
            a="""The research areas of Assoc. Prof. Dr. Tunca Doğan include:
            
Computer Vision
Multimedia Data Mining
Object, Face, and Action Recognition
Analysis of Historical Documents
            """
        ))

        self.qas.append(EvaluationSet.QAPair(
            q="""Who are the heads of division in Hacettepe Computer Engineering Department?""",
            a="""The heads of divisions in the Hacettepe University Computer Engineering Department are as follows:

Computer Science Division: Headed by Prof. Dr. İlyas ÇİÇEKLİ.
Computer Software Division: Headed by Prof. Dr. Pınar DUYGULU ŞAHİN.
Computer Hardware Division: Headed by Prof. Dr. Mehmet Önder EFE.
Artificial Intelligence Division: Headed by Prof. Dr. Ebru AKÇAPINAR SEZER.
            """
        ))

        self.qas.append(EvaluationSet.QAPair(
            q="""Tell me about the history of Hacettepe Computer Engineering Department""",
            a="""The Department of Computer Engineering at Hacettepe University was established as a graduate school in 1974 and became the first in Turkey to offer an undergraduate degree in computer engineering in 1977. It has expanded significantly over the years and is known for its strong research profile in areas such as computer vision, multimedia data mining, and the analysis of historical documents. The department has received numerous awards, including TUBITAK research grants and Google Research Awards, and has a specialized infrastructure featuring advanced labs and equipment for both educational and research activities."""
        ))

        self.qas.append(EvaluationSet.QAPair(
            q="""I have failed a graduate course, can I drop it?""",
            a="""If you fail a course in the Graduate Program, you cannot drop it from your transcript. Instead, the course will be automatically assigned to you again by the system if it is offered in the current semester. If the course is not available, you can take a different course in its place by submitting a petition."""
        ))

        self.qas.append(EvaluationSet.QAPair(
            q="""What GPA do I need to apply for Computer Engineering Graduate programs?""",
            a="""To apply for the Computer Engineering Graduate programs, you need the following GPAs:

For the Master's program: A minimum undergraduate GPA of 2.8 (in a 4-system scale).
For the Doctorate or Integrated Doctorate program: Specific GPA criteria are mentioned but not clearly stated in the provided document. You may need to refer to the program guidelines or contact the department directly for precise information regarding the GPA requirement for these programs."""
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

        self.qas.append(EvaluationSet.QAPair(
            q="""What are the course requirements for a Ph.D. student in Computer Engineering at Hacettepe University?""",
            a="""Ph.D. students accepted with M.S. degrees must complete 7 graduate courses (21 credits), while those accepted with undergraduate degrees must complete 14 graduate courses (42 credits). In addition to elective courses, all Ph.D. students are required to take four must-courses, including CMP791 (Research Methods in Computer Science), CMP793 (Advanced Academic Skills and Practices), and CMP701 (Seminar). Students with M.S. degrees must finish their coursework within four semesters, and those with B.S. degrees within six semesters."""
        ))

        self.qas.append(EvaluationSet.QAPair(
            q="""What are the steps and requirements for completing the Ph.D. thesis at Hacettepe University's Computer Engineering program?""",
            a="""After completing coursework, Ph.D. students must pass a qualifying exam consisting of a written and oral part. Within six months of passing this exam, they must prepare and present a thesis proposal to a jury. The student then actively works on their thesis, presenting progress every six months. For Ph.D. thesis defense, the student must publish a journal article based on their thesis in a reputable journal and an international conference article. The student must complete their thesis work and submit it to the defense jury members at least 15 days before the defense."""
        ))

        self.qas.append(EvaluationSet.QAPair(
            q="""Can I take courses from another department during my M.Sc. courses?""",
            a="""Yes, you can take courses from another department during your Master of Science (M.Sc.) program. However, there is a limit to the number of such courses you can enroll in. Specifically, in a Master’s program with a thesis at Hacettepe University, you are allowed to take a maximum of 2 courses from another department, institution, or institute."""
        ))

        self.qas.append(EvaluationSet.QAPair(
            q="""Tell me some awards won by the department in 2018""",
            a="""In 2018, the Hacettepe University Computer Engineering Department won the following awards:

Turkish Academy of Sciences' 2018 Outstanding Young Scientist (GEBIP) Award: Assoc. Prof. Erkut Erdem received this award, which is given by TÜBA to support young scientists with outstanding scientific studies in their research and development of their research groups and encourage young scientists to undertake successful research.

Science Academy Young Scientists Award (BAGEP) in Mathematics: Assoc. Prof. Lale Özkahya was one of the three recipients of this award in 2018, recognizing her contributions in the field of mathematics.

TÜBİTAK-1001 Grant for 'Using Synthetic Data for Deep Person Re-Identification': The project proposed by Dr. Erkut Erdem (PI), Dr. Aykut Erdem, and Dr. Ufuk Çelikcan received funding from the TÜBİTAK 1001 program. This project focuses on enhancing person re-identification techniques using synthetic data."""
        ))


        self.qas.append(EvaluationSet.QAPair(
            q="""What specific subjects  regarding Operating Systems should I be aware of for the phd qualifying exam?""",
            a="""
For the Ph.D. qualifying exam regarding Operating Systems, you should be aware of the following specific subjects:

Process management
Process scheduling
Process synchronization
Deadlocks
Memory Management Strategies
Virtual memory management
File System
Implementing file Systems"""
        ))


    @property
    def answers(self):
        return [qa.a for qa in self.qas]

    @property
    def questions(self):
        return [qa.q for qa in self.qas]

