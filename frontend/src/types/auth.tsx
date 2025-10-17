export interface User {
  username: string;
  name: string;
  email: string;
  role: "admin" | "manager" | "worker";
  worker_name?: string;
  managed_projects?: number[];
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface DemoUser {
  username: string;
  role: string;
  name: string;
  hint: string;
}