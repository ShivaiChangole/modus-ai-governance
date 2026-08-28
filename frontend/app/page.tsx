'use client';

import React, { useState } from 'react';
import { submitAssessment, UseCaseRequest, GovernanceAssessmentResponse } from '@/lib/api';

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState<UseCaseRequest>({
    title: '',
    industry: 'Human Resources',
    description: '',
    data_types: [],
    deployment_scope: 'Internal',
  });
  const [dataTypeInput, setDataTypeInput] = useState('');
  const [assessment, setAssessment] = useState<GovernanceAssessmentResponse | null>(null);
  const [error, setError] = useState('');

  const handleAddDataType = () => {
    if (dataTypeInput.trim() && !formData.data_types.includes(dataTypeInput.trim())) {
      setFormData({
        ...formData,
        data_types: [...formData.data_types, dataTypeInput.trim()],
      });
      setDataTypeInput('');
    }
  };

  const handleRemoveDataType = (tag: string) => {
    setFormData({
      ...formData,
      data_types: formData.data_types.filter((t) => t !== tag),
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const result = await submitAssessment(formData);
      setAssessment(result);
    } catch (err: any) {
      setError(err.message || 'Failed to submit evaluation request');
    } finally {
      setLoading(false);
    }
  };

  const getBadgeColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'critical risk':
      case 'critical':
      case 'high risk':
      case 'high':
        return 'bg-red-500/10 text-red-400 border-red-500/20';
      case 'medium risk':
      case 'medium':
        return 'bg-amber-500/10 text-amber-400 border-amber-500/20';
      default:
        return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 p-6 md:p-12">
      <div className="max-w-7xl mx-auto space-y-8">
        <header className="border-b border-slate-800 pb-6">
          <h1 className="text-3xl md:text-4xl font-bold tracking-tight text-white">
            AI Governance & Risk Assessment Engine
          </h1>
          <p className="mt-2 text-slate-400 text-sm md:text-base">
            Evaluate enterprise AI use cases against regulatory frameworks, industry standards, and risk metrics.
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          <div className="lg:col-span-5 bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
            <h2 className="text-xl font-semibold text-white">Use Case Profile</h2>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-300 uppercase tracking-wider mb-2">
                  System Title
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g., Automated Hiring & Screening Model"
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 uppercase tracking-wider mb-2">
                  Industry Sector
                </label>
                <select
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500"
                  value={formData.industry}
                  onChange={(e) => setFormData({ ...formData, industry: e.target.value })}
                >
                  <option value="Human Resources">Human Resources / Employment</option>
                  <option value="Finance">Financial Services & Credit</option>
                  <option value="Healthcare">Healthcare & Life Sciences</option>
                  <option value="Critical Infrastructure">Critical Infrastructure</option>
                  <option value="General Enterprise">General Enterprise</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 uppercase tracking-wider mb-2">
                  Data Attributes / Types
                </label>
                <div className="flex gap-2 mb-2">
                  <input
                    type="text"
                    placeholder="e.g., PII, Resume Data, Medical Records"
                    className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
                    value={dataTypeInput}
                    onChange={(e) => setDataTypeInput(e.target.value)}
                  />
                  <button
                    type="button"
                    onClick={handleAddDataType}
                    className="bg-slate-800 hover:bg-slate-700 text-white px-3 py-2 rounded-lg text-xs font-medium"
                  >
                    Add
                  </button>
                </div>
                <div className="flex flex-wrap gap-2">
                  {formData.data_types.map((tag) => (
                    <span
                      key={tag}
                      className="bg-slate-800 text-slate-300 text-xs px-2.5 py-1 rounded-full flex items-center gap-1.5 border border-slate-700"
                    >
                      {tag}
                      <button
                        type="button"
                        onClick={() => handleRemoveDataType(tag)}
                        className="hover:text-red-400"
                      >
                        ×
                      </button>
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 uppercase tracking-wider mb-2">
                  System Architecture Description
                </label>
                <textarea
                  required
                  rows={4}
                  placeholder="Describe model architecture, data inputs, decision pipelines, and deployment scope..."
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                />
              </div>

              {error && (
                <div className="p-3 bg-red-500/10 border border-red-500/20 text-red-400 rounded-lg text-xs">
                  {error}
                </div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-blue-600 hover:bg-blue-500 disabled:bg-slate-800 text-white font-medium py-3 rounded-lg text-sm transition"
              >
                {loading ? 'Evaluating Governance Frameworks...' : 'Run Risk Assessment'}
              </button>
            </form>
          </div>

          <div className="lg:col-span-7 space-y-6">
            {assessment ? (
              <div className="space-y-6">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                  <div>
                    <h3 className="text-sm font-medium text-slate-400 uppercase tracking-wider">
                      Overall Risk Assessment
                    </h3>
                    <p className="text-2xl font-bold text-white mt-1">
                      {assessment.use_case_title}
                    </p>
                    <span className="text-xs text-slate-400 mt-1 block">
                      Industry Sector: {assessment.industry}
                    </span>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="text-right">
                      <div className="text-3xl font-extrabold text-white">
                        {assessment.overall_score}<span className="text-slate-500 text-base">/100</span>
                      </div>
                      <span className={`inline-block mt-1 text-xs px-2.5 py-0.5 rounded-full border font-semibold ${getBadgeColor(assessment.overall_risk_level)}`}>
                        {assessment.overall_risk_level}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-4">
                  <h3 className="text-base font-semibold text-white">Governance Risk Breakdown</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {assessment.risk_breakdown.map((item) => (
                      <div key={item.category} className="bg-slate-950 border border-slate-800/80 rounded-lg p-4 space-y-2">
                        <div className="flex justify-between items-center">
                          <span className="text-sm font-medium text-slate-200">{item.category}</span>
                          <span className={`text-xs px-2 py-0.5 rounded border font-medium ${getBadgeColor(item.risk_level)}`}>
                            {item.risk_level} ({item.score})
                          </span>
                        </div>
                        <p className="text-xs text-slate-400 leading-relaxed">
                          {item.reasoning}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-4">
                  <h3 className="text-base font-semibold text-white">Regulatory Citations & Governance Knowledge Base</h3>
                  <div className="space-y-3">
                    {assessment.citations.map((cite, idx) => (
                      <div key={idx} className="bg-slate-950 border border-slate-800 rounded-lg p-4 space-y-2">
                        <div className="flex flex-wrap justify-between items-center gap-2">
                          <span className="text-xs font-semibold text-blue-400">
                            {cite.source}
                          </span>
                          <span className="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded border border-slate-700">
                            {cite.source_type}
                          </span>
                        </div>
                        <p className="text-xs text-slate-300 italic">
                          "{cite.content}"
                        </p>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-4">
                  <h3 className="text-base font-semibold text-white">Mandatory Action Items</h3>
                  <ul className="space-y-2">
                    {assessment.mandatory_actions.map((action, i) => (
                      <li key={i} className="flex items-start gap-2.5 text-xs text-slate-300">
                        <span className="text-blue-500 font-bold">•</span>
                        <span>{action}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ) : (
              <div className="bg-slate-900/50 border border-dashed border-slate-800 rounded-xl p-12 text-center flex flex-col items-center justify-center min-h-[400px]">
                <p className="text-slate-400 text-sm">
                  Fill in the use case parameters on the left and click <strong className="text-slate-200">Run Risk Assessment</strong> to evaluate governance rules, privacy implications, and retrieve citations.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}