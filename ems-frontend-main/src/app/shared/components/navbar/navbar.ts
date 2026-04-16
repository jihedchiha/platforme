import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { Router, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';
import { AuthService } from '../../../core/services/auth.service';
import { SalleService } from '../../../core/services/salle.service';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, DatePipe],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css',
})
export class NavbarComponent implements OnInit {

  currentDate = new Date();
  pageTitle   = 'EMS Management System';
  breadcrumb  = 'Vue générale du studio';
  
  salles = signal<any[]>([]); // Liste des studios pour le switcher

  // Injection publique pour accès dans le template (évite les lignes rouges)
  public auth = inject(AuthService);
  private salleService = inject(SalleService);
  private router = inject(Router);

  // Map route → titre + breadcrumb
  private readonly PAGE_MAP: Record<string, { title: string; bread: string }> = {
    '/dashboard':    { title: 'EMS Management System',  bread: 'Vue générale du studio'          },
    '/creneaux':     { title: 'Planning des Créneaux',   bread: 'Accueil / Créneaux'              },
    '/clients':      { title: 'Gestion des Clients',     bread: 'Accueil / Clients'               },
    '/abonnements':  { title: 'Abonnements',             bread: 'Accueil / Abonnements'           },
    '/ventes':       { title: 'Ventes & Paiements',      bread: 'Accueil / Ventes'                },
    '/rapports':     { title: 'Rapports & Statistiques', bread: 'Accueil / Rapports'              },
    '/parametres':   { title: 'Paramètres',              bread: 'Accueil / Paramètres'            },
    '/profile':      { title: 'Mon Profil',             bread: 'Accueil / Profil'                },
  };

  constructor() {}

  ngOnInit(): void {
    this.updateTitle(this.router.url);

    // Charger les salles uniquement pour le SuperAdmin
    if (this.auth.isSuperAdmin()) {
      this.loadAllSalles();
    }

    this.router.events
      .pipe(filter(e => e instanceof NavigationEnd))
      .subscribe((e: any) => this.updateTitle(e.urlAfterRedirects));
  }

  loadAllSalles() {
    this.salleService.getSalles().subscribe(data => {
      this.salles.set(data);
    });
  }

  onSalleChange(event: any) {
    const id = event.target.value;
    this.auth.setSelectedSalle(id);
    // Le branding changera automatiquement via l'effect() dans AppComponent
  }

  private updateTitle(url: string): void {
    const route = '/' + url.split('/')[1];
    const page  = this.PAGE_MAP[route];
    if (page) {
      this.pageTitle  = page.title;
      this.breadcrumb = page.bread;
    }
  }

  getInitials(): string {
    const user = this.auth.user();
    if (!user?.nom) return '';
    const parts = user.nom.split(' ');
    return (parts[0][0] + (parts[1]?.[0] || '')).toUpperCase();
  }

  logout() {
    this.auth.logout();
  }
}