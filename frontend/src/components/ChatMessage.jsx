import React, { useState } from 'react'
import { User, Bot, Sparkles, AlertCircle } from 'lucide-react'

export default function ChatMessage({ message }) {
  const isUser = message.role === 'user'
  const [isExpanded, setIsExpanded] = useState(false)

  if (message.isError) {
    return (
      <div className="flex gap-3">
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-red-600 flex items-center justify-center">
          <AlertCircle size={20} className="text-white" />
        </div>
        <div className="bg-red-900 bg-opacity-30 border border-red-700 text-red-300 rounded-lg px-4 py-3 rounded-bl-none max-w-lg">
          <p className="text-sm">{message.content}</p>
        </div>
      </div>
    )
  }

  return (
    <div className={`flex gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {!isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center shadow-lg">
          <Sparkles size={18} className="text-white" />
        </div>
      )}
      <div
        className={`max-w-xs lg:max-w-md xl:max-w-lg px-4 py-3 rounded-lg transition-all ${
          isUser
            ? 'bg-gradient-to-r from-blue-600 to-cyan-500 text-white rounded-br-none shadow-lg'
            : 'bg-slate-700 text-slate-50 rounded-bl-none border border-slate-600 cursor-pointer hover:bg-slate-600 transition'
        }`}
        onClick={() => !isUser && setIsExpanded(!isExpanded)}
      >
        <p className={`text-sm whitespace-pre-wrap break-words leading-relaxed ${!isUser && isExpanded ? '' : 'line-clamp-3'}`}>
          {message.content}
        </p>
        {!isUser && message.content.length > 200 && (
          <p className="text-xs text-slate-400 mt-2 italic">
            {isExpanded ? 'Click to collapse' : 'Click to expand full analysis'}
          </p>
        )}
      </div>
      {isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-slate-400 to-slate-600 flex items-center justify-center shadow-lg">
          <User size={18} className="text-white" />
        </div>
      )}
    </div>
  )
}
