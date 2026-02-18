import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function ProtectedRoute({ children }) {
  const { token } = useAuth();

  // if not logged in → redirect
  if (!token) {
    return <Navigate to="/login" replace />;
  }

  // if logged in → allow page
  return children;
}
