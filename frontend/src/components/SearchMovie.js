import React, { useState } from 'react'

export default function SearchMovie({onSubmit}) {
    const [searchTerm, setSearchTerm] = useState('')
    const [possibleMovies, setPossibleMovies] = useState([])

    const handleChange = (event) => {
        const term = event.target.value
        setSearchTerm(term);
        fetch(`/get_possible_movies?search_term=${term}`).then(res => res.json()).then(data => {
            setPossibleMovies([...data.possible_movies])
        });
    }

    const handleSubmit = (event) => {
        event.preventDefault();
        onSubmit(searchTerm)
    }

    const selectMovie = (mov) => {
        setSearchTerm(mov)
        setPossibleMovies([])
        onSubmit(mov)
    }

    return (
        <>
            <form onSubmit={handleSubmit}>   
                <label for="default-search" class="mb-2 text-sm font-medium text-gray-900 sr-only white:text-gray-300">Search</label>
                <div class="relative">
                    <div class="flex absolute inset-y-0 left-0 items-center pl-3 pointer-events-none">
                        <svg class="w-5 h-5 text-gray-500 white:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                    </div>
                    <input 
                        value={searchTerm}
                        onChange={handleChange}
                        type="search"
                        id="default-search" 
                        class="block p-4 pl-10 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 white:bg-gray-700 white:border-gray-600 white:placeholder-gray-400 white:text-white white:focus:ring-blue-500 white:focus:border-blue-500" 
                        placeholder="Search a movie that you like..." 
                        required />
                    <button 
                        type="submit" 
                        class="text-white absolute right-2.5 bottom-2.5 bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 white:bg-blue-600 white:hover:bg-blue-700 dark:focus:ring-blue-800"
                    >
                        Search
                    </button>
                </div>
            </form>
            {searchTerm !== '' && 
            <div className='absolute rounded-md bg-gray-700 px-6'>
                {possibleMovies.map(mov=>(
                    <div key={mov} className='py-2 text-white px-4 cursor-pointer' onClick={()=>selectMovie(mov)}>{mov}</div>
                ))}
            </div>}
        </>
    )
}
