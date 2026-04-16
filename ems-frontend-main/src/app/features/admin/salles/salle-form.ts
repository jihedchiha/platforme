import { Component, Input, Output, EventEmitter, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { SalleService } from '../../../core/services/salle.service';
import { Salle } from '../../../core/services/auth.service';

@Component({
  selector: 'app-salle-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './salle-form.html',
  styleUrl: './salle-form.css'
})
export class SalleFormComponent implements OnInit {
  private fb = inject(FormBuilder);
  private salleService = inject(SalleService);

  @Input() salle: Salle | null = null;
  @Output() close = new EventEmitter<void>();
  @Output() saved = new EventEmitter<void>();

  salleForm: FormGroup;
  selectedFile: File | null = null;
  imagePreview: string | null = null;
  isSubmitting = false;

  constructor() {
    this.salleForm = this.fb.group({
      nom: ['', [Validators.required, Validators.minLength(3)]],
      couleur_primaire: ['#2563eb'],
      couleur_secondaire: ['#7c3aed'],
      pack_saas: ['starter', Validators.required],
      actif: [true]
    });
  }

  ngOnInit(): void {
    if (this.salle) {
      this.salleForm.patchValue({
        nom: this.salle.nom,
        couleur_primaire: this.salle.couleur || '#2563eb',
        pack_saas: 'pro', // Mocked
        actif: true
      });
      if (this.salle.logo) {
        this.imagePreview = this.salle.logo;
      }
    }
  }

  onFileSelected(event: any): void {
    const file = event.target.files[0];
    if (file) {
      this.selectedFile = file;
      const reader = new FileReader();
      reader.onload = () => {
        this.imagePreview = reader.result as string;
      };
      reader.readAsDataURL(file);
    }
  }

  submit(): void {
    if (this.salleForm.invalid) return;

    this.isSubmitting = true;
    const formData = new FormData();
    Object.keys(this.salleForm.value).forEach(key => {
      formData.append(key, this.salleForm.value[key]);
    });

    if (this.selectedFile) {
      formData.append('logo', this.selectedFile);
    }

    const request = this.salle 
      ? this.salleService.updateSalle(this.salle.id, formData)
      : this.salleService.createSalle(formData);

    request.subscribe({
      next: () => {
        this.isSubmitting = false;
        this.saved.emit();
      },
      error: (err) => {
        console.error('Erreur lors de la sauvegarde:', err);
        this.isSubmitting = false;
      }
    });
  }
}
