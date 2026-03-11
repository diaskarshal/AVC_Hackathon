import React, { useState, useEffect } from "react";
import { Card, CardHeader, CardBody } from "../components/Card";
import Input from "../components/Input";
import Button from "../components/Button";
import { useAuth } from "../contexts/AuthContext";
import { usersAPI } from "../services/API";

const Profile: React.FC = () => {
  const { user } = useAuth();
  const [formData, setFormData] = useState({
    name: "",
    email: "",
  });
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{
    type: "success" | "error";
    text: string;
  } | null>(null);

  useEffect(() => {
    if (user) {
      setFormData({
        name: user.name,
        email: user.email,
      });
    }
  }, [user]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);

    try {
      await usersAPI.updateProfile(formData);
      setMessage({
        type: "success",
        text: "Profile updated successfully! Please log in again to see changes.",
      });
      setIsEditing(false);
    } catch (err: any) {
      setMessage({
        type: "error",
        text: err.message || "Failed to update profile",
      });
    } finally {
      setLoading(false);
    }
  };

  if (!user) return null;

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

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">My Profile</h1>
        <p className="text-gray-600 mt-1">Manage your account information</p>
      </div>

      {message && (
        <div
          className={`px-4 py-3 rounded ${
            message.type === "success"
              ? "bg-green-50 border border-green-400 text-green-700"
              : "bg-red-50 border border-red-400 text-red-700"
          }`}
        >
          {message.text}
        </div>
      )}

      {/* Profile Overview */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-medium leading-6 text-gray-900">
              Profile Information
            </h3>
            {!isEditing && (
              <Button onClick={() => setIsEditing(true)} size="sm">
                Edit Profile
              </Button>
            )}
          </div>
        </CardHeader>
        <CardBody>
          <div className="flex items-center mb-6">
            <div className="h-20 w-20 rounded-full bg-primary-100 flex items-center justify-center text-primary-600 font-bold text-3xl">
              {user.name.charAt(0)}
            </div>
            <div className="ml-6">
              <h2 className="text-2xl font-bold text-gray-900">{user.name}</h2>
              <span
                className={`mt-1 inline-block px-3 py-1 text-sm font-semibold rounded-full ${getRoleBadgeColor(user.role)}`}
              >
                {user.role.charAt(0).toUpperCase() + user.role.slice(1)}
              </span>
            </div>
          </div>

          {isEditing ? (
            <form onSubmit={handleSubmit} className="space-y-4">
              <Input
                label="Name"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                required
              />
              <Input
                label="Email"
                type="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                required
              />

              <div className="flex justify-end space-x-3 pt-4">
                <Button
                  type="button"
                  variant="secondary"
                  onClick={() => {
                    setIsEditing(false);
                    setFormData({
                      name: user.name,
                      email: user.email,
                    });
                  }}
                >
                  Cancel
                </Button>
                <Button type="submit" disabled={loading}>
                  {loading ? "Saving..." : "Save Changes"}
                </Button>
              </div>
            </form>
          ) : (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Username
                </label>
                <p className="mt-1 text-gray-900">{user.username}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Email
                </label>
                <p className="mt-1 text-gray-900">{user.email}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Role
                </label>
                <p className="mt-1 text-gray-900 capitalize">{user.role}</p>
              </div>
              {user.worker_name && (
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Worker Name
                  </label>
                  <p className="mt-1 text-gray-900">{user.worker_name}</p>
                </div>
              )}
              {user.managed_projects && user.managed_projects.length > 0 && (
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Managed Projects
                  </label>
                  <p className="mt-1 text-gray-900">
                    {user.managed_projects.length} project(s)
                  </p>
                </div>
              )}
            </div>
          )}
        </CardBody>
      </Card>

    </div>
  );
};

export default Profile;