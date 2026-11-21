import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'sonner';

import { LoginPage } from '../pages/LoginPage';
import { DashboardLayout } from '../layouts/DashboardLayout';
import { ProtectedRoute } from '../components/common/ProtectedRoute';

// Section A Pages
import { DashboardPage } from '../pages/DashboardPage';
import { CurriculumWorkspacePage } from '../pages/CurriculumWorkspacePage';
import { AgentControlRoomPage } from '../pages/AgentControlRoomPage';
import { IndustryIntelligencePage } from '../pages/IndustryIntelligencePage';
import { AcademicBenchmarkingPage } from '../pages/AcademicBenchmarkingPage';
import { GapAnalysisPage } from '../pages/GapAnalysisPage';
import { RecommendationsPage } from '../pages/RecommendationsPage';
import { FacultyReviewPage } from '../pages/FacultyReviewPage';
import { ReportsPage } from '../pages/ReportsPage';

// Section B Pages
import { StudioHubPage } from '../pages/agentic-studio/StudioHubPage';
import { CapabilityDetailPage } from '../pages/agentic-studio/CapabilityDetailPage';

// System Pages
import { MemoryExplorerPage } from '../pages/MemoryExplorerPage';
import { IntegrationsPage } from '../pages/IntegrationsPage';
import { UsersPage } from '../pages/UsersPage';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

export const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />

          {/* Protected Application Routes */}
          <Route element={<ProtectedRoute />}>
            <Route element={<DashboardLayout />}>
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
              <Route path="/dashboard" element={<DashboardPage />} />
              <Route path="/curriculum" element={<CurriculumWorkspacePage />} />
              <Route path="/agents" element={<AgentControlRoomPage />} />
              <Route path="/industry" element={<IndustryIntelligencePage />} />
              <Route path="/benchmarking" element={<AcademicBenchmarkingPage />} />
              <Route path="/gaps" element={<GapAnalysisPage />} />
              <Route path="/recommendations" element={<RecommendationsPage />} />
              <Route path="/approvals" element={<FacultyReviewPage />} />
              <Route path="/reports" element={<ReportsPage />} />

              {/* Agentic Studio Routes */}
              <Route path="/studio" element={<StudioHubPage />} />
              <Route path="/studio/:slug" element={<CapabilityDetailPage />} />

              {/* System Routes */}
              <Route path="/memory" element={<MemoryExplorerPage />} />
              <Route path="/integrations" element={<IntegrationsPage />} />
              <Route path="/users" element={<UsersPage />} />
            </Route>
          </Route>

          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </BrowserRouter>
      <Toaster richColors position="top-right" theme="dark" />
    </QueryClientProvider>
  );
};

export default App;
