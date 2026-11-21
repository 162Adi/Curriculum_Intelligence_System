import { create } from 'zustand';
import { Curriculum, Department, Programme, AgentExecution } from '../types';
import { api } from '../services/api';

interface CurriculumState {
  departments: Department[];
  programmes: Programme[];
  selectedDepartmentId: string | null;
  selectedProgrammeId: string | null;
  currentCurriculum: Curriculum | null;
  activeExecution: AgentExecution | null;
  isLoading: boolean;
  error: string | null;

  fetchInitialData: () => Promise<void>;
  selectDepartment: (id: string) => void;
  selectProgramme: (id: string) => Promise<void>;
  setCurrentCurriculum: (curriculum: Curriculum | null) => void;
  setActiveExecution: (execution: AgentExecution | null) => void;
}

const INITIAL_DEPARTMENTS: Department[] = [
  {
    id: '453afd7a-14f0-49c0-92b1-6c07592400c3',
    name: 'Department of Computer Science & Engineering',
    code: 'CSE',
    description: 'Faculty of Computing and Information Systems'
  },
  {
    id: 'fb592c82-6fbd-41d2-8650-ca5744687721',
    name: 'Department of Electronics & Communication Engineering',
    code: 'ECE',
    description: 'Faculty of Electronics and Communication'
  }
];

const INITIAL_PROGRAMMES: Programme[] = [
  {
    id: '7519fd6b-de0b-486f-98d1-0d39a8a1dcc9',
    department_id: '453afd7a-14f0-49c0-92b1-6c07592400c3',
    name: 'Bachelor of Technology in Computer Science & Engineering',
    code: 'BTECH-CSE',
    degree_type: 'B.Tech',
    duration_years: 4,
    total_credits: 160
  }
];

export const useCurriculumStore = create<CurriculumState>((set, get) => ({
  departments: INITIAL_DEPARTMENTS,
  programmes: INITIAL_PROGRAMMES,
  selectedDepartmentId: INITIAL_DEPARTMENTS[0].id,
  selectedProgrammeId: INITIAL_PROGRAMMES[0].id,
  currentCurriculum: null,
  activeExecution: null,
  isLoading: false,
  error: null,

  fetchInitialData: async () => {
    set({ isLoading: true, error: null });
    try {
      const departments = await api.getDepartments();
      const programmes = await api.getProgrammes();
      
      const depts = (departments && departments.length > 0) ? departments : INITIAL_DEPARTMENTS;
      const progs = (programmes && programmes.length > 0) ? programmes : INITIAL_PROGRAMMES;

      const currentDeptId = get().selectedDepartmentId;
      const currentProgId = get().selectedProgrammeId;

      const deptId = (currentDeptId && depts.some(d => d.id === currentDeptId))
        ? currentDeptId
        : depts[0].id;

      const deptProgs = progs.filter(p => p.department_id === deptId);
      const progId = (currentProgId && progs.some(p => p.id === currentProgId))
        ? currentProgId
        : (deptProgs.length > 0 ? deptProgs[0].id : progs[0].id);

      set({
        departments: depts,
        programmes: progs,
        selectedDepartmentId: deptId,
        selectedProgrammeId: progId,
        isLoading: false,
      });

      if (progId) {
        await get().selectProgramme(progId);
      }
    } catch (err: any) {
      console.warn('Network sync notice: using seeded initial curriculum data', err);
      set({ isLoading: false });
    }
  },

  selectDepartment: (id: string) => {
    const { programmes } = get();
    const filteredProgs = programmes.filter(p => p.department_id === id);
    const progId = filteredProgs.length > 0 ? filteredProgs[0].id : (programmes.length > 0 ? programmes[0].id : null);
    set({ selectedDepartmentId: id, selectedProgrammeId: progId });
    if (progId) {
      get().selectProgramme(progId);
    }
  },

  selectProgramme: async (id: string) => {
    set({ selectedProgrammeId: id, isLoading: true });
    try {
      const curricula = await api.getCurricula(id);
      const activeCurriculum = curricula.find(c => c.is_active) || curricula[0] || null;
      set({ currentCurriculum: activeCurriculum, isLoading: false });
    } catch (err: any) {
      set({ error: err.message, isLoading: false });
    }
  },

  setCurrentCurriculum: (curriculum: Curriculum | null) => {
    set({ currentCurriculum: curriculum });
  },

  setActiveExecution: (execution: AgentExecution | null) => {
    set({ activeExecution: execution });
  },
}));
