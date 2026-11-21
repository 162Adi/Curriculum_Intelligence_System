import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  FileSpreadsheet,
  Cpu,
  TrendingUp,
  Award,
  AlertTriangle,
  Sparkles,
  CheckCircle2,
  FileDown,
  Layers,
  Database,
  Activity,
  Users,
  BrainCircuit,
  Wrench,
  BookOpen,
  Server,
  Terminal,
  GitBranch,
  Search,
  Cloud,
  Code2,
  ShieldCheck,
  Compass,
} from 'lucide-react';
import { useAuthStore } from '../../stores/authStore';

const mainNavItems = [
  { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
  { name: 'Curriculum Workspace', path: '/curriculum', icon: FileSpreadsheet },
  { name: 'Agent Control Room', path: '/agents', icon: Cpu },
  { name: 'Industry Intelligence', path: '/industry', icon: TrendingUp },
  { name: 'Academic Benchmarking', path: '/benchmarking', icon: Award },
  { name: 'Gap Analysis', path: '/gaps', icon: AlertTriangle },
  { name: 'Recommendations', path: '/recommendations', icon: Sparkles },
  { name: 'Faculty Review', path: '/approvals', icon: CheckCircle2 },
  { name: 'Reports & Exports', path: '/reports', icon: FileDown },
];

const studioItems = [
  { name: 'Studio Hub', path: '/studio', icon: Layers },
  { name: '1. Agent vs Chatbot', path: '/studio/agent-vs-chatbot', icon: BrainCircuit },
  { name: '2. Tool-Using Agent', path: '/studio/tool-using-agent', icon: Wrench },
  { name: '3. Skill Creation', path: '/studio/skill-creation', icon: BookOpen },
  { name: '4. Memory & Retrieval', path: '/studio/memory-retrieval', icon: Database },
  { name: '5. MCP Connector', path: '/studio/mcp-connector', icon: Server },
  { name: '6. OpenClaw Runtime', path: '/studio/openclaw-runtime', icon: Terminal },
  { name: '7. Agentic Node Graph', path: '/studio/node-graph', icon: GitBranch },
  { name: '8. Parallel Swarm', path: '/studio/parallel-swarm', icon: Cpu },
  { name: '9. Deep Research', path: '/studio/deep-research', icon: Search },
  { name: '10. Cloud Operations', path: '/studio/cloud-ops', icon: Cloud },
  { name: '11. SDLC Factory', path: '/studio/sdlc-factory', icon: Code2 },
  { name: '12. Safety & Governance', path: '/studio/safety-governance', icon: ShieldCheck },
  { name: '13. Discipline-Specific', path: '/studio/discipline-agents', icon: Compass },
];

const systemItems = [
  { name: 'Memory Explorer', path: '/memory', icon: Database },
  { name: 'Integration Health', path: '/integrations', icon: Activity },
  { name: 'User Management', path: '/users', icon: Users, role: ['ADMIN'] },
];

export const Sidebar: React.FC = () => {
  const { user } = useAuthStore();

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col h-screen fixed left-0 top-0 z-30">
      {/* Brand Header */}
      <div className="h-16 flex items-center px-5 border-b border-slate-800 gap-3">
        <div className="w-9 h-9 rounded-lg bg-blue-600/20 border border-blue-500/40 flex items-center justify-center text-blue-400 font-bold">
          CIS
        </div>
        <div>
          <h1 className="text-sm font-bold tracking-tight text-white flex items-center gap-1.5">
            CIS Intelligence
            <span className="text-[10px] px-1.5 py-0.2 bg-blue-500/20 text-blue-400 rounded-full border border-blue-500/30">
              v2.0
            </span>
          </h1>
          <p className="text-[10px] text-slate-400 truncate max-w-[140px]">
            Academic & Industry Bridge
          </p>
        </div>
      </div>

      {/* Navigation Groups */}
      <div className="flex-1 overflow-y-auto px-3 py-4 space-y-6 custom-scrollbar">
        {/* Section A: Main CIS */}
        <div>
          <div className="px-3 mb-2 flex items-center justify-between text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            <span>Curriculum Intelligence</span>
            <span className="text-[9px] px-1 bg-slate-800 rounded text-slate-500">Core</span>
          </div>
          <nav className="space-y-0.5">
            {mainNavItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-medium transition-colors ${
                    isActive
                      ? 'bg-blue-600/15 text-blue-400 border border-blue-500/30'
                      : 'text-slate-300 hover:bg-slate-800/60 hover:text-white'
                  }`
                }
              >
                <item.icon className="w-4 h-4 shrink-0 text-slate-400" />
                <span className="truncate">{item.name}</span>
              </NavLink>
            ))}
          </nav>
        </div>

        {/* Section B: Agentic AI Studio */}
        <div>
          <div className="px-3 mb-2 flex items-center justify-between text-[11px] font-semibold text-blue-400 uppercase tracking-wider">
            <span>Agentic AI Studio</span>
            <span className="text-[9px] px-1 bg-blue-900/40 text-blue-300 rounded border border-blue-700/50">13 Labs</span>
          </div>
          <nav className="space-y-0.5">
            {studioItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center gap-2.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                    isActive
                      ? 'bg-blue-600/20 text-blue-300 border border-blue-500/40'
                      : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200'
                  }`
                }
              >
                <item.icon className="w-3.5 h-3.5 shrink-0 text-blue-400/80" />
                <span className="truncate">{item.name}</span>
              </NavLink>
            ))}
          </nav>
        </div>

        {/* Section C: System & Monitoring */}
        <div>
          <div className="px-3 mb-2 text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            System & Diagnostics
          </div>
          <nav className="space-y-0.5">
            {systemItems
              .filter((item) => !item.role || (user && item.role.includes(user.role)))
              .map((item) => (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={({ isActive }) =>
                    `flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-medium transition-colors ${
                      isActive
                        ? 'bg-blue-600/15 text-blue-400 border border-blue-500/30'
                        : 'text-slate-300 hover:bg-slate-800/60 hover:text-white'
                    }`
                  }
                >
                  <item.icon className="w-4 h-4 shrink-0 text-slate-400" />
                  <span className="truncate">{item.name}</span>
                </NavLink>
              ))}
          </nav>
        </div>
      </div>

      {/* User profile footer */}
      <div className="p-3 border-t border-slate-800 bg-slate-950/60">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-blue-600/30 border border-blue-500/50 flex items-center justify-center text-xs font-bold text-blue-300">
            {user?.full_name ? user.full_name[0].toUpperCase() : 'U'}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-xs font-semibold text-slate-200 truncate">{user?.full_name || 'Guest User'}</p>
            <p className="text-[10px] text-slate-400 uppercase tracking-wider">{user?.role || 'FACULTY'}</p>
          </div>
        </div>
      </div>
    </aside>
  );
};
