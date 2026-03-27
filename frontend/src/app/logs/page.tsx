'use client';

import { useState } from 'react';

export default function LogsPage() {
  const [selectedService, setSelectedService] = useState('api-gateway');

  const sampleLogs = [
    { timestamp: '2026-03-27 13:45:23', level: 'INFO', message: 'Request processed successfully', service: 'api-gateway' },
    { timestamp: '2026-03-27 13:45:21', level: 'WARNING', message: 'High memory usage detected', service: 'auth-service' },
    { timestamp: '2026-03-27 13:45:19', level: 'ERROR', message: 'Database connection timeout', service: 'payment-service' },
    { timestamp: '2026-03-27 13:45:15', level: 'INFO', message: 'Cache cleared successfully', service: 'api-gateway' },
    { timestamp: '2026-03-27 13:45:10', level: 'DEBUG', message: 'Processing batch job', service: 'backend' },
  ];

  const services = ['api-gateway', 'auth-service', 'payment-service', 'backend', 'database'];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-white">Service Logs</h1>
        <p className="text-gray-400">Monitor and analyze application logs</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {services.map(service => (
          <button
            key={service}
            onClick={() => setSelectedService(service)}
            className={`p-4 rounded-lg text-left transition ${
              selectedService === service
                ? 'bg-blue-600 text-white'
                : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
            }`}
          >
            <div className="font-semibold capitalize">{service}</div>
            <div className="text-sm opacity-75">View logs</div>
          </button>
        ))}
      </div>

      <div className="bg-gray-900 rounded-lg p-6 border border-gray-700">
        <h2 className="text-xl font-semibold text-white mb-4">
          Logs from: <span className="text-blue-400 capitalize">{selectedService}</span>
        </h2>

        <div className="space-y-2 max-h-96 overflow-y-auto">
          {sampleLogs.map((log, idx) => (
            <div key={idx} className={`p-3 rounded font-mono text-sm ${
              log.level === 'ERROR' ? 'bg-red-900/20 text-red-400' :
              log.level === 'WARNING' ? 'bg-yellow-900/20 text-yellow-400' :
              log.level === 'INFO' ? 'bg-blue-900/20 text-blue-400' :
              'bg-gray-800/20 text-gray-400'
            }`}>
              <span className="text-gray-500">[{log.timestamp}]</span>
              {' '}
              <span className="font-semibold">[{log.level}]</span>
              {' '}
              {log.message}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
