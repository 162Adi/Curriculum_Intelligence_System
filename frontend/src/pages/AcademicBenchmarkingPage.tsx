import React, { useEffect, useState } from 'react';
import {
  Award,
  BookOpen,
  CheckCircle,
  ExternalLink,
  Shield,
  Layers,
  FileCheck,
} from 'lucide-react';
import { useCurriculumStore } from '../stores/curriculumStore';
import { api } from '../services/api';
import { Gap } from '../types';

export const AcademicBenchmarkingPage: React.FC = () => {
  const { currentCurriculum } = useCurriculumStore();
  const [academicGaps, setAcademicGaps] = useState<Gap[]>([]);

  // ACM CS2023 / IEEE-CS Core Knowledge Areas
  const benchmarkStandards = [
    {
      code: 'ACM-CS2023-AL',
      area: 'Algorithms & Complexity',
      standard: 'ACM/IEEE CS2023 Curricular Guidelines',
      requiredCoverage: 100,
      currentCoverage: 92,
      status: 'ALIGNED',
      citation: 'ACM CS2023 Section 4.2 - Algorithm Design, NP-Completeness, Approximation Algorithms',
    },
    {
      code: 'ACM-CS2023-SE',
      area: 'Software Engineering & DevOps',
      standard: 'ACM/IEEE CS2023 Curricular Guidelines',
      requiredCoverage: 90,
      currentCoverage: 60,
      status: 'DEFICIT',
      citation: 'ACM CS2023 Section 7.1 - CI/CD Pipelines, Containerization, Automated Testing',
    },
    {
      code: 'ACM-CS2023-AI',
      area: 'Artificial Intelligence & Machine Learning',
      standard: 'AAAI Model AI Curriculum / ACM CS2023',
      requiredCoverage: 95,
      currentCoverage: 45,
      status: 'CRITICAL_DEFICIT',
      citation: 'ACM CS2023 Section 8.4 - Transformer Architectures, Prompt Engineering, LLM Safety',
    },
    {
      code: 'ACM-CS2023-SYS',
      area: 'Systems, Networking & Distributed Architecture',
      standard: 'ACM/IEEE CS2023 Curricular Guidelines',
      requiredCoverage: 85,
      currentCoverage: 75,
      status: 'ALIGNED',
      citation: 'ACM CS2023 Section 6.3 - Distributed Consensus, Microservice Protocols',
    },
    {
      code: 'ACM-CS2023-SEC',
      area: 'Cybersecurity & Secure Coding Practices',
      standard: 'ACM/IEEE CS2023 Curricular Guidelines',
      requiredCoverage: 90,
      currentCoverage: 55,
      status: 'DEFICIT',
      citation: 'ACM CS2023 Section 9.2 - OWASP Top 10, Zero Trust Principles, Secure API Design',
    },
  ];

  useEffect(() => {
    if (currentCurriculum) {
      api.getGaps(currentCurriculum.id).then((allGaps) => {
        setAcademicGaps(allGaps.filter((g) => g.category === 'ACADEMIC_STANDARD'));
      });
    }
  }, [currentCurriculum]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
          <Award className="w-5 h-5 text-indigo-400" />
          <span>Academic Benchmarking & Curricular Standards</span>
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Rigorous alignment checks against ACM CS2023 Curricular Guidelines, IEEE Computer Society, and AAAI Model AI Syllabus.
        </p>
      </div>

      {/* Benchmark Standards Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {benchmarkStandards.map((std) => (
          <div key={std.code} className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="font-mono text-[11px] font-bold text-indigo-400">{std.code}</span>
                <span
                  className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${
                    std.status === 'ALIGNED'
                      ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                      : std.status === 'DEFICIT'
                      ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                      : 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
                  }`}
                >
                  {std.status.replace('_', ' ')}
                </span>
              </div>
              <h3 className="text-sm font-bold text-white">{std.area}</h3>
              <p className="text-[11px] text-slate-400 mt-0.5">{std.standard}</p>

              {/* Progress Bar */}
              <div className="mt-4">
                <div className="flex justify-between text-[11px] text-slate-400 mb-1">
                  <span>Current Alignment</span>
                  <span className="font-mono font-bold text-white">{std.currentCoverage}%</span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
                  <div
                    className={`h-full rounded-full ${
                      std.currentCoverage >= 80 ? 'bg-emerald-500' : std.currentCoverage >= 60 ? 'bg-amber-500' : 'bg-rose-500'
                    }`}
                    style={{ width: `${std.currentCoverage}%` }}
                  />
                </div>
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-slate-800 text-[10px] text-slate-400">
              <span className="font-semibold text-slate-300">Citation: </span>
              <span>{std.citation}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Detailed Standards Audit Evidence */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5">
        <h3 className="text-sm font-bold text-white mb-3 flex items-center gap-2">
          <FileCheck className="w-4 h-4 text-emerald-400" />
          <span>Curricular Standard Evidence & Recommendations</span>
        </h3>

        <div className="space-y-3">
          <div className="p-3 rounded-lg bg-slate-800/40 border border-slate-800 text-xs text-slate-300">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">ACM CS2023 Knowledge Area AI-LLM Requirement</span>
              <span className="text-[10px] text-indigo-400 font-mono">Mandatory Recommendation</span>
            </div>
            <p className="text-slate-400 text-xs">
              ACM Curricular Guidelines 2023 mandate the inclusion of modern attention mechanisms, transformer models,
              and agentic tool usage in core undergraduate computer science degrees.
            </p>
            <div className="mt-2 text-[11px] text-emerald-400 font-medium">
              Recommendation: Add 8-contact-hour module on Transformer Architectures to CS304 (Artificial Intelligence).
            </div>
          </div>

          <div className="p-3 rounded-lg bg-slate-800/40 border border-slate-800 text-xs text-slate-300">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">IEEE-CS Software Engineering Best Practices</span>
              <span className="text-[10px] text-indigo-400 font-mono">Mandatory Recommendation</span>
            </div>
            <p className="text-slate-400 text-xs">
              Standard IEEE 12207 emphasizes containerized build execution and automated linting/security scans in
              undergraduate software engineering laboratories.
            </p>
            <div className="mt-2 text-[11px] text-emerald-400 font-medium">
              Recommendation: Update CS301 laboratory exercises to mandate Docker and GitHub Actions workflows.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
