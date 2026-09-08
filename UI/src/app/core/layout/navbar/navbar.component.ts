import { Component, ChangeDetectionStrategy, ChangeDetectorRef, inject } from '@angular/core';
import { debounceTime, distinctUntilChanged, Observable, of, Subject, switchMap } from 'rxjs';
import { SearchResult } from '../../../shared/interfaces/search.interface';
import { RouterLinkActive } from '@angular/router';
import { SharedButtonComponent } from '../../../shared/components/shared-button/shared-button.component';
import { MainModulesRoutingModule } from "../../../features/main-modules/main-modules-routing.module";
import { Constants } from '../../../shared/components/constants/constants';
import { MenuTab } from '../../../shared/interfaces/generic.interface';
import { FormsModule } from '@angular/forms';
import { SearchService } from '../../services/search.service';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [RouterLinkActive, FormsModule, SharedButtonComponent, MainModulesRoutingModule],
  templateUrl: './navbar.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  styleUrl: './navbar.component.css'
})
export class NavbarComponent {
  private changeDetection: ChangeDetectorRef = inject(ChangeDetectorRef);
  private searchService: SearchService = inject(SearchService);
  constants: Constants = inject(Constants);

  searchKeyword: string = '';
  searchResults: SearchResult[] = [];
  searchKeywordSubject$: Subject<string> = new Subject<string>();

  navbarMenuItems: MenuTab[] = [
    { label: 'Recipes', route: '/recipe/all' },
    { label: 'Ingredients', route: '/ingredients' },
    {
      label: 'Meal Kits', route: '/meal-kits'
    },
    { label: 'Regions', route: '/regions/all' },
    { label: 'Offers', route: '/offers' }
  ]

  public showNavMenu: boolean = false;

  toggleNavMenu(): void {
    this.showNavMenu = !this.showNavMenu;
  }

  closeNavMenu(): void {
    this.showNavMenu = false;
  }

  ngOnInit(): void {
    this.searchKeywordSubject$
      .pipe(
        debounceTime(300),
        distinctUntilChanged(),
        switchMap((keyword: string): Observable<SearchResult[] | string> => {
          if (!keyword) {
            return of([]);
          }
          return this.searchService.searchRecipesIngredients(keyword);
        })
      )
      .subscribe(results => {
        if (results && typeof results !== 'string' && Array.isArray(results)) {
          this.searchResults = results;
          this.changeDetection.markForCheck();
        }
      });
  }

  searchRecipeIngredient(): void {
    this.searchKeywordSubject$.next(this.searchKeyword.trim());
  }
}
