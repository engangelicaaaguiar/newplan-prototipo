import { create } from 'zustand'

interface AppState {
  user: any | null
  loading: boolean
  setUser: (user: any) => void
  setLoading: (loading: boolean) => void
  logout: () => void
}

export const useAppStore = create<AppState>((set) => ({
  user: null,
  loading: false,
  setUser: (user) => set({ user }),
  setLoading: (loading) => set({ loading }),
  logout: () => {
    set({ user: null })
    localStorage.removeItem('auth_token')
  },
}))
