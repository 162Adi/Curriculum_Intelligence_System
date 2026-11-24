import React, { useEffect, useState } from 'react';
import {
  CheckCircle2,
  XCircle,
  AlertCircle,
  FileCheck,
  MessageSquare,
  History,
  ShieldCheck,
  UserCheck,
  Clock,
} from 'lucide-react';
import { useCurriculumStore } from '../stores/curriculumStore';
import { api } from '../services/api';
import { Recommendation, ApprovalRecord } from '../types';

export const FacultyReviewPage: React.FC = () => {
  const { currentCurriculum, selectProgramme, selectedProgrammeId, fetchInitialData } = useCurriculumStore();
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [approvals, setApprovals] = useState<ApprovalRecord[]>([]);
  const [comments, setComments] = useState<Record<string, string>>({});
  const [signoffComment, setSignoffComment] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [notification, setNotification] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

  useEffect(() => {
    if (!currentCurriculum) {
      fetchInitialData();
    } else {
      loadData();
    }
  }, [currentCurriculum]);

  const loadData = async () => {
    try {
      const [recs, apprs] = await Promise.all([
        api.getRecommendations(currentCurriculum?.id),
        currentCurriculum ? api.getApprovals(currentCurriculum.id).catch(() => []) : Promise.resolve([]),
      ]);
      setRecommendations(recs || []);
      setApprovals(apprs || []);
    } catch (err: any) {
      console.error('Error loading recommendations or approvals:', err);
    }
  };

  const handleDecision = async (recId: string, decision: 'APPROVED' | 'REJECTED' | 'REVISE') => {
    const targetStatus = decision === 'REVISE' ? 'NEEDS_REVISION' : decision;
    const note = comments[recId] || '';

    // Optimistic UI update for instant feedback
    setRecommendations((prev) =>
      prev.map((r) =>
        r.id === recId || (r as any).recommendation_id === recId
          ? {
              ...r,
              approval_status: targetStatus,
              status: targetStatus,
              faculty_feedback: note || r.faculty_feedback,
              faculty_notes: note || (r as any).faculty_notes,
            }
          : r
      )
    );

    try {
      await api.submitApprovalDecision(recId, decision, note);
      setNotification({
        type: 'success',
        message: `Recommendation marked as ${decision === 'REVISE' ? 'REVISION REQUESTED' : decision}.`,
      });
      setComments((prev) => {
        const next = { ...prev };
        delete next[recId];
        return next;
      });
      await loadData();
    } catch (err: any) {
      setNotification({ type: 'error', message: err.message || 'Action failed' });
      await loadData();
    }
  };

  const handleFinalSignoff = async () => {
    if (!currentCurriculum) return;
    setIsSubmitting(true);
    try {
      const res = await api.signoffFinalCurriculum(currentCurriculum.id, signoffComment);
      setNotification({ type: 'success', message: res.message });
      setIsSubmitting(false);
      setSignoffComment('');
      if (selectedProgrammeId) {
        await selectProgramme(selectedProgrammeId);
      }
      await loadData();
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
          className={`p-3 rounded-lg text-xs flex items-center justify-between gap-2 transition-all ${
            notification.type === 'success'
              ? 'bg-emerald-500/10 border border-emerald-500/30 text-emerald-400'
              : 'bg-rose-500/10 border border-rose-500/30 text-rose-400'
          }`}
        >
          <div className="flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{notification.message}</span>
          </div>
          <button
            onClick={() => setNotification(null)}
            className="text-[10px] opacity-70 hover:opacity-100 underline ml-2"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Recommendations Approval Queue */}
      <div className="space-y-4">
        <h2 className="text-sm font-bold text-white flex items-center gap-2">
          <span>Pending Recommendation Queue ({recommendations.length})</span>
        </h2>

        {recommendations.length === 0 ? (
          <div className="p-8 text-center bg-slate-900/50 rounded-xl border border-slate-800 text-slate-400 text-xs">
            No recommendations currently queued for review. Run an analysis from the dashboard to generate new suggestions.
          </div>
        ) : (
          recommendations.map((rec) => {
            const currentStatus = rec.approval_status || rec.status || 'DRAFT';
            const isApproved = currentStatus === 'APPROVED';
            const isRejected = currentStatus === 'REJECTED';
            const isRevision = currentStatus === 'NEEDS_REVISION' || currentStatus === 'REVISE';

            return (
              <div
                key={rec.id}
                className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 hover:border-slate-700 transition-colors"
              >
                <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-500/20 text-blue-400 font-mono">
                        {rec.recommendation_type || (rec as any).category || 'MODIFICATION'}
                      </span>
                      <span
                        className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${
                          isApproved
                            ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                            : isRejected
                            ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
                            : isRevision
                            ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                            : 'bg-slate-700/50 text-slate-300 border border-slate-600/30'
                        }`}
                      >
                        {isRevision ? 'NEEDS REVISION' : currentStatus}
                      </span>
                    </div>

                    <h3 className="text-sm font-bold text-white">{rec.title}</h3>
                    <p className="text-xs text-slate-300 mt-1">{rec.proposed_action || rec.description}</p>

                    {rec.rationale && (
                      <div className="mt-2 text-xs text-slate-400 bg-slate-950/50 p-2.5 rounded-lg border border-slate-800">
                        <span className="font-semibold text-slate-300">Rationale: </span>
                        {rec.rationale}
                      </div>
                    )}

                    {/* Show saved notes if available */}
                    {(rec.faculty_feedback || (rec as any).faculty_notes) && (
                      <div className="mt-2 text-xs text-emerald-300/90 bg-emerald-950/30 p-2 rounded border border-emerald-800/40">
                        <span className="font-semibold text-emerald-200">Reviewer Notes: </span>
                        {rec.faculty_feedback || (rec as any).faculty_notes}
                      </div>
                    )}

                    {/* Faculty feedback input */}
                    <div className="mt-3 flex items-center gap-2">
                      <MessageSquare className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                      <input
                        type="text"
                        placeholder="Enter faculty review notes or justification..."
                        value={comments[rec.id] || ''}
                        onChange={(e) => setComments({ ...comments, [rec.id]: e.target.value })}
                        className="flex-1 bg-slate-800 border border-slate-700 text-xs text-slate-200 rounded-lg px-3 py-1.5 focus:outline-none focus:border-blue-500"
                      />
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex md:flex-col gap-2 shrink-0">
                    <button
                      onClick={() => handleDecision(rec.id, 'APPROVED')}
                      className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 border ${
                        isApproved
                          ? 'bg-emerald-600 text-white border-emerald-500'
                          : 'bg-emerald-600/20 hover:bg-emerald-600 text-emerald-300 hover:text-white border-emerald-500/40'
                      }`}
                    >
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      <span>Approve</span>
                    </button>

                    <button
                      onClick={() => handleDecision(rec.id, 'REJECTED')}
                      className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 border ${
                        isRejected
                          ? 'bg-rose-600 text-white border-rose-500'
                          : 'bg-rose-600/20 hover:bg-rose-600 text-rose-300 hover:text-white border-rose-500/40'
                      }`}
                    >
                      <XCircle className="w-3.5 h-3.5" />
                      <span>Reject</span>
                    </button>

                    <button
                      onClick={() => handleDecision(rec.id, 'REVISE')}
                      className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 border ${
                        isRevision
                          ? 'bg-amber-600 text-white border-amber-500'
                          : 'bg-amber-600/20 hover:bg-amber-600 text-amber-300 hover:text-white border-amber-500/40'
                      }`}
                    >
                      <AlertCircle className="w-3.5 h-3.5" />
                      <span>Revise</span>
                    </button>
                  </div>
                </div>
              </div>
            );
          })
        )}
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

      {/* Audit Trail Section */}
      {approvals.length > 0 && (
        <div className="space-y-3 pt-2">
          <h2 className="text-sm font-bold text-white flex items-center gap-2">
            <History className="w-4 h-4 text-blue-400" />
            <span>Board & Faculty Review Audit Trail ({approvals.length})</span>
          </h2>
          <div className="bg-slate-900/60 border border-slate-800 rounded-xl overflow-hidden divide-y divide-slate-800">
            {approvals.map((appr) => {
              const isAppr = appr.decision === 'APPROVED';
              const isRej = appr.decision === 'REJECTED';
              return (
                <div key={appr.id} className="p-3.5 flex items-start justify-between gap-4 text-xs">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <span
                        className={`text-[9px] font-semibold px-2 py-0.5 rounded-full ${
                          isAppr
                            ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                            : isRej
                            ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
                            : 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                        }`}
                      >
                        {appr.decision}
                      </span>
                      <span className="font-semibold text-slate-200">
                        {appr.user_name || 'Faculty Member'}
                      </span>
                      <span className="text-[10px] text-slate-500">
                        ({appr.user_role || 'REVIEWER'})
                      </span>
                    </div>
                    {appr.comments && (
                      <p className="text-slate-300 mt-1 text-[11px] bg-slate-950/40 p-2 rounded border border-slate-800/60">
                        {appr.comments}
                      </p>
                    )}
                  </div>
                  <div className="shrink-0 flex items-center gap-1 text-[10px] text-slate-500">
                    <Clock className="w-3 h-3" />
                    <span>{new Date(appr.created_at).toLocaleString()}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};
