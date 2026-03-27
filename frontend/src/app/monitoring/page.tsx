'use client';

import { useEffect, useState, useCallback } from 'react';
import { BarChart3, Users, MessageSquare, Server, Activity, RefreshCw, ExternalLink, CheckCircle2, AlertCircle, Clock } from 'lucide-react';
import { getMetricsSummary } from '@/lib/api';

interface ServiceHealth {
  name: string;
  status: string;
  response_time_ms: number | null;
  last_check: string | null;
}

interface MetricsSummary {
  users: number;
  conversations: number;
  messages: number;
  services: number;
  health_checks_performed: number;
  service_health: ServiceHealth[];
}

export default function MonitoringPage() {
  const [metrics, setMetrics] = useState<MetricsSummary | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchData = useCallback(async () => {
    try {
      const response = await getMetricsSummary();
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      setMetrics(data);
    } catch (error) {
      console.error('Failed to fetch metrics:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 15000);
    return () => clearInterval(interval);
  }, [fetchData]);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy': return <CheckCircle2 className="w-4 h-4 text-green-400" />;
      case 'degraded': return <AlertCircle className="w-4 h-4 text-yellow-400" />;
      case 'down': return <AlertCircle className="w-4 h-4 text-red-400" />;
      default: return <Clock className="w-4 h-4 text-gray-400" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy': return 'text-green-400';
      case 'degraded': return 'text-yellow-400';
      case 'down': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-gray-400">Loading metrics...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6 p-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Monitoring</h1>
          <p className="text-gray-400">System metrics and health overview</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={fetchData}
            className="flex items-center gap-2 px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg text-sm transition"
          >
            <RefreshCw className="w-4 h-4" />
            Refresh
          </button>
          <a
            href="http://localhost:3001"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 px-4 py-2 bg-orange-600 hover:bg-orange-700 text-white rounded-lg text-sm transition"
          >
            <ExternalLink className="w-4 h-4" />
            Open Grafana
          </a>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-5">
          <div className="flex items-center gap-3 mb-2">
            <Users className="w-5 h-5 text-blue-400" />
            <span className="text-sm text-gray-400">Users</span>
          </div>
          <p className="text-2xl font-bold text-white">{metrics?.users ?? 0}</p>
        </div>

        <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-5">
          <div className="flex items-center gap-3 mb-2">
            <MessageSquare className="w-5 h-5 text-green-400" />
            <span className="text-sm text-gray-400">Conversations</span>
          </div>
          <p className="text-2xl font-bold text-white">{metrics?.conversations ?? 0}</p>
        </div>

        <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-5">
          <div className="flex items-center gap-3 mb-2">
            <BarChart3 className="w-5 h-5 text-purple-400" />
            <span className="text-sm text-gray-400">Messages</span>
          </div>
          <p className="text-2xl font-bold text-white">{metrics?.messages ?? 0}</p>
        </div>

        <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-5">
          <div className="flex items-center gap-3 mb-2">
            <Server className="w-5 h-5 text-yellow-400" />
            <span className="text-sm text-gray-400">Services</span>
          </div>
          <p className="text-2xl font-bold text-white">{metrics?.services ?? 0}</p>
        </div>

        <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-5">
          <div className="flex items-center gap-3 mb-2">
            <Activity className="w-5 h-5 text-cyan-400" />
            <span className="text-sm text-gray-400">Health Checks</span>
          </div>
          <p className="text-2xl font-bold text-white">{metrics?.health_checks_performed ?? 0}</p>
        </div>
      </div>

      {/* Service Health */}
      <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-6">
        <h2 className="text-lg font-semibold text-white mb-4">Service Health Status</h2>
        {metrics?.service_health && metrics.service_health.length > 0 ? (
          <div className="space-y-3">
            {metrics.service_health.map((svc) => (
              <div key={svc.name} className="flex items-center justify-between py-3 border-b border-gray-700 last:border-0">
                <div className="flex items-center gap-3">
                  {getStatusIcon(svc.status)}
                  <span className="text-white font-medium">{svc.name}</span>
                </div>
                <div className="flex items-center gap-6 text-sm">
                  <span className={`capitalize font-medium ${getStatusColor(svc.status)}`}>{svc.status}</span>
                  {svc.response_time_ms != null && (
                    <span className="text-gray-400">{svc.response_time_ms}ms</span>
                  )}
                  {svc.last_check && (
                    <span className="text-gray-500">{new Date(svc.last_check).toLocaleTimeString()}</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-400 text-sm">No services configured. Add services in the Services page.</p>
        )}
      </div>

      {/* Grafana Embed */}
      <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-white">Grafana Dashboard</h2>
          <a
            href="http://localhost:3001/d/devops-overview"
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-blue-400 hover:text-blue-300 flex items-center gap-1 transition"
          >
            Open full dashboard <ExternalLink className="w-3 h-3" />
          </a>
        </div>
        <div className="bg-gray-900 rounded-lg overflow-hidden" style={{ height: '500px' }}>
          <iframe
            src="http://localhost:3001/d/devops-overview?orgId=1&kiosk&theme=dark"
            width="100%"
            height="100%"
            frameBorder="0"
            title="Grafana Dashboard"
            className="rounded-lg"
          />
        </div>
        <p className="text-xs text-gray-500 mt-2">
          Grafana runs on port 3001. Start it with: docker compose up grafana prometheus
        </p>
      </div>
    </div>
  );
}
