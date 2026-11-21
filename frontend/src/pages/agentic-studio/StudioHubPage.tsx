import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Layers,
  BrainCircuit,
  Wrench,
  BookOpen,
  Database,
  Server,
  Terminal,
  GitBranch,
  Cpu,
  Search,
  Cloud,
  Code2,
  ShieldCheck,
  Compass,
  ArrowRight,
  Sparkles,
} from 'lucide-react';
import { api } from '../../services/api';

const iconMap: Record<string, any> = {
  'agent-vs-chatbot': BrainCircuit,
  'tool-using-agent': Wrench,
  'skill-creation': BookOpen,
  'memory-retrieval': Database,
  'mcp-connector': Server,
  'openclaw-runtime': Terminal,
  'node-graph': GitBranch,
  'parallel-swarm': Cpu,
  'deep-research': Search,
  'cloud-ops': Cloud,
  'sdlc-factory': Code2,
  'safety-governance': ShieldCheck,
  'discipline-agents': Compass,
};

export const StudioHubPage: React.FC = () => {
  const navigate = useNavigate();
  const [capabilities, setCapabilities] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getStudioCapabilities()
      .then((res: any) => {
        setCapabilities(res.capabilities || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-blue-950 via-slate-900 to-indigo-950 border border-blue-500/30 rounded-2xl p-6">
        <div className="flex items-center gap-2 mb-2">
          <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-500/20 text-blue-400 border border-blue-500/30">
            Section B: University Agentic Curriculum
          </span>
          <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-purple-500/20 text-purple-400 border border-purple-500/30">
            13 Architectural Capabilities
          </span>
        </div>
        <h1 className="text-2xl font-bold text-white tracking-tight">Agentic AI Studio</h1>
        <p className="text-xs text-slate-300 mt-1 max-w-2xl leading-relaxed">
          Interactive laboratory demonstrating the 13 fundamental agentic design patterns powering the
          Curriculum Intelligence System — including real MCP server tools, OpenClaw runtime, LangGraph state
          machine, parallel swarm execution, and deterministic safety guardrails.
        </p>
      </div>

      {/* Capabilities Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {capabilities.map((cap) => {
          // Map capability ID to route slug
          const slugMap: Record<string, string> = {
            'agent-vs-chatbot': 'agent-vs-chatbot',
            'tool-using-agent': 'tool-using-agent',
            'skill-creation': 'skill-creation',
            'memory-retrieval': 'memory-retrieval',
            'mcp-connector': 'mcp-connector',
            'openclaw-runtime': 'openclaw-runtime',
            'agentic-node-graph': 'node-graph',
            'parallel-swarm': 'parallel-swarm',
            'deep-research-agent': 'deep-research',
            'cloud-operations-agent': 'cloud-ops',
            'agentic-sdlc-factory': 'sdlc-factory',
            'safety-governance': 'safety-governance',
            'discipline-specific-agents': 'discipline-agents',
          };
          const targetSlug = slugMap[cap.id] || cap.id;
          const Icon = iconMap[targetSlug] || Layers;

          return (
            <div
              key={cap.id}
              onClick={() => navigate(`/studio/${targetSlug}`)}
              className="bg-slate-900/80 border border-slate-800 hover:border-blue-500/40 rounded-xl p-5 flex flex-col justify-between transition-all cursor-pointer group hover:shadow-xl hover:shadow-blue-900/10"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <div className="w-10 h-10 rounded-lg bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400 group-hover:scale-105 transition-transform">
                    <Icon className="w-5 h-5" />
                  </div>
                  <span className="text-[10px] font-mono font-bold text-slate-500">
                    MODULE {cap.number < 10 ? `0${cap.number}` : cap.number}
                  </span>
                </div>

                <h3 className="text-base font-bold text-white group-hover:text-blue-400 transition-colors">
                  {cap.name}
                </h3>
                <p className="text-[11px] font-medium text-blue-300 mt-0.5">{cap.tagline}</p>
                <p className="text-xs text-slate-400 mt-2 line-clamp-3 leading-relaxed">
                  {cap.description}
                </p>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between text-xs">
                <span className="text-[11px] text-slate-500">Real CIS Integration</span>
                <span className="text-blue-400 group-hover:translate-x-1 transition-transform flex items-center gap-1 font-semibold text-[11px]">
                  <span>Launch Lab</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
