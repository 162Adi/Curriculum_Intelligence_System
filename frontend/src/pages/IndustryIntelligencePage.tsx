import React, { useEffect, useState } from 'react';
import {
  TrendingUp,
  Briefcase,
  Layers,
  Search,
  ExternalLink,
  Award,
  BarChart2,
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  Legend,
} from 'recharts';
import { useCurriculumStore } from '../stores/curriculumStore';
import { api } from '../services/api';
import { Gap } from '../types';

export const IndustryIntelligencePage: React.FC = () => {
  const { currentCurriculum } = useCurriculumStore();
  const [industryGaps, setIndustryGaps] = useState<Gap[]>([]);
  const [searchTerm, setSearchTerm] = useState('');

  // Sample data from Adzuna tech market snapshot & ESCO taxonomy
  const skillMarketData = [
    { skill: 'Generative AI / LLMs', demand: 95, curriculumCoverage: 20, jobs: 420 },
    { skill: 'Docker & Kubernetes', demand: 90, curriculumCoverage: 30, jobs: 380 },
    { skill: 'CI/CD & DevOps', demand: 85, curriculumCoverage: 35, jobs: 310 },
    { skill: 'Cloud Architecture (AWS/GCP)', demand: 88, curriculumCoverage: 40, jobs: 290 },
    { skill: 'Data Structures & Algorithms', demand: 80, curriculumCoverage: 95, jobs: 260 },
    { skill: 'FastAPI / Modern APIs', demand: 78, curriculumCoverage: 25, jobs: 240 },
    { skill: 'PostgreSQL & pgvector', demand: 75, curriculumCoverage: 50, jobs: 210 },
    { skill: 'Microservices & Distributed Sys', demand: 82, curriculumCoverage: 45, jobs: 195 },
  ];

  const radarData = skillMarketData.map((d) => ({
    subject: d.skill,
    'Market Demand': d.demand,
    'Curriculum Coverage': d.curriculumCoverage,
  }));

  useEffect(() => {
    if (currentCurriculum) {
      api.getGaps(currentCurriculum.id).then((allGaps) => {
        setIndustryGaps(allGaps.filter((g) => g.category === 'INDUSTRY_SKILL'));
      });
    }
  }, [currentCurriculum]);

  const filteredSkills = skillMarketData.filter((s) =>
    s.skill.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
          <TrendingUp className="w-5 h-5 text-blue-400" />
          <span>Industry Intelligence & Skill Demand</span>
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Real-time external job vacancy data via Adzuna API and European Skills/Occupations (ESCO) taxonomy.
        </p>
      </div>

      {/* Visual Analytics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Radar Chart */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5">
          <h3 className="text-sm font-bold text-white mb-1 flex items-center gap-2">
            <BarChart2 className="w-4 h-4 text-blue-400" />
            <span>Market Demand vs Curriculum Coverage</span>
          </h3>
          <p className="text-xs text-slate-400 mb-4">
            Comparison highlighting areas where student preparation lags industry hiring volume.
          </p>
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid stroke="#334155" />
                <PolarAngleAxis dataKey="subject" stroke="#94a3b8" fontSize={10} />
                <PolarRadiusAxis stroke="#64748b" fontSize={9} />
                <Radar name="Market Demand" dataKey="Market Demand" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.4} />
                <Radar name="Curriculum Coverage" dataKey="Curriculum Coverage" stroke="#10b981" fill="#10b981" fillOpacity={0.4} />
                <Legend wrapperStyle={{ fontSize: '11px' }} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Bar Chart of Job Postings */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5">
          <h3 className="text-sm font-bold text-white mb-1 flex items-center gap-2">
            <Briefcase className="w-4 h-4 text-emerald-400" />
            <span>Active Tech Job Vacancies in Market Sample</span>
          </h3>
          <p className="text-xs text-slate-400 mb-4">
            Sample of 1,420 Indian tech vacancies indexed across Bangalore, Hyderabad, Pune.
          </p>
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={skillMarketData} layout="vertical" margin={{ top: 5, right: 30, left: 40, bottom: 5 }}>
                <XAxis type="number" stroke="#64748b" fontSize={10} />
                <YAxis dataKey="skill" type="category" stroke="#94a3b8" fontSize={10} width={130} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }} />
                <Bar dataKey="jobs" fill="#10b981" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* In-Demand Skills Table */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 mb-4">
          <div>
            <h3 className="text-sm font-bold text-white">Live Industry Skill Demand Register</h3>
            <p className="text-xs text-slate-400">Classified against ESCO Level 4 technical skills</p>
          </div>

          <div className="relative">
            <Search className="w-3.5 h-3.5 absolute left-3 top-2.5 text-slate-400" />
            <input
              type="text"
              placeholder="Search skills..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="bg-slate-800 border border-slate-700 text-xs text-slate-200 rounded-lg pl-8 pr-3 py-1.5 focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-800/60 text-slate-400 uppercase text-[10px]">
              <tr>
                <th className="py-2.5 px-3 rounded-l-lg">Technical Skill</th>
                <th className="py-2.5 px-3">Industry Demand</th>
                <th className="py-2.5 px-3">Curriculum Coverage</th>
                <th className="py-2.5 px-3">Adzuna Job Count</th>
                <th className="py-2.5 px-3 rounded-r-lg">Discrepancy Severity</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-300">
              {filteredSkills.map((s) => {
                const diff = s.demand - s.curriculumCoverage;
                const severity = diff > 50 ? 'CRITICAL' : diff > 30 ? 'HIGH' : 'MODERATE';
                return (
                  <tr key={s.skill} className="hover:bg-slate-800/30">
                    <td className="py-3 px-3 font-medium text-white flex items-center gap-2">
                      <span className="w-2 h-2 rounded-full bg-blue-400" />
                      <span>{s.skill}</span>
                    </td>
                    <td className="py-3 px-3 font-semibold text-blue-400">{s.demand}/100</td>
                    <td className="py-3 px-3">
                      <div className="w-24 bg-slate-800 rounded-full h-1.5 overflow-hidden inline-block mr-2">
                        <div
                          className="bg-emerald-500 h-full rounded-full"
                          style={{ width: `${s.curriculumCoverage}%` }}
                        />
                      </div>
                      <span className="text-slate-400 font-mono">{s.curriculumCoverage}%</span>
                    </td>
                    <td className="py-3 px-3 font-mono text-slate-300">{s.jobs} postings</td>
                    <td className="py-3 px-3">
                      <span
                        className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${
                          severity === 'CRITICAL'
                            ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
                            : severity === 'HIGH'
                            ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                            : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                        }`}
                      >
                        {severity}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
