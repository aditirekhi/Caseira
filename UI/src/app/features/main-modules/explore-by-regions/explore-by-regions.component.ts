import { ChangeDetectorRef, ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { RegionsService } from '../../../core/services/regions.service';
import { FetchAllRegionsResponse } from '../../../shared/interfaces/regions.interface';
import { SharedToastNotificationService } from '../../../shared/components/shared-toast-notification/shared-toast-notification.service';
import { Constants } from '../../../shared/components/constants/constants';

@Component({
  selector: 'app-explore-by-regions',
  standalone: false,
  templateUrl: './explore-by-regions.component.html',
  styleUrl: './explore-by-regions.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ExploreByRegionsComponent {
  private changeDetection = inject(ChangeDetectorRef);
  private constants: Constants = inject(Constants);
  private sharedToastNotificationService = inject(SharedToastNotificationService);
  private regionsService: RegionsService = inject(RegionsService);

  regionsDetails: FetchAllRegionsResponse[] = [];

  ngOnInit() {
    this.fetchAllRegions();
  }

  fetchAllRegions() {
    this.regionsService.getAllRegions().subscribe({
      next: (response: FetchAllRegionsResponse[] | string) => {
        this.regionsDetails = response as FetchAllRegionsResponse[];
        this.changeDetection.detectChanges();
      },
      error: (error: any) => {
        this.sharedToastNotificationService.showNotification(this.constants.regionsConstants.UNABLE_TO_FETCH_REGIONS_ERROR_MESSAGE, 'error', 5000);
      }
    });
  }
}
