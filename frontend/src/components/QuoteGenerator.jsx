import { useState } from 'react'

export default function QuoteGenerator({ parsedData, carriers, onGenerated, onBack, onCarrierAdded }) {
  const [selectedCarriers, setSelectedCarriers] = useState(carriers.map(c => c.id))
  const [editedData, setEditedData] = useState(parsedData)
  const [newCarrierName, setNewCarrierName] = useState('')
  const [newCarrierEmail, setNewCarrierEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleAddCarrier = async () => {
    if (!newCarrierName || !newCarrierEmail) {
      setError('Please fill in carrier name and email')
      return
    }

    try {
      const response = await fetch('http://localhost:8000/api/carriers', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: newCarrierName,
          email: newCarrierEmail
        })
      })

      if (response.ok) {
        setNewCarrierName('')
        setNewCarrierEmail('')
        onCarrierAdded()
      }
    } catch (err) {
      setError(`Error adding carrier: ${err.message}`)
    }
  }

  const handleGenerate = async () => {
    setLoading(true)
    setError('')

    try {
      const selected = carriers.filter(c => selectedCarriers.includes(c.id))

      const response = await fetch('http://localhost:8000/api/generate-quote-sheet', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          quote_data: editedData,
          carriers: selected,
          client_name: editedData.client_name || 'Quote'
        })
      })

      const data = await response.json()

      if (!data.success) {
        setError(data.error || 'Failed to generate quote')
        return
      }

      // Trigger download
      window.location.href = `http://localhost:8000${data.file_url}`
      onGenerated(data)
    } catch (err) {
      setError(`Error: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-800 mb-2">Step 2: Generate Quote Sheet</h2>
        <p className="text-gray-600">Review the parsed data, select carriers, and generate your quote sheet</p>
      </div>

      {/* Parsed Data Review */}
      <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Quote Details</h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="text-sm font-semibold text-gray-700">Origin City</label>
            <input
              type="text"
              value={editedData.origin_city}
              onChange={(e) => setEditedData({...editedData, origin_city: e.target.value})}
              className="w-full mt-1 px-3 py-2 border border-gray-300 rounded-lg"
            />
          </div>
          <div>
            <label className="text-sm font-semibold text-gray-700">Origin State</label>
            <input
              type="text"
              value={editedData.origin_state}
              onChange={(e) => setEditedData({...editedData, origin_state: e.target.value})}
              className="w-full mt-1 px-3 py-2 border border-gray-300 rounded-lg"
              maxLength="2"
            />
          </div>
          <div>
            <label className="text-sm font-semibold text-gray-700">Destination City</label>
            <input
              type="text"
              value={editedData.destination_city}
              onChange={(e) => setEditedData({...editedData, destination_city: e.target.value})}
              className="w-full mt-1 px-3 py-2 border border-gray-300 rounded-lg"
            />
          </div>
          <div>
            <label className="text-sm font-semibold text-gray-700">Destination State</label>
            <input
              type="text"
              value={editedData.destination_state}
              onChange={(e) => setEditedData({...editedData, destination_state: e.target.value})}
              className="w-full mt-1 px-3 py-2 border border-gray-300 rounded-lg"
              maxLength="2"
            />
          </div>
          <div>
            <label className="text-sm font-semibold text-gray-700">Equipment Type</label>
            <input
              type="text"
              value={editedData.equipment_type}
              onChange={(e) => setEditedData({...editedData, equipment_type: e.target.value})}
              className="w-full mt-1 px-3 py-2 border border-gray-300 rounded-lg"
            />
          </div>
          <div>
            <label className="text-sm font-semibold text-gray-700">Quantity</label>
            <input
              type="number"
              value={editedData.quantity}
              onChange={(e) => setEditedData({...editedData, quantity: parseInt(e.target.value)})}
              className="w-full mt-1 px-3 py-2 border border-gray-300 rounded-lg"
            />
          </div>
        </div>
      </div>

      {/* Carrier Selection */}
      <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Select Carriers</h3>
        <div className="space-y-2 mb-4">
          {carriers.map((carrier) => (
            <label key={carrier.id} className="flex items-center">
              <input
                type="checkbox"
                checked={selectedCarriers.includes(carrier.id)}
                onChange={(e) => {
                  if (e.target.checked) {
                    setSelectedCarriers([...selectedCarriers, carrier.id])
                  } else {
                    setSelectedCarriers(selectedCarriers.filter(id => id !== carrier.id))
                  }
                }}
                className="mr-3 w-4 h-4"
              />
              <span className="text-gray-700">{carrier.name} ({carrier.email})</span>
            </label>
          ))}
        </div>

        {/* Add New Carrier */}
        <div className="border-t pt-4">
          <h4 className="text-sm font-semibold text-gray-700 mb-2">Add New Carrier</h4>
          <div className="flex gap-2">
            <input
              type="text"
              value={newCarrierName}
              onChange={(e) => setNewCarrierName(e.target.value)}
              placeholder="Carrier name"
              className="flex-1 px-3 py-2 border border-gray-300 rounded-lg"
            />
            <input
              type="email"
              value={newCarrierEmail}
              onChange={(e) => setNewCarrierEmail(e.target.value)}
              placeholder="Email"
              className="flex-1 px-3 py-2 border border-gray-300 rounded-lg"
            />
            <button
              onClick={handleAddCarrier}
              className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
            >
              Add
            </button>
          </div>
        </div>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          {error}
        </div>
      )}

      {/* Buttons */}
      <div className="flex gap-4">
        <button
          onClick={onBack}
          className="flex-1 px-6 py-3 bg-gray-300 text-gray-800 font-semibold rounded-lg hover:bg-gray-400 transition-colors"
        >
          Back
        </button>
        <button
          onClick={handleGenerate}
          disabled={loading || selectedCarriers.length === 0}
          className="flex-1 px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition-colors"
        >
          {loading ? 'Generating...' : 'Generate & Download Excel'}
        </button>
      </div>
    </div>
  )
}
