import React, { useState, useEffect } from "react";
import { useAuth } from "../contexts/AuthContext";
import { authAPI } from "../services/API";
import { DemoUser } from "../types/auth";
import Button from "../components/Button";
import Input from "../components/Input";

const Login: React.FC = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [demoUsers, setDemoUsers] = useState<DemoUser[]>([]);
  const { login } = useAuth();

  useEffect(() => {
    fetchDemoUsers();
  }, []);

  const fetchDemoUsers = async () => {
    try {
      const response = await authAPI.getDemoUsers();
      setDemoUsers(response.data);
    } catch (err) {
      console.error("Failed to fetch demo users:", err);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await login({ username, password });
    } catch (err: any) {
      setError(err.message || "Ошибка входа. Попробуйте ещё раз.");
    } finally {
      setLoading(false);
    }
  };

  const quickLogin = (user: DemoUser) => {
    setUsername(user.username);
    const passwordMatch = user.hint.match(/Password: (\w+)/);
    if (passwordMatch) {
      setPassword(passwordMatch[1]);
    }
  };

  const getRoleBadgeColor = (role: string) => {
    switch (role) {
      case "admin":
        return "bg-red-100 text-red-800";
      case "manager":
        return "bg-blue-100 text-blue-800";
      case "worker":
        return "bg-green-100 text-green-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  const getRoleLabel = (role: string) => {
    switch (role) {
      case "admin": return "Администратор";
      case "manager": return "Менеджер";
      case "worker": return "Сотрудник";
      default: return role;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100 flex items-center justify-center px-4">
      <div className="max-w-6xl w-full grid md:grid-cols-2 gap-8">
        {/* Login Form */}
        <div className="bg-white rounded-lg shadow-xl p-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              BuildFlow ERP
            </h1>
            <p className="text-gray-600">
              Система управления ремонтными проектами
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <Input
              label="Логин"
              name="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Введите логин"
              required
            />

            <Input
              label="Пароль"
              type="password"
              name="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Введите пароль"
              required
            />

            {error && (
              <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded">
                {error}
              </div>
            )}

            <Button
              type="submit"
              className="w-full"
              disabled={loading}
            >
              {loading ? "Вход..." : "Войти"}
            </Button>
          </form>

          <div className="mt-6 text-center text-sm text-gray-600">
            <p>Доступны демо-аккаунты →</p>
          </div>

          {/* AVC GROUP banner */}
          <div className="mt-6 rounded-xl border border-gray-200 bg-gray-50 px-5 py-4">
            <div className="flex items-center gap-3 mb-3">
              <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-primary-700 shrink-0">
                <span className="text-white font-black text-sm">AVC</span>
              </div>
              <div>
                <p className="font-bold text-gray-900 text-base leading-tight">AVC GROUP</p>
                <p className="text-gray-500 text-xs tracking-widest uppercase">BuildFlow — система управления ремонтами</p>
              </div>
            </div>
            <div className="grid grid-cols-3 gap-3 text-center pt-3 border-t border-gray-200">
              <div>
                <p className="text-xl font-black text-gray-900">1 000+</p>
                <p className="text-gray-500 text-xs leading-tight">сотрудников<br />в штате</p>
              </div>
              <div className="border-l border-gray-200">
                <p className="text-xl font-black text-gray-900">150+</p>
                <p className="text-gray-500 text-xs leading-tight">квалиф.<br />ИТР</p>
              </div>
              <div className="border-l border-gray-200">
                <p className="text-xl font-black text-gray-900">47+</p>
                <p className="text-gray-500 text-xs leading-tight">установок<br />АНПЗ · ПНХЗ</p>
              </div>
            </div>
          </div>
        </div>

        {/* Demo Users Panel */}
        <div className="bg-white rounded-lg shadow-xl p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Демо-аккаунты
          </h2>
          <p className="text-gray-600 mb-6">
            Нажмите на аккаунт для автозаполнения
          </p>

          <div className="space-y-3">
            {demoUsers.map((user) => (
              <button
                key={user.username}
                onClick={() => quickLogin(user)}
                className="w-full text-left p-4 border-2 border-gray-200 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition-colors"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-semibold text-gray-900">
                    {user.name}
                  </span>
                  <span
                    className={`px-2 py-1 text-xs font-semibold rounded-full ${getRoleBadgeColor(user.role)}`}
                  >
                    {getRoleLabel(user.role)}
                  </span>
                </div>
                <div className="text-sm text-gray-600">
                  <div>Логин: {user.username}</div>
                  <div className="text-xs text-gray-500 mt-1">
                    {user.hint}
                  </div>
                </div>
              </button>
            ))}
          </div>

          <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <h3 className="font-semibold text-blue-900 mb-2">
              Описание ролей:
            </h3>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>
                <strong>Администратор:</strong> Полный доступ к системе
              </li>
              <li>
                <strong>Менеджер:</strong> Управление назначенными проектами
              </li>
              <li>
                <strong>Сотрудник:</strong> Просмотр и обновление своих задач
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;