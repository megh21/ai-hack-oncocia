"use client";

import React, { useState } from 'react';
import IntakeView from './views/IntakeView';
import ProcessingView from './views/ProcessingView';
import DashboardView from './views/DashboardView';
import CopilotModal from './ui/CopilotModal';
import { IntakePayload, IntakeResponse } from './types';

export default function HeroFlowController() {
  const [currentStep, setCurrentStep] = useState<1 | 2 | 3>(1);
  const [intakeData, setIntakeData] = useState<IntakePayload | null>(null);
  const [resultsData, setResultsData] = useState<IntakeResponse | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const BACKEND_URL = 'http://127.0.0.1:8000';

  const fetchResults = async (payload: IntakePayload): Promise<IntakeResponse | null> => {
    const response = await fetch(`${BACKEND_URL}/api/intake`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Backend returned ${response.status}: ${errorText}`);
    }
    const data = await response.json();
    return data as IntakeResponse;
  };

  const handleIntakeSubmit = async (data: IntakePayload) => {
    setIntakeData(data);
    setCurrentStep(2);
    
    const startTime = Date.now();
    try {
      const results = await fetchResults(data);
      const elapsed = Date.now() - startTime;
      const minDelay = 8000;
      if (elapsed < minDelay) {
        await new Promise(resolve => setTimeout(resolve, minDelay - elapsed));
      }
      if (results) {
        setResultsData(results);
        setCurrentStep(3);
      }
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : String(e);
      console.error("Backend error:", msg);
      alert(`Could not reach the backend. Make sure it is running at http://127.0.0.1:8000\n\nError: ${msg}`);
      setCurrentStep(1);
    }
  };

  const handleStartOver = () => {
    setCurrentStep(1);
    setIntakeData(null);
    setResultsData(null);
    setIsModalOpen(false);
  };

  return (
    <>
      {currentStep === 1 && <IntakeView onSubmit={handleIntakeSubmit} />}
      {currentStep === 2 && <ProcessingView />}
      {currentStep === 3 && resultsData && intakeData && (
        <DashboardView 
          intakeData={intakeData} 
          results={resultsData} 
          onStartOver={handleStartOver}
          onOpenCopilot={() => setIsModalOpen(true)}
        />
      )}
      
      <CopilotModal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
        intakeData={intakeData} 
      />
    </>
  );
}
