import { createContext, useContext, useState, useEffect } from "react";
import api from "../api/axios";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [permissions, setPermissions] = useState([]);

  // login handler
  const login = (newToken) => {
    localStorage.setItem("token", newToken);
    setToken(newToken);
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setPermissions([]);
  };

  // 🔥 load user permissions
  useEffect(() => {
    if (!token) return;

    api.get("/issues/me")
      .then((res) => {
        setPermissions(res.data.permissions || []);
      })
      .catch(() => logout());
  }, [token]);

  return (
    <AuthContext.Provider value={{ token, permissions, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
