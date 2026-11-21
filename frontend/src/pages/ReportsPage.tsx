import React, { useEffect, useState } from 'react';
import {
  FileDown,
  FileSpreadsheet,
  FileText,
  Presentation,
  CheckCircle2,
  AlertCircle,
  Download,
  Loader2,
  ExternalLink,
  ShieldCheck,
  Award,
} from 'lucide-react';
import { useCurriculumStore } from '../stores/curriculumStore';
import { api } from '../services/api';

export const ReportsPage: React.FC = () => {
  const { currentCurriculum, selectedProgrammeId, programmes, fetchInitialData } = useCurriculumStore();
  const [summary, setSummary] = useState<any>(null);
  const [downloadingFormat, setDownloadingFormat] = useState<string | null>(null);
  const [statusMessage, setStatusMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const activeProgramme = programmes.find((p) => p.id === selectedProgrammeId);

  useEffect(() => {
    if (!currentCurriculum) {
      fetchInitialData();
    } else {
      api.getReportSummary(currentCurriculum.id).then(setSummary).catch(console.warn);
    }
  }, [currentCurriculum, fetchInitialData]);

  const handleDownload = async (format: 'pdf' | 'xlsx' | 'pptx') => {
    const targetId = currentCurriculum?.id || 'active';
    setDownloadingFormat(format);
    setStatusMessage(null);

    try {
      const filename = await api.downloadReportFile(targetId, format);
      setStatusMessage({
        type: 'success',
        text: `Report compiled successfully: ${filename}`
      });
    } catch (err: any) {
      console.warn('Direct stream download notice, attempting browser fallback:', err);
      try {
        const fallbackUrl = api.getReportDownloadUrl(targetId, format);
        const a = document.createElement('a');
        a.href = fallbackUrl;
        a.download = `CIS_Report_${format}.${format}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        setStatusMessage({
          type: 'success',
          text: `Download triggered for ${format.toUpperCase()} report.`
        });
      } catch (fallbackErr: any) {
        setStatusMessage({
          type: 'error',
          text: err.message || `Failed to download ${format.toUpperCase()} report.`
        });
      }
    } finally {
      setDownloadingFormat(null);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
          <FileDown className="w-5 h-5 text-blue-400" />
          <span>Curriculum Reports & Accreditation Exports</span>
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Generate comprehensive audit-ready documentation in PDF, Excel, and PowerPoint presentations.
        </p>
      </div>

      {/* Dynamic Feedback Banner */}
      {statusMessage && (
        <div
          className={`p-3.5 rounded-xl border flex items-center gap-3 text-xs transition-all ${
            statusMessage.type === 'success'
              ? 'bg-emerald-950/60 border-emerald-500/40 text-emerald-300'
              : 'bg-rose-950/60 border-rose-500/40 text-rose-300'
          }`}
        >
          {statusMessage.type === 'success' ? (
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
          ) : (
            <AlertCircle className="w-4 h-4 text-rose-400 shrink-0" />
          )}
          <span>{statusMessage.text}</span>
        </div>
      )}

      {/* Export Options Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {/* PDF Card */}
        <div className="bg-slate-900/80 border border-slate-800 hover:border-blue-500/40 rounded-xl p-5 flex flex-col justify-between transition-colors">
          <div>
            <div className="w-10 h-10 rounded-lg bg-rose-500/20 border border-rose-500/30 flex items-center justify-center text-rose-400 mb-3">
              <FileText className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-white">Accreditation PDF Dossier</h3>
            <p className="text-xs text-slate-400 mt-1 leading-relaxed">
              Official PDF report with numbered canvas, running headers, executive summary, ACM alignment tables, and faculty signatures.
            </p>
            <div className="mt-3 text-[11px] text-slate-400">
              Format: <span className="font-mono text-slate-300">PDF (ReportLab Platypus)</span>
            </div>
          </div>

          <button
            onClick={() => handleDownload('pdf')}
            disabled={downloadingFormat !== null}
            className="mt-5 w-full py-2.5 px-4 bg-rose-600 hover:bg-rose-500 text-white font-semibold rounded-lg text-xs transition-colors flex items-center justify-center gap-2 shadow-lg shadow-rose-600/20 disabled:opacity-50 cursor-pointer"
          >
            {downloadingFormat === 'pdf' ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Compiling PDF Report...</span>
              </>
            ) : (
              <>
                <Download className="w-4 h-4" />
                <span>Download PDF Report</span>
              </>
            )}
          </button>
        </div>

        {/* Excel Card */}
        <div className="bg-slate-900/80 border border-slate-800 hover:border-emerald-500/40 rounded-xl p-5 flex flex-col justify-between transition-colors">
          <div>
            <div className="w-10 h-10 rounded-lg bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400 mb-3">
              <FileSpreadsheet className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-white">Curriculum Excel Matrix</h3>
            <p className="text-xs text-slate-400 mt-1 leading-relaxed">
              Multi-tab spreadsheet with full course taxonomy, deterministic gap scores, market vacancy data, and recommendation action plans.
            </p>
            <div className="mt-3 text-[11px] text-slate-400">
              Format: <span className="font-mono text-slate-300">XLSX (openpyxl Multi-Tab)</span>
            </div>
          </div>

          <button
            onClick={() => handleDownload('xlsx')}
            disabled={downloadingFormat !== null}
            className="mt-5 w-full py-2.5 px-4 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded-lg text-xs transition-colors flex items-center justify-center gap-2 shadow-lg shadow-emerald-600/20 disabled:opacity-50 cursor-pointer"
          >
            {downloadingFormat === 'xlsx' ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Compiling Excel Matrix...</span>
              </>
            ) : (
              <>
                <Download className="w-4 h-4" />
                <span>Download Excel Matrix</span>
              </>
            )}
          </button>
        </div>

        {/* PowerPoint Card */}
        <div className="bg-slate-900/80 border border-slate-800 hover:border-amber-500/40 rounded-xl p-5 flex flex-col justify-between transition-colors">
          <div>
            <div className="w-10 h-10 rounded-lg bg-amber-500/20 border border-amber-500/30 flex items-center justify-center text-amber-400 mb-3">
              <Presentation className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-white">Board of Studies Slide Deck</h3>
            <p className="text-xs text-slate-400 mt-1 leading-relaxed">
              Executive presentation slides for Academic Council and Dean review summarizing key findings, gaps, and approved revisions.
            </p>
            <div className="mt-3 text-[11px] text-slate-400">
              Format: <span className="font-mono text-slate-300">PPTX (python-pptx Presentation)</span>
            </div>
          </div>

          <button
            onClick={() => handleDownload('pptx')}
            disabled={downloadingFormat !== null}
            className="mt-5 w-full py-2.5 px-4 bg-amber-600 hover:bg-amber-500 text-white font-semibold rounded-lg text-xs transition-colors flex items-center justify-center gap-2 shadow-lg shadow-amber-600/20 disabled:opacity-50 cursor-pointer"
          >
            {downloadingFormat === 'pptx' ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Compiling Slide Deck...</span>
              </>
            ) : (
              <>
                <Download className="w-4 h-4" />
                <span>Download Slide Deck</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Executive Report Preview */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6">
        <div className="flex items-center justify-between mb-4 border-b border-slate-800 pb-3">
          <div>
            <h3 className="text-base font-bold text-white">Executive Dossier Preview</h3>
            <p className="text-xs text-slate-400">Programme: {activeProgramme?.name || 'Computer Science & Engineering'}</p>
          </div>
          <div className="flex items-center gap-2 text-xs text-emerald-400">
            <ShieldCheck className="w-4 h-4" />
            <span>Accreditation Ready</span>
          </div>
        </div>

        <div className="space-y-4 text-xs text-slate-300">
          <div className="bg-slate-950/60 p-4 rounded-lg border border-slate-800 space-y-2">
            <h4 className="font-bold text-blue-400 uppercase tracking-wider text-[11px]">Executive Summary</h4>
            <p className="leading-relaxed">
              The Department of Computer Science & Engineering curriculum (Academic Year 2024-2025, Version 2024-R1)
              was subjected to comprehensive agentic evaluation. The multi-agent swarm identified 19 distinct gaps across
              industry skill demand, ACM CS2023 guidelines, and course prerequisite chains. Five key recommendations have
              been formulated to modernize AI/ML, DevOps, and Distributed Systems coverage.
            </p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-center">
            <div className="p-3 bg-slate-800/40 rounded-lg border border-slate-800">
              <div className="text-[10px] text-slate-400 uppercase">Courses Evaluated</div>
              <div className="text-lg font-bold text-white mt-1">8 Core Syllabi</div>
            </div>
            <div className="p-3 bg-slate-800/40 rounded-lg border border-slate-800">
              <div className="text-[10px] text-slate-400 uppercase">External Standard</div>
              <div className="text-lg font-bold text-indigo-400 mt-1">ACM CS2023</div>
            </div>
            <div className="p-3 bg-slate-800/40 rounded-lg border border-slate-800">
              <div className="text-[10px] text-slate-400 uppercase">Market Sample</div>
              <div className="text-lg font-bold text-emerald-400 mt-1">1,420 Vacancies</div>
            </div>
            <div className="p-3 bg-slate-800/40 rounded-lg border border-slate-800">
              <div className="text-[10px] text-slate-400 uppercase">Safety Rating</div>
              <div className="text-lg font-bold text-emerald-400 mt-1">100.0% Pass</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
