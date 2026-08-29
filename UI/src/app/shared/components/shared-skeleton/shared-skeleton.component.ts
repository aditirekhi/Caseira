import { ChangeDetectionStrategy, Component, input, inject } from '@angular/core';
import { Constants } from '../constants/constants';

@Component({
    selector: 'shared-skeleton',
    standalone: true,
    templateUrl: './shared-skeleton.component.html',
    styleUrl: './shared-skeleton.component.css',
    changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SharedSkeletonComponent {
    private constants: Constants = inject(Constants);
    skeletonType = input<(typeof this.constants.skeletonComponentConstants.SKELETON_TYPE[number])>('content');
    skeletonRowCount = input<number>(1);


    get placeholders(): number[] {
        return Array.from({ length: this.skeletonRowCount() });
    }

    private readonly skeletonTypes: string[] = ['recipe-card', 'recipe-row', 'content', 'sidebar-list'];
}