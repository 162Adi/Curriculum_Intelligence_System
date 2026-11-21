"""
Agent tests for the 5 specialized Curriculum Intelligence Agents & Support Agents.
"""
import pytest
from app.agents.curriculum_mapping import CurriculumMappingAgent
from app.agents.industry_skills import IndustrySkillsAgent
from app.agents.benchmarking import AcademicBenchmarkingAgent
from app.agents.gap_analysis import GapAnalysisAgent
from app.agents.recommendation import RecommendationAgent
from app.agents.support_agents import DeepResearchAgent, QualityEvaluator


def test_curriculum_mapping_agent(db_session, sample_curriculum):
    res = CurriculumMappingAgent.execute(db_session, sample_curriculum.id)
    assert res is not None
    assert "total_courses" in res
    assert res["total_courses"] >= 4
    assert len(res["mapped_courses"]) >= 4


def test_industry_skills_agent(db_session):
    res = IndustrySkillsAgent.execute(db_session)
    assert res is not None
    assert "ranked_skills" in res
    assert len(res["ranked_skills"]) >= 10


def test_academic_benchmarking_agent(db_session, sample_curriculum):
    res = AcademicBenchmarkingAgent.execute(db_session, sample_curriculum.id)
    assert res is not None
    assert "total_benchmark_topics" in res
    assert res["total_benchmark_topics"] >= 3


def test_gap_analysis_and_recommendations(db_session, sample_curriculum):
    mapping_res = CurriculumMappingAgent.execute(db_session, sample_curriculum.id)
    ind_res = IndustrySkillsAgent.execute(db_session)
    bench_res = AcademicBenchmarkingAgent.execute(db_session, sample_curriculum.id)
    gap_res = GapAnalysisAgent.execute(db_session, sample_curriculum.id, mapping_res, ind_res, bench_res)
    assert gap_res is not None
    assert "total_gaps_identified" in gap_res
    assert gap_res["total_gaps_identified"] > 0

    rec_res = RecommendationAgent.execute(db_session, sample_curriculum.id, gap_res)
    assert rec_res is not None
    assert "total_recommendations" in rec_res
    assert rec_res["total_recommendations"] > 0


def test_deep_research_agent():
    research = DeepResearchAgent.investigate("Large Language Model prompt safety in CS curriculum")
    assert "query" in research
    assert "citations" in research
    assert len(research["citations"]) >= 1


def test_quality_evaluator():
    test_recs = [
        {"title": "Add Docker to CS301", "rationale": "High industry demand in DevOps"},
        {"title": "Introduce Vector Databases to CS201", "rationale": "ACM CS2023 Sec 6.3 recommendation"}
    ]
    eval_res = QualityEvaluator.evaluate(test_recs)
    assert eval_res["validation_score"] == 100.0
    assert eval_res["hallucination_detected"] is False
