import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import './App.css'
import TablaEstudiantes from './components/pure/TablaEstudiantes/TablaEstudiantes'

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path='/estudiantes' element={<TablaEstudiantes/>} />
        <Route path='/admin' element={<TablaEstudiantes/>} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
