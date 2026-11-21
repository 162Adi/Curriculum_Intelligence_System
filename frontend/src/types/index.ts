export type Role = 'ADMIN' | 'FACULTY' | 'REVIEWER' | 'MANAGEMENT';

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: Role;
  department_id?: string | null;
  is_active: boolean;
  last_login?: string | null;
}

export interface Department {
  id: string;
  name: string;
  code: string;
  description?: string;
  programmes?: Programme[];
}

export interface Programme {
  id: string;
  department_id: string;
  name: string;
  code: string;
  degree_type: string;
  duration_years: number;
  total_credits: number;
}

export interface LearningOutcome {
  id: string;
  code: string;
  description: string;
  bloom_level?: string;
}

export interface Unit {
  id: string;
  unit_number: number;
  title: string;
  topics: string[];
  contact_hours: number;
}

export interface Course {
  id: string;
  curriculum_id: string;
  code: string;
  title: string;
  credits: number;
  semester: number;
  course_type: string;
  description?: string;
  syllabus_text?: string;
  units?: Unit[];
  learning_outcomes?: LearningOutcome[];
}

export interface Curriculum {
  id: string;
  programme_id: string;
  programme_name?: string;
  programme_code?: string;
  department_name?: string;
  academic_year: string;
  version: string;
  version_tag?: string;
  status: 'DRAFT' | 'INGESTED' | 'STRUCTURE_CONFIRMED' | 'ANALYSIS_RUNNING' | 'ANALYZED' | 'APPROVED' | 'ARCHIVED' | string;
  is_active: boolean;
  total_courses?: number;
  total_credits?: number;
  courses?: Course[];
  created_at: string;
  updated_at?: string;
}

export interface AgentExecution {
  id: string;
  curriculum_id: string;
  workflow_type: string;
  status: 'INITIALIZED' | 'RUNNING' | 'COMPLETED' | 'FAILED';
  started_at: string;
  completed_at?: string;
  current_stage?: string;
  execution_log?: any[];
  agent_outputs?: Record<string, any>;
  quality_score?: number;
  error_message?: string;
}

export interface Gap {
  id: string;
  curriculum_id: string;
  category: 'INDUSTRY_SKILL' | 'ACADEMIC_STANDARD' | 'PREREQUISITE' | 'PEDAGOGICAL' | 'MISSING_SKILL' | 'WEAK_COVERAGE' | string;
  title: string;
  description: string;
  importance_score: number;
  current_coverage: number;
  coverage_score?: number;
  gap_score: number;
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL' | string;
  evidence?: {
    source: string;
    details: string;
    citation?: string;
  };
  affected_courses?: string[];
}

export interface Recommendation {
  id: string;
  curriculum_id: string;
  gap_id?: string;
  recommendation_type?: 'ADD_TOPIC' | 'NEW_COURSE' | 'UPDATE_OUTCOME' | 'REMOVE_OUTREACH' | 'PEDAGOGY' | string;
  title: string;
  proposed_action?: string;
  description?: string;
  rationale?: string;
  target_course_id?: string;
  target_course_name?: string;
  target_semester?: number;
  estimated_hours?: number;
  approval_status: 'DRAFT' | 'PENDING' | 'APPROVED' | 'REJECTED' | string;
  status?: string;
  faculty_feedback?: string;
  priority: 'LOW' | 'MEDIUM' | 'HIGH' | string;
}

export interface ApprovalRecord {
  id: string;
  curriculum_id: string;
  recommendation_id?: string;
  user_id: string;
  user_name?: string;
  user_role?: Role;
  decision: 'APPROVED' | 'REJECTED' | 'REVISE';
  comments?: string;
  created_at: string;
}

export interface StudioCapability {
  id: string;
  title: string;
  category: string;
  summary: string;
  cis_integration: string;
  architecture_diagram?: string;
}
