# src/plugins/job_intelligence/__init__.py

"""
Job Intelligence Plugin Package

This package contains plugins for job market analysis.
"""

from .scraper import JobScraperPlugin
from .analyzer import SkillsAnalyzerPlugin

# This allows importing both plugins
__all__ = ["JobScraperPlugin", "SkillsAnalyzerPlugin"]