import {useEffect, useState} from 'react'
import './App.css';
import Container from './components/Container';
import Movie from './components/Movie';
import SearchMovie from './components/SearchMovie';
import Separator from './components/Separator';

function App() {
  const [movieRecs, setMovieRecs] = useState([]);

  useEffect(() => {
    fetch('/get_recs').then(res => res.json()).then(data => {
      setMovieRecs([...data.recommendations]);
    });
  }, []);

  const fetchNewRecs = (searchTerm) => {
    searchTerm = encodeURIComponent(searchTerm)
    fetch(`/get_recs?film_name=${searchTerm}`).then(res => res.json()).then(data => {
      setMovieRecs([...data.recommendations]);
    });
  }

  return (
    <div className="pt-4">
      <Separator size={2} />
      <div className='flex justify-center items-center space-x-4'>
        <img class="w-12 h-12 max-w-none object-cover hidden md:block" alt="A"
            src={process.env.PUBLIC_URL+"movie_logo.svg"} 
        />
        <div className='headline'>Movie Recommender</div>
      </div>
      <Separator size={4} />
      <Container>
        <SearchMovie onSubmit={fetchNewRecs} />
        <Separator size={2} />
        <div className='grid grid-cols-1 gap-4 p-4 md:grid-cols-3 sm:grid-cols-2'>
          {movieRecs.length > 0 && movieRecs.map((movie)=>{
            return <Movie key={movie.original_title} movie={movie}/>
          })}
        </div>
      </Container>
    </div>
  );
}

export default App;
