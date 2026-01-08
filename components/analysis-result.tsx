"use client"

import { CheckCircle2, XCircle, AlertTriangle, Brain, Activity, Zap, Network } from "lucide-react"

interface AnalysisData {
  verdict: "REAL" | "FAKE"
  confidence: number
  riskLevel: "LOW" | "MEDIUM" | "HIGH"
  modelName: string
  verificationStatus: string
}

interface AnalysisResultProps {
  data: AnalysisData
}

export function AnalysisResult({ data }: AnalysisResultProps) {
  const isReal = data.verdict === "REAL"

  return (
    <div className="mt-10 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex items-center gap-4 mb-8">
        <div className="flex-1 h-px bg-gradient-to-r from-transparent via-cyan-500/30 to-transparent" />
        <div className="flex items-center gap-2 px-4 py-2 rounded-full bg-secondary border border-border shadow-heavy">
          <Zap className="w-4 h-4 text-cyan-400" />
          <span className="text-xs text-cyan-400 font-bold uppercase tracking-wider">Analysis Complete</span>
        </div>
        <div className="flex-1 h-px bg-gradient-to-r from-transparent via-cyan-500/30 to-transparent" />
      </div>

      <div className="flex justify-center mb-8">
        <div
          className={`flex items-center gap-4 px-10 py-5 rounded-3xl border-2 ${
            isReal
              ? "bg-green-500/10 border-green-500/40 shadow-neon-green"
              : "bg-red-500/10 border-red-500/40 shadow-neon-red"
          }`}
        >
          {isReal ? (
            <CheckCircle2 className="w-10 h-10 text-green-400" />
          ) : (
            <XCircle className="w-10 h-10 text-red-400" />
          )}
          <span className={`text-4xl font-extrabold tracking-wider ${isReal ? "text-green-400" : "text-red-400"}`}>
            {data.verdict}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-5">
        {/* Confidence */}
        <div className="p-5 rounded-2xl bg-secondary/60 border border-border shadow-heavy">
          <div className="flex items-center gap-2 mb-3">
            <Activity className="w-5 h-5 text-cyan-400" />
            <span className="text-xs text-muted-foreground font-bold uppercase tracking-wider">Confidence</span>
          </div>
          <span className="text-4xl font-extrabold text-foreground">{data.confidence}%</span>
        </div>

        {/* Risk Level */}
        <div className="p-5 rounded-2xl bg-secondary/60 border border-border shadow-heavy">
          <div className="flex items-center gap-2 mb-3">
            <AlertTriangle className="w-5 h-5 text-cyan-400" />
            <span className="text-xs text-muted-foreground font-bold uppercase tracking-wider">Risk Level</span>
          </div>
          <span
            className={`text-3xl font-extrabold ${
              data.riskLevel === "LOW"
                ? "text-green-400"
                : data.riskLevel === "MEDIUM"
                  ? "text-yellow-400"
                  : "text-red-400"
            }`}
          >
            {data.riskLevel}
          </span>
        </div>

        {/* Model Name */}
        <div className="p-5 rounded-2xl bg-secondary/60 border border-border shadow-heavy">
          <div className="flex items-center gap-2 mb-3">
            <Brain className="w-5 h-5 text-cyan-400" />
            <span className="text-xs text-muted-foreground font-bold uppercase tracking-wider">ML Model</span>
          </div>
          <span className="text-base font-semibold text-foreground font-serif">{data.modelName}</span>
        </div>

        {/* Verification Status */}
        <div className="p-5 rounded-2xl bg-secondary/60 border border-border shadow-heavy">
          <div className="flex items-center gap-2 mb-3">
            <Network className="w-5 h-5 text-cyan-400" />
            <span className="text-xs text-muted-foreground font-bold uppercase tracking-wider">Status</span>
          </div>
          <span className="text-base font-bold text-cyan-400">{data.verificationStatus}</span>
        </div>
      </div>
    </div>
  )
}
