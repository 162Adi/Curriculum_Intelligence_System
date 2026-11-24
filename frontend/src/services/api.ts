import {
  User,
  Department,
  Programme,
  Curriculum,
  Course,
  AgentExecution,
  Gap,
  Recommendation,
  ApprovalRecord,
  StudioCapability,
  AdminFileItem
} from '../types';

const API_BASE = '/api';

class ApiClient {
  private getHeaders(isFormData = false): HeadersInit {
    const token = localStorage.getItem('cis_access_token');
    const headers: Record<string, string> = {};
    if (!isFormData) {
      headers['Content-Type'] = 'application/json';
    }
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
  }

  private async handleResponse<T>(response: Response): Promise<T> {
    if (response.status === 401) {
      // Clear token on 401
      localStorage.removeItem('cis_access_token');
      localStorage.removeItem('cis_user');
      if (!window.location.pathname.includes('/login')) {
        window.location.href = '/login';
      }
      throw new Error('Session expired or unauthorized');
    }

    if (!response.ok) {
      let errorMsg = `HTTP Error ${response.status}`;
      try {
        const errorData = await response.json();
        if (typeof errorData.detail === 'string') {
          errorMsg = errorData.detail;
        } else if (Array.isArray(errorData.detail)) {
          errorMsg = errorData.detail.map((d: any) => d.msg || (typeof d === 'string' ? d : JSON.stringify(d))).join('; ');
        } else if (typeof errorData.message === 'string') {
          errorMsg = errorData.message;
        }
      } catch {
        // use default error message
      }
      throw new Error(errorMsg);
    }

    return response.json();
  }

