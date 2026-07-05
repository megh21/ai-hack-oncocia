import React from 'react';
import { OrchestratorResponse, IntakePayload } from '../types';

interface DashboardViewProps {
  intakeData: IntakePayload;
  results: OrchestratorResponse;
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
            {intakeData.drugName} <span className="opacity-70 text-4xl">({intakeData.dosage})</span>
          </h1>

          <div className="mb-16">
            <p className="text-xl opacity-70 uppercase tracking-widest mb-4">Baseline Wholesale Cost</p>
            <p className="font-serif text-6xl lg:text-7xl text-[#D37B63] mb-2">{results.drugIntelligence.baselineCost}</p>
            <p className="text-xl opacity-70">per month, before insurance</p>
          </div>

          {results.drugIntelligence.generic.exists && (
            <div className="border-l-4 border-[#D37B63] pl-6">
              <p className="text-2xl font-serif mb-2">Generic Available</p>
              <p className="text-xl opacity-80 leading-relaxed">
                The FDA-approved generic is {results.drugIntelligence.generic.name}. 
                {results.drugIntelligence.generic.estimatedSavings ? ` Generics can reduce out-of-pocket costs by up to ${results.drugIntelligence.generic.estimatedSavings}.` : ' Generics can significantly reduce out-of-pocket costs.'}
              </p>
            </div>
          )}
          {!results.drugIntelligence.generic.exists && (
             <div className="border-l-4 border-[#7A8B76] pl-6 opacity-70">
               <p className="text-2xl font-serif mb-2">No Generic Found</p>
               <p className="text-xl opacity-80 leading-relaxed">
                 There is currently no FDA-approved generic available.
               </p>
             </div>
          )}
        </div>
      </div>

      {/* RIGHT COLUMN: Grants */}
      <div className="w-full lg:w-7/12 bg-[#7A8B76] text-[#F7F5F0] p-8 lg:p-16 relative pb-48 lg:pb-32 min-h-[50vh]">
        <h2 className="font-serif text-4xl mb-16">Active Financial Relief</h2>

        <div className="flex flex-col gap-12">
          {results.liveGrants.map((grant) => (
            <div key={grant.id} className={`border-b border-[#F7F5F0]/20 pb-12 ${grant.status !== 'OPEN' ? 'opacity-60' : ''}`}>
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
                <h3 className="font-serif text-3xl">{grant.foundationName}</h3>
                <span className={`text-lg px-4 py-1 rounded-full uppercase tracking-wider w-max ${grant.status === 'OPEN' ? 'bg-[#2C352A] text-[#F7F5F0]' : 'border border-[#F7F5F0] text-[#F7F5F0]'}`}>
                  {grant.status === 'OPEN' ? 'Fund Open' : grant.status.toLowerCase()}
                </span>
              </div>
              <p className="text-xl opacity-90 max-w-lg leading-relaxed">
                {grant.coverageDetails}
              </p>
              {grant.status === 'OPEN' && grant.applyUrl && (
                <a href={grant.applyUrl} target="_blank" rel="noreferrer" className="mt-6 inline-block text-xl underline decoration-2 underline-offset-8 hover:text-[#2C352A] transition-colors">
                  Apply on their website ↗
                </a>
              )}
            </div>
          ))}
          {results.liveGrants.length === 0 && (
             <div className="opacity-80 text-2xl font-serif">
               No active grants found at this time.
             </div>
          )}
        </div>

        <div className="fixed lg:absolute bottom-0 left-0 w-full p-8 lg:p-16 bg-[#7A8B76]/90 backdrop-blur-md">
          <button onClick={onOpenCopilot} className="w-full bg-[#F7F5F0] text-[#2C352A] text-2xl font-sans px-8 py-6 rounded-2xl text-center hover:scale-[1.02] transition-transform shadow-2xl">
            Draft Medical Appeal Letter 🪄
          </button>
        </div>
      </div>
    </div>
  );
}
