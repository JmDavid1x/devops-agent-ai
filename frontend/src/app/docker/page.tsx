'use client';

import { useEffect, useState, useCallback } from 'react';
import { Play, RotateCw, Square, RefreshCw, AlertTriangle } from 'lucide-react';
import { getContainers, restartContainer, stopContainer, startContainer } from '@/lib/api';

interface Container {
  id: string;
  name: string;
  image: string;
  status: 'running' | 'exited' | 'paused' | 'created' | 'restarting';
  state?: string;
  ports: string[];
  cpu?: string;
  memory?: string;
  created?: string;
}

export default function DockerPage() {
  const [containers, setContainers] = useState<Container[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    try {
      const response = await getContainers();
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      setContainers(data);
      setError(null);
    } catch (err) {
      console.error('Failed to fetch containers:', err);
      setError('Could not connect to Docker. Showing cached data.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, [fetchData]);

  const handleAction = async (containerId: string, action: 'restart' | 'stop' | 'start') => {
    setActionLoading(containerId);
    try {
      const fn = action === 'restart' ? restartContainer : action === 'stop' ? stopContainer : startContainer;
      const response = await fn(containerId);
      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || `Failed to ${action}`);
      }
      await new Promise(resolve => setTimeout(resolve, 1000));
      await fetchData();
    } catch (err) {
      console.error(`Failed to ${action} container:`, err);
    } finally {
      setActionLoading(null);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running':
        return 'bg-green-900/20 text-green-400';
      case 'exited':
        return 'bg-red-900/20 text-red-400';
      case 'paused':
        return 'bg-yellow-900/20 text-yellow-400';
      case 'restarting':
        return 'bg-blue-900/20 text-blue-400';
      default:
        return 'bg-gray-800/20 text-gray-400';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Docker Containers</h1>
          <p className="text-gray-400">Manage and monitor your Docker containers</p>
        </div>
        <button
          onClick={fetchData}
          className="flex items-center gap-2 px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg text-sm transition"
        >
          <RefreshCw className="w-4 h-4" />
          Refresh
        </button>
      </div>

      {error && (
        <div className="flex items-center gap-3 p-4 bg-yellow-900/20 border border-yellow-700 rounded-lg">
          <AlertTriangle className="w-5 h-5 text-yellow-400 shrink-0" />
          <p className="text-yellow-400 text-sm">{error}</p>
        </div>
      )}

      <div className="grid gap-4">
        {loading ? (
          <div className="text-center py-8 text-gray-400">Loading containers...</div>
        ) : containers.length === 0 ? (
          <div className="text-center py-8 text-gray-400">No containers found</div>
        ) : (
          containers.map(container => (
            <div
              key={container.id}
              className="bg-gray-800/50 border border-gray-700 rounded-lg p-6 hover:border-gray-600 transition"
            >
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-lg font-semibold text-white">{container.name}</h3>
                  <p className="text-sm text-gray-400">{container.image}</p>
                  <p className="text-xs text-gray-500 mt-1">ID: {container.id}</p>
                </div>
                <div className={`px-3 py-1 rounded-full text-sm font-medium capitalize ${getStatusColor(container.status)}`}>
                  {container.status}
                </div>
              </div>

              {(container.ports && container.ports.length > 0) && (
                <div className="mb-4">
                  <p className="text-sm text-gray-400 mb-2">
                    <span className="text-gray-500">Ports:</span> {container.ports.join(', ')}
                  </p>
                </div>
              )}

              <div className="flex gap-4 items-center">
                {container.cpu && (
                  <div className="text-sm text-gray-400">
                    <span className="text-gray-500">CPU:</span> {container.cpu}
                  </div>
                )}
                {container.memory && (
                  <div className="text-sm text-gray-400">
                    <span className="text-gray-500">Memory:</span> {container.memory}
                  </div>
                )}
              </div>

              <div className="flex gap-2 mt-4">
                {container.status === 'running' ? (
                  <>
                    <button
                      onClick={() => handleAction(container.id, 'restart')}
                      disabled={actionLoading === container.id}
                      className="flex items-center gap-2 px-3 py-2 bg-yellow-600 hover:bg-yellow-700 disabled:opacity-50 text-white rounded text-sm transition"
                    >
                      <RotateCw className={`w-4 h-4 ${actionLoading === container.id ? 'animate-spin' : ''}`} />
                      Restart
                    </button>
                    <button
                      onClick={() => handleAction(container.id, 'stop')}
                      disabled={actionLoading === container.id}
                      className="flex items-center gap-2 px-3 py-2 bg-red-600 hover:bg-red-700 disabled:opacity-50 text-white rounded text-sm transition"
                    >
                      <Square className="w-4 h-4" />
                      Stop
                    </button>
                  </>
                ) : (
                  <button
                    onClick={() => handleAction(container.id, 'start')}
                    disabled={actionLoading === container.id}
                    className="flex items-center gap-2 px-3 py-2 bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white rounded text-sm transition"
                  >
                    <Play className="w-4 h-4" />
                    Start
                  </button>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
