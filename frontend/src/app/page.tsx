"use client";

import { useEffect, useState } from 'react';
import { apiFetch } from '@/lib/api';
import { useRouter } from 'next/navigation';

export default function Dashboard() {
  const [projects, setProjects] = useState([]);
  const [tasks, setTasks] = useState([]);
  const router = useRouter();

  useEffect(() => {
    const loadData = async () => {
      try {
        const projData = await apiFetch("/projects/");
        setProjects(projData);
        const taskData = await apiFetch("/tasks/");
        setTasks(taskData);
      } catch (err) {
        // usually handle error or drop down to login interceptor in apiFetch
      }
    };
    loadData();
  }, []);

  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-800">PM Dashboard</h1>
        <button 
          onClick={() => { localStorage.removeItem("token"); router.push("/login"); }}
          className="bg-red-500 text-white px-4 py-2 rounded"
        >
          Logout
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-white p-6 rounded shadow">
          <h2 className="text-xl font-bold mb-4">Projects</h2>
          <ul>
            {projects.map((p: any) => (
              <li key={p.id} className="border-b py-2 text-gray-700">
                <strong>{p.name}</strong> - {p.description || "No description"}
              </li>
            ))}
            {projects.length === 0 && <p className="text-gray-500">No projects found.</p>}
          </ul>
        </div>
        
        <div className="bg-white p-6 rounded shadow">
          <h2 className="text-xl font-bold mb-4">Tasks</h2>
          <ul>
            {tasks.map((t: any) => (
              <li key={t.id} className="border-b py-2 text-gray-700">
                <strong>{t.title}</strong>
                <span className="ml-2 px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">
                  {t.status}
                </span>
              </li>
            ))}
            {tasks.length === 0 && <p className="text-gray-500">No tasks found.</p>}
          </ul>
        </div>
      </div>
    </div>
  );
}
