import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SalleService } from '../../../core/services/salle.service';
import { Salle } from '../../../core/services/auth.service';
import { SalleFormComponent } from './salle-form';

@Component({
  selector: 'app-salles-list',
  standalone: true,
  imports: [CommonModule, SalleFormComponent],
  templateUrl: './salles-list.html',
  styleUrl: './salles-list.css'
})
export class SallesListComponent implements OnInit {
  private salleService = inject(SalleService);

  salles = signal<Salle[]>([]);
  loading = signal<boolean>(true);
  showForm = signal<boolean>(false);
  selectedSalle = signal<Salle | null>(null);

  ngOnInit(): void {
    this.loadSalles();
  }

  loadSalles(): void {
    this.loading.set(true);
    this.salleService.getSalles().subscribe({
      next: (data) => {
        this.salles.set(data);
        this.loading.set(false);
      },
      error: () => this.loading.set(false)
    });
  }

  openCreateForm(): void {
    this.selectedSalle.set(null);
    this.showForm.set(true);
  }

  openEditForm(salle: Salle): void {
    this.selectedSalle.set(salle);
    this.showForm.set(true);
  }

  closeForm(): void {
    this.showForm.set(false);
    this.selectedSalle.set(null);
  }

  onFormSaved(): void {
    this.closeForm();
    this.loadSalles();
  }
}
