import React from 'react'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'

export default function DataChart({ data }) {
  if (!data || data.length === 0) {
    return <p className="text-gray-500 text-center py-8">No data available</p>
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data} margin={{ top: 5, right: 30, left: 0, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="year" />
        <YAxis yAxisId="left" label={{ value: 'Avg Price ($)', angle: -90, position: 'insideLeft' }} />
        <YAxis yAxisId="right" orientation="right" label={{ value: 'Avg Demand Score', angle: 90, position: 'insideRight' }} />
        <Tooltip />
        <Legend />
        <Line yAxisId="left" type="monotone" dataKey="avgPrice" stroke="#3b82f6" name="Avg Price" />
        <Line yAxisId="right" type="monotone" dataKey="avgDemand" stroke="#ef4444" name="Avg Demand" />
      </LineChart>
    </ResponsiveContainer>
  )
}
