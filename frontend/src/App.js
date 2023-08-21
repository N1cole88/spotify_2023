import logo from './logo.svg';
import './App.css';
import TopTracksForm from "./components/TopTracksForm.js";
import CurrentDate from './components/CurrentDate';
import TopSongsAnalysis from './pages/TopSongsAnalysis';
import { ThemeProvider, useTheme, createTheme } from '@mui/material/styles';
import { green, purple } from '@mui/material/colors';

function App() {
  const theme = createTheme({
    palette: {
      primary: {
        main: purple[500],
      },
      secondary: {
        main: green[500],
      },
    },
  });

  return (
    <ThemeProvider theme={theme}>
      <div>
        <CurrentDate  />
        <TopSongsAnalysis />
      </div>
    </ThemeProvider>
    
  );
}

export default App;
