import React from 'react'

export default function Chip({rating}) {
  return (
    <span
        class="rounded-full text-gray-500 bg-gray-200 font-semibold text-sm flex align-center cursor-pointer active:bg-gray-300 transition duration-300 ease w-max"
    >
        <img class="rounded-full w-9 h-9 max-w-none object-cover" alt="A"
            src={process.env.PUBLIC_URL+"imdb_logo.png"} 
        />
        <span class="flex items-center px-3 py-2">
            {rating}
        </span>
    </span>
  )
}
