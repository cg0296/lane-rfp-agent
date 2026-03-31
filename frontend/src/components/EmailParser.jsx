import { useState } from 'react'

export default function EmailParser({ onParsed }) {
  const [emailText, setEmailText] = useState('')
  const [clientName, setClientName] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleParse = async () => {
    if (!emailText.trim()) {
      setError('Please paste an email')
      return
    }

    setLoading(true)
    setError('')

    try {
      const response = await fetch('http://localhost:8000/api/parse-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email_text: emailText, client_name: clientName })
      })

      const data = await response.json()

      if (!data.success) {
        setError(data.error || 'Failed to parse email')
        return
      }

      onParsed(data.data)
    } catch (err) {
      setError(`Error: ${err.message}. Make sure backend is running on http://localhost:8000`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-800 mb-2">Step 1: Parse Email</h2>
        <p className="text-gray-600">Paste a client's freight quote request email below</p>
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Client Name (Optional)
          </label>
          <input
            type="text"
            value={clientName}
            onChange={(e) => setClientName(e.target.value)}
            placeholder="e.g., ABC Logistics"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Email Text
          </label>
          <textarea
            value={emailText}
            onChange={(e) => setEmailText(e.target.value)}
            placeholder="Paste your email here..."
            rows="10"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
          />
        </div>

        {error && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            {error}
          </div>
        )}

        <button
          onClick={handleParse}
          disabled={loading}
          className="w-full px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition-colors"
        >
          {loading ? 'Parsing...' : 'Parse Email'}
        </button>
      </div>

      {/* Sample email helper */}
      <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <p className="text-sm text-blue-900 font-semibold mb-2">Sample Email:</p>
        <code className="text-xs text-blue-800 whitespace-pre-wrap">
{`Hello Jillian & Michelle,

Could you please quote me for the following –

16x 53'
Los Angeles to Greenville, SC
Team Drivers and Solo
Loading- mid to end April
Insurance $250k per truck

All trucks need e-track throughout
Commodity is Production Equipment (lighting, audio, video etc)

Thanks,
John Smith`}
        </code>
        <button
          onClick={() => setEmailText(`Hello Jillian & Michelle,\n\nCould you please quote me for the following –\n\n16x 53'\nLos Angeles to Greenville, SC\nTeam Drivers and Solo\nLoading- mid to end April\nInsurance $250k per truck\n\nAll trucks need e-track throughout\nCommodity is Production Equipment (lighting, audio, video etc)\n\nThanks,\nJohn Smith`)}
          className="mt-2 text-xs px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Load Sample
        </button>
      </div>
    </div>
  )
}
