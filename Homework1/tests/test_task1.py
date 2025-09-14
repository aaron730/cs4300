import subprocess

def test_task1_output():
    
    result = subprocess.run(
        ["python", "/home/student/cs4300/Homework1/homework1/src/task1.py"],
        capture_output=True,
        text=True
    )
    assert result.stdout.strip() == "Hello, World!"