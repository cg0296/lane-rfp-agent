import { useState, useEffect } from 'react'
import './App.css'
import EmailParser from './components/EmailParser'
import QuoteGenerator from './components/QuoteGenerator'

function App() {
  const [step, setStep] = useState('parse')
  const [parsedData, setParsedData] = useState(null)
  const [carriers, setCarriers] = useState([])

  useEffect(() => {
    fetchCarriers()
  }, [])

  const fetchCarriers = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/carriers')
      const data = await response.json()
      setCarriers(data)
    } catch (error) {
      console.error('Error fetching carriers:', error)
    }
  }

  const handleEmailParsed = (data) => {
    setParsedData(data)
    setStep('generate')
  }

  const handleQuoteGenerated = (data) => {
    setParsedData(null)
    setStep('parse')
    alert(`Quote generated! Downloading: ${data.filename}`)
  }

  const handleBack = () => {
    setStep('parse')
    setParsedData(null)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">Lane RFP Agent</h1>
          <p className="text-gray-600">Convert client emails into quote sheets instantly</p>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-8">
          {step === 'parse' ? (
            <EmailParser onParsed={handleEmailParsed} />
          ) : (
            <QuoteGenerator
              parsedData={parsedData}
              carriers={carriers}
              onGenerated={handleQuoteGenerated}
              onBack={handleBack}
              onCarrierAdded={() => fetchCarriers()}
            />
          )}
        </div>

        <div className="text-center mt-8 text-gray-600 text-sm">
          <p>Step {step === 'parse' ? '1' : '2'} of 2: {step === 'parse' ? 'Parse Email' : 'Generate Quote'}</p>
        </div>
      </div>
    </div>
  )
}

export default App
