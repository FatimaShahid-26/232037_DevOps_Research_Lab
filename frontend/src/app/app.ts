import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { FEATURES } from './feature-schema';
import { Component, ChangeDetectorRef, inject } from '@angular/core';
import { PredictionService, PredictionResponse } from './prediction.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  fields = FEATURES;
  values: Record<string, number | null> = {};
  result: PredictionResponse | null = null;
  error = '';
  loading = false;

  // GitHub Pages is static. Only localhost can call our Flask API.
  staticDemo = !['localhost', '127.0.0.1'].includes(window.location.hostname);
  private api = inject(PredictionService);
  private cdr = inject(ChangeDetectorRef);

  constructor() {
    for (const field of this.fields) this.values[field.name] = null;
  }

  getForestDescription(label: string): string {
    if (label === 'Naturally regenerating forest') {
      return 'A forest that grows back mainly through natural processes.';
    }

    if (label === 'Primary forest') {
      return 'A naturally regenerated forest with little visible human disturbance.';
    }

    if (label === 'Planted/plantation forest') {
      return 'A forest established mainly by people through planting or seeding.';
    }

    return 'Forest classification information is unavailable.';
  }

  getPercentage(value: number): string {
    return (value * 100).toFixed(1) + '%';
  }

  
  getForestName(code: string): string {

    const forestNames: Record<string, string> = {
      '1': 'Naturally regenerating forest',
      '10': 'Primary forest',
      '20': 'Planted/plantation forest'
    };

    return forestNames[code] || 'Unknown forest type';
  }


  submit() {
    this.error = '';
    this.result = null;
    if (this.staticDemo) return;

    const payload: Record<string, number> = {};
    for (const field of this.fields) {
      const input = this.values[field.name];
      if (input === null || !Number.isFinite(Number(input))) {
        this.error = 'Please enter ' + field.label;
        return;
      }
      const number = Number(input);
      if (field.min !== undefined && number < field.min ||
          field.max !== undefined && number > field.max) {
        this.error = field.label + ' is outside the allowed range';
        return;
      }
      payload[field.name] = number;
    }

    this.loading = true;
    this.cdr.markForCheck();

    this.api.predict(payload).subscribe({
      next: (response) => {
        this.result = response;
        this.loading = false;
        this.cdr.markForCheck();
      },

      error: (error) => {
        console.error('Prediction error:', error);
        this.error = 'Prediction failed. Please try again.';
        this.loading = false;
        this.cdr.markForCheck();
      }
    });
  }
}
