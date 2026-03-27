'use client';

import { useEffect, useState, useCallback } from 'react';
import { CheckCircle2, AlertCircle, Clock, Plus, Trash2, RefreshCw, Zap } from 'lucide-react';
import { getServices, createService, deleteService, checkServiceNow } from '@/lib/api';

interface Service {
  id: string;
  name: string;
  url: string;
  status: 'healthy' | 'degraded' | 'down' | 'unknown';
  last_check: string | null;
  response_time_ms?: number | null;
  is_active: boolean;
}

export default function ServicesPage() {
  const [services, setServices] = useState<Service[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formName, setFormName] = useState('');
  const [formUrl, setFormUrl] = useState('');
  const [actionLoading, setActionLoading] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    try {
      const response = await getServices();
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      setServices(data);
    } catch (error) {
      console.error('Failed to fetch services:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 15000);
    return () => clearInterval(interval);
  }, [fetchData]);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formName || !formUrl) return;
    try {
      const response = await createService({ name: formName, url: formUrl });
      if (!response.ok) {
        const data = await response.json();
        alert(data.detail || 'Failed to create service');
        return;
      }
      setFormName('');
      setFormUrl('');
      setShowForm(false);
      await fetchData();
    } catch (error) {
      console.error('Failed to create service:', error);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await deleteService(id);
      await fetchData();
    } catch (error) {
      console.error('Failed to delete service:', error);
    }
  };

  const handleCheckNow = async (id: string) => {
    setActionLoading(id);
    try {
      await checkServiceNow(id);
      await fetchData();
    } catch (error) {
      console.error('Failed to check service:', error);
    } finally {
      setActionLoading(null);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy':
        return <CheckCircle2 className="w-5 h-5 text-green-500" />;
      case 'degraded':
        return <AlertCircle className="w-5 h-5 text-yellow-500" />;
      case 'down':
        return <AlertCircle className="w-5 h-5 text-red-500" />;
      default:
        return <Clock className="w-5 h-5 text-gray-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'bg-green-900/20 text-green-400';
      case 'degraded':
        return 'bg-yellow-900/20 text-yellow-400';
      case 'down':
        return 'bg-red-900/20 text-red-400';
      default:
        return 'bg-gray-800/20 text-gray-400';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Services</h1>
          <p className="text-gray-400">Monitor your infrastructure services</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={fetchData}
            className="flex items-center gap-2 px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg text-sm transition"
          >
            <RefreshCw className="w-4 h-4" />
            Refresh
          </button>
          <button
            onClick={() => setShowForm(!showForm)}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm transition"
          >
            <Plus className="w-4 h-4" />
            Add Service
          </button>
        </div>
      </div>

      {showForm && (
        <form onSubmit={handleCreate} className="bg-gray-800/50 border border-gray-700 rounded-lg p-6 space-y-4">
          <h3 className="text-lg font-semibold text-white">Add New Service</h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-gray-400 mb-1">Service Name</label>
              <input
                type="text"
                value={formName}
                onChange={e => setFormName(e.target.value)}
                placeholder="e.g., api-gateway"
                className="w-full px-3 py-2 bg-gray-900 border border-gray-600 rounded text-white text-sm focus:outline-none focus:border-blue-500"
                required
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Health Check URL</label>
              <input
                type="url"
                value={formUrl}
                onChange={e => setFormUrl(e.target.value)}
                placeholder="e.g., http://localhost:8080/health"
                className="w-full px-3 py-2 bg-gray-900 border border-gray-600 rounded text-white text-sm focus:outline-none focus:border-blue-500"
                required
              />
            </div>
          </div>
          <div className="flex gap-2">
            <button type="submit" className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded text-sm transition">
              Create
            </button>
            <button type="button" onClick={() => setShowForm(false)} className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded text-sm transition">
              Cancel
            </button>
          </div>
        </form>
      )}

      <div className="grid gap-4">
        {loading ? (
          <div className="text-center py-8 text-gray-400">Loading services...</div>
        ) : services.length === 0 ? (
          <div className="text-center py-12 text-gray-400">
            <p className="text-lg mb-2">No services configured</p>
            <p className="text-sm">Click &quot;Add Service&quot; to start monitoring a service.</p>
          </div>
        ) : (
          services.map(service => (
            <div
              key={service.id}
              className="bg-gray-800/50 border border-gray-700 rounded-lg p-6 hover:border-gray-600 transition"
            >
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-4">
                  {getStatusIcon(service.status)}
                  <div>
                    <h3 className="text-lg font-semibold text-white capitalize">
                      {service.name}
                    </h3>
                    <p className="text-sm text-gray-400">{service.url}</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className={`px-3 py-1 rounded-full text-sm font-medium capitalize ${getStatusColor(service.status)}`}>
                    {service.status}
                  </div>
                </div>
              </div>
              <div className="mt-4 flex items-center justify-between">
                <div className="flex gap-8 text-sm text-gray-400">
                  {service.last_check && (
                    <div>
                      <span className="text-gray-500">Last Check:</span> {new Date(service.last_check).toLocaleTimeString()}
                    </div>
                  )}
                  {service.response_time_ms != null && (
                    <div>
                      <span className="text-gray-500">Response Time:</span> {service.response_time_ms}ms
                    </div>
                  )}
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleCheckNow(service.id)}
                    disabled={actionLoading === service.id}
                    className="flex items-center gap-1 px-3 py-1.5 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white rounded text-sm transition"
                  >
                    <Zap className={`w-3 h-3 ${actionLoading === service.id ? 'animate-pulse' : ''}`} />
                    Check Now
                  </button>
                  <button
                    onClick={() => handleDelete(service.id)}
                    className="flex items-center gap-1 px-3 py-1.5 bg-red-600/20 hover:bg-red-600/40 text-red-400 rounded text-sm transition"
                  >
                    <Trash2 className="w-3 h-3" />
                    Remove
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
