import React, { useEffect, useState } from 'react';

const statuses = [
  "Identifying generic alternatives via FDA databases...",
  "Calculating baseline costs...",
  "Scanning foundations for active grants...",
  "Compiling your customized dashboard..."
];

export default function ProcessingView() {
  const [statusIndex, setStatusIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setStatusIndex((prev) => (prev < statuses.length - 1 ? prev + 1 : prev));
    }, 3500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-[#F7F5F0] flex flex-col items-center justify-center relative overflow-hidden">
      <div className="absolute w-96 h-96 bg-[#7A8B76]/30 rounded-full blur-[100px] animate-pulse mix-blend-multiply"></div>
      <div className="absolute w-72 h-72 bg-[#D37B63]/20 rounded-full blur-[80px] animate-pulse -translate-x-10 mix-blend-multiply"></div>

      <div className="relative z-10 text-center max-w-2xl px-4">
        <div className="h-24 md:h-32 flex items-center justify-center">
          <p className="font-serif text-3xl md:text-4xl text-[#2C352A] leading-snug animate-fade-in-out">
            {statuses[statusIndex]}
          </p>
        </div>
        
        <p className="font-sans text-xl opacity-60 mt-8">
          This takes a few moments. We are searching carefully.
        </p>
      </div>
    </div>
  );
}
