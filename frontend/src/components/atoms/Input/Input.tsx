import React from 'react';

// Define as propriedades (props) que o componente Input pode receber
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string; // Optional label for the input
  error?: string; // Mensagem de erro opcional
}

const Input: React.FC<InputProps> = ({ label, error, className = '', ...props }) => {
  const baseClasses = 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2';
  const errorClasses = error ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:ring-primary';

  return (
    <div className="mb-4">
      {label && (
        <label htmlFor={props.id || props.name} className="block text-gray-700 text-sm font-bold mb-2">
          {label}
        </label>
      )}
      <input
        className={`${baseClasses} ${errorClasses} ${className}`}
        {...props}
      />
      {error && (
        <p className="text-red-500 text-xs italic mt-1">{error}</p>
      )}
    </div>
  );
};

export default Input;
