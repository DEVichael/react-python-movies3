import './App.css';
import { useEffect, useState } from "react";
import "milligram";
import MovieForm from "./MovieForm";
import MoviesList from "./MoviesList";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const API_URL = process.env.REACT_APP_API_URL;

function App() {
    const [movies, setMovies] = useState([]);
    const [addingMovie, setAddingMovie] = useState(false);

    useEffect(() => {
        const fetchMovies = async () => {
            const response = await fetch(`${API_URL}/movies`);
            if (response.ok) {
                const movies = await response.json();
                setMovies(movies);
            }
        };

        fetchMovies();
    }, [movies.length]);

    async function handleAddMovie(movie) {
        const response = await fetch(`${API_URL}/movies`, {
            method: 'POST',
            body: JSON.stringify(movie),
            headers: { 'Content-Type': 'application/json' }
        });

        if (response.ok) {
            setMovies([...movies, movie]);
            setAddingMovie(false);
            toast.success("Movie added");
        }
    }

    async function handleDeleteMovie(movie) {
        const ok = window.confirm(`Czy na pewno chcesz usunąć film "${movie.title}"?`);
        if (!ok) return;

        const response = await fetch(`${API_URL}/movies/${movie.id}`, {
            method: 'DELETE',
        });

        if (response.ok) {
            setMovies(movies.filter(m => m.id !== movie.id));
            toast.success("Movie deleted");
        }
    }

    return (
        <div className="container">
            <h1>My favourite movies to watch</h1>

            {movies.length === 0
                ? <p>No movies yet. Maybe add something?</p>
                : <MoviesList
                    movies={movies}
                    onDeleteMovie={handleDeleteMovie}
                />
            }

            {addingMovie
                ? <MovieForm
                    onMovieSubmit={handleAddMovie}
                    buttonLabel="Add a movie"
                />
                : <button onClick={() => setAddingMovie(true)}>Add a movie</button>
            }

            <ToastContainer position="top-right" />
        </div>
    );
}

export default App;
