
import unittest
from persona_chain import generate_persona_from_chunks

class TestPersonaChain(unittest.TestCase):
    def test_generate_persona_from_chunks(self):
        chunks = ["I love mountain biking and hiking during weekends."]
        persona = generate_persona_from_chunks(chunks)
        self.assertIn("mountain biking", persona.lower())

if __name__ == "__main__":
    unittest.main()
