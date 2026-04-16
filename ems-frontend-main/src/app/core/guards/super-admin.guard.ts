import { inject } from '@angular/core'
import { CanActivateFn, Router } from '@angular/router'
import { AuthService } from '../services/auth.service'

/**
 * Guard : SuperAdmin seulement (Gestion de la plateforme)
 */
export const superAdminGuard: CanActivateFn = () => {
  const auth   = inject(AuthService)
  const router = inject(Router)

  if (auth.isSuperAdmin()) return true

  // Si l'utilisateur est connecté mais pas SuperAdmin, redirige vers dashboard
  if (auth.isLoggedIn()) {
    router.navigate(['/dashboard'])
  } else {
    router.navigate(['/'])
  }

  return false
}
