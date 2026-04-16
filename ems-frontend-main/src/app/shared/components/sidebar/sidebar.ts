import { Component, inject } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { CommonModule } from '@angular/common'; // ✅ AJOUT ICI
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive], // ✅ AJOUT ICI
  templateUrl: './sidebar.html',
  styleUrl: './sidebar.css',
})
export class Sidebar {
  private auth = inject(AuthService);

  isAdmin(): boolean {
    return this.auth.isAdmin();
  }

  isSuperAdmin(): boolean {
    return this.auth.isSuperAdmin();
  }

  isPersonnel(): boolean {
    return this.auth.isPersonnel();
  }

  isStudioUser(): boolean {
    return this.isAdmin() || this.isPersonnel();
  }

  menuOpen = false;

  toggleMenu(): void {
    this.menuOpen = !this.menuOpen;
  }

  closeMenu(): void {
    this.menuOpen = false;
  }
}