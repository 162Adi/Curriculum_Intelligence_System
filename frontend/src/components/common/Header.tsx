import React from 'react';
import { LogOut, RefreshCw, Bell, Sparkles } from 'lucide-react';
import { useAuthStore } from '../../stores/authStore';
import { useCurriculumStore } from '../../stores/curriculumStore';

export const Header: React.FC = () => {
  const { user, logout } = useAuthStore();
  const {
    departments,
    programmes,
    selectedDepartmentId,
    selectedProgrammeId,
    selectDepartment,
    selectProgramme,
    currentCurriculum,
    fetchInitialData,
  } = useCurriculumStore();

  return (
    <header className="h-16 bg-slate-900/90 backdrop-blur-md border-b border-slate-800 fixed top-0 right-0 left-64 z-20 px-6 flex items-center justify-between">
      {/* Programme & Department Selector */}
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2">
          <label className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Dept:</label>
          <select
            value={selectedDepartmentId || ''}
            onChange={(e) => selectDepartment(e.target.value)}
            className="bg-slate-800 border border-slate-700 text-xs text-slate-200 rounded-md px-2.5 py-1.5 focus:outline-none focus:ring-1 focus:ring-blue-500"
          >
            {departments.map((dept) => (
              <option key={dept.id} value={dept.id}>
                {dept.name} ({dept.code})
              </option>
            ))}
          </select>
        </div>

        <div className="flex items-center gap-2">
          <label className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Programme:</label>
          <select
            value={selectedProgrammeId || ''}
            onChange={(e) => selectProgramme(e.target.value)}
            className="bg-slate-800 border border-slate-700 text-xs text-slate-200 rounded-md px-2.5 py-1.5 focus:outline-none focus:ring-1 focus:ring-blue-500"
          >
            {(programmes.filter((p) => !selectedDepartmentId || p.department_id === selectedDepartmentId).length > 0
              ? programmes.filter((p) => !selectedDepartmentId || p.department_id === selectedDepartmentId)
              : programmes
            ).map((prog) => (
              <option key={prog.id} value={prog.id}>
                {prog.name} ({prog.code})
              </option>
            ))}
          </select>
        </div>

        {currentCurriculum && (
          <span className="text-[11px] px-2 py-0.5 bg-blue-500/20 text-blue-400 border border-blue-500/30 rounded-full font-mono">
            v{currentCurriculum.version} ({currentCurriculum.academic_year})
          </span>
        )}
      </div>

      {/* Actions and Profile */}
      <div className="flex items-center gap-4">
        <button
          onClick={() => fetchInitialData()}
          title="Refresh Data"
          className="p-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-lg transition-colors"
        >
          <RefreshCw className="w-4 h-4" />
        </button>

        <div className="flex items-center gap-2 px-3 py-1 bg-slate-800/60 rounded-full border border-slate-700/60 text-xs text-slate-300">
          <Sparkles className="w-3.5 h-3.5 text-blue-400" />
          <span>LangGraph + MCP Active</span>
        </div>

        <button
          onClick={logout}
          className="flex items-center gap-1.5 text-xs text-rose-400 hover:text-rose-300 hover:bg-rose-500/10 px-3 py-1.5 rounded-md transition-colors border border-rose-500/20"
        >
          <LogOut className="w-3.5 h-3.5" />
          <span>Logout</span>
        </button>
      </div>
    </header>
  );
};
