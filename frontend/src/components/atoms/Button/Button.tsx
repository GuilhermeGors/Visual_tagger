import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'danger' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  className = '',
  disabled,
  ...props
}) => {
  // Tailwind base classes for the button
  const baseClasses = 'font-semibold py-2 px-4 rounded-xl transition duration-300 ease-in-out focus:outline-none focus:ring-2 focus:ring-offset-2'; // Adicionado focus:ring-offset-2

  // Classes de variante
  const variantClasses = {
    primary: 'bg-primary text-white hover:bg-indigo-700 focus:ring-primary', // Cor mais escura no hover
    secondary: 'bg-secondary text-white hover:bg-purple-700 focus:ring-secondary', // Cor mais escura no hover
    danger: 'bg-red-500 text-white hover:bg-red-600 focus:ring-red-500',
    outline: 'bg-transparent border-2 border-primary text-primary hover:bg-primary hover:text-white focus:ring-primary',
  };

  // Classes de tamanho
  const sizeClasses = {
    sm: 'text-sm py-1.5 px-3', // Ajustado padding
    md: 'text-base py-2.5 px-5', // Ajustado padding
    lg: 'text-lg py-3.5 px-7', // Ajustado padding
  };

  // Classes de estado de carregamento/desabilitado
  const loadingClasses = isLoading || disabled ? 'opacity-60 cursor-not-allowed' : 'hover:scale-105 active:scale-95'; // Efeitos de escala no hover/click

  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${loadingClasses} ${className}`}
      disabled={isLoading || disabled}
      {...props}
    >
      {isLoading ? (
        <span className="flex items-center justify-center">
          <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Carregando...
        </span>
      ) : (
        children
      )}
    </button>
  );
};

export default Button;
