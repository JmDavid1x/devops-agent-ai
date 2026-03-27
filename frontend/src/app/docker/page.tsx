'use client';

import { useEffect, useState } from 'react';
import { Play, RotateCw, Square } from 'lucide-react';

interface Container {
  id: string;
  name: string;
  image: string;
  status: 'running' | 'exited' | 'paused';
  ports: string[];
  cpu?: string;
  memory?: string;
}

export default function DockerPage() {
  const [containers, setContainers] = useState<Container[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchContainers = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/docker/containers');
        const data = await response.json();
        setContainers(data);
      } catch (error) {
        console.error('Failed to fetch containers:', error);
        // Use mock data if API fails
        setContainers([
          { id: 'abc123', name: 'nginx-proxy', image: 'nginx:latest', status: 'running', ports: ['80:80', '443:443'], cpu: '2%', memory: '45MB' },
          { id: 'def456', name: 'postgres-db', image: 'postgres:16', status: 'running', ports: ['5432:5432'], cpu: '5%', memory: '128MB' },
          { id: 'ghi789', name: 'redis-cache', image: 'redis:7-alpine', status: 'exited', ports: [], cpu: '0%', memory: '0MB' },
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchContainers();
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running':
        return 'bg-green-900/20 text-green-400';
      case 'exited':
        return 'bg-red-900/20 text-red-400';
      case 'paused':
        return 'bg-yellow-900/20 text-yellow-400';
      default:
        return 'bg-gray-800/20 text-gray-400';
    }
  };

  const handleRestart = async (containerId: string) => {
    try {
      await fetch(`http://localhost:8000/api/docker/containers/${containerId}/restart`, {
        method: 'POST',
      });
      // Refresh containers
      const response = await fetch('http://localhost:8000/api/docker/containers');
      const data = await response.json();
      setContainers(data);
    } catch (error) {
      console.error('Failed to restart container:', error);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-white">Docker Containers</h1>
        <p className="text-gray-400">Manage and monitor your Docker containers</p>
      </div>

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

              <div className="flex gap-2 items-center">
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
                      onClick={() => handleRestart(container.id)}
                      className="flex items-center gap-2 px-3 py-2 bg-yellow-600 hover:bg-yellow-700 text-white rounded text-sm transition"
                    >
                      <RotateCw className="w-4 h-4" />
                      Restart
                    </button>
                    <button className="flex items-center gap-2 px-3 py-2 bg-red-600 hover:bg-red-700 text-white rounded text-sm transition">
                      <Square className="w-4 h-4" />
                      Stop
                    </button>
                  </>
                ) : (
                  <button className="flex items-center gap-2 px-3 py-2 bg-green-600 hover:bg-green-700 text-white rounded text-sm transition">
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
