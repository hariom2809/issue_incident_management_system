import { useAuth } from "../context/AuthContext";

/**
 * Centralized permission helper
 * Usage:
 *   const { can } = usePermissions();
 *   if (can("create_incident")) { ... }
 */
export default function usePermissions() {
  const { permissions } = useAuth();

  // check single permission
  const can = (permission) => {
    return permissions.includes(permission);
  };

  // check multiple permissions (optional helper)
  const canAny = (permissionList) => {
    return permissionList.some((p) => permissions.includes(p));
  };

  return {
    permissions,
    can,
    canAny,
  };
}