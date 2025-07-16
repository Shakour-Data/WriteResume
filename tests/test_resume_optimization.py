import unittest
import os
import json
from main import (
    perform_compatibility_analysis,
    optimize_resume_with_target,
    optimize_cover_letter_with_target,
    calculate_acceptance_probability,
    generate_improvement_report,
    read_file,
    save_file,
    RESUME_PATH,
    COVER_LETTER_PATH,
    JOB_DESC_PATH,
    OUTPUT_DIR,
    OPTIMIZED_RESUME,
    OPTIMIZED_COVER_LETTER,
    ANALYSIS_REPORT,
)

class TestResumeOptimization(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Ensure output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        # Read input files
        cls.resume = read_file(RESUME_PATH)
        cls.cover_letter = read_file(COVER_LETTER_PATH)
        cls.job_desc = read_file(JOB_DESC_PATH)

    def test_compatibility_analysis(self):
        analysis = perform_compatibility_analysis(self.resume, self.cover_letter, self.job_desc)
        self.assertIn("missing_skills", analysis)
        self.assertIn("matched_skills", analysis)
        self.assertIsInstance(analysis["missing_skills"], list)
        self.assertIsInstance(analysis["matched_skills"], list)

    def test_resume_optimization(self):
        analysis = perform_compatibility_analysis(self.resume, self.cover_letter, self.job_desc)
        optimized_resume = optimize_resume_with_target(self.resume, analysis)
        self.assertIn("# Added Skills", optimized_resume)
        self.assertTrue(save_file(optimized_resume, OPTIMIZED_RESUME))

    def test_cover_letter_optimization(self):
        analysis = perform_compatibility_analysis(self.resume, self.cover_letter, self.job_desc)
        optimized_cover_letter = optimize_cover_letter_with_target(self.cover_letter, analysis)
        self.assertIn("# Added Keywords", optimized_cover_letter)
        self.assertTrue(save_file(optimized_cover_letter, OPTIMIZED_COVER_LETTER))

    def test_acceptance_probability(self):
        analysis = perform_compatibility_analysis(self.resume, self.cover_letter, self.job_desc)
        prob = calculate_acceptance_probability(self.resume, self.cover_letter, self.job_desc, analysis)
        self.assertIn("probability", prob)
        self.assertIn("confidence", prob)
        self.assertGreaterEqual(prob["probability"], 0)
        self.assertLessEqual(prob["probability"], 100)

    def test_report_generation(self):
        analysis = perform_compatibility_analysis(self.resume, self.cover_letter, self.job_desc)
        optimized_resume = optimize_resume_with_target(self.resume, analysis)
        prob_results = {
            "original": calculate_acceptance_probability(self.resume, self.cover_letter, self.job_desc, analysis),
            "optimized": calculate_acceptance_probability(optimized_resume, self.cover_letter, self.job_desc, analysis),
            "final": calculate_acceptance_probability(optimized_resume, self.cover_letter, self.job_desc, analysis),
        }
        report = generate_improvement_report(self.resume, optimized_resume, analysis, prob_results)
        self.assertIn("# PRECISION OPTIMIZATION REPORT", report)
        self.assertTrue(save_file(report, ANALYSIS_REPORT))

if __name__ == "__main__":
    unittest.main()
