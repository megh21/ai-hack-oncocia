import React, { useState } from 'react';
import { IntakePayload } from '../types';

interface CopilotModalProps {
  isOpen: boolean;
  onClose: () => void;
  intakeData: IntakePayload | null;
}

export default function CopilotModal({ isOpen, onClose, intakeData }: CopilotModalProps) {
  const [doctor, setDoctor] = useState('');
  const [insurance, setInsurance] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);

  if (!isOpen || !intakeData) return null;

  const handleGenerate = () => {
    setIsGenerating(true);
    // Simulate generation delay
    setTimeout(() => {
      setIsGenerating(false);
    }, 1000);
  };

  return (
    <div className="fixed inset-0 bg-[#2C352A]/40 backdrop-blur-md z-50 flex items-end animate-fade-in-up" style={{ animationDuration: '0.3s' }}>
      <div className="w-full h-[90vh] bg-[#F7F5F0] rounded-t-[40px] shadow-2xl overflow-hidden flex flex-col">
        {/* Header */}
        <div className="p-8 lg:px-16 flex justify-between items-center border-b border-[#2C352A]/10">
          <h2 className="font-serif text-3xl text-[#2C352A]">Letter of Medical Necessity</h2>
          <button onClick={onClose} className="text-2xl text-[#2C352A] opacity-60 hover:opacity-100 cursor-pointer">Close ✕</button>
        </div>

        <div className="flex flex-col lg:flex-row flex-1 overflow-hidden">
          {/* LEFT: Context Inputs */}
          <div className="w-full lg:w-1/3 p-8 lg:p-16 border-r border-[#2C352A]/10 bg-white/50 overflow-y-auto">
            <h3 className="font-serif text-2xl mb-8 text-[#2C352A]">Finalize the details</h3>
            
            <div className="mb-8">
              <label className="text-xl opacity-60 mb-2 block text-[#2C352A]">Prescribing Doctor</label>
              <input 
                type="text" 
                placeholder="Dr. Smith"
                value={doctor}
                onChange={e => setDoctor(e.target.value)}
                className="bg-transparent border-b-2 border-[#2C352A]/20 text-2xl text-[#2C352A] w-full py-2 outline-none focus:border-[#D37B63]"
              />
            </div>
            
            <div className="mb-12">
              <label className="text-xl opacity-60 mb-2 block text-[#2C352A]">Insurance Provider</label>
              <input 
                type="text" 
                placeholder="BlueCross"
                value={insurance}
                onChange={e => setInsurance(e.target.value)}
                className="bg-transparent border-b-2 border-[#2C352A]/20 text-2xl text-[#2C352A] w-full py-2 outline-none focus:border-[#D37B63]"
              />
            </div>

            {/*
            <button 
              onClick={handleGenerate}
              className="bg-[#D37B63] hover:bg-[#b56550] transition-colors text-[#F7F5F0] text-xl px-8 py-4 rounded-full w-full"
            >
              {isGenerating ? 'Updating...' : 'Generate Document'}
            </button>
            */}
          </div>

          {/* RIGHT: Document Preview */}
          <div className="w-full lg:w-2/3 p-8 lg:p-16 overflow-y-auto bg-[#F7F5F0] relative">
            <div className={`max-w-2xl mx-auto font-serif text-2xl leading-loose text-[#2C352A] transition-opacity duration-300 ${isGenerating ? 'opacity-30' : 'opacity-100'}`}>
              <p>Date: {new Date().toLocaleDateString()}</p>
              <br/>
              <p>To: Appeals Department, {insurance || '[Insurance Provider]'}</p>
              <p>From: {doctor || '[Prescribing Doctor]'}</p>
              <p>Subject: Letter of Medical Necessity</p>
              <br/>
              <p>
                This letter serves to document the medical necessity of <strong>{intakeData.drug}</strong> ({intakeData.dosage}) for the treatment of <strong>{intakeData.diagnosis}</strong>. 
                Given the current clinical guidelines and the patient's specific presentation, this therapy is essential and there are currently no appropriate alternatives that have proven effective for this specific clinical profile.
                
              <br/><br/>  
                This letter was drafted with the assistance of an AI-based patient navigation tool, using publicly available FDA labeling information only. 
                It does not constitute independent medical judgment, a diagnosis, or a treatment recommendation. 
                It must be reviewed, completed, and signed by the prescribing physician before submission to any insurer.
              <br/><br/>
              physicians signature: ___________________________  date: _______________
              <br/><br/>
              </p>
            </div>
            
            <div className="fixed lg:absolute bottom-8 right-8 lg:right-16 flex gap-6 z-10 bg-[#F7F5F0]/80 p-4 rounded-3xl backdrop-blur-md">
              <button 
                onClick={() => {
                  const text = `Date: ${new Date().toLocaleDateString()}\n\nTo: Appeals Department, ${insurance || '[Insurance Provider]'}\nFrom: ${doctor || '[Prescribing Doctor]'}\nSubject: Letter of Medical Necessity\n\nThis letter serves to document the medical necessity of ${intakeData.drug} (${intakeData.dosage}) for the treatment of ${intakeData.diagnosis}. Given the current clinical guidelines and the patient's specific presentation, this therapy is essential and there are currently no appropriate alternatives that have proven effective for this specific clinical profile.`;
                  navigator.clipboard.writeText(text);
                  alert("Letter copied to clipboard!");
                }}
                className="text-2xl text-[#2C352A] hover:text-[#D37B63] underline decoration-2 underline-offset-8 transition-colors"
              >
                Copy Text
              </button>
              <button 
                onClick={() => {
                  const printWindow = window.open('', '', 'width=800,height=800');
                  if (printWindow) {
                    printWindow.document.write(`
                      <html>
                        <head>
                          <title>Letter of Medical Necessity</title>
                          <style>
                            body { font-family: Georgia, serif; line-height: 1.8; padding: 40px; color: #000; font-size: 16px; }
                            .content { max-width: 800px; margin: 0 auto; }
                          </style>
                        </head>
                        <body>
                          <div class="content">
                            <p>Date: ${new Date().toLocaleDateString()}</p>
                            <br/>
                            <p>To: Appeals Department, ${insurance || '[Insurance Provider]'}</p>
                            <p>From: ${doctor || '[Prescribing Doctor]'}</p>
                            <p>Subject: Letter of Medical Necessity</p>
                            <br/>
                            <p>
                              This letter serves to document the medical necessity of <strong>${intakeData.drug}</strong> (${intakeData.dosage}) for the treatment of <strong>${intakeData.diagnosis}</strong>. 
                              Given the current clinical guidelines and the patient's specific presentation, this therapy is essential and there are currently no appropriate alternatives that have proven effective for this specific clinical profile.
                            </p>
                          </div>
                          <script>
                            window.onload = function() { window.print(); }
                          </script>
                        </body>
                      </html>
                    `);
                    printWindow.document.close();
                  }
                }}
                className="bg-[#2C352A] hover:bg-[#1a2019] transition-colors text-[#F7F5F0] text-2xl px-8 py-4 rounded-full shadow-lg"
              >
                Download PDF
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
