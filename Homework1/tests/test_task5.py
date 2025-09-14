import homework1.src.task5 as task5
import subprocess

def test_favorite_books_len():
    assert len(task5.favorite_books) == 5

def test_top3():
    result = subprocess.run(
        ["python", "/home/student/cs4300/Homework1/homework1/src/task5.py"],
        capture_output=True,
        text=True
    )
    assert result.stdout.strip() == "['East of Eden', 'The Anthropocene Reviewed', 'All Quient on the Western Front']"

def test_student_db_keys():
    assert set(task5.student_db.keys()) == {0, 1, 2, 3}

def test_student_db_Values():
    assert set(task5.student_db.values()) == {"Aaron", "Quinn", "Alice", "Josh"}

def test_get_name_by_Id():
    assert task5.student_db[1] == "Quinn"


