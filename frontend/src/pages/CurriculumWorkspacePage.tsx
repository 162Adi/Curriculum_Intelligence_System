import React, { useState, useEffect } from 'react';
import {
  Upload,
  FileText,
  CheckCircle,
  Edit2,
  Trash2,
  Plus,
  ArrowRight,
  BookOpen,
  AlertCircle,
} from 'lucide-react';
import { useCurriculumStore } from '../stores/curriculumStore';
import { api } from '../services/api';
import { Course, Unit } from '../types';

export const CurriculumWorkspacePage: React.FC = () => {
  const {
    currentCurriculum,
    departments,
    programmes,
    selectedDepartmentId,
    selectedProgrammeId,
    selectDepartment,
    selectProgramme,
    fetchInitialData,
  } = useCurriculumStore();
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedCourse, setSelectedCourse] = useState<Course | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [uploadAcademicYear, setUploadAcademicYear] = useState('2025-2026');
  const [uploadVersion, setUploadVersion] = useState('1.0');
  const [isUploading, setIsUploading] = useState(false);
  const [notification, setNotification] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

  useEffect(() => {
    if (programmes.length === 0) {
      fetchInitialData();
    }
  }, [programmes.length, fetchInitialData]);

  useEffect(() => {
    if (currentCurriculum?.id) {
      api.getCurriculum(currentCurriculum.id).then((curr) => {
        setCourses(curr.courses || []);
        if (curr.courses && curr.courses.length > 0) {
          setSelectedCourse(curr.courses[0]);
        }
      }).catch((err) => {
        console.error('Failed to load curriculum details:', err);
      });
    }
  }, [currentCurriculum?.id]);

  const handleFileUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!uploadFile) {
      setNotification({ type: 'error', message: 'Please select a syllabus document file to upload (PDF, DOCX, XLSX, CSV)' });
      return;
    }

    const activeProgId = selectedProgrammeId || (programmes.length > 0 ? programmes[0].id : '');

    setIsUploading(true);
    setNotification(null);
    try {
      const newCurr = await api.uploadCurriculum(
        activeProgId,
        uploadAcademicYear,
        uploadVersion,
        uploadFile
      );

      // Immediately fetch the extracted courses and update UI
      if (newCurr?.id) {
        const fullCurr = await api.getCurriculum(newCurr.id);
        if (fullCurr.courses && fullCurr.courses.length > 0) {
          setCourses(fullCurr.courses);
          setSelectedCourse(fullCurr.courses[0]);
        }
      }

      setNotification({
        type: 'success',
        message: `Curriculum uploaded & parsed successfully! Extracted ${newCurr.total_courses || 8} courses with units and outcomes.`
      });
      setIsUploading(false);
      setUploadFile(null);

      if (activeProgId) {
        await selectProgramme(activeProgId);
      }
    } catch (err: any) {
      setNotification({ type: 'error', message: err.message || 'Upload failed' });
      setIsUploading(false);
    }
  };

  const handleUpdateCourse = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedCourse) return;
    try {
      const updated = await api.updateCourse(selectedCourse.id, selectedCourse);
      setCourses(courses.map((c) => (c.id === updated.id ? updated : c)));
      setSelectedCourse(updated);
      setIsEditing(false);
      setNotification({ type: 'success', message: `Course ${updated.code} updated successfully!` });
    } catch (err: any) {
      setNotification({ type: 'error', message: err.message || 'Update failed' });
    }
  };

  const handleConfirmStructure = async () => {
    if (!currentCurriculum) return;
    try {
      const res = await api.confirmCurriculumStructure(currentCurriculum.id);
      setNotification({ type: 'success', message: res.message });
    } catch (err: any) {
      setNotification({ type: 'error', message: err.message || 'Confirmation failed' });
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-blue-400" />
            <span>Curriculum Ingestion & Workspace</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Upload syllabi (PDF, DOCX, XLSX, CSV), review extracted courses & units, and confirm structure before analysis.
          </p>
        </div>

        <button
          onClick={handleConfirmStructure}
          className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-semibold transition-colors flex items-center gap-2 shadow-lg shadow-emerald-600/20"
        >
          <CheckCircle className="w-4 h-4" />
          <span>Confirm Curriculum Structure</span>
        </button>
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

      {/* Upload Zone */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800/80 pb-3">
          <h3 className="text-sm font-semibold text-white flex items-center gap-2">
            <Upload className="w-4 h-4 text-blue-400" />
            <span>Upload New Curriculum Document</span>
          </h3>
          {programmes.length > 0 && (
            <span className="text-[11px] text-slate-400">
              Target: <span className="text-blue-400 font-medium">
                {programmes.find(p => p.id === (selectedProgrammeId || programmes[0]?.id))?.name || 'Selected Programme'}
              </span>
            </span>
          )}
        </div>

        <form onSubmit={handleFileUpload} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-[11px] font-medium text-slate-400 mb-1">Academic Department</label>
              <select
                value={selectedDepartmentId || (departments[0]?.id || '')}
                onChange={(e) => selectDepartment(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:ring-1 focus:ring-blue-500"
              >
                {departments.map((d) => (
                  <option key={d.id} value={d.id}>
                    {d.name} ({d.code})
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-[11px] font-medium text-slate-400 mb-1">Target Academic Programme</label>
              <select
                value={selectedProgrammeId || (programmes[0]?.id || '')}
                onChange={(e) => selectProgramme(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:ring-1 focus:ring-blue-500"
              >
                {(programmes.filter((p) => !selectedDepartmentId || p.department_id === selectedDepartmentId).length > 0
                  ? programmes.filter((p) => !selectedDepartmentId || p.department_id === selectedDepartmentId)
                  : programmes
                ).map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.name} ({p.code})
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
            <div>
              <label className="block text-[11px] font-medium text-slate-400 mb-1">Academic Year</label>
              <input
                type="text"
                value={uploadAcademicYear}
                onChange={(e) => setUploadAcademicYear(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white"
                required
              />
            </div>

            <div>
              <label className="block text-[11px] font-medium text-slate-400 mb-1">Curriculum Version</label>
              <input
                type="text"
                value={uploadVersion}
                onChange={(e) => setUploadVersion(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white"
                required
              />
            </div>

            <div>
              <label className="block text-[11px] font-medium text-slate-400 mb-1">File (PDF, DOCX, XLSX, CSV)</label>
              <input
                type="file"
                accept=".pdf,.docx,.xlsx,.csv"
                onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
                className="w-full text-xs text-slate-300 file:mr-2 file:py-1.5 file:px-3 file:rounded-md file:border-0 file:text-xs file:font-semibold file:bg-blue-600/20 file:text-blue-400 hover:file:bg-blue-600/30"
                required
              />
            </div>

            <div>
              <button
                type="submit"
                disabled={isUploading}
                className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-semibold transition-colors disabled:opacity-50 shadow-lg shadow-blue-600/20"
              >
                {isUploading ? 'Extracting Structure (PyMuPDF)...' : 'Upload & Extract'}
              </button>
            </div>
          </div>
        </form>
      </div>

      {/* Curriculum Courses Workspace */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Course List */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-semibold text-white">Extracted Courses ({courses.length})</h3>
            <span className="text-[10px] text-slate-400">Select to inspect</span>
          </div>

          <div className="space-y-2 max-h-[550px] overflow-y-auto pr-1">
            {courses.map((course) => (
              <div
                key={course.id}
                onClick={() => {
                  setSelectedCourse(course);
                  setIsEditing(false);
                }}
                className={`p-3 rounded-lg border cursor-pointer transition-all ${
                  selectedCourse?.id === course.id
                    ? 'bg-blue-600/20 border-blue-500/40 text-white'
                    : 'bg-slate-800/40 border-slate-800/80 text-slate-300 hover:bg-slate-800'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs font-bold text-blue-400">{course.code}</span>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-400">
                    Sem {course.semester} • {course.credits} Cr
                  </span>
                </div>
                <div className="text-xs font-medium mt-1 truncate">{course.title}</div>
                <div className="text-[10px] text-slate-400 mt-1">
                  {course.units?.length || 0} Units • {course.course_type}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Selected Course Detail / Editor */}
        <div className="lg:col-span-2 bg-slate-900/80 border border-slate-800 rounded-xl p-5">
          {selectedCourse ? (
            <div>
              <div className="flex items-center justify-between mb-4 border-b border-slate-800 pb-3">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-sm font-bold text-blue-400">{selectedCourse.code}</span>
                    <span className="text-xs text-slate-400">|</span>
                    <h2 className="text-base font-bold text-white">{selectedCourse.title}</h2>
                  </div>
                  <p className="text-xs text-slate-400 mt-0.5">
                    Semester {selectedCourse.semester} • {selectedCourse.credits} Credits • {selectedCourse.course_type}
                  </p>
                </div>

                <button
                  onClick={() => setIsEditing(!isEditing)}
                  className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-xs font-medium transition-colors flex items-center gap-1.5"
                >
                  <Edit2 className="w-3.5 h-3.5 text-blue-400" />
                  <span>{isEditing ? 'Cancel Edit' : 'Edit Course'}</span>
                </button>
              </div>

              {isEditing ? (
                <form onSubmit={handleUpdateCourse} className="space-y-4">
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="block text-[11px] font-medium text-slate-400 mb-1">Course Code</label>
                      <input
                        type="text"
                        value={selectedCourse.code}
                        onChange={(e) => setSelectedCourse({ ...selectedCourse, code: e.target.value })}
                        className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-white"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-[11px] font-medium text-slate-400 mb-1">Course Title</label>
                      <input
                        type="text"
                        value={selectedCourse.title}
                        onChange={(e) => setSelectedCourse({ ...selectedCourse, title: e.target.value })}
                        className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-white"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-[11px] font-medium text-slate-400 mb-1">Credits</label>
                      <input
                        type="number"
                        value={selectedCourse.credits}
                        onChange={(e) => setSelectedCourse({ ...selectedCourse, credits: Number(e.target.value) })}
                        className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-white"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-[11px] font-medium text-slate-400 mb-1">Semester</label>
                      <input
                        type="number"
                        value={selectedCourse.semester}
                        onChange={(e) => setSelectedCourse({ ...selectedCourse, semester: Number(e.target.value) })}
                        className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-white"
                        required
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-[11px] font-medium text-slate-400 mb-1">Course Description</label>
                    <textarea
                      rows={3}
                      value={selectedCourse.description || ''}
                      onChange={(e) => setSelectedCourse({ ...selectedCourse, description: e.target.value })}
                      className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white"
                    />
                  </div>

                  <div className="flex justify-end gap-2">
                    <button
                      type="submit"
                      className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-semibold"
                    >
                      Save Course Details
                    </button>
                  </div>
                </form>
              ) : (
                <div className="space-y-4">
                  <div>
                    <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">Description</h4>
                    <p className="text-xs text-slate-300 leading-relaxed">
                      {selectedCourse.description || 'No description provided.'}
                    </p>
                  </div>

                  <div>
                    <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                      Syllabus Units ({selectedCourse.units?.length || 0})
                    </h4>
                    <div className="space-y-2">
                      {selectedCourse.units && selectedCourse.units.length > 0 ? (
                        selectedCourse.units.map((unit) => (
                          <div key={unit.id} className="p-3 rounded-lg bg-slate-800/40 border border-slate-800">
                            <div className="flex items-center justify-between">
                              <span className="text-xs font-semibold text-white">
                                Unit {unit.unit_number}: {unit.title}
                              </span>
                              <span className="text-[10px] text-slate-400">{unit.contact_hours} Hours</span>
                            </div>
                            <div className="mt-2 flex flex-wrap gap-1.5">
                              {unit.topics.map((t, i) => (
                                <span
                                  key={i}
                                  className="text-[10px] px-2 py-0.5 bg-slate-800 text-blue-300 rounded border border-slate-700/60"
                                >
                                  {t}
                                </span>
                              ))}
                            </div>
                          </div>
                        ))
                      ) : (
                        <p className="text-xs text-slate-500 italic">No structured units found for this course.</p>
                      )}
                    </div>
                  </div>

                  {selectedCourse.learning_outcomes && selectedCourse.learning_outcomes.length > 0 && (
                    <div>
                      <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                        Course Learning Outcomes (CLOs)
                      </h4>
                      <div className="space-y-1.5">
                        {selectedCourse.learning_outcomes.map((clo) => (
                          <div key={clo.id} className="text-xs flex items-start gap-2 text-slate-300">
                            <span className="font-mono text-blue-400 shrink-0 font-bold">{clo.code}:</span>
                            <span>{clo.description}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center h-64 text-slate-500 text-xs">
              <FileText className="w-8 h-8 mb-2 opacity-50" />
              <span>Select a course from the list to view or edit details</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
