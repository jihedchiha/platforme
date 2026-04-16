import { Component, OnInit, inject, effect } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { SalleService } from './core/services/salle.service';
import { AuthService } from './core/services/auth.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  private salleService = inject(SalleService);
  private auth = inject(AuthService);

  constructor() {
    // 🔄 Réagir automatiquement au changement de salle pour mettre à jour le branding
    effect(() => {
      const salleId = this.auth.activeSalleId();
      if (this.auth.isLoggedIn() && salleId) {
        this.loadBranding();
      }
    });
  }

  ngOnInit(): void {
    // Le chargement initial est géré par l'effect() ci-dessus
  }

  private loadBranding(): void {
    this.salleService.getConfig().subscribe({
      next: (config) => {
        if (config.couleur_primaire) {
          document.documentElement.style.setProperty('--color-primary', config.couleur_primaire);
        }
        if (config.couleur_secondaire) {
          document.documentElement.style.setProperty('--color-secondary', config.couleur_secondaire);
        }
      },
      error: () => {
        // En cas d'erreur ou de salle non trouvée, l'UI garde ses couleurs par défaut
      }
    });
  }
}