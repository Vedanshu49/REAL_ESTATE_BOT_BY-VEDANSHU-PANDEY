import React, { useState, useRef, useEffect } from 'react'
import { Send, Download, Loader, TrendingUp, Building2, MapPin, BarChart3, Sparkles, RefreshCw } from 'lucide-react'
import ChatMessage from './components/ChatMessage'
import EnhancedChart from './components/EnhancedChart'
import DataTable from './components/DataTable'
import { queryAnalysis, downloadData } from './api'

export default function App() {
  const [messages, setMessages] = useState([])
  const [inputValue, setInputValue] = useState('')
  const [loading, setLoading] = useState(false)
  const [currentData, setCurrentData] = useState(null)
  const messagesEndRef = useRef(null)
  const [stats, setStats] = useState(null)

  // Auto-scroll to latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!inputValue.trim()) return

    const userMessage = { role: 'user', content: inputValue }
    setMessages([...messages, userMessage])
    setInputValue('')
    setLoading(true)

    try {
      const response = await queryAnalysis(inputValue)
      const { summary, chartData, tableData, queryType } = response.data

      const botMessage = {
        role: 'bot',
        content: summary,
        chartData,
        tableData,
        queryType,
      }
      setMessages((prev) => [...prev, botMessage])
      setCurrentData({ chartData, tableData, query: inputValue, queryType })
      
      // Calculate stats for display
      if (tableData && tableData.length > 0) {
        const prices = tableData.map(t => parseFloat(t.price))
        setStats({
          count: tableData.length,
          avgPrice: (prices.reduce((a, b) => a + b, 0) / prices.length).toFixed(0),
          minPrice: Math.min(...prices).toFixed(0),
          maxPrice: Math.max(...prices).toFixed(0)
        })
      }
    } catch (error) {
      const errorMessage = {
        role: 'bot',
        content: `Error: ${error.response?.data?.error || error.message || 'Failed to process query'}`,
        isError: true,
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

  const quickQueries = [
    "Show all properties in Wakad",
    "Compare prices across locations",
    "What's the highest demand property?",
    "List properties with best ROI"
  ]

  const handleQuickQuery = (query) => {
    setInputValue(query)
  }

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 overflow-hidden">
      {/* Header - Premium */}
      <div className="bg-gradient-to-r from-blue-600 via-blue-500 to-cyan-500 text-white p-6 shadow-lg relative overflow-hidden flex-shrink-0">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-0 left-0 w-40 h-40 bg-white rounded-full blur-3xl"></div>
        </div>
        <div className="relative z-10">
          <div className="flex items-center gap-3 mb-2">
            <Sparkles className="w-8 h-8" />
            <h1 className="text-3xl font-bold">Real Estate AI</h1>
          </div>
          <p className="text-blue-100 text-sm">Integrated Gemini LLM | By: Vedanshu Pandey</p>
        </div>
      </div>

      {/* Main Content - Scrollable */}
      <div className="flex-1 overflow-y-auto scrollbar-thin scrollbar-thumb-slate-600 scrollbar-track-slate-900">
        <div className="max-w-7xl mx-auto">
          {/* Chat and Visualization - Side by Side on larger screens, stacked on smaller */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 p-6">
            
            {/* Left Column - Chat */}
            <div className="flex flex-col rounded-lg border border-slate-600 bg-slate-800 shadow-lg overflow-hidden">
              {/* Messages area */}
              <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-slate-800 max-h-96">
                {messages.length === 0 ? (
                  <div className="flex flex-col items-center justify-center h-full text-slate-300">
                    <Building2 className="w-16 h-16 text-blue-400 mb-4 opacity-50" />
                    <p className="text-lg font-semibold mb-2">Welcome to Real Estate AI</p>
                    <p className="text-sm text-slate-400 mb-6">Ask me anything about properties and I'll analyze the market</p>
                    
                    <div className="w-full space-y-2">
                      <p className="text-xs text-slate-500 font-semibold uppercase">Quick Queries</p>
                      {quickQueries.map((q, i) => (
                        <button
                          key={i}
                          onClick={() => handleQuickQuery(q)}
                          className="w-full text-left px-4 py-2 rounded-lg bg-slate-700 hover:bg-slate-600 text-slate-200 text-sm transition-all hover:translate-x-1"
                        >
                          • {q}
                        </button>
                      ))}
                    </div>
                  </div>
                ) : (
                  messages.map((msg, idx) => (
                    <ChatMessage key={idx} message={msg} />
                  ))
                )}
                {loading && (
                  <div className="flex items-center justify-center py-6 bg-slate-700 rounded-lg">
                    <Loader className="animate-spin text-blue-400 mr-3 w-5 h-5" />
                    <span className="text-slate-200">Analyzing market data...</span>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>

              {/* Input area */}
              <div className="border-t border-slate-700 p-5 bg-slate-800 flex-shrink-0">
                <form onSubmit={handleSubmit} className="flex gap-3">
                  <input
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    placeholder="Ask about properties..."
                    className="flex-1 px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition text-sm"
                    disabled={loading}
                  />
                  <button
                    type="submit"
                    disabled={loading}
                    className="bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 text-white px-4 py-3 rounded-lg flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl flex-shrink-0"
                  >
                    <Send size={18} />
                  </button>
                </form>
              </div>
            </div>

            {/* Right Column - Statistics */}
            {currentData && stats ? (
              <div className="flex flex-col gap-4">
                {/* Stats Grid */}
                <div className="grid grid-cols-2 gap-3">
                  <div className="bg-slate-800 rounded-lg p-4 border border-slate-600">
                    <div className="text-slate-400 text-xs font-semibold uppercase flex items-center gap-1">
                      <Building2 size={14} /> Properties
                    </div>
                    <p className="text-2xl font-bold text-white mt-2">{stats.count}</p>
                  </div>
                  <div className="bg-slate-800 rounded-lg p-4 border border-slate-600">
                    <div className="text-slate-400 text-xs font-semibold uppercase flex items-center gap-1">
                      <TrendingUp size={14} /> Avg Price
                    </div>
                    <p className="text-2xl font-bold text-green-400 mt-2">${stats.avgPrice}</p>
                  </div>
                  <div className="bg-slate-800 rounded-lg p-4 border border-slate-600">
                    <div className="text-slate-400 text-xs font-semibold uppercase">Min Price</div>
                    <p className="text-2xl font-bold text-blue-400 mt-2">${stats.minPrice}</p>
                  </div>
                  <div className="bg-slate-800 rounded-lg p-4 border border-slate-600">
                    <div className="text-slate-400 text-xs font-semibold uppercase">Max Price</div>
                    <p className="text-2xl font-bold text-purple-400 mt-2">${stats.maxPrice}</p>
                  </div>
                </div>

                {/* Download Button */}
                <button
                  onClick={handleDownload}
                  className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-green-600 to-emerald-500 hover:from-green-700 hover:to-emerald-600 text-white px-6 py-3 rounded-lg transition-all shadow-lg hover:shadow-xl font-semibold"
                >
                  <Download size={20} />
                  Export CSV
                </button>
              </div>
            ) : (
              <div className="flex items-center justify-center rounded-lg border border-slate-600 bg-slate-800 p-6">
                <div className="text-center text-slate-400">
                  <BarChart3 className="w-12 h-12 mx-auto mb-3 opacity-30" />
                  <p className="font-semibold">No data yet</p>
                  <p className="text-sm">Submit a query to see results</p>
                </div>
              </div>
            )}
          </div>

          {/* Full Width Visualization - Below chat */}
          {currentData ? (
            <div className="px-6 pb-6">
              {/* Chart */}
              <div className="mb-6 rounded-lg shadow-lg border border-slate-600 bg-slate-800 p-6">
                <div className="flex items-center gap-2 mb-4">
                  <BarChart3 className="w-5 h-5 text-blue-400" />
                  <h2 className="text-xl font-bold text-white">Market Visualization & Area Details</h2>
                </div>
                <EnhancedChart data={currentData.chartData} tableData={currentData.tableData} />
              </div>

              {/* Table */}
              <div className="rounded-lg shadow-lg border border-slate-600 bg-slate-800 p-6">
                <div className="flex items-center gap-2 mb-4">
                  <MapPin className="w-5 h-5 text-cyan-400" />
                  <h2 className="text-xl font-bold text-white">Property Details</h2>
                </div>
                <div className="overflow-x-auto">
                  <DataTable data={currentData.tableData} />
                </div>
              </div>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  )
}
