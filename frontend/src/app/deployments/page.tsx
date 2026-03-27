'use client';

import { CheckCircle2, AlertCircle, Clock, ArrowUpRight } from 'lucide-react';

interface Deployment {
  id: string;
  service: string;
  version: string;
  status: 'success' | 'in-progress' | 'failed';
  timestamp: string;
  duration_ms: number;
  environment: string;
}

export default function DeploymentsPage() {
  const deployments: Deployment[] = [
    {
      id: '1',
      service: 'api-gateway',
      version: '2.1.0',
      status: 'success',
      timestamp: '2026-03-27T13:30:00Z',
      duration_ms: 45000,
      environment: 'production',
    },
    {
      id: '2',
      service: 'auth-service',
      version: '1.5.3',
      status: 'in-progress',
      timestamp: '2026-03-27T13:45:00Z',
      duration_ms: 12000,
      environment: 'staging',
    },
    {
      id: '3',
      service: 'payment-service',
      version: '3.0.1',
      status: 'failed',
      timestamp: '2026-03-27T13:15:00Z',
      duration_ms: 30000,
      environment: 'staging',
    },
    {
      id: '4',
      service: 'backend',
      version: '4.2.0',
      status: 'success',
      timestamp: '2026-03-27T12:30:00Z',
      duration_ms: 60000,
      environment: 'production',
    },
  ];

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'success':
        return <CheckCircle2 className="w-5 h-5 text-green-500" />;
      case 'in-progress':
        return <Clock className="w-5 h-5 text-blue-500 animate-spin" />;
      case 'failed':
        return <AlertCircle className="w-5 h-5 text-red-500" />;
      default:
        return <Clock className="w-5 h-5 text-gray-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'success':
        return 'bg-green-900/20 text-green-400';
      case 'in-progress':
        return 'bg-blue-900/20 text-blue-400';
      case 'failed':
        return 'bg-red-900/20 text-red-400';
      default:
        return 'bg-gray-800/20 text-gray-400';
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-white">Deployments</h1>
        <p className="text-gray-400">Track and manage your deployments</p>
      </div>

      <div className="grid gap-4">
        {deployments.map(deployment => (
          <div
            key={deployment.id}
            className="bg-gray-800/50 border border-gray-700 rounded-lg p-6 hover:border-gray-600 transition"
          >
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-4">
                {getStatusIcon(deployment.status)}
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="text-lg font-semibold text-white">
                      {deployment.service}
                    </h3>
                    <span className="text-sm text-gray-400">v{deployment.version}</span>
                  </div>
                  <p className="text-sm text-gray-400 capitalize">
                    {deployment.environment} • {new Date(deployment.timestamp).toLocaleString()}
                  </p>
                </div>
              </div>
              <div className={`px-3 py-1 rounded-full text-sm font-medium capitalize ${getStatusColor(deployment.status)}`}>
                {deployment.status === 'in-progress' ? (
                  <div className="flex items-center gap-2">
                    <Clock className="w-4 h-4" />
                    In Progress
                  </div>
                ) : (
                  deployment.status
                )}
              </div>
            </div>

            <div className="mt-4 flex items-center gap-4">
              <div className="flex-1 bg-gray-700 rounded-full h-2">
                <div
                  className={`h-full rounded-full transition-all ${
                    deployment.status === 'success'
                      ? 'bg-green-500'
                      : deployment.status === 'in-progress'
                      ? 'bg-blue-500'
                      : 'bg-red-500'
                  }`}
                  style={{
                    width: deployment.status === 'in-progress' ? '60%' : '100%',
                  }}
                />
              </div>
              <span className="text-sm text-gray-400 whitespace-nowrap">
                {(deployment.duration_ms / 1000).toFixed(1)}s
              </span>
            </div>

            {deployment.status === 'failed' && (
              <div className="mt-4 p-3 bg-red-900/20 border border-red-700 rounded text-red-400 text-sm">
                Deployment failed. Check logs for details.
              </div>
            )}

            <div className="flex gap-2 mt-4">
              <button className="flex items-center gap-2 px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded text-sm transition">
                <ArrowUpRight className="w-4 h-4" />
                View Details
              </button>
              {deployment.status === 'failed' && (
                <button className="flex items-center gap-2 px-3 py-2 bg-yellow-600 hover:bg-yellow-700 text-white rounded text-sm transition">
                  Retry
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