  // --- Auth Endpoints ---
  async login(credentials: { email?: string; username?: string; password?: string } | FormData): Promise<{ access_token: string; refresh_token: string; token_type: string; user: User }> {
    let body: any;
    let headers: HeadersInit = { 'Content-Type': 'application/json' };

    if (credentials instanceof FormData) {
      const email = credentials.get('username') || credentials.get('email');
      const password = credentials.get('password');
      body = JSON.stringify({ email, password });
    } else {
      body = JSON.stringify({
        email: credentials.email || credentials.username,
        password: credentials.password,
      });
    }

    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers,
      body,
    });
    return this.handleResponse(res);
  }

  async getMe(): Promise<User> {
    const res = await fetch(`${API_BASE}/auth/me`, {
      headers: this.getHeaders(),
    });
    return this.handleResponse<User>(res);
  }

  // --- Users Endpoints ---
  async getUsers(): Promise<User[]> {
    const res = await fetch(`${API_BASE}/users/`, {
      headers: this.getHeaders(),
    });
    return this.handleResponse<User[]>(res);
  }

  async createUser(userData: Partial<User> & { password: string }): Promise<User> {
    const res = await fetch(`${API_BASE}/users/`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(userData),
    });
    return this.handleResponse<User>(res);
  }

  // --- Curriculum Endpoints ---
  async getDepartments(): Promise<Department[]> {
    const res = await fetch(`${API_BASE}/curriculum/departments`, {
      headers: this.getHeaders(),
    });
    return this.handleResponse<Department[]>(res);
  }

  async getProgrammes(departmentId?: string): Promise<Programme[]> {
    const url = departmentId
      ? `${API_BASE}/curriculum/programmes?department_id=${departmentId}`
      : `${API_BASE}/curriculum/programmes`;
    const res = await fetch(url, {
      headers: this.getHeaders(),
    });
    return this.handleResponse<Programme[]>(res);
  }

  async getCurricula(programmeId?: string): Promise<Curriculum[]> {
    const url = programmeId
      ? `${API_BASE}/curriculum/by-programme/${programmeId}`
      : `${API_BASE}/curriculum/`;
    const res = await fetch(url, {
      headers: this.getHeaders(),
    });
    return this.handleResponse<Curriculum[]>(res);
  }

  async getCurriculum(id: string): Promise<Curriculum> {
    const res = await fetch(`${API_BASE}/curriculum/${id}`, {
      headers: this.getHeaders(),
    });
    return this.handleResponse<Curriculum>(res);
  }

  async uploadCurriculum(programmeId: string, academicYear: string, version: string, file: File): Promise<Curriculum> {
    const formData = new FormData();
    if (programmeId) {
      formData.append('programme_id', programmeId);
    }
    formData.append('academic_year', academicYear);
    formData.append('version_tag', version);
    formData.append('version', version);
    formData.append('file', file);

    const res = await fetch(`${API_BASE}/curriculum/upload`, {
      method: 'POST',
      headers: this.getHeaders(true),
      body: formData,
    });
    return this.handleResponse<Curriculum>(res);
  }

  async updateCourse(courseId: string, courseData: Partial<Course>): Promise<Course> {
    const res = await fetch(`${API_BASE}/curriculum/courses/${courseId}`, {
      method: 'PATCH',
      headers: this.getHeaders(),
      body: JSON.stringify(courseData),
    });
    return this.handleResponse<Course>(res);
  }

  async confirmCurriculumStructure(curriculumId: string): Promise<{ status: string; message: string }> {
    const res = await fetch(`${API_BASE}/curriculum/${curriculumId}/confirm-structure`, {
      method: 'POST',
      headers: this.getHeaders(),
    });
    return this.handleResponse(res);
  }

  // --- Analysis & Execution Endpoints ---
  async startAnalysis(curriculumId: string, parallelSwarm: boolean = true): Promise<AgentExecution> {
    const res = await fetch(`${API_BASE}/analysis/start`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ curriculum_id: curriculumId, enable_parallel_swarm: parallelSwarm }),
    });
    return this.handleResponse<AgentExecution>(res);
  }

  async getExecutionStatus(executionId: string): Promise<AgentExecution> {
    const res = await fetch(`${API_BASE}/analysis/${executionId}/status`, {
      headers: this.getHeaders(),
    });
    return this.handleResponse<AgentExecution>(res);
  }

  async getAnalysisHistory(curriculumId: string): Promise<AgentExecution[]> {
    const res = await fetch(`${API_BASE}/analysis/${curriculumId}/history`, {
      headers: this.getHeaders(),
    });
    return this.handleResponse<AgentExecution[]>(res);
  }

  // --- Gaps Endpoints ---
  async getGaps(curriculumId?: string): Promise<Gap[]> {
    const url = curriculumId ? `${API_BASE}/gaps/${curriculumId}` : `${API_BASE}/gaps`;
    const res = await fetch(url, {
      headers: this.getHeaders(),
    });
    return this.handleResponse<Gap[]>(res);
  }

  // --- Recommendations Endpoints ---
  async getRecommendations(curriculumId?: string): Promise<Recommendation[]> {
    const url = curriculumId ? `${API_BASE}/recommendations/${curriculumId}` : `${API_BASE}/recommendations`;
    const res = await fetch(url, {
      headers: this.getHeaders(),
    });
    return this.handleResponse<Recommendation[]>(res);
  }

  async updateRecommendation(id: string, updates: Partial<Recommendation>): Promise<Recommendation> {
    const res = await fetch(`${API_BASE}/recommendations/${id}`, {
      method: 'PATCH',
      headers: this.getHeaders(),
      body: JSON.stringify(updates),
    });
    return this.handleResponse<Recommendation>(res);
  }

  // --- Approvals Endpoints ---
  async submitApprovalDecision(
    recommendationId: string,
    decision: 'APPROVED' | 'REJECTED' | 'REVISE',
    comments?: string
  ): Promise<ApprovalRecord> {
    const res = await fetch(`${API_BASE}/approvals/recommendations/${recommendationId}`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ decision, comments }),
    });
    return this.handleResponse<ApprovalRecord>(res);
  }

  async getApprovals(curriculumId: string): Promise<ApprovalRecord[]> {
    const res = await fetch(`${API_BASE}/approvals/${curriculumId}`, {
      headers: this.getHeaders(),
    });
    return this.handleResponse<ApprovalRecord[]>(res);
  }

  async signoffFinalCurriculum(curriculumId: string, comments?: string): Promise<{ status: string; message: string }> {
    const res = await fetch(`${API_BASE}/approvals/${curriculumId}/signoff`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ comments }),
    });
    return this.handleResponse(res);
  }

  // --- Reports Endpoints ---
  async getReportSummary(curriculumId: string): Promise<any> {
    const res = await fetch(`${API_BASE}/reports/${curriculumId}/summary`, {
      headers: this.getHeaders(),
    });
    return this.handleResponse(res);
  }

  getReportDownloadUrl(curriculumId: string, format: 'pdf' | 'xlsx' | 'pptx'): string {
    const token = localStorage.getItem('cis_access_token');
    return `${API_BASE}/reports/${curriculumId}/download/${format}?token=${token || ''}`;
  }

  async downloadReportFile(curriculumId: string, format: 'pdf' | 'xlsx' | 'pptx'): Promise<string> {
    const token = localStorage.getItem('cis_access_token');
    const headers: Record<string, string> = {};
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE}/reports/${curriculumId}/download/${format}?token=${token || ''}`, {
      method: 'GET',
      headers,
    });

    if (!response.ok) {
      let errDetail = `Failed to download ${format.toUpperCase()} (HTTP ${response.status})`;
      try {
        const errJson = await response.json();
        if (errJson && errJson.detail) {
          errDetail = errJson.detail;
        }
      } catch {}
      throw new Error(errDetail);
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;

    let filename = `CIS_Report_${curriculumId.slice(0, 8)}.${format === 'xlsx' ? 'xlsx' : format}`;
    const disposition = response.headers.get('Content-Disposition');
    if (disposition && disposition.includes('filename=')) {
      const match = disposition.match(/filename=["']?([^"';]+)["']?/);
      if (match && match[1]) {
        filename = match[1];
      }
    }

    a.download = filename;
    document.body.appendChild(a);
    a.click();

    setTimeout(() => {
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    }, 500);

    return filename;
  }

  // --- Integrations & Health ---
  async getIntegrationHealth(): Promise<Record<string, any>> {
    const res = await fetch(`${API_BASE}/integrations/health`, {
      headers: this.getHeaders(),
    });
    return this.handleResponse(res);
  }

  // --- Memory ---
  async searchMemory(query: string, limit: number = 5): Promise<any[]> {
    const res = await fetch(`${API_BASE}/memory/search`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ query, limit }),
    });
    return this.handleResponse(res);
  }

  async getMemoryStats(): Promise<any> {
    const res = await fetch(`${API_BASE}/memory/stats`, {
      headers: this.getHeaders(),
    });
    return this.handleResponse(res);
  }

  // --- Agentic Studio Endpoints ---
  async getStudioCapabilities(): Promise<StudioCapability[]> {
    const res = await fetch(`${API_BASE}/studio/capabilities`, {
      headers: this.getHeaders(),
    });
    return this.handleResponse<StudioCapability[]>(res);
  }

  async runStudioCapability(capabilityId: string, params: Record<string, any> = {}): Promise<any> {
    const res = await fetch(`${API_BASE}/studio/run/${capabilityId}`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(params),
    });
    return this.handleResponse(res);
  }

  // --- Admin & Storage Management ---
  async getAdminFiles(): Promise<AdminFileItem[]> {
    const res = await fetch(`${API_BASE}/admin/files`, {
      headers: this.getHeaders(),
    });
    return this.handleResponse<AdminFileItem[]>(res);
  }

  async deleteAdminFile(filePath: string): Promise<{ message: string; file_name: string; file_path: string }> {
    const res = await fetch(`${API_BASE}/admin/files?file_path=${encodeURIComponent(filePath)}`, {
      method: 'DELETE',
      headers: this.getHeaders(),
    });
    return this.handleResponse(res);
  }

  async purgeAdminFiles(target: 'uploads' | 'reports' | 'all'): Promise<{
    message: string;
    target: string;
    files_removed: number;
    bytes_freed: number;
    freed_formatted: string;
  }> {
    const res = await fetch(`${API_BASE}/admin/files/purge?target=${target}`, {
      method: 'POST',
      headers: this.getHeaders(),
    });
    return this.handleResponse(res);
  }

  async deleteCurriculum(curriculumId: string): Promise<{ message: string; curriculum_id: string }> {
    const res = await fetch(`${API_BASE}/admin/curriculum/${curriculumId}`, {
      method: 'DELETE',
      headers: this.getHeaders(),
    });
    return this.handleResponse(res);
  }
}

export const api = new ApiClient();
