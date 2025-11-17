import React, { useState, useEffect } from 'react'
import { Send, Download, Loader } from 'lucide-react'
import ChatMessage from './components/ChatMessage'
import DataChart from './components/DataChart'
import DataTable from './components/DataTable'
import { queryAnalysis, downloadData } from './api'

export default function App() {
  const [messages, setMessages] = useState([])
  const [inputValue, setInputValue] = useState('')
  const [loading, setLoading] = useState(false)
  const [currentData, setCurrentData] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!inputValue.trim()) return

    // Add user message
    const userMessage = { role: 'user', content: inputValue }
    setMessages([...messages, userMessage])
    setInputValue('')
    setLoading(true)

    try {
      const response = await queryAnalysis(inputValue)
      const { summary, chartData, tableData } = response.data

      // Add bot response
      const botMessage = {
        role: 'bot',
        content: summary,
        chartData,
        tableData,
      }
      setMessages((prev) => [...prev, botMessage])
      setCurrentData({ chartData, tableData, query: inputValue })
    } catch (error) {
      const errorMessage = {
        role: 'bot',
        content: `Error: ${error.response?.data?.error || error.message || 'Failed to process query'}`,
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const handleDownload = async () => {
    if (!currentData) {
      alert('No data to download. Please submit a query first.')
      return
    }

    try {
      const response = await downloadData(currentData.query)
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `real_estate_data_${Date.now()}.csv`)
      document.body.appendChild(link)
      link.click()
      link.parentElement.removeChild(link)
    } catch (error) {
      alert('Failed to download data: ' + error.message)
    }
  }

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Left sidebar - Chat */}
      <div className="w-1/2 flex flex-col border-r border-gray-200 bg-white">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-6 shadow-md">
          <h1 className="text-3xl font-bold">Real Estate Bot</h1>
          <p className="text-blue-100 text-sm mt-1">AI-Powered Property Analysis</p>
        </div>

        {/* Messages area */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.length === 0 ? (
            <div className="flex items-center justify-center h-full text-gray-400">
              <div className="text-center">
                <p className="text-lg font-semibold mb-2">Welcome to Real Estate Bot</p>
                <p className="text-sm">Ask me about properties in different locations</p>
                <p className="text-sm mt-2">Try: "Analyze Wakad" or "Compare demand trends"</p>
              </div>
            </div>
          ) : (
            messages.map((msg, idx) => (
              <ChatMessage key={idx} message={msg} />
            ))
          )}
          {loading && (
            <div className="flex items-center justify-center py-4">
              <Loader className="animate-spin text-blue-600 mr-2" size={20} />
              <span className="text-gray-600">Processing your query...</span>
            </div>
          )}
        </div>

        {/* Input area */}
        <div className="border-t border-gray-200 p-4 bg-white">
          <form onSubmit={handleSubmit} className="flex gap-2">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Ask about properties..."
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed transition"
            >
              <Send size={20} />
            </button>
          </form>
        </div>
      </div>

      {/* Right sidebar - Data visualization */}
      <div className="w-1/2 flex flex-col bg-gray-50 overflow-y-auto">
        {currentData ? (
          <>
            {/* Chart */}
            <div className="p-6 bg-white m-4 rounded-lg shadow-sm">
              <h2 className="text-xl font-bold mb-4 text-gray-800">Price & Demand Trends</h2>
              <DataChart data={currentData.chartData} />
            </div>

            {/* Table */}
            <div className="p-6 bg-white m-4 rounded-lg shadow-sm">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-bold text-gray-800">Property Data</h2>
                <button
                  onClick={handleDownload}
                  className="flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition"
                >
                  <Download size={18} />
                  Download CSV
                </button>
              </div>
              <DataTable data={currentData.tableData} />
            </div>
          </>
        ) : (
          <div className="flex items-center justify-center h-full text-gray-400">
            <div className="text-center">
              <p className="text-lg font-semibold">No data yet</p>
              <p className="text-sm">Submit a query to see visualizations</p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
