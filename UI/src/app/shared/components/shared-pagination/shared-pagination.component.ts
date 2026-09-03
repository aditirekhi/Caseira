import { Component, input, output, OnChanges, SimpleChanges } from '@angular/core';
import { NgClass } from '@angular/common';
import { SharedButtonComponent } from '../shared-button/shared-button.component';

@Component({
  selector: 'shared-pagination',
  imports: [SharedButtonComponent, NgClass],
  templateUrl: './shared-pagination.component.html',
  styleUrl: './shared-pagination.component.css',
})
export class SharedPaginationComponent {
  totalPages = input<number>(0);
  currentPage = input<number>(1);

  selectedPage = output<number>();

  activePage: number = 1;

  ngOnChanges() {
    this.activePage = this.currentPage();
  }

  isPageActive(page: number): boolean {
    return this.activePage === page;
  }

  generatePaginationRange(): Array<number | string> {
    const totalPages = this.totalPages();

    if (totalPages <= 5) {
      return Array.from({ length: totalPages }, (_, index) => index + 1);
    }

    if (this.activePage <= 3) {
      return [1, 2, 3, '...', totalPages];
    }

    if (this.activePage >= totalPages - 2) {
      return [1, '...', totalPages - 2, totalPages - 1, totalPages];
    }

    return [
      1,
      '...',
      this.activePage - 1,
      this.activePage,
      this.activePage + 1,
      '...',
      totalPages,
    ];
  }

  selectPage(page: number): void {
    if (this.activePage == page) {
      return;
    }
    this.activePage = page;
    this.selectedPage.emit(page);
  }

  goToFirstPage(): void {
    this.activePage = 1;
    this.selectedPage.emit(this.activePage);
  }

  goToLastPage(): void {
    this.activePage = this.totalPages();
    this.selectedPage.emit(this.activePage);
  }

  goToPreviousPage(): void {
    if (this.activePage > 1) {
      this.activePage--;
      this.selectedPage.emit(this.activePage);
    }
  }

  goToNextPage(): void {
    if (this.activePage < this.totalPages()) {
      this.activePage++;
      this.selectedPage.emit(this.activePage);
    }
  }
}
