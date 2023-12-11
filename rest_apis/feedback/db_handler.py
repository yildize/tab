import os
import sqlite3

from utils.utils import ROOT_PATH

class DBHandler:
    def __init__(self, storage_name="feedbacks.db"):
        self.storage_name = os.path.join(ROOT_PATH, "storage", "feedbacks", storage_name)
        directory = os.path.dirname(self.storage_name)
        os.makedirs(directory, exist_ok=True)

        with self.db_connection as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY,
                is_rag BOOLEAN,
                is_liked BOOLEAN,
                user_question TEXT,
                matched_question TEXT,
                matched_answer TEXT,
                suggested_answer TEXT,
                rag_answer TEXT,
                sources TEXT
            )""")

    @property
    def db_connection(self):
        return sqlite3.connect(self.storage_name)

    def read_feedbacks(self):
        with self.db_connection as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM feedback")
            return cursor.fetchall()

    def insert_feedback(self, is_rag, is_liked, user_question, matched_question=None, matched_answer=None, suggested_answer=None, rag_answer=None, sources=None):
        with self.db_connection as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO feedback (is_rag, is_liked, user_question, matched_question, matched_answer, suggested_answer, rag_answer, sources)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (is_rag, is_liked, user_question, matched_question, matched_answer, suggested_answer, rag_answer, sources))
            conn.commit()


if __name__ == "__main__":
    db_handler = DBHandler()
    feedbacks = db_handler.read_feedbacks()

    for feedback in feedbacks:
        print(feedback)
