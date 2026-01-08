"use client"

import { useState } from "react"
import { Shield, Scan, Loader2, Brain, Cpu, Network, Sparkles } from "lucide-react"
import { Button } from "@/components/ui/button"
import { AnalysisResult } from "@/components/analysis-result"

interface AnalysisData {
  verdict: "REAL" | "FAKE"
  confidence: number
  riskLevel: "LOW" | "MEDIUM" | "HIGH"
  modelName: string
  verificationStatus: string
}

export function FakeNewsDetector() {
  const [newsText, setNewsText] = useState("")
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [result, setResult] = useState<AnalysisData | null>(null)

  const analyzeNews = async () => {
    if (!newsText.trim()) return

    setIsAnalyzing(true)
    setResult(null)

    try {
      const res = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: newsText }),
      })

      if (!res.ok) {
        throw new Error("Prediction API error")
      }

      const json = await res.json()

      const confidence = Math.round(Number(json.confidence) || 0)

      setResult({
        verdict: json.verdict === "FAKE" ? "FAKE" : "REAL",
        confidence,
        riskLevel: confidence > 90 ? "LOW" : confidence > 80 ? "MEDIUM" : "HIGH",
        modelName: json.modelName || "Sklearn TF-IDF + Classifier",
        verificationStatus: confidence > 80 ? "MODEL_CONFIDENT" : "MODEL_UNSURE",
      })
    } catch (err) {
      // Fallback behavior: keep the original local stub if server is unreachable
      console.error(err)
      await new Promise((resolve) => setTimeout(resolve, 1200))
      const isFake = Math.random() > 0.5
      const confidence = Math.floor(Math.random() * 20) + 80

      setResult({
        verdict: isFake ? "FAKE" : "REAL",
        confidence,
        riskLevel: confidence > 90 ? "LOW" : confidence > 80 ? "MEDIUM" : "HIGH",
        modelName: "Local Stub",
        verificationStatus: "OFFLINE_FALLBACK",
      })
    } finally {
      setIsAnalyzing(false)
    }
  }

  return (
    <div className="relative z-10 flex flex-col items-center justify-center min-h-screen px-4 py-12">
      <div className="absolute top-20 left-10 opacity-20 animate-float">
        <Network className="w-16 h-16 text-cyan-400" />
      </div>
      <div className="absolute top-40 right-16 opacity-20 animate-float" style={{ animationDelay: "1s" }}>
        <Cpu className="w-12 h-12 text-cyan-400" />
      </div>
      <div className="absolute bottom-32 left-20 opacity-20 animate-float" style={{ animationDelay: "2s" }}>
        <Brain className="w-14 h-14 text-cyan-400" />
      </div>

      <div className="text-center mb-10">
        <div className="flex items-center justify-center gap-3 mb-6">
          <div className="p-4 rounded-2xl bg-cyan-500/10 border border-cyan-500/20 shadow-neon-cyan animate-float">
            <Shield className="w-10 h-10 text-cyan-400" />
          </div>
        </div>
        <h1 className="text-4xl md:text-5xl font-extrabold text-foreground mb-3 tracking-tight font-sans">
          Fake News Detection
        </h1>
        <p className="text-muted-foreground text-lg font-serif flex items-center justify-center gap-2">
          <Sparkles className="w-5 h-5 text-cyan-400" />
          AI-Powered Neural Verification System
          <Sparkles className="w-5 h-5 text-cyan-400" />
        </p>
      </div>

      <div className="w-full max-w-2xl glass rounded-3xl p-8 md:p-10 shadow-heavy">
        <div className="flex flex-wrap items-center gap-3 mb-8">
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-500/20 shadow-heavy">
            <div className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
            <span className="text-cyan-400 text-sm font-semibold tracking-wide">ONLINE</span>
          </div>
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-secondary border border-border shadow-heavy">
            <Brain className="w-4 h-4 text-cyan-400" />
            <span className="text-muted-foreground text-sm font-semibold">Neural Network</span>
          </div>
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-secondary border border-border shadow-heavy">
            <Cpu className="w-4 h-4 text-cyan-400" />
            <span className="text-muted-foreground text-sm font-semibold">ML Engine</span>
          </div>
        </div>

        <div className="relative mb-8">
          <textarea
            value={newsText}
            onChange={(e) => setNewsText(e.target.value)}
            placeholder="Paste the news headline or article here for AI analysis…"
            className="w-full h-44 md:h-52 p-5 bg-input border border-border rounded-2xl text-foreground placeholder:text-muted-foreground resize-none focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-500/50 transition-all text-base font-serif shadow-heavy"
          />
          {isAnalyzing && (
            <div className="absolute inset-0 bg-input/50 rounded-2xl overflow-hidden pointer-events-none">
              <div className="absolute inset-x-0 h-1 bg-gradient-to-r from-transparent via-cyan-400 to-transparent animate-scan" />
            </div>
          )}
        </div>

        <Button
          onClick={analyzeNews}
          disabled={isAnalyzing || !newsText.trim()}
          className="w-full h-16 text-lg font-bold bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white border-0 rounded-2xl transition-all duration-300 shadow-heavy hover:shadow-neon-cyan disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:shadow-heavy"
        >
          {isAnalyzing ? (
            <>
              <Loader2 className="w-6 h-6 mr-3 animate-spin" />
              <span>Processing Neural Analysis...</span>
            </>
          ) : (
            <>
              <Scan className="w-6 h-6 mr-3" />
              <span>Analyze with AI</span>
            </>
          )}
        </Button>

        {result && <AnalysisResult data={result} />}
      </div>

      <p className="mt-10 text-center text-sm text-muted-foreground font-serif">
        Powered by Machine Learning • Educational AI System • Predictions are Probabilistic
      </p>
    </div>
  )
}
