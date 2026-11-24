import React, { useEffect, useState } from 'react';
import {
  Users,
  UserPlus,
  Shield,
  CheckCircle2,
  Lock,
  Mail,
  User as UserIcon,
  HardDrive,
  Trash2,
  RefreshCw,
  FileText,
  AlertTriangle,
  Database,
  Layers,
  Clock,
} from 'lucide-react';
import { api } from '../services/api';
import { User, Role, AdminFileItem } from '../types';

export const UsersPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'users' | 'storage'>('users');
  
  // Users state
  const [users, setUsers] = useState<User[]>([]);
  const [showAddModal, setShowAddModal] = useState(false);
  const [newEmail, setNewEmail] = useState('');
  const [newFullName, setNewFullName] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [newRole, setNewRole] = useState<Role>('FACULTY');
  
  // Storage state
  const [files, setFiles] = useState<AdminFileItem[]>([]);
  const [isLoadingFiles, setIsLoadingFiles] = useState(false);
  const [isPurging, setIsPurging] = useState(false);
  
  const [notification, setNotification] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

  useEffect(() => {
    loadUsers();
    loadFiles();
  }, []);

  const loadUsers = () => {
    api.getUsers().then(setUsers).catch(() => {});
  };

  const loadFiles = async () => {
    setIsLoadingFiles(true);
    try {
      const data = await api.getAdminFiles();
      setFiles(data || []);
    } catch (err: any) {
      console.warn('Could not load storage files:', err);
    } finally {
      setIsLoadingFiles(false);
    }
  };

  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.createUser({
        email: newEmail,
        full_name: newFullName,
        password: newPassword,
        role: newRole,
      });
      setNotification({ type: 'success', message: `User ${newEmail} created successfully!` });
      setShowAddModal(false);
      setNewEmail('');
      setNewFullName('');
      setNewPassword('');
      loadUsers();
    } catch (err: any) {
      setNotification({ type: 'error', message: err.message || 'Creation failed' });
    }
  };

  const handleDeleteFile = async (filePath: string, fileName: string) => {
    if (!window.confirm(`Are you sure you want to erase "${fileName}" from disk?\n\nExtracted curriculum courses/units stored in the database will remain 100% safe.`)) {
      return;
    }
    try {
      const res = await api.deleteAdminFile(filePath);
      setNotification({ type: 'success', message: res.message });
      loadFiles();
    } catch (err: any) {
      setNotification({ type: 'error', message: err.message || 'Failed to delete file' });
    }
  };

  const handlePurge = async (target: 'uploads' | 'reports' | 'all') => {
    const label = target === 'uploads' ? 'all raw uploaded syllabus files' : target === 'reports' ? 'all generated report files' : 'all temporary disk files';
    if (!window.confirm(`Are you sure you want to purge ${label} from disk?\n\nNote: All extracted curriculum structure, courses, and analysis stored in the SQLite database will remain completely intact.`)) {
      return;
    }
    setIsPurging(true);
    try {
      const res = await api.purgeAdminFiles(target);
      setNotification({ type: 'success', message: res.message });
      loadFiles();
    } catch (err: any) {
      setNotification({ type: 'error', message: err.message || 'Failed to purge files' });
    } finally {
      setIsPurging(false);
    }
  };

  const totalBytes = files.reduce((acc, f) => acc + (f.size_bytes || 0), 0);
  const totalUploads = files.filter((f) => f.category === 'UPLOAD');
  const totalReports = files.filter((f) => f.category === 'GENERATED_REPORT');

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            <Shield className="w-5 h-5 text-amber-400" />
            <span>Administrator Control & System Maintenance</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Manage user accounts, RBAC permissions, and clean or erase uploaded and generated disk files once stored in the database.
          </p>
        </div>

        {activeTab === 'users' ? (
          <button
            onClick={() => setShowAddModal(true)}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-semibold transition-colors flex items-center gap-2 shadow-lg shadow-blue-600/20 shrink-0"
          >
            <UserPlus className="w-4 h-4" />
            <span>Add New User</span>
          </button>
        ) : (
          <div className="flex items-center gap-2 shrink-0">
            <button
              onClick={() => handlePurge('uploads')}
              disabled={isPurging || totalUploads.length === 0}
              className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 disabled:opacity-40"
            >
              <Trash2 className="w-3.5 h-3.5 text-amber-400" />
              <span>Purge Uploads (Keep DB)</span>
            </button>
            <button
              onClick={() => handlePurge('reports')}
              disabled={isPurging || totalReports.length === 0}
              className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 disabled:opacity-40"
            >
              <Trash2 className="w-3.5 h-3.5 text-rose-400" />
              <span>Purge Reports</span>
            </button>
            <button
              onClick={loadFiles}
              disabled={isLoadingFiles}
              className="p-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 rounded-lg text-xs transition-colors"
              title="Refresh Storage List"
            >
              <RefreshCw className={`w-4 h-4 ${isLoadingFiles ? 'animate-spin' : ''}`} />
            </button>
          </div>
        )}
      </div>

      {/* Tab Navigation */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-1">
        <button
          onClick={() => setActiveTab('users')}
          className={`px-4 py-2 text-xs font-semibold rounded-lg transition-all flex items-center gap-2 ${
            activeTab === 'users'
              ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30'
              : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
          }`}
        >
          <Users className="w-4 h-4" />
          <span>User Accounts & RBAC ({users.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('storage')}
          className={`px-4 py-2 text-xs font-semibold rounded-lg transition-all flex items-center gap-2 ${
            activeTab === 'storage'
              ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
              : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
          }`}
        >
          <HardDrive className="w-4 h-4" />
          <span>Storage & File Management ({files.length})</span>
        </button>
      </div>

      {notification && (
        <div
          className={`p-3 rounded-lg text-xs flex items-center justify-between gap-2 ${
            notification.type === 'success'
              ? 'bg-emerald-500/10 border border-emerald-500/30 text-emerald-400'
              : 'bg-rose-500/10 border border-rose-500/30 text-rose-400'
          }`}
        >
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 shrink-0" />
            <span>{notification.message}</span>
          </div>
          <button
            onClick={() => setNotification(null)}
            className="text-[10px] opacity-70 hover:opacity-100 underline"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Tab 1: User Accounts */}
      {activeTab === 'users' && (
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-800/60 text-slate-400 uppercase text-[10px]">
              <tr>
                <th className="py-3 px-4">User</th>
                <th className="py-3 px-4">Role</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4">Password Hash</th>
                <th className="py-3 px-4">Last Login</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-300">
              {users.map((u) => (
                <tr key={u.id} className="hover:bg-slate-800/30 transition-colors">
                  <td className="py-3 px-4">
                    <div className="font-semibold text-white">{u.full_name}</div>
                    <div className="text-slate-400 text-[11px] font-mono">{u.email}</div>
                  </td>
                  <td className="py-3 px-4">
                    <span
                      className={`text-[10px] font-bold px-2.5 py-0.5 rounded-full ${
                        u.role === 'ADMIN'
                          ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                          : u.role === 'MANAGEMENT'
                          ? 'bg-purple-500/20 text-purple-400 border border-purple-500/30'
                          : u.role === 'REVIEWER'
                          ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                          : 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                      }`}
                    >
                      {u.role}
                    </span>
                  </td>
                  <td className="py-3 px-4">
                    <span className="text-[10px] text-emerald-400 font-semibold flex items-center gap-1">
                      <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                      <span>Active</span>
                    </span>
                  </td>
                  <td className="py-3 px-4 font-mono text-[10px] text-slate-400">
                    argon2id (m=65536, t=3, p=4)
                  </td>
                  <td className="py-3 px-4 text-slate-400 text-[11px]">
                    {u.last_login ? new Date(u.last_login).toLocaleString() : 'Recent Session'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Tab 2: Storage & File Management */}
      {activeTab === 'storage' && (
        <div className="space-y-5">
          {/* Metrics Overview */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div className="p-4 bg-slate-900/80 border border-slate-800 rounded-xl">
              <div className="text-[10px] text-slate-400 uppercase font-medium">Total Files on Disk</div>
              <div className="text-xl font-bold text-white mt-1">{files.length}</div>
              <div className="text-[10px] text-slate-500 mt-0.5">Uploads + Reports</div>
            </div>

            <div className="p-4 bg-slate-900/80 border border-slate-800 rounded-xl">
              <div className="text-[10px] text-slate-400 uppercase font-medium">Disk Storage Used</div>
              <div className="text-xl font-bold text-amber-400 mt-1">
                {(totalBytes / (1024 * 1024)).toFixed(2)} MB
              </div>
              <div className="text-[10px] text-slate-500 mt-0.5">Safe to erase once in DB</div>
            </div>

            <div className="p-4 bg-slate-900/80 border border-slate-800 rounded-xl">
              <div className="text-[10px] text-slate-400 uppercase font-medium">Uploaded Syllabi</div>
              <div className="text-xl font-bold text-blue-400 mt-1">{totalUploads.length}</div>
              <div className="text-[10px] text-emerald-400 mt-0.5">Data extracted to SQLite</div>
            </div>

            <div className="p-4 bg-slate-900/80 border border-slate-800 rounded-xl">
              <div className="text-[10px] text-slate-400 uppercase font-medium">Generated Reports</div>
              <div className="text-xl font-bold text-rose-400 mt-1">{totalReports.length}</div>
              <div className="text-[10px] text-slate-500 mt-0.5">PDF / Excel / PPT dossiers</div>
            </div>
          </div>

          {/* Disk Cleanup Explanatory Note */}
          <div className="bg-blue-950/30 border border-blue-500/20 rounded-xl p-4 text-xs text-slate-300 flex items-start gap-3">
            <Database className="w-5 h-5 text-blue-400 shrink-0 mt-0.5" />
            <div>
              <span className="font-semibold text-white">Database Persistence Notice: </span>
              When syllabi documents are uploaded, the system parses all courses, units, topics, and outcomes directly into the SQLite database.
              Admins can safely erase raw upload files or stale generated reports from disk without losing curriculum structure or analysis results.
            </div>
          </div>

          {/* Files List Table */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
            <div className="p-4 border-b border-slate-800 flex items-center justify-between">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <HardDrive className="w-4 h-4 text-amber-400" />
                <span>Files on Disk ({files.length})</span>
              </h3>
              <span className="text-[11px] text-slate-400">
                Sorted by newest modification date
              </span>
            </div>

            {files.length === 0 ? (
              <div className="p-8 text-center text-xs text-slate-400">
                No uploaded files or generated reports currently present on disk. All data is managed within the database.
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-xs text-left">
                  <thead className="bg-slate-800/60 text-slate-400 uppercase text-[10px]">
                    <tr>
                      <th className="py-3 px-4">File Name</th>
                      <th className="py-3 px-4">Category</th>
                      <th className="py-3 px-4">Size</th>
                      <th className="py-3 px-4">Database Status</th>
                      <th className="py-3 px-4">Created Date</th>
                      <th className="py-3 px-4 text-right">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800 text-slate-300">
                    {files.map((file) => {
                      const isUpload = file.category === 'UPLOAD';
                      return (
                        <tr key={file.id} className="hover:bg-slate-800/30 transition-colors">
                          <td className="py-3 px-4">
                            <div className="flex items-center gap-2">
                              <FileText className={`w-4 h-4 shrink-0 ${isUpload ? 'text-blue-400' : 'text-rose-400'}`} />
                              <div>
                                <div className="font-medium text-white truncate max-w-xs" title={file.file_name}>
                                  {file.file_name}
                                </div>
                                {file.associated_title && (
                                  <div className="text-[10px] text-slate-400 truncate max-w-xs">
                                    {file.associated_title}
                                  </div>
                                )}
                              </div>
                            </div>
                          </td>
                          <td className="py-3 px-4">
                            <span
                              className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${
                                isUpload
                                  ? 'bg-blue-500/20 text-blue-300 border border-blue-500/30'
                                  : 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                              }`}
                            >
                              {file.category_label}
                            </span>
                          </td>
                          <td className="py-3 px-4 font-mono text-[11px] text-slate-300">
                            {file.size_formatted}
                          </td>
                          <td className="py-3 px-4">
                            {file.stored_in_db ? (
                              <span className="text-[10px] text-emerald-400 font-semibold flex items-center gap-1">
                                <CheckCircle2 className="w-3.5 h-3.5" />
                                <span>Saved in DB</span>
                              </span>
                            ) : (
                              <span className="text-[10px] text-slate-500">
                                Unlinked
                              </span>
                            )}
                          </td>
                          <td className="py-3 px-4 text-[11px] text-slate-400">
                            {new Date(file.created_at).toLocaleString()}
                          </td>
                          <td className="py-3 px-4 text-right">
                            <button
                              onClick={() => handleDeleteFile(file.file_path, file.file_name)}
                              className="px-2.5 py-1 bg-rose-600/20 hover:bg-rose-600 text-rose-300 hover:text-white border border-rose-500/30 rounded text-[11px] font-semibold transition-all inline-flex items-center gap-1 cursor-pointer"
                              title="Erase file from disk (preserves DB data)"
                            >
                              <Trash2 className="w-3 h-3" />
                              <span>Erase</span>
                            </button>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Add User Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-md w-full p-6 shadow-2xl">
            <h3 className="text-base font-bold text-white mb-4">Add University System User</h3>
            <form onSubmit={handleCreateUser} className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-400 mb-1">Full Name</label>
                <input
                  type="text"
                  value={newFullName}
                  onChange={(e) => setNewFullName(e.target.value)}
                  placeholder="e.g. Dr. Jane Smith"
                  required
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-400 mb-1">University Email</label>
                <input
                  type="email"
                  value={newEmail}
                  onChange={(e) => setNewEmail(e.target.value)}
                  placeholder="e.g. jsmith@university.edu"
                  required
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-400 mb-1">Password</label>
                <input
                  type="password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  placeholder="••••••••••••"
                  required
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-400 mb-1">System Role</label>
                <select
                  value={newRole}
                  onChange={(e) => setNewRole(e.target.value as Role)}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white"
                >
                  <option value="FACULTY">Faculty Member</option>
                  <option value="REVIEWER">Curriculum Reviewer</option>
                  <option value="MANAGEMENT">Academic Management / Dean</option>
                  <option value="ADMIN">System Administrator</option>
                </select>
              </div>

              <div className="flex justify-end gap-3 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded-lg text-xs"
                >
                  Create User
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
