import React from "react";
import { Card, CardHeader, CardBody } from "./Card";

interface Activity {
  id: number;
  user: string;
  action: string;
  timestamp: string;
  details: string;
}

interface ActivityLogProps {
  activities: Activity[];
}

const ActivityLog: React.FC<ActivityLogProps> = ({ activities }) => {
  const getActivityIcon = (action: string) => {
    if (action.includes("create")) return "➕";
    if (action.includes("update")) return "✏️";
    if (action.includes("delete")) return "🗑️";
    if (action.includes("login")) return "🔐";
    return "📝";
  };

  return (
    <Card>
      <CardHeader>
        <h3 className="text-lg font-medium leading-6 text-gray-900">
          Recent Activity
        </h3>
      </CardHeader>
      <CardBody>
        {activities.length > 0 ? (
          <div className="flow-root">
            <ul className="-mb-8">
              {activities.map((activity, idx) => (
                <li key={activity.id}>
                  <div className="relative pb-8">
                    {idx !== activities.length - 1 && (
                      <span
                        className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200"
                        aria-hidden="true"
                      />
                    )}
                    <div className="relative flex space-x-3">
                      <div>
                        <span className="h-8 w-8 rounded-full bg-primary-100 flex items-center justify-center text-lg">
                          {getActivityIcon(activity.action)}
                        </span>
                      </div>
                      <div className="flex-1 min-w-0">
                        <div>
                          <p className="text-sm text-gray-900">
                            <span className="font-medium">{activity.user}</span>{" "}
                            {activity.action}
                          </p>
                          <p className="text-xs text-gray-500 mt-0.5">
                            {new Date(activity.timestamp).toLocaleString()}
                          </p>
                        </div>
                        {activity.details && (
                          <p className="text-sm text-gray-600 mt-1">
                            {activity.details}
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            <p>No recent activity</p>
          </div>
        )}
      </CardBody>
    </Card>
  );
};

export default ActivityLog;