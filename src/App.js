import './App.css';
import Footer from './components/footer/Footer';
import HeroSection from './components/hero-section/HeroSection';
import Programs from './components/programs/Programs';

function App() {
  return (
    <div className="App">
      <HeroSection/>
      <Programs/>
      <Footer/>
    </div>
  );
}

export default App;
