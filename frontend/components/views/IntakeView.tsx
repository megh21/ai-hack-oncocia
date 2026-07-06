import React, { useState } from 'react';
import { IntakePayload } from '../types';

interface IntakeViewProps {
  onSubmit: (data: IntakePayload) => void;
}

export default function IntakeView({ onSubmit }: IntakeViewProps) {
  const [diagnosis, setDiagnosis] = useState('');
  const [drug, setDrug] = useState('');
  const [dosage, setDosage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = () => {
    setIsSubmitting(true);
    setTimeout(() => {
      onSubmit({ diagnosis, drug, dosage });
    }, 500);
  };

  return (
    <div className="min-h-screen bg-[#F7F5F0] text-[#2C352A] p-8 md:p-16 flex flex-col justify-between relative overflow-hidden">
      <div className="w-full flex justify-between items-start mb-24 relative z-10">
        <span className="font-sans text-xl font-medium tracking-wide">🌸 OncoAccess</span>
        <span className="text-xl opacity-70">100% Free & Private</span>
      </div>

      <div className="max-w-4xl relative z-10">
        <h1 className="font-serif text-5xl md:text-7xl leading-tight mb-12 text-[#2C352A]">
          Find financial support and <br className="hidden md:block"/>
          alternatives for your medication.
        </h1>

        <div className="flex flex-col gap-8 w-full max-w-2xl font-sans text-2xl">
          <div className="flex flex-col md:flex-row md:items-end gap-2 md:gap-4">
            <span className="whitespace-nowrap">I was recently diagnosed with</span>
            <input 
              type="text" 
              placeholder="e.g., Breast Cancer"
              value={diagnosis}
              onChange={(e) => setDiagnosis(e.target.value)}
              className="bg-transparent border-b-2 border-[#2C352A]/20 focus:border-[#D37B63] text-3xl font-serif text-[#D37B63] placeholder:text-[#2C352A]/30 w-full py-2 outline-none transition-colors"
            />
          </div>

          <div className="flex flex-col md:flex-row md:items-end gap-2 md:gap-4">
            <span className="whitespace-nowrap">My doctor prescribed</span>
            <input 
              type="text" 
              placeholder="e.g., Ibrance"
              value={drug}
              onChange={(e) => setDrug(e.target.value)}
              className="bg-transparent border-b-2 border-[#2C352A]/20 focus:border-[#D37B63] text-3xl font-serif text-[#D37B63] placeholder:text-[#2C352A]/30 w-full py-2 outline-none transition-colors"
            />
          </div>

          <div className="flex flex-col md:flex-row md:items-end gap-2 md:gap-4">
            <span className="whitespace-nowrap">at a dosage of</span>
            <input 
              type="text" 
              placeholder="e.g., 125mg"
              value={dosage}
              onChange={(e) => setDosage(e.target.value)}
              className="bg-transparent border-b-2 border-[#2C352A]/20 focus:border-[#D37B63] text-3xl font-serif text-[#D37B63] placeholder:text-[#2C352A]/30 w-full py-2 outline-none transition-colors"
            />
          </div>
        </div>

        <div className="mt-16">
          <button 
            onClick={handleSubmit}
            disabled={!diagnosis || !drug || !dosage || isSubmitting}
            className="bg-[#2C352A] text-[#F7F5F0] text-2xl font-sans px-10 py-5 rounded-full hover:bg-[#D37B63] disabled:opacity-50 disabled:hover:bg-[#2C352A] transition-all duration-500"
          >
            {isSubmitting ? 'Initializing...' : 'Find My Options ↗'}
          </button>
        </div>
      </div>

      <div className="max-w-2xl font-sans text-xl opacity-50 mt-24 relative z-10">
        Estimates and educational data only. Not medical advice.
      </div>
    </div>
  );
}
