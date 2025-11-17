import React, { useState } from 'react'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ComposedChart, ScatterChart, Scatter } from 'recharts'
import { MapPin, TrendingUp } from 'lucide-react'

export default function EnhancedChart({ data, tableData }) {
  const [chartType, setChartType] = useState('composed')
  const [selectedArea, setSelectedArea] = useState(null)

  if (!data || data.length === 0) return <p className="text-slate-400 text-center py-8">No data available</p>

  const uniqueAreas = [...new Set(tableData?.map(p => p.location) || [])]
  const areaProperties = selectedArea ? tableData?.filter(p => p.location === selectedArea) || [] : []

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload?.length) {
      return (
        <div className="bg-slate-900 border border-slate-700 rounded-lg p-3 shadow-lg">
          <p className="text-slate-300 text-sm font-semibold">{payload[0].payload.year || 'Data'}</p>
          {payload.map((entry, idx) => (
            <p key={idx} style={{ color: entry.color }} className="text-sm">
              {entry.name}: {typeof entry.value === 'number' ? `${entry.name.includes('Price') ? '$' : ''}${entry.value.toFixed(0)}` : entry.value}
            </p>
          ))}
        </div>
      )
    }
    return null
  }

  const renderChart = () => {
    const chartProps = { margin: { top: 20, right: 80, left: 80, bottom: 60 } }
    
    if (chartType === 'line') {
      return (
        <LineChart data={data} {...chartProps}>
          <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
          <XAxis dataKey="year" stroke="#94a3b8" angle={-45} textAnchor="end" height={80} />
          <YAxis yAxisId="left" stroke="#94a3b8" width={70} />
          <YAxis yAxisId="right" orientation="right" stroke="#94a3b8" width={70} />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          <Line yAxisId="left" type="monotone" dataKey="avgPrice" stroke="#3b82f6" strokeWidth={3} name="Avg Price" dot={{ r: 5 }} />
          <Line yAxisId="right" type="monotone" dataKey="avgDemand" stroke="#06b6d4" strokeWidth={3} name="Avg Demand" dot={{ r: 5 }} />
        </LineChart>
      )
    } else if (chartType === 'bar') {
      return (
        <BarChart data={data} {...chartProps}>
          <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
          <XAxis dataKey="year" stroke="#94a3b8" angle={-45} textAnchor="end" height={80} />
          <YAxis yAxisId="left" stroke="#94a3b8" width={70} />
          <YAxis yAxisId="right" orientation="right" stroke="#94a3b8" width={70} />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          <Bar yAxisId="left" dataKey="avgPrice" fill="#3b82f6" name="Avg Price" radius={[8, 8, 0, 0]} />
          <Bar yAxisId="right" dataKey="avgDemand" fill="#06b6d4" name="Avg Demand" radius={[8, 8, 0, 0]} />
        </BarChart>
      )
    } else if (chartType === 'scatter') {
      return (
        <ScatterChart data={tableData} {...chartProps}>
          <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
          <XAxis dataKey="price" name="Price" stroke="#94a3b8" type="number" />
          <YAxis dataKey="demand_score" name="Demand" stroke="#94a3b8" type="number" />
          <Tooltip cursor={{ strokeDasharray: '3 3' }} content={<CustomTooltip />} />
          <Legend />
          <Scatter name="Properties" data={tableData} fill="#3b82f6" />
        </ScatterChart>
      )
    } else {
      return (
        <ComposedChart data={data} {...chartProps}>
          <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
          <XAxis dataKey="year" stroke="#94a3b8" angle={-45} textAnchor="end" height={80} />
          <YAxis yAxisId="left" stroke="#94a3b8" width={70} />
          <YAxis yAxisId="right" orientation="right" stroke="#94a3b8" width={70} />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          <Bar yAxisId="left" dataKey="avgPrice" fill="#3b82f6" name="Avg Price" radius={[8, 8, 0, 0]} opacity={0.7} />
          <Line yAxisId="right" type="monotone" dataKey="avgDemand" stroke="#06b6d4" strokeWidth={3} name="Avg Demand" dot={{ r: 5 }} />
        </ComposedChart>
      )
    }
  }

  return (
    <div className="w-full flex flex-col gap-4">
      <div className="flex gap-2 justify-end flex-wrap">
        {['composed', 'line', 'bar', 'scatter'].map(type => (
          <button
            key={type}
            onClick={() => setChartType(type)}
            className={`px-3 py-1 rounded text-xs font-semibold transition ${chartType === type ? 'bg-blue-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}
          >
            {type === 'composed' ? 'Line+Bar' : type.charAt(0).toUpperCase() + type.slice(1)}
          </button>
        ))}
      </div>

      <div className="flex gap-4 w-full">
        <div className="flex-[0.7] rounded-lg border border-slate-600 bg-slate-800 overflow-auto scrollbar-thin scrollbar-thumb-slate-600 scrollbar-track-slate-800" style={{ maxHeight: '500px', minHeight: '350px' }}>
          <div style={{ minWidth: '600px', padding: '20px' }}>
            <ResponsiveContainer width="100%" height={380}>
              {renderChart()}
            </ResponsiveContainer>
          </div>
        </div>

        <div className="flex-[0.3] flex flex-col gap-3">
          <div className="rounded-lg border border-slate-600 bg-slate-800 p-4 overflow-y-auto scrollbar-thin scrollbar-thumb-slate-600 scrollbar-track-slate-800" style={{ maxHeight: '250px' }}>
            <div className="flex items-center gap-2 mb-3">
              <MapPin className="w-4 h-4 text-cyan-400" />
              <h3 className="font-bold text-white text-sm">Areas ({uniqueAreas.length})</h3>
            </div>
            <div className="space-y-2">
              {uniqueAreas.map((area) => (
                <button
                  key={area}
                  onClick={() => setSelectedArea(selectedArea === area ? null : area)}
                  className={`w-full text-left px-3 py-2 rounded text-xs transition ${selectedArea === area ? 'bg-blue-600 text-white border border-blue-400' : 'bg-slate-700 text-slate-200 hover:bg-slate-600 border border-slate-600'}`}
                >
                  <div className="font-semibold">{area}</div>
                  <div className="text-xs opacity-75 mt-1">{tableData?.filter(p => p.location === area).length || 0} properties</div>
                </button>
              ))}
            </div>
          </div>

          {selectedArea && areaProperties.length > 0 && (
            <div className="rounded-lg border border-slate-600 bg-slate-800 p-4 overflow-y-auto scrollbar-thin scrollbar-thumb-slate-600 scrollbar-track-slate-800" style={{ maxHeight: '250px' }}>
              <div className="flex items-center gap-2 mb-3">
                <TrendingUp className="w-4 h-4 text-green-400" />
                <h3 className="font-bold text-white text-sm">{selectedArea}</h3>
              </div>
              <div className="space-y-3">
                <div className="bg-slate-700 rounded p-2 text-xs">
                  <div className="flex justify-between mb-1">
                    <span className="text-slate-300">Avg Price:</span>
                    <span className="text-green-400 font-semibold">${(areaProperties.reduce((sum, p) => sum + parseFloat(p.price || 0), 0) / areaProperties.length).toFixed(0)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-300">Avg Demand:</span>
                    <span className="text-blue-400 font-semibold">{(areaProperties.reduce((sum, p) => sum + parseFloat(p.demand_score || 0), 0) / areaProperties.length).toFixed(0)}</span>
                  </div>
                </div>

                <div>
                  <p className="text-xs font-semibold text-slate-400 mb-2">Properties:</p>
                  <div className="space-y-1 max-h-40 overflow-y-auto scrollbar-thin scrollbar-thumb-slate-600 scrollbar-track-slate-800">
                    {areaProperties.map((prop, idx) => (
                      <div key={idx} className="bg-slate-700 rounded p-2 text-xs border-l-2 border-cyan-500">
                        <div className="flex justify-between">
                          <div>
                            <div className="font-semibold text-white">{prop.location}</div>
                            <div className="text-slate-300 text-xs">Type: {prop.property_type}</div>
                          </div>
                          <div className="text-right">
                            <div className="text-green-400 font-semibold">${parseFloat(prop.price).toFixed(0)}</div>
                            <div className="text-blue-400 text-xs">D: {parseFloat(prop.demand_score).toFixed(0)}</div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      <p className="text-xs text-slate-500">📊 Select area to view properties</p>
    </div>
  )
}
