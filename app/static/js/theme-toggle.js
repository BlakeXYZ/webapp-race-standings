/*!
 * Color mode toggler for Bootstrap's docs (https://getbootstrap.com/)
 * Copyright 2011-2024 The Bootstrap Authors
 * Licensed under the Creative Commons Attribution 3.0 Unported License.
 * https://getbootstrap.com/docs/5.3/customize/color-modes/
 * 
 */

(() => {
    'use strict'
  
    const getStoredTheme = () => localStorage.getItem('theme')
    const setStoredTheme = theme => localStorage.setItem('theme', theme)
    const checkbox = document.getElementById('daynight-checkbox');


    const getPreferredTheme = () => {
      const storedTheme = getStoredTheme()
      if (storedTheme) {
        return storedTheme
      }
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
    }
  
    const setTheme = theme => {
      if (theme === 'auto') {
        document.documentElement.setAttribute('data-bs-theme', (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'))
      } else {
        document.documentElement.setAttribute('data-bs-theme', theme)
      }
    }
  
    setTheme(getPreferredTheme())
  

    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
      const storedTheme = getStoredTheme()
      if (storedTheme !== 'light' && storedTheme !== 'dark') {
        setTheme(getPreferredTheme())
      }
    })


  
    checkbox.addEventListener('change', () => {
        const theme = checkbox.checked ? 'dark' : 'light';
        setTheme(theme);
        setStoredTheme(theme);
    });

    
    document.addEventListener('DOMContentLoaded', () => {
      const currentTheme = getPreferredTheme();
      checkbox.checked = currentTheme === 'dark';
    });
    

    document.documentElement.classList.add('no-transition');
    
    window.addEventListener('DOMContentLoaded', () => {
      setTimeout(() => {
          document.documentElement.classList.remove('no-transition');
      }, 50); // Small delay to ensure transitions remain disabled during load
    });

})()

  
