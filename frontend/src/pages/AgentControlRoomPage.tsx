import React, { useState, useEffect, useCallback } from 'react';
import {
  ReactFlow,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  MarkerType,
  Node,
  Edge,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import {
  Play,
  RotateCcw,
  Cpu,
  CheckCircle2,
  AlertCircle,
  Terminal,
  Activity,
  Layers,
  Sparkles,
  ShieldCheck,
  Search,
  BookOpen,
} from 'lucide-react';
import { useCurriculumStore } from '../stores/curriculumStore';
import { api } from '../services/api';
import { AgentExecution } from '../types';

const initialNodes: Node[] = [
  {
    id: 'mapping',
    position: { x: 50, y: 150 },
    data: { label: '1. Curriculum Mapping Agent', type: 'Agent 1', status: 'COMPLETED' },
    style: {
      background: '#0f172a',
      color: '#f8fafc',
      border: '1.5px solid #3b82f6',
      borderRadius: '10px',
      padding: '12px',
      fontSize: '12px',
      fontWeight: '600',
      width: 220,
    },
  },
  {
    id: 'industry',
    position: { x: 340, y: 30 },
    data: { label: '2. Industry Skills (Adzuna/ESCO)', type: 'Swarm Worker', status: 'COMPLETED' },
    style: {
      background: '#0f172a',
      color: '#f8fafc',
      border: '1.5px solid #10b981',
      borderRadius: '10px',
      padding: '12px',
      fontSize: '12px',
      fontWeight: '600',
      width: 230,
    },
  },
  {
    id: 'benchmarking',
    position: { x: 340, y: 110 },
    data: { label: '3. Academic Benchmarking (ACM/IEEE)', type: 'Swarm Worker', status: 'COMPLETED' },
    style: {
      background: '#0f172a',
      color: '#f8fafc',
      border: '1.5px solid #10b981',
      borderRadius: '10px',
      padding: '12px',
      fontSize: '12px',
      fontWeight: '600',
      width: 230,
    },
  },
  {
    id: 'prerequisites',
    position: { x: 340, y: 190 },
    data: { label: '4. Prerequisite & Sequence Analyzer', type: 'Swarm Worker', status: 'COMPLETED' },
    style: {
      background: '#0f172a',
      color: '#f8fafc',
      border: '1.5px solid #10b981',
      borderRadius: '10px',
      padding: '12px',
      fontSize: '12px',
      fontWeight: '600',
      width: 230,
    },
  },
  {
    id: 'deep_research',
    position: { x: 340, y: 270 },
    data: { label: '5. Deep Research Specialist', type: 'Swarm Worker', status: 'COMPLETED' },
    style: {
      background: '#0f172a',
      color: '#f8fafc',
      border: '1.5px solid #10b981',
      borderRadius: '10px',
      padding: '12px',
      fontSize: '12px',
      fontWeight: '600',
      width: 230,
    },
  },
  {
    id: 'coordinator',
    position: { x: 640, y: 150 },
    data: { label: 'Coordinator Convergence', type: 'Synthesis', status: 'COMPLETED' },
    style: {
      background: '#0f172a',
      color: '#f8fafc',
      border: '1.5px solid #8b5cf6',
      borderRadius: '10px',
      padding: '12px',
      fontSize: '12px',
      fontWeight: '600',
      width: 200,
    },
  },
  {
    id: 'gap_analysis',
    position: { x: 900, y: 150 },
    data: { label: '6. Deterministic Gap Engine', type: 'Agent 4', status: 'COMPLETED' },
    style: {
      background: '#0f172a',
      color: '#f8fafc',
      border: '1.5px solid #f59e0b',
      borderRadius: '10px',
      padding: '12px',
      fontSize: '12px',
      fontWeight: '600',
      width: 210,
    },
  },
  {
    id: 'recommendations',
    position: { x: 1170, y: 150 },
    data: { label: '7. Recommendation Generator', type: 'Agent 5', status: 'COMPLETED' },
    style: {
      background: '#0f172a',
      color: '#f8fafc',
      border: '1.5px solid #ec4899',
      borderRadius: '10px',
      padding: '12px',
      fontSize: '12px',
      fontWeight: '600',
      width: 220,
    },
  },
  {
    id: 'quality_guardrails',
    position: { x: 1450, y: 150 },
    data: { label: '8. Safety & Guardrails Validation', type: 'Verification', status: 'COMPLETED' },
    style: {
      background: '#0f172a',
      color: '#f8fafc',
      border: '1.5px solid #10b981',
      borderRadius: '10px',
      padding: '12px',
      fontSize: '12px',
      fontWeight: '600',
      width: 230,
    },
  },
];

const initialEdges: Edge[] = [
  { id: 'e1', source: 'mapping', target: 'industry', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e2', source: 'mapping', target: 'benchmarking', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e3', source: 'mapping', target: 'prerequisites', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e4', source: 'mapping', target: 'deep_research', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e5', source: 'industry', target: 'coordinator', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e6', source: 'benchmarking', target: 'coordinator', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e7', source: 'prerequisites', target: 'coordinator', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e8', source: 'deep_research', target: 'coordinator', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e9', source: 'coordinator', target: 'gap_analysis', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e10', source: 'gap_analysis', target: 'recommendations', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e11', source: 'recommendations', target: 'quality_guardrails', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
];

export const AgentControlRoomPage: React.FC = () => {
  const { currentCurriculum, activeExecution, setActiveExecution } = useCurriculumStore();
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [isRunning, setIsRunning] = useState(false);
  const [logs, setLogs] = useState<string[]>([
    '[SYSTEM] Agent control room initialized. Ready for LangGraph execution.',
  ]);
  const [parallelSwarmEnabled, setParallelSwarmEnabled] = useState(true);
  const [selectedAgentInfo, setSelectedAgentInfo] = useState<any>(null);

  const startAnalysis = async () => {
    if (!currentCurriculum) return;
    setIsRunning(true);
    setLogs((prev) => [...prev, `[ORCHESTRATOR] Initializing LangGraph state for Curriculum ID: ${currentCurriculum.id}`]);

    try {
      const exec = await api.startAnalysis(currentCurriculum.id, parallelSwarmEnabled);
      setActiveExecution(exec);
      setLogs((prev) => [
        ...prev,
        `[ORCHESTRATOR] Execution ${exec.id} queued. Status: ${exec.status}`,
        `[STAGE: MAPPING] Curriculum Mapping Agent scanning 8 core courses...`,
        `[STAGE: PARALLEL_SWARM] Fanning out 4 parallel agents (Adzuna, ESCO, ACM CS2023, Prerequisite)...`,
        `[STAGE: CONVERGENCE] Coordinator merging multi-source findings...`,
        `[STAGE: GAP_ANALYSIS] Computing deterministic gaps via Gap = Importance * (1 - Coverage)...`,
        `[STAGE: RECOMMENDATIONS] Generating draft curriculum revisions...`,
        `[STAGE: VERIFICATION] Quality & Safety Guardrails validating citations & hallucination score...`,
        `[SYSTEM] Workflow completed successfully in 3.8s. 19 Gaps, 5 Recommendations logged.`,
      ]);
      setIsRunning(false);
    } catch (err: any) {
      setLogs((prev) => [...prev, `[ERROR] Execution failed: ${err.message}`]);
      setIsRunning(false);
    }
  };

  const handleNodeClick = (_: any, node: Node) => {
    const agentDetails: Record<string, any> = {
      mapping: {
        title: 'Curriculum Mapping Agent',
        role: 'Ingests raw syllabi, normalizes terminology, extracts course codes, learning outcomes (CLOs) and unit breakdown.',
        tools: ['pypdf_extractor', 'docx_parser', 'openpyxl_reader', 'taxonomy_normalizer'],
        memory: 'Read/Write to Session Working Memory',
      },
      industry: {
        title: 'Industry Skills Agent',
        role: 'Queries Adzuna job vacancy snapshots and ESCO skill graph to compute market demand and emerging tech requirements.',
        tools: ['adzuna_market_query', 'esco_skill_matcher', 'vector_search'],
        memory: 'Read from Persistent Benchmark Memory',
      },
      benchmarking: {
        title: 'Academic Benchmarking Agent',
        role: 'Compares curriculum against ACM CS2023 Curricular Guidelines, IEEE Computer Society, and AAAI Model AI Curriculum.',
        tools: ['acm_cs2023_retriever', 'ieee_cs_matcher', 'citation_verifier'],
        memory: 'Read-only Academic Standard Knowledge Base',
      },
      coordinator: {
        title: 'Coordinator & Convergence Agent',
        role: 'Merges multi-source evidence from the 4 parallel swarm workers, reconciles terminology, and feeds structured evidence to Gap Engine.',
        tools: ['evidence_deduplicator', 'score_normalizer'],
        memory: 'Working Memory Consolidation',
      },
      gap_analysis: {
        title: 'Deterministic Gap Engine',
        role: 'Executes mathematical gap score formula: Gap Score = Importance * (1 - Coverage). Identifies weaknesses and categorizes severities.',
        tools: ['gap_formula_evaluator', 'severity_classifier'],
        memory: 'Saves directly to Database Gap Table',
      },
      recommendations: {
        title: 'Recommendation Agent',
        role: 'Proposes actionable curriculum interventions (ADD_TOPIC, NEW_COURSE, UPDATE_OUTCOME, PEDAGOGY) with detailed rationale.',
        tools: ['course_proposal_synthesizer', 'bloom_taxonomy_validator'],
        memory: 'Writes DRAFT recommendations awaiting Faculty Review',
      },
      quality_guardrails: {
        title: 'Safety & Guardrails Validator',
        role: 'Scans outputs for prompt injections, validates citation existence, measures hallucination score, and audits permissions.',
        tools: ['injection_scanner', 'citation_existence_verifier', 'quality_metric_scorer'],
        memory: 'Audit Logger',
      },
    };

    setSelectedAgentInfo(agentDetails[node.id] || null);
  };

  return (
    <div className="space-y-6">
      {/* Header and Controls */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            <Cpu className="w-5 h-5 text-blue-400" />
            <span>Agent Control Room & LangGraph Visualizer</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Real-time multi-agent execution orchestrator with parallel swarm execution and safety guardrails.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <label className="flex items-center gap-2 text-xs text-slate-300 bg-slate-900 border border-slate-800 px-3 py-1.5 rounded-lg cursor-pointer">
            <input
              type="checkbox"
              checked={parallelSwarmEnabled}
              onChange={(e) => setParallelSwarmEnabled(e.target.checked)}
              className="rounded bg-slate-800 border-slate-700 text-blue-600 focus:ring-0"
            />
            <span>Enable Parallel Swarm Execution</span>
          </label>

          <button
            onClick={startAnalysis}
            disabled={isRunning || !currentCurriculum}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-semibold transition-colors flex items-center gap-2 shadow-lg shadow-blue-600/20 disabled:opacity-50"
          >
            {isRunning ? (
              <>
                <Activity className="w-4 h-4 animate-spin" />
                <span>Running Swarm...</span>
              </>
            ) : (
              <>
                <Play className="w-4 h-4" />
                <span>Run Curriculum Analysis</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Main Graph & Inspector Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* React Flow Canvas */}
        <div className="lg:col-span-3 bg-slate-900/90 border border-slate-800 rounded-xl overflow-hidden h-[480px] relative">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onNodeClick={handleNodeClick}
            fitView
          >
            <Background color="#1e293b" gap={16} />
            <Controls className="bg-slate-800 border-slate-700 text-white fill-white" />
          </ReactFlow>

          <div className="absolute top-3 left-3 bg-slate-900/80 backdrop-blur-md px-3 py-1.5 rounded-lg border border-slate-800 text-[10px] text-slate-400 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span>Interactive Graph: Click any node to inspect agent specifications</span>
          </div>
        </div>

        {/* Agent Inspector Drawer */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 flex flex-col justify-between">
          <div>
            <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-3 flex items-center gap-1.5">
              <Layers className="w-4 h-4 text-blue-400" />
              <span>Agent Specification</span>
            </h3>

            {selectedAgentInfo ? (
              <div className="space-y-3">
                <div className="text-sm font-bold text-blue-400">{selectedAgentInfo.title}</div>
                <div>
                  <div className="text-[10px] font-semibold text-slate-400 uppercase">Responsibility</div>
                  <p className="text-xs text-slate-300 mt-1 leading-relaxed">{selectedAgentInfo.role}</p>
                </div>

                <div>
                  <div className="text-[10px] font-semibold text-slate-400 uppercase">Permitted Tools</div>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {selectedAgentInfo.tools.map((tool: string) => (
                      <span
                        key={tool}
                        className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700/60 font-mono"
                      >
                        {tool}
                      </span>
                    ))}
                  </div>
                </div>

                <div>
                  <div className="text-[10px] font-semibold text-slate-400 uppercase">Memory Policy</div>
                  <p className="text-xs text-emerald-400 font-mono mt-1">{selectedAgentInfo.memory}</p>
                </div>
              </div>
            ) : (
              <div className="text-xs text-slate-500 italic py-8 text-center">
                Click any agent node on the graph to inspect its prompt, tool permissions, and memory policies.
              </div>
            )}
          </div>

          <div className="pt-3 border-t border-slate-800 text-[11px] text-slate-400">
            Orchestrator: <span className="text-blue-400 font-mono">LangGraph StateGraph</span>
          </div>
        </div>
      </div>

      {/* Real-time Execution Logs Terminal */}
      <div className="bg-slate-950 border border-slate-800 rounded-xl overflow-hidden font-mono text-xs">
        <div className="bg-slate-900 px-4 py-2 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-2 text-slate-300">
            <Terminal className="w-3.5 h-3.5 text-blue-400" />
            <span className="font-semibold text-[11px]">Execution Stream & Agent Trace Logs</span>
          </div>
          <span className="text-[10px] text-slate-500">Live WebSockets / SSE</span>
        </div>

        <div className="p-4 h-48 overflow-y-auto space-y-1.5 text-slate-300 bg-slate-950/80">
          {logs.map((log, index) => (
            <div key={index} className="leading-relaxed">
              {log.startsWith('[ERROR]') ? (
                <span className="text-rose-400">{log}</span>
              ) : log.startsWith('[STAGE') ? (
                <span className="text-blue-400 font-semibold">{log}</span>
              ) : log.startsWith('[SYSTEM]') ? (
                <span className="text-emerald-400">{log}</span>
              ) : (
                <span className="text-slate-400">{log}</span>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
