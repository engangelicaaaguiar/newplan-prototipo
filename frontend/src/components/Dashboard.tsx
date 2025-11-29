import React from 'react'
import { useAppStore } from '../store'

export function Dashboard() {
  const user = useAppStore((state) => state.user)

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900">
          Bem-vindo ao Portal Saúde Mental NR1
        </h1>
        <p className="mt-2 text-gray-600">
          {user ? `Usuário: ${user.nome}` : 'Faça login para continuar'}
        </p>
      </div>
    </div>
  )
}
