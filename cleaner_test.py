from utils.dummy_qa_cleaner import DummyQACleaner

cleaner = DummyQACleaner(file_path="./storage/extracted_questions/qs.json")
#cleaner.how_many_unique_questions()
#cleaner.top_n_questions(10)
cleaner.clean()
