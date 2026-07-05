export interface IntakePayload {
  diagnosis: string;
  drugName: string;
  dosage: string;
}

export interface OrchestratorResponse {
  drugIntelligence: {
    baselineCost: string;
    generic: {
      exists: boolean;
      name: string | null;
      estimatedSavings: string | null;
    };
  };
  liveGrants: Array<{
    id: string;
    foundationName: string;
    status: 'OPEN' | 'WAITLISTED' | 'CLOSED';
    coverageDetails: string;
    applyUrl: string;
  }>;
}
