import React, { useEffect, useState } from 'react';
import {
  Sparkles,
  BookOpen,
  Edit2,
  CheckCircle2,
  Clock,
  ArrowRight,
  PlusCircle,
  FileText,
  AlertCircle,
} from 'lucide-react';
import { useCurriculumStore } from '../stores/curriculumStore';
import { api } from '../services/api';
import { Recommendation } from '../types';

export const RecommendationsPage: React.FC = () => {
  const { currentCurriculum } = useCurriculumStore();
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [editingRec, setEditingRec] = useState<Recommendation | null>(null);
  const [notification, setNotification] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

  useEffect(() => {
    if (currentCurriculum) {
      api.getRecommendations(currentCurriculum.id).then(setRecommendations);
    }
  }, [currentCurriculum]);

  const handleSaveEdit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingRec) return;

    try {
      const updated = await api.updateRecommendation(editingRec.id, {
        title: editingRec.title,
        proposed_action: editingRec.proposed_action,
        rationale: editingRec.rationale,
        estimated_hours: editingRec.estimated_hours,
        priority: editingRec.priority,
      });

      setRecommendations(recommendations.map((r) => (r.id === updated.id ? updated : r)));
      setEditingRec(null);
      setNotification({ type: 'success', message: 'Recommendation updated successfully!' });
    } catch (err: any) {
      setNotification({ type: 'error', message: err.message || 'Update failed' });
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-indigo-400" />
          <span>Curriculum AI Recommendations & Revision Proposals</span>
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Generated curriculum interventions created in DRAFT status awaiting faculty inspection and approval.
        </p>
      </div>

      {notification && (
        <div
          className={`p-3 rounded-lg text-xs flex items-center gap-2 ${
            notification.type === 'success'
              ? 'bg-emerald-500/10 border border-emerald-500/30 text-emerald-400'
              : 'bg-rose-500/10 border border-rose-500/30 text-rose-400'
          }`}
        >
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{notification.message}</span>
        </div>
      )}

      {/* Recommendations Cards */}
      <div className="grid grid-cols-1 gap-4">
        {recommendations.map((rec) => (
          <div
            key={rec.id}
            className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 hover:border-slate-700 transition-colors"
          >
            <div className="flex flex-col md:flex-row md:items-start justify-between gap-4 mb-3">
              <div>
                <div className="flex items-center gap-2 mb-1.5">
                  <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-full bg-indigo-500/20 text-indigo-400 border border-indigo-500/30 font-mono">
                    {rec.recommendation_type}
                  </span>

                  <span
                    className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${
                      rec.approval_status === 'APPROVED'
                        ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                        : rec.approval_status === 'REJECTED'
                        ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
                        : 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                    }`}
                  >
                    STATUS: {rec.approval_status}
                  </span>

                  <span className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-400">
                    Priority: {rec.priority}
                  </span>
                </div>

                <h3 className="text-sm font-bold text-white">{rec.title}</h3>
              </div>

              <button
                onClick={() => setEditingRec(rec)}
                className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-xs font-medium transition-colors flex items-center gap-1.5 shrink-0"
              >
                <Edit2 className="w-3.5 h-3.5 text-blue-400" />
                <span>Edit Proposal</span>
              </button>
            </div>

            {/* Current vs Proposed Diff Card */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-3 bg-slate-950/60 p-3.5 rounded-lg border border-slate-800">
              <div>
                <div className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider mb-1">
                  Proposed Curriculum Action
                </div>
                <p className="text-xs text-slate-200 leading-relaxed">{rec.proposed_action}</p>
              </div>

              <div>
                <div className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider mb-1">
                  Academic & Industry Rationale
                </div>
                <p className="text-xs text-slate-400 leading-relaxed">{rec.rationale}</p>
              </div>
            </div>

            {/* Target and Hours Footer */}
            <div className="mt-3 flex items-center justify-between text-xs text-slate-400 pt-2 border-t border-slate-800/80">
              <div className="flex items-center gap-3">
                {rec.target_course_name && (
                  <span>
                    Target: <strong className="text-slate-200">{rec.target_course_name}</strong>
                  </span>
                )}
                {rec.target_semester && (
                  <span>
                    Semester: <strong className="text-slate-200">Sem {rec.target_semester}</strong>
                  </span>
                )}
              </div>

              {rec.estimated_hours && (
                <div className="flex items-center gap-1 text-slate-300 font-mono">
                  <Clock className="w-3.5 h-3.5 text-blue-400" />
                  <span>Est: {rec.estimated_hours} Contact Hours</span>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Edit Recommendation Modal */}
      {editingRec && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-xl w-full p-6 shadow-2xl">
            <h3 className="text-base font-bold text-white mb-4">Edit Curriculum Proposal</h3>
            <form onSubmit={handleSaveEdit} className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-400 mb-1">Title</label>
                <input
                  type="text"
                  value={editingRec.title}
                  onChange={(e) => setEditingRec({ ...editingRec, title: e.target.value })}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-400 mb-1">Proposed Action</label>
                <textarea
                  rows={3}
                  value={editingRec.proposed_action}
                  onChange={(e) => setEditingRec({ ...editingRec, proposed_action: e.target.value })}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-400 mb-1">Rationale</label>
                <textarea
                  rows={3}
                  value={editingRec.rationale}
                  onChange={(e) => setEditingRec({ ...editingRec, rationale: e.target.value })}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-slate-400 mb-1">Estimated Contact Hours</label>
                  <input
                    type="number"
                    value={editingRec.estimated_hours || 0}
                    onChange={(e) => setEditingRec({ ...editingRec, estimated_hours: Number(e.target.value) })}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-white"
                  />
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-400 mb-1">Priority</label>
                  <select
                    value={editingRec.priority}
                    onChange={(e) => setEditingRec({ ...editingRec, priority: e.target.value as any })}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-white"
                  >
                    <option value="LOW">Low</option>
                    <option value="MEDIUM">Medium</option>
                    <option value="HIGH">High</option>
                  </select>
                </div>
              </div>

              <div className="flex justify-end gap-3 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setEditingRec(null)}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded-lg text-xs"
                >
                  Save Changes
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
