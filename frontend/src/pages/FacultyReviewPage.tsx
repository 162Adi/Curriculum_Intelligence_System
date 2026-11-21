import React, { useEffect, useState } from 'react';
import {
  CheckCircle2,
  XCircle,
  AlertCircle,
  FileCheck,
  Send,
  MessageSquare,
  History,
  ShieldCheck,
  UserCheck,
} from 'lucide-react';
import { useCurriculumStore } from '../stores/curriculumStore';
import { api } from '../services/api';
import { Recommendation, ApprovalRecord } from '../types';

export const FacultyReviewPage: React.FC = () => {
  const { currentCurriculum, selectProgramme, selectedProgrammeId } = useCurriculumStore();
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [approvals, setApprovals] = useState<ApprovalRecord[]>([]);
  const [comments, setComments] = useState<Record<string, string>>({});
  const [signoffComment, setSignoffComment] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [notification, setNotification] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

  useEffect(() => {
    if (currentCurriculum) {
      loadData();
    }
  }, [currentCurriculum]);

  const loadData = async () => {
    if (!currentCurriculum) return;
    const [recs, apprs] = await Promise.all([
      api.getRecommendations(currentCurriculum.id),
      api.getApprovals(currentCurriculum.id).catch(() => []),
    ]);
    setRecommendations(recs);
    setApprovals(apprs);
  };

  const handleDecision = async (recId: string, decision: 'APPROVED' | 'REJECTED' | 'REVISE') => {
    try {
      await api.submitApprovalDecision(recId, decision, comments[recId] || '');
      setNotification({
        type: 'success',
        message: `Recommendation marked as ${decision}`,
      });
      loadData();
    } catch (err: any) {
      setNotification({ type: 'error', message: err.message || 'Action failed' });
    }
  };

  const handleFinalSignoff = async () => {
    if (!currentCurriculum) return;
    setIsSubmitting(true);
    try {
      const res = await api.signoffFinalCurriculum(currentCurriculum.id, signoffComment);
      setNotification({ type: 'success', message: res.message });
      setIsSubmitting(false);
      if (selectedProgrammeId) {
        selectProgramme(selectedProgrammeId);
      }
    } catch (err: any) {
      setNotification({ type: 'error', message: err.message || 'Signoff failed' });
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
          <UserCheck className="w-5 h-5 text-emerald-400" />
          <span>Faculty Review & Board of Studies Approvals</span>
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Review, approve, or reject AI-generated curriculum modifications. Formal sign-off seals the version for accreditation.
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

      {/* Recommendations Approval Queue */}
      <div className="space-y-4">
        <h2 className="text-sm font-bold text-white flex items-center gap-2">
          <span>Pending Recommendation Queue ({recommendations.length})</span>
        </h2>

        {recommendations.map((rec) => (
          <div
            key={rec.id}
            className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 hover:border-slate-700 transition-colors"
          >
            <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-500/20 text-blue-400 font-mono">
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
                    {rec.approval_status}
                  </span>
                </div>

                <h3 className="text-sm font-bold text-white">{rec.title}</h3>
                <p className="text-xs text-slate-300 mt-1">{rec.proposed_action}</p>

                <div className="mt-2 text-xs text-slate-400 bg-slate-950/50 p-2.5 rounded-lg border border-slate-800">
                  <span className="font-semibold text-slate-300">Rationale: </span>
                  {rec.rationale}
                </div>

                {/* Faculty feedback input */}
                <div className="mt-3 flex items-center gap-2">
                  <MessageSquare className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                  <input
                    type="text"
                    placeholder="Enter faculty review notes or justification..."
                    value={comments[rec.id] || ''}
                    onChange={(e) => setComments({ ...comments, [rec.id]: e.target.value })}
                    className="flex-1 bg-slate-800 border border-slate-700 text-xs text-slate-200 rounded-lg px-3 py-1.5 focus:outline-none"
                  />
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex md:flex-col gap-2 shrink-0">
                <button
                  onClick={() => handleDecision(rec.id, 'APPROVED')}
                  className="px-3.5 py-1.5 bg-emerald-600/20 hover:bg-emerald-600 text-emerald-300 hover:text-white border border-emerald-500/40 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5"
                >
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>Approve</span>
                </button>

                <button
                  onClick={() => handleDecision(rec.id, 'REJECTED')}
                  className="px-3.5 py-1.5 bg-rose-600/20 hover:bg-rose-600 text-rose-300 hover:text-white border border-rose-500/40 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5"
                >
                  <XCircle className="w-3.5 h-3.5" />
                  <span>Reject</span>
                </button>

                <button
                  onClick={() => handleDecision(rec.id, 'REVISE')}
                  className="px-3.5 py-1.5 bg-amber-600/20 hover:bg-amber-600 text-amber-300 hover:text-white border border-amber-500/40 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5"
                >
                  <AlertCircle className="w-3.5 h-3.5" />
                  <span>Revise</span>
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Final Sign-off Box */}
      <div className="bg-gradient-to-r from-blue-950/60 via-slate-900 to-indigo-950/50 border border-blue-500/40 rounded-2xl p-6">
        <div className="flex items-center gap-3 mb-3">
          <div className="w-10 h-10 rounded-xl bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white">Board of Studies Final Curriculum Sign-off</h3>
            <p className="text-xs text-slate-400">
              Formally approve this curriculum version, locking recommendations and generating official accreditation records.
            </p>
          </div>
        </div>

        <div className="space-y-3 mt-4">
          <textarea
            rows={2}
            value={signoffComment}
            onChange={(e) => setSignoffComment(e.target.value)}
            placeholder="Official Board of Studies resolution or approval minutes (e.g. Approved by BoS meeting on 20 Nov 2026)..."
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          />

          <div className="flex justify-end">
            <button
              onClick={handleFinalSignoff}
              disabled={isSubmitting || !currentCurriculum}
              className="px-5 py-2.5 bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded-lg text-xs transition-colors flex items-center gap-2 shadow-lg shadow-blue-600/20 disabled:opacity-50"
            >
              <FileCheck className="w-4 h-4" />
              <span>{isSubmitting ? 'Signing off...' : 'Seal & Approve Curriculum Revision'}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
