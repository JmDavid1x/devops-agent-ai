'use client';

import { useEffect, useState } from 'react';
import { CheckCircle2, AlertCircle, Clock } from 'lucide-react';

interface Service {
  id: string;
  name: string;
  url: string;
  status: 'healthy' | 'degraded' | 'down';
  last_check: string;
  response_time_ms?: number;
}

export default function ServicesPage() {
  const [services, setServices] = useState<Service[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchServices = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/services');
        const data = await response.json();
        setServices(data);
      } catch (error) {
        console.error('Failed to fetch services:', error);
        // Use mock data if API fails
        setServices([
          { id: 'svc-1', name: 'api-gateway', url: 'http://localhost:8080', status: 'healthy', last_check: '2026-03-27T13:45:00Z', response_time_ms: 45 },
          { id: 'svc-2', name: 'auth-service', url: 'http://localhost:8081', status: 'healthy', last_check: '2026-03-27T13:44:50Z', response_time_ms: 62 },
          { id: 'svc-3', name: 'payment-service', url: 'http://localhost:8082', status: 'degraded', last_check: '2026-03-27T13:44:30Z', response_time_ms: 2500 },
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchServices();
    const interval = setInterval(fetchServices, 30000); // Refresh every 30s
    return () => clearInterval(interval);
  }, []);

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
      <div>
        <h1 className="text-3xl font-bold text-white">Services</h1>
        <p className="text-gray-400">Monitor your infrastructure services</p>
      </div>

      <div className="grid gap-4">
        {loading ? (
          <div className="text-center py-8 text-gray-400">Loading services...</div>
        ) : services.length === 0 ? (
          <div className="text-center py-8 text-gray-400">No services found</div>
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
                <div className={`px-3 py-1 rounded-full text-sm font-medium capitalize ${getStatusColor(service.status)}`}>
                  {service.status}
                </div>
              </div>
              <div className="mt-4 flex gap-8 text-sm text-gray-400">
                <div>
                  <span className="text-gray-500">Last Check:</span> {new Date(service.last_check).toLocaleTimeString()}
                </div>
                {service.response_time_ms && (
                  <div>
                    <span className="text-gray-500">Response Time:</span> {service.response_time_ms}ms
                  </div>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
