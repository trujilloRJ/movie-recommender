import React from 'react'

export default function Container({children}) {
  return (
    <div className='max-w-6xl mx-auto px-4'>
        {children}
    </div>
  )
}
