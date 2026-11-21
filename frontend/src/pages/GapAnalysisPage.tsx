import React, { useEffect, useState } from 'react';
import {
  AlertTriangle,
  Search,
  Filter,
  CheckCircle2,
  BookOpen,
  Calculator,
  Layers,
  ChevronRight,
} from 'lucide-react';
import { useCurriculumStore } from '../stores/curriculumStore';
import { api } from '../services/api';
import { Gap } from '../types';

export const GapAnalysisPage: React.FC = () => {
  const { currentCurriculum } = useCurriculumStore();
  const [gaps, setGaps] = useState<Gap[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('ALL');
  const [selectedSeverity, setSelectedSeverity] = useState<string>('ALL');
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (currentCurriculum) {
      setLoading(true);
      api.getGaps(currentCurriculum.id).then((data) => {
        setGaps(data);
        setLoading(false);
      });
    }
  }, [currentCurriculum]);

  const filteredGaps = gaps.filter((gap) => {
    const matchesCategory = selectedCategory === 'ALL' || gap.category === selectedCategory;
    const matchesSeverity = selectedSeverity === 'ALL' || gap.severity === selectedSeverity;
    const matchesSearch =
      gap.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      gap.description.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesCategory && matchesSeverity && matchesSearch;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-amber-400" />
          <span>Curriculum Gap Analysis & Severity Calculation</span>
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Evidence-based gap detection across industry competencies, academic standards, and prerequisites.
        </p>
      </div>

      {/* Mathematical Formula Callout */}
      <div className="bg-slate-900/90 border border-amber-500/30 rounded-xl p-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-amber-500/20 border border-amber-500/30 flex items-center justify-center text-amber-400">
            <Calculator className="w-5 h-5" />
          </div>
          <div>
            <div className="text-xs font-semibold text-amber-400 uppercase tracking-wider">
              Deterministic Scoring Engine
            </div>
            <div className="text-sm font-bold text-white mt-0.5 font-mono">
              Gap Score = Importance × (1.0 − Current Coverage)
            </div>
          </div>
        </div>

        <div className="flex items-center gap-4 text-xs text-slate-300">
          <div><span className="text-rose-400 font-bold">Critical:</span> Score &ge; 70</div>
          <div><span className="text-amber-400 font-bold">High:</span> Score &ge; 45</div>
          <div><span className="text-yellow-400 font-bold">Medium:</span> Score &ge; 25</div>
          <div><span className="text-blue-400 font-bold">Low:</span> Score &lt; 25</div>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 bg-slate-900/80 border border-slate-800 p-3 rounded-xl">
        <div className="flex flex-wrap items-center gap-2">
          <Filter className="w-4 h-4 text-slate-400 mr-1" />
          <span className="text-xs text-slate-400 mr-1">Category:</span>
          {['ALL', 'INDUSTRY_SKILL', 'ACADEMIC_STANDARD', 'PREREQUISITE', 'PEDAGOGICAL'].map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`text-xs px-2.5 py-1 rounded-lg transition-colors ${
                selectedCategory === cat
                  ? 'bg-blue-600 text-white font-medium'
                  : 'bg-slate-800 text-slate-400 hover:text-slate-200'
              }`}
            >
              {cat.replace('_', ' ')}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-3">
          <select
            value={selectedSeverity}
            onChange={(e) => setSelectedSeverity(e.target.value)}
            className="bg-slate-800 border border-slate-700 text-xs text-slate-200 rounded-lg px-2.5 py-1.5 focus:outline-none"
          >
            <option value="ALL">All Severities</option>
            <option value="CRITICAL">Critical</option>
            <option value="HIGH">High</option>
            <option value="MEDIUM">Medium</option>
            <option value="LOW">Low</option>
          </select>

          <div className="relative">
            <Search className="w-3.5 h-3.5 absolute left-3 top-2.5 text-slate-400" />
            <input
              type="text"
              placeholder="Search gaps..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="bg-slate-800 border border-slate-700 text-xs text-slate-200 rounded-lg pl-8 pr-3 py-1.5 focus:outline-none"
            />
          </div>
        </div>
      </div>

      {/* Gap Cards List */}
      <div className="space-y-3">
        {loading ? (
          <div className="text-center py-12 text-slate-400 text-xs">Loading identified gaps...</div>
        ) : filteredGaps.length === 0 ? (
          <div className="text-center py-12 text-slate-500 text-xs bg-slate-900/40 rounded-xl border border-slate-800">
            No curriculum gaps found matching your filter criteria.
          </div>
        ) : (
          filteredGaps.map((gap) => (
            <div
              key={gap.id}
              className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 hover:border-slate-700 transition-colors"
            >
              <div className="flex flex-col md:flex-row md:items-start justify-between gap-3">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1.5">
                    <span
                      className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                        gap.severity === 'CRITICAL'
                          ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
                          : gap.severity === 'HIGH'
                          ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                          : gap.severity === 'MEDIUM'
                          ? 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30'
                          : 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                      }`}
                    >
                      {gap.severity}
                    </span>

                    <span className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-400 font-mono">
                      {gap.category}
                    </span>
                  </div>

                  <h3 className="text-sm font-bold text-white">{gap.title}</h3>
                  <p className="text-xs text-slate-300 mt-1 leading-relaxed">{gap.description}</p>

                  {gap.evidence && (
                    <div className="mt-2 text-[11px] text-slate-400 bg-slate-950/60 p-2.5 rounded-lg border border-slate-800/80">
                      <span className="font-semibold text-slate-300">Evidence Citation: </span>
                      <span>{gap.evidence.details || gap.evidence.citation}</span>
                    </div>
                  )}

                  {gap.affected_courses && gap.affected_courses.length > 0 && (
                    <div className="mt-2 flex items-center gap-1.5 flex-wrap">
                      <span className="text-[10px] text-slate-400">Affected Courses:</span>
                      {gap.affected_courses.map((courseCode, i) => (
                        <span
                          key={i}
                          className="text-[10px] px-2 py-0.5 rounded bg-blue-600/20 text-blue-300 border border-blue-500/30 font-mono"
                        >
                          {courseCode}
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                {/* Score Breakdown Pill */}
                <div className="bg-slate-950 border border-slate-800 rounded-lg p-3 shrink-0 flex flex-col items-center justify-center min-w-[150px]">
                  <div className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider">Gap Score</div>
                  <div className="text-xl font-bold font-mono text-amber-400 mt-0.5">
                    {gap.gap_score.toFixed(1)}
                  </div>
                  <div className="text-[9px] text-slate-500 font-mono mt-1">
                    Imp: {gap.importance_score} | Cov: {(gap.current_coverage * 100).toFixed(0)}%
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
