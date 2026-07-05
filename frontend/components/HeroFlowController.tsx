"use client";

import React, { useState } from 'react';
import IntakeView from './views/IntakeView';
import ProcessingView from './views/ProcessingView';
import DashboardView from './views/DashboardView';
import CopilotModal from './ui/CopilotModal';
import { IntakePayload, OrchestratorResponse } from './types';

export default function HeroFlowController() {
  const [currentStep, setCurrentStep] = useState<1 | 2 | 3>(1);
  const [intakeData, setIntakeData] = useState<IntakePayload | null>(null);
  const [resultsData, setResultsData] = useState<OrchestratorResponse | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const fetchResults = async (payload: IntakePayload) => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!response.ok) throw new Error('API failed');
      const data = await response.json();
      return data as OrchestratorResponse;
    } catch (e) {
      console.warn("API failed, using fallback data.");
      // Fallback mock data
      return {
        drugIntelligence: {
          baselineCost: "~$13,000",
          generic: {
            exists: true,
            name: "Palbociclib",
            estimatedSavings: "80%",
          }
        },
        liveGrants: [
          {
            id: '1',
            foundationName: "HealthWell Foundation",
            status: "OPEN",
            coverageDetails: `Up to $10,000/year for Medicare patients with ${payload.diagnosis}.`,
            applyUrl: "#"
          },
          {
            id: '2',
            foundationName: "Patient Advocate Foundation",
            status: "WAITLISTED",
            coverageDetails: "Currently accepting waitlist applications for next funding cycle.",
            applyUrl: "#"
          }
        ]
      } as OrchestratorResponse;
    }
  };

  const handleIntakeSubmit = async (data: IntakePayload) => {
    setIntakeData(data);
    setCurrentStep(2);
    
    // Simulate a minimum 8s delay to show the Processing view properly,
    // combined with the real API call.
    const startTime = Date.now();
    const results = await fetchResults(data);
    const elapsed = Date.now() - startTime;
    const minDelay = 8000; // 8 seconds minimum
    
    if (elapsed < minDelay) {
      await new Promise(resolve => setTimeout(resolve, minDelay - elapsed));
    }
    
    setResultsData(results);
    setCurrentStep(3);
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
