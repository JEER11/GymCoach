import './App.css';
import Footer from './components/footer/Footer';
import HeroSection from './components/hero-section/HeroSection';
import Join from './components/join/Join';
import Programs from './components/programs/Programs';

function App() {
  return (
    <div className="App">
      <HeroSection/>
      <Programs/>
      <Join/>
      <Footer/>
    </div>
  );
}

export default App;
