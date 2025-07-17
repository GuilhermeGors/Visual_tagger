import React from 'react';
import './index.css'; // Make sure Tailwind CSS is imported
import VisualTaggerModule from './components/organisms/VisualTaggerModule/VisualTaggerModule'; // Caminho direto

const App: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4 font-inter">
      <VisualTaggerModule />
    </div>
  );
}

export default App;
