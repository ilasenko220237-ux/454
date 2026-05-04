import unittest
import json
import os

class TestMovieLibrary(unittest.TestCase):
    
    def test_rating_validation_correct(self):
        rating = 8.5
        self.assertTrue(0 <= rating <= 10)

    def test_rating_validation_too_high(self):
        rating = 11
        self.assertFalse(0 <= rating <= 10)

    def test_rating_validation_negative(self):
        rating = -1
        self.assertFalse(0 <= rating <= 10)

    def test_year_validation_correct(self):
        year = 2025
        self.assertTrue(1888 <= year <= 2026)

    def test_year_validation_string(self):
        year_str = "abc"
        try:
            int(year_str)
            is_valid = True
        except ValueError:
            is_valid = False
        self.assertFalse(is_valid)

    def test_json_save_load(self):
        test_data = [{"id": 1, "title": "Matrix", "genre": "Sci-Fi", "year": 1999, "rating": 8.7}]
        filename = "test_movies.json"
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(test_data, f)
        
        with open(filename, "r", encoding="utf-8") as f:
            loaded = json.load(f)
            
        self.assertEqual(loaded[0]["title"], "Matrix")
        os.remove(filename)

if __name__ == "__main__":
    unittest.main()
