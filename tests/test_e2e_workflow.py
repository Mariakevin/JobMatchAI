import io
import unittest
import asyncio

from api.main import (
    extract_resume,
    extract_internship_details,
    match,
    reanalyze,
    InternshipParseRequest,
    StructuredMatchRequest,
)
from api.models import (
    EducationItem,
    InternshipDetail,
    OverallEligibility,
    SkillEvidenceState,
    StudentPreferences,
    StudentProfile,
    WorkMode,
)


class EndToEndWorkflowTests(unittest.TestCase):
    def test_complete_student_journey(self):
        # Step 1: Student uploads resume
        resume_content = (
            "Alex Smith\n"
            "Education\n"
            "B.Tech in Computer Science and Engineering\n"
            "CGPA: 8.6/10\n"
            "Expected Graduation: 2025\n"
            "Current Semester: 6\n"
            "Technical Skills\n"
            "Python, React, TypeScript, SQL, Docker, FastAPI\n"
            "Projects\n"
            "JobMatch Assistant: Developed full-stack web application using React, FastAPI, and Docker\n"
            "Data Analytics Dashboard: Built visualization tool in Python using pandas\n"
            "Experience\n"
            "Software Intern at OpenSource Labs: Implemented REST APIs and wrote SQL queries for PostgreSQL"
        ).encode("utf-8")

        upload_res = asyncio.run(
            extract_resume(
                upload_file := type("MockUpload", (), {
                    "filename": "alex_resume.txt",
                    "read": lambda self, sz: asyncio.sleep(0, result=resume_content),
                })()
            )
        )
        self.assertIn("structured_profile", upload_res)
        profile_data = upload_res["structured_profile"]
        profile = StudentProfile.model_validate(profile_data)

        # Step 2: Verify extracted facts
        self.assertEqual(len(profile.education), 1)
        self.assertEqual(profile.education[0].degree, "B.Tech")
        self.assertEqual(profile.education[0].discipline, "Computer Science")
        self.assertEqual(profile.education[0].cgpa, 8.6)
        self.assertEqual(profile.education[0].graduation_date, "2025")

        # Step 3: Student reviews and adjusts preferences
        profile.preferences = StudentPreferences(
            preferred_work_modes=[WorkMode.REMOTE, WorkMode.HYBRID],
            willing_to_relocate=False,
            available_hours_per_week=40,
            minimum_stipend=1000.0,
            unpaid_acceptable=False,
        )

        # Step 4: Add multiple internship postings
        posting_1 = (
            "Role: Junior Backend Engineer Intern\n"
            "Company: CloudScale\n"
            "Work mode: remote. Stipend: $1,500/month. Duration: 3 months.\n"
            "Eligibility: Degree: B.Tech in Computer Science or IT. Minimum CGPA of 7.5. Graduating in 2025.\n"
            "Required skills: Python, FastAPI, Docker, SQL.\n"
            "Preferred: Kubernetes."
        )
        detail_1 = InternshipDetail.model_validate(
            extract_internship_details(
                InternshipParseRequest(
                    title="Junior Backend Engineer Intern",
                    company="CloudScale",
                    description=posting_1,
                )
            )["internship"]
        )

        posting_2 = (
            "Role: Mobile App Developer Intern\n"
            "Company: AppWorks\n"
            "Work mode: on-site in Austin. Duration: 6 months.\n"
            "Eligibility: Degree: BCA only.\n"
            "Required skills: Flutter, Dart, Swift."
        )
        detail_2 = InternshipDetail.model_validate(
            extract_internship_details(
                InternshipParseRequest(
                    title="Mobile App Developer Intern",
                    company="AppWorks",
                    description=posting_2,
                )
            )["internship"]
        )

        posting_3 = (
            "Role: ML Intern\n"
            "Company: Apex AI\n"
            "Application fee of $30 required to review profile.\n"
            "Required: Python, PyTorch."
        )
        detail_3 = InternshipDetail.model_validate(
            extract_internship_details(
                InternshipParseRequest(
                    title="ML Intern",
                    company="Apex AI",
                    description=posting_3,
                )
            )["internship"]
        )

        # Step 5: Run Match Analysis
        match_res = match(
            StructuredMatchRequest(
                profile=profile,
                internships=[detail_1, detail_2, detail_3],
            )
        )
        matches = match_res["matches"]
        self.assertEqual(len(matches), 3)

        # Role 1 verification:
        m1 = next(m for m in matches if m["title"] == "Junior Backend Engineer Intern")
        self.assertEqual(m1["eligibility"]["status"], "ELIGIBLE")
        self.assertGreater(m1["fit_score"]["score"], 70)
        self.assertFalse(m1["fit_score"]["is_provisional"])
        # Skills check: Python demonstrated
        py_match = next(s for s in m1["skill_matches"] if s["normalized_skill"] == "python")
        self.assertEqual(py_match["status"], SkillEvidenceState.DEMONSTRATED.value)

        # Role 2 verification: Degree mismatch (BCA only vs candidate B.Tech)
        m2 = next(m for m in matches if m["title"] == "Mobile App Developer Intern")
        self.assertEqual(m2["eligibility"]["status"], "NOT_ELIGIBLE")
        self.assertIn("does not match required degree", m2["eligibility"]["summary"])

        # Role 3 verification: Warning indicator for application fee
        m3 = next(m for m in matches if m["title"] == "ML Intern")
        self.assertTrue(any(r["category"] == "application_fee" for r in m3["risk_indicators"]))
        self.assertIn("Application fee of $30", m3["risk_indicators"][0]["excerpt"])

        # Step 6: Student Correction & Re-analysis
        # Candidate explicitly declares they do not have PyTorch (Confirmed gap)
        for s in profile.skills:
            if s.normalized_name == "docker":
                s.is_confirmed_gap = True
                s.student_confirmed = True

        re_res = reanalyze(
            StructuredMatchRequest(
                profile=profile,
                internships=[detail_1],
            )
        )
        m1_updated = re_res["matches"][0]
        docker_match = next(
            s for s in m1_updated["skill_matches"] if s["normalized_skill"] == "docker"
        )
        self.assertEqual(docker_match["status"], SkillEvidenceState.CONFIRMED_GAP.value)
        self.assertTrue(
            any(g["category"] == "confirmed_gap" for g in m1_updated["gap_report"]["gaps"])
        )


if __name__ == "__main__":
    unittest.main()
