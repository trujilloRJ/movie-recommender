import React from 'react'
import Chip from './Chip'

export default function Movie({movie}) {
    return (
        <div class="max-w-sm rounded overflow-hidden shadow-lg mx-auto">
            {/* <img class="w-full" src="/img/card-top.jpg" alt="Sunset in the mountains" /> */}
            <a href={`https://www.imdb.com/title/${movie.imdb_id}/`} target="_blank">
                <div class="px-6 py-4">
                    <div class="font-bold text-xl mb-2">{movie.original_title}</div>
                    <div class="flex flex-row justify-between items-center">
                        <Chip rating={movie.vote_average}/>
                        <div>
                            Year: <span className='font-bold text-yellow-600'>{movie.release_year}</span>
                        </div>
                    </div>
                    <p class="text-gray-700 text-base text-clamp mt-2 text-justify">
                        {movie.overview}
                    </p>
                </div>
            </a>
            <div class="px-6 pt-2 pb-4">
                {movie.genres.map(gen=>(
                    <span class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">#{gen}</span>
                ))}
            </div>
        </div>
    )
}
