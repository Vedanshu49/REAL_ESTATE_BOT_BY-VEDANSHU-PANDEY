import React, { useState } from 'react'
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ComposedChart,
} from 'recharts'

export default function DataChart({ data }) {
  const [chartType, setChartType] = useState('composed')

  if (!data || data.length === 0) {
    return <p className="text-slate-400 text-center py-8">No data available for visualization</p>
  }

  // Ensure minimum height for chart
  const minChartHeight = Math.max(350, data.length * 40)

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-slate-900 border border-slate-700 rounded-lg p-3 shadow-lg">
          <p className="text-slate-300 text-sm font-semibold">{payload[0].payload.year || 'Data'}</p>
          {payload.map((entry, index) => (
            <p key={index} style={{ color: entry.color }} className="text-sm">
              {entry.name}: {typeof entry.value === 'number' ? (entry.name.includes('Price') ? `$${entry.value.toFixed(0)}` : entry.value.toFixed(0)) : entry.value}
            </p>
          ))}
        </div>
      )
    }
    return null
  }

  return (
    <div className="w-full h-full flex flex-col">
      {/* Chart Type Selector */}
      <div className="flex gap-2 mb-4 justify-end">
        <button
          onClick={() => setChartType('composed')}
          className={`px-3 py-1 rounded text-xs font-semibold transition ${
            chartType === 'composed'
              ? 'bg-blue-600 text-white'
              : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
          }`}
        >
          Line + Bar
        </button>
        <button
          onClick={() => setChartType('line')}
          className={`px-3 py-1 rounded text-xs font-semibold transition ${
            chartType === 'line'
              ? 'bg-blue-600 text-white'
              : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
          }`}
        >
          Line
        </button>
        <button
          onClick={() => setChartType('bar')}
          className={`px-3 py-1 rounded text-xs font-semibold transition ${
            chartType === 'bar'
              ? 'bg-blue-600 text-white'
              : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
          }`}
        >
          Bar
        </button>
      </div>

      {/* Charts Container - FIXED HEIGHT WITH VERTICAL SCROLL */}
      <div className="flex-1 flex flex-col overflow-y-auto overflow-x-hidden rounded-lg border border-slate-600 bg-slate-800 scrollbar-thin scrollbar-thumb-slate-600 scrollbar-track-slate-800" style={{ maxHeight: '500px', minHeight: '350px' }}>
        <div style={{ width: '100%', minHeight: '100%' }}>
          <ResponsiveContainer width="100%" height={400}>
          {chartType === 'line' ? (
            <LineChart 
              data={data} 
              margin={{ top: 20, right: 80, left: 80, bottom: 60 }}
            >
              <defs>
                <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.1}/>
                </linearGradient>
                <linearGradient id="colorDemand" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#06b6d4" stopOpacity={0.1}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
              <XAxis 
                dataKey="year" 
                stroke="#94a3b8"
                angle={-45}
                textAnchor="end"
                height={80}
              />
              <YAxis 
                yAxisId="left" 
                stroke="#94a3b8" 
                width={70} 
                label={{ value: 'Avg Price ($)', angle: -90, position: 'insideLeft', fill: '#94a3b8' }} 
              />
              <YAxis 
                yAxisId="right" 
                orientation="right" 
                stroke="#94a3b8" 
                width={70} 
                label={{ value: 'Avg Demand Score', angle: 90, position: 'insideRight', fill: '#94a3b8' }} 
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend wrapperStyle={{ paddingTop: '20px' }} />
              <Line 
                yAxisId="left" 
                type="monotone" 
                dataKey="avgPrice" 
                stroke="#3b82f6" 
                strokeWidth={3} 
                name="Avg Price" 
                dot={{ fill: '#3b82f6', r: 5 }} 
                activeDot={{ r: 7 }} 
              />
              <Line 
                yAxisId="right" 
                type="monotone" 
                dataKey="avgDemand" 
                stroke="#06b6d4" 
                strokeWidth={3} 
                name="Avg Demand" 
                dot={{ fill: '#06b6d4', r: 5 }} 
                activeDot={{ r: 7 }} 
              />
            </LineChart>
          ) : chartType === 'bar' ? (
            <BarChart 
              data={data} 
              margin={{ top: 20, right: 80, left: 80, bottom: 60 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
              <XAxis 
                dataKey="year" 
                stroke="#94a3b8"
                angle={-45}
                textAnchor="end"
                height={80}
              />
              <YAxis 
                yAxisId="left" 
                stroke="#94a3b8" 
                width={70}
                label={{ value: 'Avg Price ($)', angle: -90, position: 'insideLeft', fill: '#94a3b8' }}
              />
              <YAxis 
                yAxisId="right" 
                orientation="right" 
                stroke="#94a3b8" 
                width={70}
                label={{ value: 'Avg Demand Score', angle: 90, position: 'insideRight', fill: '#94a3b8' }}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend wrapperStyle={{ paddingTop: '20px' }} />
              <Bar yAxisId="left" dataKey="avgPrice" fill="#3b82f6" name="Avg Price" radius={[8, 8, 0, 0]} />
              <Bar yAxisId="right" dataKey="avgDemand" fill="#06b6d4" name="Avg Demand" radius={[8, 8, 0, 0]} />
            </BarChart>
          ) : (
            <ComposedChart 
              data={data} 
              margin={{ top: 20, right: 80, left: 80, bottom: 60 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
              <XAxis 
                dataKey="year" 
                stroke="#94a3b8"
                angle={-45}
                textAnchor="end"
                height={80}
              />
              <YAxis 
                yAxisId="left" 
                stroke="#94a3b8" 
                width={70}
                label={{ value: 'Avg Price ($)', angle: -90, position: 'insideLeft', fill: '#94a3b8' }}
              />
              <YAxis 
                yAxisId="right" 
                orientation="right" 
                stroke="#94a3b8" 
                width={70}
                label={{ value: 'Avg Demand Score', angle: 90, position: 'insideRight', fill: '#94a3b8' }}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend wrapperStyle={{ paddingTop: '20px' }} />
              <Bar yAxisId="left" dataKey="avgPrice" fill="#3b82f6" name="Avg Price" radius={[8, 8, 0, 0]} opacity={0.7} />
              <Line 
                yAxisId="right" 
                type="monotone" 
                dataKey="avgDemand" 
                stroke="#06b6d4" 
                strokeWidth={3} 
                name="Avg Demand" 
                dot={{ fill: '#06b6d4', r: 5 }} 
              />
            </ComposedChart>
          )}
        </ResponsiveContainer>
        </div>
      </div>
      
      {/* Scroll info */}
      <p className="text-xs text-slate-500 mt-2">📊 Scroll horizontally to view all data points</p>
    </div>
  )
}
