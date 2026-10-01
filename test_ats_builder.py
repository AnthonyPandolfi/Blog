import os
import json
import pytest
from ats_builder import generate_resume_txt, generate_resume_html, generate_cover_letter, load_profile

@pytest.fixture
def mock_profile():
    return {
      "personal_info": {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "555-5555"
      },
      "summary": "A test summary",
      "skills": ["Test1", "Test2"],
      "experience": [
        {
          "company": "Test Co",
          "role": "Tester",
          "start_date": "2020",
          "end_date": "2021",
          "responsibilities": ["Tested things"]
        }
      ]
    }

def test_generate_resume_txt(mock_profile):
    txt = generate_resume_txt(mock_profile)
    assert "JOHN DOE" in txt
    assert "john@example.com" in txt
    assert "A test summary" in txt
    assert "Test1, Test2" in txt
    assert "Tester at Test Co" in txt

def test_generate_resume_html(mock_profile):
    html = generate_resume_html(mock_profile)
    assert "<h1>John Doe</h1>" in html
    assert "<p>A test summary</p>" in html
    assert "<h2>Skills</h2>" in html

def test_generate_cover_letter(mock_profile):
    cl = generate_cover_letter(mock_profile, "Software Engineer", "OpenAI")
    assert "Software Engineer position at OpenAI" in cl
    assert "Dear Hiring Manager at OpenAI" in cl
    assert "John Doe" in cl
    assert "john@example.com" in cl

def test_load_profile(tmp_path):
    p = tmp_path / "test_profile.json"
    p.write_text('{"test": "data"}')
    loaded = load_profile(str(p))
    assert loaded == {"test": "data"}
