import React from 'react';
import { IntakeResponse, IntakePayload } from '../types';

interface DashboardViewProps {
  intakeData: IntakePayload;
  results: IntakeResponse;
  onStartOver: () => void;
  onOpenCopilot: () => void;
}

export default function DashboardView({ intakeData, results, onStartOver, onOpenCopilot }: DashboardViewProps) {
  return (
    <div className="min-h-screen flex flex-col lg:flex-row w-full font-sans animate-fade-in-up">
      {/* LEFT COLUMN: Drug Data */}
      <div className="w-full lg:w-5/12 bg-[#F7F5F0] text-[#2C352A] p-8 lg:p-16 flex flex-col justify-between">
        <div>
          <button onClick={onStartOver} className="text-xl opacity-60 hover:opacity-100 transition-opacity mb-16 flex items-center gap-2">
            <span>&larr;</span> Start Over
          </button>
          
          <p className="text-2xl mb-2">Options for</p>
          <h1 className="font-serif text-5xl lg:text-6xl mb-16">
            {intakeData.drug} <span className="opacity-70 text-4xl">({intakeData.dosage})</span>
          </h1>

          <div className="mb-16">
            <p className="text-xl opacity-70 uppercase tracking-widest mb-4">Baseline Wholesale Cost</p>
            <p className="font-serif text-6xl lg:text-7xl text-[#D37B63] mb-2">
              {results.data.clinical_analysis.medicare_cost_per_claim ? `$${results.data.clinical_analysis.medicare_cost_per_claim}` : 'N/A'}
            </p>
            <p className="text-xl opacity-70">per Medicare claim average</p>
          </div>

          {results.data.clinical_analysis.generic_name && (
            <div className="border-l-4 border-[#D37B63] pl-6">
              <p className="text-2xl font-serif mb-2">Generic Available</p>
              <p className="text-xl opacity-80 leading-relaxed mb-4">
                The FDA-approved generic is <strong>{results.data.clinical_analysis.generic_name}</strong>. 
                Generics can significantly reduce out-of-pocket costs.
              </p>
            </div>
          )}
          {!results.data.clinical_analysis.generic_name && (
             <div className="border-l-4 border-[#7A8B76] pl-6 opacity-70">
               <p className="text-2xl font-serif mb-2">No Generic Found</p>
               <p className="text-xl opacity-80 leading-relaxed mb-4">
                 There is currently no FDA-approved generic available in our database.
               </p>
             </div>
          )}
          <div className="mt-8 opacity-80 text-lg leading-relaxed bg-[#2C352A]/5 p-6 rounded-lg">
             <p className="font-medium mb-2">Clinical Summary:</p>
             {results.data.clinical_analysis.summary}
          </div>
        </div>
      </div>

      {/* RIGHT COLUMN: Grants */}
      <div className="w-full lg:w-7/12 bg-[#7A8B76] text-[#F7F5F0] p-8 lg:p-16 relative pb-48 lg:pb-32 min-h-[50vh]">
        <h2 className="font-serif text-4xl mb-16">Active Financial Relief</h2>

        <div className="flex flex-col gap-12">
          {results.data.grant_navigation.human_readable_summary && (
            <p className="text-xl opacity-90 leading-relaxed italic border-l-2 border-[#F7F5F0] pl-4 mb-4">
              {results.data.grant_navigation.human_readable_summary}
            </p>
          )}
          {results.data.grant_navigation.recommended_funds.map((grant, idx) => (
            <div key={idx} className={`border-b border-[#F7F5F0]/20 pb-12`}>
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
                <h3 className="font-serif text-3xl">{grant.foundation}</h3>
                <span className={`text-lg px-4 py-1 rounded-full uppercase tracking-wider w-max bg-[#2C352A] text-[#F7F5F0]`}>
                  Fund Open
                </span>
              </div>
              <div className="text-xl opacity-90 max-w-lg leading-relaxed">
                <p className="mb-2 font-medium">Requirements:</p>
                <ul className="list-disc pl-6 space-y-2">
                  {grant.requirements.map((req, rIdx) => (
                    <li key={rIdx}>{req}</li>
                  ))}
                </ul>
              </div>
              {grant.url && (
                <a href={grant.url} target="_blank" rel="noreferrer" className="mt-6 inline-block text-xl underline decoration-2 underline-offset-8 hover:text-[#2C352A] transition-colors">
                  Apply on their website ↗
                </a>
              )}
            </div>
          ))}
          {results.data.grant_navigation.recommended_funds.length === 0 && (
             <div className="opacity-80 text-2xl font-serif">
               No active grants found at this time.
             </div>
          )}
        </div>

        {results.data.grant_navigation.recommended_funds.length > 0 && (
          <div className="fixed lg:absolute bottom-0 left-0 w-full p-8 lg:p-16 bg-[#7A8B76]/90 backdrop-blur-md">
            <button onClick={onOpenCopilot} className="w-full bg-[#F7F5F0] text-[#2C352A] text-2xl font-sans px-8 py-6 rounded-2xl text-center hover:scale-[1.02] transition-transform shadow-2xl">
              Draft Medical Appeal Letter 🪄
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
