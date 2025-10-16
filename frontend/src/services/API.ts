import axios from "axios";

const API_BASE_URL =
  process.env.REACT_APP_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export interface Project {
  id: number;
  name: string;
  description?: string;
  status: string;
  start_date?: string;
  planned_end_date?: string;
  actual_end_date?: string;
  total_budget: number;
  spent_amount: number;
  budget_utilization: number;
  remaining_budget: number;
  location?: string;
  created_at: string;
  updated_at: string;
}

export interface Task {
  id: number;
  project_id: number;
  name: string;
  description?: string;
  status: string;
  priority: string;
  start_date?: string;
  planned_end_date?: string;
  actual_end_date?: string;
  progress_percentage: number;
  assigned_to?: string;
  is_overdue: boolean;
  created_at: string;
  updated_at: string;
}

export interface Resource {
  id: number;
  project_id: number;
  name: string;
  resource_type: string;
  status: string;
  quantity: number;
  unit?: string;
  unit_cost: number;
  total_cost: number;
  supplier?: string;
  allocated_date: string;
  created_at: string;
  updated_at: string;
}

export interface Budget {
  id: number;
  project_id: number;
  category: string;
  description?: string;
  planned_amount: number;
  actual_amount: number;
  variance: number;
  variance_percentage: number;
  budget_date: string;
  created_at: string;
  updated_at: string;
}

export interface DashboardStats {
  total_projects: number;
  active_projects: number;
  completed_projects: number;
  total_budget: number;
  total_spent: number;
  budget_utilization: number;
  total_tasks: number;
  completed_tasks: number;
  overdue_tasks: number;
  task_completion_rate: number;
}

export interface TeamMember {
  username: string;
  role: string;
  name: string;
  email: string;
  worker_name?: string;
  managed_projects?: number[];
}

export interface TeamPerformance {
  worker_name: string;
  total_tasks: number;
  completed_tasks: number;
  avg_progress: number;
  completion_rate: number;
}

export interface ActivityLog {
  id: number;
  user: string;
  action: string;
  timestamp: string;
  details: string;
}

// Projects
export const projectsAPI = {
  getAll: () => api.get<Project[]>("/api/projects/"),
  getById: (id: number) => api.get<Project>(`/api/projects/${id}`),
  create: (data: Partial<Project>) =>
    api.post<Project>("/api/projects/", data),
  update: (id: number, data: Partial<Project>) =>
    api.put<Project>(`/api/projects/${id}`, data),
  delete: (id: number) => api.delete(`/api/projects/${id}`),
  getSummary: () => api.get("/api/projects/summary"),
};

// Tasks
export const tasksAPI = {
  getAll: (params?: { project_id?: number; status?: string }) =>
    api.get<Task[]>("/api/tasks/", { params }),
  getById: (id: number) => api.get<Task>(`/api/tasks/${id}`),
  create: (data: Partial<Task>) => api.post<Task>("/api/tasks/", data),
  update: (id: number, data: Partial<Task>) =>
    api.put<Task>(`/api/tasks/${id}`, data),
  delete: (id: number) => api.delete(`/api/tasks/${id}`),
  getOverdue: (projectId: number) =>
    api.get<Task[]>(`/api/tasks/project/${projectId}/overdue`),
};

// Resources
export const resourcesAPI = {
  getAll: (params?: {
    project_id?: number;
    resource_type?: string;
  }) => api.get<Resource[]>("/api/resources/", { params }),
  getById: (id: number) => api.get<Resource>(`/api/resources/${id}`),
  create: (data: Partial<Resource>) =>
    api.post<Resource>("/api/resources/", data),
  update: (id: number, data: Partial<Resource>) =>
    api.put<Resource>(`/api/resources/${id}`, data),
  delete: (id: number) => api.delete(`/api/resources/${id}`),
};

// Budgets
export const budgetsAPI = {
  getAll: (params?: { project_id?: number; category?: string }) =>
    api.get<Budget[]>("/api/budgets/", { params }),
  getById: (id: number) => api.get<Budget>(`/api/budgets/${id}`),
  create: (data: Partial<Budget>) =>
    api.post<Budget>("/api/budgets/", data),
  update: (id: number, data: Partial<Budget>) =>
    api.put<Budget>(`/api/budgets/${id}`, data),
  delete: (id: number) => api.delete(`/api/budgets/${id}`),
};

export const usersAPI = {
  getAll: () => api.get<TeamMember[]>("/api/users/"),
  getProfile: () => api.get<TeamMember>("/api/users/profile"),
  updateProfile: (data: Partial<TeamMember>) =>
    api.put<TeamMember>("/api/users/profile", data),
  getTeam: () => api.get<TeamMember[]>("/api/users/team"),
  getActivityLog: (limit: number = 50) =>
    api.get<ActivityLog[]>(`/api/users/activity-log?limit=${limit}`),
};

export const analyticsAPI = {
  getDashboard: () => api.get<DashboardStats>("/api/analytics/dashboard"),
  getProjectKPI: (projectId: number) =>
    api.get(`/api/analytics/project/${projectId}/kpi`),
  getBudgetBreakdown: (projectId: number) =>
    api.get(`/api/analytics/project/${projectId}/budget-breakdown`),
  getResourceDistribution: (projectId: number) =>
    api.get(`/api/analytics/project/${projectId}/resource-distribution`),
  getTimeline: (projectId: number) =>
    api.get(`/api/analytics/project/${projectId}/timeline`),
  predictCompletion: (projectId: number) =>
    api.get(`/api/analytics/project/${projectId}/predict-completion`),
  getTeamPerformance: (projectId?: number) =>
    api.get<{ team_members: number; performance: TeamPerformance[] }>(
      `/api/analytics/team-performance${projectId ? `?project_id=${projectId}` : ""}`
    ),
};

export const importAPI = {
  uploadExcel: (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    return api.post("/api/import/excel", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  },
  uploadCSV: (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    return api.post("/api/import/csv", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  },
};

export const authAPI = {
  login: (credentials: { username: string; password: string }) =>
    api.post("/api/auth/login", credentials),
  getCurrentUser: (token: string) =>
    api.get("/api/auth/me", {
      headers: { Authorization: `Bearer ${token}` },
    }),
  getDemoUsers: () => api.get("/api/auth/demo-users"),
};



export default api;