// Utility functions
// Constants are imported from common/constants.js

/**
 * Debounce function execution
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} Debounced function
 */
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

/**
 * Throttle function execution
 * @param {Function} func - Function to throttle
 * @returns {Function} Throttled function
 */
function throttle(func) {
  let ticking = false;
  return function (...args) {
    if (!ticking) {
      window.requestAnimationFrame(() => {
        func(...args);
        ticking = false;
      });
      ticking = true;
    }
  };
}

/**
 * Check if screen is wide (desktop)
 * @returns {boolean}
 */
function isWideScreen() {
  return window.innerWidth > WIDE_SCREEN_BREAKPOINT;
}

/**
 * Check if screen is mobile
 * @returns {boolean}
 */
function isMobileScreen() {
  return window.innerWidth <= MOBILE_BREAKPOINT;
}

/**
 * Escape special regex characters
 * @param {string} string - String to escape
 * @returns {string} Escaped string
 */
function escapeRegex(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

/**
 * Format date string for display (locale-aware)
 * @param {string} dateString - ISO date string
 * @returns {string} Formatted date string
 */
function formatDate(dateString) {
  if (!dateString) return "";

  try {
    // Date-only values represent an editorial calendar date, not midnight UTC.
    const date = /^\d{4}-\d{2}-\d{2}$/.test(dateString)
      ? new Date(`${dateString}T12:00:00`)
      : new Date(dateString);
    const locale = document.documentElement.lang || "en";
    return new Intl.DateTimeFormat(locale, {
      month: "short",
      day: "numeric",
      year: "numeric",
    }).format(date);
  } catch (error) {
    console.error("Error formatting date:", error);
    return dateString;
  }
}

/**
 * Initialize module when DOM is ready
 * @param {Function} initFunction - Function to initialize
 */
function initOnReady(initFunction) {
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initFunction);
  } else {
    initFunction();
  }
}
