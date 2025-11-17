import React, { useState } from 'react'
import { ChevronDown, ChevronUp, Search } from 'lucide-react'

export default function DataTable({ data }) {
  const [sortConfig, setSortConfig] = useState({ key: 'year', direction: 'desc' })
  const [currentPage, setCurrentPage] = useState(1)
  const [searchTerm, setSearchTerm] = useState('')
  const itemsPerPage = 10

  if (!data || data.length === 0) {
    return <p className="text-slate-400 text-center py-8">No data available for display</p>
  }

  // Filter data
  const filteredData = data.filter(row =>
    Object.values(row).some(val =>
      String(val).toLowerCase().includes(searchTerm.toLowerCase())
    )
  )

  // Sort data
  const sortedData = [...filteredData].sort((a, b) => {
    const aValue = a[sortConfig.key]
    const bValue = b[sortConfig.key]
    const direction = sortConfig.direction === 'asc' ? 1 : -1

    if (typeof aValue === 'string') {
      return aValue.localeCompare(bValue) * direction
    }
    return (aValue - bValue) * direction
  })

  // Paginate
  const totalPages = Math.ceil(sortedData.length / itemsPerPage)
  const startIdx = (currentPage - 1) * itemsPerPage
  const displayData = sortedData.slice(startIdx, startIdx + itemsPerPage)

  const handleSort = (key) => {
    setSortConfig({
      key,
      direction: sortConfig.key === key && sortConfig.direction === 'asc' ? 'desc' : 'asc',
    })
    setCurrentPage(1)
  }

  const SortIcon = ({ column }) => {
    if (sortConfig.key !== column) return <ChevronDown size={14} className="opacity-30" />
    return sortConfig.direction === 'asc' ? <ChevronUp size={14} /> : <ChevronDown size={14} />
  }

  const getValueColor = (key, value) => {
    if (key === 'price' && value > 5000000) return 'text-purple-400'
    if (key === 'price' && value > 3000000) return 'text-blue-400'
    if (key === 'demandScore' && value > 2500) return 'text-green-400'
    if (key === 'demandScore' && value > 1500) return 'text-cyan-400'
    return 'text-slate-200'
  }

  return (
    <div className="w-full h-full flex flex-col">
      {/* Search Bar */}
      <div className="mb-4 flex items-center gap-2 bg-slate-700 rounded-lg px-4 py-2 border border-slate-600">
        <Search size={18} className="text-slate-400" />
        <input
          type="text"
          placeholder="Search properties..."
          value={searchTerm}
          onChange={(e) => {
            setSearchTerm(e.target.value)
            setCurrentPage(1)
          }}
          className="flex-1 bg-transparent text-slate-200 placeholder-slate-500 focus:outline-none"
        />
      </div>

      {/* Table */}
      <div className="flex-1 overflow-x-auto overflow-y-auto rounded-lg border border-slate-600">
        <table className="w-full text-sm">
          <thead className="sticky top-0 bg-slate-700 border-b border-slate-600 z-10">
            <tr>
              {['location', 'type', 'price', 'pricePerSqft', 'area', 'year', 'demand', 'demandScore'].map((col) => (
                <th
                  key={col}
                  onClick={() => handleSort(col)}
                  className="px-4 py-3 text-left font-semibold text-slate-200 cursor-pointer hover:bg-slate-600 transition"
                >
                  <div className="flex items-center gap-1">
                    {col.charAt(0).toUpperCase() + col.slice(1).replace(/([A-Z])/g, ' $1')}
                    <SortIcon column={col} />
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {displayData.map((row, idx) => (
              <tr key={idx} className={`border-b border-slate-600 hover:bg-slate-700 transition ${idx % 2 === 0 ? 'bg-slate-800' : 'bg-slate-750'}`}>
                <td className="px-4 py-3 text-slate-300 font-medium">{row.location}</td>
                <td className="px-4 py-3 text-slate-400 capitalize">{row.type}</td>
                <td className={`px-4 py-3 font-semibold ${getValueColor('price', row.price)}`}>
                  ${row.price.toLocaleString()}
                </td>
                <td className="px-4 py-3 text-slate-400">{row.pricePerSqft ? `$${row.pricePerSqft.toFixed(2)}` : '-'}</td>
                <td className="px-4 py-3 text-slate-400">{row.area ? row.area.toLocaleString() : '-'}</td>
                <td className="px-4 py-3 text-slate-400">{row.year}</td>
                <td className="px-4 py-3 text-slate-400">{row.demand}</td>
                <td className={`px-4 py-3 font-semibold ${getValueColor('demandScore', row.demandScore)}`}>
                  {row.demandScore.toFixed(2)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div className="flex justify-between items-center mt-4 pt-4 border-t border-slate-600">
        <p className="text-sm text-slate-400">
          Showing {startIdx + 1} to {Math.min(startIdx + itemsPerPage, sortedData.length)} of {sortedData.length} properties
        </p>
        <div className="flex gap-2">
          <button
            onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
            disabled={currentPage === 1}
            className="px-3 py-1 bg-slate-700 border border-slate-600 rounded text-slate-300 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-slate-600 transition"
          >
            Previous
          </button>
          {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
            const page = i + Math.max(1, currentPage - 2)
            if (page > totalPages) return null
            return (
              <button
                key={page}
                onClick={() => setCurrentPage(page)}
                className={`px-3 py-1 rounded transition ${
                  currentPage === page
                    ? 'bg-gradient-to-r from-blue-600 to-cyan-500 text-white font-semibold'
                    : 'bg-slate-700 border border-slate-600 text-slate-300 hover:bg-slate-600'
                }`}
              >
                {page}
              </button>
            )
          })}
          <button
            onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
            disabled={currentPage === totalPages}
            className="px-3 py-1 bg-slate-700 border border-slate-600 rounded text-slate-300 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-slate-600 transition"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  )
}
