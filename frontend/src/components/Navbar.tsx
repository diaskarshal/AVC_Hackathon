import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Navbar.css';

const Navbar: React.FC = () => {
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname === path ? 'active' : '';
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          🏗️ BuildFlow
        </Link>
        <ul className="navbar-menu">
          <li>
            <Link to="/" className={isActive('/')}>
              Dashboard
            </Link>
          </li>
          <li>
            <Link to="/projects" className={isActive('/projects')}>
              Projects
            </Link>
          </li>
          <li>
            <Link to="/tasks" className={isActive('/tasks')}>
              Tasks
            </Link>
          </li>
          <li>
            <Link to="/resources" className={isActive('/resources')}>
              Resources
            </Link>
          </li>
          <li>
            <Link to="/budgets" className={isActive('/budgets')}>
              Budgets
            </Link>
          </li>
          <li>
            <Link to="/import" className={isActive('/import')}>
              Import
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;