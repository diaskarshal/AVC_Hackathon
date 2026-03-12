import React, { useEffect, useState } from "react";
import { Card, CardHeader, CardBody } from "../components/Card";
import {
  Table,
  TableHeader,
  TableBody,
  TableHead,
  TableCell,
} from "../components/Table";
import { usersAPI, TeamMember } from "../services/API";

const Users: React.FC = () => {
  const [users, setUsers] = useState<TeamMember[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const response = await usersAPI.getAll();
      setUsers(response.data);
      setError(null);
    } catch (err: any) {
      setError(err.message || "Ошибка загрузки пользователей");
    } finally {
      setLoading(false);
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


  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Загрузка...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded">
        Ошибка: {error}
      </div>
    );
  }

  const adminUsers = users.filter((u) => u.role === "admin");
  const managerUsers = users.filter((u) => u.role === "manager");
  const workerUsers = users.filter((u) => u.role === "worker");

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Управление пользователями</h1>
          <p className="text-gray-600 mt-1">
            Управление пользователями системы и их ролями
          </p>
        </div>
        <button
          onClick={fetchUsers}
          className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
        >
          Обновить
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Всего пользователей</div>
            <div className="text-2xl font-bold text-gray-900">
              {users.length}
            </div>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Администраторы</div>
            <div className="text-2xl font-bold text-red-600">
              {adminUsers.length}
            </div>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Менеджеры</div>
            <div className="text-2xl font-bold text-blue-600">
              {managerUsers.length}
            </div>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Сотрудники</div>
            <div className="text-2xl font-bold text-green-600">
              {workerUsers.length}
            </div>
          </CardBody>
        </Card>
      </div>

      {/* Administrators */}
      <Card>
        <CardHeader>
          <h3 className="text-lg font-medium leading-6 text-gray-900">
            Администраторы
          </h3>
        </CardHeader>
        <Table>
          <TableHeader>
            <TableHead>Пользователь</TableHead>
            <TableHead>Логин</TableHead>
            <TableHead>Email</TableHead>
            <TableHead>Роль</TableHead>
          </TableHeader>
          <TableBody>
            {adminUsers.map((user) => (
              <tr key={user.username}>
                <TableCell>
                  <div className="flex items-center">
                    <div className="h-10 w-10 rounded-full bg-red-100 flex items-center justify-center text-red-600 font-bold mr-3">
                      {user.name.charAt(0)}
                    </div>
                    <div className="font-medium text-gray-900">
                      {user.name}
                    </div>
                  </div>
                </TableCell>
                <TableCell>{user.username}</TableCell>
                <TableCell>{user.email}</TableCell>
                <TableCell>
                  <span
                    className={`px-2 py-1 text-xs font-semibold rounded-full ${getRoleBadgeColor(user.role)}`}
                  >
                    {getRoleLabel(user.role)}
                  </span>
                </TableCell>
              </tr>
            ))}
          </TableBody>
        </Table>
      </Card>

      {/* Managers */}
      <Card>
        <CardHeader>
          <h3 className="text-lg font-medium leading-6 text-gray-900">
            Менеджеры проектов
          </h3>
        </CardHeader>
        <Table>
          <TableHeader>
            <TableHead>Пользователь</TableHead>
            <TableHead>Логин</TableHead>
            <TableHead>Email</TableHead>
            <TableHead>Проекты</TableHead>
            <TableHead>Роль</TableHead>
          </TableHeader>
          <TableBody>
            {managerUsers.map((user) => (
              <tr key={user.username}>
                <TableCell>
                  <div className="flex items-center">
                    <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold mr-3">
                      {user.name.charAt(0)}
                    </div>
                    <div className="font-medium text-gray-900">
                      {user.name}
                    </div>
                  </div>
                </TableCell>
                <TableCell>{user.username}</TableCell>
                <TableCell>{user.email}</TableCell>
                <TableCell>
                  {user.managed_projects && user.managed_projects.length > 0 ? (
                    <span className="text-sm text-gray-600">
                      {user.managed_projects.length} проект(ов)
                    </span>
                  ) : (
                    <span className="text-sm text-gray-400">
                      Нет проектов
                    </span>
                  )}
                </TableCell>
                <TableCell>
                  <span
                    className={`px-2 py-1 text-xs font-semibold rounded-full ${getRoleBadgeColor(user.role)}`}
                  >
                    {getRoleLabel(user.role)}
                  </span>
                </TableCell>
              </tr>
            ))}
          </TableBody>
        </Table>
      </Card>

      {/* Workers */}
      <Card>
        <CardHeader>
          <h3 className="text-lg font-medium leading-6 text-gray-900">
            Сотрудники
          </h3>
        </CardHeader>
        <Table>
          <TableHeader>
            <TableHead>Пользователь</TableHead>
            <TableHead>Логин</TableHead>
            <TableHead>Email</TableHead>
            <TableHead>Имя сотрудника</TableHead>
            <TableHead>Роль</TableHead>
          </TableHeader>
          <TableBody>
            {workerUsers.map((user) => (
              <tr key={user.username}>
                <TableCell>
                  <div className="flex items-center">
                    <div className="h-10 w-10 rounded-full bg-green-100 flex items-center justify-center text-green-600 font-bold mr-3">
                      {user.name.charAt(0)}
                    </div>
                    <div className="font-medium text-gray-900">
                      {user.name}
                    </div>
                  </div>
                </TableCell>
                <TableCell>{user.username}</TableCell>
                <TableCell>{user.email}</TableCell>
                <TableCell>
                  <span className="text-sm text-gray-600">
                    {user.worker_name || "N/A"}
                  </span>
                </TableCell>
                <TableCell>
                  <span
                    className={`px-2 py-1 text-xs font-semibold rounded-full ${getRoleBadgeColor(user.role)}`}
                  >
                    {getRoleLabel(user.role)}
                  </span>
                </TableCell>
              </tr>
            ))}
          </TableBody>
        </Table>
      </Card>
    </div>
  );
};

export default Users;